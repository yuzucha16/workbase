"""exceltext のテスト。標準ライブラリで組んだダミーの xlsx で、見えている値と図形だけが出ることを確かめる。"""
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import exceltext as ex  # noqa: E402

HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
XNS = ('xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
       'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
       'xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"')
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
PR = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'


def rels(*items):
    return HDR + f"<Relationships {PR}>" + "".join(
        f'<Relationship Id="{i}" Type="{RT}{t}" Target="{g}"/>' for i, t, g in items) + "</Relationships>"


def anchor(row, inner):
    return (f'<xdr:twoCellAnchor><xdr:from><xdr:col>0</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>{row}</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>'
            f'<xdr:to><xdr:col>2</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>{row + 2}</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:to>{inner}<xdr:clientData/></xdr:twoCellAnchor>')


def tb(i, text, hidden=False):
    h = ' hidden="1"' if hidden else ""
    return (f'<xdr:sp><xdr:nvSpPr><xdr:cNvPr id="{i}" name="TextBox {i}" descr="代替の秘密"{h}/><xdr:cNvSpPr txBox="1"/></xdr:nvSpPr>'
            f'<xdr:spPr/><xdr:txBody><a:bodyPr/><a:p><a:r><a:t>{text}</a:t></a:r></a:p></xdr:txBody></xdr:sp>')


def build():
    sst = (HDR + f'<sst {NS} count="4" uniqueCount="4">'
           '<si><t>品目</t></si><si><t>金額</t></si>'
           '<si><r><t>りんご</t></r><rPh sb="0" eb="3"><t>フリガナノヒミツ</t></rPh></si>'
           '<si><t>隠れた行の秘密</t></si></sst>')
    styles = (HDR + f'<styleSheet {NS}><numFmts count="1"><numFmt numFmtId="164" formatCode="yyyy/m/d"/></numFmts>'
              '<cellXfs count="4"><xf numFmtId="0"/><xf numFmtId="164"/><xf numFmtId="9"/><xf numFmtId="0"/></cellXfs></styleSheet>')
    sheet1 = (HDR + f'<worksheet {NS}><cols><col min="3" max="3" hidden="1"/></cols><sheetData>'
              '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c><c r="C1" t="inlineStr"><is><t>隠れた列の秘密</t></is></c><c r="D1" t="inlineStr"><is><t>日付</t></is></c></row>'
              '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2"><f>100+20</f><v>120</v></c><c r="D2" s="1"><v>46000</v></c><c r="E2" s="2"><v>0.125</v></c></row>'
              '<row r="3" hidden="1"><c r="A3" t="s"><v>3</v></c></row>'
              '<row r="5"><c r="A5" t="b"><v>1</v></c><c r="B5"><f>SUM(秘密の数式!A1)</f></c><c r="D5" t="inlineStr"><is><t>a|b\nc</t></is></c></row>'
              '</sheetData><drawing r:id="rId1"/></worksheet>')
    chart = (HDR + f'<c:chartSpace {XNS}><c:chart><c:title><c:tx><c:rich><a:p><a:r><a:t>売上の推移</a:t></a:r></a:p></c:rich></c:tx></c:title></c:chart></c:chartSpace>')
    gframe = ('<xdr:graphicFrame><xdr:nvGraphicFramePr><xdr:cNvPr id="5" name="Chart 5"/><xdr:cNvGraphicFramePr/></xdr:nvGraphicFramePr><xdr:xfrm/>'
              '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:chart r:id="rId1"/></a:graphicData></a:graphic></xdr:graphicFrame>')
    pic = '<xdr:pic><xdr:nvPicPr><xdr:cNvPr id="6" name="Picture 6" descr="画像の秘密"/><xdr:cNvPicPr/></xdr:nvPicPr><xdr:blipFill/><xdr:spPr/></xdr:pic>'
    cxn = ('<xdr:cxnSp><xdr:nvCxnSpPr><xdr:cNvPr id="7" name="c"/><xdr:cNvCxnSpPr><a:stCxn id="2" idx="0"/><a:endCxn id="3" idx="0"/>'
           '</xdr:cNvCxnSpPr></xdr:nvCxnSpPr><xdr:spPr/></xdr:cxnSp>')
    drawing = (HDR + f'<xdr:wsDr {XNS}>' + anchor(10, tb(3, "下の箱")) + anchor(1, tb(2, "上の箱")) + anchor(4, tb(4, "隠れた箱", hidden=True))
               + anchor(20, gframe) + anchor(30, pic) + anchor(40, cxn) + '</xdr:wsDr>')
    wb = (HDR + f'<workbook {NS}><workbookPr/><sheets>'
          '<sheet name="一覧" sheetId="1" r:id="rId1"/><sheet name="隠しシート" sheetId="2" state="hidden" r:id="rId2"/>'
          '<sheet name="とても隠し" sheetId="3" state="veryHidden" r:id="rId3"/></sheets>'
          '<definedNames><definedName name="秘密の名前">一覧!$A$1</definedName></definedNames></workbook>')
    hid = HDR + f'<worksheet {NS}><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>隠しシートの秘密</t></is></c></row></sheetData></worksheet>'
    files = {
        "[Content_Types].xml": HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
        "_rels/.rels": rels(("rId1", "officeDocument", "xl/workbook.xml")),
        "xl/workbook.xml": wb,
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml"), ("rId2", "worksheet", "worksheets/sheet2.xml"),
                                           ("rId3", "worksheet", "worksheets/sheet3.xml"), ("rId4", "sharedStrings", "sharedStrings.xml"),
                                           ("rId5", "styles", "styles.xml")),
        "xl/sharedStrings.xml": sst,
        "xl/styles.xml": styles,
        "xl/worksheets/sheet1.xml": sheet1,
        "xl/worksheets/sheet2.xml": hid,
        "xl/worksheets/sheet3.xml": hid.replace("隠しシートの秘密", "とても隠しの秘密"),
        "xl/worksheets/_rels/sheet1.xml.rels": rels(("rId1", "drawing", "../drawings/drawing1.xml"), ("rId2", "comments", "../comments1.xml")),
        "xl/comments1.xml": HDR + f'<comments {NS}><commentList><comment ref="A1"><text><t>コメントの秘密</t></text></comment></commentList></comments>',
        "xl/drawings/drawing1.xml": drawing,
        "xl/drawings/_rels/drawing1.xml.rels": rels(("rId1", "chart", "../charts/chart1.xml")),
        "xl/charts/chart1.xml": chart,
        "docProps/core.xml": HDR + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                                   'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>作者の秘密</dc:creator></cp:coreProperties>',
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for n, d in files.items():
            z.writestr(n, d)
    return buf.getvalue()


class T(unittest.TestCase):
    def setUp(self):
        self.md = ex.extract(build())

    def test_visible_only(self):
        for bad in ("隠しシート", "とても隠し", "隠れた行の秘密", "隠れた列の秘密", "フリガナノヒミツ", "コメントの秘密",
                    "秘密の名前", "秘密の数式", "代替の秘密", "画像の秘密", "隠れた箱", "作者の秘密", "TextBox"):
            self.assertNotIn(bad, self.md)

    def test_table_values(self):
        self.assertIn("## シート 1: 一覧", self.md)
        self.assertIn("| 行 | A | B | D | E |", self.md)  # 隠れた列 C は詰める
        self.assertIn("| 2 | りんご | 120 | 2025-12-09 | 12.5% |", self.md)  # 数式は計算済みの値、日付・% の書式
        self.assertIn("| 5 | TRUE |  | a\\|b<br>c |  |", self.md)  # 計算していない数式は空
        self.assertNotIn("| 3 |", self.md)

    def test_shapes(self):
        self.assertLess(self.md.index("上の箱"), self.md.index("下の箱"))  # 位置の順
        self.assertIn("- [グラフ: 売上の推移]", self.md)
        self.assertIn("- [画像]", self.md)
        self.assertIn("- 上の箱 → 下の箱", self.md)

    def test_cli_refuses_existing_output_and_other_ext(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "a.xlsx", Path(tmp) / "a.md"
            src.write_bytes(build())
            self.assertEqual(ex.main([str(src), str(dst)]), 0)
            self.assertEqual(ex.main([str(src), str(dst)]), 2)
            self.assertEqual(ex.main([str(src), str(dst), "--force"]), 0)
            self.assertEqual(ex.main([str(Path(tmp) / "a.pptx"), str(dst), "--force"]), 2)


if __name__ == "__main__":
    unittest.main()
