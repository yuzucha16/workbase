# stock の下書き回収: 引き継ぎ（2026-10-13）

ロードマップ4番のうち、`room stock <Project>` を実装した。単体テスト（45件）まで。実機は未確認。

## できたもの

- `room stock <名>`: `ai/out/stock/*.md` を1件ずつ人が確認して `resources/exmem/inbox/` に運ぶ。frontmatter の `base_commit` と `observed` が無い下書き、対応表の語を含む下書きは運ばない。基準以降に統合先の `lessons/` が変わっていれば `base_stale` を足す。manifest の `stock` に記録して二重に運ばない。コミットしない。
- 書き方は `workflow-kit/room-context.md` の「`stock` の下書きの書き方」。

## 解決した未決

- 下書きのヘッダー項目と `check-inbox.ps1`: スクリプトを読むと、決まった項目だけを見ていて、知らない frontmatter 項目は FAIL にしない（読んで確認。`pwsh` で実行はしていない）。PC で `pwsh` を使って、`base_commit` と `observed` と `base_stale` 入りのメモで確認する。
- Vault 側の AI が下書きを受け取る場所: Vault 側の AI を介さず、人が `room stock` で `exmem/inbox/` に直接運ぶ。

## 承認を得て反映した kit の変更（2026-10-13）

`integrate-hook.md` に「`base_stale` が付いたメモは、`base_commit` の版・下書き・最新の版の3点で照らして統合し、食い違いは Open Questions に書く。並べる順は `observed`」を足す。`workflow-kit/AGENTS.md` の規則で、ユーザーの承認が要るので、承認を得て、`integrate-hook.md` の「統合そのものの手順」に 2a として足した。

## PC での確認の結果（2026-10-14）

ダミーの下書き 4 件（架空の内容。基準が最新・基準が古い・ヘッダー欠け・対応表の語を含む）を `ai/out/stock/` に置き、`room stock` を実機で実行した。

| 確認 | 結果 |
|---|---|
| 基準が最新の下書き | 印なしで `exmem/inbox/` に運ばれた。同じ内容を再実行すると「済み」で飛ばされた |
| 基準が古い下書き | 「統合先の lessons が基準以降に変わった: reference-doc-types.md」と表示され、運ぶと frontmatter に `base_stale` が付いた |
| `base_commit` と `observed` が無い下書き | 運ばれなかった |
| 対応表の語を含む下書き | 運ばれなかった（語を表示して拒否） |
| `pwsh` の `check-inbox.ps1` | 追加の frontmatter 項目（`base_commit`、`observed`、`base_stale`）による FAIL は無い |

**未確認**: 実際の部屋の AI に下書きを書かせて運ぶ通し（ダミーは人が置いたファイル）。部屋の AI が `ROOM.md` に従って、先頭に基準コミットと観測日を付けられるか。
**残る小さな点**: `check-inbox.ps1` の FAIL（`tags` が 3〜6 個、Goal の末尾の形）は、ダミーの形が原因。運んだ下書きの形は、AI が `stock-hook.md` に従って書く。
