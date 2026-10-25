#!/usr/bin/env python3
"""重い会話を、Claude Code の会話記録（jsonl）から挙げる（読み取り専用。`review` の入力 5）。

1回の入力の大きさ = 1回の応答の usage の input_tokens + cache_read_input_tokens + cache_creation_input_tokens。
会話ごとに、その最大値と、最大になった時点の依頼の番号、依頼の数、`wrap` の後に続いた依頼の数を出す。
切るべきだった区切りの手がかり: 「wrap の後も同じ会話で続けた」（`wrap` で始まる依頼より後の依頼の数）。

使い方: python -I heavy_sessions.py [--since YYYY-MM-DD] [--top N] [会話記録のディレクトリ...]
  既定のディレクトリ = ~/.claude/projects/ の下のすべて。サブエージェントの記録（isSidechain）は数えない。
"""
import argparse
import json
from pathlib import Path


def analyze(path, since):
    prompts = 0
    wrap_at = None  # `wrap` で始まる最初の依頼の番号
    peak = (0, 0, "")  # (トークン, 依頼の番号, 時刻)
    first_ts = ""
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isSidechain"):
            continue
        ts = d.get("timestamp", "")
        if ts and not first_ts:
            first_ts = ts
        m = d.get("message") or {}
        c = m.get("content")
        if d.get("type") == "user" and not d.get("isMeta"):
            blocks = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in blocks):
                continue
            text = " ".join(b.get("text", "") for b in blocks if isinstance(b, dict) and b.get("type") == "text").strip()
            if not text:
                continue
            prompts += 1
            if wrap_at is None and text.lower().startswith(("wrap", "締めて")):
                wrap_at = prompts
        elif d.get("type") == "assistant":
            u = m.get("usage") or {}
            n = sum(u.get(k, 0) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            if n > peak[0]:
                peak = (n, prompts, ts)
    if since and first_ts[:10] < since and peak[2][:10] < since:
        return None
    return {
        "file": path.name,
        "dir": path.parent.name,
        "start": first_ts[:16],
        "prompts": prompts,
        "peak": peak[0],
        "peak_at": peak[1],
        "after_wrap": 0 if wrap_at is None else prompts - wrap_at,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("dirs", nargs="*")
    a = ap.parse_args()
    roots = [Path(x) for x in a.dirs] or [Path.home() / ".claude" / "projects"]
    rows = []
    for r in roots:
        for p in r.rglob("*.jsonl"):
            row = analyze(p, a.since)
            if row and row["peak"]:
                rows.append(row)
    rows.sort(key=lambda x: -x["peak"])
    print(f"会話記録 {len(rows)} 本（since {a.since or '指定なし'}）。1回の入力の最大が大きい順に上位 {a.top} 件")
    for x in rows[: a.top]:
        print(f"{x['peak']:>9,} トークン  {x['start']}  依頼 {x['prompts']} 件（最大は {x['peak_at']} 件目）"
              f"  wrap 後に続いた依頼 {x['after_wrap']} 件  {x['dir']}/{x['file'][:8]}")


if __name__ == "__main__":
    main()
