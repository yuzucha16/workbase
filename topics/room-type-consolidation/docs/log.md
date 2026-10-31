# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に、room の GitHub 認証（読み取り専用 deploy key、push は room に許さない）を実機で確認した。works の再定義などの論点（Open Questions）は見送った（ユーザー、10-31）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【ユーザー作業】deploy key の作成を自分でもう一度やる（手順は `log-history.md` の 10-31。リポジトリ作成 → room で `ssh-keygen -t ed25519` → Deploy keys に公開鍵を登録（Allow write access は付けない）→ `~/.ssh/config` の別名 → clone）。手順書にするかは、やってみてから決める。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

なし（10-31 に見送り。元の論点 7 件は `log-history.md` の 10-31 に残してある）。
