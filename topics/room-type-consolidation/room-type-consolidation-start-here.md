# 窓口: room-type-consolidation

- 型: Project 型。完了条件: type 集約（`dev` と `inv`）に合わせて手順書の整合が取れ、type の考え方が `project-structure.md` に記載される（済み、2026-10-24）。実測を踏まえた見直しが残る。
- 何の取り組みか: `room open` の type が5つ（`doc` `dev` `dev-env` `dev-test` `research`）あったが、違いは成果物のサブディレクトリの組み合わせと調べ方だった。`dev` と `inv` の2つに集約した（実装済み、2026-10-24）。議論の叩き台は [[room-type-consolidation-notes]]。

## いま

type の集約は反映済み（2026-10-24）。10-31 に、room の GitHub 認証（読み取り専用 deploy key）を実機で確認し、works の再定義と開発リポジトリの置き場を決めた（`docs/decisions.md`）。詳細は `docs/log.md`。

## あなた待ち

なし。

## 次の一手

案 A の実装は済み（単体テストのみ）。実機の確認は、`src/` を含む 1 Project の実測にまとめる（`docs/log.md`）。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: [[room-type-consolidation-notes]]（type 集約の事実の表、論点）、[[room-type-consolidation-guide-review]]（guide の不整合と活動の対応）、`docs/log-history.md`（経緯）

## リポジトリに無いローカルの状態

なし。
