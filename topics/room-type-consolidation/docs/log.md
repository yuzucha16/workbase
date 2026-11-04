# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認（① 〜 ⑤）と置き場の実測（ケース A・B・C）を済ませ、`git -C` 緩和の反映（`ROOM.md` は `start` ごとに再生成されるので追加作業なし）と Vault 2 分割の両 PC 確認も済んだ。同日に、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用した（実験は未）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【期日 11-11、起票 11-04】`inv` の工程別構造（素案は `project-structure.md` の `inv` の構成要素。11-04 に採用）の実験を、別セッションで観点別に行う。最初は eg1 を通しで 1 回: お題は「プレゼン資料作成ツールの比較（Marp、Quarto、Slidev）。AI 活用を想定した選定軸と、作成時間短縮の方法」。`report.md` の清書（`publish/`）をこれらでできないか、という `topics/office-output-types` の検討（markdown → pptx。Quarto は部屋に導入済み）のインプットになる。調査の起点は `guides/explain/markdown-to-pptx-quarto-explain.md`。次に eg2（社内 Excel・テキスト。マスクの差分）。結果は `records/` に残し、構造を直す。

## Open Questions

- `inv` の基準文書は仮決めのまま（11-04 ユーザー「仮決めのままでよい」。見直しの期日は置かない）。
