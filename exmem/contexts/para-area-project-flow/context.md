---
type: project
title: PARA の Area と Project のデータの流れ Project Context
status: active
tags:
  - para
  - workflow
aliases:
  - PARA の Area と Project のデータの流れ Project Context
  - Area の雛形
  - 3ラベル
created: 2026-10-07
updated: 2026-10-07
---

# PARA の Area と Project のデータの流れ Project Context

## Current State

- 2026-10-07 に、Vault の外（Claude のプロジェクトのスレッド）で、Area と Project の間のデータの流れを論点整理した。この内容は、まだ Vault の手順書と [[para-operations]] に反映していない。
- 既存の決定（[[para-operations]]）は、Project ができた後の開始インタビュー（「作業を始めて」）と終了処理までを扱う。その前（Area から Project を作る open）と、その後（Project から Area へ戻す）は、決まっていなかった。
- ユーザーが決めたこと（2026-10-07）:
  - 定義: Area = 期間未定の案件。Project = 案件から切り出した、期限とゴールのあるタスク。案件全体の情報は Area が持ち、各タスクの状況を Area に集約する。既存の定義（Area = 終わりのない責任領域）は、これに書き換える。
  - 案件が終わったら、Area も `archives/` へ移す。
  - タスクの状態の正本は、Project 側（Project の `README.md` の frontmatter）に置く。Area は、Bases の一覧で集約して読むだけで、書き戻さない。
  - 未着手のタスク候補（まだ Project にしていないもの）は、Area の `README.md` に置く。
  - Area に `docs/decisions.md` を持たせ、案件全体の決定を置く。
  - 判断の項目のラベルを3つにする（変更がある前提で試す）: 【この件】= Project に残す、【案件】= 見つけた時点で Area の `docs/decisions.md` に直接書く（例: タスクで判明した、仕様変更などの案件全体への影響）、【汎用】= workbase へ（今の `exmem/inbox/` の流れ）。これで、close のときに Project から Area へ戻す処理は要らなくなる。
  - open のフックは、「作業を始めて」とは別にする。
  - まず Vault ローカル（`docs/drafts/` の手順書）で試し、安定したら kit に昇格する。
- 2026-10-07 の論点整理はここで区切った。この進め方（決めることを決める）は、`exmem/inbox/2026-10-07-deciding-what-to-decide.md` にナレッジ化した（未統合）。
- AI の提案（未承認）: 終了処理の棚卸しで、Project 側に【案件】の項目が残っていないかを点検する。close の仕事は、status の更新、`archives/` への移動、【汎用】のナレッジ化だけになる。

## Next Actions

- Area の雛形を決める（「作業を始めて」の次にやること）。叩き台: `README.md`（frontmatter に `type: area` と `status`。本文に、案件の概要・目的、タスク候補、Project 一覧の Bases）、`docs/log.md`、`docs/decisions.md`（2026-10-07 時点）。
- その後に、open（タスク候補を Project に切り出す）の雛形と手順書を決める。論点は下の「open の雛形の論点」。その次に、close の雛形（status の更新、`archives/` への移動、【案件】の残りの点検、【汎用】のナレッジ化）を決める。
- 3ラベルを `docs-rules.md` の【汎用】【この件】に足すか、Vault ローカルの規則で試すかを決める。kit を変えるときは承認を取る。
- Vault 側の手順書（`project-open.md`、`project-close.md`）と、既存の Area・Project を、上の決定と照合する。
- [[para-operations]] の Area の定義と Decisions を、統合のときに書き換える。

## open の雛形の論点（Area の雛形の次に決めること）

2026-10-07 に整理した。未決。Area の雛形（PC で決める）の後に決める。後に続くのは、close の雛形と、3ラベルの kit への反映。

1. 呼び出しの言葉: 「作業を始めて」とは別にする（決定済み）。言葉は未定（例: 「タスクを切り出して」）。
2. 入力: Area の `README.md` のタスク候補から1件を選ぶ。タスク候補の書式（タスク名、ゴール、期限）は、Area の雛形と合わせて決める。
3. Project の作業ディレクトリの雛形: `projects/<名>/README.md`（frontmatter: `type: project`、`status`、`area`、`review`。期限と完了条件を足すか）、`docs/log.md`、`docs/decisions.md`。「workflowを導入して」の項目1〜3と同じ形にするか、Project 用の軽い雛形にするか。
4. Project ごとの `AGENTS.md`: 置くか。提案: 置かない（Claude Code は親ディレクトリの `CLAUDE.md` も読むので、Vault のトップの規則が効く。固有の規則が要るときだけ足す）（AI の提案。未承認）。
5. Area から渡すもの: 完了条件の1文（判断基準①）を、open のときに必須にするか。関連する決定や資料は、コピーせずにリンクで渡すか。
6. Area 側の後処理: タスク候補から、その行を消すか、Project へのリンクに置き換えるか（一覧は Bases が集めるので、二重に持たない）。
7. 命名: `projects/<名>/` の名前の規則（Area 名を前に付けるか、日付を付けるか）。ファイル名は Vault の中で一意に保つ規約がある。
8. 上限: open のときに、進行中の Project が上限（3件、暫定）を超えないか点検するか。
9. 接続: open の直後に、そのまま開始インタビュー（「作業を始めて」）に入るか。
10. 記録: open をイベントログ（`docs/metrics/`）に残すか。

## Goal

Area（案件）と Project（タスク）の間で、開始と終了のデータの流れを決め、open と close のフックを作れる状態にする。

## Open Questions

- 【案件】を、作業の途中で書き忘れたときの検出方法（終了処理の棚卸しで足りるか）。
- Area の `docs/log.md` に何を書くか（Project の作業ログと重ならないか）。
- 案件が終わったと判断する条件（Area を `archives/` へ移す契機）。
- 上限（Project 3 件、Area 5 件）を、Area = 案件の定義のもとで見直すか。

## Related

- [[para-operations]]
- [[obsidian-vault]]
- [[workflow-kit]]
- [[ai-work-metrics]]
