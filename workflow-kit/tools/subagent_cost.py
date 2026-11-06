#!/usr/bin/env python3
"""subagent を使った会話について、本体と subagent の入力トークン・応答数を並べる（token-cap NA 5h の観察用）。

requests_by_kind.py は subagent（isSidechain）を数えない。ここでは `<会話>/subagents/agent-*.jsonl` を会話ごとに合算する。
入力トークンの数え方は requests_by_kind.py と同じ（input + cache_read + cache_creation。出力を含まない）。

使い方: python -I subagent_cost.py [root ...] [--since YYYY-MM-DD]   （root 省略時は ~/.claude/projects）
出力: 会話 | 本体の応答 | 本体トークン | subagent 数 | subagent の応答 | subagent トークン | subagent の割合 | 最初の subagent の依頼文の冒頭
"""
import argparse
import json
from pathlib import Path

USAGE_KEYS = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def totals(path):
    """(応答数, 入力トークン合計, 冒頭の依頼文, 最初の時刻)。同じ応答の重複行は数えない。"""
    seen, resp, tok, head, ts = set(), 0, 0, "", ""
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        ts = ts or d.get("timestamp", "")
        m = d.get("message") or {}
        if d.get("type") == "user" and not head and isinstance(m.get("content"), str):
            head = m["content"].strip().replace("\n", " ")[:40]
        if d.get("type") != "assistant":
            continue
        key = (m.get("id"), d.get("requestId"))
        if key in seen:
            continue
        seen.add(key)
        u = m.get("usage") or {}
        resp += 1
        tok += sum(u.get(k, 0) or 0 for k in USAGE_KEYS)
    return resp, tok, head, ts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*")
    ap.add_argument("--since", default="")
    a = ap.parse_args()
    roots = [Path(r) for r in a.roots] or [Path.home() / ".claude" / "projects"]
    rows = []
    for r in roots:
        for sub in r.rglob("subagents"):
            agents = sorted(sub.glob("agent-*.jsonl"))
            main_file = sub.parent.with_suffix(".jsonl")
            if not agents or not main_file.exists():
                continue
            mr, mt, _, ts = totals(main_file)
            if ts < a.since:
                continue
            ar = at = 0
            head = ""
            for p in agents:
                r_, t_, h_, _ = totals(p)
                ar, at, head = ar + r_, at + t_, head or h_
            rows.append((main_file.stem[:8], mr, mt, len(agents), ar, at, head))
    if not rows:
        raise SystemExit("subagent を使った会話がない")
    print("会話 | 本体の応答 | 本体トークン | subagent 数 | subagent の応答 | subagent トークン | subagent の割合 | 最初の依頼文の冒頭")
    for s, mr, mt, n, ar, at, h in rows:
        print(f"{s} | {mr} | {mt/1e6:.2f}M | {n} | {ar} | {at/1e6:.2f}M | {at/(mt+at):.0%} | {h}")
    mt = sum(r[2] for r in rows)
    at = sum(r[5] for r in rows)
    print(f"合計: {len(rows)} 会話、本体 {mt/1e6:.1f}M、subagent {at/1e6:.1f}M（{at/(mt+at):.0%}）")


if __name__ == "__main__":
    main()
