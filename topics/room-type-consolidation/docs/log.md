# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認（① 〜 ⑤）と置き場の実測（ケース A・B・C）を済ませ、`git -C` 緩和の反映（`ROOM.md` は `start` ごとに再生成されるので追加作業なし）と Vault 2 分割の両 PC 確認も済んだ。同日に、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用した。eg1（Web）の実験を済ませ、構造を直した（工程ログの提案 1・3・4 を反映）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【期日 11-11、起票 11-04】`inv` の工程別構造の実験 eg2（社内の Excel・テキスト。マスクの差分）を、別セッションで行う。eg1（Web）の結果と構造の直しは済み（`records/2026-11-04-inv-slide-tools-compare-result.md`）。結果は `records/` に残し、構造を直す。
- 【期日 11-11、起票 11-04】Marp と Slidev を部屋に入れて、Quarto と横並びで実機比較する（eg1 で npx が権限判定で拒否され、文書だけの評価になったため）。導入は人が行う（11-04 決定: 版を固定して部屋に `npm i -g` で入れる。AI は npx を使わず、導入済みのコマンドを実行する。`docs/decisions.md`）。導入後に、同じ qmd 相当の入力で pptx を出し、編集できるか・日本語・表・ノート・所要を比べる。結果は `topics/office-output-types` に渡す。

## Open Questions

- `inv` の基準文書は仮決めのまま（11-04 ユーザー「仮決めのままでよい」。見直しの期日は置かない）。
