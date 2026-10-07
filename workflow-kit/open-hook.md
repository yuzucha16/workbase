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
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 主題（言語や方式など）、完了条件の種類、見直し日。開発系の Project は、`start-hook.md` の「開発」の差分の項目を、**実装の前に**ここで聞く。
4. **作る**: `projects/<名>/` に、`README.md`（frontmatter: `status: active`、`area`、`review`、`created`、`updated`。本文: 目的、完了条件、成果物、範囲外、Open Questions）。複数セッションにまたがるなら、`docs/log.md` と `docs/decisions.md`（`docs-rules.md` の書式）。必要なら `AGENTS.md`。名前は、`<動詞か領域>-<主題>`（例: `learn-c-pool-allocator`）で、ワークスペース内で一意にする。
5. **Area の一覧を更新する**: `areas/<名>/README.md` の「進行中の Project」に、パス付きの wikilink（`[[projects/<名>/README|<名>]]`。README が複数あるのでファイル名だけのリンクは使えない）で足す。
6. **記録する**: `docs/log.md` に Log を1項目。呼び出し元に `docs/metrics/events.csv` があるときは、質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `docs/decisions.md` に決定として書く。
7. **コミットする**: パスを指定して `git add`。push はユーザー（使い捨ての環境では `docs-rules.md` に従う）。
8. **`start` を呼ぶ**。

## 実測から分かっていること

- 完了条件は、AI が具体案（成果物）を出し、ユーザーが承認する形が効率的。承認の前に、承認の記述（「ユーザー承認: 日付」）を README に書かない。
- 開発系の前提（専門領域、設計の優先順位、コーディングルール、ポインタの規則）が、`open` の時点で聞かれず、後から出た。手順 3 で、実装の前に聞く。

## 未決

- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
