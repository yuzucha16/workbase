# 窓口: token-cap

- 型: Project 型。完了条件: 月の使用量を上限（2億トークン）の内に収める見直しの角度が決まり、効くものが仕組み・運用に反映されて、翌月の使用量で確かめられる。
- 何の取り組みか: 職場の AI 使用に月次の上限が付いた（2026-10 は 26 日で 90%）。トークンを抑える角度の洗い出しと、詰める順番の決定。ee の挙げた角度は、①workbase の仕組み（ベーストークン）、②AI と人の作業の線引き。90% に達した主因は Excel マクロの全面実装を AI に任せたこと。起点と既存資料は `records/2026-10-26-angles.md`。

## いま

切る目安 60k で明日から運用。伸びの主因は土台でなくファイルの全文読みと分かった（`records/2026-10-26-growth-by-reads.md`）。最初の一手の `docs-rules.md` の「コミットと push」の切り出しは完了（`workflow-kit/commit-push-rules.md`）。`review 消化` の 100k の原因も判明（旧名の横断の掃除での大きい Grep と全文読み）し、読み込みを抑える規則を `AGENTS.md` に書いた。`exmem-index.md` の読み方も `exmem/AGENTS.md` で完了。次は `brief` の読む量。PC1 の集計は明日 ee が取る（2026-10-26）。

## あなた待ち

- PC1 で `usage_report.py` と `heavy_sessions.py` の出力を取る（`docs/log.md` Next Actions 1）。
- 上限が「キャッシュ読みを含む総量」か、モデルで重みが違うかの確認（haiku 案の前提）。
- マクロの現況（規模・残り・実行できる環境）の回答（`records/2026-10-26-macro-split.md` の末尾）。

## 次の一手

「token-cap の続き」。PC1 の集計が届いたら、角度ごとの削減量を実数で見積もる。どこでも可。

## 読む順

1. `docs/log.md`（現在状態。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（出力）

## リポジトリに無いローカルの状態

PC1 の Claude Code の会話記録（`~/.claude/projects/`）。PC2 には無い。
