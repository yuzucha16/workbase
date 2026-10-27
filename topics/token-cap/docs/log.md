# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%。キャッシュ読みを含む数かは確認しない（ee の決定 10-27）。
- PC1 は 2 か所: Windows 側 10-09〜20 が 91.85M、room（WSL）側 10-21〜27 が 78.80M。合算 約 170.7M（85%）、残り約 29M。10-26 の勢い（23.7M/日）なら 1〜2 日で尽きる。`records/2026-10-27-pc1-meter.md`、`pc1-room-meter.md`。
- **ee は今月の残りの重い作業を止める**。切る目安は「作業の区切り、または 100k」（`docs/decisions.md`）。
- room の会話記録は `/home/ai/.claude/projects/`。`room reap` は消す前に退避する。
- 会話別の偏り: room は上位 10 本で 66%、PC2 は 41%、Windows は 91%（`records/2026-10-27-pc1-room-ranking.md`）。
- PC2（10-27）: 251.1M（目安）、2,733 応答、土台 27.9k、60k 超の応答はトークンの 86%。
- **傾向分析の骨子は埋めた**（`records/2026-10-27-trend-skeleton.md`）。伸びの要因別（PC1 Windows、文字数の按分）: Read 45%、書き込み本文 23%、Grep 10%、AI 本文 9%、PowerShell 9%、ユーザー発言 1.6%。効く順: 区切る → 大きな読み込みを避ける → 土台。
- 解説は `guides/explain/claude-code-cost-session-size.md`。未統合の下書き `exmem/inbox/2026-10-26-token-cap-meter-reading.md` の統合先候補はこのガイド。

## Next Actions

1. 骨子の残り（任意）: PC2 と room で要因別の分解を同じ方法で行う。room の 107k（10-27 03:22）の確認は後日（会話のある room で。この PC の room-myenv は 10-25 22:27 まで）。172k の型は `records/2026-10-27-pc2-one-request-172k.md`。
2. `integrate` の読む量の上限（`integrate-hook.md`、仮 〜11-29）と lessons の分割（全 6 本）は済み。効果は 10-27 以降の日ごとの値で測る。`--check-triggers` の FAIL 1 件は `claude-code-cost-session-size.md` の 16 語（別件）。
3. （低優先）マクロ側の常駐文書に、全文読みを避ける指示を入れる案。マクロの現況は閉じた（ee の決定 10-27）。
4. `room reap` の退避は済み。残り: `-home-ai`（Project に紐づかない履歴）は退避も削除もしない。部屋を直接消す場合は手で退避する。
5. 土台の整理（`AGENTS.md` など）は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`。前倒しはしない。ee の決定 10-27）。**漏らさない**: 土台は区切りまでの余裕を食い、1 会話の依頼数を減らす（作業性）。再判断のときは、動かせる土台の内訳を先に測る。

## Open Questions

- 差の約 16M の出どころ（10-01〜08 の分、Desktop）は取らない（ee の決定 10-27）。
- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
