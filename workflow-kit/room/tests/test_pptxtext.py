"""pptxtext のテスト。標準ライブラリで組んだダミーの pptx で、見えている内容だけが出ることを確かめる。"""
import io
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pptxtext as px  # noqa: E402

HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
NS = ('xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
PR = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'


def rels(*items):
    return HDR + f"<Relationships {PR}>" + "".join(
        f'<Relationship Id="{i}" Type="{RT}{t}" Target="{g}"/>' for i, t, g in items) + "</Relationships>"


def sp(i, text, x, y, title=False, hidden=False, lvl=None):
    ph = '<p:nvPr><p:ph type="title"/></p:nvPr>' if title else "<p:nvPr/>"
    h = ' hidden="1"' if hidden else ""
    pp = f'<a:pPr lvl="{lvl}"/>' if lvl is not None else ""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="n{i}" descr="代替の秘密"{h}/><p:cNvSpPr/>{ph}</p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="100" cy="100"/></a:xfrm></p:spPr>'
            f'<p:txBody><a:p>{pp}<a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')


def build():
    body1 = (sp(2, "論点", 0, 0, title=True) + sp(3, "下の文", 0, 5000) + sp(4, "上の文", 0, 1000)
             + sp(5, "子の項目", 0, 2000, lvl=1) + sp(6, "隠れた図形", 0, 3000, hidden=True)
             + sp(7, "枠外の文字", 99999999, 0))
    cxn = ('<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="9" name="c"/><p:cNvCxnSpPr><a:stCxn id="3" idx="0"/><a:endCxn id="4" idx="0"/>'
           '</p:cNvCxnSpPr><p:nvPr/></p:nvCxnSpPr><p:spPr/></p:cxnSp>')
    tbl = ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="10" name="t"/></p:nvGraphicFramePr>'
           '<p:xfrm><a:off x="0" y="9000"/><a:ext cx="100" cy="100"/></p:xfrm><a:graphic><a:graphicData><a:tbl>'
           '<a:tr><a:tc><a:txBody><a:p><a:r><a:t>列A</a:t></a:r></a:p></a:txBody></a:tc>'
           '<a:tc><a:txBody><a:p><a:r><a:t>列B</a:t></a:r></a:p></a:txBody></a:tc></a:tr>'
           '<a:tr><a:tc><a:txBody><a:p><a:r><a:t>1</a:t></a:r></a:p></a:txBody></a:tc>'
           '<a:tc><a:txBody><a:p><a:r><a:t>2</a:t></a:r></a:p></a:txBody></a:tc></a:tr></a:tbl></a:graphicData></a:graphic></p:graphicFrame>')
    pic = '<p:pic><p:nvPicPr><p:cNvPr id="11" name="p" descr="画像の秘密"/></p:nvPicPr><p:blipFill/><p:spPr/></p:pic>'

    def slide(inner, hidden=False):
        return (HDR + f'<p:sld {NS}' + (' show="0"' if hidden else "") +
                f'><p:cSld><p:spTree>{inner}</p:spTree></p:cSld></p:sld>')
    pres = (HDR + f'<p:presentation {NS}><p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId3"/>'
            '</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/></p:presentation>')
    files = {
        "[Content_Types].xml": HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
        "_rels/.rels": rels(("rId1", "officeDocument", "ppt/presentation.xml")),
        "ppt/presentation.xml": pres,
        "ppt/_rels/presentation.xml.rels": rels(("rId2", "slide", "slides/slide1.xml"), ("rId3", "slide", "slides/slide2.xml")),
        "ppt/slides/slide1.xml": slide(body1 + cxn + tbl + pic),
        "ppt/slides/slide2.xml": slide(sp(2, "非表示スライドの文字", 0, 0), hidden=True),
        "ppt/slides/_rels/slide1.xml.rels": rels(("rId1", "notesSlide", "../notesSlides/n1.xml")),
        "ppt/notesSlides/n1.xml": HDR + f'<p:notes {NS}><p:cSld><p:spTree>{sp(2, "ノートの秘密", 0, 0)}</p:spTree></p:cSld></p:notes>',
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for n, d in files.items():
            z.writestr(n, d)
    return buf.getvalue()


class T(unittest.TestCase):
    def setUp(self):
        self.md = px.extract(build())

    def test_visible_only(self):
        for bad in ("非表示スライドの文字", "ノートの秘密", "隠れた図形", "枠外の文字", "代替の秘密", "画像の秘密"):
            self.assertNotIn(bad, self.md)

    def test_title_and_order(self):
        self.assertIn("## スライド 1: 論点", self.md)
        self.assertLess(self.md.index("上の文"), self.md.index("下の文"))
        self.assertIn("  - 子の項目", self.md)

    def test_table_picture_arrow(self):
        self.assertIn("| 列A | 列B |", self.md)
        self.assertIn("| 1 | 2 |", self.md)
        self.assertIn("[画像]", self.md)
        self.assertIn("下の文 → 上の文", self.md)


if __name__ == "__main__":
    unittest.main()
