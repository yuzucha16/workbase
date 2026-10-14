# 部屋の運用（5番）と PC での最終確認: 引き継ぎ（2026-10-13）

モバイルでできる範囲（1〜4、6、7）は実装・文書化した。5番と、全体の確認は実際の WSL・Excel が要るので PC で行う。

## 5番（PC で実装・確認）

- **`room init <Area>`**: `wsl --install Ubuntu-24.04 --name room-<Area> --no-launch`（または `--import`）→ `/etc/wsl.conf`（`automount.enabled=false`、`interop.enabled=false`、`mountFsTab=false`、既定ユーザー `ai`）→ 道具（`curl` `rg` `uv` Claude Code）→ ログイン → `~/CLAUDE.md` に `~/shared/ROOM.md` への案内。手順の正本は `guides/howto/ai-room-setup.md`。
- **reap**: close から14日（`--reap-days`）。会話履歴（部屋の `~/.claude/projects/-mnt-room-<名>/`）を `ai/records/sessions/` に写してから消す。バイナリを `wsl.exe` の標準出力で受けるので、`Wsl` に `pull`（tar を標準出力から受ける）を足す設計。
- **対応表のバックアップ**: `_noai/map/mapping.json` は追跡しない。失うと復元できない。方針（案）: `room close` で `archives/` へ移る `_noai/` ごと Windows 側のバックアップ対象にする。ユーザーの決定が要る。

## 2026-10-14 の更新（PC のセッション。ユーザーの決定と、実機で分かったこと）

**決定（ユーザー、2026-10-14）**
- 対応表のバックアップ: 上の案のとおり。`room close` で `archives/` へ移る `_noai/` ごと、Windows 側のバックアップに任せる。`_noai/` は `.gitignore` で追跡外なので、守っているのは PC のバックアップ機能であり、コミットではない。
- 会話履歴: **写さずに、期限（close から 14 日）で消すだけ**。復元が要るときは、`exmem` や `docs/` に残した記録でする。このため、reap の `Wsl.pull`（tar を標準出力から受ける）は要らなくなった。会話履歴に実データの語が混ざる問題（人が語を貼る場合）も、写さないので起きない。
- 決定の項目のラベルは、【汎用】【案件】【この件】の 3 種類（`docs-rules.md` に【案件】を足した）。

**実機で分かったこと（実装の前提）**
- `wsl.exe -- sh -c "<script>"` は、引数を部屋の側の外側のシェルでもう一度解釈する。スクリプト内で代入した変数が空に展開されるので、複数行のスクリプトは `sh -s`（標準入力）で渡す（`Wsl.script`）。`sh -c` を使うなら、変数を使わず `$HOME` を直接書く。WSL を差し替える単体テストでは検出できない。
- 部屋の案内は `~/CLAUDE.md` ではなく、**`~/.claude/CLAUDE.md`**（作業ディレクトリが `/mnt/room/<Project>` なので、`~` の直下は読まれない）。`room start` が、目印で囲んだ範囲だけを毎回入れ替える。`room init` では扱わない。
- 部屋の AI が `~/shared` を読むたびに許可の確認が出る。当面は手動で運用する。
- Windows Terminal は部屋のディストロを自動で `settings.json` に書き足すので、WSL の動的プロファイル（`Microsoft.WSL`）を無効にし、`Ubuntu-24.04` だけ固定した。部屋には、PowerShell の `room-sh <Area>` で入る（dotfiles の `profile.ps1`）。Zed の `wsl_connections` は、Zed の画面から接続すると書き足される（避けられない。部屋ごとに 1 項目）。
- `--no-launch` で待っている間、別の `wsl.exe` セッションから `/mnt/room/<Project>` が空で、`/proc/mounts` にマウントが無い。drvfs のマウントがセッションごとに見えている可能性がある（未解決）。

**案（提案。決定ではない）**
- 5-a `room init <Area>`: `wsl --install Ubuntu-24.04 --name room-<Area> --no-launch` → `/etc/wsl.conf`（`automount` と `interop` を無効、既定ユーザー `ai`）→ `wsl --terminate` → 道具（`curl` `rg` `uv` Claude Code）→ **ログインは人**（`init` は止まって `room-sh <Area>` を案内）。使い捨ての `room-init-test` で実装・確認し、既存の `room-office-admin` と `Ubuntu-24.04` には触れない。
- 5-b reap: close から 14 日で、部屋の `~/.claude/projects/-mnt-room-<名>/` を消すだけ（写さない）。
- 5-d `room intake <Project> <ファイル>`（仮名。`exmem/lessons/ai-tool-deliverable-structure` の Next Actions）: 人が実環境で得た結果を、`room` がマスクして `ai/in/` へ入れる。`mask` の仕組みを再利用できる。今は「人が語を伏せてから貼る」規約。
- `room restore`: `ai/out/<成果物>/` のサブディレクトリを復元できるか（`stock/` の経験からの推測）、`mapping.json` が無い・版が食い違うときに止まるかを、実機で確認する。
- `room-context.md` に、「Windows が要る検証は人に頼む。結果は語を伏せて貼る」の 1 行を足す（kit の手順書の変更。承認制）。

**保留**: 項目 5 は、別セッションで議論しているディレクトリ構造と合流してから進める（ユーザー、2026-10-14）。

## 反映済みの雛形（実機で未検証）

- `templates/workspace/gitignore.template`（`**/_noai/`、`!**/ai/out/` など）、`claude-settings.template.json`（Vault 側の deny。`Read(./projects/**)` の書式が Windows ネイティブで効くか PC で確認）、`templates/workspace/AGENTS.md` の「AI 作業部屋」の節、`init-workspace.md`。
- `exmem/lessons/ai-isolated-work-room.md`（決定の記録）。

## 全体の確認（PC）

各 handover の「PC で確認すること」: [[ai-room-mask-handover]]、[[ai-room-shared-push-handover]]、[[ai-room-stock-handover]]。実 Project での1巡（8番）で、手数・マスク漏れ・復元の失敗を測る。

## 片付け

PC の確認が済んだら、`mobile-session/ai-workspace-boundary/` を削除する（`ai-room-next-steps.md` の TODO。履歴は git に残る）。
