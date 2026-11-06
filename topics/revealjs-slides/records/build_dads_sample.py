"""DADS 案の見本 HTML を作る（何度でも作り直せる）。

使い方（Windows。Quarto が PATH にあること）:
    python -I build_dads_sample.py [--out OUT_DIR] [--no-spacing] [--qmd QMD]

やること:
  1. records/ の revealjs-diagram-theme.scss（v1）を読み、下の PALETTE と SPACING で置換して
     OUT_DIR に revealjs-diagram-theme.scss として書く（v1 は変えない）。
  2. qmd（既定: revealjs-diagram-layouts.qmd）とアイコン定義を OUT_DIR にコピーする。
  3. quarto render で自己完結の HTML（OUT_DIR/dads.html）を作る。比較用に v1 も v1.html として作る。

微修正のしかた: PALETTE の値を直して再実行する。採否の根拠は
2026-11-06-dads-selection-table.md。OUT_DIR の既定は records/dads-sample/（コミットしない。.gitignore 不要の一時扱い）。
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# v1 の値 -> DADS の値（トークン名はコメント）。提案の色。採否が決まったら直す。
PALETTE = {
    "#1f5fd1": "#0017c1",  # 強調色 -> blue-900
    "#174aa3": "#00118f",  # 強調の濃い側 -> blue-1000
    "#eaf1fd": "#e8f1fe",  # 強調の薄い地 -> blue-50
    "#1f2933": "#1a1a1a",  # 本文の文字 -> solid-gray-900
    "#52606d": "#4d4d4d",  # 副次の帯 -> solid-gray-700
    "#f3f4f6": "#f2f2f2",  # 面の地 -> solid-gray-50
    "#f5f7fa": "#f2f2f2",  # 面の地（灰の箱）-> solid-gray-50
    "#d9dee3": "#cccccc",  # 番号の列 -> solid-gray-200
    "#9aa5b1": "#767676",  # 灰の枠 -> solid-gray-536（白に 4.54:1）
    "#374151": "#333333",  # 濃灰の枠 -> solid-gray-800
}
# 余白: em 由来を px の 8 の倍数に（--no-spacing で無効）
SPACING = [("--gap: 0.5em; --pad: 0.7em 0.9em;", "--gap: 8px; --pad: 16px 24px;")]


def make_scss(src: str, spacing: bool) -> str:
    for old, new in PALETTE.items():
        src = re.sub(re.escape(old), new, src, flags=re.I)
    if spacing:
        for old, new in SPACING:
            if old not in src:
                continue  # 土台に反映済み
            src = src.replace(old, new)
    return src


def render(d: Path, qmd: str, out_name: str) -> None:
    subprocess.run(["quarto", "render", qmd, "--output", out_name], cwd=d, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE / "dads-sample"))
    ap.add_argument("--qmd", default="revealjs-diagram-layouts.qmd")
    ap.add_argument("--no-spacing", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    v1, dads = out / "v1", out / "dads"
    scss0 = (HERE / "revealjs-diagram-theme.scss").read_text(encoding="utf-8")
    for d, scss in ((v1, scss0), (dads, make_scss(scss0, not a.no_spacing))):
        d.mkdir(parents=True, exist_ok=True)
        (d / "revealjs-diagram-theme.scss").write_text(scss, encoding="utf-8", newline="\n")
        shutil.copy(HERE / a.qmd, d / a.qmd)
        shutil.copy(HERE / "revealjs-diagram-icons.html", d / "revealjs-diagram-icons.html")
    render(v1, a.qmd, "v1.html")
    render(dads, a.qmd, "dads.html")
    print("できた:", v1 / "v1.html", dads / "dads.html")


if __name__ == "__main__":
    main()
