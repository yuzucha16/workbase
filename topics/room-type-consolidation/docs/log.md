# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に、room の GitHub 認証（読み取り専用 deploy key、push は room に許さない）を実機で確認し、works の再定義と開発リポジトリの置き場を決めた（`docs/decisions.md` の「works の再定義と開発リポジトリの置き場」）。cwd は常に `/mnt/room/<Project>`（案 A）に決定し、`git -C ~/src/<repo>` が効くよう git ラッパーを直した（同日、実機で確認済み。`decisions.md` の「cwd は案 A に決定」）。Zed から room の ext4 上のコードを扱えることも確認済み。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【実装済み 10-31、実機は未確認】`room.py` の `cmd_start` が、`claude` のとき `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` と、README の `repos:`（`where: wsl`、既定）の `~/src/<repo>` への `--add-dir` を渡す（`read_repos` `claude_extra_args`。部屋に clone が無ければ注意を出して渡さない。単体テスト済み）。残り: 実機で `room start` し、追加ディレクトリの `CLAUDE.md` が読まれるか確かめる。対話での `cd` 後の cwd の持続は未測。
- 【反映済み 10-31】`ROOM.md`（`ROOM_GUIDE`）に `git -C ~/src/<repo>` と push 不可を追記。`project-structure.md` に `repos:` の節、`ai-isolated-work-room.md` の Decisions に案 A、`room open` の README 雛形に `repos:` の案内。`obsidian-vault-structure.md`（works の再定義）は未反映。
- 【実装済み 10-31、実機は未確認】`room close` が、README の `repos:` の clone に未コミット・未 push があれば止める（`unpushed_repos`。単体テスト済み）。
- 【ユーザー作業、手すきで】deploy key の作成を自分でもう一度やる（手順は `log-history.md` の 10-31）。手順書にするかは、やってみてから決める。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

- `target:`（サーバーを使う Project の実行環境の記述）の書式と、`ai/in/target/` に置くものの一覧。
- サーバー側で AI を動かす形（room の外のモード）の設計。今は対象外。
- 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
