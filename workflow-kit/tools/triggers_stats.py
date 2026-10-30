#!/usr/bin/env python3
"""作業の言葉の索引（triggers）の引き当て率を、Claude Code の会話記録（jsonl）から数える（読み取り専用）。

見るもの: UserPromptSubmit フック（triggers_hook.py）が依頼ごとに出したノートの一覧と、同じ依頼の間（次の依頼まで）に
AI が実際に読んだファイル（Read・Grep の path、Bash / PowerShell のコマンドに書かれたパス）。
  引当率   = 出したノートのうち、同じ依頼の間に読まれた割合。上位 1 件だけの割合も出す。
  取りこぼし = lessons / guides/explain のノートを読んだのに、その依頼でも前の依頼でも出ていなかったもの（索引の語の不足の候補）。
  索引の効いた割合 = lessons / guides/explain のノートの読みのうち、出していたものの割合。
注意: 読まれたことは「引き当てた」ことの代用。読んだだけで使ったかは分からない。AI が AGENTS.md の指示で自分で引いた分は、出力に含めない。

使い方: python -I triggers_stats.py [--since YYYY-MM-DD] [--detail] [会話記録のディレクトリ...]
  既定のディレクトリ = ~/.claude/projects/ の下のすべて。--detail で、依頼ごとの行と取りこぼしの一覧を出す。
"""
import argparse
import json
import re
import sys
from pathlib import Path

MARK = "[作業の言葉の索引]"
KNOW = re.compile(r"(exmem/lessons/|guides/explain/)[A-Za-z0-9_.-]+\.md")
HIT_LINE = re.compile(r"^((?:exmem/lessons|guides/explain|exmem/inbox)/\S+\.md)\s")


def norm(s):
    return s.replace("\\", "/").lower()


def tool_text(block):
    """tool_use の入力から、読んだ先を探すための文字列を作る。"""
    inp = block.get("input") or {}
    return norm(" ".join(str(v) for k, v in inp.items() if k in ("file_path", "path", "command", "pattern", "glob")))


def analyze(path, since):
    turns = []  # {"prompt", "hits", "text"}
    cur = None
    with path.open(encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isSidechain"):
            continue
        ts = d.get("timestamp", "")
        t = d.get("type")
        m = d.get("message") or {}
        c = m.get("content")
        if t == "user" and not d.get("isMeta"):
            blocks = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
            texts = [b.get("text", "") for b in blocks if isinstance(b, dict) and b.get("type") == "text"]
            if texts and not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in blocks):
                cur = {"ts": ts, "prompt": " ".join(texts)[:60].replace("\n", " "), "hits": [], "text": ""}
                turns.append(cur)
        elif t == "attachment" and cur is not None:
            a = d.get("attachment") or {}
            if a.get("type") == "hook_success" and MARK in (a.get("content") or ""):
                for ln in a["content"].splitlines():
                    h = HIT_LINE.match(ln.strip())
                    if h:
                        cur["hits"].append(h.group(1))
        elif t == "assistant" and cur is not None and isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    cur["text"] += " " + tool_text(b)
    return [x for x in turns if x["ts"][:10] >= since]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--since", default="0000-00-00")
    ap.add_argument("--detail", action="store_true")
    a = ap.parse_args()
    dirs = [Path(d) for d in a.dirs] or [Path.home() / ".claude" / "projects"]
    files = [f for d in dirs for f in d.rglob("*.jsonl")]

    prompts = with_hits = shown = shown_read = top1 = top1_read = 0
    know_reads = know_hit = 0
    missed, rows = [], []
    for f in files:
        seen = set()  # このセッションで出したノート
        for x in analyze(f, a.since):
            prompts += 1
            hits = x["hits"]
            seen.update(hits)
            read = {h for h in hits if norm(h) in x["text"]}
            if hits:
                with_hits += 1
                shown += len(hits)
                shown_read += len(read)
                top1 += 1
                top1_read += hits[0] in read
                rows.append(f"{x['ts'][:16]} 出 {len(hits)} 件 / 読 {len(read)} 件  {x['prompt']}")
            for m in {mm.group(0) for mm in KNOW.finditer(x["text"])}:
                know_reads += 1
                if any(m.endswith(s) or s.endswith(m) for s in seen):
                    know_hit += 1
                else:
                    missed.append(f"{x['ts'][:10]} {m}  （依頼: {x['prompt']}）")
    print(f"会話記録 {len(files)} 本 / 依頼 {prompts} 件 / 索引が出した依頼 {with_hits} 件（since {a.since}）")
    if shown:
        print(f"引当率（出したノートが読まれた）: {shown_read}/{shown} = {round(100 * shown_read / shown)}%  上位1件: {top1_read}/{top1} = {round(100 * top1_read / top1)}%")
    else:
        print("引当率: 索引が出した記録がまだ無い（フック導入後の会話が無い）")
    if know_reads:
        print(f"索引の効いた割合（知識ノートの読みのうち、出していたもの）: {know_hit}/{know_reads} = {round(100 * know_hit / know_reads)}%  取りこぼし候補 {len(missed)} 件")
    else:
        print("知識ノートの読み: 0 件")
    if a.detail:
        print("\n依頼ごと:")
        print("\n".join(rows) or "なし")
        print("\n取りこぼし候補（語の不足かもしれない。読んだ理由は会話を見て判断する）:")
        print("\n".join(sorted(set(missed))) or "なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
