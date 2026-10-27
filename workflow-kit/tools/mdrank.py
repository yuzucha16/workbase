#!/usr/bin/env python3
"""場面の依頼文を、本番の索引（find_knowledge.py --triggers）で引き、期待ノートの順位を数える（2026-10-25）。

使い方: python -I workflow-kit/tools/mdrank.py [リポジトリのルート] [--scenarios 場面.md] [--top 5]
場面は workflow-kit/triggers-scenarios.md の S 行（2列目の「場面」の文）と B 行（2列目の依頼文）。期待ノートは、S 行は4列目、B 行は3列目のバッククォートのパス。
期待ノートが索引の対象（lessons・guides/explain・inbox）に無い場面は「対象外」として数えない。
出力は件数と、1 位でない場面だけ（読むだけ。ノートは直さない）。mdreach.py が語の列で測るのに対し、こちらは依頼の文で測る。
"""
import argparse, contextlib, importlib.util, io, re, sys
from pathlib import Path

sys.dont_write_bytecode = True  # kit の tools/ に __pycache__ を作らない
HERE = Path(__file__).resolve()
ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(HERE.parents[2]))
ap.add_argument("--scenarios", default=str(HERE.parents[1] / "triggers-scenarios.md"))
ap.add_argument("--top", type=int, default=5, help="本番の既定（find_knowledge.py --triggers の上位件数）")
a = ap.parse_args()
root = Path(a.root).resolve()

spec = importlib.util.spec_from_file_location("find_knowledge", root / "workflow-kit" / "tools" / "find_knowledge.py")
fk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fk)
indexed = {f.relative_to(root).as_posix() for _, f in fk.trigger_files(root)}


def ranking(query):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fk.lookup_triggers(root, query, 999)
    return [l.split()[0] for l in buf.getvalue().splitlines() if re.match(r"\S+\.md\s", l)]


rows = []
for l in Path(a.scenarios).read_text(encoding="utf-8").splitlines():
    m = re.match(r"\| ([SB]\d+) ", l)
    if not m:
        continue
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    goal_col = c[3] if m.group(1).startswith("S") else c[2]
    rows.append((m.group(1), c[1].replace("`", ""), set(re.findall(r"`([^`\s]+\.md)`", goal_col))))

top1 = topn = n = 0
out_of_scope, notes = [], []
for sid, query, goals in rows:
    goals &= indexed
    if not goals:
        out_of_scope.append(sid)
        continue
    n += 1
    order = ranking(query)
    rank = min((order.index(g) + 1 for g in goals if g in order), default=None)
    top1 += rank == 1
    topn += rank is not None and rank <= a.top
    if rank != 1:
        notes.append(f"  {sid} {'なし' if rank is None else f'{rank} 位'} / {len(order)} 件: {query}")

print(f"場面 {n} 件（対象外 {len(out_of_scope)}: {' '.join(out_of_scope) or 'なし'}）/ 1 位 {top1}/{n} / 上位 {a.top} 件 {topn}/{n}")
if notes:
    print("1 位でない場面:")
    print("\n".join(notes))
