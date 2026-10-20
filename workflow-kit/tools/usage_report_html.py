#!/usr/bin/env python3
"""usage_report.py の集計を、概要と詳細・分析の1枚の HTML にする（標準ライブラリだけ。外部通信なし。読み取り専用）。

概要: 直近の期間の合計・費用・キャッシュ読取率・セッション数と、期間ごとの推移。
詳細・分析: 期間ごとの 1件当たり（平均/中央値/最大/最小）、費用の内訳（トークン種別）、モデル別、プロジェクト別、
上位セッションの集中度、セッションの大きさの分布、上位セッションのランキング。

使い方: python usage_report_html.py [--by week|month] [--last N] [--top N] [--prices FILE] [--root DIR] [--out FILE]
  --out  出力先（既定 ~/usage-report.html）。題名に作業内容の断片が入るので、リポジトリの中に置かない（公開リポジトリに載せない）。
  単価表の既定は、このファイルの隣の usage_prices.json。
"""
import argparse
import html
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

from usage_report import KINDS, add, hit_rate, load, project_name, total, zero

LABEL = {"input": "入力", "output": "出力", "cache_read": "キャッシュ読取", "cache_write": "キャッシュ作成(5分)", "cache_write_1h": "キャッシュ作成(1時間)"}
COLOR = {"input": "#6b7fd7", "output": "#e0795a", "cache_read": "#4aa58a", "cache_write": "#c9a227", "cache_write_1h": "#9a6bb5"}
BUCKETS = [(0, 5e5, "〜50万"), (5e5, 2e6, "50万〜200万"), (2e6, 5e6, "200万〜500万"), (5e6, 1e7, "500万〜1000万"), (1e7, float("inf"), "1000万〜")]

CSS = """
body{font:14px/1.6 system-ui,"Yu Gothic UI",sans-serif;margin:0;background:#f6f7f9;color:#1f2430}
main{max-width:1000px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:18px;margin:36px 0 12px;border-bottom:2px solid #d8dce3;padding-bottom:4px}
h3{font-size:15px;margin:24px 0 8px}.sub{color:#677}.cards{display:flex;gap:12px;flex-wrap:wrap}
.card{background:#fff;border-radius:8px;padding:12px 16px;min-width:180px;flex:1;box-shadow:0 1px 2px #0002}
.card b{display:block;font-size:22px}.card span{color:#677;font-size:12px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:13px}th,td{padding:5px 8px;border-bottom:1px solid #e5e8ee;text-align:right}
th{background:#eef0f4;font-weight:600}td.l,th.l{text-align:left}.bar{height:12px;border-radius:2px;background:#6b7fd7;display:inline-block;vertical-align:middle}
.stack{display:flex;height:16px;border-radius:3px;overflow:hidden;background:#e5e8ee}.stack i{display:block;height:100%}
.legend span{margin-right:14px;font-size:12px}.legend i{display:inline-block;width:10px;height:10px;margin-right:4px;border-radius:2px}
.note{background:#fff8e1;border-left:4px solid #e0b23a;padding:8px 12px;margin:12px 0}ul.find li{margin:4px 0}
"""


def n(x):
    return f"{x:,.0f}"


def m(x):
    return f"{x / 1e6:,.1f}M"


def e(s):
    return html.escape(str(s))


def stats(per, prices):
    out = []
    for pk in sorted(per):
        sess = per[pk]
        tot, models, projects = zero(), {}, {}
        cost_kind = {k: 0.0 for k in KINDS}
        for s in sess.values():
            add(tot, s["u"])
            for mo, t in s["models"].items():
                models[mo] = models.get(mo, 0) + t
            projects[s["project"]] = projects.get(s["project"], 0) + total(s["u"])
        sizes = sorted(total(s["u"]) for s in sess.values())
        costs = sorted(s["cost"] for s in sess.values())
        out.append({"pk": pk, "sess": sess, "tot": tot, "all": total(tot), "cost": sum(costs), "sizes": sizes, "costs": costs,
                    "models": models, "projects": projects})
    return out


def stack(parts):
    s = sum(v for _, v in parts) or 1
    return '<div class="stack">' + "".join(f'<i title="{e(LABEL[k])} {v / s * 100:.1f}%" style="width:{v / s * 100:.2f}%;background:{COLOR[k]}"></i>' for k, v in parts if v) + "</div>"


def legend():
    return '<p class="legend">' + "".join(f'<span><i style="background:{COLOR[k]}"></i>{LABEL[k]}</span>' for k in KINDS) + "</p>"


def build(per, titles, prices, by, top):
    P = stats(per, prices)
    if not P:
        sys.exit("期間が無い")
    cur = P[-1]
    unit = "月" if by == "month" else "週"
    h = [f"<h1>Claude Code 使用量レポート</h1><p class='sub'>{unit}次 / 直近 {len(P)} 期間 / 生成 {datetime.now():%Y-%m-%d %H:%M} / 価格は概算（{e(prices.get('_source', '単価表') if prices else '未指定')}）</p>",
         "<div class='note'>題名・プロジェクト名に作業内容の断片が含まれます。このファイルを公開リポジトリや外部に置かないでください。</div>",
         "<h2>概要</h2>"]
    avg_sess = statistics.mean(cur["sizes"])
    cache_cost_share = (cur_cost_kind(cur, prices)["cache_read"] / cur["cost"] * 100) if prices and cur["cost"] else None
    cards = [(f"{cur['pk']}（最新の{unit}）", m(cur["all"]) + " tokens"), ("概算費用", f"${cur['cost']:,.2f}" if prices else "—"),
             ("セッション数", f"{len(cur['sess'])} 件"), ("キャッシュ読取率", hit_rate(cur["tot"])),
             ("1件当たり平均", m(avg_sess)), ("最大セッション", m(cur["sizes"][-1]))]
    h.append("<div class='cards'>" + "".join(f"<div class='card'><span>{e(a)}</span><b>{e(b)}</b></div>" for a, b in cards) + "</div>")
    h.append(f"<h3>{unit}ごとの推移</h3><table><tr><th class='l'>期間</th><th>合計</th><th></th><th>出力</th><th>費用</th><th>セッション</th><th>平均/件</th><th>最大/件</th><th>読取率</th></tr>")
    mx = max(p["all"] for p in P)
    for p in P:
        h.append(f"<tr><td class='l'>{e(p['pk'])}</td><td>{n(p['all'])}</td><td class='l'><span class='bar' style='width:{p['all'] / mx * 160:.0f}px'></span></td><td>{n(p['tot']['output'])}</td>"
                 f"<td>{'$%.2f' % p['cost'] if prices else '—'}</td><td>{len(p['sess'])}</td><td>{m(statistics.mean(p['sizes']))}</td><td>{m(p['sizes'][-1])}</td><td>{hit_rate(p['tot'])}</td></tr>")
    h.append("</table>")
    h.append("<h3>最新の期間の気づき</h3><ul class='find'>")
    ranked = sorted(cur["sess"].items(), key=lambda kv: -total(kv[1]["u"]))
    top5 = sum(total(s["u"]) for _, s in ranked[:5]) / cur["all"] * 100
    h.append(f"<li>上位5セッションで全体の {top5:.0f}% を占める（{len(cur['sess'])} 件中）。</li>")
    h.append(f"<li>トークンの {cur['tot']['cache_read'] / cur['all'] * 100:.0f}% はキャッシュ読取。出力は {cur['tot']['output'] / cur['all'] * 100:.1f}% で、量の多さは「長く続いた会話」で決まる。</li>")
    if cache_cost_share is not None:
        ck = cur_cost_kind(cur, prices)
        h.append(f"<li>費用の内訳は、キャッシュ読取 {cache_cost_share:.0f}% / 出力 {ck['output'] / cur['cost'] * 100:.0f}% / キャッシュ作成 {(ck['cache_write'] + ck['cache_write_1h']) / cur['cost'] * 100:.0f}% / 入力 {ck['input'] / cur['cost'] * 100:.0f}%。</li>")
    if len(P) >= 2:
        pv = P[-2]
        h.append(f"<li>前の{unit}（{e(pv['pk'])}）と比べて、合計は {((cur['all'] / pv['all']) - 1) * 100:+.0f}%、セッション数は {len(cur['sess']) - len(pv['sess']):+d} 件。"
                 f"（最新の期間は集計の途中なら少なく出る）</li>")
    h.append("</ul>")

    h.append("<h2>詳細・分析</h2>" + legend())
    for p in reversed(P):
        sess = p["sess"]
        h.append(f"<h3>{e(p['pk'])}</h3>")
        h.append(stack([(k, p["tot"][k]) for k in KINDS]))
        h.append("<table><tr><th class='l'>トークン種別</th><th>量</th><th>割合</th>" + ("<th>概算費用</th>" if prices else "") + "</tr>")
        ck = cur_cost_kind(p, prices) if prices else None
        for k in KINDS:
            h.append(f"<tr><td class='l'>{LABEL[k]}</td><td>{n(p['tot'][k])}</td><td>{p['tot'][k] / p['all'] * 100:.1f}%</td>" + (f"<td>${ck[k]:,.2f}</td>" if ck else "") + "</tr>")
        h.append("</table>")
        sizes = p["sizes"]
        h.append("<h3 style='font-size:13px'>セッション 1件当たり</h3><table><tr><th></th><th>平均</th><th>中央値</th><th>最大</th><th>最小</th></tr>"
                 f"<tr><td class='l'>トークン</td><td>{n(statistics.mean(sizes))}</td><td>{n(statistics.median(sizes))}</td><td>{n(sizes[-1])}</td><td>{n(sizes[0])}</td></tr>")
        if prices:
            c = p["costs"]
            h.append(f"<tr><td class='l'>概算費用</td><td>${statistics.mean(c):.2f}</td><td>${statistics.median(c):.2f}</td><td>${c[-1]:.2f}</td><td>${c[0]:.2f}</td></tr>")
        h.append("</table>")
        h.append("<h3 style='font-size:13px'>セッションの大きさの分布</h3><table><tr><th class='l'>合計トークン</th><th>件数</th><th>トークン合計</th><th>全体比</th>" + ("<th>費用</th>" if prices else "") + "</tr>")
        for lo, hi, name in BUCKETS:
            ss = [s for s in sess.values() if lo <= total(s["u"]) < hi]
            if ss:
                t = sum(total(s["u"]) for s in ss)
                h.append(f"<tr><td class='l'>{name}</td><td>{len(ss)}</td><td>{n(t)}</td><td>{t / p['all'] * 100:.0f}%</td>" + (f"<td>${sum(s['cost'] for s in ss):,.2f}</td>" if prices else "") + "</tr>")
        h.append("</table>")
        for title, cols in (("モデル別", p["models"]), ("プロジェクト別（上位8）", p["projects"])):
            h.append(f"<h3 style='font-size:13px'>{title}</h3><table>")
            for k, v in sorted(cols.items(), key=lambda x: -x[1])[:8]:
                h.append(f"<tr><td class='l'>{e(project_name(k) if 'プロ' in title else k)}</td><td>{n(v)}</td><td>{v / p['all'] * 100:.0f}%</td><td class='l'><span class='bar' style='width:{v / p['all'] * 200:.0f}px'></span></td></tr>")
            h.append("</table>")
        h.append(f"<h3 style='font-size:13px'>上位 {top} セッション（合計トークン順）</h3><table><tr><th>#</th><th>合計</th><th>出力</th><th>読取率</th><th>応答</th>" + ("<th>費用</th>" if prices else "") + "<th class='l'>プロジェクト</th><th class='l'>題名</th><th class='l'>ID</th></tr>")
        for i, (sid, s) in enumerate(sorted(sess.items(), key=lambda kv: -total(kv[1]["u"]))[:top], 1):
            t = titles.get(sid) or "(題名なし)"
            h.append(f"<tr><td>{i}</td><td>{n(total(s['u']))}</td><td>{n(s['u']['output'])}</td><td>{hit_rate(s['u'])}</td><td>{s['n']}</td>" + (f"<td>${s['cost']:.2f}</td>" if prices else "")
                     + f"<td class='l'>{e(project_name(s['project']))}</td><td class='l'>{e(t[:60])}</td><td class='l'>{sid[:8]}</td></tr>")
        h.append("</table>")
    h.append("<h2>数え方</h2><ul><li>1つの API 応答は JSONL の複数行に同じ usage で繰り返されるため、message.id + requestId で1回だけ数える。サブエージェントは親のセッションに含める。</li>"
             "<li>期間はローカル時刻の各応答の時刻で決める（週は月曜始まり）。セッションが期間をまたぐと、期間ごとに分かれて数える。</li>"
             "<li>キャッシュ読取率 = 読取 ÷（入力 + 読取 + 作成）。費用は単価表の概算で、突合先（ccusage）と近いが完全一致ではない。</li></ul>")
    return f"<!doctype html><html lang='ja'><meta charset='utf-8'><title>Claude Code 使用量レポート</title><style>{CSS}</style><body><main>{''.join(h)}</main></body></html>"


def cur_cost_kind(p, prices):
    """トークン種別ごとの概算費用（モデルごとの単価で計算するため、セッションのモデル比率で按分する）。"""
    out = {k: 0.0 for k in KINDS}
    if not prices:
        return out
    for s in p["sess"].values():
        t = sum(s["models"].values()) or 1
        for mo, mt in s["models"].items():
            pr = next((v for name, v in prices.items() if not name.startswith("_") and mo.startswith(name)), None)
            if pr:
                for k in KINDS:
                    out[k] += s["u"][k] * mt / t * pr.get(k, 0) / 1e6
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--by", choices=("week", "month"), default="week")
    ap.add_argument("--last", type=int, default=4)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--prices", default=str(Path(__file__).resolve().parent / "usage_prices.json"))
    ap.add_argument("--root", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--out", default=str(Path.home() / "usage-report.html"))
    a = ap.parse_args()
    root = Path(a.root)
    if not root.is_dir():
        sys.exit(f"ログの場所が無い: {root}")
    pf = Path(a.prices)
    prices = json.loads(pf.read_text(encoding="utf-8")) if pf.is_file() else None
    per, titles = load(root, a.by, prices)
    per = {k: per[k] for k in sorted(per)[-a.last:]}
    Path(a.out).write_text(build(per, titles, prices, a.by, a.top), encoding="utf-8")
    print(f"書き出した: {a.out}")


if __name__ == "__main__":
    main()
