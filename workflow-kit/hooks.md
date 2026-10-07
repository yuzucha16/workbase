# フックの呼び出し表（正本）

合言葉を受けたら、この表の「読むファイル」を読んで実行する。**この表の写しを、ほかの場所に作らない**（各 `AGENTS.md` には、この表への1行のポインタだけを置く）。合言葉は、ユーザーが言ったときだけ実行する（自発的には実行しない）。

| 合言葉 | 別名（日本語） | 読むファイル | 寿命・時機 | 要点 |
|---|---|---|---|---|
| `init` | 「workflowを導入して」 | `init-hook.md` | ワークスペース | 作業ディレクトリへの導入の入口（Vault のトップの生成を含む） |
| `open` | | `open-hook.md`（試験運用） | Project の開始 | Project のひな形を作り、`start` を呼ぶ |
| `start` | 「作業を始めて」 | `start-hook.md`（試験運用） | セッションの開始 | 開始インタビュー |
| `wrap` | 「終了処理して」 | `wrap-hook.md` | セッションの終了 | `docs/` の更新・棚卸し・ナレッジ化・コミットを、順序を固定して行う |
| `close` | | `close-hook.md`（試験運用） | Project の終了 | Project を閉じる |
| `stock` | 「ナレッジ化して」 | `stock-hook.md` | 随時 | 書き込みは `exmem/inbox/` の新規ファイルだけ（例外は `stock-hook.md`） |
| `integrate` | 「inboxを整理して」 | `integrate-hook.md` | 随時（exmem 側の作業） | `inbox/` のメモを `knowledge/` に統合し、台帳に記録する |
| `review` | 「見直して」 | `review-hook.md`（試験運用） | 週1回を目途 | チェック機能の集約先 |
| （常時） | | `docs-rules.md` | 作業を始める前と、`docs/` を更新するとき | `docs/` の運用規則 |

- 連鎖: `init`、`open → [start → 作業 → wrap]×N → close`。`stock` と `integrate` は随時。
- 上のファイルが読めない場合（`workbase` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。
- 旧ファイル名 `closing-hook.md` `knowledge-hook.md` `setup-hook.md` は、2026-10-08 に削除した（新名は `wrap` `stock` `init`）。履歴の中の旧名は、この表で読み替える。
