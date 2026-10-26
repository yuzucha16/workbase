#!/usr/bin/env python3
"""月次の上限（量で数える）に対する消費と、会話の切り方・土台の大きさを、Claude Code の会話記録（jsonl）から出す（標準ライブラリだけ。読み取り専用）。

出す内容: 当月の合計（上限に対する割合、日割り、月末の見込み、残りの1日あたりの枠）、直近の日ごとの合計、
切る目安 --cut を超えた応答の割合とそのトークンの割合、会話の土台（各会話の最初の応答の大きさ）の分布。
1回の応答の大きさ = input + output + cache_read + cache_write（Zed の表示 `used` と同じ数え方）。上限への算入 = 全応答の大きさの合計。
上限の数え方（読みを含むか）は勤務先の案内で確かめる。違うときは、usage_report.py の種別ごとの量で読み替える。

使い方: python -I cap_meter.py [--budget 200000000] [--cut 60000] [--month YYYY-MM] [--days 7] [--latest] [--root DIR]
  --latest  月の集計の代わりに、いちばん新しい会話（最後の応答の時刻が最新）の 応答数・積算・いまの大きさ・土台 だけを出す（`wrap` の前に見る用）
数え方: 1つの応答は jsonl の複数行に分かれるので、message.id + requestId で1回だけ数える。サブエージェントも合計に含める。
ログは作業内容を含むので、出力は数字だけ（題名は出さない）。プロジェクト名は出さない。
"""
import argparse
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def read(root):
    seen = {}
    for f in root.rglob("*.jsonl"):
        try:
            fh = f.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message")
                if d.get("type") != "assistant" or not isinstance(m, dict):
                    continue
                u, ts, sid = m.get("usage"), d.get("timestamp"), d.get("sessionId")
                if not u or not ts or not sid:
                    continue
                n = sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                if not n:
                    continue
                key = (m.get("id"), d.get("requestId")) if m.get("id") else (d.get("uuid"),)
                seen[key] = (sid, ts, n, bool(d.get("isSidechain")))
    return list(seen.values())


def local(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()


def pct(a, b):
    return f"{a / b * 100:.0f}%" if b else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=200_000_000)
    ap.add_argument("--cut", type=int, default=60_000)
    ap.add_argument("--month", default=datetime.now().strftime("%Y-%m"))
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--root", default=str(Path.home() / ".claude" / "projects"))
    a = ap.parse_args()

    rows = [(sid, local(ts), n, side) for sid, ts, n, side in read(Path(a.root))]
    if a.latest:
        if not rows:
            raise SystemExit("応答が無い")
        sid = max(rows, key=lambda r: r[1])[0]
        mine = sorted((r for r in rows if r[0] == sid), key=lambda r: r[1])
        main_rows = [r for r in mine if not r[3]] or mine
        print(f"最新の会話 [{sid[:8]}]: 応答 {len(mine)}、積算 {sum(r[2] for r in mine):,}、いまの大きさ {main_rows[-1][2]:,}、土台 {main_rows[0][2]:,}、開始 {mine[0][1]:%m-%d %H:%M}")
        return
    rows = [r for r in rows if r[1].strftime("%Y-%m") == a.month]
    if not rows:
        raise SystemExit(f"{a.month} の応答が無い")
    tot = sum(r[2] for r in rows)
    y, mo = map(int, a.month.split("-"))
    nxt = datetime(y + (mo == 12), mo % 12 + 1, 1)
    dim = (nxt - datetime(y, mo, 1)).days
    last = max(r[1] for r in rows)
    elapsed = last.day if last.strftime("%Y-%m") == a.month else dim
    per_day = tot / elapsed
    print(f"【{a.month}】合計 {tot:,}（上限 {a.budget:,} の {pct(tot, a.budget)}）  会話 {len({r[0] for r in rows})}  応答 {len(rows):,}")
    print(f"  経過 {elapsed}/{dim} 日、1日平均 {per_day:,.0f}、月末の見込み {per_day * dim:,.0f}（上限の {pct(per_day * dim, a.budget)}）")
    if elapsed < dim:
        print(f"  残り {dim - elapsed} 日の枠: 1日あたり {max(a.budget - tot, 0) / (dim - elapsed):,.0f}")

    day = defaultdict(int)
    for _, dt, n, _ in rows:
        day[dt.strftime("%m-%d")] += n
    print(f"直近 {a.days} 日（日ごと）: " + "  ".join(f"{k} {v / 1e6:.1f}M" for k, v in sorted(day.items())[-a.days:]))

    over = [r for r in rows if r[2] > a.cut]
    print(f"切る目安 {a.cut:,} を超えた応答: {len(over):,} 件（応答の {pct(len(over), len(rows))}）、トークンの {pct(sum(r[2] for r in over), tot)}")

    first = {}
    for sid, dt, n, side in rows:
        if not side and (sid not in first or dt < first[sid][0]):
            first[sid] = (dt, n)
    base = sorted(v[1] for v in first.values())
    if base:
        q = lambda p: base[min(len(base) - 1, int(len(base) * p))]
        print(f"会話の土台（最初の応答の大きさ）: 中央値 {int(statistics.median(base)):,}、上位10% {q(0.9):,}、最小 {base[0]:,}、最大 {base[-1]:,}（{len(base)} 会話）")
        print(f"  土台が全応答に占める量の目安: 土台の中央値 × 応答数 = {int(statistics.median(base)) * len(rows):,}（合計の {pct(int(statistics.median(base)) * len(rows), tot)}）")


if __name__ == "__main__":
    main()
