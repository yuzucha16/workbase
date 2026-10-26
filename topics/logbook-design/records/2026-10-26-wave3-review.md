# 第3陣の本文確認（2 ファイル）

日付: 2026-10-26。対象は `para-operations`（16KB）と `session-handoff`（19KB）。Facts・Open Questions・Next Actions・Decisions を読んだ（Principles は見出しと冒頭だけ）。**実装はしていない**。記号は第1陣と同じ（① 時系列、②一 版依存・一方向、②並 版依存・並存、③ 試行の途中、K 残す、X 1 回きり）。

## 1 ファイル別の仕分け

### para-operations（16KB）

| 節 | 字数 | 型 | 提案 | 確度 |
|---|---|---|---|---|
| Purpose / Principles / Decisions（2026-10-06） | 約 7.3k | K（一部 X） | 判断基準 8 項目と構造の決定は残す。open / close / 開始インタビューの連鎖の項は、2026-10-08 に名前が変わり、10-24 に `init`/`open` が廃止されている。古い名前の注があるが、現行の `room mkworks` / `brief` に合っているか確認して書き直す | 中 |
| Facts（採用率 66 件中 98%、最初の Project の開始インタビューの適合率など） | 約 2.4k | ① | 2026-10-06 の 1 回の測定（n=1 の Project）。`logbook/` の「明細」へ。`git mv` の `Permission denied` は `obsidian-vault` の Gotchas と重複 | 高 |
| Area と Project の間のデータの流れ / open の雛形の論点（未決） | 約 3.1k | K＋③ | 流れ（2026-10-07 決定）は残す。「open の雛形の論点（未決）」は、`open` 廃止（10-24）で前提が変わった。畳む候補 | 高 |
| Open Questions（9 項） | 約 1k | ③ | 重複が 2 組（上限 3/5 件の見直し、`archives/` へ移す契機）。`open`/`close` の前提のものは古い | 高 |
| Next Actions（5 項。2026-10-06〜07 時点） | 約 0.9k | ③ | Area の雛形、open の雛形、2 回目の Project の開始。`topics/` 型と `room` の整備で置き換わった可能性が高い。ユーザーに確認 | 高 |

- 版依存（②）はほぼ無い。性質は ① と古い ③。logbook に移すのは Facts の測定値だけ。

### session-handoff（19KB）

| 節 | 字数 | 型 | 提案 | 確度 |
|---|---|---|---|---|
| Purpose / Principles | 約 5.1k | K | 残す | 高 |
| Decisions（2026-10-10〜10-18 の 6 項） | 約 5.7k | K | 残す。3 行の型は「<名前> の続き」の 1 行に置き換わった経緯が書いてある。数値の目安（間 5 分、10 万／2 万トークン）は暫定で、TTL の項で置換済み | 高 |
| Facts（キャッシュ TTL、実験の費用、単価） | 約 4.6k | ②並＋① | 単価（Sonnet 5.5 の入力 $2、キャッシュ読み $0.10 など）と TTL（サブスク 1 時間、API 5 分）は版・時点に縛られる。印を付ける。実験の費用の数値（2026-10-17 の 1 回の測定）は ① で、`logbook/` の「明細」へ | 高 |
| Facts（2026-10-19 の部屋の自動化、状態表の古さ、議論の置き場） | 約 1k | K | 残す。状態表の古さは `log.md` の運用の一般則 | 中 |
| Gotchas | 約 1.2k | K | 残す | 中 |
| Open Questions（3 項） | 約 0.5k | ③ | 数値の目安の検証と TTL の確認。`review` の入力 5 に依存 | 中 |
| Next Actions（4 項。2026-10-17〜18 時点） | 約 0.5k | ③ | 期日が無く、誰も回していない可能性が高い。ユーザーに確認 | 中 |

- 近い内容が `topics/` 側のトークン節約の記録（`notes/token-saving/` の 10-15〜10-18）にもある。単価は 1 か所に寄せる。

## 2 この確認で分かったこと

1. 3 陣を通じて、降格（logbook へ移す）の対象は 3 ファイルの測定値だけ（①）。残りは、② の印と、X・古い ③ の畳み。
2. 古い ③ は、期日が無いために残っている。第1陣 `claude-code-storage`、第2陣 6 ファイル、第3陣 2 ファイルのすべてに出た。logbook の `review_by` より先に、lessons の Next Actions に日付を付けるだけでも減らせる（推測）。
3. 単価と TTL は複数のノートに散る（`session-handoff` `claude-code-auth-providers` ほか）。

## 3 3 段チェックに載せる単位（案）

1. `para-operations` の Facts を `logbook/` へ。古い ③ と未決の雛形の節を畳む。
2. `session-handoff` の実験の費用を `logbook/` へ。単価・TTL に印。古い ③ の畳み。
