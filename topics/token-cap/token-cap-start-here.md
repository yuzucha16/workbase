# 窓口: token-cap

- 型: Project 型。完了条件: 月の使用量を上限（2億トークン）の内に収める見直しの角度が決まり、効くものが仕組み・運用に反映されて、翌月の使用量で確かめられる。
- 何の取り組みか: 職場の AI 使用に月次の上限が付いた（2026-10 は 26 日で 90%）。トークンを抑える角度の洗い出しと、詰める順番の決定。ee の挙げた角度は、①workbase の仕組み（ベーストークン）、②AI と人の作業の線引き。90% に達した主因は Excel マクロの全面実装を AI に任せたこと。起点と既存資料は `records/2026-10-26-angles.md`。

## いま

PC1 の 10-21 以降は room（WSL）側にあり、合算 約 170.7M（85%）、残り約 29M（`records/2026-10-27-pc1-room-meter.md`）。ee は今月の重い作業を止める。切る目安は「作業の区切り、または 100k」のまま。解説は `guides/explain/claude-code-cost-session-size.md`。

## あなた待ち

- なし（マクロの現況は 10-27 に回答を受けて閉じた）。

## 次の一手

「token-cap の続き」。止める基準の案（`integrate` の読む量を減らす。`docs/log.md` の Next Actions 2）、room の 107k の確認。lessons の分割は全 6 本が済んだ（10-27）。room の会話記録の退避は済み（`room reap`、10-27）。どこでも可。

## 読む順

1. `docs/log.md`（現在状態。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（出力）

## リポジトリに無いローカルの状態

PC1 の Claude Code の会話記録（`~/.claude/projects/`）。PC2 には無い。
