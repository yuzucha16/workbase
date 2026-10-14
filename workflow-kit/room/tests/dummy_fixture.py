"""マスク・復元の確認用ダミーを作る（標準ライブラリだけ。実在の名前は使わない）。

作るもの（_noai/raw/ に置く）:
  dummy_sales.xlsx     実際のピボットテーブル、コメント、定義名、プロパティ、通常+太字が混ざったセルを含む
  dummy_customers.csv  cp932 の csv（全角・半角カナ・英字の表記ゆれを含む）
作るもの（_noai/ に置く）:
  mask.toml            上のダミー用の語の表

使い方: python tests/dummy_fixture.py <Project のディレクトリ>   （room の下で。<Project>/_noai/ に作る。単体テスト（unittest discover）の対象ではない）
語の意味: アクメ商事=顧客A、ベータ工業=顧客B、新規ガンマ社=辞書にない顧客C（列指定で拾う）、田中太郎=担当者。
"""
import io
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
RNS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

SHEET1 = "売上"
SHEET2 = "集計_アクメ商事"  # シート名に語が入るケース

CUSTOMERS = ["アクメ商事株式会社", "ベータ工業", "新規ガンマ社"]  # ピボットの共有アイテム（この順）
ROWS = [  # 顧客, 担当, 金額
    ("アクメ商事株式会社", "田中太郎", 1000),
    ("ベータ工業", "田中太郎", 2000),
    ("新規ガンマ社", "田中太郎", 500),
    ("ベータ工業", "田中太郎", 800),
]


class SST:
    def __init__(self):
        self.items = []

    def add(self, xml_si):
        self.items.append(xml_si)
        return len(self.items) - 1

    def text(self, s):
        return self.add(f"<si><t>{escape(s)}</t></si>")

    def xml(self):
        return (HDR + f'<sst {NS} count="{len(self.items)}" uniqueCount="{len(self.items)}">'
                + "".join(self.items) + "</sst>")


def build_xlsx():
    sst = SST()
    t = sst.text
    # 売上シート
    h = [t("顧客名"), t("担当"), t("金額")]
    rich = sst.add('<si><r><t>アクメ</t></r><r><rPr><b/><sz val="11"/><rFont val="Calibri"/></rPr>'
                   '<t>商事</t></r><r><t>への請求メモ</t></r></si>')  # 語が run をまたぐ
    mail = t("連絡先 info@acme.co.jp / ACME Trading")
    cust = [t(c) for c in CUSTOMERS]
    tanaka = t("田中太郎")

    def sc(ref, idx):
        return f'<c r="{ref}" t="s"><v>{idx}</v></c>'

    rows = ['<row r="1">' + sc("A1", h[0]) + sc("B1", h[1]) + sc("C1", h[2]) + sc("E1", rich) + "</row>"]
    for i, (c, _p, amt) in enumerate(ROWS, start=2):
        r = f'<row r="{i}">' + sc(f"A{i}", cust[CUSTOMERS.index(c)]) + sc(f"B{i}", tanaka) + f'<c r="C{i}"><v>{amt}</v></c>'
        if i == 2:
            r += sc("E2", mail)
        rows.append(r + "</row>")
    sheet1 = (HDR + f'<worksheet {NS} {RNS}><dimension ref="A1:E5"/><sheetData>' + "".join(rows)
              + '</sheetData><legacyDrawing r:id="rId1"/></worksheet>')
    sheet1_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/vmlDrawing" Target="../drawings/vmlDrawing1.vml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="../comments1.xml"/>'
                   "</Relationships>")

    # 集計シート（ピボットの表示。値はキャッシュと一致させる）
    totals = {c: sum(a for cc, _p, a in ROWS if cc == c) for c in CUSTOMERS}
    lab = t("行ラベル"); dat = t("合計 / 金額"); grand = t("総計")
    p_rows = ['<row r="3">' + sc("A3", lab) + sc("B3", dat) + "</row>"]
    for i, c in enumerate(CUSTOMERS, start=4):
        p_rows.append(f'<row r="{i}">' + sc(f"A{i}", cust[i - 4]) + f'<c r="B{i}"><v>{totals[c]}</v></c></row>')
    p_rows.append('<row r="7">' + sc("A7", grand) + f'<c r="B7"><v>{sum(totals.values())}</v></c></row>')
    sheet2 = (HDR + f'<worksheet {NS}><dimension ref="A3:B7"/><sheetData>' + "".join(p_rows) + "</sheetData></worksheet>")
    sheet2_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/pivotTable" Target="../pivotTables/pivotTable1.xml"/>'
                   "</Relationships>")

    pivot_table = (HDR + f'<pivotTableDefinition {NS} name="ピボット1" cacheId="1" applyNumberFormats="0" applyBorderFormats="0" '
                   'applyFontFormats="0" applyPatternFormats="0" applyAlignmentFormats="0" applyWidthHeightFormats="1" '
                   'dataCaption="値" updatedVersion="6" minRefreshableVersion="3" useAutoFormatting="1" itemPrintTitles="1" '
                   'createdVersion="6" indent="0" outline="1" outlineData="1" multipleFieldFilters="0">'
                   '<location ref="A3:B7" firstHeaderRow="1" firstDataRow="1" firstDataCol="1"/>'
                   '<pivotFields count="3"><pivotField axis="axisRow" showAll="0"><items count="4">'
                   '<item x="0"/><item x="1"/><item x="2"/><item t="default"/></items></pivotField>'
                   '<pivotField showAll="0"/><pivotField dataField="1" showAll="0"/></pivotFields>'
                   '<rowFields count="1"><field x="0"/></rowFields>'
                   '<rowItems count="4"><i><x/></i><i><x v="1"/></i><i><x v="2"/></i><i t="grand"><x/></i></rowItems>'
                   '<colItems count="1"><i/></colItems>'
                   '<dataFields count="1"><dataField name="合計 / 金額" fld="2" baseField="0" baseItem="0"/></dataFields>'
                   "</pivotTableDefinition>")
    pivot_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/pivotCacheDefinition" Target="../pivotCache/pivotCacheDefinition1.xml"/>'
                  "</Relationships>")
    cache_def = (HDR + f'<pivotCacheDefinition {NS} {RNS} r:id="rId1" refreshedBy="作成者" refreshedDate="45000" '
                 f'createdVersion="6" refreshedVersion="6" minRefreshableVersion="3" recordCount="{len(ROWS)}">'
                 f'<cacheSource type="worksheet"><worksheetSource ref="A1:C5" sheet="{SHEET1}"/></cacheSource>'
                 '<cacheFields count="3">'
                 '<cacheField name="顧客名" numFmtId="0"><sharedItems count="3">'
                 + "".join(f'<s v="{escape(c)}"/>' for c in CUSTOMERS) + "</sharedItems></cacheField>"
                 '<cacheField name="担当" numFmtId="0"><sharedItems count="1"><s v="田中太郎"/></sharedItems></cacheField>'
                 '<cacheField name="金額" numFmtId="0"><sharedItems containsSemiMixedTypes="0" containsString="0" '
                 'containsNumber="1" containsInteger="1" minValue="500" maxValue="2000"/></cacheField>'
                 "</cacheFields></pivotCacheDefinition>")
    cache_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/pivotCacheRecords" Target="pivotCacheRecords1.xml"/>'
                  "</Relationships>")
    records = (HDR + f'<pivotCacheRecords {NS} count="{len(ROWS)}">'
               + "".join(f'<r><x v="{CUSTOMERS.index(c)}"/><x v="0"/><n v="{a}"/></r>' for c, _p, a in ROWS)
               + "</pivotCacheRecords>")

    workbook = (HDR + f'<workbook {NS} {RNS}><sheets>'
                f'<sheet name="{SHEET1}" sheetId="1" r:id="rId1"/><sheet name="{SHEET2}" sheetId="2" r:id="rId2"/></sheets>'
                f'<definedNames><definedName name="アクメ商事_範囲">{SHEET1}!$A$1:$C$5</definedName></definedNames>'
                '<calcPr calcId="191029"/><pivotCaches><pivotCache cacheId="1" r:id="rId5"/></pivotCaches></workbook>')
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
    wb_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               f'<Relationship Id="rId1" Type="{R}worksheet" Target="worksheets/sheet1.xml"/>'
               f'<Relationship Id="rId2" Type="{R}worksheet" Target="worksheets/sheet2.xml"/>'
               f'<Relationship Id="rId3" Type="{R}styles" Target="styles.xml"/>'
               f'<Relationship Id="rId4" Type="{R}sharedStrings" Target="sharedStrings.xml"/>'
               f'<Relationship Id="rId5" Type="{R}pivotCacheDefinition" Target="pivotCache/pivotCacheDefinition1.xml"/>'
               "</Relationships>")
    styles = (HDR + f'<styleSheet {NS}><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    comments = (HDR + f'<comments {NS}><authors><author>田中太郎</author></authors><commentList>'
                '<comment ref="A2" authorId="0"><text><r><t>田中太郎さんに確認する（アクメ商事の請求先）</t></r></text></comment>'
                "</commentList></comments>")
    vml = ('<xml xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" '
           'xmlns:x="urn:schemas-microsoft-com:office:excel"><o:shapelayout v:ext="edit"><o:idmap v:ext="edit" data="1"/></o:shapelayout>'
           '<v:shapetype id="_x0000_t202" coordsize="21600,21600" o:spt="202" path="m,l,21600r21600,l21600,xe">'
           '<v:stroke joinstyle="miter"/><v:path gradientshapeok="t" o:connecttype="rect"/></v:shapetype>'
           '<v:shape id="_x0000_s1025" type="#_x0000_t202" style="position:absolute;margin-left:80pt;margin-top:5pt;width:120pt;height:60pt;z-index:1;visibility:hidden" '
           'fillcolor="#ffffe1" o:insetmode="auto"><v:fill color2="#ffffe1"/><v:shadow on="t" color="black" obscured="t"/>'
           '<v:path o:connecttype="none"/><v:textbox style="mso-direction-alt:auto"><div style="text-align:left"></div></v:textbox>'
           '<x:ClientData ObjectType="Note"><x:MoveWithCells/><x:SizeWithCells/><x:Anchor>1, 15, 1, 2, 3, 15, 5, 16</x:Anchor>'
           "<x:AutoFill>False</x:AutoFill><x:Row>1</x:Row><x:Column>0</x:Column></x:ClientData></v:shape></xml>")
    core = (HDR + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>アクメ商事 売上ダミー</dc:title>'
            "<dc:creator>田中太郎</dc:creator><cp:lastModifiedBy>田中太郎</cp:lastModifiedBy></cp:coreProperties>")
    app = (HDR + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           "<Application>Microsoft Excel</Application><Company>アクメ商事株式会社</Company></Properties>")
    ct = (HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="vml" ContentType="application/vnd.openxmlformats-officedocument.vmlDrawing"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
          '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
          '<Override PartName="/xl/comments1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml"/>'
          '<Override PartName="/xl/pivotTables/pivotTable1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml"/>'
          '<Override PartName="/xl/pivotCache/pivotCacheDefinition1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheDefinition+xml"/>'
          '<Override PartName="/xl/pivotCache/pivotCacheRecords1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheRecords+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          "</Types>")
    root_rels = (HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 f'<Relationship Id="rId1" Type="{R}officeDocument" Target="xl/workbook.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 f'<Relationship Id="rId3" Type="{R}extended-properties" Target="docProps/app.xml"/>'
                 "</Relationships>")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/sharedStrings.xml", sst.xml())
        z.writestr("xl/worksheets/sheet1.xml", sheet1)
        z.writestr("xl/worksheets/_rels/sheet1.xml.rels", sheet1_rels)
        z.writestr("xl/worksheets/sheet2.xml", sheet2)
        z.writestr("xl/worksheets/_rels/sheet2.xml.rels", sheet2_rels)
        z.writestr("xl/comments1.xml", comments)
        z.writestr("xl/drawings/vmlDrawing1.vml", vml)
        z.writestr("xl/pivotTables/pivotTable1.xml", pivot_table)
        z.writestr("xl/pivotTables/_rels/pivotTable1.xml.rels", pivot_rels)
        z.writestr("xl/pivotCache/pivotCacheDefinition1.xml", cache_def)
        z.writestr("xl/pivotCache/_rels/pivotCacheDefinition1.xml.rels", cache_rels)
        z.writestr("xl/pivotCache/pivotCacheRecords1.xml", records)
    return buf.getvalue()


CSV = ("顧客名,担当,備考,金額\n"
       "アクメ商事株式会社,田中太郎,ACME TRADING と取引,1000\n"
       "ＡＣＭＥ　Ｔrading,田中,ﾍﾞｰﾀ工業の紹介,1500\n"
       "新規ガンマ社,山田,辞書にない顧客（列指定で拾う）,500\n")

TOML = """# ダミー用。顧客A=アクメ商事、顧客B=ベータ工業、担当者=田中太郎（すべて架空）
[terms.CUST]
acme = ["アクメ商事株式会社", "アクメ商事", "ACME Trading", "info@acme.co.jp"]
beta = ["ベータ工業", "ﾍﾞｰﾀ工業"]

[terms.PERSON]
tanaka = ["田中太郎", "田中"]

[columns]
"売上!顧客名" = "CUST"
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("使い方: python tests/dummy_fixture.py <Project のディレクトリ>")
    ROOT = Path(sys.argv[1]).resolve()
    RAW = ROOT / "_noai" / "raw"
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "dummy_sales.xlsx").write_bytes(build_xlsx())
    (RAW / "dummy_customers.csv").write_bytes(CSV.encode("cp932"))
    (ROOT / "_noai" / "mask.toml").write_text(TOML, encoding="utf-8", newline="\n")
    print("作った:", RAW / "dummy_sales.xlsx", RAW / "dummy_customers.csv", ROOT / "_noai" / "mask.toml")


if __name__ == "__main__":
    main()
