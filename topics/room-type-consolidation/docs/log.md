# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。2026-10-31 に room の GitHub 認証と cwd（案 A）を実機で確認し、11-01 に Obsidian の Vault の 2 分割を仮決めした（実装は未着手）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【保留 〜11-08、起票 11-01、期日 11-09（③④の後）】Vault を `resources/` と `works/` の 2 つに分ける（`decisions.md` の 11-01 の項）。実体は両方 dotfiles で、resources 用が正本。works 用の共通ファイルは、反映のたびに生成する派生物で追跡しない（リンク適用時に自動、手動でも可、`--check` で点検）。実装の前に、入れ子の Vault（works の Vault から `resources/` などを除外する）の実機確認（③）と、今の `windows\obsidian\.obsidian` の移し先（④。works 用が自然）、pc1 のリンク調査、「Vault ＝ works」の文面の直し方の一覧を済ませる（期日 11-06、`docs/due.md`）。論点 3 の仕組みの詳細は dotfiles 側に置く（`decisions.md` のスクリーニング結果）。実装は dotfiles（`links.map`・反映スクリプト・試験・README。別コミット）、`resources/.gitignore` の `/.obsidian`、`app-config-placement.md` の更新。

- 【起票 11-01、期日 11-05】置き場の実測(実機)。ケース A(`src/` のみ)、B(`src/` `tests/` `docs/`)、C(`env/` `src/` `tests/` `docs/` `report.md`)を、置き場を依頼に書かずに通す。まず規則なしで `<成果物名>` の付け方を観察し、その後に `dev-deliverable-guide.md` へ「既定は Project 名と同じ」を書いて再測する(`decisions.md` の 11-01)。判定は、配置が `project-structure.md` の表どおりか、取り違えが再発しないか、聞き返したか。`due.md` の 11-05 の実機確認(`~/src/<repo>` など 5 点)と同時に行う。

## Open Questions

- 【期日 11-05。Next Actions の実測と同時】置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
