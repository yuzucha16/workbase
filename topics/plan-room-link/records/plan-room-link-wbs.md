---
type: topic-note
title: plan-room-link の成果物 WBS
created: 2026-10-21
updated: 2026-10-21
---

# plan-room-link の成果物 WBS

6R（[[plan-room-link-6r]]）の「変更先の洗い出し」から作った。第 2 層は成果物の種類で分ける。葉は 1 ファイルに対応させ、各葉に置き場と状態を書く。

| # | 成果物 | 置き場 | 状態 |
|---|---|---|---|
| 1 | 計画の置き場の仕組み（kit） | | |
| 1.1 | 雛形の固定 1 行（`room.py` の `README_TEMPLATE`。テストを含む） | `workflow-kit/room/room.py`、`room/tests/test_room.py` | 済 `9b4db50` |
| 1.2 | Project の README 雛形 | `workflow-kit/templates/project/README.template.md` | 済 `9b4db50` |
| 1.3 | 部屋の AI への案内（節「計画（部屋の中）」） | `workflow-kit/room-context.md` | 済 `9b4db50` |
| 1.4 | 計画の置き場の表（works の行） | `workflow-kit/start-plan.md` | 済 `ea9866c` |
| 2 | 知識 | | |
| 2.1 | 計画の置き場の決定（案 D、実名なし）の追記 | `exmem/lessons/planning-method.md` | 未 |
| 3 | 動作確認 | | |
| 3.1 | 実機確認（次の `open` で README の 1 行を見る。結果は `docs/log.md` に 1 行書く） | 親の葉に含む（読み手がいる記録は `docs/log.md`） | 未（次の `open` 次第） |
| 4 | プロジェクトマネジメント | | |
| 4.1 | 6R | `topics/plan-room-link/records/plan-room-link-6r.md` | 済 |
| 4.2 | 憲章 | 同 `plan-room-link-charter.md` | 済 |
| 4.3 | WBS（このファイル） | 同 `plan-room-link-wbs.md` | 済 |
| 4.4 | マイルストーン | 同 `plan-room-link-milestones.md` | 済 |
| 4.5 | 作り方のメモ | 同 `plan-room-link-plan-notes.md` | 済 |
| 4.6 | 決定と経緯 | `topics/plan-room-link/docs/`（決定、経緯。閉じるとき root の `docs/` へ） | 済（更新中） |
| 5 | 案 A の再検討（条件付き） | 条件: README に完了時期が無くて困る場面が出たとき。出なければ空 | 空 |

親は子の足し算。モレ・ダブりの確認: 6R の変更先 6 行は、1.1〜1.4、2.1、4.6（root の `decisions.md`）に対応する。

## 変更の記録

| 日付 | 追加した葉 | 理由 |
|---|---|---|
| 2026-10-21 | 1.1〜1.4 を「済」で起票 | 実装が計画より先に済んだ後追いの計画のため |
