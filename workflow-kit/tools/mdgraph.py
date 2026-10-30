#!/usr/bin/env python3
"""Markdown の参照グラフを数えて、循環・階層・複雑度を文字で出す（HTML は 2026-10-30 にやめた。使われなかったため）。

使い方: python -I workflow-kit/tools/mdgraph.py [リポジトリのルート] [--start AGENTS.md ...] [--kinds wiki md include tick] [--top 5]
既定: ルート = この files の 2 つ上（リポジトリのトップ）、起点 = AGENTS.md README.md docs/log.md、
出力 = 標準出力のみ（読むだけ。ファイルは書かない）。見る指標: 循環（最大の強連結成分の割合）、階層（起点からの深さ、未到達）、複雑度（1 ファイルあたりの辺、入次数・出次数の上位）。辺の種類: wiki（[[名前]]）、md（[](x.md)）、include（行頭の @x.md）、tick（`x.md`）。
"""
import argparse, collections, re, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(HERE.parents[2]))
ap.add_argument("--top", type=int, default=5, help="入次数・出次数の上位の件数")
ap.add_argument("--start", nargs="*", default=["AGENTS.md", "README.md", "docs/log.md"])
ap.add_argument("--kinds", nargs="*", default=["wiki", "md", "include", "tick"], help="数える辺の種類（wiki md include tick）")
a = ap.parse_args()
root = Path(a.root).resolve()
sys.stdout.reconfigure(encoding="utf-8")

SKIP = {".git", "node_modules", ".obsidian"}
def is_unlinked_by_design(p):
    """辿って読まれないファイル。雛形（templates/）と、`@AGENTS.md` だけの CLAUDE.md（Claude Code が自動で取り込む）。2026-10-25 ユーザーの決定。"""
    r = p.relative_to(root).as_posix()
    if "/templates/" in "/" + r:
        return True
    return p.name == "CLAUDE.md" and re.fullmatch(r"@\S+\.md\s*", p.read_text(encoding="utf-8", errors="replace")) is not None


files = [p for p in root.rglob("*.md") if not (SKIP & set(p.relative_to(root).parts)) and not is_unlinked_by_design(p)]
rel = {p: p.relative_to(root).as_posix() for p in files}
by_rel = {r: p for p, r in rel.items()}
by_name = collections.defaultdict(list)
for r in by_rel:
    by_name[Path(r).stem].append(r)

WIKI = re.compile(r"\[\[([^\]|#]+)")
MDL = re.compile(r"\]\(([^)#\s]+\.md)")
INC = re.compile(r"^@(\S+\.md)", re.M)
TICK = re.compile(r"`([^`\s]+\.md)`")


def resolve(src, tgt):
    t = tgt.strip().replace("\\", "/")
    base = Path(rel[src]).parent
    for c in ((base / t).as_posix(), t):
        parts = []
        for seg in c.split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg != ".":
                parts.append(seg)
        c = "/".join(parts)
        if c in by_rel:
            return c
    m = by_name.get(Path(t).stem, [])
    if len(m) == 1:
        return m[0]
    s = [r for r in by_rel if r == t or r.endswith("/" + t)]
    return s[0] if len(s) == 1 else None


edges = collections.defaultdict(lambda: collections.defaultdict(set))  # src -> dst -> kinds
for p in files:
    text = p.read_text(encoding="utf-8", errors="replace")
    for rx, k in ((WIKI, "wiki"), (MDL, "md"), (INC, "include"), (TICK, "tick")):
        if k not in a.kinds:
            continue
        for m in rx.finditer(text):
            t = resolve(p, m.group(1))
            if t and t != rel[p]:
                edges[rel[p]][t].add(k)

nodes = sorted(rel.values())
adj = {n: sorted(edges[n]) for n in nodes}
indeg = collections.Counter(t for n in nodes for t in adj[n])
dist = {}
q = collections.deque()
for s in a.start:
    if s in adj:
        dist[s] = 0
        q.append(s)
while q:
    n = q.popleft()
    for t in adj[n]:
        if t not in dist:
            dist[t] = dist[n] + 1
            q.append(t)

# 強連結成分（反復 Tarjan）
index, low, on, st, comp_of, comps, cnt = {}, {}, set(), [], {}, [], [0]
for v0 in nodes:
    if v0 in index:
        continue
    index[v0] = low[v0] = cnt[0]; cnt[0] += 1; st.append(v0); on.add(v0)
    work = [(v0, iter(adj[v0]))]
    while work:
        n, it = work[-1]
        for w in it:
            if w not in index:
                index[w] = low[w] = cnt[0]; cnt[0] += 1; st.append(w); on.add(w)
                work.append((w, iter(adj[w])))
                break
            elif w in on:
                low[n] = min(low[n], index[w])
        else:
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[n])
            if low[n] == index[n]:
                c = []
                while True:
                    w = st.pop(); on.discard(w); c.append(w)
                    if w == n:
                        break
                for w in c:
                    comp_of[w] = len(comps)
                comps.append(c)
big = max(comps, key=len)


kind_count = collections.Counter(k for n in nodes for t in adj[n] for k in edges[n][t])
n_edges = sum(len(adj[n]) for n in nodes)
depth = dict(sorted(collections.Counter(dist.values()).items()))
unreached = sorted(n for n in nodes if n not in dist)
orphans = sorted(n for n in nodes if indeg[n] == 0)
top = lambda key: ", ".join(f"{n}({key[n]})" for n in sorted(nodes, key=lambda n: -key[n])[:a.top])
outdeg = {n: len(adj[n]) for n in nodes}

print(f"{len(nodes)} ファイル / {n_edges} 辺 / 辺の種類 " + " ".join(f"{k} {v}" for k, v in sorted(kind_count.items())))
print(f"[循環] 最大の循環 {len(big)} ファイル（{round(100 * len(big) / len(nodes))}%） / 循環の数 {sum(1 for c in comps if len(c) > 1)}")
print(f"[階層] 起点から到達 {len(dist)} / 未到達 {len(unreached)} / 最大の深さ {max(depth)} / 深さ別 {depth}")
print(f"[複雑度] 1 ファイルあたりの辺 {n_edges / len(nodes):.1f} / 入次数の上位 {top(indeg)} / 出次数の上位 {top(outdeg)}")
print(f"入次数 0 {len(orphans)} / 未到達 {len(unreached)}")
for label, names in (("未到達", unreached), ("入次数 0", orphans)):
    print(f"{label}: {' '.join(names) or 'なし'}")
