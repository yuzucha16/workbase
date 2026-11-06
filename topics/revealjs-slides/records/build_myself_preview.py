"""自作アイコン（revealjs-diagram-icons-myself.html）のプレビューを作る。

使い方: python -I build_myself_preview.py
出力:   revealjs-diagram-icons-myself-preview.html（ブラウザで開いて見る一覧と id。手で直さず作り直す）
自作の定義（myself.html）は手で書く。増減したらこのスクリプトを再実行する。
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
mine = (HERE / "revealjs-diagram-icons-myself.html").read_text(encoding="utf-8")
ids = re.findall(r'<symbol id="i-([^"]+)"', mine)
cells = "".join(
    f'<div class="c"><svg viewBox="0 0 24 24" width="48" height="48"><use href="#i-{i}"/></svg><br>{i}</div>'
    for i in ids)
page = ('<!doctype html><meta charset="utf-8"><title>自作アイコン一覧</title>'
        "<style>body{font-family:sans-serif;margin:24px;color:#1a1a1a}"
        ".g{display:grid;grid-template-columns:repeat(auto-fill,120px);gap:12px}"
        ".c{text-align:center;font-size:12px;border:1px solid #ddd;padding:10px 4px;border-radius:6px}"
        "svg{color:#0017c1}</style>" + mine
        + f'<h1>自作アイコン（{len(ids)}）</h1><p>使い方: 札の icon に <code>myself-フォルダ</code> のように書く（symbol の id は <code>i-myself-…</code>）。</p>'
        + f'<div class="g">{cells}</div>')
(HERE / "revealjs-diagram-icons-myself-preview.html").write_text(page, encoding="utf-8", newline="\n")
print(len(ids), "icons")
