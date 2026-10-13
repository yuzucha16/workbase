# 部屋の運用（5番）と PC での最終確認: 引き継ぎ（2026-10-13）

モバイルでできる範囲（1〜4、6、7）は実装・文書化した。5番と、全体の確認は実際の WSL・Excel が要るので PC で行う。

## 5番（PC で実装・確認）

- **`room init <Area>`**: `wsl --install Ubuntu-24.04 --name room-<Area> --no-launch`（または `--import`）→ `/etc/wsl.conf`（`automount.enabled=false`、`interop.enabled=false`、`mountFsTab=false`、既定ユーザー `ai`）→ 道具（`curl` `rg` `uv` Claude Code）→ ログイン → `~/CLAUDE.md` に `~/shared/ROOM.md` への案内。手順の正本は `guides/howto/ai-room-setup.md`。
- **reap**: close から14日（`--reap-days`）。会話履歴（部屋の `~/.claude/projects/-mnt-room-<名>/`）を `ai/records/sessions/` に写してから消す。バイナリを `wsl.exe` の標準出力で受けるので、`Wsl` に `pull`（tar を標準出力から受ける）を足す設計。
- **対応表のバックアップ**: `_noai/map/mapping.json` は追跡しない。失うと復元できない。方針（案）: `room close` で `archives/` へ移る `_noai/` ごと Windows 側のバックアップ対象にする。ユーザーの決定が要る。

## 反映済みの雛形（実機で未検証）

- `templates/workspace/gitignore.template`（`**/_noai/`、`!**/ai/out/` など）、`claude-settings.template.json`（Vault 側の deny。`Read(./projects/**)` の書式が Windows ネイティブで効くか PC で確認）、`templates/workspace/AGENTS.md` の「AI 作業部屋」の節、`init-workspace.md`。
- `exmem/lessons/ai-isolated-work-room.md`（決定の記録）。

## 全体の確認（PC）

各 handover の「PC で確認すること」: [[ai-room-mask-handover]]、[[ai-room-shared-push-handover]]、[[ai-room-stock-handover]]。実 Project での1巡（8番）で、手数・マスク漏れ・復元の失敗を測る。

## 片付け

PC の確認が済んだら、`mobile-session/ai-workspace-boundary/` を削除する（`ai-room-next-steps.md` の TODO。履歴は git に残る）。
