# 作業ログ（log）

`stock` のモード追加（`stock 理解` / `stock ナレッジ`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。2026-10-21 に `planning-method` から切り出した。

## 状態

M1〜M3 を 2026-10-21 に通した（ユーザーが設計の【提案】を一括承認）。`workflow-kit/` に `stock 理解` を実装し、点検スクリプト（py・ps1）と単体テストで確認した。コミットは未了なら下の1。詳細は `docs/decisions.md` の同日の項。

## Next Actions

1. 実機で通す: `stock 理解` で下書きを作り、`integrate` で `guides/explain/` に入れる（実際の理解ガイドの題材で。本物のファイルができるので、使うときに行う）。`room stock` の実機も同じ。通ったらトピックを閉じる（`topics/AGENTS.md`）。
2. （済 2026-10-21）設計からの差分4件はユーザーが承認した。
3. フィードバック（`topics/planning-method/planning-method-feedback-stock-modes-m1.md`）の案8件は未承認。`review 消化` で扱う。6R 末尾の6件も同じ。

## Open Questions

- `stock-modes-plan.md` の WBS 1.4.1 の結果の置き場（解決済み: 結果は `decisions.md` に書いた）。計画の置き場の見直しは `planning-method` 側。
- 使われなければ `kind: explain` の分岐を外して戻す（履歴は git。見直しの条件は `decisions.md`）。
