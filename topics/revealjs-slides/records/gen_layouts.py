"""revealjs 図解レイアウトの生成スクリプト。

型と文言（辞書または JSON）から、Quarto の qmd を出す。手書きの SVG を避ける。

使い方:
  python -I gen_layouts.py                      # 組み込みの見本から qmd を出す（標準出力）
  python -I gen_layouts.py -o out.qmd           # ファイルへ
  python -I gen_layouts.py --spec spec.json -o out.qmd

出力の qmd は、同じディレクトリの revealjs-diagram-theme.scss と
revealjs-diagram-icons-myself.html と revealjs-diagram-icons-dads.html（デジタル庁の素材。build_dads_icons.py で作る）を読む（render は両ファイルを同じ場所に置いて行う）。

型:
  箱の型  A 左右 / B 上左右+下全幅 / D 左一本+右2 / E 1ブロック / F 2x2 / G 上全幅+下左右
  （A〜G は PRESETS の preset 名。並びは grid-template-areas で決まり、新しい並びは PRESETS に 1 行足すだけ）
  C 目次（番号 + 章名 + ひとこと + 小項目。current で表示中の章を強調）
  H 行ラベル x 列（行・列は文言の数で決まる）
  I 工程 x 行（シェブロンの列見出し。行ラベルは任意）
  J 表（背景なし・罫線だけの表。emphasize で強調列、rowhead で先頭列を太字）
  T 図解なし（見出し + 段落 + 箇条書き。入れ子はリストの中のリスト。まとめ・前置き・補足用）。
    "side" で右側にコード（{"code","lang"}）か画像（{"img","alt"}）を置ける。
  K ディレクトリ構造（"tree" に 2 桁インデントの文字列。書き方は tree_rows の docstring。アイコンは Lucide。lc-<名前> で札や tree の [..] にも使える）
  DADS コンポーネント S ステップナビゲーション / L 説明リスト / N 注釈ブロック
    （spec の形は steps_slide / dlist_slide / notice_slide の docstring。split の部品にも使える）
  split 2 つの型（"parts" を左右に置く組み合わせ。例: 表 + 箇条書き(T)、図 + コード）。
  レイアウト番号: 各スライドの右下に型の記号（例 H+notes、split(J+T)）を出す。台帳は LAYOUTS。
    無い型が欲しいときは近い型で作り、slide に "want": "欲しい形" を書く（番号に ※要新設 が付き、stderr に一覧が出る）。
  全型（A〜J）が "lead"（上）と "notes"（下）の箇条書きを持てる。
  箱の型 A〜G は "height"（例 "500px"）で下の空きを埋める。
"""
import argparse
import html
import json
import re
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
    include-before-body:
      - revealjs-diagram-icons-myself.html
      - revealjs-diagram-icons-dads.html
      - revealjs-diagram-icons-lucide.html
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
# 値 = (名前, 使いどころ)。AI は提案のとき「番号 + 使いどころ」を理由として言う。--list で一覧。
LAYOUTS = {
    "A": ("左右二分割（比較）", "2 つの案・前後・Before/After を対等に並べて比べるとき"),
    "B": ("上は左右・下は全幅（共通・結論を下に）", "2 つを比べたあと、共通点や結論を 1 本で下に示すとき"),
    "C": ("目次（番号 + 章名 + ひとこと）", "全体の流れを最初に見せる、または章の区切りで現在地を示すとき"),
    "D": ("左は一本・右は 2 ブロック（1 つの元から分岐）", "1 つの原因・入力から 2 つの結果・用途に分かれる説明"),
    "E": ("1 ブロックの大きな図", "構成図・フローなど 1 枚の図を大きく見せたいとき"),
    "F": ("2×2（2 軸の比較）", "2 つの軸で 4 象限に分類するとき（優先度、得意・不得意など）"),
    "G": ("上は全幅・下は左右（全体→内訳）", "全体像を 1 本で示し、その内訳を 2 つに分けるとき"),
    "H": ("行ラベル × 列", "項目ごとに複数の観点を並べる（行ラベルが主役の比較）"),
    "I": ("工程（シェブロン）× 行", "段階・手順・時間の流れが列で、行ごとに内容が違うとき"),
    "J": ("表（罫線だけ）", "数値・仕様など、格子で正確に読ませたい一覧"),
    "T": ("図解なし（見出し + 段落 + 箇条書き）", "図にしにくい説明、まとめ、コードや画像を横に添える話（side）"),
    "S": ("ステップナビゲーション（手順 + 現在位置）", "手順の全体と今どこかを見せるとき。横（既定）か縦（dir）。完了・現在・未を丸の形で区別"),
    "L": ("説明リスト（項目名 + 説明）", "用語と説明、名前と値の組（設定項目・仕様・申請内容）。比較は表（J）にする"),
    "N": ("注釈ブロック（補足・例）", "手続きに必要な補足、入力例、選択肢の違いの例。強調や飾りには使わない"),
    "K": ("ディレクトリ構造（ツリー + アイコン）", "フォルダ・ファイルの階層を見せるとき（プロジェクト構成、配置、マウント）。行ごとに補足・強調ができる"),
    "split": ("2 つの型を左右に組み合わせ", "表 + 箇条書き、図 + コードなど、性質の違う 2 つを同じ画面に置くとき"),
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


# ---- アイコン素材の出典（スライドごとに、使った素材の 1 行を下に出す。自作は出さない） ----
CREDITS = {
    "dads": "アイコン: 「イラストレーション・アイコン素材」（デジタル庁）を元に、色を変更して使用 https://www.digital.go.jp/policies/servicedesign/designsystem/Illustration_Icons",
    "lucide": "アイコン: Lucide（ISC License） https://lucide.dev",
}


def credit_div(text):
    """本文（生成済みの qmd 断片）が参照する symbol から、素材ごとの出典行を作る。DADS → Lucide の順。"""
    ids = set(re.findall(r'href="#i-([^"]+)"', text))
    kinds = {"lucide" if i.startswith("lc-") else "dads" for i in ids if i.startswith(("lc-", "dads-"))}
    lines_ = [CREDITS[k] for k in ("dads", "lucide") if k in kinds]
    if not lines_:
        return ""
    return raw('<div class="src">' + "<br>".join(esc(x) for x in lines_) + "</div>")


def lid_div(s, show):
    return raw(f'<div class="lid">{esc(layout_id(s))}</div>') if show else ""


# 見出しで始まる div を Pandoc が <section> にすると、reveal の縦スライドになって後続が見えなくなる。空の印を先頭に置いて防ぐ
NOSEC = raw("<span hidden></span>")


def no_ol(t):
    """DADS: ol を使わない。行頭の「1.」は Markdown が ol にするので止める（番号は「1」と文字で書く）。"""
    if re.match(r"\s*\d+[.)]\s", t):
        raise SystemExit(f"行頭の番号付き（{t[:20]!r}）は ol になる。番号は「1」と文字で書く（DADS 準拠）")


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
def cell(c, extra="", area=None):
    cls = " ".join(x for x in ["cell", c.get("tone"), extra] if x)
    style = f' style="grid-area:{area}"' if area else ""
    out = f"::: {{.{cls.replace(' ', ' .')}{style}}}\n"
    if c.get("tab"):
        icon = f'<svg viewBox="0 0 24 24"><use href="#i-{c["icon"]}"/></svg>' if c.get("icon") else ""
        out += raw(f'<div class="tab">{icon}{esc(c["tab"])}</div>') + "\n"
    fig = c.get("fig")
    if fig is not None:
        svg = fig if isinstance(fig, str) else flow_svg(**fig)
        # DADS: 画像は代替テキストを持つ。alt が無ければ tab の文言で代え、それも無ければ装飾（読み上げない）にする
        alt = c.get("alt") or c.get("tab")
        label = f'role="img" aria-label="{esc(alt)}"' if alt else 'aria-hidden="true"'
        svg = svg.replace("<svg ", f"<svg {label} ", 1)
        out +="::: {.fig}\n" + raw(svg) + ":::\n"
    if c.get("text"):
        out += "::: {.txt}\n" + "<br>".join(esc(t) for t in c["text"].split("\n")) + "\n:::\n"
    return out + ":::\n"


# 箱の並び（preset）。A〜G は preset 名。新しい並びは、ここに 1 行足すだけで作れる（CSS は触らない）。
#   areas: grid-template-areas の各行（cells の順に a, b, c… を割り当てる。"l" は B の矢印）
#   cols / rows: grid-template-columns / rows
#   wide: 幅広のセル（図を少し大きく）の番号 / link: 矢印を置く領域（areas の "l"）
PRESETS = {
    "A": {"areas": ["a b"], "cols": "1fr 1fr"},
    "B": {"areas": ["a l b", "c c c"], "cols": "1fr 4.2em 1fr", "wide": [2], "link": True},
    "D": {"areas": ["a b", "a c"], "cols": "1fr 1fr", "rows": "1fr 1fr"},
    "E": {"areas": ["a"], "cols": "1fr"},
    "F": {"areas": ["a b", "c d"], "cols": "1fr 1fr"},
    "G": {"areas": ["a a", "b c"], "cols": "1fr 1fr", "wide": [0]},
}


def preset_cells(p):
    """preset の areas に出てくるセル用の領域名（"l" を除く）の数。"""
    return len({ch for row in p["areas"] for ch in row.split()} - {"l"})


def box_slide(s):
    t = s["type"]
    cells = s["cells"]
    p = PRESETS[t]
    n = preset_cells(p)
    if len(cells) != n:
        raise SystemExit(f"型 {t} の cells は {n} 個（{len(cells)} 個ありました）")
    style = f"grid-template-columns:{p['cols']};" + (f"grid-template-rows:{p['rows']};" if p.get("rows") else "")
    style += "grid-template-areas:" + " ".join(f"'{r}'" for r in p["areas"])  # 属性が "…" で囲まれるので、中は単一引用符 + ";"
    if s.get("height"):
        style += f"--lh:{s['height']};"
    out = f'::: {{.lay .lay-{t.lower()} style="{style}"}}\n'
    for i, c in enumerate(cells):
        out += cell(c, "wide" if i in p.get("wide", []) else "", "abcdefgh"[i])
        if p.get("link") and i == 0:
            out += f"::: {{.link style=\"grid-area:l\"}}\n{esc(s.get('link', '▶'))}\n:::\n"
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
            if isinstance(x, str):
                no_ol(x)
                out += "  " * depth + "- " + x + "\n"
            else:
                out += bullets(x, depth + 1)
        return out
    for b in s["blocks"]:
        for p in b.get("p", []):
            no_ol(p)
    main = "".join(f"### {b['h']}\n\n" + "".join(p + "\n\n" for p in b.get("p", [])) + f"{bullets(b.get('items', []))}\n" for b in s["blocks"])
    side = s.get("side")
    if not side:
        return main
    # 右側: {"code": "...", "lang": "bash"} か {"img": "path", "alt": "..."}。左 = 文章、右 = コード・画像
    if "code" in side:
        right = raw(f'<pre class="plain"><code>{esc(side["code"].rstrip())}</code></pre>')
    elif "img" in side:
        if not side.get("alt"):
            raise SystemExit("T の side の画像には alt（代替テキスト）が要る（DADS 準拠）")
        img = f'<img src="{esc(side["img"])}" alt="{esc(side["alt"])}">'
        cap = f'<figcaption>{esc(side["caption"])}</figcaption>' if side.get("caption") else ""
        right = raw(f"<figure>{img}{cap}</figure>") + "\n"
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


CHECK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def steps_slide(s):
    """S: ステップナビゲーション（DADS）。steps は文字列か {"t","d"(任意)}。current（1 始まり）で現在の手順。
    完了=灰の丸に✓、現在=黒の二重丸、未=白い丸。"dir": "h"（横。既定）か "v"（縦）。"""
    items = s["steps"]
    cur = s.get("current", 1)
    vertical = s.get("dir", "h") == "v"
    if not 1 <= cur <= len(items):
        raise SystemExit(f"S の current は 1〜{len(items)}")
    out = [f'<ol class="stp{" v" if vertical else ""}">']
    for n, it in enumerate(items, 1):
        it = {"t": it} if isinstance(it, str) else it
        st, word = ("done", "完了") if n < cur else (("now", "現在") if n == cur else ("todo", "未"))
        mk = CHECK_SVG if st == "done" else ""
        cur_attr = ' aria-current="step"' if st == "now" else ""
        out.append(f'<li class="{st}"{cur_attr}><span class="mk">{mk}</span><span class="tx"><span class="t"><span class="vh">{word}：</span>{esc(it["t"])}</span>'
                   + (f'<span class="d">{lines(it["d"])}</span>' if it.get("d") else "") + "</span></li>")
    out.append("</ol>")
    return raw("".join(out))


def dlist_slide(s):
    """L: 説明リスト（DADS）。items は {"t": 項目名, "d": 説明（文字列かリスト）}。
    "bullet": true で項目名の頭に黒丸。"wide": true で項目名を左・説明を右の 2 列にする。"""
    cls = "dl" + (" bul" if s.get("bullet") else "") + (" wide" if s.get("wide") else "")
    out = [f'<dl class="{cls}">']
    for it in s["items"]:
        out.append(f'<dt>{esc(it["t"])}</dt><dd>{lines(it["d"])}</dd>')
    out.append("</dl>")
    return raw("".join(out))


NOTICE_STYLES = ("blue", "gray", "bar")  # DADS 注釈ブロックの 3 パターン: 青の角丸枠 / 灰の角丸枠 + 薄灰の地 + タイトル / 直角の灰枠で左だけ太い


def notice_slide(s):
    """N: 注釈ブロック（DADS）。blocks は {"style": blue|gray|bar, "title"(任意), "text": 文字列かリスト}。
    手続きに必要な補足・例に使う。本文の強調・飾りには使わない。折りたたみ（ディスクロージャー）は静的なスライドでは使わない。"""
    out = []
    for b in s["blocks"]:
        st = b.get("style", "blue")
        if st not in NOTICE_STYLES:
            raise SystemExit(f"N の style は {NOTICE_STYLES} のどれか")
        title = f'<div class="nt">{esc(b["title"])}</div>' if b.get("title") else ""
        out.append(f'<div class="nb {st}" role="note">{title}<div class="nx">{lines(b["text"])}</div></div>')
    return raw("".join(out))


# K: ディレクトリ構造。拡張子 → Lucide のアイコン（素材は revealjs-diagram-icons-lucide.html。意味は資料全体で固定）
TREE_ICONS = {
    "folder": "lc-folder", "folder_open": "lc-folder-open",
    ".ts": "lc-file-code", ".tsx": "lc-file-code", ".js": "lc-file-code", ".jsx": "lc-file-code", ".py": "lc-file-code",
    ".sh": "lc-file-terminal", ".ps1": "lc-file-terminal", ".html": "lc-file-code", ".css": "lc-file-code", ".scss": "lc-file-code", ".qmd": "lc-file-code",
    ".json": "lc-file-braces", ".md": "lc-file-text", ".txt": "lc-file-text",
    ".yml": "lc-file-cog", ".yaml": "lc-file-cog", ".toml": "lc-file-cog", ".ini": "lc-file-cog", ".conf": "lc-file-cog",
    ".png": "lc-file-image", ".jpg": "lc-file-image", ".svg": "lc-file-image",
    ".csv": "lc-file-spreadsheet", ".xlsx": "lc-file-spreadsheet", ".zip": "lc-file-archive",
    ".lock": "lc-file-lock", ".env": "lc-file-lock", ".key": "lc-file-key", ".pem": "lc-file-key",
}


def tree_rows(text):
    """行の書き方: インデント 2 桁で 1 段深く。名前が `/` で終わるとフォルダ。
    `  # 注` で右に補足、先頭の `*` でその行を強調（薄青の地）、`name  [icon]` で icon を指定（例 `[lc-database]`）。"""
    rows = []
    for raw_line in text.strip("\n").split("\n"):
        if not raw_line.strip():
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise SystemExit(f"K のインデントは 2 桁単位（{raw_line!r}）")
        t = raw_line.strip()
        hl = t.startswith("*")
        t = t.lstrip("*").strip()
        note = ""
        if "  #" in t:
            t, note = t.split("  #", 1)
            note = note.strip()
        icon = None
        m = re.search(r"\s+\[([a-z0-9-]+)\]$", t)
        if m:
            icon, t = m.group(1), t[:m.start()]
        rows.append({"d": indent // 2, "name": t.strip(), "note": note, "hl": hl, "icon": icon})
    for i, r in enumerate(rows):
        r["dir"] = r["name"].endswith("/") or (i + 1 < len(rows) and rows[i + 1]["d"] > r["d"])
    return rows


def _tree_icon(r):
    if r["icon"]:
        return r["icon"], "fo" if r["dir"] else "fi"
    if r["dir"]:
        return TREE_ICONS["folder"], "fo"
    name = r["name"].lower()
    ext = "." + name.rsplit(".", 1)[1] if "." in name else ""
    return TREE_ICONS.get(ext, "lc-file"), "fi"


def _tree_html(rows):
    """rows（d = 深さ）から入れ子の ul を作る。"""
    out, i = [], 0
    while i < len(rows):
        r = rows[i]
        j = i + 1
        while j < len(rows) and rows[j]["d"] > r["d"]:
            j += 1
        kids = rows[i + 1:j]
        icon, kind = _tree_icon(r)
        note = f'<span class="nt">{esc(r["note"])}</span>' if r["note"] else ""
        row = (f'<div class="rw {kind}{" hl" if r["hl"] else ""}"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{icon}"/></svg>'
               f'<span class="nm">{esc(r["name"])}</span>{note}</div>')
        sub = f'<ul class="tr">{_tree_html(kids)}</ul>' if kids else ""
        out.append(f"<li>{row}{sub}</li>")
        i = j
    return "".join(out)


def tree_slide(s):
    """K: ディレクトリ構造（ツリー）。"tree" は tree_rows の書き方の文字列。"tab"（箱の見出し）と "caption"（下の一言）は任意。
    アイコンは Lucide（フォルダは青、ファイルは灰）。入れ子の ul で表すので、読み上げでも階層が分かる。"""
    rows = tree_rows(s["tree"])
    base = rows[0]["d"] if rows else 0
    for r in rows:
        r["d"] -= base
    out = "::: {.cell .dark .tree-box}\n"
    if s.get("tab"):
        out += raw(f'<div class="tab"><svg viewBox="0 0 24 24"><use href="#i-lc-folder-tree"/></svg>{esc(s["tab"])}</div>') + "\n"
    out += raw(f'<ul class="tr root">{_tree_html(rows)}</ul>')
    if s.get("caption"):
        out += "::: {.cap}\n" + esc(s["caption"]) + "\n:::\n"
    return out + ":::\n"

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
    return {"C": lambda: toc_slide(s), "S": lambda: steps_slide(s), "L": lambda: dlist_slide(s), "N": lambda: notice_slide(s), "K": lambda: tree_slide(s), "H": lambda: grid(s, False), "I": lambda: grid(s, True), "J": lambda: table_slide(s)}.get(t, lambda: box_slide(s))()


def slide(s, show_id=True):
    """単独の型、または "split"（"parts" の 2 つを左右に置く組み合わせ。"cols" 例 "1fr 1fr"）。lead/notes は T 以外の全型で使える。"""
    out = _slide(s, show_id)
    if s.get("cls"):  # スライドにクラスを付ける（例 "tight" = 字間を詰める版）
        out = out.replace(f"## {s['title']}\n", f"## {s['title']} {{.{s['cls']}}}\n", 1)
    return out + credit_div(out) if s.get("credit", True) else out


def _slide(s, show_id):
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


K_SAMPLE = """project/
  src/
    components/
    App.tsx  # 画面の入口
    index.ts
  tests/
  *README.md  # まず読む
  package.json
  .env"""
RIGHT = {
    "T": {"type": "T", "blocks": [{"h": "構成のポイント", "items": ["src に画面の部品をまとめる", ["components は再利用する部品"], "tests は src と同じ構造にする", "README を最初に読む"]}]},
    "L": {"type": "L", "wide": True, "items": [{"t": "src/", "d": "画面と処理のコード。入口は App.tsx"}, {"t": "tests/", "d": "テスト。src と同じ構造にそろえる"}, {"t": "README.md", "d": "最初に読む説明書"}, {"t": ".env", "d": "環境ごとの設定（公開しない）"}]},
}

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
            {"h": "メモ", "p": ["文字列の例: ABC-123 / 2026-11-06 / 12,345 円 / v1.2.3"]}]},        {"title": "A 左右二分割（比較）", "type": "A", "cells": [_c("dark", "myself-ban", "左"), _c("blue", "myself-check", "右")]},
        {"title": "B 上は左右・下は全幅", "type": "B", "cells": [
            _c("gray", "myself-pc", "左"), _c("blue", "myself-room", "右"),
            _c("", "myself-shield", "共通", {"n": 5, "hl": 2, "w": 570, "h": 92}, "共通の前提\n1〜2行")]},
        {"title": "D 左は一本・右は2ブロック", "type": "D", "cells": [
            _c("gray", "myself-pc", "元", {"n": 3, "hl": 1, "w": 280, "h": 400, "vertical": True}),
            _c("blue", "myself-room", "分岐 1"), _c("dark", "myself-ban", "分岐 2")]},
        {"title": "E 1スライド1ブロック（大きな図）", "type": "E", "cells": [
            _c("", "myself-shield", "全体像", {"n": 4, "hl": 1, "w": 760, "h": 330}, "要点を\n2〜3行")]},
        {"title": "F 2×2（Z に読む）", "type": "F", "cells": [
            _c("dark", "myself-ban", "左上"), _c("blue", "myself-check", "右上"), _c("dark", "myself-ban", "左下"), _c("blue", "myself-check", "右下")]},
        {"title": "G 上は全幅・下は左右（全体→内訳）", "type": "G", "cells": [
            _c("", "myself-shield", "全体", {"n": 5, "hl": 2, "w": 570, "h": 92}, "全体の流れ\n1〜2行"),
            _c("gray", "myself-pc", "内訳 1", {"w": 280, "h": 90}), _c("blue", "myself-room", "内訳 2", {"w": 280, "h": 90})]},
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
        # DADS コンポーネント（S 手順 / L 説明リスト / N 注釈ブロック）
        {"title": "S ステップナビゲーション（横）", "type": "S", "current": 3,
         "steps": [{"t": "申請", "d": "書類を準備"}, {"t": "確認", "d": "内容を見直す"}, {"t": "審査", "d": "結果を待つ"}, {"t": "完了", "d": "通知を受け取る"}],
         "notes": ["完了は灰の丸に ✓、現在は黒の二重丸、未は白い丸"]},
        {"title": "S ステップナビゲーション（縦）", "type": "S", "dir": "v", "current": 2,
         "steps": [{"t": "準備", "d": "必要なものをそろえる"}, {"t": "実行", "d": "手順どおりに進める"}, {"t": "確認", "d": "結果を見る"}]},
        {"title": "L 説明リスト", "type": "L", "items": [
            {"t": "対象", "d": "社内の勉強会・LT"}, {"t": "形式", "d": "自己完結の HTML スライド"}, {"t": "期間", "d": ["準備 1 週間", "本番 30 分"]}]},
        {"title": "L 説明リスト（黒丸 + 2 列）", "type": "L", "bullet": True, "wide": True, "items": [
            {"t": "名前", "d": "値を 1 行で"}, {"t": "場所", "d": "会議室 A"}, {"t": "持ち物", "d": "PC と電源"}]},
        {"title": "N 注釈ブロック", "type": "N", "blocks": [
            {"style": "blue", "text": "必要な資料は申請の前にそろえておく"},
            {"style": "gray", "title": "入力例", "text": ["姓：山田", "名：太郎"]},
            {"style": "bar", "title": "補足", "text": "読まなくても手続きは進められる補足情報"}]},
        {"title": "アイコン出典の見本（デジタル庁 + Lucide）", "type": "A", "cells": [
            _c("dark", "dads-search", "デジタル庁の素材", {}, "dads-search（検索）\ndads-authentication（認証）"),
            _c("blue", "lc-database", "Lucide", {}, "lc-database\nlc-folder-tree")]},
        {"title": "K ディレクトリ構造", "type": "K", "tab": "ディレクトリ構造", "tree": """project/
  src/
    components/
    App.tsx  # 画面の入口
    index.ts
  tests/
  *README.md  # まず読む
  package.json
  .env""", "caption": "フォルダ・ファイルのアイコンと名前を組み合わせて作る"},
        *[{"title": f"K 横幅 {w} の列 + {r}（字間: {lab}）", "type": "split", "cols": cols, "cls": cls, "parts": [
            {"type": "K", "tab": "構成", "tree": K_SAMPLE},
            RIGHT[r]]} for w, cols, r in (("1/3", "1fr 2fr", "T"), ("1/4", "1fr 3fr", "L")) for lab, cls in (("標準 2%", ""), ("詰め 0%", "tight"))],
        {"title": "組み合わせ 手順 + 注釈", "type": "split", "cols": "1.6fr 1fr",
         "parts": [{"type": "S", "dir": "v", "current": 1, "steps": ["書く", "確かめる", "出す"]},
                   {"type": "N", "blocks": [{"style": "gray", "title": "ポイント", "text": "提出前に必ず見直す"}]}]},
    ],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="JSON の仕様（省略時は組み込みの見本）")
    ap.add_argument("-o", "--out", help="出力先（省略時は標準出力）")
    ap.add_argument("--no-id", action="store_true", help="レイアウト番号を表示しない（完成版）")
    ap.add_argument("--list", action="store_true", help="レイアウトの台帳（番号・名前・使いどころ）を出して終わる")
    a = ap.parse_args()
    if a.list:
        sys.stdout.reconfigure(encoding="utf-8")
        for k, (name, use) in LAYOUTS.items():
            print(f"{k}\t{name}\t{use}")
        return
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
