# 効果確認 PC2 Windows 側（2026-11-05）

PC2 の Windows 側の会話記録で、`repeat_reads.py` と `requests_by_kind.py` を 2 通りの `--since` で実行した（AI が実行）。方針（ee の決定 11-05）: 主戦場だけを測る（PC1 = room、PC2 = Windows）。反対側は動作確認のみのため除外。PC1 と PC2 は合算も直接比較もしない。`--since 10-27` は 100k 運用全体、`--since 10-30` は 10-29 の縮小・wrap-hook・AGENTS.md 2 行の効果。

## 1. 全文読みの縮小（`repeat_reads.py`。1 回あたりの文字数）

| ファイル | 基準（10-01〜。縮小前後が混在） | 10-27〜 | 10-30〜 | 判定 |
|---|---|---|---|---|
| docs/log.md | 3,831（173 回） | 2,354（175 回） | 2,149（86 回） | 下がった |
| commit-push-rules.md | 5,895（51 回） | 4,258（115 回） | 3,154（53 回） | 下がった |
| wrap-hook.md | 2,630（100 回） | 3,383（115 回） | 3,803（55 回） | 上がった（原因未確認） |
| docs-rules.md | 11,289（27 回） | 3,969（11 回） | 上位 15 に無い | 下がった。回数も減った |
| stock-hook.md | 8,503（17 回） | 8,954（5 回） | 8,777（2 回） | 変わらず（読みの数が少ない） |
| hook-common.md | 6,304（21 回） | 6,307（7 回） | 6,360（4 回） | 変わらず |

- 全体: 全文読みの割合は 56% → 57%。重複読みは 12% → 10%。
- wrap-hook.md の 1 回あたりが上がった原因は、ファイルの増加（`git log` で確認）。5,960 バイト（10-29 の縮小直後）→ 7,693（同日、応答のまとめ方を追加）→ 8,267（11-02）。縮小ではなく増量されていた。応答は 8.2 → 6.7 に減ったので、読みが増えた分は元を取れているが、読みの量は縮小の効果として数えない。
- `docs-format.md` は 10-30 以降の上位 15 に無い。wrap が読んで増えたという兆候はない（上位 15 の範囲での判断）。

## 2. 依頼別（`requests_by_kind.py`。CSV から区間別に集計）

| 区間 | 全体 応答/件 | 全体 1 件 | wrap 応答 | wrap 1 件 | integrate 件数・応答・1 件 |
|---|---|---|---|---|---|
| 〜10-26 | 6.2（426 件） | 574k | 8.2（60 件） | 882k | 13 件・9.4・809k |
| 10-27〜29 | 5.8（300 件） | 323k | 7.7（68 件） | 535k | 3 件・11.0・708k |
| 10-30〜 | 6.2（354 件） | 384k | 6.7（73 件） | 501k | 5 件・7.0・396k |

- **100k 運用（10-27〜）**: 全体の 1 件あたりが 574k → 323k〜384k（−33〜44%）、ピーク平均が 89k → 55〜65k。応答数は変わらず、文脈の大きさが下がったことが主因。
- **wrap-hook 見直し（10-30〜）**: 応答 8.2 → 6.7、1 件 882k → 501k。目標だった「8.3 から下げる」は達成。ただし 10-27〜29 の時点で 7.7 まで下がっており、見直し単独の効果は応答 −1.0、1 件 −34k 程度で、100k 運用との分離は難しい。
- **AGENTS.md の 2 行**: 全体の応答平均は 5.8 → 6.2 と上がり、効果は見えない。他の要因（continue 4.9 → 7.8 など）に埋もれる。判定保留。
- **integrate の上限**: 10-27 以降は 8 件。応答 7.0、1 件 396k に下がったが、件数が少ない。保留（判定には 10-29 時点の 3 件からほとんど増えていない）。
- continue は応答が 4.9 → 6.0 → 7.8 と増加傾向（1 件 246k → 323k）。要注意。件数 41 で、最初の依頼が 40 件（応答 7.9）。

## 3. 判断（案）

- 縮小は log・commit-push-rules・docs-rules で効いた。wrap-hook は原因の切り分けが先。stock-hook・hook-common は動いていないので、次の縮小候補。
- 応答数を減らす施策（NA 5 の (b)(g)(h)）の効果は、この区間では見えない。PC1 の結果を見てから判断する。
- continue の増加を NA 5 の (b) の優先に入れるかは、PC1 の結果で決める。

PC1（room）は 11-06 に同じ手順で実行する。基準（前の区間）は、room の会話記録が 10-21 以降のため 10-21〜10-26 で切る。

## PC1（room）で実行するコマンド（11-06。workbase を pull したあと、リポジトリのルートで）

`repeat_reads.py` の `--since` は会話記録の更新日（終了日は指定できない）。前の区間は `--since 10-21`（縮小前後が混在の基準）で代える。依頼別は CSV を出し、集計で区間を切る。

```
python3 -I workflow-kit/tools/repeat_reads.py --since 2026-10-21 --detail 15
python3 -I workflow-kit/tools/repeat_reads.py --since 2026-10-27 --detail 15
python3 -I workflow-kit/tools/repeat_reads.py --since 2026-10-30 --detail 15
python3 -I workflow-kit/tools/requests_by_kind.py --since 2026-10-27 --detail
python3 -I workflow-kit/tools/requests_by_kind.py --since 2026-10-30 --detail
python3 -I workflow-kit/tools/requests_by_kind.py --since 2026-10-21 --csv /tmp/rbk.csv > /dev/null
python3 -I - <<'PY'
import csv,statistics as st
r=list(csv.DictReader(open('/tmp/rbk.csv',encoding='utf-8')))
def grp(f,k=None):
    x=[a for a in r if f(a['ts'][:10]) and (k is None or a['kind']==k)]
    if not x: return 'n=0'
    return f"n={len(x)} resp={st.mean(int(a['responses']) for a in x):.1f} tok={st.mean(int(a['tokens']) for a in x)/1000:.0f}k peak={st.mean(int(a['peak']) for a in x)/1000:.0f}k"
for k in [None,'wrap','integrate','other','continue']:
    print(k)
    print(' <10-27',grp(lambda d:d<'2026-10-27',k))
    print(' 10-27~29',grp(lambda d:'2026-10-27'<=d<'2026-10-30',k))
    print(' >=10-30',grp(lambda d:d>='2026-10-30',k))
PY
```

出力は貼る。`python3` が無ければ `python`。
