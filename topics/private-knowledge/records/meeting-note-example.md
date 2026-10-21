---
type: record
title: Area の会議録の型の見本（案）
tags:
  - workflow
  - knowledge-management
created: 2026-10-21
updated: 2026-10-21
---

# Area の会議録の型の見本（案）

Area の `knowledge/` に置く会議録の形を、1つの完成例で示す。**内容は架空で、事実として扱わない。** 型の案は下の「型の案」。ユーザーの承認前の提案で、承認後に `docs/decisions.md` へ決定として書く。設計は [[private-knowledge-plan]] の WBS 1.1.1・1.1.3、軸の決定は `docs/decisions.md`。置き場は `areas/<Area>/knowledge/`（決定 ⑪）。

## 型の案

- 置き場とファイル名: `areas/<Area>/knowledge/YYYY-MM-DD-<slug>.md`。打合せ1件 = 1ファイル。統合したノートは `kind: integrated` で、同じ置き場にトピック単位で置く（統合の手順は別途）。
- frontmatter: `type: area-note`、`kind: meeting | integrated`、`title`、`status: active | superseded`、`date`（打合せ日。統合ノートは省略可）、`org`（顧客を表す名前。リスト可）、`project`（関連する Project。任意）、`tags`（`exmem/tags.md` の語彙）、`created`、`updated`、`sources`（文字起こしやメモの名前）、`todo_open`（未了の ToDo の件数）、`todo_due`（未了の最も早い期日）。
- 本文の見出し（固定。該当しないものは省く）: `## 冒頭`（人向け。決定・ToDo・次の一手を10行以内〔仮〕）、`## 決定`、`## ToDo`（表）、`## 背景・経緯`、`## 事実・数値`、`## 未決・要確認`。
- ToDo の正は本文の表。`todo_open` と `todo_due` は、表から数えて書く（Bases の一覧用。更新のたびに再計算する）。冒頭は、表と決定から書く。
- 決定と教訓の各行に、ラベル【この件】【案件】【汎用】を付ける。【汎用】は、一般化して `room stock` で workbase に出す候補（固有の事実は出さない）。
- AI に渡す写しは、ファイル全体をマスクする。冒頭は人向けなので、AI は読み飛ばしてよい。

## 見本

````markdown
---
type: area-note
kind: meeting
title: 在庫システム更新の進め方（定例）
status: active
date: 2026-10-14
org:
  - 自社
  - A社
project: stock-system-renewal
tags:
  - para
  - knowledge-management
created: 2026-10-14
updated: 2026-10-15
sources:
  - 自動の文字起こし（2026-10-14 定例）
  - 自分の議事録メモ
todo_open: 2
todo_due: 2026-10-21
---

# 在庫システム更新の進め方（定例）

## 冒頭
- 決定: 切替は11月第2週。旧システムの並行稼働は2週間。
- ToDo: 移行データの項目一覧を A社が10-21 までに出す（A社）。テスト計画の初版を10-28 までに作る（自社）。
- 次の一手: 10-21 に項目一覧を受け取り、差分を確認する。

## 決定
- 切替日を11月第2週にする。理由: A社の締め処理と重ならない。【案件】
- 並行稼働は2週間。短縮は、不具合が0件のときだけ検討する。【この件】
- 打合せの冒頭で、前回の決定を読み上げると、認識違いが減る。【汎用】

## ToDo
| 内容 | 担当 | 期日 | 状態 |
|---|---|---|---|
| 移行データの項目一覧を出す | A社 | 2026-10-21 | 未了 |
| テスト計画の初版を作る | 自社 | 2026-10-28 | 未了 |
| 会議室の予約 | 自社 | 2026-10-16 | 済 |

## 背景・経緯
- 旧システムの保守が年度末で切れるため、更新を前倒しした。
- 前回は切替日が10月末案だったが、A社の締め処理と重なる指摘が出た。

## 事実・数値
- 移行対象は約12万件（A社の説明）。件数は未確認。

## 未決・要確認
- 並行稼働中の二重入力の扱い（運用の負担を A社に確認する）。
````
