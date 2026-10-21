---
type: topic-note
title: plan-room-link の 6R（start 計画 A）
created: 2026-10-21
updated: 2026-10-21
---

# plan-room-link の 6R

`start 計画` の A（`workflow-kit/start-plan.md`）。ユーザーの依頼は `docs/decisions.md` の末尾の項（2026-10-21）。実装（案 D）が先に済んだので、この 6R は後追いで、残りの作業（反映の確認、知識化、トピックを閉じる）の範囲を決めるために作る〔推測〕。

条件: 期日は 2026-10-28（予算の1週間）。

## 1. 状況・問題意識（1欄にまとめた）

**計画の出力が、部屋の README と結び付かず、承認のたびに手で直す運用は漏れる。**

- `start 計画` の出力と `room init` / `room open` が作る README は、これまで無関係だった〔資料: `plan-room-link-issues.md` 3 章〕。
- 計画は改良のたびに作り直され、README に写すと必ずずれる〔資料: ユーザーの発言、2026-10-21「承認前後どちらも改良で繰り返し作成」〕。
- 論点は「計画を README に写すか、指すか」。写す案 A は取り下げ、指す案 D にした〔資料: `docs/decisions.md` の先頭の項〕。

## 2. 要求

**Project の README から、承認版の計画の場所が分かる。**

- Project の README の雛形に、固定の1行（`計画: ai/in/plan/`）が入る〔済 `9b4db50`〕。
- 部屋の AI が、計画を `ai/in/plan/` から読む決まりが書かれている〔済 `room-context.md`〕。
- 計画の置き場の決まりが、`start-plan.md` と食い違わない〔済 `ea9866c`〕。

## 3. 意図・裏づけ

**写さないので、ずれる所が無い。後から案 A に進める。**

- 裏づけ（確かめた）: 単体テスト 109 件パス（スキップ 3）、`close` の雛形チェックは新しい1行を `<...>` と見なさない〔テスト、`room.py` の `README_PLACEHOLDERS`〕。
- 裏づけ（未確認。最初に確かめる）: 実機で `room open` した README に1行が入る。確かめる方法: 次に `room open` するとき README を見る。時期: 次の `open`。
- 使ってみて確かめること: 完了時期などが README に無くて困る場面が出るか。出たら案 A（印の節）を再検討する。

## 4. 今回のスコープ

**反映の確認、知識化、トピックを閉じるまで。**

変更先の洗い出し（済は実装済み）:

| ファイル | 内容 | 状態 |
|---|---|---|
| `workflow-kit/room/room.py`、`templates/project/README.template.md` | 雛形に固定の1行 | 済 |
| `workflow-kit/room/tests/test_room.py` | 1行と `close` の関係のテスト | 済 |
| `workflow-kit/room-context.md` | 節「計画（部屋の中）」 | 済 |
| `workflow-kit/start-plan.md` | works の置き場 | 済 |
| `exmem/lessons/planning-method.md` | 計画の置き場の決定（案 D、実名なし）を足す | 未 |
| `docs/decisions.md`（root） | トピックの【この件】を1項にまとめる（閉じるとき） | 未 |

変えないこと: `open-hook.md`、Area の README、`close` の雛形チェック、`room.py` のロジック。

対象外: README への計画の要約の差し替え（案 A。理由: 運用が重く、ずれる。見直す条件: README に完了時期が無くて困る場面が出たとき）。

前提・注意: 公開リポジトリなので実名・機密を書かない。`workflow-kit/` はユーザーの承認が要る（今回は承認済みの範囲）。

## 5. 期待する成果

**Project の README と部屋の AI の両方が、計画の場所に迷わない。**

- 指標: 次に `open` した Project の README の「計画:」の行が、実機で入っている（1つ）。

## 未決

- 憲章・WBS・マイルストーンまで作るか。残りは4行（未の2つと実機確認、トピックを閉じる）で、6R で足りる可能性が高い〔推測〕。ユーザーに聞く。
