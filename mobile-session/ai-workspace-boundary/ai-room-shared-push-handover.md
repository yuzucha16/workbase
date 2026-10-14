# 共有知の写しを部屋へ入れる: PC への引き継ぎ（2026-10-13）

ロードマップ2番（方式 A）を実装した。**単体テスト（40件）まで。実際の WSL では未確認**。

## できたもの

- `room start` が、マウントの前に `<Vault>/resources/` の `AGENTS.md`、`workflow-kit/`、`exmem/{AGENTS.md,README.md,tags.md,lessons/}`、`guides/` を tar.gz にして、部屋の一般ユーザーの `~/shared` へ送る。読み取り専用（`chmod -R a-w`）。次の起動で入れ替える（先に `u+w` に戻して消す）。
- 基準コミットと「未コミットの変更の有無」を、`ai/records/manifest.json` の `shared` に記録。`~/shared/ROOM.md` に、基準コミットと読む場所の案内、`stock` の下書きの書き方（`ai/out/stock/`、ヘッダーに基準コミットと観測日）を置く。
- `resources/` が無い Vault では、送らずに続ける。

## PC で確認すること

1. 実際の部屋で `room start` → 部屋の AI が `~/shared/ROOM.md` と `~/shared/workflow-kit/hooks.md` を読めるか。書き込めないか。
2. 送る時間とサイズ（`guides/` と `lessons/` が増えたとき）。遅ければ、範囲を絞るか差分にする。
3. `resources/` の位置が、PC の Vault（`$HOME\works\resources`）と合っているか。
4. 部屋の `~/CLAUDE.md` などから `~/shared/ROOM.md` へ案内する（部屋の作成手順に足す。未実施）。
5. 部屋の AI が、合言葉（`start` `wrap` など）で `~/shared/workflow-kit/*-hook.md` を読んで動けるか（`pwsh` 製の道具は動かない）。

## PC での確認の結果（2026-10-14）

実際の部屋（`room-<Area>`）で、架空のダミー Project に `room start --no-launch` を実行して確認した。

| 確認 | 結果 |
|---|---|
| 1 読める・書き込めない | `~/shared/ROOM.md` と `workflow-kit/hooks.md` を一般ユーザーで読めた。`touch` は `Permission denied`（ディレクトリは `dr-xr-xr-x`） |
| 2 時間とサイズ | 1.5MB、120ファイル。送付は数秒で、遅さは感じなかった。`guides/` と `lessons/` が増えたら再測定 |
| 3 `resources/` の位置 | Vault の `resources/` から送れた。manifest の `shared` に基準コミット、`dirty`、送付時刻、tar の sha256 が入った。`ai/ctx/SHARED.md` も作られた |
| 4 部屋の AI への案内 | 実装した（ユーザーが方式 A を選択）。`room start` が、部屋の `~/.claude/CLAUDE.md` に `~/shared/ROOM.md` への案内を、目印で囲んだ範囲だけ入れ替えて置く。**`~/CLAUDE.md` ではない**: 作業ディレクトリは `/mnt/room/<Project>` なので、`~` の直下の `CLAUDE.md` は読まれない。`~/.claude/CLAUDE.md` は作業ディレクトリによらず読まれる。部屋で `sh -s` を2回実行して、ブロックが1つだけ・既存の行が残ることを確認した。次の `room start` で、実際の部屋に入る |
| 5 部屋の AI が合言葉で動けるか | **読むところまで確認した**（2026-10-14）。案内（`~/.claude/CLAUDE.md`）に従い、AI が `ROOM.md` → `hooks.md` → `wrap-hook.md` → `hook-common.md` → `room-context.md` を順に読んだ。**手順の実行の完遂は未確認**（`wrap` の最後まで通す、`pwsh` 製の道具が動かない場合の挙動）。`~/shared` は作業ディレクトリの外なので、Claude Code が「作業ディレクトリ外の読み取りを許可するか」を毎回聞く（下の「未解決」） |

**見つけて直した不具合**: 初回の `room start` が `mkdir: cannot create directory ''` で止まった。`wsl.exe -- sh -c "<script>"` は、引数を部屋の側の外側のシェルでもう一度解釈するので、スクリプト内で代入した変数（`$d`）が空に展開される。`$HOME` は外側でも定義されているので問題ない。変数を使わず `"$HOME/shared"` を直接書くようにした（コミット `930b8ac`）。**WSL を差し替える単体テストでは検出できない**ので、`wsl.exe` に渡す `sh -c` のスクリプトでは、スクリプト内で代入した変数を使わない。

**未解決（項目5で扱う）**: `--no-launch` で待っている間、別の `wsl.exe` セッションから見ると、`/mnt/room/<Project>` は空のディレクトリで、`/proc/mounts` にドライブのマウントが無かった（root でも同じ）。drvfs のマウントが、マウントしたセッションの中だけに見えている可能性がある。`room_mounts`（マウントの残りの検査）が別セッションから働くか、Zed の WSL リモートから `ai/` が見えるかを確かめる。

**未解決（提案。ユーザーの承認待ち）**: 部屋の AI が `~/shared` を読むたびに許可の確認が出る。「常に許可（作業ディレクトリ外のすべて）」は、部屋の `~/.claude/.credentials.json` まで許すので選ばない（今回は「今回だけ許可」で進めた）。案: `room start` が、部屋の `~/.claude/settings.json`（既存の項目は残す）に、`~/shared` だけの読み取りを許可する設定（`permissions.additionalDirectories` か `Read(~/shared/**)` の許可）を、目印つきで足す。設定のキーの形は、実装の前に Claude Code のドキュメントで確認する。

## 未決（変わらず）

下書きのヘッダー項目と `check-inbox.ps1` の整合、`review` の記録の置き場、下書きの回収（ロードマップ4番）。
