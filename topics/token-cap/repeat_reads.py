#!/usr/bin/env python3
"""Read の「同じファイルの重複読み」と「全文読み」が、結果の大きさのどれだけを占めるかを数える（読み取り専用）。

出すのは件数と文字数だけ（題名・本文・ファイル名は出さない。拡張子ごとの集計のみ）。
大きさは文字数（トークンではない）。サブエージェントの記録（isSidechain）は数えない。
重複 = 同じ会話の中で、同じ file_path を 2 回目以降に Read したもの。
全文読み = offset も limit も付かない Read。

使い方:
  python -I repeat_reads.py [--since YYYY-MM-DD] [--detail [N]] [ディレクトリ...]
    --detail: 全文読みの md の名前（末尾 2 階層）・回数・文字数を上位 N 件出す。本文は出さない。
    既定のディレクトリ = ~/.claude/projects/ の下のすべて。
    --since: 会話記録の更新日がその日以降のものだけ数える。
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def text_len(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(x.get("text", "")) for x in content if isinstance(x, dict))
    return 0


def scan(path):
    """会話 1 本の Read を [(file_path, 全文か, 文字数)] で返す。"""
    calls, result_len = {}, {}
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isSidechain"):
            continue
        c = (d.get("message") or {}).get("content")
        if not isinstance(c, list):
            continue
        for b in c:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_result":
                result_len[b.get("tool_use_id")] = text_len(b.get("content"))
            elif b.get("type") == "tool_use" and b.get("name") == "Read" and b["id"] not in calls:
                i = b.get("input") or {}
                calls[b["id"]] = (i.get("file_path", ""), not ("offset" in i or "limit" in i))
    return [(fp, full, result_len.get(tid, 0)) for tid, (fp, full) in calls.items()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("--detail", type=int, nargs="?", const=15, default=0, help="全文読みの md を上位 N 件（既定 15）出す")
    ap.add_argument("roots", nargs="*")
    a = ap.parse_args()
    roots = [Path(r) for r in a.roots] or [Path.home() / ".claude" / "projects"]
    since = datetime.fromisoformat(a.since).timestamp() if a.since else 0

    n_sess = n_read = chars = 0
    full_n = full_c = dup_n = dup_c = full_dup_c = 0
    big_full = Counter()  # 拡張子 -> 全文読みの文字数
    by_file = {}  # md の名前 -> (回数, 文字数)
    for r in roots:
        for p in r.rglob("*.jsonl"):
            if p.stat().st_mtime < since:
                continue
            reads = scan(p)
            if not reads:
                continue
            n_sess += 1
            seen = set()
            for fp, full, n in reads:
                n_read += 1
                chars += n
                if full:
                    full_n += 1
                    full_c += n
                    big_full[Path(fp.replace("\\", "/")).suffix or "(なし)"] += n
                    if fp.endswith(".md"):
                        k = "/".join(fp.replace("\\", "/").split("/")[-2:])
                        c0, n0 = by_file.get(k, (0, 0))
                        by_file[k] = (c0 + 1, n0 + n)
                if fp in seen:
                    dup_n += 1
                    dup_c += n
                    if full:
                        full_dup_c += n
                seen.add(fp)

    def pct(x):
        return f"{100 * x / chars:.0f}%" if chars else "-"

    print(f"会話 {n_sess} 本、Read {n_read} 回、結果 {chars:,} 文字")
    print(f"全文読み {full_n} 回（{full_n * 100 // max(n_read, 1)}%）、{full_c:,} 文字（{pct(full_c)}）")
    print(f"重複読み {dup_n} 回（{dup_n * 100 // max(n_read, 1)}%）、{dup_c:,} 文字（{pct(dup_c)}）。うち全文の重複 {full_dup_c:,} 文字")
    print("全文読みの拡張子別（文字数の多い順）: " + "、".join(f"{k} {v:,}" for k, v in big_full.most_common(5)))
    if a.detail:
        print(f"全文読みの md（文字数の多い順、上位 {a.detail} 件。名前 = 末尾 2 階層）:")
        for k, (cnt, ch) in sorted(by_file.items(), key=lambda x: -x[1][1])[: a.detail]:
            print(f"  {ch:>9,} 文字 {cnt:>3} 回 {ch // cnt:>7,}/回  {k}")


if __name__ == "__main__":
    main()
