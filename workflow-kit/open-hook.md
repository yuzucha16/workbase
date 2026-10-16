# `open` フック

呼び出し名は `open`（Project の開始）。別名は無い。呼び出し表の正本は `hooks.md`（体系の経緯は `README.md` の「フックの体系」）。

実測で直して育てる。

## 目的と契機

- **目的**: `open` は Project の主題と完了条件を決めて、ひな形を作る。作ったあとに `start`（`start-hook.md`）を呼び、その日のゴールと前提を決める。
- **契機**: Project を新しく始めるときに、ユーザーが言う、または `start` が、進行中の Project が無いと判断したときに案内する。小さな再開では、`open` は不要。
- **前提**: ワークスペース（PARA 構成。`areas/` `projects/` `archives/`）がある。

## 場所と書き込みの制約

- 書き込み先は、`projects/<名>/`（手順「作る」）、`areas/<名>/README.md` の一覧（手順「Area の一覧を更新する」）、呼び出し元の記録（`docs/log.md`、`docs/decisions.md`、`events`。手順「記録する」）だけ。`archives/` は触らない（`close` の領分）。
- 実行する場所: ワークスペースの Vault 側の AI は、`projects/` `areas/` `archives/` を読み書きしない。この手順の書き込みは AI 作業部屋の中で行う。副作用（ひな形、状態の更新、コミット）は人が `room` で行い、AI は判断をファイルに書く（`room-context.md`）。
- コミットと push は、手順「コミットする」に従う。

## 手順

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（無ければ Area を作る。Area の上限は、ワークスペースの規約に従う。暫定: 5件）。
2. **判断基準で検査する**:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project の上限を超えないか（暫定: 3件）。
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 種類 `type`（`doc` `dev` `research`。成果物の種類で決める。Area は既定値のヒント）、主題（言語や方式など）、完了条件の種類、見直し日。開発系の Project は、`start-hook.md` の「開発」の差分の項目を、**実装の前に**ここで聞く。
4. **作る**: `projects/<名>/` に、`README.md`（ひな形: `templates/project/README.template.md`。frontmatter: `status: active`、`area`、`type`、`review`、`created`、`updated`。本文: 目的、完了条件、成果物、範囲外、Open Questions）。複数セッションにまたがるなら、`docs/log.md` と `docs/decisions.md`（`docs-rules.md` の書式）。構造は下の「Project の構造」。必要なら `AGENTS.md`。名前は、`<動詞か領域>-<主題>`（例: `learn-c-pool-allocator`）で、ワークスペース内で一意にする。
5. **Area の一覧を更新する**: `areas/<名>/README.md` の「進行中の Project」に、パス付きの wikilink（`[[projects/<名>/README|<名>]]`。README が複数あるのでファイル名だけのリンクは使えない）で足す。
6. **記録する**: `docs/log-history.md` の `## Log` に1項目（現在状態に影響するなら `docs/log.md` も更新）。呼び出し元に `events` があるときは、質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `docs/decisions.md` に決定として書く。
7. **コミットする**: パスを指定して `git add`。push はユーザー（使い捨ての環境では `docs-rules.md` に従う）。
8. **`start` を呼ぶ**。

## 報告の型

1. **作った Project**: パス、種類（`type`）、完了条件、見直し日。
2. **更新した Area の一覧**: 対象の `areas/<名>/README.md`。
3. **コミット**: ハッシュと内容。push の有無。
4. **次**: `start` を呼んだこと（または呼ばなかった理由）。
5. **改善案**（あったときだけ）: `hook-common.md` の「改善」に従う。

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
| `research`（調査） | 旧 `sources/` のうち、人が渡した資料 | 旧 `sources/` のうち、AI が集めた資料と抜粋。調べ途中の整理 | `report.md`（結論） |

基準文書（`exmem/lessons/change-method.md`。変更の設計と検証の物差しになる、AI が読めるテキスト。人と AI の工程の境界）:

- 置き場は、成果物と同じ `ai/out/<成果物名>/`（全 type 共通）。`dev` は、成果物の `docs/` の3文書（要求仕様・機能仕様・運用マニュアル）が兼ねる。
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
- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
- Project の構造（type は3種、`ai/work/` の下書きの分離）の実測。`research` と、`dev` と `doc` の混合の Project の扱い。
