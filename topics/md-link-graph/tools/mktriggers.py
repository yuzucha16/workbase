#!/usr/bin/env python3
"""lessons の frontmatter の triggers: から、作業の言葉の表を作る（試作）。

使い方: python -I topics/md-link-graph/tools/mktriggers.py [リポジトリのルート] [--out 出力.md]
既定の出力 = topics/md-link-graph/records/triggers-prototype.md。
"""
import argparse, re
from pathlib import Path

HERE = Path(__file__).resolve()
ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(HERE.parents[3]))
ap.add_argument("--out", default=str(HERE.parents[1] / "records" / "triggers-prototype.md"))
a = ap.parse_args()
root = Path(a.root).resolve()

rows = []
for p in sorted((root / "exmem" / "lessons").glob("*.md")):
    m = re.search(r"^triggers:\s*\[(.*?)\]\s*$", p.read_text(encoding="utf-8").split("\n---", 1)[0], re.M)
    if m:
        words = [w.strip() for w in m.group(1).split(",") if w.strip()]
        rows.append(f"- {' / '.join(words)} → `{p.relative_to(root).as_posix()}`")

head = "# 作業の言葉の表（試作。`triggers:` から生成）\n\n作業の前に、この表で作業の言葉を引く。1 行 = 言葉の一覧 → 読むノート。\n\n"
Path(a.out).write_text(head + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
print(f"{len(rows)} 件 → {a.out}")
