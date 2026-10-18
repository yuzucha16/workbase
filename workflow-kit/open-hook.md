# `open` フック

呼び出し名は `open`。別名は無い。呼び出し表の正本は `hooks.md`（体系の経緯は `README.md` の「フックの体系」）。

実測で直して育てる。

## 目的と契機

- **目的**: `open` は Project の主題と完了条件を決めて、README 本文を下書きする。続けて `start`（`start-hook.md`）を呼び、その日のゴールと前提を決める。ひな形（`README.md`、`ai/`、`_noai/`）、Area の一覧、状態、コミットは、人が行う `room open` / `room readme` の責務で、この手順書は持たない（`room-context.md`、`room/README.md`）。
- **契機**: Project を新しく始めるときに、ユーザーが言う、または `start` が、進行中の Project が無いと判断したときに案内する。小さな再開では、`open` は不要。
- **前提**: works（PARA 構成。`areas/` `projects/` `archives/`）があり、人が `room open <名>` で Project のひな形を作ってある。

## 場所と書き込みの制約

- 書き込み先: `ai/out/readme-draft.md`（README の本文だけ。frontmatter を含めない）と、呼び出し元の記録（`ai/docs/log.md`、`ai/docs/decisions.md`、`events`。手順「記録する」）だけ。Project と Area の `README.md` は書き込めない（`ai/ctx/` の写しを読む）。
- 実行する場所: AI 作業部屋の中だけ（`hooks.md` の「領域とフックの権限」。works などでは行わない）。反映は人が `room readme <名>` で行う。`archives/` は触らない。

## 手順

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`ai/docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（Area の上限は、works の規約に従う。暫定: 5件）。
2. **判断基準で検査する**:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project の上限を超えないか（暫定: 3件）。
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 種類 `type`（`doc` `dev` `dev-env` `dev-test` `research`。成果物の種類で決める。Area は既定値のヒント。環境やテストだけが成果物なら `dev` でなく `dev-env` `dev-test`）、主題（言語や方式など）、完了条件の種類、見直し日。type ごとの置き場、固定の核、基準文書の置き場は `project-structure.md`（type を決めるときと、`ai/` の置き場に迷ったときに読む）。開発系（`dev` `dev-env` `dev-test`）の Project は、`start-work-types.md` の「開発」の項目を、**実装の前に**ここで聞く。
4. **下書きを書く**: `ai/out/readme-draft.md` に、README の本文（目的、完了条件、成果物、範囲外、Open Questions。雛形は `templates/project/README.template.md`）を書く。完了条件は、ユーザーが承認してから書く（承認の前に「ユーザー承認: 日付」を書かない）。Project の名前の案（`<動詞か領域>-<主題>`、例: `learn-c-pool-allocator`。works 内で一意）を添える。
5. **記録する**: `ai/docs/log-history.md` に1項目（現在状態に影響するなら `ai/docs/log.md` も更新）。呼び出し元に `events` があるときは、質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `ai/docs/decisions.md` に決定として書く。
6. **`start` を呼ぶ**。
7. **報告する**（下の「報告の型」）。

## 報告の型

共通の項目（`hook-common.md` の「報告の型」。ユーザーに求めること、コミットを先に、次にやることを最後に）を報告する。このフックでの追記:

- **ユーザーに求めること**: 人が `room readme <名>` で下書きを反映すること。未承認の完了条件があれば、その確認。
- **次にやること**: `start` を呼んだこと、または呼ばなかった理由。
- **コミット**: このフックはコミットしない（人が行う `room open` / `room readme`）ので、「なし」と書く。

続けて、固有の項目を次の順で報告する。

1. **下書き**: `ai/out/readme-draft.md`、種類（`type`）、完了条件、見直し日。

## 実測から分かっていること

- 完了条件は、AI が具体案（成果物）を出し、ユーザーが承認する形が効率的。承認の前に、承認の記述（「ユーザー承認: 日付」）を README に書かない。
- 開発系の前提（専門領域、設計の優先順位、コーディングルール、ポインタの規則）が、`open` の時点で聞かれず、後から出た。手順「聞く」で、実装の前に聞く。

## 未決

- `doc` と `research` の基準文書の形（2026-10-16）。置き場と最小の中身（Must の3項目）は `change-method.md` で決まっているが、type 別の書き方は、最初の利用の後に決める（`dev` だけ、3文書が兼ねる）。
- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
- Project の構造（type は5種、`ai/work/` の下書きの分離）の実測。`dev-env` と `dev-test` は2026-10-16 に足した叩き台で、実測が無い。`research` と、`dev` と `doc` の混合の Project の扱い。
