# `open` フック

呼び出し名は `open`（Project の開始）。別名は無い。呼び出し表の正本は `hooks.md`（体系の経緯は `README.md` の「フックの体系」）。

実測で直して育てる。

## 目的と契機

- **目的**: `open` は Project の主題と完了条件を決めて、README 本文を下書きする。続けて `start`（`start-hook.md`）を呼び、その日のゴールと前提を決める。ひな形（`README.md`、`ai/`、`_noai/`）、Area の一覧、状態、コミットは、人が行う `room open` / `room readme` の責務で、この手順書は持たない（`room-context.md`、`room/README.md`）。
- **契機**: Project を新しく始めるときに、ユーザーが言う、または `start` が、進行中の Project が無いと判断したときに案内する。小さな再開では、`open` は不要。
- **前提**: ワークスペース（PARA 構成。`areas/` `projects/` `archives/`）があり、人が `room open <名>` で Project のひな形を作ってある。

## 場所と書き込みの制約

- 書き込み先は、`ai/out/readme-draft.md`（README の本文だけ。frontmatter を含めない）と、呼び出し元の記録（`ai/docs/log.md`、`ai/docs/decisions.md`、`events`。手順「記録する」）だけ。Project と Area の `README.md` は書き込めない（`ai/ctx/` の写しを読む）。
- 実行する場所: AI 作業部屋の中だけ（`hooks.md` の「領域とフックの権限」。works などでは行わない）。反映は人が `room readme <名>` で行う。`archives/` は触らない。

## 手順

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`ai/docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（Area の上限は、ワークスペースの規約に従う。暫定: 5件）。
2. **判断基準で検査する**:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project の上限を超えないか（暫定: 3件）。
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 種類 `type`（`doc` `dev` `dev-env` `dev-test` `research`。成果物の種類で決める。Area は既定値のヒント。環境やテストだけが成果物なら `dev` でなく `dev-env` `dev-test`）、主題（言語や方式など）、完了条件の種類、見直し日。開発系（`dev` `dev-env` `dev-test`）の Project は、`start-hook.md` の「開発」の差分の項目を、**実装の前に**ここで聞く。
4. **下書きを書く**: `ai/out/readme-draft.md` に、README の本文（目的、完了条件、成果物、範囲外、Open Questions。雛形は `templates/project/README.template.md`）を書く。完了条件は、ユーザーが承認してから書く（承認の前に「ユーザー承認: 日付」を書かない）。Project の名前の案（`<動詞か領域>-<主題>`、例: `learn-c-pool-allocator`。ワークスペース内で一意）を添える。
5. **記録する**: `ai/docs/log-history.md` に1項目（現在状態に影響するなら `ai/docs/log.md` も更新）。呼び出し元に `events` があるときは、質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `ai/docs/decisions.md` に決定として書く。
6. **`start` を呼ぶ**。

## 報告の型

共通の項目（`hook-common.md` の「報告の型」。ユーザーに求めること、コミット）を先に報告する。このフックでの追記:

- **ユーザーに求めること**: 人が `room readme <名>` で下書きを反映すること。未承認の完了条件があれば、その確認。
- **コミット**: このフックはコミットしない（人が行う `room open` / `room readme`）ので、「なし」と書く。

続けて、固有の項目を次の順で報告する。

1. **下書き**: `ai/out/readme-draft.md`、種類（`type`）、完了条件、見直し日。
2. **`start` の呼び出し**: 呼んだこと（または呼ばなかった理由）。

## Project の構造

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
| `_noai/` | 原本 `raw/`、対応表 `map/`、復元済みの成果物 `final/`、`mask.toml`。追跡しない | 見えない |

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

## 実測から分かっていること

- 完了条件は、AI が具体案（成果物）を出し、ユーザーが承認する形が効率的。承認の前に、承認の記述（「ユーザー承認: 日付」）を README に書かない。
- 開発系の前提（専門領域、設計の優先順位、コーディングルール、ポインタの規則）が、`open` の時点で聞かれず、後から出た。手順「聞く」で、実装の前に聞く。

## 未決

- `doc` と `research` の基準文書の形（2026-10-16）。置き場と最小の中身（Must の3項目）は `change-method.md` で決まっているが、type 別の書き方は、最初の利用の後に決める（`dev` だけ、3文書が兼ねる）。
- リポジトリが正の `src`、remote で動くものの置き場（2026-10-16 残件）。この構造は、新規にフルスクラッチで作る前提。clone を `ai/out/` に置くと、`.git` の中身で `restore` が止まる（復元できない形式）。案（未検証）: clone は `repos/` に置いたまま、人がスナップショットを `ai/work/<名>/` に写し、AI の成果は `ai/out/<成果物名>/` に基準文書と patch で置く。基準文書の「正の向き」はリポジトリ側。remote の検証は人が行う（検証項目に書く）。
- `remote` という type（2026-10-16 ee の案）。WSL から SSH で接続し、user 権限でリモート（Docker を含む）を操作する、AI の活用。`dev-env` に限らず `dev` でも使うので、置き場の違いを `type` にする案。`dev-env` は、テスト環境を作る用途に絞る。`remote` の接続の安全（鍵、権限、記録）は、AI 作業部屋の境界の設計（`topics/ai-workspace-boundary/`）と合わせて決める。実測の後に決める。
- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
- Project の構造（type は5種、`ai/work/` の下書きの分離）の実測。`dev-env` と `dev-test` は2026-10-16 に足した叩き台で、実測が無い。`research` と、`dev` と `doc` の混合の Project の扱い。
