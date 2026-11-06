#!/usr/bin/env python3
"""応答の多い依頼を、応答ごとのツール種別の並びで仕分ける（読み取り専用。依頼文・ツールの入出力は出さない）。

依頼・応答の数え方は requests_by_kind.py と同じ。応答ごとに、呼んだツールを次の記号にして並べる。
  R = 読み・探索（Read, Grep, Glob, WebFetch, WebSearch, Agent 以外の検索系）
  W = 書き込み（Edit, Write, NotebookEdit）
  X = 実行（Bash, PowerShell）
  A = サブエージェント（Agent, Task）
  O = 上のどれでもないもの
  . = ツールを呼ばない応答（文章だけ）
1 応答に複数の種別があれば、W > X > R > A > O の順で強いものを 1 文字にする。

出力（1 依頼 1 行）: session 日付 応答 ピークk 先頭W前の応答数 R W X A O . の回数 型 並び
  先頭W前 = 最初の書き込みの前にあった応答の数（長い = 書く前の探索が長い）。
  型: 書込なし = W が 1 回も無い（実行・読みだけ）/ 探索 =先頭W前が応答の 40% 以上 / 試行錯誤 = W→X→W の往復（WX の切替）が 4 回以上 / 混合 = どちらでもない。

使い方:
  python3 -I long_request_shape.py [--since 2026-10-27] [--min 21] [ディレクトリ...]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from requests_by_kind import USAGE_KEYS, user_text  # noqa: E402

SYM = {
    "Read": "R", "Grep": "R", "Glob": "R", "WebFetch": "R", "WebSearch": "R", "ToolSearch": "R",
    "Edit": "W", "Write": "W", "NotebookEdit": "W",
    "Bash": "X", "PowerShell": "X",
    "Agent": "A", "Task": "A",
}
RANK = "WXRAO"


def shape(path):
    cur = None
    first = True
    order = {}
    seen_tool = set()
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = user_text(d)
        if t is not None:
            if cur:
                yield cur
            cur = {"ts": d.get("timestamp", ""), "resp": []}
            order = {}
            first = False
            continue
        if cur is None or d.get("isSidechain") or d.get("type") != "assistant":
            continue
        m = d.get("message") or {}
        key = (m.get("id"), d.get("requestId"))
        if key not in order:
            u = m.get("usage") or {}
            n = sum(u.get(k, 0) or 0 for k in USAGE_KEYS)
            order[key] = {"syms": set(), "n": n}
            cur["resp"].append(order[key])
        for b in m.get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and ("tu", b.get("id")) not in seen_tool:
                seen_tool.add(("tu", b.get("id")))
                name = b.get("name", "")
                s = SYM.get(name) or ("R" if name.startswith("mcp__") else "O")
                order[key]["syms"].add(s)
    if cur:
        yield cur


def letter(r):
    for c in RANK:
        if c in r["syms"]:
            return c
    return "."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*")
    ap.add_argument("--since", default="")
    ap.add_argument("--min", type=int, default=21)
    a = ap.parse_args()
    roots = [Path(r) for r in a.roots] or [Path.home() / ".claude" / "projects"]
    print("session 日付 応答 ピークk 先頭W前 | R W X A O . | 型 | 並び")
    for r in roots:
        for p in r.rglob("*.jsonl"):
            for q in shape(p):
                n = len(q["resp"])
                if n < a.min or q["ts"] < a.since:
                    continue
                seq = "".join(letter(x) for x in q["resp"])
                before = seq.find("W")
                before = n if before < 0 else before
                sw = sum(1 for i in range(1, len(seq)) if seq[i - 1] in "WX" and seq[i] in "WX" and seq[i - 1] != seq[i])
                kind = "書込なし" if "W" not in seq else "探索" if before >= 0.4 * n else ("試行錯誤" if sw >= 4 else "混合")
                cnt = " ".join(str(seq.count(c)) for c in "RWXAO.")
                peak = max(x["n"] for x in q["resp"]) // 1000
                print(f"{p.stem[:8]} {q['ts'][:10]} {n} {peak}k {before} | {cnt} | {kind} | {seq}")


if __name__ == "__main__":
    main()
