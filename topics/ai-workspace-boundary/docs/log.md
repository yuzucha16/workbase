# ai-workspace-boundary: 現在状態（正本）

更新: 2026-10-16。経緯は `log-history.md`、決定は `decisions.md`。

## 項目の状態（優先順位 1〜8）

| # | 項目 | 実装 | 実機の確認 | 場所 |
|---|---|---|---|---|
| 1 | マスク・復元 | 済 | ダミーで 1〜4・6 済。残り: 5 `room start` の通し、7 実データの警告量 | PC |
| 2 | 共有知を部屋へ | 済 | 1〜4 済。残り: 5 AI が `wrap` を通せるか。許可の確認が出なくなるか | PC |
| 3 | フックの整理 | 済（文書・`room readme`） | 残り: `room init`、`open`〜`close` の1巡 | PC |
| 4 | `stock` の回収 | 済 | ダミーで済。残り: 部屋の AI が実際に下書きを書く通し | PC |
| 5 | 部屋の運用 | `room init` `room reap` 済み（単体テストのみ）。`room intake` は作らない（2026-10-16 承認。1巡で規約が回らないと分かってから） | `init` `reap` を使い捨ての Area / Project で実機に通す。案は `notes/ai-room-ops-handover.md` | PC |
| 6 | Area の切り方 | 済 | — | — |
| 7 | 雛形・記録 | 済 | 残り: Vault 側 deny の書式 `Read(./projects/**)` が Windows で効くか | PC |
| 8 | 実 Project での1巡 | — | 未 | PC |

## あなた待ち

- 対応表（`mapping.json`）は、`archives/` へ移る `_noai/` ごと PC のバックアップに任せる（2026-10-14 決定。実施の確認だけ）。

## 次の一手（PC）

0. 実機で、新しい3つを通す（使い捨てで。単体テストのみ）:
   - `room restore`: 人が変えた `_noai/final/` で止まる、`--force` で通る、AI だけの変更では止まらない。
   - `room init <Area>`: 分離の確認、`wsl --install --name`、ログイン後に `claude -p` が返る。終わったら `wsl --unregister`。
   - `room reap`: close して `reap_after` を過去に。その Project の分だけ消える。
1. 項目 1 → 2 → 4 の「実機の確認の残り」を進める。`notes/*-handover.md` の「PC で確認すること」。
2. 小さな不具合: マウントが別の `wsl.exe` から見えない件（対策は実装済み。`--no-launch` 中に別セッションから `/proc/mounts` と `ai/` が見えるか確認する）。
3. リモート（ssh 先）の dev 用に、部屋専用の SSH 鍵を1本作って試す（対象ホストの権限を絞ったユーザーだけに登録、`authorized_keys` の `command=` `from=` で絞る。1Password のエージェントは渡さず、interop は切ったまま）。結果を見て採否を `decisions.md` に書く（部屋に鍵を置く決定の変更になる）。

## 残りの確認・保留

- dev の実装対象がリポジトリ・remote のとき（推奨は未承認）: 公開リポジトリから進める。clone は部屋の `~/tmp/<Project>/`、成果は基準文書と patch、マスク無しの Project は `room restore` を飛ばす（差分で承認を得る）。経緯と比較は `log-history.md` の 2026-10-16。
- `room start` が `ai/ctx/area-README.md` を写して、部屋の AI が開始時に読めるか（実機。単体テストのみ）。Area の README の書き方（共通ルールの節）の指針は未整備。
- `type: dev` の Project を1つ、`dev-deliverable-guide.md` どおりに `open` から1巡して、手順の過不足を測る。
- `SharedPermissionTest` 2件は Windows で失敗（元から。Linux では通る）。
- `room restore` が `ai/out/<成果物>/` のサブディレクトリを復元できるか、`mapping.json` が無い・食い違うときに止まるか（実機）。
- 文書2本（`ai-room-why.md`、`ai-room-setup.md`）のレビュー（「草稿」の注記を外す）。
- 後回し: 経緯 `log-history.md` の 2026-10-16 を参照。

## 完了の条件

優先順位 1〜7 が PC で確認済み（8 以降は新しい Project か改善の1行）。そのとき: 検証用の環境（`ai-room-test`、`_spike-room`、`%TEMP%\s5\`）を消し、このトピックを close して削除する。
