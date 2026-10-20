#!/usr/bin/env python3
"""Claude Code のセッションログ（JSONL）から、トークン使用量を週次・月次で振り返る（標準ライブラリだけ。読み取り専用）。

出す内容: 期間ごとの合計・セッション数・セッション当たりの平均/最大/最小・キャッシュ読取率・モデル別・プロジェクト別、
期間内の上位セッションのランキング。価格($)は --prices で単価表（JSON）を渡したときだけ出す（単価は改定されるので、このスクリプトには持たない）。

使い方: python usage_report.py [--by week|month] [--last N] [--top N] [--sort total|output|cost] [--prices FILE] [--root DIR]
  --by     期間の単位（既定 week。月曜始まり、ローカル時刻）
  --last   直近 N 期間だけ出す（既定 4）
  --top    期間ごとのランキング件数（既定 5）
  --sort   ランキングの基準（既定 total = 全トークン）
  --prices 単価表 JSON。{"モデル名の前方一致": {"input":x,"output":x,"cache_read":x,"cache_write":x,"cache_write_1h":x}}（"_" で始まるキーは注記） （$ / 100万トークン）
  --root   ログの場所（既定 ~/.claude/projects）

数え方: 1つの API 応答は JSONL の複数行に分かれて同じ usage が繰り返されるので、message.id + requestId で1回だけ数える。
サブエージェントのログ（subagents/）も、親と同じ sessionId に含める。ログは個人の作業内容を含むので、出力を公開リポジトリに貼らない。
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

KINDS = ("input", "output", "cache_read", "cache_write", "cache_write_1h")   # cache_write は 5分、cache_write_1h は 1時間のキャッシュ作成


def read_messages(root):
    """(session, project, model, timestamp, usage dict) を重複なしで返す。session のタイトルも別に集める。"""
    seen = {}
    titles = {}
    for f in root.rglob("*.jsonl"):
        project = f.relative_to(root).parts[0]
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
                sid = d.get("sessionId")
                if not sid:
                    continue
                if d.get("type") == "user" and sid not in titles and not d.get("isSidechain") and not d.get("isMeta"):
                    t = user_text(d)
                    if t:
                        titles[sid] = t
                m = d.get("message")
                if d.get("type") != "assistant" or not isinstance(m, dict):
                    continue
                u = m.get("usage")
                ts = d.get("timestamp")
                if not u or not ts:
                    continue
                key = (m.get("id"), d.get("requestId")) if m.get("id") else (d.get("uuid"),)
                w_all = u.get("cache_creation_input_tokens") or 0
                w_1h = min(w_all, (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens") or 0)
                seen[key] = (sid, project, m.get("model") or "?", ts, {
                    "input": u.get("input_tokens") or 0,
                    "output": u.get("output_tokens") or 0,
                    "cache_read": u.get("cache_read_input_tokens") or 0,
                    "cache_write": w_all - w_1h,
                    "cache_write_1h": w_1h,
                })
    return list(seen.values()), titles


def user_text(d):
    c = (d.get("message") or {}).get("content")
    if isinstance(c, list):
        c = next((b.get("text") for b in c if isinstance(b, dict) and b.get("type") == "text"), None)
    if not isinstance(c, str):
        return None
    c = " ".join(c.split())
    if not c or c.startswith("<"):   # <command-name> や <system-reminder> などの自動挿入は題名にしない
        return None
    return c


def period_key(ts, by):
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
    if by == "month":
        return dt.strftime("%Y-%m")
    monday = (dt - timedelta(days=dt.weekday())).date()
    return monday.strftime("%Y-%m-%d") + "~"


def total(u):
    return sum(u[k] for k in KINDS)


def add(a, b):
    for k in KINDS:
        a[k] += b[k]


def zero():
    return {k: 0 for k in KINDS}


def cost(u, model, prices):
    if not prices:
        return None
    for name, p in prices.items():
        if not name.startswith("_") and model.startswith(name):
            return sum(u[k] * p.get(k, 0) for k in KINDS) / 1e6
    return None


def fmt(n):
    return f"{n:,.0f}"


def hit_rate(u):
    d = u["input"] + u["cache_read"] + u["cache_write"] + u["cache_write_1h"]
    return f"{u['cache_read'] / d * 100:.0f}%" if d else "-"


def short(s, n=36):
    s = s or "(題名なし)"
    return s if len(s) <= n else s[: n - 1] + "…"


def project_name(p):
    return re.sub(r"^[A-Za-z]--Users-[^-]+-(works-)?", "", p) or p   # ログのフォルダ名（cwd の / と : を - にしたもの）から、ホームまでを落とす


def load(root, by, prices):
    """期間 -> セッション -> {u: トークン, cost, project, models, n} と、セッションの題名を返す。"""
    msgs, titles = read_messages(root)
    if not msgs:
        sys.exit("集計できるメッセージが無い")
    per = defaultdict(lambda: defaultdict(lambda: {"u": zero(), "cost": 0.0, "project": "", "models": defaultdict(int), "n": 0}))
    for sid, project, model, ts, u in msgs:
        if not total(u):   # <synthetic>（エラー応答など）は使用量が 0
            continue
        s = per[period_key(ts, by)][sid]
        add(s["u"], u)
        s["project"] = project
        s["models"][model] += total(u)
        s["n"] += 1
        s["cost"] += cost(u, model, prices) or 0.0
    return per, titles


def main():
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--by", choices=("week", "month"), default="week")
    ap.add_argument("--last", type=int, default=4)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--sort", choices=("total", "output", "cost"), default="total")
    ap.add_argument("--prices")
    ap.add_argument("--root", default=str(Path.home() / ".claude" / "projects"))
    a = ap.parse_args()

    root = Path(a.root)
    if not root.is_dir():
        sys.exit(f"ログの場所が無い: {root}")
    prices = json.loads(Path(a.prices).read_text(encoding="utf-8")) if a.prices else None
    if a.sort == "cost" and not prices:
        sys.exit("--sort cost には --prices が要る")

    per, titles = load(root, a.by, prices)

    for pk in sorted(per)[-a.last:]:
        sess = per[pk]
        tot, models, projects = zero(), defaultdict(int), defaultdict(int)
        for s in sess.values():
            add(tot, s["u"])
            for m, n in s["models"].items():
                models[m] += n
            projects[s["project"]] += total(s["u"])
        sizes = sorted(total(s["u"]) for s in sess.values())
        avg = sum(sizes) / len(sizes)
        median = sizes[len(sizes) // 2]
        print(f"■ {pk}  ({'月' if a.by == 'month' else '週'}次)")
        line = f"  合計 {fmt(total(tot))}  (入力 {fmt(tot['input'])} / 出力 {fmt(tot['output'])} / キャッシュ読取 {fmt(tot['cache_read'])} / キャッシュ作成 {fmt(tot['cache_write'] + tot['cache_write_1h'])})  キャッシュ読取率 {hit_rate(tot)}"
        if prices:
            line += f"  概算 ${sum(s['cost'] for s in sess.values()):,.2f}"
        print(line)
        print(f"  セッション {len(sess)} 件  1件当たり: 平均 {fmt(avg)} / 中央値 {fmt(median)} / 最大 {fmt(sizes[-1])} / 最小 {fmt(sizes[0])}")
        print("  モデル別: " + ", ".join(f"{m} {fmt(n)} ({n / total(tot) * 100:.0f}%)" for m, n in sorted(models.items(), key=lambda x: -x[1])))
        print("  プロジェクト別: " + ", ".join(f"{project_name(p)} {fmt(n)} ({n / total(tot) * 100:.0f}%)" for p, n in sorted(projects.items(), key=lambda x: -x[1])[:5]))
        keyf = {"total": lambda kv: total(kv[1]["u"]), "output": lambda kv: kv[1]["u"]["output"], "cost": lambda kv: kv[1]["cost"]}[a.sort]
        print(f"  上位 {a.top} セッション（{a.sort} 順）:")
        for i, (sid, s) in enumerate(sorted(sess.items(), key=keyf, reverse=True)[: a.top], 1):
            c = f"  ${s['cost']:,.2f}" if prices else ""
            print(f"   {i}. {fmt(total(s['u'])):>12}  出力 {fmt(s['u']['output']):>9}  読取率 {hit_rate(s['u']):>4}  応答 {s['n']:>4}{c}  {project_name(s['project'])[:18]:<18} {short(titles.get(sid))}  [{sid[:8]}]")
        print()
    if not prices:
        print("価格($)は未表示。--prices 単価表.json で概算を出せる（単価の出典と取得日は単価表の側に残す）。")


if __name__ == "__main__":
    main()
