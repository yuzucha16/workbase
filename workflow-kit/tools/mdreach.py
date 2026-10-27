#!/usr/bin/env python3
"""場面ごとの到達を数える（md-link-graph の論点 D の (a)）。

使い方: python -I workflow-kit/tools/mdreach.py [リポジトリのルート] [--scenarios 場面.md] [--table]
--table: lessons の frontmatter の triggers: から作業の言葉の表を（ファイルにせず）メモリ上で作り、起点に足す。
各場面で、起点（AGENTS.md README.md docs/log.md）から、作業の言葉が書かれた行にあるリンクだけを辿り、
期待ノートに何ホップで着くかを出す。比較として、言葉を問わず辿った最短ホップ（構造上の距離）も出す。
辺の種類は mdgraph.py と同じ（wiki / md / include / tick）。
"""
import argparse, collections, re, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(HERE.parents[2]))
ap.add_argument("--scenarios", default=str(HERE.parents[1] / "triggers-scenarios.md"))
ap.add_argument("--start", nargs="*", default=["AGENTS.md", "README.md", "docs/log.md"])
ap.add_argument("--table", action="store_true", help="作業の言葉の表（triggers: から作る）。毎回読まれる前提で、起点に足す")
a = ap.parse_args()
TABLE = "(triggers-table)"
if a.table:
    a.start = a.start + [TABLE]
root = Path(a.root).resolve()
sys.stdout.reconfigure(encoding="utf-8")

SKIP = {".git", "node_modules", ".obsidian"}
files = {p.relative_to(root).as_posix(): p for p in root.rglob("*.md") if not (SKIP & set(p.relative_to(root).parts))}
by_name = collections.defaultdict(list)
for r in files:
    by_name[Path(r).stem].append(r)
WIKI = re.compile(r"\[\[([^\]|#]+)")
MDL = re.compile(r"\]\(([^)#\s]+\.md)")
INC = re.compile(r"^@(\S+\.md)")
TICK = re.compile(r"`([^`\s]+\.md)`")


def resolve(src, tgt):
    t = tgt.strip().replace("\\", "/")
    for c in ((Path(src).parent / t).as_posix(), t):
        parts = []
        for seg in c.split("/"):
            if seg == "..":
                parts and parts.pop()
            elif seg != ".":
                parts.append(seg)
        c = "/".join(parts)
        if c in files:
            return c
    m = by_name.get(Path(t).stem, [])
    if len(m) == 1:
        return m[0]
    s = [r for r in files if r == t or r.endswith("/" + t)]
    return s[0] if len(s) == 1 else None


links = collections.defaultdict(list)  # src -> [(dst, 行の文字列)]
for r, p in files.items():
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        for rx in (WIKI, MDL, INC, TICK):
            for m in rx.finditer(line):
                t = resolve(r, m.group(1))
                if t and t != r:
                    links[r].append((t, line))


if a.table:
    files[TABLE] = None
    for p in sorted((root / "exmem" / "lessons").glob("*.md")):
        m = re.search(r"^triggers:\s*\[(.*?)\]\s*$", p.read_text(encoding="utf-8").split("\n---", 1)[0], re.M)
        if m:
            words = [w.strip() for w in m.group(1).split(",") if w.strip()]
            links[TABLE].append((p.relative_to(root).as_posix(), " / ".join(words)))


def hops(goal_set, words):
    """起点から最短ホップ。words があれば、その語を含む行のリンクだけ辿る。着かなければ None。"""
    d = {s: 0 for s in a.start if s in files}
    q = collections.deque(d)
    while q:
        n = q.popleft()
        if n in goal_set:
            return d[n]
        for t, line in links[n]:
            if t in d:
                continue
            if words and not any(w.lower() in line.lower() for w in words):
                continue
            d[t] = d[n] + 1
            q.append(t)
    return None


rows = [l for l in Path(a.scenarios).read_text(encoding="utf-8").splitlines() if re.match(r"\| S\d+ ", l)]
print("| ID | 作業の言葉で着く | 言葉を問わず着く | 期待ノート |\n|---|---|---|---|")
miss = 0
for l in rows:
    c = [x.strip() for x in l.strip("|").split("|")]
    goals = {g for g in (resolve("AGENTS.md", x) for x in re.findall(r"`([^`\s]+\.md)`", c[3])) if g}
    words = [w for w in re.split(r"\s+", c[2].replace("`", "")) if w]
    h = hops(goals, words)
    h0 = hops(goals, None)
    miss += h is None
    print(f"| {c[0]} | {'着かない' if h is None else str(h) + ' ホップ'} | {'着かない' if h0 is None else str(h0) + ' ホップ'} | {', '.join(sorted(goals)) or '（解決できない）'} |")
print(f"\n届かない場面: {miss} / {len(rows)}")
