"""Lucide のアイコン（SVG）から、図解レイアウト用の symbol 定義を作る。ソフトウェア開発系のストック。

使い方: python -I build_lucide_icons.py <lucide の icons ディレクトリ（SVG）>   # 素材から作り直す
出力:   revealjs-diagram-icons-lucide.html（同じディレクトリ。手で直さず作り直す）
        revealjs-diagram-icons-lucide-preview.html（ブラウザで開いて見る一覧と id）
        lucide-LICENSE.txt は素材の LICENSE をそのまま置く（再配布の条件: 著作権表示と許諾文を同梱する）。

素材: Lucide https://lucide.dev （ISC License。Feather 由来の一部は MIT。lucide-LICENSE.txt）
      版: 1.70.0（2026-11-06 に取得。GitHub の lucide-icons/lucide、タグ 1.70.0 の icons/*.svg）
加工: svg の外枠を除き、線の属性（fill=none, stroke=currentColor, 太さ 2, 丸い端）を <g> に移した（形は変えていない）。
      symbol の id は i-lc-<素材名>（i-myself-*、i-dads-* と衝突しない。形式は i-<素材>-<名前>）。線の太さは CSS 側で変えられる（.cell .tab svg など）。
取得: 素材は新しい空のディレクトリへ置く（信頼できない入力として扱う）。名前が無い素材は取得時に 404 になる
      （1.70.0 では github・triangle-alert・trash-2・history は無い。別名: trash・undo-2・octagon-x）。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
G_OPEN = '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'

# プレビューの区分（意味は資料全体で固定する。区分に無い素材は「その他」に出る）
GROUPS = {
    "フォルダ・ファイル": "folder folder-open folder-closed folder-git folder-code folder-tree folder-lock folder-cog file file-text file-code file-braces file-cog file-terminal file-lock file-key file-image file-spreadsheet file-archive file-diff file-check file-x",
    "コード・言語": "terminal square-terminal code code-xml braces brackets binary regex variable bug",
    "Git": "git-branch git-commit-horizontal git-merge git-pull-request git-compare tag",
    "インフラ・実行環境": "database server cloud container package boxes blocks cpu hard-drive network globe wifi monitor laptop smartphone",
    "運用・実行": "settings wrench hammer play rocket workflow webhook plug activity gauge flask-conical",
    "セキュリティ・利用者": "key-round lock shield-check user users bot brain sparkles wand-sparkles",
    "文書・操作": "scroll-text book-open hash link search eye eye-off pencil save download upload trash refresh-cw undo-2 clock bell image list-checks notebook-pen clipboard-list layers puzzle",
    "状態": "circle-check circle-x octagon-x info",
}


def symbol(name, svg):
    body = re.sub(r"<svg[^>]*>|</svg>", "", svg, flags=re.S)
    body = re.sub(r"\s+", " ", body).strip()
    body = re.sub(r"\s*/>", "/>", body)
    return f'<symbol id="i-lc-{name}" viewBox="0 0 24 24">{G_OPEN}{body}</g></symbol>'


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    files = sorted(src.glob("*.svg"))
    if not files:
        raise SystemExit(f"SVG が見つかりません: {src}")
    syms = []
    for f in files:
        svg = f.read_text(encoding="utf-8")
        if re.search(r"<script|on\w+=|<foreignObject|href=", svg, re.I):  # 素材は信頼しない。図形以外が混じっていたら止める
            raise SystemExit(f"図形以外の要素・属性があります: {f.name}")
        syms.append(symbol(f.stem, svg))
    head = ("<!-- Lucide（ISC License。https://lucide.dev）のアイコンを元に、線の属性を g に移して symbol 化。"
            "版 1.70.0。ライセンスは lucide-LICENSE.txt -->\n")
    defs = head + '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(syms) + "</defs></svg>\n"
    (HERE / "revealjs-diagram-icons-lucide.html").write_text(defs, encoding="utf-8", newline="\n")
    lic = src.parent / "LICENSE.txt"
    if lic.exists():
        (HERE / "lucide-LICENSE.txt").write_text(lic.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    have = {f.stem for f in files}
    seen, sections = set(), []
    for title, names in GROUPS.items():
        ns = [n for n in names.split() if n in have]
        seen.update(ns)
        sections.append((title, ns))
    sections.append(("その他", sorted(have - seen)))
    cells = lambda ns: "".join(
        f'<div class="c"><svg viewBox="0 0 24 24" width="40" height="40"><use href="#i-lc-{n}"/></svg><br>lc-{n}</div>' for n in ns)
    page = ('<!doctype html><meta charset="utf-8"><title>Lucide アイコン一覧</title>'
            "<style>body{font-family:sans-serif;margin:24px;color:#1a1a1a}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,130px);gap:10px}"
            ".c{text-align:center;font-size:11px;border:1px solid #ddd;padding:8px 2px;border-radius:6px}"
            "svg{color:#0017c1}</style>" + defs
            + f"<h1>Lucide アイコン（{len(files)}）</h1><p>使い方: 札の icon に <code>lc-フォルダ名</code> のように書く。</p>"
            + "".join(f"<h2>{t}（{len(ns)}）</h2><div class=\"g\">{cells(ns)}</div>" for t, ns in sections if ns))
    (HERE / "revealjs-diagram-icons-lucide-preview.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"{len(files)} 種を出力しました")


if __name__ == "__main__":
    main()
