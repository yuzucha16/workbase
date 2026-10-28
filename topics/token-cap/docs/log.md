# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%。キャッシュ読みを含む数かは確認しない（ee の決定 10-27）。
- PC1 は 2 か所: Windows 側 10-09〜20 が 91.85M、room（WSL）側 10-21〜27 が 78.80M。合算 約 170.7M（85%）、残り約 29M。10-26 の勢い（23.7M/日）なら 1〜2 日で尽きる。`records/2026-10-27-pc1-meter.md`、`pc1-room-meter.md`。
- **ee は今月の残りの重い作業を止める**。切る目安は「作業の区切り、または 100k」（`docs/decisions.md`）。
- room の会話記録は `/home/ai/.claude/projects/`。`room reap` は消す前に退避する。`-home-ai`（Project に紐づかない履歴）は退避も削除もしない。部屋を直接消す場合は手で退避する。
- 会話別の偏り: room は上位 10 本で 66%、PC2 は 41%、Windows は 91%（`records/2026-10-27-pc1-room-ranking.md`）。
- PC2（10-27）: 251.1M（目安）、2,733 応答、土台 27.9k、60k 超の応答はトークンの 86%。
- **傾向分析の骨子は埋めた**（`records/2026-10-27-trend-skeleton.md`）。伸びの要因別（PC1 Windows、文字数の按分）: Read 45%、書き込み本文 23%、Grep 10%、AI 本文 9%、PowerShell 9%、ユーザー発言 1.6%。効く順: 区切る → 大きな読み込みを避ける → 土台。
- 解説は `guides/explain/claude-code-cost-session-size.md`。未統合の下書き `exmem/inbox/2026-10-26-token-cap-meter-reading.md` の統合先候補はこのガイド。

## Next Actions

1. 骨子の残り（任意）: room の 107k（10-27 03:22）の分解結果を判定する。ee が PC1 で `decompose_session.py --at 2026-10-27T03:22 /home/ai/.claude/projects` のログを取得済み（10-28）。ee の PC での続きで結果を読み、172k の型（全文読みの連発。`records/2026-10-27-pc2-one-request-172k.md`）かを判定する。PC2 の要因別の分解は任意で残る。
2. `integrate` の読む量の上限（仮 〜11-29）と lessons の分割の効果を、10-27 以降の日ごとの値で測る。
3. （低優先）マクロ側の常駐文書に、全文読みを避ける指示を入れる案。マクロの現況は閉じた（ee の決定 10-27）。
5. 土台の整理（`AGENTS.md` など）は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`。前倒しはしない。ee の決定 10-27）。**漏らさない**: 土台は区切りまでの余裕を食い、1 会話の依頼数を減らす（作業性）。再判断のときは、動かせる土台の内訳を先に測る。
6. 【10-28 試験中】`brief` の引数を絞る案（`records/2026-10-28-brief-input-output-split.md`、測定は `records/2026-10-28-brief-mode-load.md`）。振り返りだけ切り出して試験中（ee の決定 10-28）。**2 回目は型だけで成立**（応答 4、土台 26.4k、積算 130k、増えた分 約 12.7k。型の全文読み以外の無駄な読みは無し）。判定: 良い。残りの無駄は、突発の失敗用の型（`-2-output`）も読んだこと（原因の `triggers` の「振り返」は外した。応答 4 → 3 回になるかを次の「振り返って」で確かめる）。良ければ調査・計画・改善1〜3 に広げ、`brief` の引数と `brief-modes.md` の聞き取りをやめる（`methods.md` は全文を読まない）。残す条件は、出力の型の価値（ee）。
7. 次の会話の最初に、ee の依頼: ① `cap_meter --latest` の表（応答数・土台・いまの大きさ・積算・土台の分の積算・増えた分）の見方を説明する。② Zed の ACP の表示は「1 会話の最後の応答の大きさ」かを答える（ガイド `token-cap-meter-reading.md` の基礎知識に「直近の応答の合計」とあり、ACP アダプタ 0.95.0 のコードで確認済み。答えはこれ）。③ `--session` を使った分解の実行例を出す。

## Open Questions

- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
