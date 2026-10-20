# 作業ログ（log）

トークン・コスト可視化の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。2026-10-21 に `planning-method` から切り出した。

## Next Actions

1. HTML の見た目をブラウザで確認する（未確認。自動テストは無い）。
2. トピックを閉じる判断（完了条件は達成済み。`topics/AGENTS.md` の「トピックを終わらせるとき」）。【汎用】は `docs/decisions.md` に無いが、実装で見つかった落とし穴（1つの API 応答がログの複数行に繰り返される、キャッシュ作成が5分と1時間に分かれる）は `log-history.md` にある。`guides/howto/claude-usage-report.md` に反映済みか見る。
3. （済 2026-10-20）実行後のフィードバックは `records/usage-viz-*.md` の末尾にあり、ユーザーの指示で `workflow-kit/start-plan.md` に反映した。効果は `planning-method` の品質チェックで見る。

## Open Questions

- 上限3つのため、10-23 以降の作業（運用の手順書）を M3 に束ねた件（この題材1件に限り可）。一般の条件は未決で、`planning-method` の Open Questions にある。
