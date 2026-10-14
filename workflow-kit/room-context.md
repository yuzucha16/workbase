# 部屋の中でフックを使うとき

AI 作業部屋（`workflow-kit/room/`）の中で、合言葉のフックを使うときの読み替えと分担。`hooks.md` の表が正本で、ここは部屋の中での差分だけを書く。部屋でないときは読まない。

## 2つの層

| | 運用コマンド（`room …`） | 合言葉のフック |
|---|---|---|
| 呼ぶ人・場所 | 人が Windows の端末で打つ | 人が言い、AI が手順書を読んで実行 |
| 性質 | 決まった手順の副作用（マウント、写しの送付、マスク、移動、コミット） | 判断（聞き取り、確認、振り分け、下書き） |
| 実行者 | スクリプト。**AI は実行しない** | AI |

同じ名前（`open` `start` `close`）が両方にあるときは、運用コマンドには必ず `room` を前置し、合言葉は日本語の別名で呼ぶ。2つをつなぐのは**ファイルの受け渡しだけ**。

## 部屋の中の読み替え

- 起動する場所は `/mnt/room/<名>`（Project の `ai/`）に固定される。開始時に読むのは `~/shared/ROOM.md` → `ai/ctx/README.md`（Project の窓口の写し）→ `ai/ctx/area-README.md`（所属する Area の README の写し。Area の共通ルール）→ `ai/docs/log.md`。
- 手順書の `docs/` は、部屋では `ai/docs/`（Project の記録）。Project と Area の `README.md` は書き込めない。写し（`ai/ctx/README.md`、`ai/ctx/area-README.md`）を読む。
- 手順書は `~/shared/workflow-kit/` にある（読み取り専用の写し。基準コミットは `~/shared/ROOM.md`）。
- 副作用を伴う手順（Project の作成、状態の更新、`archives/` への移動、コミット）は AI が行わない。判断をファイルに書いて、人が `room` で反映する。

## `stock` の下書きの書き方（部屋の中）

`ai/out/stock/YYYY-MM-DD-<topic>.md` に、`stock-hook.md` の形式で書く。frontmatter に次の2つを足す（点検スクリプトは、知らない項目があっても FAIL にしない）。

- `base_commit: <~/shared/ROOM.md の基準コミット>`
- `observed: YYYY-MM-DD`（観測した日。並べる順は到着順でなく、この日付）

人が `room stock <名>` で確認して `exmem/inbox/` に運ぶ。基準以降に統合先の `lessons/` が変わっていると、`base_stale` が付く。`integrate` は、印が付いたメモを、基準の版・下書き・最新の版の3点で照らして統合する（食い違いは Open Questions）。

## 分担と受け渡し

| 場面 | AI（部屋の中）が行う | 人（`room`）が行う | 受け渡しのファイル |
|---|---|---|---|
| `open` | 目的・完了条件の聞き取りと README 本文の下書き | `room open <名>`（ひな形）→ `room readme <名>`（下書きの反映） | `ai/out/readme-draft.md`（本文だけ。frontmatter を含めない） |
| `start` | 開始インタビュー | `room start <名>`（チェック、マスク、写しの送付、マウント、起動） | `ai/ctx/`、`ai/in/` |
| `wrap` | `ai/docs/` の更新、昇格の案 | 回収（復元、コミット） | `ai/docs/log.md`、`ai/docs/decisions.md`（Area へ渡す項目に【案件】ラベル） |
| `close` | 完了条件の確認、暫定の見直し、未解決の振り分け、【汎用】候補の提示 | `room close <名>`（Area へ転記、状態の更新、`archives/` へ移動） | `ai/out/close.md` |
| `stock` | 下書きまで | `room stock <名>`（人が1件ずつ確認して `exmem/inbox/` へ運ぶ） | `ai/out/stock/`（先頭に基準コミットと観測日） |
| `integrate` `review` | 部屋では行わない（Vault 側の workbase の作業） | — | — |
| `init` | 部屋では行わない（ワークスペースへの導入。部屋の作成は `room` の手順） | — | — |
