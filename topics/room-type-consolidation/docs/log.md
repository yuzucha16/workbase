# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に論点が広がった: works を「PC ローカルの台帳」と再定義し、開発用リポジトリを room の ext4 に置く（works と 1:N）。Zed からの読み書き・LSP・git・Agent は room の distro で確認できた。次は認証。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【次回の最初】room の中で非公開リポジトリを clone / push するための GitHub 認証を、SSH 鍵にするか `gh auth` にするか、ベストプラクティスをユーザーが AI に聞く。観点: room の AI から見える認証情報の範囲（読み取り専用にして push は人にするか）、リポジトリ単位の deploy key / fine-grained PAT、「部屋の中で clone（C 案）」を却下した理由（`ai-isolated-work-room.md` の 2026-10-13 の決定）との整合。
- 【方針の整理待ち】works の再定義（下の Open Questions 1）。認証の方式が決まってから、このトピックで決定として書くか、別トピックを立てるかを決める（AI は別トピックを推した。範囲が `--type` を超えるため）。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

1. works の再定義（ユーザーの整理、10-31。決定ではなく方針）: works と workbase は 1:1（Obsidian が見るのは `resources/`）。works と projects は 1:N の PC ローカルの台帳（remote なし）。成果物は `inv` が Office（Windows）、`dev` が WSL 内の git リポジトリ（N 個）。今のルールを works に合わせるのでなく、この定義に既存のルールを合わせに行く。
2. Project の README に `repos:`（`url` `where: wsl|win` `branch`）を持たせるか。`dev` は既定で `where: wsl`、`inv` は repo なし。
3. 閉じる条件に「room 内の clone が全部 push 済み」を足すか（room を作り直すと未 push の分が失われる）。
4. pc2 の works は公開 remote 付き。remote を外すとき、公開済みの成果物の切り出し先。
5. clone の置き場の規約（`~/src/<repo>` でよいか）。`ai/src` との関係。
6. 影響する文書: `obsidian-vault-structure.md`、`ai-isolated-work-room.md` の Decisions、`room.py` の `open`、`project-structure.md`。
7. 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
