# /// script
# requires-python = "==3.13.*"
# dependencies = []
# ///
"""exceltext: xlsx の「見えているシートの値と図形」を markdown に取り出す（標準ライブラリだけ。v0）。

pptxtext の xlsx 版。AI に読ませる用途（分析・示唆の抽出・論点整理）の取り出し。掃除（cleankit）と違い、
見えているシートの見えているセルの値だけを拾うので、非表示のシート・行・列、コメント、定義名、
プロパティ、外部リンク、キャッシュの写しは構造上出ない。
元ファイルは読むだけ。出力は実データを含むので、AI に見せない場所（raw 側）に置き、人が読んでから ai/in へ。

  python exceltext.py <入力.xlsx> <出力.md> [--force]

出すもの（シートの順）:
  - 見出し: `## シート N: <シート名>`
  - セル: markdown の表。1 列目は行番号、見出し行は列の記号（A, B, …）。表示される値（数式は計算済みの値）。
    日付の書式は YYYY-MM-DD（時刻つきは hh:mm）、% の書式は百分率。値の無い行・列は詰める
  - 図形: テキストボックスの文字、両端が図形につながった矢印 `A → B`、SmartArt の文字、
    `[グラフ: <タイトル>]` `[画像]`（中身は出さない。画像の中の文字は取り出せない）
  - グラフシート: `[グラフシート: <タイトル>]`
出さないもの: 非表示・とても非表示のシート、非表示の行（フィルターで隠れた行を含む）・列、非表示の図形、
  コメント・メモ、ヘッダー・フッター、定義名、数式そのもの、入力規則、代替テキスト、図形の名前、プロパティ。
終了コード: 0 = 書いた、2 = 実行できない。
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cleankit import CleanError, Pkg, col_num, guard_outputs, main_part, wb_sheets  # noqa: E402
from pptxtext import body_lines, chart_title, local, smartart_lines, xml_of  # noqa: E402

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
XDR = "{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

# 組み込みの書式番号のうち、日付・時刻のもの（ECMA-376 18.8.30）
DATE_IDS = set(range(14, 18)) | {22} | set(range(27, 37)) | set(range(50, 59))
TIME_IDS = {18, 19, 20, 21, 45, 46, 47}
PCT_IDS = {9, 10}


def col_name(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def si_text(si):
    """共有文字列・インライン文字列の文字。ふりがな（rPh）は出さない。"""
    out = []
    for el in si:
        n = local(el)
        if n == "t":
            out.append(el.text or "")
        elif n == "r":
            t = el.find(S + "t")
            out.append(t.text or "" if t is not None else "")
    return "".join(out)


def load_sst(pkg, wb):
    for _rid, ty, tgt in pkg.internal(wb):
        if ty == "sharedStrings":
            root = xml_of(pkg, tgt)
            return [] if root is None else [si_text(si) for si in root.findall(S + "si")]
    return []


def strip_fmt(code):
    """書式コードから、引用符・エスケープ・色や条件の [..] を外す（日付・% の判定用）。"""
    code = re.sub(r'"[^"]*"', "", code)
    code = re.sub(r"\\.", "", code)
    return re.sub(r"\[[^\]]*\]", "", code)


def load_styles(pkg, wb):
    """セルの書式番号（s）→ 種類（'date' 'datetime' 'time' 'pct' None）。"""
    root = None
    for _rid, ty, tgt in pkg.internal(wb):
        if ty == "styles":
            root = xml_of(pkg, tgt)
    if root is None:
        return []
    custom = {}
    nf = root.find(S + "numFmts")
    for f in (nf if nf is not None else []):
        custom[int(f.get("numFmtId", "0"))] = f.get("formatCode", "")
    kinds = []
    xfs = root.find(S + "cellXfs")
    for xf in (xfs if xfs is not None else []):
        i = int(xf.get("numFmtId", "0"))
        kind = None
        if i in DATE_IDS:
            kind = "datetime" if i == 22 else "date"
        elif i in TIME_IDS:
            kind = "time"
        elif i in PCT_IDS:
            kind = "pct"
        elif i in custom:
            c = re.sub(r"(?i)general|E[+-]", "", strip_fmt(custom[i]).split(";")[0])
            has_t = bool(re.search(r"[hHsS]", c))
            has_d = bool(re.search(r"[yYdDge]", c) or (re.search(r"[mM]", c) and not has_t))  # m は時刻と並べば分
            if has_d and has_t:
                kind = "datetime"
            elif has_d:
                kind = "date"
            elif has_t:
                kind = "time"
            elif "%" in c:
                kind = "pct"
        kinds.append(kind)
    return kinds


def num_text(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return format(x, ".15g")


def fmt_number(v, kind, date1904):
    try:
        x = float(v)
    except ValueError:
        return v
    if kind in ("date", "datetime", "time"):
        base = dt.datetime(1904, 1, 1) if date1904 else dt.datetime(1899, 12, 30)
        if x < 0 or x > 2958465:
            return num_text(x)
        t = base + dt.timedelta(days=x)
        t = (t + dt.timedelta(seconds=0.5)).replace(microsecond=0)
        if kind == "time" or (x < 1 and kind == "datetime"):
            return t.strftime("%H:%M:%S") if t.second else t.strftime("%H:%M")
        if kind == "datetime" and (t.hour or t.minute or t.second):
            return t.strftime("%Y-%m-%d %H:%M")
        return t.strftime("%Y-%m-%d")
    if kind == "pct":
        return num_text(round(x * 100, 10)) + "%"
    return num_text(x)


def cell_value(c, sst, kinds, date1904):
    t = c.get("t", "n")
    if t == "inlineStr":
        is_ = c.find(S + "is")
        return si_text(is_) if is_ is not None else ""
    v = c.find(S + "v")
    if v is None or v.text is None:
        return ""  # 計算していない数式・空のセルは、見えている値が無い
    if t == "s":
        try:
            return sst[int(v.text)]
        except (ValueError, IndexError):
            return ""
    if t == "b":
        return "TRUE" if v.text.strip() in ("1", "true") else "FALSE"
    if t in ("str", "e"):
        return v.text
    s = int(c.get("s", "0") or 0)
    return fmt_number(v.text, kinds[s] if s < len(kinds) else None, date1904)


def md_cell(s):
    return s.replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "\n").replace("\n", "<br>").strip()


def sheet_table(root, sst, kinds, date1904):
    hidden = set()
    cols = root.find(S + "cols")
    for col in (cols if cols is not None else []):
        if col.get("hidden") in ("1", "true"):
            hidden.update(range(int(col.get("min", "0")), min(int(col.get("max", "0")), 16384) + 1))
    data = root.find(S + "sheetData")
    grid, used, rn = {}, set(), 0
    for row in (data if data is not None else []):
        rn = int(row.get("r", rn + 1))
        if row.get("hidden") in ("1", "true"):
            continue
        cn = 0
        for c in row.findall(S + "c"):
            ref = c.get("r")
            cn = col_num(ref) if ref else cn + 1
            if cn in hidden:
                continue
            val = md_cell(cell_value(c, sst, kinds, date1904))
            if val:
                grid.setdefault(rn, {})[cn] = val
                used.add(cn)
    if not grid:
        return []
    cs = sorted(used)
    out = ["| 行 | " + " | ".join(col_name(x) for x in cs) + " |", "|" + " --- |" * (len(cs) + 1)]
    for r in sorted(grid):
        out.append(f"| {r} | " + " | ".join(grid[r].get(x, "") for x in cs) + " |")
    return out


class Drawing:
    """シートの図形（drawing の部品）。位置（行, 列）の順に並べる。"""

    def __init__(self, pkg, path):
        self.pkg, self.path = pkg, path
        self.rel = {rid: (ty, tgt) for rid, ty, tgt in pkg.internal(path)}
        self.items, self.names, self.arrows, self.seq = [], {}, [], 0

    def add(self, pos, lines):
        if lines:
            self.seq += 1
            self.items.append((pos, self.seq, lines))

    def run(self):
        root = xml_of(self.pkg, self.path)
        if root is None:
            return []
        for anc in root:
            if local(anc) not in ("twoCellAnchor", "oneCellAnchor", "absoluteAnchor"):
                continue
            fr = anc.find(XDR + "from")
            pos = (int(fr.findtext(XDR + "row", "0")), int(fr.findtext(XDR + "col", "0"))) if fr is not None else (10**9, 0)
            self.walk(anc, pos)
        out = []
        for _pos, _s, lines in sorted(self.items, key=lambda i: (i[0], i[1])):
            out += lines
        for st, en in self.arrows:
            out.append(f"{self.names.get(st, '?')} → {self.names.get(en, '?')}")
        return out

    def walk(self, parent, pos):
        for el in parent:
            n = local(el)
            if n not in ("sp", "pic", "cxnSp", "graphicFrame", "grpSp"):
                continue
            c = next(el.iter(XDR + "cNvPr"), None)
            if c is not None and c.get("hidden") in ("1", "true"):
                continue
            if n == "grpSp":
                self.walk(el, pos)
            elif n == "sp":
                lines = body_lines(el.find(XDR + "txBody"))
                if c is not None and lines:
                    self.names[c.get("id")] = " ".join(l.strip("- ").strip() for l in lines)[:40]
                self.add(pos, lines)
            elif n == "cxnSp":
                cc = el.find(f"{XDR}nvCxnSpPr/{XDR}cNvCxnSpPr")
                st = cc.find(A + "stCxn") if cc is not None else None
                en = cc.find(A + "endCxn") if cc is not None else None
                if st is not None and en is not None:
                    self.arrows.append((st.get("id"), en.get("id")))
            elif n == "pic":
                self.add(pos, ["[画像]"])
            elif n == "graphicFrame":
                self.frame(el, pos)

    def frame(self, gf, pos):
        gd = gf.find(f"{A}graphic/{A}graphicData")
        first = next(iter(gd), None) if gd is not None else None
        if first is None:
            return
        if local(first) == "chart":
            _ty, tgt = self.rel.get(first.get(R_ID), (None, None))
            title = chart_title(xml_of(self.pkg, tgt)) if tgt else ""
            self.add(pos, [f"[グラフ: {title}]" if title else "[グラフ]"])
        elif local(first) == "relIds":
            dm = next((v for k, v in first.attrib.items() if k.endswith("}dm")), None)
            _ty, tgt = self.rel.get(dm, (None, None))
            self.add(pos, smartart_lines(xml_of(self.pkg, tgt)) if tgt else ["[SmartArt]"])
        else:
            self.add(pos, ["[埋め込みオブジェクト]"])


def drawing_lines(pkg, part):
    out = []
    for _rid, ty, tgt in pkg.internal(part):
        if ty == "drawing":
            out += Drawing(pkg, tgt).run()
    return out


def chartsheet_lines(pkg, part):
    titles = []
    for _rid, ty, tgt in pkg.internal(part):
        if ty == "drawing":
            for _r2, ty2, tgt2 in pkg.internal(tgt):
                if ty2 == "chart":
                    titles.append(chart_title(xml_of(pkg, tgt2)))
    return [f"[グラフシート: {t}]" if t else "[グラフシート]" for t in titles] or ["[グラフシート]"]


def extract(data):
    pkg = Pkg(data)
    if pkg.dups:
        raise CleanError("同じ名前のエントリーが複数ある zip は取り出さない")
    wb = main_part(pkg)
    wbx = xml_of(pkg, wb)
    if wbx is None or local(wbx) != "workbook":
        raise CleanError("ブック（workbook）として読めない")
    pr = wbx.find(S + "workbookPr")
    date1904 = pr is not None and pr.get("date1904") in ("1", "true")
    sst, kinds = load_sst(pkg, wb), load_styles(pkg, wb)
    out, n = [], 0
    for s in wb_sheets(pkg, wb):
        n += 1
        if s["state"] != "visible" or not s["path"]:
            continue
        root = xml_of(pkg, s["path"])
        if root is None:
            continue
        out.append(f"## シート {n}: {s['name']}")
        if local(root) == "chartsheet":
            out += [""] + chartsheet_lines(pkg, s["path"])
        else:
            table = sheet_table(root, sst, kinds, date1904)
            shapes = drawing_lines(pkg, s["path"])
            out += ["", *table] if table else ["", "（値なし）"]
            if shapes:
                out += ["", "図形:"] + [x if x.startswith(("  ", "- ")) else f"- {x}" for x in shapes]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="xlsx の見えているシートの値と図形を markdown に取り出す")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--force", action="store_true", help="出力が既にあっても上書きする")
    a = ap.parse_args(argv)
    src, dst = Path(a.input), Path(a.output)
    try:
        if src.suffix.lower() not in (".xlsx", ".xlsm"):
            raise CleanError("xlsx・xlsm だけ扱う")
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
