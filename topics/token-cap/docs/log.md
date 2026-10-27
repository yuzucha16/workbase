# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%（約 1.8 億）。キャッシュ読みを含む数かは未確認。
- **PC1 は 2 か所に分かれていた**。10-09〜10-20 は Windows 側（91.85M。`records/2026-10-27-pc1-meter.md`）、10-21〜10-27 は room（WSL）側（78.80M、37 会話、1,056 応答。`records/2026-10-27-pc1-room-meter.md`）。合算 約 170.7M（85%）。10-26 までの合算は約 164.1M で、勤務先の表示との差は約 16M（10-01〜08 の分、Desktop、別端末のいずれか）。
- room の会話記録の置き場は `/home/ai/.claude/projects/`（`/mnt/room/<Project>/records` ではない）。部屋を消すと記録も消える。
- room の土台は中央値 約 18k（Windows 側は 31k）。60k 超の応答は 56%（トークンの 78%）、1 応答の平均 約 75k（Windows 側は 124k）。
- 残りは約 29M（10-27 時点）。10-26 の 1 日分（23.7M）の勢いなら 1〜2 日で尽きる。**ee は今月の残りの重い作業を止める**（10-27）。
- 切る目安は「作業の区切り（Task 1 件）、または 100k」の早いほう（変更なし。`docs/decisions.md`）。
- 解説は `guides/explain/claude-code-cost-session-size.md`。未統合の下書き `exmem/inbox/2026-10-26-token-cap-meter-reading.md` の統合先候補はこのガイド。

## Next Actions

1. **別セッションで、PC1 と PC2 のデータを分析する**（傾向と対策。ee が言った。10-27）。入力: `records/` の PC1（Windows、room）と PC2 の実測。
2. room の会話記録を、部屋を消す前に退避する手順を作る（ee が決めた。10-27）。置き場は `/home/ai/.claude/projects/`。`room close` と、集計の `--root` との結びつけを検討する。
3. 勤務先に、上限の数え方（読みを含むか、モデルの重み、Desktop の分）を確かめる（文面は `records/2026-10-26-desk-prep.md` の 4。ee が送る）。
4. マクロ側の常駐の文書に、ファイルの全文読みを避ける指示を入れる案を、ee と相談する。マクロの現況（`records/2026-10-26-macro-split.md` の末尾）を聞いて、役割分割を具体化する。
5. `AGENTS.md` の整理は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`）。

## Open Questions

- Desktop（添付やチャット）の分が上限にどれだけ入っているか。差の約 16M の出どころ。
- マクロの会話を `brief` でなく「<名前> の続き」で始めるか（B1）、`hooks.md` の表を分けるか（B3）。
- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
