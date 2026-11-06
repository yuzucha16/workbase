"""room-structure.svg を revealjs のスライドに入れる試験。2 通りの入れ方を 1 本にまとめて render する。

使い方: python -I build_slide.py <作業ディレクトリ(空・一時)>
- 入れ方 1: E の fig にインライン SVG(alt は tab の文言。SVG 内の role / aria-label は外す)
- 入れ方 2: T の side に <img src="room-structure-half.svg">(alt 必須)
出力は作業ディレクトリに作る(コミットしない)。quarto が PATH に要る。
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
rec = here.parent
work = Path(sys.argv[1])
work.mkdir(parents=True, exist_ok=True)

svg_text = (here / "room-structure.svg").read_text(encoding="utf-8")
inline = re.sub(r'\s(role|aria-label)="[^"]*"', "", svg_text).replace("\n", "")

spec = {"title": "Excalidraw 試験: room の構造図", "slides": [
    {"title": "全体像: 部屋には ai/ だけを渡す(インライン SVG)", "type": "E", "height": "500px", "cells": [
        {"tone": "", "icon": "shield", "tab": "Windows と部屋(WSL)の関係",
         "text": "原本と対応表は\n部屋の外(_noai/)\n\nAI は ai/ の中だけで作業", "fig": inline}]},
    {"title": "全体像: 部屋には ai/ だけを渡す(画像ファイル)", "type": "T",
     "blocks": [{"h": "渡し方", "items": ["ai/ だけをマウントして渡す", "部屋の C: は空", "成果物は room close で戻す"]}],
     "side": {"img": "room-structure-half.svg", "alt": "Windows の works から、ai/ だけを部屋の WSL へマウントする図",
              "caption": "図: room の構造(Excalidraw で作成)"}},
]}
spec["slides"][1]["title"] = "全体像: 部屋には ai/ だけを渡す(半幅用の版)"
spec["slides"].append({"title": "全体像: 部屋には ai/ だけを渡す(全幅の版を半幅に置く)", "type": "T",
     "blocks": [{"h": "渡し方", "items": ["ai/ だけをマウントして渡す", "部屋の C: は空", "成果物は room close で戻す"]}],
     "side": {"img": "room-structure.svg", "alt": "Windows の works から、ai/ だけを部屋の WSL へマウントする図",
              "caption": "図: room の構造(全幅の版)"}})
(work / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
for f in ("revealjs-diagram-theme.scss", "revealjs-diagram-icons.html", "revealjs-diagram-icons-dads.html",
          "revealjs-diagram-icons-lucide.html"):
    if (rec / f).exists():
        shutil.copy(rec / f, work / f)
for n in ("room-structure.svg", "room-structure-half.svg"):
    shutil.copy(here / n, work / n)
subprocess.run([sys.executable, "-I", str(rec / "gen_layouts.py"), "--spec", str(work / "spec.json"),
                "-o", str(work / "excalidraw-trial.qmd"), "--no-id"], check=True)
subprocess.run(["quarto", "render", "excalidraw-trial.qmd"], cwd=work, check=True, shell=(sys.platform == "win32"))
print("done:", work / "excalidraw-trial.html")
