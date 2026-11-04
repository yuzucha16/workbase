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
          '</sheets><externalReferences><externalReference r:id="rId6"/></externalReferences><definedNames>'
          "<definedName name=\"担当一覧\">'社外秘'!$A$1:$A$2</definedName>"
          '<definedName name="_xlnm.Print_Area" localSheetId="2">極秘!$A$1</definedName>'
          "<definedName name=\"公開範囲\">'公開'!$A$1:$B$1</definedName>"
          '<definedName name="消えた範囲">#REF!$A$1</definedName>'
          '<definedName name="外部名">[1]Sheet1!$A$1</definedName>'
          '<definedName name="AccessDatabase" hidden="1">"C:\\Users\\dummyuser\\dummy.mdb"</definedName>'
          '<definedName name="_xlfn.DUMMY" hidden="1">#NAME?</definedName>'
          '</definedNames></workbook>')
    s1 = (HDR + f'<worksheet {M} {R}><cols><col min="7" max="7" width="9" hidden="1"/></cols><sheetData>'
          '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><f>SUM(\'社外秘\'!B1:B2)</f><v>300</v></c>'
          '<c r="C1"><f t="shared" ref="C1:D1" si="0">社外秘!B1</f><v>100</v></c><c r="D1"><f t="shared" si="0"/><v>200</v></c>'
          '<c r="E1"><f>B1*2</f><v>600</v></c><c r="F1"><f>[1]Sheet1!A1+1</f><v>77</v></c><c r="G1"><v>9999</v></c></row>'
          '<row r="2" hidden="1"><c r="A2" t="s"><v>4</v></c><c r="B2"><f>E1+1</f><v>601</v></c>'
          '<c r="C2"><f t="shared" ref="C2:D2" si="1">E1+2</f><v>602</v></c><c r="D2"><f t="shared" si="1"/><v>603</v></c></row>'
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
                                   ("xl/leftover.xml", "application/xml"),
                                   ("xl/externalLinks/externalLink1.xml", S + "externalLink+xml")]),
        "_rels/.rels": rels(("rId1", "officeDocument", "xl/workbook.xml"),
                            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                            ("rId3", "extended-properties", "docProps/app.xml"), ("rId4", "custom-properties", "docProps/custom.xml")),
        "xl/workbook.xml": wb,
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml"), ("rId2", "worksheet", "worksheets/sheet2.xml"),
                                           ("rId3", "worksheet", "worksheets/sheet3.xml"), ("rId4", "sharedStrings", "sharedStrings.xml"),
                                           ("rId5", "calcChain", "calcChain.xml"), ("rId6", "externalLink", "externalLinks/externalLink1.xml")),
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
        "xl/externalLinks/externalLink1.xml": HDR + f'<externalLink {M}><externalBook {R} r:id="rId1"><sheetNames><sheetName val="ダミー外部シート"/></sheetNames>'
                                                 '<sheetDataSet><sheetData sheetId="0"><row r="1"><cell r="A1"><v>12345</v></cell></row></sheetData></sheetDataSet></externalBook></externalLink>',
        "xl/externalLinks/_rels/externalLink1.xml.rels": rels(("rId1", "externalLinkPath", "file:///C:/Users/dummyuser/ext.xlsx", "External")),
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
        self.assertEqual(len(names.samples), 4)  # 社外秘を参照、極秘の印刷範囲、#REF!、非表示の AccessDatabase。公開範囲と _xl の内部名は出さない

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
        self.assertIn('<c r="F1"><v>77</v></c>', s1)  # 外部リンクの数式は値にする
        self.assertNotIn("externalLink", "".join(t))
        self.assertNotIn("外部名", wb)
        self.assertNotIn("AccessDatabase", wb)
        self.assertNotIn("dummy.mdb", allt)
        self.assertIn("_xlfn.DUMMY", wb)  # Excel 内部の名前は残す
        self.assertNotIn("ダミー外部シート", allt)
        self.assertNotIn("12345", allt)
        self.assertIn("<f>E1+1</f>", s1)  # 非表示の行の数式は、--also hidden-rows のときだけ外す
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

    def test_also_hidden_rows(self):
        out, log = ck.clean(self.data, ".xlsx", list(ck.CLEAN_ACTIONS) + ["hidden-rows", "hidden-cols"])
        self.assertNotIn("hidden-rowcol", codes(ck.check(ck.Pkg(out), ".xlsx")))  # 行・列は隠れたままでも、値が無ければ出さない
        self.assertNotIn("9999", texts(out)["xl/worksheets/sheet1.xml"])
        self.assertNotIn("<f", re.search(r'<row r="2".*?</row>', texts(out)["xl/worksheets/sheet1.xml"], re.S).group(0))  # 共有数式の親子とも外れる
        self.assertEqual(ck.integrity(out), [])
        s1 = texts(out)["xl/worksheets/sheet1.xml"]
        self.assertIn('<row r="2" hidden="1"><c r="A2"/><c r="B2"/><c r="C2"/><c r="D2"/></row>', s1)
        self.assertNotIn("公開の値", texts(out)["xl/sharedStrings.xml"])  # 共有文字列も詰まる
        self.assertTrue(any("非表示の行" in x for x in log))

    def test_unseen_text(self):
        # 見えている文字（見えているセルの値・数式・シート名）と固定語に当たらない文字を出す（2026-10-28）
        fs = [f for f in ck.check(ck.Pkg(self.data), ".xlsx") if f.code == "unseen-text"]
        got = {s for f in fs for s in f.samples}
        for word in ("ダミー極秘メモ", "使っていない旧担当", "公開の値", "ダミー作成者", "ダミーの古い部品", "極秘"):
            self.assertIn(word, got, word)  # 非表示シート・未使用・非表示の行・コメント・孤立した部品・非表示のシート名
        for word in ("見出し", "公開", "社外秘"):  # 見えているセル・シート名・見えている数式の中のシート名
            self.assertNotIn(word, got, word)
        out, _log = ck.clean(self.data, ".xlsx", list(ck.CLEAN_ACTIONS))
        after = {f.part: f.samples for f in ck.check(ck.Pkg(out), ".xlsx") if f.code == "unseen-text"}
        self.assertEqual(after["xl/sharedStrings.xml"], ["公開の値"])  # 非表示の行に残る値
        self.assertIn("ダミー太郎", after["xl/charts/chart1.xml"])  # グラフの写しに残る非表示シートの値

    def test_unseen_text_split_runs(self):
        # 書式で割れた文字（<r> ごと）も、つないで調べる。数・番地・自動の名前・ふりがなは出さない
        xml = ('<sst><si><r><t>3</t></r><r><t>月</t></r></si><si><t>表示</t><rPh sb="0" eb="2"><t>ヒョウジ</t></rPh></si></sst>'
               '<x><xdr:cNvPr id="2" name="グラフ 1"/><c r="A1"><v>12.5</v></c><dimension ref="A1:B3"/></x>')
        got = [ck._norm(x) for x in ck.text_candidates("p.xml", xml)]
        self.assertIn("3月", got)
        self.assertNotIn("ヒョウジ", got)
        self.assertTrue(ck._AUTO_NAME_RE.match("グラフ 1") and ck._AUTO_NAME_RE.match("PlaceHolder 3"))
        self.assertTrue(ck._STRUCT_TEXT_RE.match("12.5") and ck._STRUCT_TEXT_RE.match("A1:B3"))

    def test_unseen_text_skips_calc_features(self):
        # Excel が workbook.xml の末尾に書く計算機能の一覧（microsoft.com:RD など）は、文字として調べない（2026-10-30）
        xml = ('<extLst><ext><xcalcf:calcFeatures><xcalcf:feature name="microsoft.com:RD"/>'
               '<xcalcf:feature name="microsoft.com:LET_WF"/></xcalcf:calcFeatures></ext></extLst>'
               '<definedName name="ダミー名">1</definedName>')
        got = [ck._norm(x) for x in ck.text_candidates("xl/workbook.xml", xml)]
        self.assertIn("ダミー名", got)
        self.assertFalse([x for x in got if "microsoft.com" in x])

    def test_self_closing_cell_and_row(self):
        # 空のセル <c .../> と中身のない行 <row .../> の次を巻き込まない（2026-10-28 の修正。以前は次のセルの共有文字列を
        # 使っていないとみなして消し、番号が範囲の外になって Excel が修復していた。非表示の空の行の次の行も空にしていた）
        xml = ('<sheetData><row r="1"><c r="A1" s="1"/><c r="B1" t="s"><v>2</v></c></row>'
               '<row r="2" hidden="1"/><row r="3"><c r="A3"><v>9</v></c></row></sheetData>')
        pkg = ck.Pkg(zipit({"s.xml": xml}))
        self.assertEqual(ck.used_sst(pkg, ["s.xml"]), {2})
        self.assertEqual(ck.blank_hidden(xml, True, False), (xml, 0))
        self.assertEqual(ck.hidden_content(xml), (0, 0))

    def test_integrity_finds_bad_string_index(self):
        out, _log = ck.clean(self.data, ".xlsx", list(ck.CLEAN_ACTIONS))
        pkg = ck.Pkg(out)
        pkg.put("xl/worksheets/sheet1.xml", re.sub(r'(<c r="A1" t="s"><v>)\d+', r"\g<1>99", pkg.text("xl/worksheets/sheet1.xml")))
        self.assertTrue(any("範囲の外" in p for p in ck.integrity(pkg.tobytes())))

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
            self.assertTrue((Path(d) / "tmp" / "dummy.xlsx-report.md").exists())  # 報告は入力の隣の tmp/（room clean と同じ）
            self.assertIn("(clean)", (Path(d) / "tmp" / "dummy.xlsx-report.md").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(ck.main(["check", str(src)]), 1)
            self.assertIn("(check)", (Path(d) / "tmp" / "dummy.xlsx-report.md").read_text(encoding="utf-8").splitlines()[0])
            self.assertFalse((Path(d) / "dummy.xlsx-report.md").exists())
            self.assertEqual(ck.main(["clean", str(src), str(src)]), 2)
            self.assertEqual(ck.main(["clean", str(src), str(Path(d) / "out")]), 2)  # 上書きしない
            (Path(d) / "a.docx").write_bytes(b"x")
            self.assertEqual(ck.main(["check", str(Path(d) / "a.docx")]), 2)


class InPlaceTest(unittest.TestCase):
    def test_in_place_backs_up_original(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "dummy.xlsx"
            data = build_xlsx()
            src.write_bytes(data)
            ck.main(["clean", str(src)])
            self.assertEqual((Path(d) / "tmp" / "dummy_org1.xlsx").read_bytes(), data)  # 元は tmp/ に退避
            self.assertNotEqual(src.read_bytes(), data)  # 入力の位置は掃除済み
            self.assertTrue((Path(d) / "tmp" / "dummy_org1.xlsx-report.md").exists())  # 報告は退避した元と対
            self.assertFalse((Path(d) / "tmp" / "dummy.xlsx-report.md").exists())
            self.assertFalse((Path(d) / "dummy.xlsx.new").exists())
            ck.main(["clean", str(src)])  # もう一度: 番号が進む（掃除済みのものが _org2 になる）
            self.assertTrue((Path(d) / "tmp" / "dummy_org2.xlsx").exists())
            self.assertTrue((Path(d) / "tmp" / "dummy_org2.xlsx-report.md").exists())
            self.assertEqual((Path(d) / "tmp" / "dummy_org1.xlsx").read_bytes(), data)

    def test_integrity_failure_leaves_original(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "dummy.xlsx"
            data = build_xlsx()
            src.write_bytes(data)
            orig = ck.integrity
            ck.integrity = lambda x: ["dummy: 壊れている"]
            try:
                rc = ck.main(["clean", str(src)])
            finally:
                ck.integrity = orig
            self.assertEqual(rc, 2)
            self.assertEqual(src.read_bytes(), data)
            self.assertFalse((Path(d) / "tmp" / "dummy_org1.xlsx").exists())
            self.assertTrue((Path(d) / "tmp" / "dummy_org1.xlsx-report.md").exists())  # 止めても報告は書く


class IntegrityStopTest(unittest.TestCase):
    def test_no_output_when_integrity_fails(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "dummy.xlsx"
            src.write_bytes(build_xlsx())
            orig = ck.integrity
            ck.integrity = lambda data: ["dummy: 壊れている"]
            try:
                rc = ck.main(["clean", str(src), str(Path(d) / "out")])
            finally:
                ck.integrity = orig
            self.assertEqual(rc, 2)
            self.assertFalse((Path(d) / "out").exists())  # 出力は書かない
            self.assertTrue((Path(d) / "tmp" / "dummy.xlsx-report.md").exists())  # 報告は書く


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
        after = ck.check(ck.Pkg(out), ".pptx")
        self.assertLessEqual({"alt-text", "off-slide"}, codes(after))  # 報告だけのもの
        unseen = {s for f in after if f.code == "unseen-text" for s in f.samples}
        self.assertEqual(unseen, {"ダミーの代替テキスト"})  # 見えているスライドの文字は出ない

    def test_unseen_text(self):
        got = {s for f in ck.check(ck.Pkg(self.data), ".pptx") if f.code == "unseen-text" for s in f.samples}
        self.assertLessEqual({"ダミーの非表示メモ", "ダミーの話す内容", "ダミーのコメント", "ダミー作成者"}, got)
        self.assertNotIn("公開のスライド", got)


XDR = 'xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'


def with_parts(data, changes):
    parts = texts(data)
    parts.update(changes)
    return zipit({n: s for n, s in parts.items() if s is not None})


class StripProfileTest(unittest.TestCase):
    def xlsx(self):
        anchor = lambda body: f"<xdr:twoCellAnchor><xdr:from/><xdr:to/>{body}</xdr:twoCellAnchor>"
        drawing = (HDR + f"<xdr:wsDr {XDR} {R}>"
                   + anchor('<xdr:graphicFrame><a:graphic><c:chart xmlns:c="c" r:id="rId1"/></a:graphic></xdr:graphicFrame>')
                   + anchor('<xdr:pic><xdr:blipFill><a:blip r:embed="rId2"/></xdr:blipFill></xdr:pic>')
                   + anchor("<xdr:sp><xdr:txBody>ダミーの図形</xdr:txBody></xdr:sp>") + "</xdr:wsDr>")
        data = with_parts(build_xlsx(), {
            "xl/drawings/drawing1.xml": drawing,
            "xl/drawings/_rels/drawing1.xml.rels": rels(("rId1", "chart", "../charts/chart1.xml"), ("rId2", "image", "../media/image1.png")),
            "xl/media/image1.png": "ダミー画像",
            "[Content_Types].xml": texts(build_xlsx())["[Content_Types].xml"].replace("<Override", '<Default Extension="png" ContentType="image/png"/><Override', 1),
        })
        return data

    def test_strict_strips_kinds(self):
        out, log = ck.clean(self.xlsx(), ".xlsx", list(ck.CLEAN_ACTIONS) + list(ck.PROFILES["strict"][1]))
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        self.assertNotIn("xl/charts/chart1.xml", t)
        self.assertNotIn("xl/media/image1.png", t)
        d = t["xl/drawings/drawing1.xml"]
        self.assertNotIn("graphicFrame", d)
        self.assertNotIn("r:embed", d)
        self.assertIn("ダミーの図形", d)
        self.assertNotIn("rId", t["xl/drawings/_rels/drawing1.xml.rels"])

    def test_standard_keeps_kinds(self):
        out, _log = ck.clean(self.xlsx(), ".xlsx", list(ck.CLEAN_ACTIONS))
        self.assertIn("xl/charts/chart1.xml", texts(out))
        self.assertIn("xl/media/image1.png", texts(out))

    def test_allow_images(self):
        actions = list(ck.CLEAN_ACTIONS) + [a for a in ck.PROFILES["strict"][1] if a != "images"]
        out, _log = ck.clean(self.xlsx(), ".xlsx", actions)
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        self.assertNotIn("xl/charts/chart1.xml", t)
        self.assertIn("xl/media/image1.png", t)

    def test_pptx_pic_and_frame(self):
        P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        slide = (HDR + f'<p:sld {P} {R}><p:cSld><p:spTree><p:pic><p:blipFill><a:blip xmlns:a="a" r:embed="rId5"/></p:blipFill></p:pic>'
                 '<p:graphicFrame><a:graphic xmlns:a="a"><c:chart xmlns:c="c" r:id="rId6"/></a:graphic></p:graphicFrame>'
                 '<p:sp>残す文字</p:sp></p:spTree></p:cSld></p:sld>')
        base = build_pptx()
        old = texts(base)
        data = with_parts(base, {
            "ppt/slides/slide1.xml": slide,
            "ppt/slides/_rels/slide1.xml.rels": rels(("rId5", "image", "../media/a.jpeg"), ("rId6", "chart", "../charts/c.xml")),
            "ppt/media/a.jpeg": "x", "ppt/charts/c.xml": "<c/>",
            "[Content_Types].xml": old["[Content_Types].xml"].replace("<Override", '<Override PartName="/ppt/charts/c.xml" ContentType="application/xml"/><Override', 1),
        })
        out, _log = ck.clean(data, ".pptx", list(ck.CLEAN_ACTIONS) + list(ck.PROFILES["strict"][1]))
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        self.assertNotIn("ppt/media/a.jpeg", t)
        self.assertNotIn("ppt/charts/c.xml", t)
        s = t["ppt/slides/slide1.xml"]
        self.assertNotIn("p:pic", s)
        self.assertNotIn("graphicFrame", s)
        self.assertIn("残す文字", s)

    def test_cli_profile(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in"
            src.mkdir()
            f = src / "a.xlsx"
            f.write_bytes(self.xlsx())
            out = Path(d) / "out" / "a.xlsx"
            rc = ck.main(["clean", str(f), str(out), "--profile", "strict", "--allow", "images", "--report", str(Path(d) / "r.md")])
            self.assertIn(rc, (0, 1))
            t = texts(out.read_bytes())
            self.assertNotIn("xl/charts/chart1.xml", t)
            self.assertIn("xl/media/image1.png", t)
            self.assertEqual(ck.main(["clean", str(f), str(out), "--allow", "nothing", "--force"]), 2)
        self.assertEqual(ck.main(["profiles"]), 0)



class SensitiveCheckTest(unittest.TestCase):
    def run_check(self, texts, terms=()):
        orig = ck.visible_text_xlsx
        ck.visible_text_xlsx = lambda pkg: texts
        try:
            fs = []
            ck.check_sensitive(None, ".xlsx", fs, terms)
            return fs
        finally:
            ck.visible_text_xlsx = orig

    def test_load_terms_reads_mask_toml_shape(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "mask.toml"
            f.write_text('[terms.CUST]\nacme = ["ACME株式会社", "ACME"]\n[terms.PERSON]\nt = ["田中"]\n[columns]\n"a!b" = "CUST"\n', encoding="utf-8")
            self.assertEqual(ck.load_terms(f), ["ACME株式会社", "ACME", "田中"])

    def test_detects_amount_mail_phone_percent_and_terms(self):
        fs = self.run_check(["売上 ¥1,200,000 / 3億円", "a.b@example.com", "03-1234-5678", "達成率 85%", "アクメ商事の件"], ["アクメ商事"])
        by = {f.part: f for f in fs}
        self.assertEqual(set(by), {"金額", "メール", "電話番号", "大きな数", "割合・KPI", "mask.toml の語"})
        self.assertIn("3億円", by["金額"].samples)
        self.assertEqual({f.code for f in fs}, {"sensitive-pattern", "sensitive-term"})

    def test_plain_text_has_no_findings(self):
        self.assertEqual(self.run_check(["手順を整理する", "項目 12", "2026-11-02"]), [])

    def test_check_default_does_not_scan_sensitive(self):
        self.assertNotIn("sensitive-pattern", codes(ck.check(ck.Pkg(build_xlsx()), ".xlsx")))

TENANT = "11111111-2222-3333-4444-555555555555"
LABEL_ID = "66666666-7777-8888-9999-000000000000"
SP_URL = "https://dummytenant.sharepoint.com/sites/DummySite"


def add_tenant_parts(data, pres_part=None):
    """既存のダミーに、ラベル・customXml・共同編集の履歴など、テナントを特定できる部品を足す。"""
    t = texts(data)
    t["docMetadata/LabelInfo.xml"] = (HDR + f'<clbl:labelList xmlns:clbl="http://schemas.microsoft.com/office/2020/mipLabelMetadata">'
                                      f'<clbl:label id="{{{LABEL_ID}}}" siteId="{{{TENANT}}}" enabled="1"/></clbl:labelList>')
    t["customXml/item1.xml"] = HDR + f'<p:properties xmlns:p="http://schemas.microsoft.com/office/2006/metadata/properties"><Url>{SP_URL}/doc</Url></p:properties>'
    t["customXml/itemProps1.xml"] = HDR + '<ds:datastoreItem xmlns:ds="http://schemas.openxmlformats.org/officeDocument/2006/customXml" ds:itemID="{ITEM}"/>'
    t["customXml/_rels/item1.xml.rels"] = rels(("rId1", "customXmlProps", "itemProps1.xml"))
    t["_rels/.rels"] = t["_rels/.rels"].replace(
        "</Relationships>", '<Relationship Id="rIdL" Type="http://schemas.microsoft.com/office/2020/02/relationships/classificationlabels" '
        'Target="docMetadata/LabelInfo.xml"/></Relationships>')
    t["[Content_Types].xml"] = t["[Content_Types].xml"].replace("</Types>",
        '<Override PartName="/docMetadata/LabelInfo.xml" ContentType="application/vnd.ms-office.classificationlabels+xml"/>'
        '<Override PartName="/customXml/itemProps1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlProperties+xml"/></Types>')
    core = t["docProps/core.xml"].replace("</cp:coreProperties>", f"<dc:identifier>DOCID-{TENANT}</dc:identifier></cp:coreProperties>")
    t["docProps/core.xml"] = core
    t["docProps/app.xml"] = t.get("docProps/app.xml", APP).replace("</Properties>", f"<Template>{SP_URL}/t.potx</Template></Properties>")
    return t


def rel_add(t, part, item):
    rp = re.sub(r"([^/]+)$", r"_rels/\1.rels", part)
    t[rp] = t[rp].replace("</Relationships>", item + "</Relationships>")


class TenantTest(unittest.TestCase):
    def xlsx(self):
        t = add_tenant_parts(build_xlsx())
        t["xl/workbook.xml"] = t["xl/workbook.xml"].replace(
            "<sheets>", f'<fileSharing userName="dummy.user@dummytenant.onmicrosoft.com"/><xr:revisionPtr xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" documentId="13_ncr:1_{{{TENANT}}}"/><sheets>', 1)
        rel_add(t, "xl/workbook.xml", f'<Relationship Id="rIdCx" Type="{RT}customXml" Target="../customXml/item1.xml"/>')
        return zipit(t)

    def pptx(self):
        t = add_tenant_parts(build_pptx())
        t["ppt/changesInfos/changesInfo1.xml"] = HDR + f'<pc:chgInfo xmlns:pc="x"><pc:docChg userId="S::dummy.user@dummytenant.onmicrosoft.com::{TENANT}"/></pc:chgInfo>'
        t["ppt/revisionInfo.xml"] = HDR + f'<r:revInfo xmlns:r="x"><r:client id="{{{TENANT}}}"/></r:revInfo>'
        t["[Content_Types].xml"] = t["[Content_Types].xml"].replace("</Types>",
            '<Override PartName="/ppt/changesInfos/changesInfo1.xml" ContentType="application/vnd.ms-powerpoint.changesinfo+xml"/>'
            '<Override PartName="/ppt/revisionInfo.xml" ContentType="application/vnd.ms-powerpoint.revisioninfo+xml"/></Types>')
        rel_add(t, "ppt/presentation.xml",
                f'<Relationship Id="rIdCx" Type="{RT}customXml" Target="../customXml/item1.xml"/>'
                '<Relationship Id="rIdCh" Type="http://schemas.microsoft.com/office/2016/11/relationships/changesInfo" Target="changesInfos/changesInfo1.xml"/>'
                '<Relationship Id="rIdRv" Type="http://schemas.microsoft.com/office/2015/10/relationships/revisionInfo" Target="revisionInfo.xml"/>')
        t["ppt/tags/tag1.xml"] = HDR + '<p:tagLst xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:tag name="PATH" val="dummy"/></p:tagLst>'
        rel_add(t, "ppt/presentation.xml", f'<Relationship Id="rIdTg" Type="{RT}tags" Target="tags/tag1.xml"/>')
        t["ppt/slides/_rels/slide1.xml.rels"] = t["ppt/slides/_rels/slide1.xml.rels"].replace(
            "</Relationships>", f'<Relationship Id="rIdH" Type="{RT}hyperlink" Target="{SP_URL}/x" TargetMode="External"/></Relationships>')
        t["ppt/slides/slide1.xml"] = t["ppt/slides/slide1.xml"].replace(
            "<a:t>", '<a:t>', 1)
        return zipit(t)

    def test_check_finds_tenant(self):
        for data, ext in ((self.xlsx(), ".xlsx"), (self.pptx(), ".pptx")):
            fs = ck.check(ck.Pkg(data), ext)
            self.assertLessEqual({"label-info", "tenant-id", "custom-xml"}, codes(fs))
        self.assertLessEqual({"revision-ptr", "file-sharing"}, codes(ck.check(ck.Pkg(self.xlsx()), ".xlsx")))
        self.assertIn("pptx-revisions", codes(ck.check(ck.Pkg(self.pptx()), ".pptx")))

    def test_standard_clean_removes_labels_and_ids(self):
        for data, ext in ((self.xlsx(), ".xlsx"), (self.pptx(), ".pptx")):
            out, _log = ck.clean(data, ext, list(ck.CLEAN_ACTIONS))
            self.assertEqual(ck.integrity(out), [])
            t = texts(out)
            self.assertNotIn("docMetadata/LabelInfo.xml", t)
            self.assertNotIn("customXml/item1.xml", t)
            self.assertNotIn("dummytenant", "".join(v for n, v in t.items() if n.startswith(("docProps", "customXml", "ppt/changesInfos", "xl/workbook"))))
            allt = "\n".join(t.values())
            self.assertNotIn(LABEL_ID, allt)
            self.assertNotIn(f"DOCID-{TENANT}", allt)
            self.assertNotIn("fileSharing", allt)
            self.assertNotIn("revisionPtr", allt)
            self.assertNotIn("changesInfo", allt)
            self.assertNotIn("revisionInfo", allt)
            self.assertNotIn("classificationlabels", allt)

    def test_keep_labels(self):
        out, _log = ck.clean(self.xlsx(), ".xlsx", [a for a in ck.CLEAN_ACTIONS if a != "labels"])
        self.assertIn("docMetadata/LabelInfo.xml", texts(out))

    def test_strict_removes_links_and_tags(self):
        out, _log = ck.clean(self.pptx(), ".pptx", list(ck.CLEAN_ACTIONS) + list(ck.PROFILES["strict"][1]))
        self.assertEqual(ck.integrity(out), [])
        t = texts(out)
        self.assertNotIn("dummytenant", "\n".join(t.values()))
        self.assertNotIn("ppt/tags/tag1.xml", t)

    def test_standard_keeps_external_link_and_reports_it(self):
        out, _log = ck.clean(self.pptx(), ".pptx", list(ck.CLEAN_ACTIONS))
        self.assertIn(SP_URL, texts(out)["ppt/slides/_rels/slide1.xml.rels"])
        self.assertIn("tenant-id", codes(ck.check(ck.Pkg(out), ".pptx")))


if __name__ == "__main__":
    unittest.main()
