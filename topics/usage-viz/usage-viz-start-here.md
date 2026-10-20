# 窓口: usage-viz（トークン・コスト可視化）

- 型: Project 型。完了条件: セッション単位のトークン・価格・キャッシュ利用を CLI で集計・順位付け・傾向表示できる（合計が突合先と ±5% 以内）。達成済み（2026-10-20）。
- 何の取り組みか: 使用量が多い条件を見つけ、使い方の見直しに使う。計画のやり方（`planning-method`）の試行の題材で、kit 以外の初の題材。計画は `records/` の [[usage-viz-6r]]、[[usage-viz-plan]]、[[usage-viz-plan-notes]]。ツールは `workflow-kit/tools/usage_report.py` ほか、使い方は `guides/howto/claude-usage-report.md`。2026-10-21 に `planning-method/records/` から切り出した。

## いま

実装まで終わった（2026-10-20）。残りは実行後のフィードバックの扱いと、HTML の見た目の確認。詳細は `docs/log.md`。

## あなた待ち

- HTML の見た目の確認（ブラウザで開いていない）。トピックを閉じてよいかの判断。

## 次の一手

HTML をブラウザで開いて確認する。PC。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: [[usage-viz-plan]]（計画）、`docs/log-history.md`（経緯）

## リポジトリに無いローカルの状態

なし（突合に使った `ccusage` は `npx` で実行）。
