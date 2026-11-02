# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。2026-10-31 に room の GitHub 認証と cwd（案 A）を実機で確認し、11-01 に Obsidian の Vault の 2 分割を仮決めし、11-02 に入れ子の Vault の実機確認と `.obsidian` の写し先（works）を済ませた（実装は未着手）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【保留 〜11-08、起票 11-01、期日 11-09】Vault を `resources/` と `works/` の 2 つに分ける（`decisions.md` の 11-01 の項）。実体は両方 dotfiles で、resources 用が正本。works 用の共通ファイルは、反映のたびに生成する派生物で追跡しない（リンク適用時に自動、手動でも可、`--check` で点検）。11-02 に ③（除外フィルタは検索・リンクに効く。ファイルエクスプローラーには残る。入れ子の `.obsidian` は互いに独立）、④（今の `.obsidian` の写し先は works と決定）、pc1 のリンク調査（`resources/` を指すもの 0 本）、「Vault ＝ works」の文面の直し方の一覧が済んだ。`30_link.bat` が止まるのは、リンク先に実ファイル（実ディレクトリ）がすでにあるときだけで、ジャンクションなら上書きする（ユーザー確認）。これで前提は済んだので、正式化・却下をユーザーに聞く（期日 11-06）。論点 3 の仕組みの詳細は dotfiles 側に置く。実装は dotfiles（`links.map`・反映スクリプト・試験・README。別コミット）、`resources/.gitignore` の `/.obsidian`、`app-config-placement.md` などの文面（一覧は `decisions.md`）。

- 【起票 11-01、期日 11-05】置き場の実測(実機)。ケース A(`src/` のみ)、B(`src/` `tests/` `docs/`)、C(`env/` `src/` `tests/` `docs/` `report.md`)を、置き場を依頼に書かずに通す。まず規則なしで `<成果物名>` の付け方を観察し、その後に `dev-deliverable-guide.md` へ「既定は Project 名と同じ」を書いて再測する(`decisions.md` の 11-01)。判定は、配置が `project-structure.md` の表どおりか、取り違えが再発しないか、聞き返したか。名前を Project 名と同じにしたとき、AI が grep・find で階層を取り違えないかも見る。`due.md` の 11-05 の実機確認(`~/src/<repo>` など 5 点)と同時に行う。

## Open Questions

- 【期日 11-05。Next Actions の実測と同時】置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
