# stock の下書き回収: 引き継ぎ（2026-10-13）

ロードマップ4番のうち、`room stock <Project>` を実装した。単体テスト（45件）まで。実機は未確認。

## できたもの

- `room stock <名>`: `ai/out/stock/*.md` を1件ずつ人が確認して `resources/exmem/inbox/` に運ぶ。frontmatter の `base_commit` と `observed` が無い下書き、対応表の語を含む下書きは運ばない。基準以降に統合先の `lessons/` が変わっていれば `base_stale` を足す。manifest の `stock` に記録して二重に運ばない。コミットしない。
- 書き方は `workflow-kit/room-context.md` の「`stock` の下書きの書き方」。

## 解決した未決

- 下書きのヘッダー項目と `check-inbox.ps1`: スクリプトを読むと、決まった項目だけを見ていて、知らない frontmatter 項目は FAIL にしない（読んで確認。`pwsh` で実行はしていない）。PC で `pwsh` を使って、`base_commit` と `observed` と `base_stale` 入りのメモで確認する。
- Vault 側の AI が下書きを受け取る場所: Vault 側の AI を介さず、人が `room stock` で `exmem/inbox/` に直接運ぶ。

## 承認が要ること（kit の変更）

`integrate-hook.md` に「`base_stale` が付いたメモは、`base_commit` の版・下書き・最新の版の3点で照らして統合し、食い違いは Open Questions に書く。並べる順は `observed`」を足す。`workflow-kit/AGENTS.md` の規則で、ユーザーの承認が要るので、まだ変えていない。

## PC で確認すること

1. 実際の部屋で下書きを書かせ、`room stock` で運べるか。`base_stale` の印が正しく付くか（`resources/` が git であること）。
2. `pwsh` で `check-inbox.ps1` が、追加の frontmatter 項目で通るか。
