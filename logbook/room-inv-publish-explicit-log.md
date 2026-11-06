---
type: logbook
title: inv で清書の形式（pptx・quarto）を明示したときの置き場の試験
source: "[[room-inv-combo-test-log]]"
created: 2026-11-06
updated: 2026-11-06
review_by: 2027-01-05
budget: 8KB
---

# inv で清書の形式を明示したときの置き場の試験（2026-11-05〜06）

組み合わせ試験の指摘 1 の追試。部屋 `room-myenv`（internal）、`--type inv`、`room start --cmd` で `claude -p`（起動の注意は [[room-inv-combo-test-log]]）。題材は Marp・Slidev・Quarto の選び方。

## いま

- 「pptx で」と明示すると `publish/` に pptx が出る（`guides/quickref/ai-work-prompts.md` に反映済み）。
- 「quarto/revealjs で」と明示したときは、最初、清書物が `publish/` でなく `ai/out/<Project>/` の直下に出て、`report.md` も作られなかった。
- **原因**: `claude -p` の部屋のエージェントは `~/shared` の手順書を読みに行かない。手順書（`project-structure.md`、`room-context.md`）に足しても変わらず、**常に読まれる案内文（`room.py` の `POINTER_TEXT`、`~/.claude/CLAUDE.md`）に書いて初めて効いた**。知見は `exmem/lessons/ai-isolated-work-room.md` に統合済み。
- 案内文と `project-structure.md` に「形式を書いたら `report.md` 本体、清書物は `publish/`」「軽い依頼・報告資料では `question.md` を作らず、情報源は 1〜2 件なら直下の `sources.md`、3 件以上なら `sources/sources.md`」を足した後は、pptx・quarto とも `report.md` `sources/sources.md` `publish/` の同じ構成になった（各 1〜2 回。ばらつきが無いとまでは言えない）。

## 明細

### 「pptx で」（11-05、`sample_invP`）

- 作った: `report.md` `sources/sources.md` `findings/findings.md` `publish/sample_invP.pptx`（5 枚）と生成スクリプト `publish/deck.js`。作らなかった: `question.md` `checks/`（未確認 5 項目は `report.md`）。聞き返し 0。
- 指摘: `deck.js` は pptxgenjs を `/tmp` に入れて動かしたため、再実行には入れ直しが要る（`init` の段に入れるかは未決）。Marp の編集版は部屋で 150 秒打ち切りで未確認と明記された。

### 「quarto/revealjs で」（11-06、`sample_invQ`）

- 終了コード 0、聞き返し 0。`slide-tool-selection.qmd`（5.9KB）と html（3.9MB、`embed-resources: true`、10 枚）を `ai/out/sample_invQ/` 直下に作った。`report.md` `question.md` `sources/` `findings/` `checks/` `publish/` は無し。根拠・未確認はスライド内。
- 3.9MB の html は一枚で共有しやすい（pptx の `deck.js` のような再実行の手間が無い）。

### 修正と再試（同日）

| 回 | 直し | 結果 |
|---|---|---|
| `sample_invR` | `project-structure.md` に追記 | 変わらず（`out/` 直下に `report.qmd` `report.html`） |
| `sample_invS` | `room-context.md` にも追記 | 変わらず |
| `sample_invT` | 案内文 `POINTER_TEXT` に追記 | `report.md` `question.md` `sources.md` `findings/` `publish/report.{qmd,html}` |
| `sample_invU`（pptx 対照） | 同上 | `report.md` `sources/sources.md` `findings/` `publish/` |

ばらつき（`question.md` の有無、`sources` の形）を規則でそろえて再試（ユーザーの指示）:

| 回 | 形式 | 結果 |
|---|---|---|
| `sample_invV` | quarto | `report.md` `sources/sources.md` `publish/` |
| `sample_invW` | pptx | `report.md` `sources.md`（6 件なのに直下。基準から外れた）`publish/` |
| `sample_invX`（基準の文を強めた） | quarto | `report.md` `sources/sources.md` `publish/` |
| `sample_invY` | pptx | `report.md` `sources/sources.md` `publish/` |
