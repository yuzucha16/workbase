#!/usr/bin/env python3
"""依頼ごとの応答数を、依頼の種類別に集計する（読み取り専用。本文は出さない）。

依頼 = ユーザーのテキスト入力（tool_result でない user 行）から、次のテキスト入力の直前まで。
応答 = (message.id, requestId) の固有数（jsonl は内容ブロックごとに行が増える）。サブエージェント（isSidechain）は数えない。
種類は、依頼文の語の一致で付ける（本文は出力しない。どれにも当たらなければ other）。
トークンは入力側（input + cache_read + cache_creation）の合計で、出力を含まない。

使い方:
  python -I requests_by_kind.py [--since 2026-10-01] [--detail] [--csv out.csv] [ディレクトリ...]
    --detail: other の 101 文字以上を、置き場（cwd）・長さ・最初か途中か・コードブロックの有無で仕分け、
              continue と全体を「会話の最初の依頼か」で分ける（依頼文は出さない）。
    既定のディレクトリ = ~/.claude/projects/ の下のすべて。
"""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

USAGE_KEYS = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")

# (種類, 語)。上から順に最初に当たったものを採る。
KINDS = [
    ("wrap", ("wrap", "ラップ", "終わりにして")),
    ("review", ("review", "レビュー")),
    ("integrate", ("integrate", "inbox", "統合", "ナレッジ化", "理解ガイド")),
    ("commit-push", ("commit", "push", "コミット", "プッシュ")),
    ("retrospective", ("振り返", "retrospective")),
    ("research", ("調べ", "調査", "リサーチ")),
    ("plan", ("計画", "プラン")),
    ("continue", ("の続き", "続き")),
]


def user_text(d):
    """実プロンプトのテキストを返す。tool_result・システム注入なら None。"""
    if d.get("type") != "user" or d.get("isSidechain") or d.get("isMeta"):
        return None
    c = (d.get("message") or {}).get("content")
    if isinstance(c, str):
        t = c
    elif isinstance(c, list):
        if any(b.get("type") == "tool_result" for b in c if isinstance(b, dict)):
            return None
        t = "".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    t = t.strip()
    if not t or t.startswith(("<system-reminder", "<command-", "<local-command", "[Request interrupted")):
        return None
    return t


def kind_of(t):
    low = t[:80].lower()  # 貼り付けの本文に引かれないよう、冒頭だけで判定する
    for k, words in KINDS:
        if any(w in low for w in words):
            return k
    return "other"


def requests(path):
    cur = None
    first = True
    seen = set()
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = user_text(d)
        if t is not None:
            if cur:
                yield cur
            cwd = (d.get("cwd") or "").replace("\\", "/").rstrip("/").rsplit("/", 1)[-1] or "?"
            cur = {"kind": kind_of(t), "chars": len(t), "ts": d.get("timestamp", ""),
                   "responses": 0, "tokens": 0, "peak": 0, "tools": 0,
                   "cwd": cwd, "first": first, "code": "```" in t}
            first = False
            continue
        if cur is None or d.get("isSidechain") or d.get("type") != "assistant":
            continue
        m = d.get("message") or {}
        key = (m.get("id"), d.get("requestId"))
        for b in m.get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                bid = ("tu", b.get("id"))
                if bid not in seen:
                    seen.add(bid)
                    cur["tools"] += 1
        if key in seen:
            continue
        seen.add(key)
        u = m.get("usage") or {}
        n = sum(u.get(k, 0) or 0 for k in USAGE_KEYS)
        cur["responses"] += 1
        cur["tokens"] += n
        cur["peak"] = max(cur["peak"], n)
    if cur:
        yield cur


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def group_table(title, qs, key, tot_r, tot_t):
    """qs を key の値で分け、件数・応答・トークンを表にする（トークンの多い順）。"""
    print(title)
    print("区分 | 件数 | 応答 平均 | ツール平均 | 応答の割合 | トークンの割合 | トークンの合計")
    g = defaultdict(list)
    for q in qs:
        g[key(q)].append(q)
    for k, xs in sorted(g.items(), key=lambda kv: -sum(q["tokens"] for q in kv[1])):
        st = sum(q["tokens"] for q in xs)
        sr = sum(q["responses"] for q in xs)
        print(f"{k} | {len(xs)} | {statistics.mean(q['responses'] for q in xs):.1f} | "
              f"{statistics.mean(q['tools'] for q in xs):.1f} | {sr/tot_r:.0%} | {st/tot_t:.0%} | {st/1e6:.1f}M")
    print()


def detail(rows, tot_r, tot_t):
    """other の長い依頼（101 文字以上）の仕分けと、continue の位置。依頼文は出さない。"""
    long_other = [q for q in rows if q["kind"] == "other" and q["chars"] >= 101]
    print()
    print(f"== --detail: other の 101 文字以上 {len(long_other)} 件（依頼文は出さない。区分名は cwd の末尾の名前）")
    band = lambda q: next(f"{lo}-{hi}" for lo, hi in ((101, 300), (301, 1000), (1001, 10**9)) if lo <= q["chars"] <= hi)
    group_table("① 置き場（cwd）別", long_other, lambda q: q["cwd"], tot_r, tot_t)
    group_table("② 長さの帯別（文字）", long_other, band, tot_r, tot_t)
    group_table("③ 会話の最初の依頼か", long_other, lambda q: "最初" if q["first"] else "途中", tot_r, tot_t)
    group_table("④ コードブロックの有無", long_other, lambda q: "あり" if q["code"] else "なし", tot_r, tot_t)
    cont = [q for q in rows if q["kind"] == "continue"]
    print(f"== --detail: continue {len(cont)} 件")
    group_table("⑤ 会話の最初の依頼か（最初なら「続き」の起動の読みが入る）", cont, lambda q: "最初" if q["first"] else "途中", tot_r, tot_t)
    group_table("⑥ 全体: 会話の最初の依頼か（種類別でなく全依頼）", rows, lambda q: "最初" if q["first"] else "途中", tot_r, tot_t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*")
    ap.add_argument("--detail", action="store_true", help="other の長い依頼と continue の仕分けを足す")
    ap.add_argument("--since", default="")
    ap.add_argument("--csv", default="")
    a = ap.parse_args()
    roots = [Path(r) for r in a.roots] or [Path.home() / ".claude" / "projects"]
    rows = []
    for r in roots:
        for p in r.rglob("*.jsonl"):
            for q in requests(p):
                if q["responses"] and q["ts"] >= a.since:
                    q["session"] = p.stem[:8]
                    rows.append(q)
    if not rows:
        raise SystemExit("該当する依頼がない")
    by = defaultdict(list)
    for q in rows:
        by[q["kind"]].append(q)
    tot_r = sum(q["responses"] for q in rows)
    tot_t = sum(q["tokens"] for q in rows)
    print(f"依頼 {len(rows)} 件、応答 {tot_r}、入力トークン {tot_t/1e6:.1f}M（出力を含まない）")
    rs = [q["responses"] for q in rows]
    print(f"全体の1依頼あたり応答: 平均 {statistics.mean(rs):.1f}、中央値 {statistics.median(rs):.0f}、上位10% {pct(rs, .9)}、最大 {max(rs)}")
    print()
    print("種類 | 件数 | 応答 平均 | 中央値 | 上位10% | 最大 | 応答の割合 | トークンの割合 | 1応答の平均入力 | ツール平均 | 依頼文の長さ(中央値・文字)")
    for k, qs in sorted(by.items(), key=lambda kv: -sum(q["tokens"] for q in kv[1])):
        rr = [q["responses"] for q in qs]
        sr = sum(rr)
        st = sum(q["tokens"] for q in qs)
        tl = statistics.mean(q["tools"] for q in qs)
        print(f"{k} | {len(qs)} | {statistics.mean(rr):.1f} | {statistics.median(rr):.0f} | {pct(rr, .9)} | {max(rr)} | "
              f"{sr/tot_r:.0%} | {st/tot_t:.0%} | {st/sr/1000:.0f}k | {tl:.1f} | {statistics.median(q['chars'] for q in qs):.0f}")
    print()
    print("応答数の分布（依頼の件数 / 応答の合計 / トークンの合計）")
    for lo, hi in ((1, 1), (2, 3), (4, 6), (7, 10), (11, 20), (21, 10**9)):
        qs = [q for q in rows if lo <= q["responses"] <= hi]
        label = f"{lo}" if lo == hi else (f"{lo}+" if hi == 10**9 else f"{lo}-{hi}")
        print(f"{label:>6} | {len(qs):4d} | {sum(q['responses'] for q in qs)/tot_r:4.0%} | {sum(q['tokens'] for q in qs)/tot_t:4.0%}")
    print()
    print("other の内訳（依頼文の長さ別）: 長さ | 件数 | 応答 平均 | ツール平均 | トークンの合計")
    oth = by.get("other", [])
    for lo, hi in ((0, 15), (16, 40), (41, 100), (101, 10**9)):
        qs = [q for q in oth if lo <= q["chars"] <= hi]
        if qs:
            print(f"{lo}-{hi} | {len(qs)} | {statistics.mean(q['responses'] for q in qs):.1f} | "
                  f"{statistics.mean(q['tools'] for q in qs):.1f} | {sum(q['tokens'] for q in qs)/1e6:.1f}M")
    if a.detail:
        detail(rows, tot_r, tot_t)
    if a.csv:
        with open(a.csv, "w", newline="\n", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["session", "ts", "kind", "chars", "responses", "tools", "peak", "tokens"])
            for q in rows:
                w.writerow([q["session"], q["ts"], q["kind"], q["chars"], q["responses"], q["tools"], q["peak"], q["tokens"]])


if __name__ == "__main__":
    main()
