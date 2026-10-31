# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に、room の GitHub 認証（読み取り専用 deploy key、push は room に許さない）を実機で確認し、works の再定義と開発リポジトリの置き場を決めた（`docs/decisions.md` の「works の再定義と開発リポジトリの置き場」）。cwd は常に `/mnt/room/<Project>`（案 A）に決定し、`git -C ~/src/<repo>` が効くよう git ラッパーを直した（同日、実機で確認済み。`decisions.md` の「cwd は案 A に決定」）。Zed から room の ext4 上のコードを扱えることも確認済み。deploy key の手順書は `guides/howto/room-github-deploy-key-setup.md`（ユーザーが手で通して確認済み、11-01）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【実施待ち、案 A の実機確認もここでまとめる】1 Project で `env/` と `tests/` と `docs/` に加えて `src/`（コード開発）を通す実測（題材は同じ WSL の Python 環境。`repos:` を書いた `dev` の Project）。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか（ユーザー、10-25）。案 A の実装（`a9d03cc` `721f3f9`。単体テストのみ）の実機確認: ① `room start` で `~/src/<repo>` が `--add-dir` で渡り、その `CLAUDE.md` が読まれる ② AI が `git -C ~/src/<repo>` で commit でき、`ai/` に化けない ③ 修正した `ROOM.md` が届いて置き場の取り違えが再発しない ④ `room close` が未 push の clone で止まる ⑤ 対話での `cd` 後の cwd の持続（未測）。
- 【未反映】`obsidian-vault-structure.md` に works の再定義（works と workbase は 1:1、projects は 1:N の PC ローカルの台帳）を反映する。

## Open Questions

- `target:`（サーバーを使う Project の実行環境の記述）の書式と、`ai/in/target/` に置くものの一覧。
- サーバー側で AI を動かす形（room の外のモード）の設計。今は対象外。
- 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
