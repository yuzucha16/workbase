# Project を始める（open）手順書の下書き

> 2026-10-08: 正本は kit（`resources/workflow-kit` の `start-hook.md` `open-hook.md` `close-hook.md`）に移した。このファイルは、実測の経緯（出どころの ID つきの理由）の記録として残す。改善は kit を直す。

状態: **下書き**。最初の Project（`learn-c-pool-allocator`、2026-10-06）で実際に行った手順から起こした。2回目で実測して直す。kit への昇格は、安定してから判断する（いまは PoC）。判断基準は `docs/decisions.md`（「PARA の `areas/` `projects/` `archives/` の役割と判断基準を定める」）。

## 呼び出し

「作業を始めて」のとき、進行中の Project が無ければ、開始インタビューの前に、この手順で Project を作る（`AGENTS.md`）。`areas/learning/README.md` の「次の Project の候補」から選ぶのが、基本。

## 手順

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（無ければ Area を作る。Area は5件まで）。
2. **判断基準で検査する**（`decisions.md` の基準 1〜3、5）:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project が3件を超えないか。
3. **聞く**（選択式。答えが1つに定まるものは宣言する）: 言語や方式などの主題、完了条件の種類、見直し日。開発系の Project は、開始インタビューの「開発の差分」（専門領域、設計の優先順位、コーディングルールとチェック、対象環境）を、**実装の前に**ここで聞く。
4. **作る**: `projects/<名>/` に、`README.md`（frontmatter: `status: active`、`area`、`review`、`created`、`updated`。本文: 目的、完了条件、成果物、範囲外、Open Questions）。複数セッションにまたがるなら、`docs/log.md` と `docs/decisions.md`（`docs-rules.md` の書式）。名前は、`<動詞か領域>-<主題>`（例: `learn-c-pool-allocator`）で、Vault 内で一意にする。
5. **Area の一覧を更新する**: `areas/<名>/README.md` の「進行中の Project」に、パス付きの wikilink（`[[projects/<名>/README|<名>]]`。README が複数あるのでファイル名だけのリンクは使えない）で足す。
6. **記録する**: `docs/log.md` に Log を1項目、`docs/metrics/events.csv` に質問ごとの行を足す（回答を受けた同じターンで）。判断（完了条件など）は、ユーザーが承認したものだけを `docs/decisions.md` に決定として書く。
7. **コミットする**: パスを指定して `git add`。push はユーザー。

## 初回の実測で分かったこと（2026-10-06）

- 完了条件は、AI が具体案（成果物）を出し、ユーザーが承認する形が効率的だった。承認の前に、承認の記述（「ユーザー承認: 日付」）を README に書かない。
- 開発系の前提（専門領域、設計の優先順位、コーディングルール、ポインタの規則）が、open の時点で聞かれず、後から4回出た（`gap`）。上の手順 3 に、実装の前の確認として入れた。
- 開始インタビューとの境界: open は Project の主題と完了条件を決める。開始インタビューは、その日のゴールと前提を決める。小さな再開では、open は不要。

## 未決

- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
