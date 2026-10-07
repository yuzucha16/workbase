# `open` フック

呼び出し名は `open`（Project の開始）。別名は無い。Project を新しく始めるときに、ユーザーが言う、または `start` が、進行中の Project が無いと判断したときに案内する。名前の体系は `README.md` の「フックの体系」。

状態: **試験運用**。実測で直して育てる。ワークスペース（PARA 構成。`areas/` `projects/` `archives/`）がある前提。

`open` は Project の主題と完了条件を決めて、ひな形を作る。作ったあとに `start`（`start-hook.md`）を呼び、その日のゴールと前提を決める。小さな再開では、`open` は不要。

## 手順

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（無ければ Area を作る。Area の上限は、ワークスペースの規約に従う。暫定: 5件）。
2. **判断基準で検査する**:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project の上限を超えないか（暫定: 3件）。
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 種類 `type`（`doc` `dev` `research`。成果物の種類で決める。Area は既定値のヒント）、主題（言語や方式など）、完了条件の種類、見直し日。開発系の Project は、`start-hook.md` の「開発」の差分の項目を、**実装の前に**ここで聞く。
4. **作る**: `projects/<名>/` に、`README.md`（ひな形: `templates/project/README.template.md`。frontmatter: `status: active`、`area`、`type`、`review`、`created`、`updated`。本文: 目的、完了条件、成果物、範囲外、Open Questions）。複数セッションにまたがるなら、`docs/log.md` と `docs/decisions.md`（`docs-rules.md` の書式）。構造は下の「Project の構造」。必要なら `AGENTS.md`。名前は、`<動詞か領域>-<主題>`（例: `learn-c-pool-allocator`）で、ワークスペース内で一意にする。
5. **Area の一覧を更新する**: `areas/<名>/README.md` の「進行中の Project」に、パス付きの wikilink（`[[projects/<名>/README|<名>]]`。README が複数あるのでファイル名だけのリンクは使えない）で足す。
6. **記録する**: `docs/log.md` に Log を1項目。呼び出し元に `docs/metrics/events.csv` があるときは、質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `docs/decisions.md` に決定として書く。
7. **コミットする**: パスを指定して `git add`。push はユーザー（使い捨ての環境では `docs-rules.md` に従う）。
8. **`start` を呼ぶ**。

## Project の構造（2026-10-08 ユーザーが承認。試験運用）

固定の核に、種類別の追加を足す。`start` の「共通の項目＋作業の種類の差分」と同じ形。深さは Project 直下から2階層まで（`src/` の中身などは対象外）。空のディレクトリは先に作らず、最初のファイルが来たときに作る（固定なのは `README.md` と、必要なときの `docs/`）。

固定の核（全 type 共通）:

| パス | 内容 |
|---|---|
| `README.md` | frontmatter と、目的・完了条件・成果物・範囲外・Open Questions |
| `docs/` | 作業の記録だけ。`log.md` と `decisions.md`（複数セッションにまたがるとき） |
| 最終成果物 | Project 直下に置く |

種類別の追加:

| type | 追加 | 備考 |
|---|---|---|
| `doc`（手順書・仕様・設計・チェックリスト） | `drafts/`（版ごとの下書き、レビュー版）、`refs/`（ユーザーから渡された資料、チェックリスト） | 下書きは `docs/` に入れない（`docs/` を「作業の記録」の意味だけにする） |
| `dev`（設計・実装・評価） | `src/` `tests/` `tools/`、ビルド設定 | 設計メモ（design、coding-rules）は `docs/` |
| `research`（調査） | `sources/`（収集した資料と抜粋）。結論は直下の `report.md` | 実測が無い。叩き台 |

## 実測から分かっていること

- 完了条件は、AI が具体案（成果物）を出し、ユーザーが承認する形が効率的。承認の前に、承認の記述（「ユーザー承認: 日付」）を README に書かない。
- 開発系の前提（専門領域、設計の優先順位、コーディングルール、ポインタの規則）が、`open` の時点で聞かれず、後から出た。手順 3 で、実装の前に聞く。

## 未決

- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
- Project の構造（type は3種、`drafts/` の分離）の実測。`research` と、`dev` と `doc` の混合の Project の扱い。
