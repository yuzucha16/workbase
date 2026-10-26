# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。26 日時点で 90%（約 1.8 億、1 日約 700 万）。キャッシュ読みを含む数かは未確認。上限は PC1 のもので、PC1 と PC2 は別々に数える。
- PC2 の `cap_meter.py` 実測（`records/2026-10-26-cap-meter-pc2.md`）: 合計 2.33 億、応答 2,412（平均 96.5k）。60k 超は件数の 74%、トークンの 89%。土台は中央値 27.9k。60k で切ると平均 約 44k（約 54% 減の見込み）。10-25 と 10-26 が運用前の比較の基準。理解ガイドの下書きは `exmem/inbox/2026-10-26-token-cap-meter-reading.md`。
- 切る目安は 60k（会話の大きさ）で、2026-10-27 から運用。`cap_meter.py --latest` で最新の会話の積算が出る。
- 角度の一覧は `records/2026-10-26-angles.md`。優先は、会話を切る → ベーストークン → AI の線引き。間（TTL）とモデルの切替は、上限の重み付けが分かるまで保留。haiku 案は、重み付けかモデルごとの枠があるときだけ効く。主因はマクロの全面実装（`records/2026-10-26-macro-split.md`）。
- 会話の伸びの原因（`records/2026-10-26-growth-by-reads.md`）: 土台は固定で約 28k、その先はファイルの全文読みが支配的。読む量の一手は一巡済み。見込みの実測は 10-27 以降。
- 土台の skills を整理した（10-27、`records/2026-10-27-skills-trim.md`）。Zed の Skills は 5.8k → 3.5k（−2.3k）、土台は 19.4k → 19.7k。差は System tools が 7.6k → 9.9k に増えたため（原因不明。再起動でも戻らず、ハーネス側とみる）。
  - 切った: claude.ai 同期の `skill-creator` `google-workspace` `deep-research` `import-memory` `morning`、`docs` `computer-use` `built-in-browser` `chrome-browser`（claude.ai の Customize > Skills でオフ。ローカルで消しても再同期される）。obsidian プラグイン 6 件は Claude Code で uninstall（Zed にも出ない）。
  - 残した: `xlsx` `docx` `pptx` `pdf`（約 1.1k。ee の判断）。残りの 2.2k は組み込みで外せない。
- 下準備は `records/2026-10-26-desk-prep.md`、`/context` の実測は `records/2026-10-26-context-measure.md`。

## Next Actions

1. 【起票 10-26】ee が PC1 で取る（予定 10-27）: `cap_meter.py`、`usage_report.py --by month --last 2 --top 10`、`heavy_sessions.py --since 2026-10-01 --top 10`（`python -I workflow-kit/tools/` の下）。題名に機密が出ていないか見てから、集計だけを持ち帰る。
2. PC1 の分が届いたら、PC2 の見積もりと比べ、上位の会話の作業の種類（マクロの実装か）を見る。10-27 以降は `cap_meter.py` の日ごとの値で、60k 運用の前後を比べる。
3. 勤務先に、上限の数え方（読みを含むか、モデルの重み、Desktop の分）を確かめる。文面は `records/2026-10-26-desk-prep.md` の 4（ee が送る）。
4. マクロの現況を聞いて、役割分割の案（基準文書、部品化、台帳）を具体化する。
5. 切る基準を「会話の大きさ」と「会話ごとの積算」のどちらにするか、PC1 の実測で決める（当面は 60k）。
6. `AGENTS.md` の整理は、60k 運用の結果を見てから再判断する（案は `records/2026-10-26-base-trim.md`）。

## Open Questions

- Desktop（添付やチャット）の分が上限にどれだけ入っているか。
- マクロの会話を `brief` でなく「<名前> の続き」で始めるか（B1）、`hooks.md` の表を分けるか（B3）。
- Zed の System tools が 9.0k → 9.9k に増えた原因（10-27 に増加。`/reload-skill` の後。再起動でも戻らず）。
