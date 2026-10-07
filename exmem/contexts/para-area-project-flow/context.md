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
- AI の提案（未承認）: 終了処理の棚卸しで、Project 側に【案件】の項目が残っていないかを点検する。close の仕事は、status の更新、`archives/` への移動、【汎用】のナレッジ化だけになる。

## Next Actions

- Area の雛形を決める（「作業を始めて」の次にやること）。叩き台: `README.md`（frontmatter に `type: area` と `status`。本文に、案件の概要・目的、タスク候補、Project 一覧の Bases）、`docs/log.md`、`docs/decisions.md`（2026-10-07 時点）。
- その後に、open（タスク候補を Project に切り出す）の雛形と手順書を決める。Area から渡すもの（ゴール、期限、関連する決定や資料へのリンク）と、Project の `README.md` の frontmatter（`status` `area` `review` に、期限を足すか）を決める。
- 3ラベルを `docs-rules.md` の【汎用】【この件】に足すか、Vault ローカルの規則で試すかを決める。kit を変えるときは承認を取る。
- Vault 側の手順書（`project-open.md`、`project-close.md`）と、既存の Area・Project を、上の決定と照合する。
- [[para-operations]] の Area の定義と Decisions を、統合のときに書き換える。

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
