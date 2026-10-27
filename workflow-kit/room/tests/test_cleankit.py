"""cleankit のテスト。標準ライブラリで組んだダミーの xlsx・pptx（実在の名前は使わない）で、点検で見つかること、掃除で消えること、出力の整合を確かめる。"""
import io
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cleankit as ck  # noqa: E402

HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
M = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
PR = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
CT_NS = 'xmlns="http://schemas.openxmlformats.org/package/2006/content-types"'


def rels(*items):
    body = "".join(f'<Relationship Id="{i}" Type="{t if "://" in t else RT + t}" Target="{g}"{m}/>'
                   for i, t, g, *rest in items for m in [f' TargetMode="{rest[0]}"' if rest else ""])
    return HDR + f"<Relationships {PR}>{body}</Relationships>"


def ct(defaults, overrides):
    d = "".join(f'<Default Extension="{e}" ContentType="{c}"/>' for e, c in defaults)
    o = "".join(f'<Override PartName="/{p}" ContentType="{c}"/>' for p, c in overrides)
    return HDR + f"<Types {CT_NS}>{d}{o}</Types>"


def zipit(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, s in parts.items():
            z.writestr(n, s.encode("utf-8") if isinstance(s, str) else s)
    return buf.getvalue()


CORE = (HDR + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>ダミー作成者</dc:creator>'
        '<cp:lastModifiedBy>ダミー更新者</cp:lastModifiedBy><dc:title>ダミー案件の資料</dc:title></cp:coreProperties>')
APP = (HDR + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
       'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Company>ダミー会社</Company>'
       '<TitlesOfParts><vt:vector size="3" baseType="lpstr"><vt:lpstr>公開</vt:lpstr><vt:lpstr>社外秘</vt:lpstr>'
       '<vt:lpstr>極秘</vt:lpstr></vt:vector></TitlesOfParts></Properties>')
CUSTOM = (HDR + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
          'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
          '<property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="MSIP_Label_dummy_Name">'
          '<vt:lpwstr>社外秘</vt:lpwstr></property></Properties>')


def build_xlsx():
    sst_items = ["見出し", "ダミー太郎", "使っていない旧担当", "ダミー極秘メモ", "公開の値"]
    sst = (HDR + f'<sst {M} count="5" uniqueCount="5">' + "".join(f"<si><t>{s}</t></si>" for s in sst_items) + "</sst>")
    wb = (HDR + f'<workbook {M} {R} xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
          'xmlns:x15ac="http://schemas.microsoft.com/office/spreadsheetml/2010/11/ac">'
          '<mc:AlternateContent><mc:Choice Requires="x15"><x15ac:absPath url="C:\\Users\\dummyuser\\Desktop\\"/>'
          '</mc:Choice></mc:AlternateContent>'
          '<bookViews><workbookView activeTab="0"/></bookViews><sheets>'
          '<sheet name="公開" sheetId="1" r:id="rId1"/>'
          '<sheet name="社外秘" sheetId="2" state="hidden" r:id="rId2"/>'
          '<sheet name="極秘" sheetId="3" state="veryHidden" r:id="rId3"/>'
          '</sheets><definedNames>'
          "<definedName name=\"担当一覧\">'社外秘'!$A$1:$A$2</definedName>"
          '<definedName name="_xlnm.Print_Area" localSheetId="2">極秘!$A$1</definedName>'
          "<definedName name=\"公開範囲\">'公開'!$A$1:$B$1</definedName>"
          '<definedName name="消えた範囲">#REF!$A$1</definedName>'
          '</definedNames></workbook>')
    s1 = (HDR + f'<worksheet {M} {R}><sheetData>'
          '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><f>SUM(\'社外秘\'!B1:B2)</f><v>300</v></c>'
          '<c r="C1"><f t="shared" ref="C1:D1" si="0">社外秘!B1</f><v>100</v></c><c r="D1"><f t="shared" si="0"/><v>200</v></c>'
          '<c r="E1"><f>B1*2</f><v>600</v></c></row>'
          '<row r="2" hidden="1"><c r="A2" t="s"><v>4</v></c></row>'
          '</sheetData><pageSetup r:id="rId9"/><legacyDrawing r:id="rId8"/></worksheet>')
    s2 = (HDR + f'<worksheet {M}><sheetData><row r="1"><c r="A1" t="s"><v>1</v></c><c r="B1"><v>100</v></c></row>'
          '</sheetData></worksheet>')
    s3 = (HDR + f'<worksheet {M}><sheetData><row r="1"><c r="A1" t="s"><v>3</v></c></row></sheetData></worksheet>')
    chart = (HDR + '<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:chart><c:plotArea>'
             '<c:barChart><c:ser><c:cat><c:strRef><c:f>社外秘!$A$1:$A$1</c:f><c:strCache><c:ptCount val="1"/>'
             '<c:pt idx="0"><c:v>ダミー太郎</c:v></c:pt></c:strCache></c:strRef></c:cat></c:ser></c:barChart>'
             '</c:plotArea></c:chart></c:chartSpace>')
    drawing = (HDR + '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"/>')
    comments = (HDR + f'<comments {M}><authors><author>ダミー作成者</author></authors><commentList>'
                '<comment ref="A1" authorId="0"><text><t>ダミーの確認メモ</t></text></comment></commentList></comments>')
    vml = '<xml xmlns:x="urn:schemas-microsoft-com:office:excel"><v:shape><x:ClientData ObjectType="Note"/></v:shape></xml>'
    S = "application/vnd.openxmlformats-officedocument.spreadsheetml."
    return zipit({
        "[Content_Types].xml": ct([("rels", "application/vnd.openxmlformats-package.relationships+xml"),
                                   ("xml", "application/xml"), ("vml", "application/vnd.openxmlformats-officedocument.vmlDrawing"),
                                   ("bin", "application/vnd.openxmlformats-officedocument.spreadsheetml.printerSettings")],
                                  [("xl/workbook.xml", S + "sheet.main+xml"), ("xl/worksheets/sheet1.xml", S + "worksheet+xml"),
                                   ("xl/worksheets/sheet2.xml", S + "worksheet+xml"), ("xl/worksheets/sheet3.xml", S + "worksheet+xml"),
                                   ("xl/sharedStrings.xml", S + "sharedStrings+xml"), ("xl/calcChain.xml", S + "calcChain+xml"),
                                   ("xl/comments1.xml", S + "comments+xml"), ("xl/charts/chart1.xml", "application/vnd.openxmlformats-officedocument.drawingml.chart+xml"),
                                   ("xl/drawings/drawing1.xml", "application/vnd.openxmlformats-officedocument.drawing+xml"),
                                   ("docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
                                   ("docProps/app.xml", "application/vnd.openxmlformats-officedocument.extended-properties+xml"),
                                   ("docProps/custom.xml", "application/vnd.openxmlformats-officedocument.custom-properties+xml"),
                                   ("xl/leftover.xml", "application/xml")]),
        "_rels/.rels": rels(("rId1", "officeDocument", "xl/workbook.xml"),
                            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                            ("rId3", "extended-properties", "docProps/app.xml"), ("rId4", "custom-properties", "docProps/custom.xml")),
        "xl/workbook.xml": wb,
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml"), ("rId2", "worksheet", "worksheets/sheet2.xml"),
                                           ("rId3", "worksheet", "worksheets/sheet3.xml"), ("rId4", "sharedStrings", "sharedStrings.xml"),
                                           ("rId5", "calcChain", "calcChain.xml")),
        "xl/worksheets/sheet1.xml": s1, "xl/worksheets/sheet2.xml": s2, "xl/worksheets/sheet3.xml": s3,
        "xl/worksheets/_rels/sheet1.xml.rels": rels(("rId7", "drawing", "../drawings/drawing1.xml"), ("rId6", "comments", "../comments1.xml"),
                                                    ("rId8", "vmlDrawing", "../drawings/vmlDrawing1.vml"),
                                                    ("rId9", "printerSettings", "../printerSettings/printerSettings1.bin"),
                                                    ("rId10", "hyperlink", "file:///C:/Users/dummyuser/secret.xlsx", "External")),
        "xl/drawings/drawing1.xml": drawing,
        "xl/drawings/_rels/drawing1.xml.rels": rels(("rId1", "chart", "../charts/chart1.xml")),
        "xl/charts/chart1.xml": chart,
        "xl/comments1.xml": comments, "xl/drawings/vmlDrawing1.vml": vml,
        "xl/printerSettings/printerSettings1.bin": b"\x00dummy-printer\x00",
        "xl/sharedStrings.xml": sst,
        "xl/calcChain.xml": HDR + f'<calcChain {M}><c r="B1" i="1"/></calcChain>',
        "xl/leftover.xml": HDR + "<old>ダミーの古い部品</old>",
        "docProps/core.xml": CORE, "docProps/app.xml": APP, "docProps/custom.xml": CUSTOM,
    })


def build_pptx():
    P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'

    def slide(text, hidden=False):
        return (HDR + f'<p:sld {P} {A} {R}' + (' show="0"' if hidden else "") + '><p:cSld><p:spTree>'
                f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="t" descr="ダミーの代替テキスト"/></p:nvSpPr><p:spPr><a:xfrm>'
                '<a:off x="20000000" y="0"/><a:ext cx="100" cy="100"/></a:xfrm></p:spPr>'
                f'<p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
    pres = (HDR + f'<p:presentation {P} {R}><p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId3"/>'
            '</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/></p:presentation>')
    notes = HDR + f'<p:notes {P} {A}><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>ダミーの話す内容</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>'
    authors = HDR + f'<p:cmAuthorLst {P}><p:cmAuthor id="0" name="ダミー作成者" initials="D"/></p:cmAuthorLst>'
    cm = HDR + f'<p:cmLst {P}><p:cm authorId="0"><p:text>ダミーのコメント</p:text></p:cm></p:cmLst>'
    PP = "application/vnd.openxmlformats-officedocument.presentationml."
    return zipit({
        "[Content_Types].xml": ct([("rels", "application/vnd.openxmlformats-package.relationships+xml"), ("xml", "application/xml"),
                                   ("jpeg", "image/jpeg")],
                                  [("ppt/presentation.xml", PP + "presentation.main+xml"), ("ppt/slides/slide1.xml", PP + "slide+xml"),
                                   ("ppt/slides/slide2.xml", PP + "slide+xml"), ("ppt/notesSlides/notesSlide1.xml", PP + "notesSlide+xml"),
                                   ("ppt/commentAuthors.xml", PP + "commentAuthors+xml"), ("ppt/comments/comment1.xml", PP + "comments+xml"),
                                   ("docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml")]),
        "_rels/.rels": rels(("rId1", "officeDocument", "ppt/presentation.xml"),
                            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                            ("rId3", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail", "docProps/thumbnail.jpeg")),
        "ppt/presentation.xml": pres,
        "ppt/_rels/presentation.xml.rels": rels(("rId2", "slide", "slides/slide1.xml"), ("rId3", "slide", "slides/slide2.xml"),
                                                ("rId4", "commentAuthors", "commentAuthors.xml")),
        "ppt/slides/slide1.xml": slide("公開のスライド"), "ppt/slides/slide2.xml": slide("ダミーの非表示メモ", hidden=True),
        "ppt/slides/_rels/slide1.xml.rels": rels(("rId1", "notesSlide", "../notesSlides/notesSlide1.xml"),
                                                 ("rId2", "comments", "../comments/comment1.xml")),
        "ppt/notesSlides/notesSlide1.xml": notes,
        "ppt/notesSlides/_rels/notesSlide1.xml.rels": rels(("rId1", "slide", "../slides/slide1.xml")),
        "ppt/commentAuthors.xml": authors, "ppt/comments/comment1.xml": cm,
        "docProps/core.xml": CORE, "docProps/thumbnail.jpeg": b"\xff\xd8dummy",
    })


def texts(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    return {n: z.read(n).decode("utf-8", "replace") for n in z.namelist()}


def codes(fs):
    return {f.code for f in fs}


class XlsxTest(unittest.TestCase):
    def setUp(self):
        self.data = build_xlsx()

    def test_check_finds_residue(self):
        fs = ck.check(ck.Pkg(self.data), ".xlsx")
        want = {"hidden-sheet", "defined-name", "abspath", "unused-shared-string", "hidden-sheet-string", "chart-cache",
                "comment", "props-core", "props-app", "props-custom", "calcchain", "printer", "orphan-part",
                "hidden-rowcol", "external-target"}
        self.assertLessEqual(want, codes(fs))
        chart = next(f for f in fs if f.code == "chart-cache")
        self.assertIn("社外秘", chart.detail)
        names = next(f for f in fs if f.code == "defined-name")
        self.assertEqual(len(names.samples), 3)  # 社外秘を参照、極秘の印刷範囲、#REF!。公開範囲は出さない

    def test_clean_removes(self):
        out, log = ck.clean(self.data, ".xlsx", list(ck.CLEAN_ACTIONS))
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        allt = "\n".join(t.values())
        for word in ("ダミー極秘メモ", "使っていない旧担当", "ダミー作成者", "ダミー更新者", "ダミー会社", "dummyuser\\Desktop",
                     "ダミーの確認メモ", "ダミーの古い部品", "MSIP_Label"):
            self.assertNotIn(word, allt, word)
        for gone in ("xl/worksheets/sheet2.xml", "xl/worksheets/sheet3.xml", "xl/calcChain.xml", "xl/comments1.xml",
                     "xl/printerSettings/printerSettings1.bin", "xl/leftover.xml", "docProps/custom.xml"):
            self.assertNotIn(gone, t, gone)
        wb = t["xl/workbook.xml"]
        self.assertEqual(re.findall(r'<sheet name="([^"]+)"', wb), ["公開"])
        self.assertIn("公開範囲", wb)
        self.assertNotIn("担当一覧", wb)
        self.assertNotIn("_xlnm.Print_Area", wb)
        self.assertNotIn("消えた範囲", wb)
        s1 = t["xl/worksheets/sheet1.xml"]
        self.assertNotIn("社外秘", s1)
        self.assertIn("<c r=\"B1\"><v>300</v></c>", s1)  # 数式は外し、値は残す
        self.assertIn("<c r=\"D1\"><v>200</v></c>", s1)  # 共有の数式の子も外す
        self.assertIn("<f>B1*2</f>", s1)  # 関係ない数式は残す
        self.assertNotIn("legacyDrawing", s1)
        self.assertNotIn('r:id="rId9"', s1)
        # 共有文字列を詰めても、セルが指す文字は変わらない
        items = re.findall(r"<t>(.*?)</t>", t["xl/sharedStrings.xml"])
        idx = [int(x) for x in re.findall(r'<c r="A\d" t="s"><v>(\d+)</v>', s1)]
        self.assertEqual([items[i] for i in idx], ["見出し", "公開の値"])
        self.assertIn('uniqueCount="2"', t["xl/sharedStrings.xml"])
        after = ck.check(ck.Pkg(out), ".xlsx")
        self.assertIn("chart-cache", codes(after))  # グラフの写しは消さない（報告に残る）
        self.assertNotIn("hidden-sheet", codes(after))

    def test_keep(self):
        out, _log = ck.clean(self.data, ".xlsx", [a for a in ck.CLEAN_ACTIONS if a not in ("hidden-sheets", "props")])
        t = texts(out)
        self.assertIn("xl/worksheets/sheet2.xml", t)
        self.assertIn("ダミー作成者", t["docProps/core.xml"])
        self.assertEqual(ck.integrity(out), [])

    def test_cli_leaves_original(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "dummy.xlsx"
            src.write_bytes(self.data)
            rc = ck.main(["clean", str(src), str(Path(d) / "out")])
            self.assertEqual(rc, 1)  # グラフの写しと非表示の行が残る
            self.assertEqual(src.read_bytes(), self.data)
            self.assertTrue((Path(d) / "out" / "dummy.xlsx").exists())
            self.assertTrue((Path(d) / "out" / "dummy.xlsx.clean-report.md").exists())
            self.assertEqual(ck.main(["clean", str(src), str(src)]), 2)
            self.assertEqual(ck.main(["clean", str(src), str(Path(d) / "out")]), 2)  # 上書きしない
            (Path(d) / "a.docx").write_bytes(b"x")
            self.assertEqual(ck.main(["check", str(Path(d) / "a.docx")]), 2)


class GuardTest(unittest.TestCase):
    def test_refuses_inside_own_repo(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "dummy.xlsx"
            src.write_bytes(build_xlsx())
            here = Path(ck.__file__).resolve().parent
            self.assertEqual(ck.main(["clean", str(src), str(here / "tmp_out")]), 2)
            self.assertEqual(ck.main(["check", str(src), "--report", str(here / "tmp.md")]), 2)
            self.assertFalse((here / "tmp_out").exists() or (here / "tmp.md").exists())


class PptxTest(unittest.TestCase):
    def setUp(self):
        self.data = build_pptx()

    def test_check_finds_residue(self):
        fs = ck.check(ck.Pkg(self.data), ".pptx")
        self.assertLessEqual({"hidden-slide", "notes", "comment", "comment-author", "thumbnail", "props-core",
                              "alt-text", "off-slide"}, codes(fs))

    def test_clean_removes(self):
        out, _log = ck.clean(self.data, ".pptx", list(ck.CLEAN_ACTIONS))
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        allt = "\n".join(t.values())
        for word in ("ダミーの非表示メモ", "ダミーの話す内容", "ダミー作成者", "ダミーのコメント"):
            self.assertNotIn(word, allt, word)
        self.assertNotIn("docProps/thumbnail.jpeg", t)
        self.assertEqual(re.findall(r'<p:sldId id="(\d+)"', t["ppt/presentation.xml"]), ["256"])
        self.assertIn("公開のスライド", t["ppt/slides/slide1.xml"])
        after = codes(ck.check(ck.Pkg(out), ".pptx"))
        self.assertLessEqual({"alt-text", "off-slide"}, after)  # 報告だけのもの


if __name__ == "__main__":
    unittest.main()
