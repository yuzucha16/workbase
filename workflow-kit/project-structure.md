# Project の構造

`open-hook.md` から移した（2026-10-17、ユーザーの承認。本文は原文のまま）。`open` の手順（対象の決定、検査、聞き取り、下書き）は `open-hook.md`。

2026-10-08 ユーザーが承認。2026-10-16 に、AI 作業部屋の構造（`ai/` と `_noai/`）への対応に書き直した（ユーザーが承認）。

すべての Project は AI 作業部屋で行う（部屋の外の読み替えは持たない）。type ごとの違いは、**成果物の中身と、`ai/` のどこに何を置くか**だけ。`ai/` と `_noai/` の中身は `room open` が作る（`workflow-kit/room/README.md`）。`ai/` 直下の5つは `room open` が先に作る。その下は、空のディレクトリを先に作らず、最初のファイルが来たときに作る。深さは `ai/out/<成果物名>/` の下まで数えて2階層以内（`src/` の中身などは対象外）。

固定の核（全 type 共通）:

| パス | 内容 | 部屋の AI |
|---|---|---|
| `README.md` | frontmatter と、目的・完了条件・成果物・範囲外・Open Questions | 読むだけ（`ai/ctx/` の写し） |
| `ai/docs/` | 作業の記録だけ。`log.md` と `decisions.md` | 読み書き |
| `ai/in/` | 人が渡す入力（マスク済み、または人が `--adopt` で確認したもの）。部屋では読み取り専用 | 読むだけ |
| `ai/work/` | 中間成果物、下書き、使い捨てのスクリプト | 読み書き |
| `ai/out/` | 最終成果物 `<成果物名>/`。予約名: `readme-draft.md` `close.md` `stock/`（成果物の名前にしない） | 読み書き |
| `ai/records/` | 実行記録、AI への指示の記録 | 読み書き |
| `_noai/` | 原本 `raw/`、対応表 `map/`、復元済みの成果物 `final/`、`mask.toml`、人だけの仮置き `user/`。`data:`（`none` / `mask` / `restore`）に応じて作る（`room/README.md`）。追跡しない | 見えない |

種類別の置き場（同じ表を、`ai/` の下に読み替えたもの。旧: `drafts/` `refs/` `src/` `sources/` `report.md`）:

| type | `ai/in/` | `ai/work/` | `ai/out/<成果物名>/` |
|---|---|---|---|
| `doc`（手順書・仕様・設計・チェックリスト） | 旧 `refs/`: 渡された資料、チェックリスト | 旧 `drafts/`: 版ごとの下書き、レビュー版 | 最終版の文書 |
| `dev`（設計・実装・評価） | 参考資料、マスク済みの入力 | 中間物、使い捨てのスクリプト | `src/` `tests/` `tools/`、ビルド設定、文書。構成は `dev-deliverable-guide.md` |
| `dev-env`（環境構築） | 対象環境の情報（OS、既存の道具と版の一覧。マスク済み）、既存の手順書 | 試行のログ、調べ途中のメモ、使い捨てのスクリプト | 環境定義（セットアップのスクリプト、コンテナ定義、版の固定）、確認スクリプト、文書。構成は `dev-deliverable-guide.md` の「`dev-env` と `dev-test`」 |
| `dev-test`（テスト） | テスト対象（ソースのスナップショット）と、その要求仕様 | 試しのテスト、失敗の切り分け | `tests/` `tools/`、テスト仕様、`report.md`（実行結果）。構成は同上 |
| `research`（調査） | 旧 `sources/` のうち、人が渡した資料 | 旧 `sources/` のうち、AI が集めた資料と抜粋。調べ途中の整理 | `report.md`（結論） |

基準文書（`exmem/lessons/change-method.md`。変更の設計と検証の物差しになる、AI が読めるテキスト。人と AI の工程の境界）:

- 置き場は、成果物と同じ `ai/out/<成果物名>/`（全 type 共通）。`dev` は、成果物の `docs/` の3文書（要求仕様・機能仕様・運用マニュアル）が兼ねる。`dev-env` は環境の要求仕様、`dev-test` はテスト仕様が兼ねる（`dev-deliverable-guide.md`）。
- `ai/work/` の下書きや使い捨てのスクリプトとは別物。`ai/docs/`（作業の記録）にも入れない。
- 前の Project の基準文書を次の Project に渡すときは、人が次の Project の `ai/in/` に置き、`room start --adopt` で入力として記録する。
- 設計メモ（design、coding-rules）は `ai/docs/`。下書きは `ai/docs/` に入れない（`ai/docs/` を「作業の記録」の意味だけにする）。
- `ai/in/` は部屋では読み取り専用なので、AI が集めた資料は `ai/work/` に置く。
- `research` の「実測が無い。叩き台」は変わらない。
