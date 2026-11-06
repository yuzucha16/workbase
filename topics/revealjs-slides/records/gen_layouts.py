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
  C 目次（番号 + 章名 + ひとこと + 小項目。current で表示中の章を強調）
  H 行ラベル x 列（行・列は文言の数で決まる）
  I 工程 x 行（シェブロンの列見出し。行ラベルは任意）
  J 表（背景なし・罫線だけの表。emphasize で強調列、rowhead で先頭列を太字）
  T 図解なし（見出し + 段落 + 箇条書き。入れ子はリストの中のリスト。まとめ・前置き・補足用）。
    "side" で右側にコード（{"code","lang"}）か画像（{"img","alt"}）を置ける。
  split 2 つの型（"parts" を左右に置く組み合わせ。例: 表 + 箇条書き(T)、図 + コード）。
  レイアウト番号: 各スライドの右下に型の記号（例 H+notes、split(J+T)）を出す。台帳は LAYOUTS。
    無い型が欲しいときは近い型で作り、slide に "want": "欲しい形" を書く（番号に ※要新設 が付き、stderr に一覧が出る）。
  全型（A〜J）が "lead"（上）と "notes"（下）の箇条書きを持てる。
  箱の型 A〜G は "height"（例 "500px"）で下の空きを埋める。
"""
import argparse
import html
import json
import sys

BLUE, GRAY, TEXT = "#0017c1", "#767676", "#1a1a1a"

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


# 見出しで始まる div を Pandoc が <section> にすると、reveal の縦スライドになって後続が見えなくなる。空の印を先頭に置いて防ぐ
NOSEC = raw("<span hidden></span>")


# ---- レイアウトの台帳（番号・名前・使いどころの正。ここに足すと、番号表示と一覧に出る） ----
# 番号 = 型の記号（A〜J、T）。組み合わせは「split(J+T)」のように部品の番号をつなぐ。付属は +lead +notes +side。
LAYOUTS = {
    "A": "左右二分割（比較）", "B": "上は左右・下は全幅（共通・結論を下に）", "C": "目次（番号 + 章名 + ひとこと）",
    "D": "左は一本・右は 2 ブロック（1 つの元から分岐）", "E": "1 ブロックの大きな図", "F": "2×2（2 軸の比較）",
    "G": "上は全幅・下は左右（全体→内訳）", "H": "行ラベル × 列", "I": "工程（シェブロン）× 行",
    "J": "表（罫線だけ）", "T": "図解なし（見出し + 段落 + 箇条書き）", "split": "2 つの型を左右に組み合わせ",
}
WANTS = []  # 作成中に「無いレイアウト」として申告されたもの（spec の "want"）。build の最後に報告する


def layout_id(s):
    """スライドに表示するレイアウト番号。例: H+notes / split(J+T)+lead / T+side"""
    t = s["type"]
    base = f"split({'+'.join(p['type'] for p in s.get('parts', []))})" if t == "split" else t
    extra = "".join(f"+{k}" for k in ("lead", "notes") if s.get(k)) + ("+side" if s.get("side") else "")
    label = base + extra
    if s.get("want"):  # 近い型で代用したが、本当は別のレイアウトが欲しい（逐次作る対象）
        WANTS.append((s.get("title", ""), label, s["want"]))
        label += f" ※要新設: {s['want']}"
    return label


def lid_div(s, show):
    return raw(f'<div class="lid">{esc(layout_id(s))}</div>') if show else ""


# 見出しで始まる div を Pandoc が <section> にすると、reveal の縦スライドになって後続が見えなくなる。空の印を先頭に置いて防ぐ
NOSEC = raw("<span hidden></span>")


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
    fill, stroke, sw = ("#e8f1fe", BLUE, 3) if on else ("#f2f2f2", GRAY, 2)
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
    attr = f' style="--lh:{s["height"]}"' if s.get("height") else ""
    out = f"::: {{.lay .lay-{t.lower()}{attr}}}\n"
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
    style = f"grid-template-columns:{' '.join(tracks)};grid-template-rows:{'auto ' if cols else ''}repeat({nrow},{'1fr' if s.get('height') else 'auto'});"
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
    emph = s.get("emphasize")  # 強調する列番号（0 始まり。負の数は後ろから）
    if emph is not None and emph < 0:
        emph += len(head)
    rowhead = s.get("rowhead", False)  # 先頭列を太字の行ラベルにする
    out = ['<table class="tb"' + (f' style="--h:{s["height"]}"' if s.get("height") else "") + ">", "<thead><tr>"]
    if index:
        out.append('<th class="no">#</th>')
    out += [f'<th class="{a}{" em" if i == emph else ""}">{lines(h)}</th>' for i, (h, a) in enumerate(zip(head, align))]
    out.append("</tr></thead><tbody>")
    for n, row in enumerate(s["rows"], 1):
        out.append("<tr>" + (f'<td class="no">{n}</td>' if index else "")
                   + "".join(f'<td class="{a}{" em" if i == emph else ""}{" rl" if rowhead and i == 0 else ""}">{lines(v)}</td>' for i, (v, a) in enumerate(zip(list(row) + [""] * (len(head) - len(row)), align)))
                   + "</tr>")
    out.append("</tbody></table>")
    return raw("".join(out))


def text_slide(s):
    """T: 見出し + 箇条書き（入れ子はリストの中のリスト）。インデントの確認用。"""
    def bullets(items, depth=0):
        if depth > 1:
            raise ValueError("箇条書きは 2 段（入れ子 1 回）まで")
        out = ""
        for x in items:
            out += ("  " * depth + "- " + x + "\n") if isinstance(x, str) else bullets(x, depth + 1)
        return out
    main = "".join(f"### {b['h']}\n\n" + "".join(p + "\n\n" for p in b.get("p", [])) + f"{bullets(b.get('items', []))}\n" for b in s["blocks"])
    side = s.get("side")
    if not side:
        return main
    # 右側: {"code": "...", "lang": "bash"} か {"img": "path", "alt": "..."}。左 = 文章、右 = コード・画像
    if "code" in side:
        right = raw(f'<pre class="plain"><code>{esc(side["code"].rstrip())}</code></pre>')
    elif "img" in side:
        right = f"![{side.get('alt', '')}]({side['img']})\n"
    else:
        raise SystemExit("T の side は code か img を持つ")
    return f"::: {{.tside}}\n::: {{.tmain}}\n{NOSEC}{main}:::\n::: {{.tright}}\n{right}:::\n:::\n"


def toc_slide(s):
    """C: 目次。items は文字列か {"t": 章名, "d": ひとこと(任意), "sub": [小項目](任意)}。
    current（1 始まり）を指すと、その章だけ薄青の地・太字（章の区切りで再掲する目次用）。
    DADS の目次は web ページ内ナビ（点線の箱 + 入れ子の箇条書き）なので、スライドでは罫線だけの番号付き一覧に置き換えた。"""
    cur = s.get("current")
    out = ['<ol class="toc">']
    for n, it in enumerate(s["items"], 1):
        it = {"t": it} if isinstance(it, str) else it
        sub = "".join(f"<li>{esc(x)}</li>" for x in it.get("sub", []))
        out.append(f'<li{" class=cur" if n == cur else ""}><span class="n">{n}</span><span class="t">{esc(it["t"])}</span>'
                   + (f'<span class="d">{esc(it["d"])}</span>' if it.get("d") else "")
                   + (f'<ul class="sub">{sub}</ul>' if sub else "") + "</li>")
    out.append("</ol>")
    return raw("".join(out))


def summary(v, cls):
    """lead（図表の上のひとこと）/ notes（下のまとめ・総評）。文字列は 1 段落、リストは箇条書き。"""
    if not v:
        return ""
    return raw(f'<div class="sum {cls}">{lines(v)}</div>')


def body(s):
    """型ごとの本体（タイトル・lead・notes を除く）。"""
    t = s["type"]
    if t == "T":
        return text_slide(s)
    return {"C": lambda: toc_slide(s), "H": lambda: grid(s, False), "I": lambda: grid(s, True), "J": lambda: table_slide(s)}.get(t, lambda: box_slide(s))()


def slide(s, show_id=True):
    """単独の型、または "split"（"parts" の 2 つを左右に置く組み合わせ。"cols" 例 "1fr 1fr"）。lead/notes は T 以外の全型で使える。"""
    if s["type"] == "split":
        parts = s["parts"]
        if len(parts) != 2:
            raise SystemExit("split の parts は 2 つ")
        inner = "".join(f"::: {{.sp}}\n{NOSEC}{body(p)}\n:::\n" for p in parts)
        inner = f'::: {{.split style="--cols:{s.get("cols", "1fr 1fr")}"}}\n{inner}:::\n'
        return f"## {s['title']}\n\n{summary(s.get('lead'), 'lead')}{inner}\n{summary(s.get('notes'), '')}{lid_div(s, show_id)}\n"
    if s["type"] == "T":
        return f"## {s['title']}\n\n{body(s)}{lid_div(s, show_id)}"
    return f"## {s['title']}\n\n{summary(s.get('lead'), 'lead')}{body(s)}\n{summary(s.get('notes'), '')}{lid_div(s, show_id)}\n"

def build(spec, show_id=None):
    if show_id is None:
        show_id = spec.get("show_id", True)  # 作成中は番号を出す（最終判断はユーザー）。完成版は --no-id か "show_id": false
    return HEADER.format(title=spec.get("title", "レイアウト見本")) + "\n" + "\n".join(slide(s, show_id) for s in spec["slides"])


# ---- 組み込みの見本（ダミーの文言。行・列の数を変えた例を並べる） ----
def _c(tone, icon, tab, fig=None, text="文字は短く\n2〜3行"):
    return {"tone": tone, "icon": icon, "tab": tab, "fig": fig if fig is not None else {}, "text": text}


SAMPLE = {
    "title": "レイアウト見本",
    "slides": [
        {"title": "T 見出しと箇条書き（インデント確認）", "type": "T", "blocks": [
            {"h": "見出し 1", "items": ["箇条書きは 1 行で言い切る", ["入れ子は 1 段ずつ深くする"]]},
            {"h": "見出し 2", "items": ["項目 A", "項目 B"]}]},
        {"title": "目次", "type": "C", "items": [
            {"t": "背景と目的", "d": "なぜ今やるのか"},
            {"t": "現状の整理", "d": "数字で見る", "sub": ["指標 A", "指標 B"]},
            {"t": "進め方", "d": "3 つの工程"},
            "まとめと次の一手"]},
        {"title": "目次（2 章を表示中）", "type": "C", "current": 2, "items": [
            {"t": "背景と目的"}, {"t": "現状の整理", "sub": ["指標 A", "指標 B"]}, {"t": "進め方"}, {"t": "まとめと次の一手"}]},
        {"title": "T 右にコード（サンプル）", "type": "T", "blocks": [{"h": "手順", "items": ["設定を置く", "起動する"]}], "side": {"lang": "bash", "code": "room init Area --resume\nfc-list | grep 'Noto Sans JP,'"}},
        {"title": "組み合わせ 表 + 箇条書き（サンプル）", "type": "split", "cols": "1.4fr 1fr",
         "lead": "表と箇条書きを左右に並べる例",
         "parts": [{"type": "J", "head": ["項目", "現在", "目標"], "rows": [["指標 A", "4,000", "4,400"], ["指標 B", "3,200", "3,500"]], "align": ["l", "r", "r"]},
                   {"type": "T", "blocks": [{"h": "ポイント", "items": ["A は目標まで 10%", ["B は季節要因を除く"], "確認は月 1 回"]}]}],
         "notes": ["まとめは下に箇条書きで置ける"]},
        {"title": "T 文章・文字列・箇条書き（サンプル）", "type": "T", "blocks": [
            {"h": "はじめに", "p": ["この見本は、段落と箇条書きが混ざったときの並びを確かめるためのダミーです。", "文の長さは、1 行に収まる程度から 2 行に折り返す程度まで混ぜています。"]},
            {"h": "進め方", "items": ["最初に目的を 1 文で決める", ["背景は短く、数字があれば添える"], "次に作業を 3 つ以内に分ける", "最後に確認する項目を並べる"]},
            {"h": "メモ", "p": ["文字列の例: ABC-123 / 2026-11-06 / 12,345 円 / v1.2.3"]}]},        {"title": "A 左右二分割（比較）", "type": "A", "cells": [_c("dark", "ban", "左"), _c("blue", "check", "右")]},
        {"title": "B 上は左右・下は全幅", "type": "B", "cells": [
            _c("gray", "pc", "左"), _c("blue", "room", "右"),
            _c("", "shield", "共通", {"n": 5, "hl": 2, "w": 570, "h": 92}, "共通の前提\n1〜2行")]},
        {"title": "D 左は一本・右は2ブロック", "type": "D", "cells": [
            _c("gray", "pc", "元", {"n": 3, "hl": 1, "w": 280, "h": 400, "vertical": True}),
            _c("blue", "room", "分岐 1"), _c("dark", "ban", "分岐 2")]},
        {"title": "E 1スライド1ブロック（大きな図）", "type": "E", "cells": [
            _c("", "shield", "全体像", {"n": 4, "hl": 1, "w": 760, "h": 330}, "要点を\n2〜3行")]},
        {"title": "F 2×2（Z に読む）", "type": "F", "cells": [
            _c("dark", "ban", "左上"), _c("blue", "check", "右上"), _c("dark", "ban", "左下"), _c("blue", "check", "右下")]},
        {"title": "G 上は全幅・下は左右（全体→内訳）", "type": "G", "cells": [
            _c("", "shield", "全体", {"n": 5, "hl": 2, "w": 570, "h": 92}, "全体の流れ\n1〜2行"),
            _c("gray", "pc", "内訳 1", {"w": 280, "h": 90}), _c("blue", "room", "内訳 2", {"w": 280, "h": 90})]},
        # H: 行ラベル x 列。行・列は文言の数で決まる。
        {"title": "H 行ラベル × 列（3行 × 2列）", "type": "H",
         "notes": ["行の高さは内容なり。表の下に、まとめ・総評を箇条書きで置く", "上に置くなら lead（ひとこと）。どちらも省略できる"], "cols": ["見出し A", "見出し B"], "rows": [
            {"label": "行ラベル 1", "cells": ["本文は 1〜2 行で言い切る", "本文は 1〜2 行で言い切る"]},
            {"label": "行ラベル 2", "cells": [["項目を 3 つまで", "短い名詞で", "揃える"], "本文は 1〜2 行で言い切る"]},
            {"label": "行ラベル 3", "cells": ["本文は 1〜2 行で言い切る", "本文は 1〜2 行で言い切る"]}]},
        {"title": "H 行ラベル × 列（3行 × 1列）", "type": "H", "rows": [
            {"label": f"行ラベル {i}", "cells": ["帯の本文。行を増やすと、高さが等分に縮む"]} for i in range(1, 4)]},
        {"title": "H 行ラベル × 列（3行 × 3列）", "type": "H",
         "lead": ["上に置くときは、結論や前提を 1〜2 点の箇条書きで", "どちらに置くかは、AI が内容で選ぶ"], "cols": ["列 1", "列 2", "列 3"], "rows": [
            {"label": f"行 {i}", "cells": ["短い文言", "短い文言", "短い文言"]} for i in range(1, 4)]},
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
         "cols": [f"工程 {i}" for i in range(1, 6)], "rows": [
             {"cells": ["説明", "説明", "説明", "説明", "説明"]}]},
        # J: 表
        {"title": "J 表（3行 × 3列 + 番号）", "type": "J", "head": ["項目", "完了条件", "出力"], "rowhead": True, "emphasize": 2,
         "rows": [["項目 " + str(i), "条件を 1 行で", "成果物の名前"] for i in range(1, 4)]},
        {"title": "J 表（4行 × 4列、数値は右寄せ）", "type": "J", "head": ["指標", "今期", "前期", "増減"],
         "align": ["l", "r", "r", "r"], "rows": [["指標 A", "4,000", "4,000", "▲0.2%"], ["指標 B", "3,200", "3,100", "+3.2%"],
                                              ["指標 C", "1,800", "1,950", "▲7.7%"], ["指標 D", "920", "900", "+2.2%"]]},
    ],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="JSON の仕様（省略時は組み込みの見本）")
    ap.add_argument("-o", "--out", help="出力先（省略時は標準出力）")
    ap.add_argument("--no-id", action="store_true", help="レイアウト番号を表示しない（完成版）")
    a = ap.parse_args()
    spec = SAMPLE
    if a.spec:
        with open(a.spec, encoding="utf-8") as f:
            spec = json.load(f)
    text = build(spec, False if a.no_id else None)
    for title, label, want in WANTS:
        print(f"[要新設] {title} ({label}): {want}", file=sys.stderr)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
