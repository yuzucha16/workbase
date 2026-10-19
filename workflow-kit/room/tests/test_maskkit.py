"""maskkit のテスト。合成データ（csv と、標準ライブラリで組んだ xlsx）で、往復の一致と語の残りが無いことを確かめる。"""
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import maskkit as mk  # noqa: E402

TOML = """
[terms.CUST]
acme = ["アクメ商事株式会社", "アクメ商事", "ACME Trading"]
beta = ["ベータ工業", "ﾍﾞｰﾀ工業"]

[terms.PERSON]
tanaka = ["田中太郎", "田中"]

[columns]
"売上!顧客名" = "CUST"
"""


def cfg(tmp):
    p = Path(tmp) / "mask.toml"
    p.write_text(TOML, encoding="utf-8")
    return mk.load_config(p)


def build_xlsx(split_runs=False):
    """アクメ商事を含むシート名・定義名・コメント・プロパティ・プリンタ設定つきの最小 xlsx。"""
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Override PartName="/xl/workbook.xml" ContentType="x"/>'
          '<Override PartName="/xl/printerSettings/printerSettings1.bin" ContentType="y"/></Types>')
    wb = ('<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<sheets><sheet name="アクメ商事" sheetId="1" r:id="rId1"/><sheet name="売上" sheetId="2" r:id="rId2"/></sheets>'
          '<definedNames><definedName name="アクメ商事_範囲">売上!$A$1</definedName></definedNames></workbook>')
    wbrels = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
              '<Relationship Id="rId1" Type="t" Target="worksheets/sheet1.xml"/>'
              '<Relationship Id="rId2" Type="t" Target="worksheets/sheet2.xml"/></Relationships>')
    if split_runs:
        si1 = '<si><r><t>アクメ</t></r><r><rPr><b/></rPr><t>商事への請求</t></r></si>'
    else:
        si1 = '<si><t>アクメ商事への請求</t></si>'
    ss = ('<?xml version="1.0"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
          + si1 + '<si><t>顧客名</t></si><si><t>ベータ工業</t></si><si><t>連絡先 info@acme.co.jp</t></si></sst>')
    sheet1 = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
              'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
              '<sheetData><row r="1"><c r="A1" t="s"><v>0</v></c></row></sheetData>'
              '<pageSetup r:id="rId1"/></worksheet>')
    sheet1rels = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="t" Target="../printerSettings/printerSettings1.bin"/></Relationships>')
    sheet2 = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
              '<row r="1"><c r="A1" t="s"><v>1</v></c><c r="B1" t="n"><v>1</v></c></row>'
              '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2" t="n"><v>100</v></c></row>'
              '<row r="3"><c r="A3" t="inlineStr"><is><t>新規顧客ガンマ社</t></is></c><c r="B3"><v>50</v></c></row>'
              '</sheetData></worksheet>')
    comments = ('<?xml version="1.0"?><comments xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><commentList>'
                '<comment ref="A1"><text><r><t>田中太郎さんに確認</t></r></text></comment></commentList></comments>')
    core = ('<?xml version="1.0"?><cp:coreProperties xmlns:cp="c" xmlns:dc="d"><dc:creator>田中太郎</dc:creator>'
            '<cp:lastModifiedBy>田中</cp:lastModifiedBy></cp:coreProperties>')
    app = '<?xml version="1.0"?><Properties><Company>アクメ商事株式会社</Company></Properties>'
    pivot = ('<?xml version="1.0"?><pivotCacheDefinition><cacheSource><worksheetSource ref="A1:B3" sheet="売上"/></cacheSource>'
             '<cacheField name="顧客名"/><sharedItems><s v="ベータ工業"/></sharedItems></pivotCacheDefinition>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wbrels)
        z.writestr("xl/sharedStrings.xml", ss)
        z.writestr("xl/worksheets/sheet1.xml", sheet1)
        z.writestr("xl/worksheets/_rels/sheet1.xml.rels", sheet1rels)
        z.writestr("xl/worksheets/sheet2.xml", sheet2)
        z.writestr("xl/comments1.xml", comments)
        z.writestr("xl/pivotCache/pivotCacheDefinition1.xml", pivot)
        z.writestr("xl/printerSettings/printerSettings1.bin", b"\x00PRINTER\x00" + "アクメ商事".encode("cp932"))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
    return buf.getvalue()


def all_text(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    return "\n".join(z.read(n).decode("utf-8", "replace") for n in z.namelist())


class CsvTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = cfg(self.tmp.name)

    def test_roundtrip_cp932_and_variants(self):
        raw = "顧客名,担当,備考\nアクメ商事株式会社,田中太郎,ACME TRADING と取引\nＡＣＭＥ　Ｔrading,田中,ﾍﾞｰﾀ工業の紹介\n新規ガンマ社,山田,\n".encode("cp932")
        m = mk.Mapping()
        res = mk.mask_files({"売上.csv": raw}, self.cfg, m)
        out = res["outputs"]["売上.csv"].decode("utf-8-sig")
        for w in ("アクメ", "田中", "ACME", "ベータ", "ﾍﾞｰﾀ"):
            self.assertNotIn(w, out)
        self.assertIn("⟦CUST_001⟧", out)
        # 長い語が優先される（アクメ商事株式会社 が アクメ商事 + 株式会社 にならない）
        self.assertNotIn("株式会社", out)
        # 列で拾った値は新しい番号になる
        self.assertIn("⟦CUST_003⟧", out)
        # 復元
        back, problems = mk.restore_files({"売上.csv": res["outputs"]["売上.csv"]}, m)
        self.assertEqual(problems, [])
        text = back["売上.csv"].decode("utf-8-sig")
        self.assertIn("アクメ商事株式会社", text)  # 正式名に戻る
        self.assertIn("新規ガンマ社", text)
        self.assertIn("田中太郎", text)

    def test_stable_numbers_append_only(self):
        m = mk.Mapping()
        mk.mask_files({"a.csv": "アクメ商事\n".encode("utf-8")}, self.cfg, m)
        before = json.dumps(m.data, sort_keys=True)
        mk.mask_files({"a.csv": "アクメ商事\nベータ工業\n".encode("utf-8")}, self.cfg, m)
        self.assertEqual(m.data["entries"]["CUST"]["acme"]["id"], 1)
        self.assertEqual(m.data["entries"]["CUST"]["beta"]["id"], 2)
        self.assertEqual(before, json.dumps(m.data, sort_keys=True))

    def test_unresolved_placeholder_reported(self):
        m = mk.Mapping()
        mk.mask_files({"a.csv": "アクメ商事\n".encode("utf-8")}, self.cfg, m)
        _res, problems = mk.restore_files({"x.md": "⟦CUST_099⟧ と ⟦CUST_001".encode("utf-8")}, m)
        self.assertEqual(len(problems), 2)

    def test_unknown_format_in_out(self):
        _res, problems = mk.restore_files({"x.pdf": b"%PDF"}, mk.Mapping())
        self.assertTrue(any("復元できない形式" in p for p in problems))

    def test_unsupported_raw_stops(self):
        with self.assertRaises(mk.MaskError):
            mk.mask_files({"a.pdf": b"%PDF"}, self.cfg, mk.Mapping())

    def test_short_term_rejected(self):
        p = Path(self.tmp.name) / "bad.toml"
        p.write_text('[terms.CUST]\nx = ["A"]\n', encoding="utf-8")
        with self.assertRaises(mk.MaskError):
            mk.load_config(p)

    def test_hints(self):
        res = mk.mask_files({"a.csv": "連絡先,未知の会社株式会社,suzuki@example.com,03-1234-5678,〒100-0001\n".encode("utf-8")},
                            self.cfg, mk.Mapping())
        joined = "\n".join(res["hints"])
        for w in ("法人格", "メール", "電話", "郵便番号"):
            self.assertIn(w, joined)


class XlsxTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = cfg(self.tmp.name)

    def run_case(self, split):
        raw = build_xlsx(split_runs=split)
        m = mk.Mapping()
        res = mk.mask_files({"売上.xlsx": raw}, self.cfg, m)
        out = res["outputs"]["売上.xlsx"]
        text = all_text(out)
        for w in ("アクメ", "田中", "ベータ", "ガンマ", "ACME"):
            self.assertNotIn(w, text, w)
        z = zipfile.ZipFile(io.BytesIO(out))
        self.assertFalse([n for n in z.namelist() if "printerSettings" in n])
        self.assertNotIn("printerSettings", all_text(out))
        self.assertIn("SHEET_001", z.read("xl/workbook.xml").decode())
        self.assertIn("NAME_001", z.read("xl/workbook.xml").decode())
        self.assertTrue(any("メール" in h and "acme.co.jp" in h for h in res["hints"]))  # 語でない手がかりは候補に出る
        self.assertEqual(mk.verify_xlsx(out, mk.Table(m)), [])
        back, problems = mk.restore_files({"売上.xlsx": out}, m)
        self.assertEqual(problems, [])
        rt = all_text(back["売上.xlsx"])
        self.assertIn("アクメ商事への請求", rt)
        self.assertIn('name="アクメ商事"', rt)
        self.assertIn("田中太郎さんに確認", rt)
        self.assertIn("新規顧客ガンマ社", rt)
        # 復元後は構造が読める
        info = mk.xlsx_info(back["売上.xlsx"])
        self.assertEqual([n for n, _p in info["sheets"]], ["アクメ商事", "売上"])
        return res

    def test_plain(self):
        res = self.run_case(False)
        self.assertTrue(any("プリンタ設定" in w for w in res["warnings"]))

    def test_split_runs_are_merged(self):
        res = self.run_case(True)
        self.assertTrue(any("run" in w for w in res["warnings"]))

    def test_leak_detected_when_unmasked(self):
        """run をまたぐ語を、連結して検出できる（点検の単体）。"""
        m = mk.Mapping()
        mk.mask_files({"a.csv": "アクメ商事\n".encode("utf-8")}, self.cfg, m)
        t = mk.Table(m)
        xml = '<si><r><t>アクメ</t></r><r><t>商事</t></r></si>'
        self.assertTrue(mk.spanning_hits(xml, t))

    def test_properties_blank_even_without_terms(self):
        raw = build_xlsx()
        z = zipfile.ZipFile(io.BytesIO(raw))
        core = z.read("docProps/core.xml").decode()
        self.assertIn("田中太郎", core)
        m = mk.Mapping()
        cfg2 = mk.Config({}, {})
        res = mk.mask_files({"a.xlsx": raw}, cfg2, m)
        core2 = zipfile.ZipFile(io.BytesIO(res["outputs"]["a.xlsx"])).read("docProps/core.xml").decode()
        self.assertNotIn("田中太郎", core2)
        self.assertIn("<dc:creator></dc:creator>", core2)


def build_pptx(split_runs=False):
    """アクメ商事を含むスライド・ノート・プロパティ・縮小画像つきの最小 pptx（標準ライブラリで組む）。"""
    para1 = ('<a:r><a:rPr b="1"/><a:t>アクメ</a:t></a:r><a:r><a:t>商事</a:t></a:r><a:r><a:t>との合意</a:t></a:r>'
             if split_runs else '<a:r><a:t>アクメ商事との合意</a:t></a:r>')
    slide = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
             'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree>'
             f'<p:sp><p:txBody><a:p>{para1}</a:p><a:p><a:r><a:t>担当: 田中太郎 &amp; ベータ工業</a:t></a:r></a:p></p:txBody></p:sp>'
             '</p:spTree></p:cSld></p:sld>')
    notes = ('<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
             'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:sp><p:txBody>'
             '<a:p><a:r><a:t>メモ: アクメ商事の件</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>')
    core = ('<cp:coreProperties xmlns:cp="x" xmlns:dc="y"><dc:creator>田中太郎</dc:creator>'
            '<cp:lastModifiedBy>田中太郎</cp:lastModifiedBy></cp:coreProperties>')
    app = '<Properties><Company>アクメ商事</Company></Properties>'
    rels = ('<Relationships><Relationship Id="rId1" Type="t" Target="ppt/presentation.xml"/>'
            '<Relationship Id="rId2" Type="t" Target="docProps/thumbnail.jpeg"/></Relationships>')
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("_rels/.rels", rels)
        z.writestr("ppt/slides/slide1.xml", slide)
        z.writestr("ppt/notesSlides/notesSlide1.xml", notes)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("docProps/thumbnail.jpeg", b"\xff\xd8jpeg")
    return out.getvalue()


class PptxTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = cfg(self.tmp.name)

    def run_case(self, split):
        m = mk.Mapping()
        res = mk.mask_files({"会議.pptx": build_pptx(split)}, self.cfg, m)
        out = res["outputs"]["会議.pptx"]
        text = all_text(out)
        for w in ("アクメ", "田中", "ベータ"):
            self.assertNotIn(w, text, w)
        z = zipfile.ZipFile(io.BytesIO(out))
        self.assertNotIn("docProps/thumbnail.jpeg", z.namelist())
        self.assertNotIn("thumbnail", z.read("_rels/.rels").decode())
        self.assertEqual(mk.verify_xlsx(out, mk.Table(m)), [])
        back, problems = mk.restore_files({"会議.pptx": out}, m)
        self.assertEqual(problems, [])
        slide = zipfile.ZipFile(io.BytesIO(back["会議.pptx"])).read("ppt/slides/slide1.xml").decode()
        self.assertIn("アクメ商事", slide)
        self.assertIn("田中太郎 &amp; ベータ工業", slide)
        return res, out

    def test_plain(self):
        self.run_case(False)

    def test_split_runs_keep_formatting(self):
        res, out = self.run_case(True)
        self.assertTrue(any("段落" in w for w in res["warnings"]))
        slide = zipfile.ZipFile(io.BytesIO(out)).read("ppt/slides/slide1.xml").decode()
        self.assertIn('<a:rPr b="1"/><a:t>⟦CUST_001⟧</a:t>', slide)  # 先頭の run の書式に置く
        self.assertIn("<a:t>との合意</a:t>", slide)

    def test_properties_blank(self):
        res = mk.mask_files({"a.pptx": build_pptx()}, mk.Config({}, {}), mk.Mapping())
        z = zipfile.ZipFile(io.BytesIO(res["outputs"]["a.pptx"]))
        self.assertIn("<dc:creator></dc:creator>", z.read("docProps/core.xml").decode())
        self.assertIn("<Company></Company>", z.read("docProps/app.xml").decode())


class TextFilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = cfg(self.tmp.name)

    def test_md_txt_roundtrip(self):
        raw = {"議事録.md": "# アクメ商事 定例\n- 田中太郎: 見積を出す\n".encode("utf-8"),
               "メモ.txt": "ベータ工業との件\n".encode("cp932")}
        m = mk.Mapping()
        res = mk.mask_files(raw, self.cfg, m)
        for rel, data in res["outputs"].items():
            t = data.decode("utf-8")
            for w in ("アクメ", "田中", "ベータ"):
                self.assertNotIn(w, t)
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"))
        back, problems = mk.restore_files(res["outputs"], m)
        self.assertEqual(problems, [])
        self.assertIn("アクメ商事株式会社 定例", back["議事録.md"].decode("utf-8"))
        self.assertIn("ベータ工業との件", back["メモ.txt"].decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
