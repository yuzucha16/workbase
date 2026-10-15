"""maskkit: マスクと復元（標準ライブラリだけ）。

人が実行する（`room.py` から呼ばれる）。AI には実行させない（原本と対応表を読むため）。
仕様は topics/ai-workspace-boundary/notes/ai-room-mask-spec.md（引き継ぎ中）。

- mask.toml（人が書く）: 種類ごとの語と表記ゆれ、列の指定
- mapping.json（このモジュールが書く。追記専用）: プレースホルダーの番号と正式名
- csv と xlsx を対象に、全部の語を1回の走査で、長い語を優先して置換する
- 復元は ai/out の既知の形式だけ。戻らなかったものがあれば、何も書かずに止める
"""
import csv
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as _esc, unescape as _unesc
import xml.etree.ElementTree as ET

try:
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None


class MaskError(Exception):
    pass


KIND_RE = re.compile(r"^[A-Z][A-Z0-9]*$")
NAME_KINDS = ("SHEET", "NAME")  # 定義名・シート名に使える ASCII のプレースホルダー
TEXT_EXT = (".csv", ".md", ".txt", ".bas", ".json", ".html")
XML_EXT = (".xml", ".rels", ".vml")
MIN_LEN = 2  # 1文字の語は、置換が広がりすぎるので受け付けない

PH_RE = re.compile(r"⟦([A-Z][A-Z0-9]*)_(\d{3,})⟧|(?<![A-Za-z0-9_])((?:SHEET|NAME)_\d{3,})(?![A-Za-z0-9_])")
BROKEN_PH_RE = re.compile(r"[⟦⟧]")

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
_XML_UNESC = {"&quot;": '"', "&apos;": "'", "&#39;": "'"}


def placeholder(kind, n):
    return f"{kind}_{n:03d}" if kind in NAME_KINDS else f"⟦{kind}_{n:03d}⟧"


def norm(s):
    return unicodedata.normalize("NFKC", s).casefold()


def xml_unescape(s):
    return _unesc(s, _XML_UNESC)


def xml_escape(s):
    return _esc(s, {'"': "&quot;"})


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


# ---------- 設定（mask.toml） ----------

class Config:
    def __init__(self, terms, columns):
        self.terms = terms      # {kind: {key: [variants...]}}
        self.columns = columns  # {"シート!列名": kind}


def load_config(path):
    path = Path(path)
    if not path.exists():
        raise MaskError(f"mask.toml が無い: {path}")
    if tomllib is None:
        raise MaskError("tomllib が使えない（Python 3.11 以上が要る）")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    terms, columns = {}, {}
    for kind, group in (data.get("terms") or {}).items():
        if not KIND_RE.match(kind):
            raise MaskError(f"[terms.{kind}] の種類は英大文字と数字だけ（例: CUST）")
        if kind in NAME_KINDS:
            raise MaskError(f"[terms.{kind}] は予約（シート名・定義名用）。別の種類名にする")
        for key, variants in group.items():
            if isinstance(variants, str):
                variants = [variants]
            variants = [v for v in variants if v]
            if not variants:
                raise MaskError(f"[terms.{kind}] {key}: 語が空")
            for v in variants:
                if len(v) < MIN_LEN:
                    raise MaskError(f"[terms.{kind}] {key}: 語は{MIN_LEN}文字以上（短い語は置換が広がりすぎる）: {v!r}")
            terms.setdefault(kind, {})[key] = variants
    for col, kind in (data.get("columns") or {}).items():
        if "!" not in col:
            raise MaskError(f'[columns] のキーは "シート名!列名" の形: {col!r}')
        if not KIND_RE.match(kind) or kind in NAME_KINDS:
            raise MaskError(f"[columns] {col}: 種類名が不正: {kind!r}")
        columns[col] = kind
    return Config(terms, columns)


# ---------- 対応表（mapping.json。追記専用） ----------

class Mapping:
    def __init__(self, data=None):
        self.data = data or {"version": 1, "counters": {}, "entries": {}}

    @classmethod
    def load(cls, path):
        path = Path(path)
        if path.exists():
            return cls(json.loads(path.read_text(encoding="utf-8")))
        return cls()

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    def ensure(self, kind, key, variants):
        ents = self.data["entries"].setdefault(kind, {})
        e = ents.get(key)
        if e is None:
            n = self.data["counters"].get(kind, 0) + 1
            self.data["counters"][kind] = n
            e = {"id": n, "canonical": variants[0], "variants": list(variants)}
            ents[key] = e
        else:
            e["canonical"] = variants[0]
            for v in variants:
                if v not in e["variants"]:
                    e["variants"].append(v)
        return e

    def entries(self):
        for kind, group in self.data["entries"].items():
            for key, e in group.items():
                yield kind, key, e

    def by_placeholder(self):
        return {placeholder(kind, e["id"]): e for kind, _k, e in self.entries()}


# ---------- 置換表（正規表現） ----------

_FULL = {chr(c): chr(c + 0xFEE0) for c in range(0x21, 0x7F)}
_FULL[" "] = "　"
_HALF_KANA = {}
for _cp in range(0xFF61, 0xFFA0):
    _h = chr(_cp)
    _f = unicodedata.normalize("NFKC", _h)
    if _f != _h and len(_f) == 1:
        _HALF_KANA.setdefault(_f, _h)
_XML_ENT = {"&": ("&amp;",), "<": ("&lt;",), ">": ("&gt;",), '"': ("&quot;",), "'": ("&apos;", "&#39;")}


def _piece(c, xml):
    fs = {c, c.lower(), c.upper()}
    n = unicodedata.normalize("NFKC", c)
    fs |= {n, n.lower(), n.upper()}
    for f in list(fs):
        if len(f) == 1:
            if f in _FULL:
                fs.add(_FULL[f])
            if f in _HALF_KANA:
                fs.add(_HALF_KANA[f])
    if xml:
        for f in list(fs):
            fs.update(_XML_ENT.get(f, ()))
    singles = sorted(f for f in fs if len(f) == 1)
    multis = sorted((f for f in fs if len(f) > 1), key=lambda s: (-len(s), s))
    cls = None
    if len(singles) == 1:
        cls = re.escape(singles[0])
    elif singles:
        cls = "[" + "".join(re.escape(s) for s in singles) + "]"
    parts = [re.escape(m) for m in multis] + ([cls] if cls else [])
    return parts[0] if len(parts) == 1 else "(?:" + "|".join(parts) + ")"


def _variant_regex(v, xml):
    return "".join(_piece(c, xml) for c in v)


class Table:
    """mapping の全ての表記ゆれを、1つの正規表現にまとめる（長い語を優先）。"""

    def __init__(self, mapping):
        self.lookup = {}
        variants = []
        for kind, key, e in mapping.entries():
            ph = placeholder(kind, e["id"])
            for v in e["variants"]:
                k = norm(v)
                prev = self.lookup.get(k)
                if prev is not None and prev != ph:
                    # シート名・定義名（ASCII）は、本文の語より優先する（名前に ⟦ ⟧ は使えないため）
                    if ph.startswith(NAME_KINDS):
                        pass
                    elif prev.startswith(NAME_KINDS):
                        continue
                    else:
                        raise MaskError(f"同じ語が2つの項目にある: {v!r}（{prev} と {ph}）")
                self.lookup[k] = ph
                variants.append(v)
        variants = sorted(set(variants), key=lambda s: (-len(s), s))
        self._rx = {}
        for xml in (False, True):
            self._rx[xml] = (re.compile("|".join(_variant_regex(v, xml) for v in variants), re.IGNORECASE)
                             if variants else None)

    def mask_text(self, text, xml=False):
        rx = self._rx[xml]
        if rx is None:
            return text

        def repl(m):
            s = xml_unescape(m.group(0)) if xml else m.group(0)
            return self.lookup[norm(s)]
        return rx.sub(repl, text)

    def search(self, text, xml=False):
        rx = self._rx[xml]
        return rx.search(text) if rx else None

    def finditer(self, text, xml=False):
        rx = self._rx[xml]
        return rx.finditer(text) if rx else iter(())


# ---------- 復元 ----------

class Restorer:
    def __init__(self, mapping):
        self.by_ph = mapping.by_placeholder()

    def restore_text(self, text, xml=False):
        """(復元した文字列, 戻らなかったプレースホルダーの一覧)。"""
        bad = []

        def repl(m):
            ph = m.group(0)
            e = self.by_ph.get(ph)
            if e is None:
                bad.append(ph)
                return ph
            return xml_escape(e["canonical"]) if xml else e["canonical"]
        out = PH_RE.sub(repl, text)
        for m in BROKEN_PH_RE.finditer(out):
            bad.append("壊れたプレースホルダー（⟦ か ⟧ が残っている）: …" + out[max(0, m.start() - 8):m.end() + 8].replace("\n", " ") + "…")
            break
        return out, bad


# ---------- 文字コード ----------

def decode_text(data):
    """(文字列, 文字コード名)。utf-8（BOM つきも）→ cp932 の順。"""
    for enc in ("utf-8-sig", "cp932"):
        try:
            s = data.decode(enc)
            if enc == "utf-8-sig" and data.startswith(b"\xef\xbb\xbf"):
                return s, "utf-8-sig"
            return s, "utf-8" if enc == "utf-8-sig" else enc
        except UnicodeDecodeError:
            continue
    raise MaskError("文字コードを判定できない（utf-8 と cp932 以外）")


def encode_text(text, prefer):
    """prefer の文字コードで書く。書けなければ utf-8-sig に落とす。(bytes, 使った文字コード)。"""
    if prefer == "cp932":
        try:
            return text.encode("cp932"), "cp932"
        except UnicodeEncodeError:
            return text.encode("utf-8-sig"), "utf-8-sig"
    if prefer == "utf-8":
        return text.encode("utf-8"), "utf-8"
    return text.encode("utf-8-sig"), "utf-8-sig"


# ---------- xlsx の読み取り（列の洗い出し、シート名・定義名） ----------

def _col_letters(ref):
    return re.match(r"[A-Z]+", ref).group(0)


def _t_text(el):
    """si / is の文字列（ふりがな rPh は除く）。"""
    parts = []
    for ch in el:
        tag = ch.tag.split("}")[-1]
        if tag == "t":
            parts.append(ch.text or "")
        elif tag == "r":
            for t in ch:
                if t.tag.split("}")[-1] == "t":
                    parts.append(t.text or "")
    return "".join(parts)


def xlsx_info(data):
    """{'sheets': [(名前, part)], 'names': [定義名], 'shared': [文字列], 'grid': {シート名: {行: {列: (種類, 値)}}}}"""
    z = zipfile.ZipFile(io.BytesIO(data))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels.findall("pr:Relationship", NS)}
    sheets = []
    for s in wb.findall("m:sheets/m:sheet", NS):
        t = targets.get(s.get("{%s}id" % NS["r"]), "")
        part = t.lstrip("/") if t.startswith("/") else "xl/" + t
        sheets.append((s.get("name"), part))
    names = [d.get("name") for d in wb.findall("m:definedNames/m:definedName", NS)
             if d.get("name") and not d.get("name").startswith("_xlnm.")]
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
        shared = [_t_text(si) for si in ss.findall("m:si", NS)]
    grid = {}
    for name, part in sheets:
        if part not in z.namelist():
            continue
        root = ET.fromstring(z.read(part))
        rows = {}
        for row in root.findall("m:sheetData/m:row", NS):
            rn = int(row.get("r") or 0)
            for c in row.findall("m:c", NS):
                ref, ty = c.get("r"), c.get("t")
                col = _col_letters(ref)
                if ty == "s":
                    v = c.find("m:v", NS)
                    val = ("s", shared[int(v.text)]) if v is not None and v.text is not None else None
                elif ty == "inlineStr":
                    i = c.find("m:is", NS)
                    val = ("s", _t_text(i)) if i is not None else None
                else:
                    v = c.find("m:v", NS)
                    val = ("n", v.text) if v is not None and v.text is not None else None
                if val is not None:
                    rows.setdefault(rn, {})[col] = val
        grid[name] = rows
    return {"sheets": sheets, "names": names, "shared": shared, "grid": grid}


def column_values_xlsx(info, sheet, column, warns):
    rows = info["grid"].get(sheet)
    if rows is None:
        return []
    header = rows.get(1, {})
    cols = [c for c, (_t, v) in header.items() if v == column]
    if not cols:
        return []
    col = cols[0]
    vals = []
    for rn in sorted(rows):
        if rn == 1 or col not in rows[rn]:
            continue
        ty, v = rows[rn][col]
        if ty == "s":
            vals.append(v)
        else:
            warns.append(f"{sheet}!{column}（{col}{rn}）: 数値のセルはマスクできない")
    return vals


def column_values_csv(text, column):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or column not in rows[0]:
        return []
    i = rows[0].index(column)
    return [r[i] for r in rows[1:] if len(r) > i and r[i]]


# ---------- 表の組み立て（設定 → mapping） ----------

def build_mapping(config, mapping, raw_files, warns):
    """設定の語と、列の値と、語を含むシート名・定義名を mapping に足す。"""
    for kind, group in config.terms.items():
        for key, variants in group.items():
            mapping.ensure(kind, key, variants)
    table = Table(mapping)
    for rel, data in raw_files.items():
        ext = Path(rel).suffix.lower()
        for colspec, kind in config.columns.items():
            sheet, col = colspec.split("!", 1)
            vals = []
            if ext == ".csv" and Path(rel).stem == sheet:
                vals = column_values_csv(decode_text(data)[0], col)
            elif ext == ".xlsx":
                vals = column_values_xlsx(xlsx_info(data), sheet, col, warns)
            for v in dict.fromkeys(v for v in vals if v):
                if len(v) < MIN_LEN:
                    warns.append(f"{colspec}: {v!r} は{MIN_LEN}文字未満なのでマスクしない")
                    continue
                if table.search(v) and table.lookup.get(norm(v)):
                    continue
                mapping.ensure(kind, v, [v])
                table = Table(mapping)
        if ext == ".xlsx":
            info = xlsx_info(data)
            for nm in [n for n, _p in info["sheets"]]:
                if table.search(nm):
                    mapping.ensure("SHEET", nm, [nm])
            for nm in info["names"]:
                if table.search(nm):
                    mapping.ensure("NAME", nm, [nm])
            table = Table(mapping)
    return Table(mapping)


# ---------- xlsx のマスク ----------

_CONTAINERS = (("si", "t"), ("is", "t"), ("text", "t"), ("a:p", "a:t"), ("w:p", "w:t"))
_PRINTER_REL = re.compile(r'<Relationship\b[^>]*Target="[^"]*printerSettings[^"]*"[^>]*/>')
_PRINTER_ID = re.compile(r'<Relationship\b[^>]*\bId="([^"]+)"[^>]*Target="[^"]*printerSettings')
_PRINTER_ID2 = re.compile(r'<Relationship\b[^>]*Target="[^"]*printerSettings[^"]*"[^>]*\bId="([^"]+)"')
_BLANK = (("dc:creator", ""), ("cp:lastModifiedBy", ""), ("Company", ""), ("Manager", ""))


def _is_text_part(name):
    return name.lower().endswith(XML_EXT)


def _decode_part(raw):
    for enc in ("utf-8-sig", "utf-16"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return None, None


def _runs(inner, tname):
    inner = re.sub(r"<rPh\b.*?</rPh>", "", inner, flags=re.S)
    return re.findall(rf"<{tname}(?:\s[^>]*)?>(.*?)</{tname}>", inner, flags=re.S)


def merge_runs(text, table, stats):
    """語が複数の run（書式の違いで分かれた文字列）にまたがるとき、その文字列を1つの run にまとめて置換する。"""
    for cont, tname in _CONTAINERS[:3]:  # si / is / text（書き換えるのはここだけ。他は点検で止める）
        pat = re.compile(rf"<{cont}>(.*?)</{cont}>", re.S)

        def fix(m):
            ts = _runs(m.group(1), tname)
            if len(ts) < 2:
                return m.group(0)
            pieces = [xml_unescape(t) for t in ts]
            plain = "".join(pieces)
            bounds, pos = [], 0
            for p in pieces:
                bounds.append((pos, pos + len(p)))
                pos += len(p)
            spanning = any(not any(a <= mm.start() and mm.end() <= b for a, b in bounds)
                           for mm in table.finditer(plain))
            if not spanning:
                return m.group(0)
            stats["merged"] = stats.get("merged", 0) + 1
            return f'<{cont}><{tname} xml:space="preserve">{xml_escape(table.mask_text(plain))}</{tname}></{cont}>'
        text = pat.sub(fix, text)
    return text


def spanning_hits(text, table):
    """各コンテナの文字を連結して、語が残っていないか調べる（run をまたぐ語を見つける）。"""
    hits = []
    for cont, tname in _CONTAINERS:
        for m in re.finditer(rf"<{cont}\b[^>]*>(.*?)</{cont}>", text, flags=re.S):
            plain = "".join(xml_unescape(t) for t in _runs(m.group(1), tname))
            mm = table.search(plain)
            if mm:
                hits.append(mm.group(0))
    return hits


def mask_xlsx(data, table, stats):
    zin = zipfile.ZipFile(io.BytesIO(data))
    names = zin.namelist()
    printer_parts = {n for n in names if re.match(r"xl/printerSettings/.*\.bin$", n, re.I)}
    parts = {n: zin.read(n) for n in names if n not in printer_parts}
    # プリンタ設定: 関係と r:id を外す
    removed_ids = {}
    for n in list(parts):
        if n.endswith(".rels"):
            text, enc = _decode_part(parts[n])
            if text is None:
                continue
            ids = set(_PRINTER_ID.findall(text)) | set(_PRINTER_ID2.findall(text))
            if ids:
                text = _PRINTER_REL.sub("", text)
                parts[n] = text.encode("utf-8")
                removed_ids[n] = ids
    for rels, ids in removed_ids.items():
        part = re.sub(r"_rels/([^/]+)\.rels$", r"\1", rels)
        if part in parts:
            text, _e = _decode_part(parts[part])
            if text is not None:
                for i in ids:
                    text = re.sub(rf'\s+r:id="{re.escape(i)}"', "", text)
                parts[part] = text.encode("utf-8")
    ct = parts.get("[Content_Types].xml")
    if ct is not None and printer_parts:
        text, _e = _decode_part(ct)
        text = re.sub(r'<Override\b[^>]*PartName="[^"]*printerSettings[^"]*"[^>]*/>', "", text)
        parts["[Content_Types].xml"] = text.encode("utf-8")
    stats["removed_parts"] = sorted(printer_parts)
    # 本文: run をまたぐ語 → 通常の置換 → プロパティを空に
    for n in list(parts):
        if not _is_text_part(n):
            continue
        text, enc = _decode_part(parts[n])
        if text is None:
            stats.setdefault("undecodable", []).append(n)
            continue
        text = merge_runs(text, table, stats)
        text = table.mask_text(text, xml=True)
        if n in ("docProps/core.xml", "docProps/app.xml"):
            for tag, val in _BLANK:
                text = re.sub(rf"(<{tag}\b[^>]*>).*?(</{tag}>)", rf"\1{val}\2", text, flags=re.S)
        parts[n] = text.encode("utf-8")
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            if n in printer_parts:
                continue
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, parts[n])
    return out.getvalue()


def verify_xlsx(data, table):
    """マスク後の xlsx に、対応表の語が残っていないか（全 part と、run を連結した文字列）。"""
    res = []
    z = zipfile.ZipFile(io.BytesIO(data))
    for n in z.namelist():
        if not _is_text_part(n):
            continue
        text, _e = _decode_part(z.read(n))
        if text is None:
            res.append(f"{n}: 文字コードを判定できず検査できない")
            continue
        m = table.search(text, xml=True)
        if m:
            res.append(f"{n}: {xml_unescape(m.group(0))}")
        for h in spanning_hits(text, table):
            res.append(f"{n}: {h}（run をまたぐ）")
    return res


def uninspectable_parts(data):
    """語を検査できない part（画像、埋め込みなど）。"""
    z = zipfile.ZipFile(io.BytesIO(data))
    return [n for n in z.namelist() if not _is_text_part(n) and not n.endswith("/")]


def restore_xlsx(data, restorer):
    zin = zipfile.ZipFile(io.BytesIO(data))
    names = zin.namelist()
    bad = []
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            raw = zin.read(n)
            if _is_text_part(n):
                text, _e = _decode_part(raw)
                if text is not None:
                    text, b = restorer.restore_text(text, xml=True)
                    bad.extend(f"{n}: {x}" for x in b)
                    raw = text.encode("utf-8")
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, raw)
    return out.getvalue(), bad


# ---------- 候補（対応表に無い固有名詞の手がかり） ----------

_HINTS = (
    ("法人格", re.compile(r"[^\s,、。]{0,12}(?:株式会社|有限会社|合同会社|\(株\)|（株）|㈱|㈲)[^\s,、。]{0,12}")),
    ("敬称", re.compile(r"[^\s,、。]{1,12}(?:様|御中|殿)")),
    ("メール", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("電話", re.compile(r"(?<![\d-])0\d{1,4}-\d{1,4}-\d{3,4}(?![\d-])")),
    ("URL・ドメイン", re.compile(r"https?://[^\s\"'<>]+|\b[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?:co\.jp|or\.jp|com|net|org|jp)\b")),
    ("郵便番号", re.compile(r"〒?\d{3}-\d{4}")),
)


def candidate_hints(label, text, limit=5):
    out = []
    for name, rx in _HINTS:
        seen = []
        for m in rx.finditer(text):
            s = m.group(0).strip()
            if s and s not in seen:
                seen.append(s)
        for s in seen[:limit]:
            out.append(f"{label}: [{name}] {s}")
    return out


def xlsx_texts(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    texts = []
    for n in z.namelist():
        if n == "xl/sharedStrings.xml" or n == "xl/workbook.xml" or re.match(r"xl/(comments|drawings/)", n):
            t, _e = _decode_part(z.read(n))
            if t:
                texts.append(xml_unescape(re.sub(r"<[^>]+>", " ", t)))
    return "\n".join(texts)


# ---------- ディレクトリ単位 ----------

def list_files(base):
    base = Path(base)
    if not base.exists():
        return {}
    return {f.relative_to(base).as_posix(): f.read_bytes()
            for f in sorted(base.rglob("*")) if f.is_file() and f.name != ".gitkeep" and not f.name.startswith("~$")}


def mask_files(raw_files, config, mapping, only=None):
    """raw_files: {相対パス: bytes}。only: マスクして返す相対パスの集合（None なら全部）。

    返り値: dict(outputs={相対パス: bytes}, hints=[...], warnings=[...], stats=...)。
    未対応の形式、語の残り、があれば MaskError（何も返さない。mapping も保存しない）。
    """
    warns, hints, outs, stats = [], [], {}, {}
    unsupported = [r for r in raw_files if Path(r).suffix.lower() not in (".csv", ".xlsx")]
    if unsupported:
        raise MaskError("マスクできない形式が原本にある（csv と xlsx だけ）:\n  " + "\n  ".join(sorted(unsupported)))
    table = build_mapping(config, mapping, raw_files, warns)
    residual = []
    for rel, data in raw_files.items():
        if only is not None and rel not in only:
            continue
        ext = Path(rel).suffix.lower()
        if ext == ".csv":
            text, _enc = decode_text(data)
            masked = table.mask_text(text)
            if table.search(masked):
                residual.append(f"{rel}: {table.search(masked).group(0)}")
            hints.extend(candidate_hints(rel, masked))
            outs[rel] = masked.encode("utf-8-sig")
        else:
            st = {}
            out = mask_xlsx(data, table, st)
            stats[rel] = st
            residual.extend(f"{rel}: {r}" for r in verify_xlsx(out, table))
            unins = uninspectable_parts(out)
            if unins:
                warns.append(f"{rel}: 語を検査できない part がある（画像・埋め込みなど。中身を確認する）: " + ", ".join(unins))
            if st.get("merged"):
                warns.append(f"{rel}: 語が複数の書式（run）にまたがる文字列 {st['merged']} 件を、1つの書式にまとめた")
            if st.get("removed_parts"):
                warns.append(f"{rel}: プリンタ設定を削除した: " + ", ".join(st["removed_parts"]))
            hints.extend(candidate_hints(rel, xlsx_texts(out)))
            outs[rel] = out
    if residual:
        raise MaskError("マスク後に、対応表の語が残っている（引き渡しを止める）:\n  " + "\n  ".join(residual))
    return {"outputs": outs, "hints": hints, "warnings": warns, "stats": stats}


RESTORE_SKIP = ("close.md",)
RESTORE_SKIP_DIRS = ("stock/",)
RESTORE_TEXT = TEXT_EXT


def restore_files(out_files, mapping):
    """out_files: {相対パス: bytes}（ai/out の中身）。(復元後 {相対パス: bytes}, 問題の一覧) を返す。問題があっても復元は試す。"""
    rs = Restorer(mapping)
    res, problems = {}, []
    for rel, data in out_files.items():
        if rel in RESTORE_SKIP or rel.startswith(RESTORE_SKIP_DIRS):
            continue
        ext = Path(rel).suffix.lower()
        if ext == ".xlsx":
            out, bad = restore_xlsx(data, rs)
            res[rel] = out
            problems.extend(f"{rel}: {b}" for b in bad)
        elif ext in RESTORE_TEXT:
            text, enc = decode_text(data)
            text, bad = rs.restore_text(text)
            problems.extend(f"{rel}: {b}" for b in bad)
            prefer = "utf-8-sig" if ext == ".csv" else ("cp932" if ext == ".bas" else "utf-8")
            res[rel], _used = encode_text(text, prefer)
        else:
            problems.append(f"{rel}: 復元できない形式（既知の形式: xlsx と " + " ".join(RESTORE_TEXT) + "）")
    return res, problems
