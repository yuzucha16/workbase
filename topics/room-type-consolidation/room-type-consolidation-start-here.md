# 窓口: room-type-consolidation

- 型: Project 型。完了条件: `dev-deliverable-guide.md` が、type 集約（`dev` と `inv`、構成要素）に合わせて見直され、承認される。
- 何の取り組みか: `room open` の type が5つ（`doc` `dev` `dev-env` `dev-test` `research`）あったが、違いは成果物のサブディレクトリの組み合わせと調べ方だった。`dev` と `inv` の2つに集約した（実装済み、2026-10-24）。議論の叩き台は [[room-type-consolidation-notes]]。

## いま

type の集約は実装して main に反映済み。次は `dev-deliverable-guide.md` の見直し（ユーザーが、区分が明文化された後にやると希望）。詳細は `docs/log.md`。

## あなた待ち

- `dev-deliverable-guide.md` の見直しに着手する時期。

## 次の一手

どこでも: `dev-deliverable-guide.md` を、構成要素（`src/` `env/` `tests/` `tools/` `docs/`）から必要なものを選ぶ形に組み直す。旧 `dev-env` `dev-test` の節は、差分でなく選び方にする。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: [[room-type-consolidation-notes]]（事実の表、論点、変更範囲）、`docs/log-history.md`（経緯）

## リポジトリに無いローカルの状態

なし。
