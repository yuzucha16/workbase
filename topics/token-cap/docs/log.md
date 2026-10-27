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

1. 骨子の残り（任意）: PC2 と room で要因別の分解を同じ方法で行う。room の 107k（10-27 03:22）の確認は後日: 道具 `decompose_session.py` を置いた（10-27、ダミーでのみ確認）。PC1 の room で `python3 -I topics/token-cap/decompose_session.py --at 2026-10-27T03:22 /home/ai/.claude/projects`（先に pull）。172k の型は `records/2026-10-27-pc2-one-request-172k.md`。
2. `integrate` の読む量の上限（`integrate-hook.md`、仮 〜11-29）と lessons の分割（全 6 本）は済み。効果は 10-27 以降の日ごとの値で測る。`--check-triggers` の FAIL 1 件は `claude-code-cost-session-size.md` の 16 語（別件）。
3. （低優先）マクロ側の常駐文書に、全文読みを避ける指示を入れる案。マクロの現況は閉じた（ee の決定 10-27）。
4. `room reap` の退避は済み。残り: `-home-ai`（Project に紐づかない履歴）は退避も削除もしない。部屋を直接消す場合は手で退避する。
5. 土台の整理（`AGENTS.md` など）は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`。前倒しはしない。ee の決定 10-27）。**漏らさない**: 土台は区切りまでの余裕を食い、1 会話の依頼数を減らす（作業性）。再判断のときは、動かせる土台の内訳を先に測る。
6. 【起票 10-28、hook-room-alignment から】`brief` の引数（モード）を絞るか: 100k で 3 会話が限界だと、開始時に `brief-hook.md`（8KB）+ `brief-modes.md`（4.9KB）+ `brief-work-types.md`（3.3KB）で最大 約 7k トークンが以後に乗り、型で聞く往復も増える（概算）。10-18〜27 のログでは引数つきは 10 回で、改善 5・振り返り 4・計画 1、解決・変更・調査は 0。案: 引数なしの `brief` + 普通の依頼文を主にし、使われないモードを削る。**残す条件**: 型の価値は入力より出力（応答の型）にある（ee、調査と改善/振り返りで特に）。削るのは聞き取りの型で、出力の型は残す。未決（ee の決定待ち）。使用回数は暫定（別名は数えていない、ログは 10-19 以降のみ）。追加案（10-28）: 出力の型を依頼の言葉（`triggers:`）で呼び、`brief` の引数を入力と出力に分けて設計する。ee は好意的。概要と具体例は `records/2026-10-28-brief-input-output-split.md`。 机上の測定（10-28）: 引数つきの開始時の読み込みは 約 7k ではなく 17〜24k（`methods.md` 全文とやり方のノートまで読むため）。出力の型だけなら 1 型 0.5〜2k。今の索引は「振り返って」に当たらず、「振り返り」では元のノート 2 本（約 15.5k）を出す。案（Must 3 点）と判断の材料は `records/2026-10-28-brief-mode-load.md`。 **振り返りだけで試す**（ee の決定 10-28）: 型のノート 2 本（`retrospective-method-output` 6.7KB、`-2-output` 2.8KB）に切り出し済み。索引は「振り返って」で 2 本 計 9.5KB（約 4.5k。前は該当なし、「振り返り」では 33KB）を出す。残り: ee が次の daily / weekly を「振り返って」で頼み、開始時の大きさ（`cap_meter.py --latest`）と出力の形が保てたかを見る。良ければ調査・計画に広げ、`brief` の引数をやめる。

## Open Questions

- 差の約 16M の出どころ（10-01〜08 の分、Desktop）は取らない（ee の決定 10-27）。
- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
