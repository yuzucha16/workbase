"""revealjs 図解レイアウトの生成スクリプト。

型と文言（辞書または JSON）から、Quarto の qmd を出す。手書きの SVG を避ける。

使い方:
  python -I gen_layouts.py                      # 組み込みの見本から qmd を出す（標準出力）
  python -I gen_layouts.py -o out.qmd           # ファイルへ
  python -I gen_layouts.py --spec spec.json -o out.qmd

出力の qmd は、同じディレクトリの revealjs-diagram-theme.scss と
revealjs-diagram-icons.html を読む（render は両ファイルを同じ場所に置いて行う）。

型:
  箱の型  A 左右 / B 上左右+下全幅 / D 左一本+右2 / E 1ブロック / F 2x2 / G 上全幅+下左右
  H 行ラベル x 列（行・列は文言の数で決まる）
  I 工程 x 行（シェブロンの列見出し。行ラベルは任意）
  J 表（濃紺ヘッダー + 薄グレー行）
"""
import argparse
import html
import json
import sys

BLUE, GRAY, TEXT = "#1f5fd1", "#9aa5b1", "#1f2933"

HEADER = """---
title: "{title}"
format:
  revealjs:
    theme: [default, revealjs-diagram-theme.scss]
    width: 1280
    height: 720
    margin: 0.06
    slide-number: true
    transition: none
    embed-resources: true
    include-before-body: revealjs-diagram-icons.html
---
"""


def esc(s):
    return html.escape(str(s), quote=False)


def raw(s):
    return "```{=html}\n" + s + "\n```\n"


# ---- 図（ダミーの n ブロックの流れ。実スライドでは fig に SVG 文字列を渡す） ----
def flow_svg(n=3, hl=1, w=280, h=100, vertical=False):
    if vertical:
        bw, bh, gap = w - 4, (h - 4 - 28 * (n - 1)) / n, 28
        parts = []
        for i in range(n):
            y = 2 + i * (bh + gap)
            on = i == hl
            parts.append(_block(2, y, bw, bh, i + 1, on))
            if i < n - 1:
                ay = y + bh
                parts.append(f'<line x1="{w/2}" y1="{ay+4}" x2="{w/2}" y2="{ay+12}" stroke="{BLUE}" stroke-width="3.5"/>'
                             f'<polygon points="{w/2},{ay+24} {w/2-7},{ay+12} {w/2+7},{ay+12}" fill="{BLUE}"/>')
        return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"
    gap = 28
    bw, bh = (w - 4 - gap * (n - 1)) / n, h - 20
    parts = []
    for i in range(n):
        x = 2 + i * (bw + gap)
        parts.append(_block(x, 10, bw, bh, i + 1, i == hl))
        if i < n - 1:
            ax = x + bw
            parts.append(f'<line x1="{ax+4}" y1="{h/2}" x2="{ax+12}" y2="{h/2}" stroke="{BLUE}" stroke-width="3.5"/>'
                         f'<polygon points="{ax+24},{h/2} {ax+12},{h/2-7} {ax+12},{h/2+7}" fill="{BLUE}"/>')
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def _block(x, y, w, h, label, on):
    fill, stroke, sw = ("#eaf1fd", BLUE, 3) if on else ("#f3f4f6", GRAY, 2)
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<text x="{x+w/2:.1f}" y="{y+h/2+7:.1f}" font-size="20" text-anchor="middle" fill="{TEXT}">{esc(label)}</text>')


# ---- 箱の型 ----
def cell(c, extra=""):
    cls = " ".join(x for x in ["cell", c.get("tone"), extra] if x)
    out = f"::: {{.{cls.replace(' ', ' .')}}}\n"
    if c.get("tab"):
        icon = f'<svg viewBox="0 0 24 24"><use href="#i-{c["icon"]}"/></svg>' if c.get("icon") else ""
        out += raw(f'<div class="tab">{icon}{esc(c["tab"])}</div>') + "\n"
    fig = c.get("fig")
    if fig is not None:
        svg = fig if isinstance(fig, str) else flow_svg(**fig)
        out += "::: {.fig}\n" + raw(svg) + ":::\n"
    if c.get("text"):
        out += "::: {.txt}\n" + "<br>".join(esc(t) for t in c["text"].split("\n")) + "\n:::\n"
    return out + ":::\n"


BOX_COUNT = {"A": 2, "B": 3, "D": 3, "E": 1, "F": 4, "G": 3}


def box_slide(s):
    t = s["type"]
    cells = s["cells"]
    if len(cells) != BOX_COUNT[t]:
        raise SystemExit(f"型 {t} の cells は {BOX_COUNT[t]} 個（{len(cells)} 個ありました）")
    out = f"::: {{.lay .lay-{t.lower()}}}\n"
    if t == "B":
        out += cell(cells[0]) + f"::: {{.link}}\n{esc(s.get('link', '▶'))}\n:::\n" + cell(cells[1]) + cell(cells[2], "wide")
    elif t == "D":
        out += cell(cells[0], "tall") + cell(cells[1]) + cell(cells[2])
    elif t == "G":
        out += cell(cells[0], "wide") + cell(cells[1]) + cell(cells[2])
    else:
        out += "".join(cell(c) for c in cells)
    return out + ":::\n"


# ---- H / I / J（行・列の数は文言の数で決まる。間隔は scss の --gap に集約） ----
def lines(v):
    """セル文言: 文字列は 1 段落（\\n で改行）、リストは箇条書き。"""
    if isinstance(v, list):
        return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in v) + "</ul>"
    return "<br>".join(esc(x) for x in str(v).split("\n"))


def grid(s, chevron):
    cols = s.get("cols")
    rows = s["rows"]
    ncol = max(len(r["cells"]) for r in rows) if rows else len(cols or [])
    if cols:
        ncol = max(ncol, len(cols))
    has_label = any(r.get("label") for r in rows)
    for r in rows:  # 足りない列は空で埋める（揃える）
        r["cells"] = list(r["cells"]) + [""] * (ncol - len(r["cells"]))
    tracks = (["var(--lw)"] if has_label else []) + ["1fr"] * ncol
    nrow = len(rows)
    style = f"grid-template-columns:{' '.join(tracks)};grid-template-rows:{'auto ' if cols else ''}repeat({nrow},1fr);"
    if s.get("height"):
        style += f"--h:{s['height']};"
    emph = s.get("emphasize")  # 強調する列番号（0 始まり。負の数は後ろから）
    if emph is not None and emph < 0:
        emph += ncol
    cls = "mx" + (" chev" if chevron else "") + (" has-label" if has_label else "")
    out = [f'<div class="{cls}" style="{style}">']
    if cols:
        if has_label:
            out.append('<div class="corner"></div>')
        out += [f'<div class="h{" em" if i == emph else ""}"><span>{lines(c)}</span></div>' for i, c in enumerate(cols)]
    for r in rows:
        if has_label:
            out.append(f'<div class="rl"><span>{lines(r.get("label", ""))}</span></div>')
        out += [f'<div class="c{" em" if i == emph else ""}">{lines(c)}</div>' for i, c in enumerate(r["cells"])]
    out.append("</div>")
    return raw("\n".join(out))


def table_slide(s):
    head = s["head"]
    align = s.get("align") or ["l"] * len(head)
    index = s.get("index", False)
    out = ['<table class="tb"' + (f' style="--h:{s["height"]}"' if s.get("height") else "") + ">", "<thead><tr>"]
    if index:
        out.append('<th class="no">#</th>')
    out += [f'<th class="{a}">{lines(h)}</th>' for h, a in zip(head, align)]
    out.append("</tr></thead><tbody>")
    for n, row in enumerate(s["rows"], 1):
        out.append("<tr>" + (f'<td class="no">{n}</td>' if index else "")
                   + "".join(f'<td class="{a}">{lines(v)}</td>' for v, a in zip(list(row) + [""] * (len(head) - len(row)), align))
                   + "</tr>")
    out.append("</tbody></table>")
    return raw("".join(out))


def slide(s):
    t = s["type"]
    body = {"H": lambda: grid(s, False), "I": lambda: grid(s, True), "J": lambda: table_slide(s)}.get(t) or (lambda: box_slide(s))
    return f"## {s['title']}\n\n{body()}\n"


def build(spec):
    return HEADER.format(title=spec.get("title", "レイアウト見本")) + "\n" + "\n".join(slide(s) for s in spec["slides"])


# ---- 組み込みの見本（ダミーの文言。行・列の数を変えた例を並べる） ----
def _c(tone, icon, tab, fig=None, text="文字は短く\n2〜3行"):
    return {"tone": tone, "icon": icon, "tab": tab, "fig": fig if fig is not None else {}, "text": text}


SAMPLE = {
    "title": "レイアウト見本",
    "slides": [
        {"title": "A 左右二分割（比較）", "type": "A", "cells": [_c("red", "ban", "左"), _c("green", "check", "右")]},
        {"title": "B 上は左右・下は全幅", "type": "B", "cells": [
            _c("gray", "pc", "左"), _c("green", "room", "右"),
            _c("", "shield", "共通", {"n": 5, "hl": 2, "w": 570, "h": 92}, "共通の前提\n1〜2行")]},
        {"title": "D 左は一本・右は2ブロック", "type": "D", "cells": [
            _c("gray", "pc", "元", {"n": 3, "hl": 1, "w": 280, "h": 400, "vertical": True}),
            _c("green", "room", "分岐 1"), _c("red", "ban", "分岐 2")]},
        {"title": "E 1スライド1ブロック（大きな図）", "type": "E", "cells": [
            _c("", "shield", "全体像", {"n": 4, "hl": 1, "w": 760, "h": 330}, "要点を\n2〜3行")]},
        {"title": "F 2×2（Z に読む）", "type": "F", "cells": [
            _c("red", "ban", "左上"), _c("green", "check", "右上"), _c("red", "ban", "左下"), _c("green", "check", "右下")]},
        {"title": "G 上は全幅・下は左右（全体→内訳）", "type": "G", "cells": [
            _c("", "shield", "全体", {"n": 5, "hl": 2, "w": 570, "h": 92}, "全体の流れ\n1〜2行"),
            _c("gray", "pc", "内訳 1", {"w": 280, "h": 90}), _c("green", "room", "内訳 2", {"w": 280, "h": 90})]},
        # H: 行ラベル x 列。行・列は文言の数で決まる。
        {"title": "H 行ラベル × 列（3行 × 2列）", "type": "H", "cols": ["見出し A", "見出し B"], "rows": [
            {"label": "行ラベル 1", "cells": ["本文は 1〜2 行で言い切る", "本文は 1〜2 行で言い切る"]},
            {"label": "行ラベル 2", "cells": [["項目を 3 つまで", "短い名詞で", "揃える"], "本文は 1〜2 行で言い切る"]},
            {"label": "行ラベル 3", "cells": ["本文は 1〜2 行で言い切る", "本文は 1〜2 行で言い切る"]}]},
        {"title": "H 行ラベル × 列（5行 × 1列）", "type": "H", "rows": [
            {"label": f"行ラベル {i}", "cells": ["帯の本文。行を増やすと、高さが等分に縮む"]} for i in range(1, 6)]},
        {"title": "H 行ラベル × 列（4行 × 3列）", "type": "H", "cols": ["列 1", "列 2", "列 3"], "rows": [
            {"label": f"行 {i}", "cells": ["短い文言", "短い文言", "短い文言"]} for i in range(1, 5)]},
        # I: 工程 x 行（シェブロンの列見出し）
        {"title": "I 工程 × 行（4工程 × 2行）", "type": "I",
         "cols": ["工程 1", "工程 2", "工程 3", "工程 4"], "rows": [
             {"label": "内容", "cells": [["入力 1", "入力 2"], "本文", "本文", "本文"]},
             {"label": "ポイント", "cells": ["本文", "本文", "本文", ["最後の工程", "を強調する"]]}], "emphasize": -1},
        {"title": "I 工程 × 行（3工程 × 3行）", "type": "I",
         "cols": ["入力", "処理", "出力"], "rows": [
             {"label": "目的", "cells": ["本文", "本文", "本文"]},
             {"label": "内容", "cells": ["本文", "本文", "本文"]},
             {"label": "成果", "cells": ["本文", "本文", "本文"]}]},
        {"title": "I 工程の流れだけ（5工程、ラベルなし）", "type": "I",
         "cols": [f"工程 {i}" for i in range(1, 6)], "height": "10em", "rows": [
             {"cells": ["説明", "説明", "説明", "説明", "説明"]}]},
        # J: 表
        {"title": "J 表（5行 × 3列 + 番号）", "type": "J", "head": ["項目", "完了条件", "出力"], "index": True,
         "rows": [["項目 " + str(i), "条件を 1 行で", "成果物の名前"] for i in range(1, 6)]},
        {"title": "J 表（4行 × 4列、数値は右寄せ）", "type": "J", "head": ["指標", "今期", "前期", "増減"],
         "align": ["l", "r", "r", "r"], "rows": [["指標 A", "4,000", "4,000", "▲0.2%"], ["指標 B", "3,200", "3,100", "+3.2%"],
                                              ["指標 C", "1,800", "1,950", "▲7.7%"], ["指標 D", "920", "900", "+2.2%"]]},
    ],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="JSON の仕様（省略時は組み込みの見本）")
    ap.add_argument("-o", "--out", help="出力先（省略時は標準出力）")
    a = ap.parse_args()
    spec = SAMPLE
    if a.spec:
        with open(a.spec, encoding="utf-8") as f:
            spec = json.load(f)
    text = build(spec)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
