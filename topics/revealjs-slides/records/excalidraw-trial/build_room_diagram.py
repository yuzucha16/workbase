"""room の構造図を、1 つの仕様から .excalidraw(JSON)と SVG に出す。MCP なしの試験(方式 A)。

使い方: python -I build_room_diagram.py <出力ディレクトリ>
- .excalidraw は excalidraw.com か Obsidian の Excalidraw で開いて手直しできる。
- SVG は自前の描画(Excalidraw の書き出しではない)。revealjs に埋め込む用。
- 図の仕様は SPEC だけを直す。座標は左上起点の px。
"""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

BLUE, GRAY, INK, SUB = "#0017c1", "#767676", "#1a1a1a", "#4d4d4d"
PALE, LIGHT = "#e8f1fe", "#f2f2f2"
W, H = 980, 520

# kind: box / text / arrow。dash は破線、bold は太線、fill は塗り。
SPEC = [
    dict(kind="box", x=10, y=10, w=360, h=500, stroke=GRAY, fill=LIGHT, label="Windows(works)", size=24, top=True),
    dict(kind="box", x=40, y=70, w=300, h=100, stroke=GRAY, fill="#ffffff", label="_noai/", sub="原本・対応表(AI に見せない)", size=24),
    dict(kind="box", x=40, y=200, w=300, h=100, stroke=BLUE, fill=PALE, label="ai/", sub="作業フォルダ(渡す)", size=24, bold=True),
    dict(kind="box", x=40, y=330, w=300, h=100, stroke=GRAY, fill="#ffffff", label="areas/ projects/ …", sub="そのほかの works", size=22),
    dict(kind="box", x=610, y=10, w=360, h=500, stroke=BLUE, fill=PALE, label="部屋(専用の WSL)", size=24, top=True, bold=True),
    dict(kind="box", x=640, y=70, w=300, h=100, stroke=GRAY, fill=None, dash=True, label="/mnt/c は空", sub="automount を切る", size=22),
    dict(kind="box", x=640, y=200, w=300, h=100, stroke=BLUE, fill="#ffffff", label="/mnt/room/<Project>", sub="ai/ の中身だけが見える", size=22, bold=True),
    dict(kind="box", x=640, y=330, w=300, h=100, stroke=BLUE, fill="#ffffff", label="Claude Code", sub="一般ユーザー(ai)で動く", size=22),
    dict(kind="arrow", x1=342, y1=250, x2=638, y2=250, color=BLUE, label="room start がマウント", size=20, bold=True),
    dict(kind="text", cx=490, cy=285, text="成果物は", size=18, color=SUB),
    dict(kind="text", cx=490, cy=308, text="room close で戻す", size=18, color=SUB),
    dict(kind="text", cx=790, cy=462, text="interop を切る", size=18, color=SUB),
    dict(kind="text", cx=790, cy=486, text="Windows のプログラムを起動できない", size=18, color=SUB),
]


def tw(s, size):
    """文字列の幅の概算。全角は size、半角は 0.55 size。"""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)


def box_texts(e):
    """box の文字を (text, cx, cy, size, color) の列で返す。"""
    cx = e["x"] + e["w"] / 2
    if e.get("top"):
        return [(e["label"], cx, e["y"] + 30, e["size"], INK)]
    out = [(e["label"], cx, e["y"] + e["h"] * 0.36, e["size"], INK)]
    if e.get("sub"):
        out.append((e["sub"], cx, e["y"] + e["h"] * 0.70, 18, SUB))
    return out


def arrow_text(e):
    return (e["label"], (e["x1"] + e["x2"]) / 2, e["y1"] - 22, e["size"], e["color"])


_n = [0]


def base(type_, x, y, w, h, **kw):
    _n[0] += 1
    d = dict(id=f"el{_n[0]}", type=type_, x=x, y=y, width=w, height=h, angle=0,
             strokeColor=INK, backgroundColor="transparent", fillStyle="solid",
             strokeWidth=2, strokeStyle="solid", roughness=0, opacity=100,
             groupIds=[], frameId=None, roundness=None, seed=1000 + _n[0],
             version=1, versionNonce=2000 + _n[0], isDeleted=False,
             boundElements=None, updated=1, link=None, locked=False)
    d.update(kw)
    return d


def text_el(t, cx, cy, size, color):
    w, h = tw(t, size), size * 1.25
    return base("text", cx - w / 2, cy - h / 2, w, h, strokeColor=color, text=t,
                originalText=t, fontSize=size, fontFamily=2, textAlign="center",
                verticalAlign="middle", containerId=None, lineHeight=1.25, autoResize=True)


def build_excalidraw():
    els = []
    for e in SPEC:
        if e["kind"] == "box":
            els.append(base("rectangle", e["x"], e["y"], e["w"], e["h"],
                            strokeColor=e["stroke"], strokeWidth=3 if e.get("bold") else 2,
                            backgroundColor=e["fill"] or "transparent",
                            strokeStyle="dashed" if e.get("dash") else "solid",
                            roundness={"type": 3}))
            els += [text_el(*t) for t in box_texts(e)]
        elif e["kind"] == "arrow":
            dx, dy = e["x2"] - e["x1"], e["y2"] - e["y1"]
            els.append(base("arrow", e["x1"], e["y1"], dx, dy, strokeColor=e["color"],
                            strokeWidth=3, points=[[0, 0], [dx, dy]], lastCommittedPoint=None,
                            startBinding=None, endBinding=None, startArrowhead=None,
                            endArrowhead="arrow", elbowed=False))
            els.append(text_el(*arrow_text(e)))
        else:
            els.append(text_el(e["text"], e["cx"], e["cy"], e["size"], e["color"]))
    return {"type": "excalidraw", "version": 2, "source": "build_room_diagram.py",
            "elements": els, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}


def svg_text(t, cx, cy, size, color, bold=False):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text x="{cx:.0f}" y="{cy + size * 0.35:.0f}" font-size="{size}" '
            f'text-anchor="middle" fill="{color}"{weight}>{escape(t)}</text>')


def build_svg():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Windows の works と専用 WSL の部屋の関係。ai/ だけをマウントして渡す。" '
         f'font-family="\'Noto Sans JP\',\'Yu Gothic\',sans-serif">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>']
    for e in SPEC:
        if e["kind"] == "box":
            dash = ' stroke-dasharray="8 6"' if e.get("dash") else ""
            sw = 3 if e.get("bold") else 2
            p.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="10" '
                     f'fill="{e["fill"] or "none"}" stroke="{e["stroke"]}" stroke-width="{sw}"{dash}/>')
            p += [svg_text(*t) for t in box_texts(e)]
        elif e["kind"] == "arrow":
            p.append(f'<line x1="{e["x1"]}" y1="{e["y1"]}" x2="{e["x2"] - 4}" y2="{e["y2"]}" '
                     f'stroke="{e["color"]}" stroke-width="3.5" marker-end="url(#ah)"/>')
            p.append(svg_text(*arrow_text(e), bold=True))
        else:
            p.append(svg_text(e["text"], e["cx"], e["cy"], e["size"], e["color"]))
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "room-structure.excalidraw").write_text(json.dumps(build_excalidraw(), ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    (out / "room-structure.svg").write_text(build_svg(), encoding="utf-8", newline="\n")
    print("wrote", out)
