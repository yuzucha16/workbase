# /// script
# requires-python = "==3.13.*"
# dependencies = []
# ///
"""cleankit: xlsx・pptx の残存情報の点検と掃除（標準ライブラリだけ）。

人が実行する。AI には実行させない（原本と、残っていた実データを読むため）。
元ファイルは読むだけで、掃除の結果は別のファイルに書く。報告（実データの抜粋が載る）は AI に見せない場所に置く。
考え方と残り方の一覧は mask-spec.md の「クリーン化」。

  python cleankit.py check <ファイル> [--report <md>]
  python cleankit.py clean <ファイル> <出力> [--profile standard|strict] [--allow <種類,...>] [--keep <動作,...>] [--also <動作,...>] [--report <md>] [--force]
  python cleankit.py profiles

check: 残っている情報を一覧にする（既知の残り方に加え、見えている文字と固定語に当たらない文字を unseen-text として出す）。clean: 既定の動作（CLEAN_ACTIONS）で取り除いた別ファイルを書き、出力をもう一度点検する。
画面には件数だけを出す（抜粋は報告のファイルだけに書く）。終了コード: 0 = 要確認なし、1 = 要確認あり、2 = 実行できない。
"""
import argparse
import html
import io
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import unescape as _unesc
import xml.etree.ElementTree as ET

SUPPORTED = (".xlsx", ".xlsm", ".pptx", ".pptm")
XML_EXT = (".xml", ".rels", ".vml")
SAMPLE_LEN = 60
SAMPLE_MAX = 5

# clean の既定の動作（--keep で外せる）。報告だけのもの（キャッシュ、外部リンク、埋め込みなど）は消さない
CLEAN_ACTIONS = {
    "hidden-sheets": "非表示シート（hidden / veryHidden）を消し、参照する数式は値に、定義名は削除",
    "hidden-slides": "非表示スライドを消す",
    "notes": "スライドのノートを外す",
    "comments": "コメントと作成者（xlsx の persons、pptx の commentAuthors / authors）を外す",
    "props": "文書プロパティの個人情報（作成者・更新者・会社・管理者・タイトルなど）を空にし、シート名の一覧と custom.xml を外す",
    "abspath": "保存場所の絶対パス（x15ac:absPath）を消す",
    "printer": "プリンター設定を外す",
    "thumbnail": "縮小画像を外す",
    "calcchain": "計算順の一覧（calcChain）を外す（Excel が作り直す）",
    "revisions": "変更履歴（revisions）を外す",
    "ref-names": "参照先が無い（#REF!）定義名を消す",
    "hidden-names": "非表示の定義名を消す（取り込み元のパスを持つ AccessDatabase など。_xl で始まる Excel 内部の名前は残す）",
    "external-links": "外部ブックへのリンクを切る（数式は値に、リンクの部品・外部パス・値の写し・外部を参照する定義名を消す）",
    "shared-strings": "どのセルも使っていない共有文字列を消す",
    "orphans": "関係からたどれない部品を消す",
}

# 既定では行わず、--also で指定したときだけ行う動作（表の中身を変えるため）
OPTIONAL_ACTIONS = {
    "hidden-rows": "非表示の行のセルの値と数式を空にする（行は残る。共有数式は残す）",
    "hidden-cols": "非表示の列のセルの値と数式を空にする（列は残る。共有数式は残す）",
}

# 部品の種類ごとの除去（プロファイル strict が使う）。種類 → (説明, 関係の種類)。参照元の要素も外す
STRIP_KINDS = {
    "charts": ("グラフ（図形ごと外す。元データのセルは残る）", {"chart", "chartEx", "chartUserShapes"}),
    "images": ("画像（図形・背景・シートの背景。縮小画像は thumbnail が別に外す）", {"image"}),
    "embeddings": ("埋め込みオブジェクト（OLE、埋め込みブック）", {"oleObject", "package"}),
    "pivots": ("ピボットの部品（キャッシュ全件を含む。ピボットの表は値として残る）", {"pivotCacheDefinition", "pivotCacheRecords", "pivotTable"}),
    "connections": ("接続・クエリ・データモデル・customXml", {"connections", "queryTable", "customXml", "powerPivotData"}),
}

# プロファイル: 名前 → (説明, 足す動作)。standard は既定の掃除だけ。--allow で strict から種類を許可に戻せる
PROFILES = {
    "standard": ("既定の掃除だけ（グラフ・画像・ピボットなどは残して報告）", ()),
    "strict": ("standard に加え、部品の種類（STRIP_KINDS）をすべて外し、非表示の行・列の値を空にする", tuple(STRIP_KINDS) + ("hidden-rows", "hidden-cols")),
}

R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_XML_UNESC = {"&quot;": '"', "&apos;": "'", "&#39;": "'"}
_REL_RE = re.compile(r"<Relationship\b[^>]*?(?:/>|>\s*</Relationship>)", re.S)
_ATTR_RE = re.compile(r'([\w:.-]+)\s*=\s*"([^"]*)"')
_TAG_RE = re.compile(r"<[^>]+>")


class CleanError(Exception):
    pass


def attrs(tag):
    return {k: _unesc(v, _XML_UNESC) for k, v in _ATTR_RE.findall(tag)}


def plain(xml):
    """XML から文字だけを取り出す（抜粋用）。"""
    t = _unesc(_TAG_RE.sub(" ", xml), _XML_UNESC)
    return re.sub(r"\s+", " ", t).strip()


def clip(s):
    return s if len(s) <= SAMPLE_LEN else s[:SAMPLE_LEN] + "…"


def rels_path(part):
    d, b = posixpath.split(part)
    return posixpath.join(d, "_rels", b + ".rels")


def resolve(src, target):
    if target.startswith("/"):
        return target[1:]
    return posixpath.normpath(posixpath.join(posixpath.dirname(src), target))


def rtype(rel):
    return rel.get("Type", "").rsplit("/", 1)[-1]


class Finding:
    def __init__(self, code, part, detail, samples=()):
        self.code, self.part, self.detail = code, part, detail
        self.samples = [clip(s) for s in samples if s][:SAMPLE_MAX]
        self.refs = []


# ---------- パッケージ（zip）の読み書き ----------

class Pkg:
    def __init__(self, data):
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile as e:
            raise CleanError(f"zip として読めない: {e}")
        names = [i.filename for i in z.infolist() if not i.filename.endswith("/")]
        self.dups = sorted({n for n in names if names.count(n) > 1})
        self.order = list(dict.fromkeys(names))
        self.parts = {n: z.read(n) for n in self.order}

    def has(self, n):
        return n in self.parts

    def text(self, n):
        raw = self.parts.get(n)
        if raw is None:
            return None
        for enc in ("utf-8-sig", "utf-16"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return None

    def put(self, n, s):
        self.parts[n] = s.encode("utf-8")

    def rels(self, part):
        t = self.text(rels_path(part)) if part else self.text("_rels/.rels")
        return [attrs(m.group(0)) for m in _REL_RE.finditer(t or "")]

    def internal(self, part, types=None):
        """part の内部の関係（Id, 種類, 解決したパス）。"""
        out = []
        for r in self.rels(part):
            if r.get("TargetMode") == "External":
                continue
            if types and rtype(r) not in types:
                continue
            out.append((r.get("Id"), rtype(r), resolve(part, r.get("Target", ""))))
        return out

    def drop_rel(self, part, rid):
        rp = rels_path(part) if part else "_rels/.rels"
        t = self.text(rp)
        if t is None:
            return
        self.put(rp, _REL_RE.sub(lambda m: "" if attrs(m.group(0)).get("Id") == rid else m.group(0), t))

    def drop_rels_of(self, part, types):
        dropped = []
        for rid, ty, tgt in self.internal(part, types):
            self.drop_rel(part, rid)
            dropped.append((rid, tgt))
        return dropped

    def remove(self, n):
        self.parts.pop(n, None)
        self.parts.pop(rels_path(n), None)
        ct = self.text("[Content_Types].xml")
        if ct is not None:
            pat = re.compile(r'<Override\b[^>]*PartName="/' + re.escape(n) + r'"[^>]*/>', re.I)
            self.put("[Content_Types].xml", pat.sub("", ct))

    def reachable(self):
        seen, todo = set(), [""]
        while todo:
            p = todo.pop()
            for _rid, _ty, tgt in self.internal(p):
                if tgt not in seen and tgt in self.parts:
                    seen.add(tgt)
                    todo.append(tgt)
        return seen

    def orphans(self):
        reach = self.reachable()
        out = []
        for n in self.order:
            if n not in self.parts or n == "[Content_Types].xml" or n.endswith(".rels") or n in reach:
                continue
            out.append(n)
        return out

    def tobytes(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for n in self.order:
                if n in self.parts:
                    zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(zi, self.parts[n])
        return buf.getvalue()


def main_part(pkg):
    for _rid, ty, tgt in pkg.internal(""):
        if ty == "officeDocument":
            return tgt
    raise CleanError("本体の部品（officeDocument）が見つからない")


# ---------- 点検: 共通 ----------

def check_common(pkg, fs):
    if pkg.dups:
        fs.append(Finding("zip-duplicate", "", f"同じ名前のエントリーが複数ある（{len(pkg.dups)} 件）", pkg.dups))
    orph = pkg.orphans()
    if orph:
        fs.append(Finding("orphan-part", "", f"関係からたどれない部品（{len(orph)} 件）", orph))
    core = pkg.text("docProps/core.xml")
    if core:
        vals = []
        for tag in ("dc:creator", "cp:lastModifiedBy", "dc:title", "dc:subject", "cp:keywords",
                    "dc:description", "cp:category", "cp:contentStatus"):
            for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", core, re.S):
                if plain(m.group(1)):
                    vals.append(f"{tag}: {plain(m.group(1))}")
        if vals:
            fs.append(Finding("props-core", "docProps/core.xml", "作成者などのプロパティ", vals))
    app = pkg.text("docProps/app.xml")
    if app:
        vals = []
        for tag in ("Company", "Manager", "HyperlinkBase"):
            m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", app, re.S)
            if m and plain(m.group(1)):
                vals.append(f"{tag}: {plain(m.group(1))}")
        m = re.search(r"<TitlesOfParts\b.*?</TitlesOfParts>", app, re.S)
        if m:
            vals.append("TitlesOfParts: " + " / ".join(plain(x) for x in re.findall(r"<vt:lpstr>(.*?)</vt:lpstr>", m.group(0), re.S)))
        if vals:
            fs.append(Finding("props-app", "docProps/app.xml", "会社名・部品名の一覧（シート名・スライドのタイトル）", vals))
    for _rid, ty, tgt in pkg.internal(""):
        if ty == "custom-properties" and pkg.has(tgt):
            t = pkg.text(tgt) or ""
            props = [f"{attrs(m.group(1)).get('name', '')}: {plain(m.group(2))}"
                     for m in re.finditer(r"<property\b([^>]*)>(.*?)</property>", t, re.S)]
            if props:
                fs.append(Finding("props-custom", tgt, f"ユーザー定義のプロパティ（{len(props)} 件。秘密度ラベル MSIP_Label_* もここ）", props))
        if ty == "thumbnail" and pkg.has(tgt):
            fs.append(Finding("thumbnail", tgt, "縮小画像（文字が写る）"))
    ext = []
    for n in pkg.order:
        if n.endswith(".rels") and n in pkg.parts:
            for m in _REL_RE.finditer(pkg.text(n) or ""):
                a = attrs(m.group(0))
                if a.get("TargetMode") == "External":
                    ext.append(f"{rtype(a)}: {a.get('Target', '')}")
    if ext:
        fs.append(Finding("external-target", "", f"外部への参照（リンク・パス。{len(ext)} 件）", sorted(set(ext))))
    groups = (("embedding", r"(^|/)embeddings/", "埋め込み（ブック・文書・OLE。中身は人が見る）"),
              ("media", r"(^|/)media/", "画像・動画（写った文字、EXIF）"),
              ("vba", r"vbaProject\.bin$", "マクロ（コードと作成者）"),
              ("custom-xml", r"^customXml/", "カスタム XML（Power Query、SharePoint のメタデータなど）"),
              ("activex", r"(^|/)activeX/", "ActiveX コントロール"),
              ("webextension", r"(^|/)webextensions/", "アドイン"),
              ("printer", r"printerSettings", "プリンター設定（プリンター名、共有パス）"))
    for code, pat, label in groups:
        hit = [n for n in pkg.order if n in pkg.parts and re.search(pat, n, re.I) and not n.endswith(".rels")]
        if hit:
            fs.append(Finding(code, "", f"{label}（{len(hit)} 件）", hit))
    for n in pkg.order:
        if n in pkg.parts and re.search(r"/charts/chart[^/]*\.xml$", n):
            t = pkg.text(n) or ""
            refs = sorted(set(plain(x) for x in re.findall(r"<c:f>(.*?)</c:f>", t, re.S)))
            pts = [plain(x) for x in re.findall(r"<c:pt\b[^>]*>\s*<c:v>(.*?)</c:v>", t, re.S)]
            if pts:
                f = Finding("chart-cache", n, f"グラフの元データの写し（{len(pts)} 個。参照: {', '.join(refs) or 'なし'}）", pts)
                f.refs = refs
                fs.append(f)


# ---------- 点検: xlsx ----------

def wb_sheets(pkg, wb):
    t = pkg.text(wb) or ""
    rid2path = {rid: tgt for rid, _ty, tgt in pkg.internal(wb)}
    out = []
    for m in re.finditer(r"<sheet\b[^>]*/>", t):
        a = attrs(m.group(0))
        out.append({"name": a.get("name", ""), "state": a.get("state", "visible"),
                    "rid": a.get("r:id", ""), "path": rid2path.get(a.get("r:id", ""), ""), "tag": m.group(0)})
    return out


def sheet_ref_re(name):
    q = re.escape(name.replace("'", "''"))
    return re.compile(rf"(?:'{q}'|(?<![\w.']){re.escape(name)})!")


def check_xlsx(pkg, fs):
    wb = main_part(pkg)
    t = pkg.text(wb) or ""
    sheets = wb_sheets(pkg, wb)
    hidden = [s for s in sheets if s["state"] != "visible"]
    for s in hidden:
        fs.append(Finding("hidden-sheet", s["path"], f"非表示シート「{s['name']}」（{s['state']}。中身は全部入ったまま）", [s["name"]]))
    names = []
    for m in re.finditer(r"<definedName\b([^>]*)>(.*?)</definedName>", t, re.S):
        a = attrs(m.group(1))
        flag = []
        if "#REF!" in m.group(2):
            flag.append("#REF!")
        if a.get("hidden") in ("1", "true") and not a.get("name", "").startswith("_xl"):
            flag.append("非表示")
        if any(sheet_ref_re(s["name"]).search(_unesc(m.group(2), _XML_UNESC)) for s in hidden):
            flag.append("非表示シートを参照")
        if flag:
            names.append(f"{a.get('name', '')} = {plain(m.group(2))}（{'・'.join(flag)}）")
    if names:
        fs.append(Finding("defined-name", wb, f"参照先を消した・隠した定義名（{len(names)} 件。名前と元の参照が残る）", names))
    visible = {s["name"] for s in sheets if s["state"] == "visible"}
    for f in fs:
        if f.code == "chart-cache":
            bad = sorted({m.group(1) or m.group(2) for r in f.refs for m in re.finditer(r"(?:'((?:[^']|'')+)'|([^'!,()\s]+))!", r)}
                         - visible)
            if bad:
                f.detail += f"（非表示・無いシートを参照: {', '.join(bad)}。グラフは写しで描かれ続ける）"
    m = re.search(r'<x15ac:absPath\b[^>]*\burl="([^"]*)"', t)
    if m:
        fs.append(Finding("abspath", wb, "保存した場所の絶対パス", [_unesc(m.group(1), _XML_UNESC)]))
    m = re.search(r"<fileSharing\b[^>]*/>", t)
    if m and attrs(m.group(0)).get("userName"):
        fs.append(Finding("file-sharing", wb, "書き込みパスワードの設定者名", [attrs(m.group(0))["userName"]]))
    # セル: 非表示の行・列
    for s in sheets:
        st = pkg.text(s["path"]) or ""
        rows, cols = hidden_content(st)
        if (rows or cols) and s["state"] == "visible":
            fs.append(Finding("hidden-rowcol", s["path"], f"「{s['name']}」の非表示の行にある値入りのセル {rows} 個・非表示の列にある値入りのセル {cols} 個（値は入ったまま）"))
    # 共有文字列: どのセルも使っていないもの
    sst = [tgt for _rid, ty, tgt in pkg.internal(wb, {"sharedStrings"})]
    if sst and pkg.has(sst[0]):
        items = re.findall(r"<si\b[^>]*?(?:/>|>.*?</si>)", pkg.text(sst[0]) or "", re.S)
        used = used_sst(pkg, [s["path"] for s in sheets])
        unused = [plain(items[i]) for i in range(len(items)) if i not in used]
        if unused:
            fs.append(Finding("unused-shared-string", sst[0], f"どのセルも使っていない共有文字列（{len(unused)} 件）", unused))
        hidden_only = used_sst(pkg, [s["path"] for s in hidden]) - used_sst(pkg, [s["path"] for s in sheets if s["state"] == "visible"])
        if hidden_only:
            fs.append(Finding("hidden-sheet-string", sst[0], f"非表示シートだけが使う共有文字列（{len(hidden_only)} 件）",
                              [plain(items[i]) for i in sorted(hidden_only) if i < len(items)]))
    for n in pkg.order:
        if n not in pkg.parts:
            continue
        if re.match(r"xl/pivotCache/pivotCacheDefinition[^/]*\.xml$", n):
            d = pkg.text(n) or ""
            src = re.search(r"<worksheetSource\b[^>]*/>", d)
            items = [attrs(x).get("v", "") for x in re.findall(r"<s\b[^>]*/>", d)]
            recs = sum(len(re.findall(r"<r>", pkg.text(tgt) or "")) for _r, _t, tgt in pkg.internal(n, {"pivotCacheRecords"}))
            fs.append(Finding("pivot-cache", n, f"ピボットの元データの写し（行 {recs} 件、項目 {len(items)} 個。元: "
                              f"{plain(' '.join(f'{k}={v}' for k, v in attrs(src.group(0)).items())) if src else '不明'}）", items))
        elif re.match(r"xl/externalLinks/externalLink[^/]*\.xml$", n):
            d = pkg.text(n) or ""
            sn = [attrs(x).get("val", "") for x in re.findall(r"<sheetName\b[^>]*/>", d)]
            cells = len(re.findall(r"<cell\b", d))
            fs.append(Finding("external-link", n, f"外部のブックへのリンク（シート名 {len(sn)} 件、値の写し {cells} 個）", sn))
        elif n == "xl/connections.xml":
            d = pkg.text(n) or ""
            cs = [f"{attrs(x).get('name', '')}: {attrs(x).get('connection', '')}"
                  for x in re.findall(r"<(?:connection|dbPr)\b[^>]*>", d)]
            fs.append(Finding("connection", n, "外部データの接続（サーバー名・ユーザー名・クエリ）", cs))
        elif re.match(r"xl/(model|queryTables|revisions)/", n) and not n.endswith(".rels"):
            label = {"model": "データモデル（取り込んだデータ全件）", "queryTables": "クエリテーブル",
                     "revisions": "変更履歴（消した値を含む）"}[n.split("/")[1]]
            fs.append(Finding(n.split("/")[1].lower(), n, label))
        elif n == "xl/calcChain.xml":
            fs.append(Finding("calcchain", n, "計算順の一覧（シート番号とセル番地。値は持たない）"))
    cparts = [tgt for s in sheets for _r, _t, tgt in pkg.internal(s["path"], {"comments", "threadedComment"})]
    cparts += [tgt for _r, _t, tgt in pkg.internal(wb, {"person"})]
    for n in cparts:
        if pkg.has(n):
            d = pkg.text(n) or ""
            who = [attrs(x).get("displayName", "") for x in re.findall(r"<person\b[^>]*>", d)]
            who += [plain(x) for x in re.findall(r"<author>(.*?)</author>", d, re.S)]
            body = [plain(x) for x in re.findall(r"<(?:comment|threadedComment)\b[^>]*>(.*?)</(?:comment|threadedComment)>", d, re.S)]
            fs.append(Finding("comment", n, "コメント・作成者", who + body))
    return sheets


def used_sst(pkg, paths):
    used = set()
    for p in paths:
        for m in _CELL_RE.finditer(pkg.text(p) or ""):  # 空のセル <c .../> を飛ばす（次のセルを巻き込まない）
            if attrs(m.group(1)).get("t") == "s":
                v = re.search(r"<v>(\d+)</v>", m.group(2) or "")
                if v:
                    used.add(int(v.group(1)))
    return used


# ---------- 点検: pptx ----------

def pres_slides(pkg, pres):
    t = pkg.text(pres) or ""
    rid2path = {rid: tgt for rid, _ty, tgt in pkg.internal(pres)}
    out = []
    for m in re.finditer(r"<p:sldId\b[^>]*/>", t):
        a = attrs(m.group(0))
        p = rid2path.get(a.get("r:id", ""), "")
        st = pkg.text(p) or ""
        hm = re.search(r"<p:sld\b[^>]*>", st)
        hidden = bool(hm and attrs(hm.group(0)).get("show") in ("0", "false"))
        out.append({"id": a.get("id", ""), "rid": a.get("r:id", ""), "path": p, "hidden": hidden, "tag": m.group(0)})
    return out


def check_pptx(pkg, fs):
    pres = main_part(pkg)
    t = pkg.text(pres) or ""
    slides = pres_slides(pkg, pres)
    sz = re.search(r"<p:sldSz\b[^>]*/>", t)
    cx, cy = (int(attrs(sz.group(0)).get("cx", 0)), int(attrs(sz.group(0)).get("cy", 0))) if sz else (0, 0)
    used_layouts, unused = set(), []
    for i, s in enumerate(slides, 1):
        st = pkg.text(s["path"]) or ""
        text = [plain(x) for x in re.findall(r"<a:t>(.*?)</a:t>", st, re.S)]
        if s["hidden"]:
            fs.append(Finding("hidden-slide", s["path"], f"非表示スライド（{i} 枚目）", text))
        hid = [attrs(x).get("name", "") for x in re.findall(r"<p:cNvPr\b[^>]*>", st) if attrs(x).get("hidden") in ("1", "true")]
        if hid:
            fs.append(Finding("hidden-shape", s["path"], f"{i} 枚目の非表示の図形（{len(hid)} 件）", hid))
        alt = [attrs(x).get("descr", "") for x in re.findall(r"<p:cNvPr\b[^>]*>", st) if attrs(x).get("descr")]
        if alt:
            fs.append(Finding("alt-text", s["path"], f"{i} 枚目の代替テキスト（{len(alt)} 件）", alt))
        if cx and cy:
            off = 0
            for m in re.finditer(r'<a:off x="(-?\d+)" y="(-?\d+)"\s*/>\s*<a:ext cx="(\d+)" cy="(\d+)"', st):
                x, y, w, h = map(int, m.groups())
                if x >= cx or y >= cy or x + w <= 0 or y + h <= 0:
                    off += 1
            if off:
                fs.append(Finding("off-slide", s["path"], f"{i} 枚目のスライドの外に置いた図形（{off} 件）"))
        for _rid, ty, tgt in pkg.internal(s["path"]):
            if ty == "notesSlide" and pkg.has(tgt):
                nt = [plain(x) for x in re.findall(r"<a:t>(.*?)</a:t>", pkg.text(tgt) or "", re.S)]
                if any(nt):
                    fs.append(Finding("notes", tgt, f"{i} 枚目のノート", [" ".join(nt)]))
            elif ty == "slideLayout":
                used_layouts.add(tgt)
            elif ty == "comments" and pkg.has(tgt):
                fs.append(Finding("comment", tgt, f"{i} 枚目のコメント", [plain(pkg.text(tgt) or "")]))
    for n in pkg.order:
        if n in pkg.parts and re.match(r"ppt/(commentAuthors|authors)\.xml$", n):
            d = pkg.text(n) or ""
            who = [attrs(x).get("name", "") for x in re.findall(r"<p(?:188)?:(?:cmAuthor|author)\b[^>]*>", d)]
            fs.append(Finding("comment-author", n, "コメントの作成者", who))
        elif n in pkg.parts and re.match(r"ppt/slideLayouts/slideLayout[^/]*\.xml$", n) and n not in used_layouts:
            unused.append(n)
        elif n in pkg.parts and re.match(r"ppt/tags/", n) and not n.endswith(".rels"):
            fs.append(Finding("tags", n, "タグ（アドインが書いた情報）", [plain(pkg.text(n) or "")]))
    if unused:
        fs.append(Finding("unused-layout", "", f"どのスライドも使っていないレイアウト（{len(unused)} 件。以前のテンプレートの文字が残ることがある）", unused))
    return slides


# ---------- 点検: 見えている文字に当たらない文字（許可方式の第一歩） ----------
# 既知の残り方を列挙する点検の外に、取りこぼしの網を張る。ファイルの中の文字を全部集め、
# 「開いたときに見える文字（見えているセルの値と数式・シート名・見えているスライドの文字）」と固定語に当たらないものを出す。
# 消しはしない（報告だけ）。数えないもの: 書式・テーマ・型・関係の部品、数・日付・番地・GUID などの形だけの文字、ふりがな（rPh）、
# 文書プロパティの件数の欄（HeadingPairs）。非表示の図形・スライドの外の図形の文字は見える側に数える（hidden-shape・off-slide で出る）。

_STRUCT_PART_RE = re.compile(r"(^\[Content_Types\]\.xml$|\.rels$|(^|/)theme/|(^|/)styles\.xml$|"
                             r"(^|/)(presProps|viewProps|tableStyles|fontTable)\.xml$)")
_STRUCT_TEXT_RE = re.compile(r"^(?:[-+\d\s.,:;%/()TZE]*|true|false|\{[0-9A-Fa-f-]{36}\}|[0-9A-Fa-f]{8,}|"
                             r"\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?|#(?:REF!|N/A|NAME\?|VALUE!|DIV/0!|NUM!|NULL!))$", re.I)
# 製品が自動で付ける名前（図形・表・ピボット・既定のスタイル・Excel 内部の定義名）
_AUTO_NAME_RE = re.compile(r"^(?:(?:Title|Subtitle|Content|Text|Picture|Rectangle|TextBox|Text Box|Chart|Table|Group|Oval|"
                           r"Straight Connector|Straight Arrow Connector|Slide Number|Date|Footer|Diagram|Graphic|"
                           r"Vertical Title|Vertical Text|Slide Image|[\w ]*Place[Hh]older|"
                           r"PivotTable|Drop Down|Check Box|Button|"
                           r"タイトル|サブタイトル|テキスト ボックス|正方形/長方形|図|グラフ|表|グループ化|楕円|直線コネクタ|"
                           r"直線矢印コネクタ|コンテンツ プレースホルダー|テキスト プレースホルダー|タイトル プレースホルダー|"
                           r"[^\s\d]* ?プレースホルダー|"
                           r"ピボットテーブル|テーブル|ドロップ ダウン|チェック ボックス|ボタン) ?\d*|"
                           r"_xl.*|TableStyle\w+|PivotStyle\w+|SlicerStyle\w+)$")
# 固定語: 製品・テンプレートが書く文字（文書プロパティの一覧、既定のフォント）
FIXED_WORDS = {
    "Microsoft Excel", "Microsoft Office Excel", "Microsoft Office PowerPoint", "Microsoft PowerPoint",
    "Microsoft Macintosh Excel", "Microsoft Macintosh PowerPoint",
    "Worksheets", "ワークシート", "Named Ranges", "名前付き一覧", "Charts", "Theme", "テーマ", "Fonts Used",
    "使用されているフォント", "Slide Titles", "スライド タイトル", "Office Theme", "Office テーマ",
    "Calibri", "Calibri Light", "Arial", "Aptos", "Aptos Display", "Aptos Narrow", "Century", "Meiryo UI", "メイリオ",
    "游ゴシック", "游ゴシック Light", "Yu Gothic", "Yu Gothic Light", "ＭＳ Ｐゴシック", "ＭＳ ゴシック", "ＭＳ 明朝",
    "MS PGothic", "MS Gothic", "MS Mincho", "Liberation Sans", "Liberation Serif", "DejaVu Sans",
    "General", "標準", "PresentationFormat", "On-screen Show (4:3)", "On-screen Show (16:9)", "Widescreen", "ワイド画面",
    "画面に合わせる (4:3)", "画面に合わせる (16:9)",
}
# 中身を文字として調べない要素（製品名・版・件数・時刻など）
_STRUCT_ELEMS = {"Application", "AppVersion", "DocSecurity", "ScaleCrop", "LinksUpToDate", "SharedDoc", "HyperlinksChanged",
                 "TotalTime", "Template", "PresentationFormat", "Words", "Characters", "CharactersWithSpaces", "Lines",
                 "Paragraphs", "Pages", "Slides", "Notes", "HiddenSlides", "MMClips", "cp:revision", "dcterms:created",
                 "dcterms:modified", "dc:language", "c:formatCode", "formatCode", "x:Anchor", "x:AutoFill", "x:Row", "x:Column", "x:SizeWithCells", "x:MoveWithCells"}
# 中身が参照式の要素: 文字列の定数（"..."）とシート名（'...'! / 名前!）だけを調べる
_FORMULA_ELEMS = {"f", "definedName", "formula", "formula1", "formula2", "xm:f", "c:f", "sqref", "xm:sqref"}
# 自由な文字を持つ属性（要素の名前つき。None はどの要素でも）
_FREE_ATTRS = {("name", None), ("descr", None), ("title", None), ("displayName", None), ("userName", None),
               ("initials", None), ("v", "s"), ("val", "sheetName"), ("url", "x15ac:absPath")}
_LEAF_RE = re.compile(r"<([\w:.-]+)\b[^>]*>([^<]+)</\1>")
_OPEN_RE = re.compile(r"<([\w:.-]+)\b([^>]*)>")


def _norm(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def _runs(xml):
    """<t>・<a:t> の文字をつないだもの（書式の切れ目で語を割らない）。ふりがなは除く。"""
    xml = re.sub(r"<rPh\b.*?</rPh>", "", xml, flags=re.S)
    return "".join(html.unescape(x) for x in re.findall(r"<(?:a:)?t\b[^>]*>(.*?)</(?:a:)?t>", xml, re.S))


def _formula_bits(f):
    f = html.unescape(f)
    out = re.findall(r'"((?:[^"]|"")*)"', f)
    out += [a or b for a, b in re.findall(r"'((?:[^']|'')+)'!|([^\s'!,()=+\-*/&<>:\"\[\]]+)!", f)]
    return [x.replace('""', '"').replace("''", "'") for x in out]


def visible_text_xlsx(pkg):
    wb = main_part(pkg)
    sheets = wb_sheets(pkg, wb)
    vis = [s for s in sheets if s["state"] == "visible"]
    sst = [tgt for _rid, _ty, tgt in pkg.internal(wb, {"sharedStrings"})]
    items = [_runs(x) for x in re.findall(r"<si\b[^>]*?(?:/>|>.*?</si>)", pkg.text(sst[0]) or "", re.S)] if sst and pkg.has(sst[0]) else []
    out = [s["name"] for s in vis]
    for s in vis:
        xml = pkg.text(s["path"]) or ""
        hc = hidden_cols(xml)
        for r in re.finditer(_ROW_PAT, xml, re.S):
            hr = attrs(r.group(1)).get("hidden") in ("1", "true")
            for c in _CELL_RE.finditer(r.group(2) or ""):
                a, body = attrs(c.group(1)), c.group(2) or ""
                if hr or col_num(a.get("r", "A1")) in hc:
                    continue
                v = re.search(r"<v>(.*?)</v>", body, re.S)
                if a.get("t") == "s" and v and v.group(1).isdigit() and int(v.group(1)) < len(items):
                    out.append(items[int(v.group(1))])
                elif a.get("t") == "inlineStr":
                    out.append(_runs(body))
                elif v:
                    out.append(html.unescape(v.group(1)))
                out += [html.unescape(x) for x in re.findall(r"<f\b[^>]*>(.*?)</f>", body, re.S)]
        hf = re.search(r"<headerFooter\b.*?</headerFooter>", xml, re.S)
        if hf:
            out.append(plain(hf.group(0)))  # 印刷すると見える
        # 見えているシートの図形・グラフの文字（タイトル・軸・テキストボックス）
        for _r, ty, d in pkg.internal(s["path"], {"drawing"}):
            parts = [d] + [t for _r2, _t2, t in pkg.internal(d, {"chart", "diagramData"})]
            out += [_runs(pkg.text(p) or "") for p in parts]
            out += [_norm(x) for p in parts for x in re.findall(r"<a:t>(.*?)</a:t>", pkg.text(p) or "", re.S)]
    return [x for x in out if x]


def visible_text_pptx(pkg):
    pres = main_part(pkg)
    out, seen = [], set()
    for s in pres_slides(pkg, pres):
        if s["hidden"]:
            continue
        parts = [s["path"]]
        for _r, ty, t in pkg.internal(s["path"]):
            if ty in ("chart", "diagramData", "slideLayout"):
                parts.append(t)
                if ty == "slideLayout":
                    parts += [m for _r2, t2, m in pkg.internal(t, {"slideMaster"})]
        for p in parts:
            if p in seen:
                continue
            seen.add(p)
            xml = pkg.text(p) or ""
            out += [_norm(x) for x in re.findall(r"<a:t>(.*?)</a:t>", xml, re.S)]
            out += [_runs(m) for m in re.findall(r"<a:p>.*?</a:p>", xml, re.S)]  # 段落ごとにつないだ文字
    return [x for x in out if x]


def text_candidates(name, xml):
    """部品の中の文字の候補（自由な文字の属性と、葉の要素の中身）。"""
    xml = re.sub(r"<rPh\b.*?</rPh>|<HeadingPairs\b.*?</HeadingPairs>|<xcalcf:calcFeatures\b.*?</xcalcf:calcFeatures>", "", xml, flags=re.S)  # calcFeatures: Excel が書く計算機能の一覧（microsoft.com:RD など）
    out = []
    for m in _OPEN_RE.finditer(xml):
        tag = m.group(1)
        for k, v in _ATTR_RE.findall(m.group(2)):
            if (k, None) in _FREE_ATTRS or (k, tag.split(":")[-1]) in _FREE_ATTRS or (k, tag) in _FREE_ATTRS:
                if k == "name" and tag in ("p:cSld", "cSld"):
                    continue  # レイアウトの名前（テンプレートの既定）
                out.append(_norm(v))
    for m in _LEAF_RE.finditer(xml):
        tag, body = m.group(1), m.group(2)
        if tag in _STRUCT_ELEMS:
            continue
        if tag in _FORMULA_ELEMS:
            out += [_norm(x) for x in _formula_bits(body)]
        else:
            out.append(_norm(body))
    # 書式で割れた文字（<r> ごとの <t>）は、文字列・段落の単位でつないでも調べる
    out += [_norm(_runs(m)) for m in re.findall(r"<si\b.*?</si>|<is\b.*?</is>|<a:p>.*?</a:p>", xml, re.S)]
    return out


def check_text(pkg, ext, fs):
    vis = visible_text_xlsx(pkg) if ext in (".xlsx", ".xlsm") else visible_text_pptx(pkg)
    joined = "\x00".join(_norm(x) for x in vis)
    for n in pkg.order:
        if n not in pkg.parts or not n.lower().endswith(XML_EXT) or _STRUCT_PART_RE.search(n):
            continue
        miss = []
        for s in text_candidates(n, pkg.text(n) or ""):
            if (not s or s in FIXED_WORDS or _STRUCT_TEXT_RE.match(s) or _AUTO_NAME_RE.match(s)
                    or s in joined or s in miss):
                continue
            miss.append(s)
        if miss:
            fs.append(Finding("unseen-text", n, f"見えている文字に当たらない文字（{len(miss)} 種類。ここに出ないものは、"
                              "見えている文字か固定語に当たった）", miss))


def check(pkg, ext):
    fs = []
    check_common(pkg, fs)
    if ext in (".xlsx", ".xlsm"):
        check_xlsx(pkg, fs)
    else:
        check_pptx(pkg, fs)
    check_text(pkg, ext, fs)
    return fs


# ---------- 掃除: xlsx ----------

def drop_formulas(xml, pats):
    """消したシートを参照する数式を外し、キャッシュの値だけを残す。共有の数式は、同じ si をまとめて外す。"""
    n = 0
    shared = set()
    f_re = re.compile(r"<f\b([^>]*?)(?:/>|>(.*?)</f>)", re.S)
    for m in f_re.finditer(xml):
        if any(p.search(_unesc(m.group(2) or "", _XML_UNESC)) for p in pats):
            a = attrs(m.group(1))
            if a.get("t") == "shared" and "si" in a:
                shared.add(a["si"])

    def sub(m):
        nonlocal n
        a = attrs(m.group(1) or "")
        body = m.group(2) or ""
        if any(p.search(_unesc(body, _XML_UNESC)) for p in pats) or (a.get("t") == "shared" and a.get("si") in shared):
            n += 1
            return ""
        return m.group(0)
    xml = f_re.sub(sub, xml)
    return xml, n


def clean_xlsx(pkg, actions, log):
    wb = main_part(pkg)
    t = pkg.text(wb) or ""
    sheets = wb_sheets(pkg, wb)
    if "hidden-sheets" in actions:
        gone = [s for s in sheets if s["state"] != "visible"]
        if gone and len(gone) == len(sheets):
            raise CleanError("すべてのシートが非表示なので、消すと空になる（--keep hidden-sheets で外す）")
        if gone:
            old_idx = {s["name"]: i for i, s in enumerate(sheets)}
            keep = [s for s in sheets if s["state"] == "visible"]
            new_idx = {old_idx[s["name"]]: i for i, s in enumerate(keep)}
            pats = [sheet_ref_re(s["name"]) for s in gone]
            for s in gone:
                t = t.replace(s["tag"], "")
                pkg.drop_rel(wb, s["rid"])
                pkg.remove(s["path"])
            # 定義名: 消したシートのもの・消したシートを参照するものを外し、localSheetId を付け替える
            def dn(m):
                a = attrs(m.group(1))
                lid = a.get("localSheetId")
                if lid is not None and int(lid) not in new_idx:
                    return ""
                if any(p.search(_unesc(m.group(2), _XML_UNESC)) for p in pats):
                    return ""
                if lid is not None:
                    return m.group(0).replace(f'localSheetId="{lid}"', f'localSheetId="{new_idx[int(lid)]}"', 1)
                return m.group(0)
            before = len(re.findall(r"<definedName\b", t))
            t = re.sub(r"<definedName\b([^>]*)>(.*?)</definedName>", dn, t, flags=re.S)
            t = re.sub(r"<definedNames>\s*</definedNames>", "", t)
            dropped_names = before - len(re.findall(r"<definedName\b", t))

            def view(m):
                tag = m.group(0)
                for k in ("activeTab", "firstSheet"):
                    a = attrs(tag)
                    if k in a:
                        tag = tag.replace(f'{k}="{a[k]}"', f'{k}="{new_idx.get(int(a[k]), 0)}"', 1)
                return tag
            t = re.sub(r"<workbookView\b[^>]*/?>", view, t)
            nf = 0
            for s in keep:
                x, c = drop_formulas(pkg.text(s["path"]) or "", pats)
                if c:
                    pkg.put(s["path"], x)
                    nf += c
            log.append(f"非表示シートを消した: {len(gone)} 件（定義名 {dropped_names} 件を外し、数式 {nf} 個を値にした）")
            if nf and "calcchain" not in actions:
                actions = set(actions) | {"calcchain"}
                log.append("数式を値にしたので、calcChain も外した")
            sheets = keep
    if "external-links" in actions:
        ext_ids = [(rid, tgt) for rid, _ty, tgt in pkg.internal(wb, {"externalLink"})]
        if ext_ids:
            pats = [re.compile(r"\[\d+\]")]
            nf = 0
            for s in sheets:
                x, c = drop_formulas(pkg.text(s["path"]) or "", pats)
                if c:
                    pkg.put(s["path"], x)
                    nf += c
            before = len(re.findall(r"<definedName\b", t))
            t = re.sub(r"<definedName\b[^>]*>[^<]*\[\d+\][^<]*</definedName>", "", t)
            t = re.sub(r"<definedNames>\s*</definedNames>", "", t)
            t = re.sub(r"<externalReferences>.*?</externalReferences>", "", t, flags=re.S)
            for rid, tgt in ext_ids:
                pkg.drop_rel(wb, rid)
                pkg.remove(tgt)
            after_n = len(re.findall(r"<definedName\b", t))
            log.append(f"外部ブックへのリンクを切った: {len(ext_ids)} 件（数式 {nf} 個を値にし、定義名 {before - after_n} 件を外した）")
            if nf:
                actions = set(actions) | {"calcchain"}
    if "ref-names" in actions:
        t2 = re.sub(r"<definedName\b[^>]*>[^<]*#REF![^<]*</definedName>", "", t)
        t2 = re.sub(r"<definedNames>\s*</definedNames>", "", t2)
        if t2 != t:
            log.append(f"参照先が無い定義名を消した: {len(re.findall(r'<definedName\b', t)) - len(re.findall(r'<definedName\b', t2))} 件")
        t = t2
    if "hidden-names" in actions:
        def hn(m):
            a = attrs(m.group(1))
            return "" if a.get("hidden") in ("1", "true") and not a.get("name", "").startswith("_xl") else m.group(0)
        t2 = re.sub(r"<definedName\b([^>]*)>.*?</definedName>", hn, t, flags=re.S)
        t2 = re.sub(r"<definedNames>\s*</definedNames>", "", t2)
        if t2 != t:
            log.append(f"非表示の定義名を消した: {len(re.findall(r'<definedName\b', t)) - len(re.findall(r'<definedName\b', t2))} 件")
        t = t2
    if "abspath" in actions:
        t2 = re.sub(r"<mc:AlternateContent\b[^>]*>(?:(?!</mc:AlternateContent>).)*?x15ac:absPath(?:(?!</mc:AlternateContent>).)*?</mc:AlternateContent>",
                    "", t, flags=re.S)
        t2 = re.sub(r"<x15ac:absPath\b[^>]*/>", "", t2)
        if t2 != t:
            log.append("保存場所の絶対パスを消した")
        t = t2
    pkg.put(wb, t)
    if "calcchain" in actions and pkg.drop_rels_of(wb, {"calcChain"}):
        log.append("calcChain を外した")
    if "revisions" in actions and pkg.drop_rels_of(wb, {"revisionHeaders", "usernames"}):
        log.append("変更履歴を外した")
    for s in sheets:
        p = s["path"]
        st = pkg.text(p) or ""
        if "comments" in actions:
            d = pkg.drop_rels_of(p, {"comments", "threadedComment"})
            for rid, _ty, tgt in pkg.internal(p, {"vmlDrawing"}) if d else []:
                types = set(re.findall(r'ObjectType="(\w+)"', pkg.text(tgt) or ""))
                if types <= {"Note"}:  # コメントの枠だけの VML（フォームのコントロールが無い）
                    pkg.drop_rel(p, rid)
                    st = re.sub(rf'<legacyDrawing\b[^>]*r:id="{re.escape(rid)}"[^>]*/>', "", st)
            if d:
                log.append(f"「{s['name']}」のコメントを外した")
        if "hidden-rows" in actions or "hidden-cols" in actions:
            st, nh = blank_hidden(st, "hidden-rows" in actions, "hidden-cols" in actions)
            if nh:
                log.append(f"「{s['name']}」の非表示の行・列のセル {nh} 個の中身を空にした")
        if "printer" in actions:
            for rid, _tgt in pkg.drop_rels_of(p, {"printerSettings"}):
                st = re.sub(rf'\s+r:id="{re.escape(rid)}"', "", st)
                log.append(f"「{s['name']}」のプリンター設定を外した")
        pkg.put(p, st)
    if "comments" in actions and pkg.drop_rels_of(wb, {"person"}):
        log.append("コメントの作成者（persons）を外した")
    if "shared-strings" in actions:
        shrink_sst(pkg, wb, [s["path"] for s in sheets], log)


def col_num(ref):
    n = 0
    for ch in re.match(r"[A-Za-z]+", ref).group(0).upper():
        n = n * 26 + ord(ch) - 64
    return n


def hidden_cols(xml):
    out = set()
    for m in re.finditer(r"<col\b[^>]*>", xml):
        a = attrs(m.group(0))
        if a.get("hidden") in ("1", "true"):
            out.update(range(int(a.get("min", 0)), min(int(a.get("max", 0)), 16384) + 1))
    return out


def _has_content(body):
    return bool(re.search(r"<v>|<is>|<f\b", body or ""))


def hidden_content(xml):
    """非表示の行・列にある、中身の入ったセルの数（行, 列）。"""
    hc, rows, cols = hidden_cols(xml), 0, 0
    for r in re.finditer(_ROW_PAT, xml, re.S):
        hr = attrs(r.group(1)).get("hidden") in ("1", "true")
        for c in re.finditer(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", r.group(2) or "", re.S):
            if not _has_content(c.group(2)):
                continue
            if hr:
                rows += 1
            elif col_num(attrs(c.group(1)).get("r", "A1")) in hc:
                cols += 1
    return rows, cols


_ROW_PAT = r"<row\b([^>]*?)(?:/>|>(.*?)</row>)"  # 空の行 <row .../> を次の行と一緒に読まない
_F_RE = re.compile(r"<f\b([^>]*?)(?:/>|>.*?</f>)", re.S)
_CELL_RE = re.compile(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", re.S)


def blank_hidden(xml, do_rows, do_cols):
    """非表示の行・列のセルから、値・文字・数式を外す。書式とセルは残す。
    共有数式の親（ref を持つ f）は、空にならないセルがまだ使っているときだけ残す（残すと子が壊れるため）。"""
    hc = hidden_cols(xml) if do_cols else set()
    rows = [(m, do_rows and attrs(m.group(1)).get("hidden") in ("1", "true")) for m in re.finditer(_ROW_PAT, xml, re.S)]

    def target(hr, c):
        return (hr or col_num(attrs(c.group(1)).get("r", "A1")) in hc) and _has_content(c.group(2))
    used = set()
    for m, hr in rows:
        for c in _CELL_RE.finditer(m.group(2) or ""):
            if not target(hr, c):
                for f in _F_RE.finditer(c.group(2) or ""):
                    fa = attrs(f.group(1))
                    if fa.get("t") == "shared":
                        used.add(fa.get("si"))
    n = 0

    def row(m):
        nonlocal n
        hr = do_rows and attrs(m.group(1)).get("hidden") in ("1", "true")

        def cell(c):
            nonlocal n
            if not target(hr, c):
                return c.group(0)
            n += 1
            a, body = c.group(1), c.group(2) or ""
            body = re.sub(r"<v>.*?</v>|<is>.*?</is>", "", body, flags=re.S)

            def f(fm):
                fa = attrs(fm.group(1))
                return fm.group(0) if fa.get("t") == "shared" and "ref" in fa and fa.get("si") in used else ""
            body = _F_RE.sub(f, body)
            a = re.sub(r'\s+t="[^"]*"', "", a)
            return f"<c{a}>{body}</c>" if body else f"<c{a}/>"
        if m.group(2) is None:
            return m.group(0)
        return "<row" + m.group(1) + ">" + _CELL_RE.sub(cell, m.group(2)) + "</row>"
    xml = re.sub(_ROW_PAT, row, xml, flags=re.S)
    return xml, n


def shrink_sst(pkg, wb, paths, log):
    sst = [tgt for _rid, ty, tgt in pkg.internal(wb, {"sharedStrings"})]
    if not sst or not pkg.has(sst[0]):
        return
    t = pkg.text(sst[0]) or ""
    items = list(re.finditer(r"<si\b[^>]*?(?:/>|>.*?</si>)", t, re.S))
    used = used_sst(pkg, paths)
    if any(i >= len(items) for i in used):
        log.append("共有文字列は詰めなかった（範囲の外の番号を指すセルがある。元のファイルが壊れている）")
        return
    if len(used) == len(items):
        return
    remap = {old: new for new, old in enumerate(sorted(i for i in used if i < len(items)))}
    body = "".join(items[i].group(0) for i in sorted(remap))
    head = t[:items[0].start()] if items else t
    tail = t[items[-1].end():] if items else ""
    head = re.sub(r'\buniqueCount="\d+"', f'uniqueCount="{len(remap)}"', head)
    pkg.put(sst[0], head + body + tail)

    def cell(m):
        if attrs(m.group(1)).get("t") != "s":
            return m.group(0)
        return re.sub(r"<v>(\d+)</v>", lambda v: f"<v>{remap[int(v.group(1))]}</v>", m.group(0))
    for p in paths:
        pkg.put(p, _CELL_RE.sub(cell, pkg.text(p) or ""))
    log.append(f"使っていない共有文字列を消した: {len(items) - len(remap)} 件")


# ---------- 掃除: pptx ----------

def clean_pptx(pkg, actions, log):
    pres = main_part(pkg)
    t = pkg.text(pres) or ""
    slides = pres_slides(pkg, pres)
    if "hidden-slides" in actions:
        gone = [s for s in slides if s["hidden"]]
        if gone and len(gone) == len(slides):
            raise CleanError("すべてのスライドが非表示なので、消すと空になる（--keep hidden-slides で外す）")
        for s in gone:
            t = t.replace(s["tag"], "")
            pkg.drop_rel(pres, s["rid"])
            pkg.remove(s["path"])
            t = re.sub(rf'<p14:sldId\b[^>]*\bid="{re.escape(s["id"])}"[^>]*/>', "", t)
            t = re.sub(rf'<p:sld\b[^>]*r:id="{re.escape(s["rid"])}"[^>]*/>', "", t)
        if gone:
            log.append(f"非表示スライドを消した: {len(gone)} 件")
        slides = [s for s in slides if not s["hidden"]]
    pkg.put(pres, t)
    if "printer" in actions and pkg.drop_rels_of(pres, {"printerSettings"}):
        log.append("プリンター設定を外した")
    for s in slides:
        if "notes" in actions and pkg.drop_rels_of(s["path"], {"notesSlide"}):
            log.append(f"ノートを外した: {s['path']}")
        if "comments" in actions and pkg.drop_rels_of(s["path"], {"comments"}):
            log.append(f"コメントを外した: {s['path']}")
    if "comments" in actions and pkg.drop_rels_of(pres, {"commentAuthors", "authors"}):
        log.append("コメントの作成者を外した")


# ---------- 掃除: 共通 ----------

def clean_common(pkg, actions, log):
    if "props" in actions:
        core = pkg.text("docProps/core.xml")
        if core is not None:
            for tag in ("dc:creator", "cp:lastModifiedBy", "dc:title", "dc:subject", "cp:keywords",
                        "dc:description", "cp:category", "cp:contentStatus"):
                core = re.sub(rf"(<{tag}\b[^>]*>).*?(</{tag}>)", r"\1\2", core, flags=re.S)
            pkg.put("docProps/core.xml", core)
        app = pkg.text("docProps/app.xml")
        if app is not None:
            for tag in ("Company", "Manager", "HyperlinkBase"):
                app = re.sub(rf"(<{tag}\b[^>]*>).*?(</{tag}>)", r"\1\2", app, flags=re.S)
            app = re.sub(r"<(HeadingPairs|TitlesOfParts)\b.*?</\1>", "", app, flags=re.S)
            pkg.put("docProps/app.xml", app)
        pkg.drop_rels_of("", {"custom-properties"})
        log.append("文書プロパティの個人情報を空にした")
    if "thumbnail" in actions and pkg.drop_rels_of("", {"thumbnail"}):
        log.append("縮小画像を外した")


def strip_refs(xml, rid):
    """参照元の XML から、関係 rid を使う要素を外す（関係だけ消すと参照が宙に浮く）。"""
    ref = rf'(?:r:(?:id|embed|link|pict)|o:relid)="{re.escape(rid)}"'
    flags = re.S
    xml = re.sub(rf'<xdr:(\w*Anchor)\b(?:(?!</xdr:\1>).)*?{ref}.*?</xdr:\1>', "", xml, flags=flags)
    xml = re.sub(rf'<p:(graphicFrame|pic)\b(?:(?!</p:\1>).)*?{ref}.*?</p:\1>', "", xml, flags=flags)
    xml = re.sub(rf'<mc:AlternateContent\b(?:(?!</mc:AlternateContent>).)*?<oleObject\b[^>]*{ref}.*?</mc:AlternateContent>', "", xml, flags=flags)
    xml = re.sub(rf'<oleObject\b[^>]*{ref}[^>]*(?:/>|>.*?</oleObject>)', "", xml, flags=flags)
    xml = re.sub(rf'<(picture|pivotCache)\b[^>]*{ref}[^>]*/>', "", xml)
    xml = re.sub(r"<(oleObjects|pivotCaches)>\s*</\1>", "", xml)
    return re.sub(rf'\s+(?:r:(?:id|embed|link|pict)|o:relid)="{re.escape(rid)}"', "", xml)


def strip_kinds(pkg, kinds, log):
    types = {t: k for k in kinds for t in STRIP_KINDS[k][1]}
    counts = {}
    for n in list(pkg.order):
        if n not in pkg.parts or not n.endswith(".rels"):
            continue
        src = "" if n == "_rels/.rels" else re.sub(r"(^|/)_rels/([^/]+)\.rels$", r"\1\2", n)
        for rid, ty, _tgt in pkg.internal(src, set(types)):
            xml = pkg.text(src) if src else None
            if xml is not None and src.lower().endswith(XML_EXT):
                pkg.put(src, strip_refs(xml, rid))
            pkg.drop_rel(src, rid)
            counts[types[ty]] = counts.get(types[ty], 0) + 1
    for k, c in counts.items():
        log.append(f"{STRIP_KINDS[k][0].split('（')[0]}を外した: 関係 {c} 件")


def clean(data, ext, actions):
    pkg = Pkg(data)
    if pkg.dups:
        raise CleanError("同じ名前のエントリーが複数ある zip は掃除しない（どちらが読まれるかがアプリで違う）")
    log = []
    kinds = [k for k in STRIP_KINDS if k in actions]
    if kinds:
        actions = set(actions) | {"orphans"}  # 外した部品の本体を消すのに要る
    if ext in (".xlsx", ".xlsm"):
        clean_xlsx(pkg, set(actions), log)
    else:
        clean_pptx(pkg, set(actions), log)
    clean_common(pkg, set(actions), log)
    if kinds:
        strip_kinds(pkg, kinds, log)
    if "orphans" in actions:
        orph = pkg.orphans()
        for n in orph:
            pkg.remove(n)
        if orph:
            log.append(f"関係からたどれない部品を消した: {len(orph)} 件")
    return pkg.tobytes(), log


def integrity(data):
    """掃除後の最低限の整合: XML が読める、内部の関係の先がある、型（Content_Types）がある。"""
    pkg = Pkg(data)
    probs = []
    ct = pkg.text("[Content_Types].xml") or ""
    defaults = {attrs(m).get("Extension", "").lower() for m in re.findall(r"<Default\b[^>]*/>", ct)}
    overrides = {attrs(m).get("PartName", "").lstrip("/") for m in re.findall(r"<Override\b[^>]*/>", ct)}
    for n in pkg.order:
        if n not in pkg.parts:
            continue
        if n.lower().endswith(XML_EXT) and not n.lower().endswith(".vml"):
            try:
                ET.fromstring(pkg.parts[n])
            except ET.ParseError as e:
                probs.append(f"{n}: XML として読めない（{e}）")
        if n != "[Content_Types].xml" and n not in overrides and n.rsplit(".", 1)[-1].lower() not in defaults:
            probs.append(f"{n}: 型が無い")
        if n.endswith(".rels"):
            src = re.sub(r"(^|/)_rels/([^/]+)\.rels$", r"\1\2", n)
            src = "" if n == "_rels/.rels" else src
            for _rid, _ty, tgt in pkg.internal(src):
                if tgt not in pkg.parts:
                    probs.append(f"{n}: 関係の先が無い（{tgt}）")
    for o in overrides:
        if o not in pkg.parts:
            probs.append(f"[Content_Types].xml: 無い部品の型（{o}）")
    # 共有文字列の番号が範囲の中か（外れると Excel が「読み取れない内容」として修復する）
    sst = [n for n in pkg.order if re.match(r"xl/sharedStrings[^/]*\.xml$", n) and n in pkg.parts]
    if sst:
        size = len(re.findall(r"<si\b", pkg.text(sst[0]) or ""))
        for n in pkg.order:
            if n in pkg.parts and re.match(r"xl/worksheets/[^/]+\.xml$", n):
                bad = used_sst(pkg, [n]) - set(range(size))
                if bad:
                    probs.append(f"{n}: 共有文字列の番号が範囲の外（{len(bad)} 個。文字列は {size} 件）")
    return probs


# ---------- 報告 ----------

def report_md(src, fs, log=None, after=None, probs=None, out=None):
    L = [f"# cleankit の報告: {Path(src).name}", "",
         "この報告には、ファイルに残っていた実データの抜粋が載る。AI に見せない場所に置く。", ""]
    if log is not None:
        L += [f"## 掃除したこと（出力: {Path(out).name}）", ""] + [f"- {x}" for x in log or ["（なし）"]] + [""]
        L += ["## 出力の整合", ""] + ([f"- {p}" for p in probs] or ["- 問題なし"]) + [""]
    sections = [("元のファイルに残っていたもの", fs)] if after is None else [("元のファイルに残っていたもの", fs), ("掃除の後も残っているもの（人が確かめる）", after)]
    for title, items in sections:
        L += [f"## {title}", ""]
        if not items:
            L += ["- なし", ""]
        for f in items:
            L.append(f"- `{f.code}` {f.part + ': ' if f.part else ''}{f.detail}")
            L += [f"  - {s}" for s in f.samples]
        L.append("")
    return "\n".join(L)


def summary(fs):
    c = {}
    for f in fs:
        c[f.code] = c.get(f.code, 0) + 1
    return ", ".join(f"{k} {v}" for k, v in c.items()) or "なし"


def repo_root(path):
    """path に最も近い、.git のある祖先（無ければ None）。"""
    p = Path(path).resolve()
    for d in (p, *p.parents):
        if (d / ".git").exists():
            return d
    return None


def guard_outputs(*paths):
    """出力と報告を、この kit を含むリポジトリ（公開）の中に書かない。報告は実データを含む。"""
    mine = repo_root(__file__)
    for p in paths:
        if mine is not None and repo_root(Path(p).parent if not Path(p).is_dir() else p) == mine:
            raise CleanError(f"出力先がこのリポジトリ（公開）の中: {p}。_noai/ など、リポジトリの外か追跡しない場所を指定する")


def read_input(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext not in SUPPORTED:
        raise CleanError(f"対象外の形式: {ext}（対象: {' '.join(SUPPORTED)}）")
    if not p.is_file():
        raise CleanError(f"ファイルが無い: {p}")
    return p, ext, p.read_bytes()


def main(argv=None):
    ap = argparse.ArgumentParser(description="xlsx・pptx の残存情報の点検（check）と掃除（clean）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="残っている情報を一覧にする（ファイルは変えない）")
    c.add_argument("file")
    c.add_argument("--report", help="報告の md（既定: 入力の隣の <名前>.check-report.md）")
    k = sub.add_parser("clean", help="掃除した別ファイルを書く")
    k.add_argument("file")
    k.add_argument("out", help="出力のファイル、またはディレクトリ")
    k.add_argument("--keep", default="", help="外さない動作（カンマ区切り）: " + ", ".join(CLEAN_ACTIONS))
    k.add_argument("--also", default="", help="既定では行わない動作を足す（カンマ区切り）: " + ", ".join(OPTIONAL_ACTIONS))
    k.add_argument("--profile", default="standard", choices=list(PROFILES), help="掃除の強さ: " + "; ".join(f"{n} = {d}" for n, (d, _x) in PROFILES.items()))
    k.add_argument("--allow", default="", help="プロファイルが外す部品の種類のうち、残すもの（カンマ区切り）: " + ", ".join(STRIP_KINDS))
    k.add_argument("--report", help="報告の md（既定: 出力の隣の <名前>.clean-report.md）")
    k.add_argument("--force", action="store_true", help="出力が既にあれば上書きする")
    sub.add_parser("profiles", help="プロファイルと、部品の種類・動作の一覧を出す")
    a = ap.parse_args(argv)
    if a.cmd == "profiles":
        print("プロファイル（clean --profile <名前>）")
        for n, (d, extra) in PROFILES.items():
            print(f"  {n}: {d}\n    足す動作: {', '.join(extra) or 'なし'}")
        print("\n部品の種類（プロファイルが外す。--allow で残す）")
        for n, (d, _t) in STRIP_KINDS.items():
            print(f"  {n}: {d}")
        print("\n既定の掃除（--keep で外す）")
        for n, d in CLEAN_ACTIONS.items():
            print(f"  {n}: {d}")
        print("\n任意の動作（--also で足す）")
        for n, d in OPTIONAL_ACTIONS.items():
            print(f"  {n}: {d}")
        return 0
    try:
        src, ext, data = read_input(a.file)
        if a.cmd == "check":
            fs = check(Pkg(data), ext)
            rep = Path(a.report) if a.report else src.with_name(src.name + ".check-report.md")
            guard_outputs(rep)
            rep.write_text(report_md(src, fs), encoding="utf-8")
            print(f"点検: {src.name}: {len(fs)} 件（{summary(fs)}）")
            probs = integrity(data)
            if probs:
                print(f"整合の問題: {len(probs)} 件（{'; '.join(p.split(':')[0] for p in probs[:3])}。Excel が修復を求めることがある）")
            print(f"報告: {rep}（実データの抜粋が載る。AI に見せない）")
            return 1 if (fs or probs) else 0
        keep = {x.strip() for x in a.keep.split(",") if x.strip()}
        bad = keep - set(CLEAN_ACTIONS)
        if bad:
            raise CleanError(f"知らない動作: {', '.join(sorted(bad))}")
        out = Path(a.out)
        if out.is_dir() or out.suffix.lower() not in SUPPORTED:
            out = out / src.name  # 拡張子が対象の形式でなければ、ディレクトリとみなす
        if out.resolve() == src.resolve():
            raise CleanError("出力が元のファイルと同じ（元のファイルは変えない）")
        if out.exists() and not a.force:
            raise CleanError(f"出力が既にある: {out}（--force で上書き）")
        rep = Path(a.report) if a.report else out.with_name(out.name + ".clean-report.md")
        guard_outputs(out, rep)
        also = {x.strip() for x in a.also.split(",") if x.strip()}
        if also - set(OPTIONAL_ACTIONS):
            raise CleanError(f"知らない動作: {', '.join(sorted(also - set(OPTIONAL_ACTIONS)))}")
        allow = {x.strip() for x in a.allow.split(",") if x.strip()}
        if allow - set(STRIP_KINDS):
            raise CleanError(f"知らない部品の種類: {', '.join(sorted(allow - set(STRIP_KINDS)))}")
        also |= set(PROFILES[a.profile][1]) - allow
        actions = [x for x in CLEAN_ACTIONS if x not in keep] + sorted(also)
        before = check(Pkg(data), ext)
        cleaned, log = clean(data, ext, actions)
        probs = integrity(cleaned)
        after = check(Pkg(cleaned), ext)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(cleaned)
        rep.write_text(report_md(src, before, log, after, probs, out), encoding="utf-8")
        print(f"掃除: {src.name} → {out}（{len(log)} 項目）")
        print(f"残り: {len(after)} 件（{summary(after)}）")
        if probs:
            print(f"整合の問題: {len(probs)} 件（報告を見る。出力を AI に渡さない）")
        print(f"報告: {rep}（実データの抜粋が載る。AI に見せない）")
        return 1 if (after or probs) else 0
    except CleanError as e:
        print(f"止めた: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
