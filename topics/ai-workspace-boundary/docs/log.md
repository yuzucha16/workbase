# ai-workspace-boundary: 現在状態（正本）

更新: 2026-10-15。状態の写しをほかに置かない。経緯は `log-history.md`、決定は `decisions.md`。

## 項目の状態（優先順位 1〜8）

| # | 項目 | 実装 | 実機の確認 | 場所 |
|---|---|---|---|---|
| 1 | マスク・復元 | 済 | ダミーで 1〜4・6 済。残り: 5 `room start` の通し、7 実データの警告量 | PC |
| 2 | 共有知を部屋へ | 済 | 1〜4 済。残り: 5 AI が `wrap` を通せるか。許可の確認（`Read(~/shared/**)` 追加済み）が出なくなるか | PC |
| 3 | フックの整理 | 済（文書・`room readme`） | 残り: `room init`、`open`〜`close` の1巡 | PC |
| 4 | `stock` の回収 | 済 | ダミーで済。残り: 部屋の AI が実際に下書きを書く通し | PC |
| 5 | 部屋の運用 | 未（`room init`、reap、`room intake`） | — | PC（保留中。別セッションの構造の議論と合流してから） |
| 6 | Area の切り方 | 済 | — | — |
| 7 | 雛形・記録 | 済 | 残り: Vault 側 deny の書式 `Read(./projects/**)` が Windows で効くか | PC |
| 8 | 実 Project での1巡 | — | 未 | PC |

## あなた待ち

- 対応表（`mapping.json`）のバックアップ方針。案: `room close` で `archives/` へ移る `_noai/` ごと Windows 側のバックアップに任せる（2026-10-14 に決定済み。実施の確認だけ）。

## 次の一手（PC）

1. 項目 1 → 2 → 4 の「実機の確認の残り」を進める。各 `notes/*-handover.md` の「PC で確認すること」を見る。
2. 小さな不具合: マウントが別の `wsl.exe` から見えない件（対策を実装済み。`--no-launch` 中に別セッションから `/proc/mounts` と `ai/` が見えるか確認する）。

## 残りの確認・保留

- `room start` が `ai/ctx/area-README.md` を写して、部屋の AI が開始時に読めるか（実機。単体テストのみ）。Area の README の書き方（共通ルールの節）の指針は未整備。
- `type: dev` の Project を1つ、`dev-deliverable-guide.md` どおりに `open` から1巡して、手順の過不足を測る。
- 実環境の結果を AI に渡す受け取り口（人が置いた結果を `room` がマスクして `ai/in/` へ）を作るか。当面は、人が語を伏せる規約。
- `room` の単体テストの `SharedPermissionTest` 2件が失敗する（元から。原因は未調査）。
- `room restore` が `ai/out/<成果物>/` のサブディレクトリを復元できるか、`mapping.json` が無い・版が食い違うときに止まるか（実機）。
- 文書2本（`guides/explain/ai-room-why.md`、`guides/howto/ai-room-setup.md`）のレビュー（「草稿（未レビュー）」の注記を外す）。
- 後回し: `areas/dev-env/certs` の移し替え、対応表の保護、Obsidian の AI プラグイン、Codex・Copilot の設定、小さいファイルが多い処理の遅さ（規則で対処済み）。

## 完了の条件

優先順位 1〜7 が PC で確認済み（8 以降は新しい Project か改善の1行にする。子には分けない）。そのとき: 検証用の環境（`ai-room-test`、`_spike-room`、`%TEMP%\s5\`）を消し、このトピックを close して削除する。
