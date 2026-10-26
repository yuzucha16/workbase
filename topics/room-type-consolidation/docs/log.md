# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。最初の実利用（`sample_dev` と `sample_inv`）の観察と、`env/` だけ・`tests/` だけ・`docs/` だけの実測を受け、手順書を直した（2026-10-25）。残りは、次の `dev` で置き場の取り違えが再発しないかの確認だけ。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【済 10-25】`report.md` の置き場: コードは `ai/out/deliverable/` だけ Area に、それ以外は `_noai/final/` に戻す。食い違いは `methods.md` の書き方だけだったので、`ai/out/<成果物名>/report.md` に直した。決定は要らなかった。
- 【済 10-25】単一の問いの章立て（`brief-hook.md`、`research-method.md`）。
- 【済 10-25】`dev` の「テスト」の節に、文書と実装の食い違いを機械で検査する型を足した(ユーザー承認)。
- 【済 10-25】`dev-deliverable-guide.md` の旧名（`dev-env` `dev-test`）の説明を削った(ユーザー承認)。
- 【済 10-25】`env/` だけの実測(`sample_devenv`): Ubuntu 24.04 実機で ENV-001〜010 全件 PASS、SET-001(root で中止)も確認。型(ID 付き検証項目、人が実機で確認する項目の分離)は機能した。静的検査は shellcheck と ruff が部屋に無く `bash -n` まで。uv の版は固定していない(実行時の最新)。
- 【済 10-25】`tests/` だけの実測(`sample_devtest`、成果物 `ai/out/devenv-tests/`): 要求 14 ID すべてに対応して実行(65 件実行、PASS 62、FAIL 3、SKIP 1)。型は機能した。対象の不具合 3 件と仕様の曖昧さ 2 件を `report.md` に書き、`ai/in/` は直さずハッシュで不変を確認した。観察: (1) 質問の推奨の置き場が `work/` で、ガイドの `ai/out/<成果物名>/` と食い違った(人が正した)。(2) テストを実装に合わせて緩めた件は、変更前後と理由を `report.md` に書かせた(依頼が要った)。(3) `tests/t_static.sh`(文書と実装の整合の検査)は、上の起票(型を足すか)の2例目。
- 【済 10-25】`docs/` だけの `dev` の実測(`sample_devdoc`)。「文書作成」の項は残す。基準文書の形を仮決め(`project-structure.md` の未決)。
- 【済 10-25】`room.py:1197`(`ROOM.md` の元)と `room-context.md:67` の「人が読む最終版」の記述を、「Area に実名で戻したい最終版だけ `deliverable/`。Project の成果物は `ai/out/<成果物名>/`」に直した。`brief-work-types.md` に、`dev` の最初の `brief` で `project-structure.md` と `dev-deliverable-guide.md` を読む指示を足した。`room` の単体テスト 139 件 OK(skip 3)。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方(`docs/` が運用マニュアルと重複するか)、置き場の取り違えの再発、検証が自己向けになって弱くならないか。分離した 3 本との差を知識として残す(ユーザー、10-25)。サブエージェントで一部のループを回す案は、未承認(`exmem/inbox/2026-10-25-procedure-validation-trial-runs.md`)。
- 【実施待ち】`dev` の成果物が `ai/work/` に出る件(2026-10-26、PC1 の `dev` の部屋。全件が一貫して `work/` で、`out/` と混在はしなかった)の原因を、部屋の AI に聞く方法で特定し、手順書を最適化する(ユーザー「部屋の AI に聞くやり方で最適化しましょう」)。10-25 の置き場の取り違えと同じ手順: 部屋の AI に「`ai/work/` に置いた理由と、そのとき読んだ手順書」を聞く。候補は 3 つ: (1) PC1 の写しが修正前(cfd3b81、10-25 22:35 より前。部屋の `~/shared/ROOM.md` の基準コミットで確かめる)、(2) `project-structure.md` の `work/`(試行、使い捨てのスクリプト)と `out/`(基準文書と検証を伴う最終成果物)の線が、基準文書の無い段階で曖昧、(3) `script-guide.md` が `verify-result.json` やログを `ai/work/` に出すと繰り返し書くので、`dev` のスクリプトが `work` の物と読まれる。(1) か (3) なら、`ROOM.md`(`room.py`)と `brief-work-types.md` に「コードやスクリプトも成果物は `ai/out/<成果物名>/`。`ai/work/` は捨ててよい下書きだけ」を明記する。ユーザーが PC1 で聞いた答えと基準コミット、その README の成果物の行を待つ。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。`ROOM.md` は `room start` が生成するので、既存の部屋は次の `room start` で更新される。

## Open Questions

- 置き場の取り違え 5 回の原因は特定した(`decisions.md`): `ROOM.md` と `room-context.md:67` の `ai/out/deliverable/` の記述が、`dev-deliverable-guide.md` と食い違う。直すのは上の起票。
- `sample_devenv` への不具合の返却は、しない(ユーザーの判断、10-25)。
- 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測(実測Aは依頼に書いた)。
- 成果物の形を AI が決める場面（依頼で指定が無いとき）は、まだ起きていない。
- `inv` の基準文書は仮決め（問い＋完了条件の 1 行）。複数の問いの調査で見直す。
- 既存の Project の README の旧 type 値（`doc` `dev-env` など）は、そのまま。読むコードが無いので影響なし。
