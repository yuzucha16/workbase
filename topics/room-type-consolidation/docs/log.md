# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に論点が広がった（works を PC ローカルの台帳と再定義し、開発用リポジトリを room の ext4 に置く 1:N）。その認証は、読み取り専用 deploy key（SSH）で通った。works の再定義と `repos:` は、別トピックで扱う（ユーザー、10-31）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【次回の最初】別トピックを立てる（名前はユーザーが決める。例: `dev-repos-in-room`）。Open Questions 1〜6（works の再定義、`repos:`、閉じる条件、pc2 の remote、clone の置き場、影響する文書）をそこへ移し、このトピックからは消す。`room close` の「部屋の中の clone が全部 push 済み」の検査（ユーザー承認済み、10-31）は、`repos:` と置き場の後にそこで実装する。room は Area ごとで `~/src` を Project をまたいで共有するので、`repos:` が無いと別の Project の clone で止まる。
- 【ユーザー作業】GitHub の確認用リポジトリ `yuzucha16/room-auth-check` を消す（`gh` に `delete_repo` の権限が無く、AI は消せなかった。Web の Settings か、`gh auth refresh -h github.com -s delete_repo` の後に `gh repo delete`）。room 側の鍵と clone は消した。
- 【ユーザー作業】deploy key の作成を自分でもう一度やる（手順は `log-history.md` の 10-31。リポジトリ作成 → room で `ssh-keygen -t ed25519` → Deploy keys に公開鍵を登録（Allow write access は付けない）→ `~/.ssh/config` の別名 → clone）。手順書にするかは、やってみてから決める。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

別トピックへ移す予定（上の【次回の最初】）。

1. works の再定義（ユーザーの整理、10-31。決定ではなく方針）: works と workbase は 1:1（Obsidian が見るのは `resources/`）。works と projects は 1:N の PC ローカルの台帳（remote なし）。成果物は `inv` が Office（Windows）、`dev` が WSL 内の git リポジトリ（N 個）。今のルールを works に合わせるのでなく、この定義に既存のルールを合わせに行く。
2. Project の README に `repos:`（`url` `where: wsl|win` `branch`）を持たせるか。`dev` は既定で `where: wsl`、`inv` は repo なし。
3. 閉じる条件に「room 内の clone が全部 push 済み」を足す（決定済み、10-31）。実装の前提は 2 と 5。push は room に許さないので、未 push は人が room の外から push する。
4. pc2 の works は公開 remote 付き。remote を外すとき、公開済みの成果物の切り出し先。
5. clone の置き場の規約（`~/src/<repo>` でよいか）。`ai/src` との関係。
6. 影響する文書: `obsidian-vault-structure.md`、`room.py` の `open`、`project-structure.md`（`ai-isolated-work-room.md` の Decisions は 10-31 に更新済み）。
7. 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
