---
type: procedure
title: 分割して進める試験の手順（通し試験）
tags:
  - workflow
  - knowledge-management
created: 2026-11-06
updated: 2026-11-06
---

# 分割して進める試験の手順（通し試験）

`room` の手順書や案内文（`project-structure.md`、`room-context.md`、`room.py` の `POINTER_TEXT`）を直したときに、新しいセッションを工程ごとに起動し直して進める基本形が崩れていないかを確かめる。ユーザーが言ったときだけ行う。前回の結果は [[room-split-test-log]]（2026-11-05〜06。`dev` `inv` とも 6 回、同じ観点で動けた）。

## 準備

- 部屋は `internal` の Area（前回は `myenv`）。Project は `dev` 用と `inv` 用に 1 つずつ、新規に `room open <Project> --area <Area> --type dev|inv`（名前は `sample_split<dev|inv>` の形。試験が終われば消す）。同じ Project を再利用しない（成果物名や 6R が前回のまま引き継がれて、規則の効果が見えなくなる）。
- 題材は小さな問いにする（前回: `dev` は CSV の概要を出す小さな CLI、`inv` は uv と pip-tools の比較）。結果の正否ではなく、構造と引き継ぎを見る。
- 人の役は、エージェント（試験を回す側）が判断・承認の文を書いて演じる。

## 6 回の依頼

各回のプロンプトを Project の `ai/records/p/p<番号>.txt` に書く。依頼は短く、置き場や構成の名前を書かない。

| 回 | 依頼 |
|---|---|
| 1 | 計画を立てて。今回は 6R まで |
| 2 | 続きです。論点出し |
| 3 | 続きです。判断（人の返答）を書き戻し、承認。最初の工程まで |
| 4 | 続きです。次は src／findings まで |
| 5 | 続きです。次は tests／checks まで |
| 6 | 続きです。最後。報告まで、終える前にやることも |

## 起動

回ごとに、`workflow-kit/room` で 1 回起動する（前の回が終わってから。並行しない）。

```powershell
uv run room.py start <Project> --cmd "claude -p --permission-mode acceptEdits --allowedTools 'Bash WebFetch WebSearch Read Write Edit Glob Grep' < records/p/p<番号>.txt"
```

- プロンプトは引数でなく stdin で渡す（`--allowedTools` が可変長引数でプロンプトを吸う）。`--permission-mode acceptEdits` が無いと、書き込みの許可で止まって何も作れない。
- 長く待つので、バックグラウンドで実行して、`start` の出力に「回収」「マウント解除」が出るのを待つ。
- 次の回の前に、マウントが残っていないか確かめる。残っていたら `uv run room.py umount --area <Area>`（Zed の remote server がつかんでいるときは、Zed を再起動してから）。

## 見る点（回ごと）

1. 引き継ぎ: 依頼が一文でも、`ai/docs/log.md`・`decisions.md`・`ai/work/plan/` から文脈を拾ったか。
2. 範囲: 「その先にはまだ進まない」を守ったか。
3. 記録: 判断は `decisions.md`、状態は `log.md`、承認は `6r.md` に残り、来歴が区別されているか。
4. 置き場: 成果物名が Project 名と同じか。`report.md` が成果物の下か。`inv` に `src/` が無いか（スクリプトは `ai/work/scripts/`）。
5. 6R: 承認後に `仮` へ戻っていないか。
6. 裏取り: 事実と推測の分離、未確認の明記、前の回の数値の訂正の仕方（元を直さず、`checks.md` に訂正を足す）。
7. 終わり方: 依頼になくても `ai/out/close.md` が書かれたか。

結果は `logbook/` に `room-split-test-log.md` と同じ型で残す（古い結果は畳む）。
