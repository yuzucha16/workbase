#!/usr/bin/env python3
"""1 本の会話を、道具名・ファイル名・大きさだけで分解する（読み取り専用。題名と本文は出さない）。

`heavy_sessions.py` で見つけた重い会話が、全文読みの連発（`integrate` の型）かを確かめる。
応答は message.id、道具の呼び出しは tool_use の id で重複を除く（jsonl は内容ブロックごとに行が増える）。
大きさは文字数（トークンではない）。サブエージェントの記録（isSidechain）は数えない。

使い方:
  python -I decompose_session.py <会話記録.jsonl>
  python -I decompose_session.py --at 2026-10-27T03:22 [ディレクトリ...]
    --at: その時刻に最も近い所で最大の入力に達した会話を選ぶ（時刻は heavy_sessions.py の表示と同じ記録上の値）。
    既定のディレクトリ = ~/.claude/projects/ の下のすべて。
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

USAGE_KEYS = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def records(path):
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not d.get("isSidechain"):
            yield d


def peak_ts(path):
    best = (0, "")
    seen = set()
    for d in records(path):
        if d.get("type") != "assistant":
            continue
        m = d.get("message") or {}
        key = (m.get("id"), d.get("requestId"))
        if key in seen:
            continue
        seen.add(key)
        u = m.get("usage") or {}
        n = sum(u.get(k, 0) or 0 for k in USAGE_KEYS)
        if n > best[0]:
            best = (n, d.get("timestamp", ""))
    return best


def find_by_time(at, roots):
    target = parse_ts(at)
    if target is None:
        raise SystemExit(f"--at の形式が読めない: {at}（例 2026-10-27T03:22）")
    cands = []
    for r in roots:
        for p in r.rglob("*.jsonl"):
            n, ts = peak_ts(p)
            t = parse_ts(ts)
            if n and t:
                cands.append((abs((t - target).total_seconds()), p, n, ts))
    if not cands:
        raise SystemExit("会話記録が見つからない")
    cands.sort(key=lambda x: x[0])
    for gap, p, n, ts in cands[:3]:
        print(f"候補: 最大 {n:,} トークン {ts[:16]}（差 {int(gap)} 秒） {p}")
    return cands[0][1]


def where(file_path):
    parts = Path(file_path.replace("\\", "/")).parts
    return "/".join(parts[-3:-1]) if len(parts) >= 3 else "/".join(parts[:-1]) or "?"


def text_len(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(x.get("text", "")) for x in content if isinstance(x, dict))
    return 0


def decompose(path):
    seen_msg = set()
    inputs = []  # 応答ごとの入力の大きさ
    calls = {}  # tool_use id -> (name, file_path)
    result_len = {}  # tool_use id -> 文字数
    prompts = 0
    for d in records(path):
        m = d.get("message") or {}
        c = m.get("content")
        if d.get("type") == "user" and not d.get("isMeta") and isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    result_len[b.get("tool_use_id")] = text_len(b.get("content"))
        if d.get("type") == "user" and not d.get("isMeta"):
            blocks = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
            if not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in blocks):
                if any(isinstance(b, dict) and b.get("text", "").strip() for b in blocks):
                    prompts += 1
        if d.get("type") != "assistant":
            continue
        key = (m.get("id"), d.get("requestId"))
        if key not in seen_msg:
            seen_msg.add(key)
            u = m.get("usage") or {}
            inputs.append(sum(u.get(k, 0) or 0 for k in USAGE_KEYS))
        for b in c if isinstance(c, list) else []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b["id"] not in calls:
                i = b.get("input") or {}
                calls[b["id"]] = (b["name"], i.get("file_path") or i.get("path") or "", "offset" in i or "limit" in i)

    print(f"会話: {path}")
    print(f"依頼 {prompts} 件、応答 {len(inputs)} 回、土台（1 回目） {inputs[0]:,}、最大 {max(inputs):,}" if inputs else "応答なし")
    if len(inputs) > 1:
        steps = sorted((b - a for a, b in zip(inputs, inputs[1:])), reverse=True)
        print(f"1 回の増加: 最大 {steps[0]:,}、8k 超 {sum(1 for s in steps if s > 8000)} 回")

    by_tool, chars = Counter(), Counter()
    for tid, (name, _, _) in calls.items():
        by_tool[name] += 1
        chars[name] += result_len.get(tid, 0)
    print("\n道具: 回数 / 結果の文字数")
    for name, n in by_tool.most_common():
        print(f"  {name:<12}{n:>5} 回 {chars[name]:>10,} 文字")

    reads = [(fp, part, result_len.get(tid, 0)) for tid, (name, fp, part) in calls.items() if name == "Read"]
    full = sum(1 for _, part, _ in reads if not part)
    print(f"\nRead {len(reads)} 回のうち、全文読み（offset/limit なし）{full} 回、部分読み {len(reads) - full} 回")
    per_file = Counter(fp for fp, _, _ in reads)
    dups = {fp: n for fp, n in per_file.items() if n > 1}
    print(f"同じファイルの重複読み: {len(dups)} ファイル" + ("" if not dups else " : " +", ".join(f"{Path(f).name}×{n}" for f, n in dups.items())))

    by_dir, size_of = Counter(), Counter()
    for fp, _, n in reads:
        by_dir[where(fp)] += n
        size_of[fp] += n
    total = sum(by_dir.values()) or 1
    print(f"\nRead の結果を置き場別に（計 {total:,} 文字）")
    for dname, n in by_dir.most_common(8):
        print(f"  {dname:<30}{n:>10,} 文字 {n * 100 // total:>3}%")
    print("\n大きい順のファイル（上位 8）")
    for fp, n in size_of.most_common(8):
        print(f"  {n:>8,} 文字  {Path(fp.replace(chr(92), '/')).name}  ×{per_file[fp]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", default="")
    ap.add_argument("target", nargs="*", help="jsonl のパス、または --at と使うディレクトリ")
    a = ap.parse_args()
    if a.at:
        roots = [Path(x) for x in a.target] or [Path.home() / ".claude" / "projects"]
        path = find_by_time(a.at, roots)
    elif len(a.target) == 1 and a.target[0].endswith(".jsonl"):
        path = Path(a.target[0])
    else:
        ap.error("jsonl のパスを 1 つ、または --at を指定する")
    decompose(path)


if __name__ == "__main__":
    main()
