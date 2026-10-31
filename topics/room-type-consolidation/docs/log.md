# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。手順書の実測の修正も済み（10-25）。2026-10-31 に、room の GitHub 認証（読み取り専用 deploy key、push は room に許さない）を実機で確認した。あわせて Zed から room の ext4 上のコードを扱えることも確認した（編集、LSP、git 表示、Agent）。「works の再定義」の論点は、このトピックで続ける（別トピックにしない。ユーザー、10-31）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【方針の整理】works の再定義（Open Questions 1）を、このトピックで続ける。決まったら `decisions.md` に書く。
- 【起票 10-31】`room close` に、未 push の clone を検出する検査を足す（`decisions.md` の 10-31 の項）。注意: room は Area ごとで `~/src` は Project をまたいで共有されるので、Project との対応が無いと別の Project の clone でも止まる。push は room に許さないので、未 push は人が room の外から push する。実装は Open Questions 2・5 の後。
- 【ユーザー作業】deploy key の作成を自分でもう一度やる（手順は `log-history.md` の 10-31）。手順書にするかは、やってみてから決める。
- 【実施待ち】1 Project で `env/` と `tests/` と `docs/` を通す実測(題材は同じ WSL の Python 環境)。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか(ユーザー、10-25)。
- 【確認待ち】直した `ROOM.md` が部屋に届いたあと、次の `dev` の実測で置き場の取り違えが再発しないか。

## Open Questions

1. works の再定義（ユーザーの整理、10-31。方針で、決定ではない）: works と workbase は 1:1（Obsidian が見るのは `resources/`）。works と projects は 1:N の PC ローカルの台帳（remote なし）。成果物は `inv` が Office（Windows）、`dev` が WSL 内の git リポジトリ（N 個）。今のルールを works に合わせるのでなく、この定義に既存のルールを合わせに行く。
2. Project の README に `repos:`（`url` `where: wsl|win` `branch`）を持たせるか。`dev` は既定で `where: wsl`、`inv` は repo なし。
3. 閉じる条件「room 内の clone が全部 push 済み」: 決定済み（10-31）。実装は Next Actions 2。
4. pc2 の works は公開 remote 付き。remote を外すとき、公開済みの成果物の切り出し先。
5. clone の置き場の規約（`~/src/<repo>` でよいか）。`ai/src` との関係。
6. 影響する文書: `obsidian-vault-structure.md`、`ai-isolated-work-room.md` の Decisions、`room.py` の `open`、`project-structure.md`。
7. 置き場と対象環境を依頼に書かないとき、AI が聞き返すかは未測。成果物の形を AI が決める場面はまだ無い。`inv` の基準文書は仮決め。
