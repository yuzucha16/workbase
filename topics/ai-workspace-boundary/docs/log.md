# ai-workspace-boundary: 現在状態（正本）

更新: 2026-10-18。経緯は `log-history.md`、決定は `decisions.md`。

## 項目の状態（優先順位 1〜8）

2026-10-18 に PC で通しの確認が済んだ（`init`、`open`、`mask`、`start`、`restore`、`readme`、`stock`、`close`、`reap`、Excel、手作業版。経緯は root の `docs/log-history.md`）。

| # | 項目 | 状態 | 残り |
|---|---|---|---|
| 1 | マスク・復元 | 済 | 実データの警告量 |
| 2 | 共有知を部屋へ | 済 | 部屋の AI が `wrap` に従えるか（root の Next Actions 20） |
| 3 | フックの整理 | 済 | — |
| 4 | `stock` の回収 | 済 | — |
| 5 | 部屋の運用 | 済（`room intake` は作らない。2026-10-16 承認） | — |
| 6 | Area の切り方 | 済 | — |
| 7 | 雛形・記録 | 済 | Vault 側 deny の書式 `Read(./projects/**)` が Windows で効くか |
| 8 | 実 Project での1巡 | 未 | 新しい Project か改善の1行 |

## あなた待ち

- 対応表（`mapping.json`）は、`archives/` へ移る `_noai/` ごと PC のバックアップに任せる（2026-10-14 決定。実施の確認だけ）。

## 次の一手（PC）

root の `docs/log.md` に既にある項目（Next Actions 10・20・37、Open Questions の `restore` の上書き保護と `remote` の type）は、そちらで進める。ここに残すのは次だけ。

1. 実データで `mask` の警告量を見る（項目 1）。
2. Windows で Vault 側 deny の書式を確かめる（項目 7）。
3. `base_stale` を確かめる。
4. `room start` が写した `ai/ctx/area-README.md` を、部屋の AI が開始時に読めるか。
5. `room restore` が、`mapping.json` が無い・食い違うときに止まるか。
6. `SharedPermissionTest` 2件は Windows で失敗（元から。Linux では通る）。原因は未調査。

## 完了の条件

優先順位 1〜7 が PC で確認済み（8 以降は新しい Project か改善の1行）。そのとき: 検証用の環境（`ai-room-test`、`_spike-room`、`%TEMP%\s5\`）を消し、このトピックを close して削除する。
