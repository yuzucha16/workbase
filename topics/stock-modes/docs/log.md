# 作業ログ（log）

`stock` のモード追加（`stock 理解` / `stock ナレッジ`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。2026-10-21 に `planning-method` から切り出した。

## Next Actions

1. 進行中: 6R・憲章・WBS・マイルストーンは作成済み（2026-10-20。`records/stock-modes-*.md`）。M1（設計の確認）は途中: 出力先・モード名・引数なし（「両方」なし）・更新は対象外・`find-knowledge` 対応は不要、までユーザーが決めた（`docs/decisions.md`）。残りの【提案】（`kind` の値、6見出し、`integrate` の変換、`check-inbox` の分岐、権限は変えない）は未確認。見本は `records/explain-inbox-example.md`。その後 M2 で `workflow-kit/` を書き換える（承認が要る）。`room.py` が `kind` をそのまま運ぶかは未確認。
2. 6R へのフィードバック（`records/stock-modes-6r.md` の末尾。`start-plan.md` への案6件）は未承認。`review 消化` で扱う。

## Open Questions

- `stock-modes-plan.md` の WBS 1.4.1（通し試験）の結果の置き場が、`kit-growth/records/planning-method-record.md` を指している。`records/` は2か所（測ったことは `kit-growth/records/`、各トピックの出力はそのトピックの `records/`）にした（2026-10-21、`private-knowledge` の決定）ので、見直す（`stock-modes-plan.md` の WBS 1.4.1 は直した）。
- `private-knowledge`（会議録のナレッジ化）の流れと、どこで重なるか（あちらの裏づけ #5）。
