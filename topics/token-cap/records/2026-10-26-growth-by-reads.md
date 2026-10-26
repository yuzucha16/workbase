# 会話の伸びは「読み込み」で決まる（会話記録の実測、2026-10-26）

目的: ベーストークンとフックのどちらが支配的かを決める。ee の問い: 「ベーストークンを減らす、フックを減らす、いずれか支配的な方から」。

## 方法

PC2 の `~/.claude/projects/` の会話記録（直近 12 会話）から、応答ごとの入力量（input + cache_read + cache_creation）を取り、増分が大きい応答の直前のツール呼び出しを見た。`cap_meter.py` は集計だけで、増分の原因までは出ないため、一時の PowerShell で行った（道具化はしていない）。

## 結果

- 土台は固定で 27.7〜28.3k（`cap_meter.py` の土台と同じ）。ここから先の伸びは、すべて会話に残った読み込みと出力。
- 1 回の読み込みで増えた量（読んだファイル → 直後の増分）:

| 読んだもの | 増分 |
|---|---|
| `workflow-kit/docs-rules.md` 全文（24.6KB） | +11.5k、+11.8k、+6.7k（3 会話） |
| `exmem/exmem-index.md`（直前に Glob） | +16k |
| `topics/logbook-design/docs/log.md`（6.4KB。窓口の予算 4KB 超え） | +12.5k |
| `find_knowledge.py --triggers` の出力 | +8k |
| `guides/explain/review-hook-why.md`（10KB） | +7.7k |
| `workflow-kit/approval-screening.md`（2.9KB） ほか | +7.5k |

- 読んだ分は以後の全応答に乗る。`docs-rules.md` の 12k を 40 応答目に読むと、残り 40 応答で約 48 万。
- 日本語は約 0.47 トークン/バイト（24.6KB が約 12k）。KB × 0.47k で見積もれる。
- `hook-common.md` と `AGENTS.md` は「`docs-rules.md` はコミットと push の節だけ」と書くが、実際は 3 会話とも全文を読んでいた。節だけを読む仕組みが無い。

## ee の観察（同日）

- このセッション（フックを使っていない）は 1 応答目で 55k。`review 消化` は 2 応答目で 100k。「会話 `[les コミット残件と承認待ちの整理]`（10-26）」が 100k に届いた例。よってフックだけでなく `AGENTS.md` 経由の読み込みにも余地がある、という予想（ee）。
- このセッションの内訳（`cap_meter` の記録）: 土台 28.0k → 1 応答目の読み込みで 55.1k（`AGENTS.md` が指示した `docs/log.md`、窓口、`token-cap/docs/log.md`、`cap-meter-pc2.md`、`context-measure.md`、`hooks.md` 8.7KB と grep 3 回）。うち `hooks.md` と 2 つの records は AI の判断で読んだ分で、必須ではない。必須の最小は `README.md`（1.7KB）と `docs/log.md`（4KB）だけ。

## 読み取り

- ベース（土台 28k、うち自前で動かせるのは約 6k）より、読み込みの方が支配的。ただし土台は全応答に乗る固定費で、60k で切る運用では 63% を占める（`2026-10-26-cap-meter-pc2.md`）。切る運用が定着したら、土台と常駐の `AGENTS.md` の連鎖の効きが増す。
- 「フック」と「`AGENTS.md`」は別の入口から同じ構造に当たっている: 大きいファイルを全文で読む。直す対象は、(1) 大きい正本の分割（`docs-rules.md` から「コミットと push」を切り出す）、(2) 起動時に読む量の上限（`log.md` 4KB の予算を守る）、(3) AI が必須でない records まで読まない運用。

## 次の一手

別セッションで、`docs-rules.md` の「コミットと push」を別ファイルに切り出す（`workflow-kit/` の変更なので、ee の承認の上で。参照元は `AGENTS.md`、`hooks.md`、`hook-common.md`、`wrap-hook.md`）。会話 `[les コミット残件と承認待ちの整理]` と `review 消化` の 2 応答目で、何を読んで 100k に達したかを同じ方法で見る。
