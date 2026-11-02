# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。2026-10-31 に room の GitHub 認証と cwd（案 A）を実機で確認し、11-01 に Obsidian の Vault の 2 分割を仮決めし、11-02 に入れ子の Vault の実機確認と `.obsidian` の写し先（works）を済ませた（実装は dotfiles に入れ、動作確認 a〜e も問題なしで閉じた）。「Vault ＝ works」の文面直しも 11-02 に済んだ（`README.md` `AGENTS.md` `exmem/` `templates/workspace/` `ai-room-why.md`）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【起票 11-01、期日 11-05】置き場の実測(実機)。ケース A(`src/` のみ)、B(`src/` `tests/` `docs/`)、C(`env/` `src/` `tests/` `docs/` `report.md`)を、置き場を依頼に書かずに通す。まず規則なしで `<成果物名>` の付け方を観察し、その後に `dev-deliverable-guide.md` へ「既定は Project 名と同じ」を書いて再測する(`decisions.md` の 11-01)。判定は、配置が `project-structure.md` の表どおりか、取り違えが再発しないか、聞き返したか。名前を Project 名と同じにしたとき、AI が grep・find で階層を取り違えないかも見る。`due.md` の 11-05 の実機確認(`~/src/<repo>` など 5 点)と同時に行う。

## Open Questions

- 【期日 11-05。Next Actions の実測と同時】置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
