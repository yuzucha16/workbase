# /// script
# requires-python = "==3.13.*"
# dependencies = []
# ///
"""pptxtext: pptx の「見えている文章と図解」を markdown に取り出す（標準ライブラリだけ。v0）。

AI に読ませる用途の取り出し。掃除（cleankit）と違い、見えているスライドの内容だけを拾うので、
非表示・ノート・コメント・マスター・使っていないレイアウト・プロパティ・写しは構造上出ない。
元ファイルは読むだけ。出力は実データを含むので、AI に見せない場所（raw 側）に置き、マスクしてから ai/in へ。

  python pptxtext.py <入力.pptx> <出力.md> [--force]

出すもの（スライドの順）:
  - 見出し: `## スライド N: <タイトル>`（タイトルが無ければ `## スライド N`）
  - 文章: 箇条書きは段落の階層をインデントにする。図形の並びは上から下、左から右
  - 表: markdown の表
  - 矢印: 両端が図形につながっているものだけ `A → B`（つながっていない線は出さない）
  - SmartArt: 文字を入れ子の箇条書きで
  - グラフ・画像: `[グラフ: <タイトル>]` `[画像]`（中身は出さない。画像の中の文字は取り出せない）
出さないもの: 非表示のスライド・図形、スライドの外の図形、ノート、コメント、マスター・レイアウト、代替テキスト、図形の名前。
終了コード: 0 = 書いた、2 = 実行できない。
"""
import argparse
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cleankit import CleanError, Pkg, attrs, guard_outputs, main_part, pres_slides  # noqa: E402

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
C = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
DGM = "{http://schemas.openxmlformats.org/drawingml/2006/diagram}"


def local(el):
    return el.tag.rsplit("}", 1)[-1]


def xml_of(pkg, part):
    t = pkg.text(part)
    if t is None:
        return None
    try:
        return ET.fromstring(t)
    except ET.ParseError:
        return None


def para_text(p):
    out = []
    for el in p:
        n = local(el)
        if n == "r":
            t = el.find(A + "t")
            out.append(t.text or "" if t is not None else "")
        elif n == "br":
            out.append(" ")
        elif n == "fld":
            t = el.find(A + "t")
            out.append(t.text or "" if t is not None else "")
    return "".join(out).strip()


def body_lines(txbody):
    """段落 → 箇条書きの行。階層(lvl)をインデントにする。"""
    lines = []
    if txbody is None:
        return lines
    for p in txbody.findall(A + "p"):
        s = para_text(p)
        if not s:
            continue
        ppr = p.find(A + "pPr")
        lvl = int(ppr.get("lvl", "0")) if ppr is not None else 0
        bulleted = ppr is not None and ppr.find(A + "buNone") is None and (
            ppr.find(A + "buChar") is not None or ppr.find(A + "buAutoNum") is not None or lvl > 0)
        lines.append(("  " * lvl + "- " + s) if bulleted else s)
    return lines


def xfrm(sp):
    """図形の位置 (x, y, w, h)。無ければ None（プレースホルダーはレイアウトを継ぐので位置が分からない）。"""
    for path in (f"{P}spPr", f"{P}grpSpPr", f"{P}xfrm"):
        e = sp.find(path)
        if e is None:
            continue
        x = e if local(e) == "xfrm" else e.find(A + "xfrm")
        if x is None:
            continue
        o, ext = x.find(A + "off"), x.find(A + "ext")
        if o is not None and ext is not None:
            return int(o.get("x", 0)), int(o.get("y", 0)), int(ext.get("cx", 0)), int(ext.get("cy", 0))
    return None


def cnv(sp):
    """cNvPr（id・非表示）。"""
    for e in sp.iter(P + "cNvPr"):
        return e
    return None


def is_title(sp):
    ph = next(sp.iter(P + "ph"), None)
    return ph is not None and ph.get("type") in ("title", "ctrTitle")


class Slide:
    def __init__(self, pkg, path, sw, sh):
        self.pkg, self.path, self.sw, self.sh = pkg, path, sw, sh
        self.blocks = []   # (y, x, order, [行])
        self.names = {}    # 図形 id → 図形の文字（矢印の端の名前に使う）
        self.arrows = []   # (開始 id, 終了 id)
        self.title = ""
        self.rel = {rid: (ty, tgt) for rid, ty, tgt in pkg.internal(path)}
        self.seq = 0

    def off(self, pos):
        if pos is None or not (self.sw and self.sh):
            return False
        x, y, w, h = pos
        return x >= self.sw or y >= self.sh or x + w <= 0 or y + h <= 0

    def add(self, pos, lines):
        if not lines:
            return
        self.seq += 1
        y, x = (pos[1], pos[0]) if pos else (10**12, 0)  # 位置が分からないものは最後
        self.blocks.append((y, x, self.seq, lines))

    def walk(self, parent):
        for el in parent:
            n = local(el)
            c = cnv(el) if n in ("sp", "pic", "cxnSp", "graphicFrame", "grpSp") else None
            if c is not None and c.get("hidden") in ("1", "true"):
                continue
            if n == "grpSp":
                self.walk(el)
            elif n == "sp":
                self.shape(el, c)
            elif n == "cxnSp":
                cc = el.find(f"{P}nvCxnSpPr/{P}cNvCxnSpPr")
                st = cc.find(A + "stCxn") if cc is not None else None
                en = cc.find(A + "endCxn") if cc is not None else None
                if st is not None and en is not None and not self.off(xfrm(el)):
                    self.arrows.append((st.get("id"), en.get("id"), el))
            elif n == "pic":
                if not self.off(xfrm(el)):
                    self.add(xfrm(el), ["[画像]"])
            elif n == "graphicFrame":
                self.frame(el)

    def shape(self, sp, c):
        pos = xfrm(sp)
        if self.off(pos):
            return
        lines = body_lines(sp.find(P + "txBody"))
        if c is not None and lines:
            self.names[c.get("id")] = " ".join(l.strip("- ").strip() for l in lines)[:40]
        if is_title(sp):
            self.title = " ".join(l.strip("- ").strip() for l in lines)
            return
        self.add(pos, lines)

    def frame(self, gf):
        pos = xfrm(gf)
        if self.off(pos):
            return
        gd = gf.find(f"{A}graphic/{A}graphicData")
        if gd is None:
            return
        tbl = gd.find(A + "tbl")
        if tbl is not None:
            self.add(pos, table_lines(tbl))
            return
        rid = None
        for e in gd.iter():
            for k, v in e.attrib.items():
                if k.endswith("}id") and local(e) in ("chart", "relIds") or k.endswith("}dm"):
                    rid = rid or v
        if local(next(iter(gd), gd)) == "chart":
            ty, tgt = self.rel.get(rid, (None, None))
            title = chart_title(xml_of(self.pkg, tgt)) if tgt else ""
            self.add(pos, [f"[グラフ: {title}]" if title else "[グラフ]"])
        elif local(next(iter(gd), gd)) == "relIds":
            ty, tgt = self.rel.get(rid, (None, None))
            self.add(pos, smartart_lines(xml_of(self.pkg, tgt)) if tgt else ["[SmartArt]"])
        else:
            self.add(pos, ["[埋め込みオブジェクト]"])


def table_lines(tbl):
    rows = []
    for tr in tbl.findall(A + "tr"):
        cells = []
        for tc in tr.findall(A + "tc"):
            t = " ".join(filter(None, (para_text(p) for p in tc.iter(A + "p"))))
            cells.append(t.replace("|", "\\|"))
        rows.append(cells)
    if not rows:
        return []
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * w]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return out


def chart_title(root):
    if root is None:
        return ""
    t = root.find(f".//{C}title")
    if t is None:
        return ""
    return "".join(x.text or "" for x in t.iter(A + "t")).strip()


def smartart_lines(root):
    """データモデルの点（pt）を、親子（parOf）で入れ子にする。"""
    if root is None:
        return ["[SmartArt]"]
    pts, kids, has_parent = {}, {}, set()
    for pt in root.iter(DGM + "pt"):
        if pt.get("type", "node") not in ("node", "pres") and pt.get("type") != "doc":
            continue
        txt = " ".join(filter(None, (para_text(p) for p in pt.iter(A + "p"))))
        pts[pt.get("modelId")] = (pt.get("type", "node"), txt)
    for cx in root.iter(DGM + "cxn"):
        if cx.get("type", "parOf") != "parOf":
            continue
        s, d = cx.get("srcId"), cx.get("destId")
        if s in pts and d in pts and pts[d][0] == "node":
            kids.setdefault(s, []).append((int(cx.get("srcOrd", 0)), d))
            has_parent.add(d)
    out = []

    def rec(i, depth):
        if pts[i][1]:
            out.append("  " * depth + "- " + pts[i][1])
        for _o, k in sorted(kids.get(i, [])):
            rec(k, depth + (1 if pts[i][1] else 0))

    roots = [i for i, (t, _x) in pts.items() if t == "doc"] or [i for i, (t, _x) in pts.items() if t == "node" and i not in has_parent]
    for r in roots:
        rec(r, 0)
    return out or ["[SmartArt]"]


def extract(data):
    pkg = Pkg(data)
    if pkg.dups:
        raise CleanError("同じ名前のエントリーが複数ある zip は取り出さない")
    pres = main_part(pkg)
    t = pkg.text(pres) or ""
    sz = re.search(r"<p:sldSz\b[^>]*/>", t)
    a = attrs(sz.group(0)) if sz else {}
    sw, sh = int(a.get("cx", 0)), int(a.get("cy", 0))
    out, n = [], 0
    for s in pres_slides(pkg, pres):
        n += 1
        if s["hidden"]:
            continue
        root = xml_of(pkg, s["path"])
        if root is None:
            continue
        sl = Slide(pkg, s["path"], sw, sh)
        tree = root.find(f"{P}cSld/{P}spTree")
        if tree is not None:
            sl.walk(tree)
        arrows = []
        for st, en, _el in sl.arrows:
            arrows.append(f"{sl.names.get(st, '?')} → {sl.names.get(en, '?')}")
        head = f"## スライド {n}" + (f": {sl.title}" if sl.title else "")
        out.append(head)
        for _y, _x, _o, lines in sorted(sl.blocks, key=lambda b: (b[0], b[1], b[2])):
            out.append("")
            out += lines
        if arrows:
            out += ["", "矢印:"] + [f"- {x}" for x in arrows]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="pptx の見えている文章と図解を markdown に取り出す")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--force", action="store_true", help="出力が既にあっても上書きする")
    a = ap.parse_args(argv)
    src, dst = Path(a.input), Path(a.output)
    try:
        if src.suffix.lower() not in (".pptx", ".pptm"):
            raise CleanError("pptx・pptm だけ扱う")
        guard_outputs(dst)
        if dst.exists() and not a.force:
            raise CleanError("出力が既にある（--force で上書き）")
        md = extract(src.read_bytes())
    except (CleanError, OSError) as e:
        print(f"実行できない: {e}", file=sys.stderr)
        return 2
    dst.write_text(md, encoding="utf-8", newline="\n")
    print(f"書いた: {dst}（{md.count(chr(10))} 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
