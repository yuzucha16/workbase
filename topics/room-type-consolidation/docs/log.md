# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に、room の GitHub 認証（読み取り専用 deploy key、push は room に許さない）を実機で確認し、works の再定義と開発リポジトリの置き場を決めた（`docs/decisions.md` の「works の再定義と開発リポジトリの置き場」。cwd は案 A で、実測前）。Zed から room の ext4 上のコードを扱えることも確認済み。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【案 A に決定、ラッパー改修は済み 10-31】cwd は常に `/mnt/room/<Project>`、`~/src/<repo>` は `--add-dir`（`records` を `ai/records` の一か所に保つため）。実測（`room-myenv`、`claude -p`）: `--add-dir` で読み書きできる。`records` は `ai/records` に出る。`CLAUDE.md` は `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` のときだけ読まれる。`ROOM_GIT_WRAPPER` が `$PWD` だけで判定して `git -C ~/src/<repo>` が部屋用 git に化けたので、git の対象（cwd に `-C` を順に当てる）で判定するよう直した（`--git-dir` `--work-tree` `--bare`、`GIT_DIR` 設定済み、`clone` は素通し）。単体テスト `RoomGitWrapperTest`（全 140 件 OK）と実機（`git -C` の add/commit、ローカル clone、AI の commit）で確認。**実機の `/usr/local/bin/git` は新版に差し替え済み**（次の `start` でも同じものが入る）。
  - 残り: `room start` が `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` を渡す。`repos:` の clone を `--add-dir` で渡す（`open`/`start` の実装）。対話での `cd` 後の cwd の持続は未測（AI には `git -C` を使わせる）。
- 【影響する文書の更新】10-31 の決定を、`obsidian-vault-structure.md`、`ai-isolated-work-room.md` の Decisions、`room.py` の `open`、`project-structure.md`（`repos:` と `target:` の項目）に反映する。案 A の実測の後。
- 【起票 10-31】`room close` に、未 push の clone を検出する検査を足す（`decisions.md` の 10-31 の項）。`repos:` と置き場は決まったので、実装できる。room は Area ごとで `~/src` は Project をまたいで共有されるため、README の `repos:` で Project と clone を対応づけて検査する。push は room に許さないので、未 push は人が room の外から push する。
- 【ユーザー作業、手すきで】deploy key の作成を自分でもう一度やる（手順は `log-history.md` の 10-31）。手順書にするかは、やってみてから決める。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

- `target:`（サーバーを使う Project の実行環境の記述）の書式と、`ai/in/target/` に置くものの一覧。
- サーバー側で AI を動かす形（room の外のモード）の設計。今は対象外。
- 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
