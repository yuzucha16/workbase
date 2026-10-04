---
type: knowledge
title: Zedのdotfiles管理
status: active
tags:
  - tool/zed
  - dotfiles
  - setup
  - acp
aliases:
  - Zedのdotfiles管理
  - Zedの設定の再現
created: 2026-10-01
updated: 2026-10-03
sources:
  - Claude (Claude Code via Zed ACP) conversation "Zedのextension/ACPエージェントのdotfiles管理" (2026-10-01)
  - "%APPDATA%\\Zed / %LOCALAPPDATA%\\Zed / dotfilesリポジトリ（2026-10-01 に確認）"
  - "%APPDATA%\\Zed\\settings.json、PowerShellプロファイル（2026-10-02 に再確認）"
---

# Zedのdotfiles管理

## Purpose

Zedの設定・extension・ACPエージェントをdotfilesリポジトリで管理し、PCを変えてもすぐ再現できるようにする。

## Principles

- 手で書く設定だけを管理する。Zedが自動生成するキャッシュや本体は管理しない。
- 管理対象のファイルを増やさない。できるだけ `settings.json` 1ファイルに寄せる。

## 管理しているもの

2026-10-01 時点で確認済み。

`%APPDATA%\Zed\` の設定ファイルは、dotfilesリポジトリ（`C:\vault\repos\github.com\yuzucha16\dotfiles`）へのシンボリックリンクになっている。

> 2026-10-03 の dotfiles 再編で、正本は `home/.config/zed/` に移った（`manifests/links.map` で `%APPDATA%\zed\` へリンク。詳細は dotfiles リポジトリ）。下の表は2026-10-01 時点のパス。フォント設定（`ui_font_*` `buffer_font_*`、`terminal.shell` の削除）も追加されている（[[fonts]]）。

| ファイル | リンク先（2026-10-01 時点） |
|---|---|
| `%APPDATA%\Zed\settings.json` | `dotfiles\zed\settings.json` |
| `%APPDATA%\Zed\keymap.json` | `dotfiles\zed\keymap.json` |

`settings.json` で管理している内容:

```json
"auto_install_extensions": {
  "powershell": true
},
"agent_servers": {
  "claude-acp": {
    "default_config_options": { "model": "sonnet" },
    "type": "registry"
  },
  "codex-acp": { "type": "registry" }
}
```

- `auto_install_extensions`: 起動時に不足しているextensionを自動インストールする。`powershell` を登録済み（コミット `0533feb`）。
- `agent_servers`: ACPエージェントの設定。Registryからインストールした時点で自動的に記録される（[[zed-acp]]）。2026-10-02 の確認で、`claude-acp` に `default_config_options.model: "sonnet"`（既定モデル）が加わっていた。

PowerShellのプロファイルも同じ方式で管理されている（2026-10-02 に確認）。

| ファイル | リンク先 |
|---|---|
| `%USERPROFILE%\Documents\PowerShell\profile.ps1` | `dotfiles\profile.ps1`（シンボリックリンク。2026-10-03 以降の正本は `windows\powershell\profile.ps1`） |

プロファイルの先頭には、非対話起動なら抜けるガードがあり、ZedのClaude Agent起動に必要（[[zed-acp]]）。dotfilesのGit追跡ファイルの一覧には `Microsoft.PowerShell_profile.ps1` があるが、リンク先の `profile.ps1` が追跡されているかは今回確認していない。

## Windowsでの配置

2026-10-01 時点で確認済み。

| パス | 中身 | 管理 |
|---|---|---|
| `%APPDATA%\Zed\settings.json` / `keymap.json` | 設定 | dotfiles |
| `%APPDATA%\Zed\AGENTS.md` | Zed全体のエージェント向けルール | 未管理 |
| `%LOCALAPPDATA%\Zed\extensions\installed\` | extension本体（このPCでは `html` と `powershell`） | しない |
| `%LOCALAPPDATA%\Zed\extensions\index.json` | 自動生成の索引 | しない |
| `%LOCALAPPDATA%\Zed\external_agents\registry\` | ACPエージェント本体（npx経由） | しない |
| `%LOCALAPPDATA%\Zed\node\` | Zed同梱のNode（v24.11.0） | しない |
| `%LOCALAPPDATA%\Zed\threads\threads.db` | Zedのスレッド履歴 | しない |

- Zedには「インストール済みextensionの一覧」を書いた設定ファイルはない。
- `powershell` はPowerShellのextension（`id = "powershell"`、リポジトリは zed-extensions/powershell）。`html` はZedが標準で入れるもの。
- `threads.db` は 2026-08-13 から更新されていない。Claude AgentのACPチャットはここではなく、Claude Code側に保存される（[[claude-code-storage]]）。

## Decisions

### extensionは `auto_install_extensions` で管理する（2026-10-01）

- 根拠: 起動時に不足分を自動インストールしてくれる。すでにGit管理している `settings.json` 1ファイルで済む。
- 却下案: `extensions\installed\` や `index.json` をdotfilesに入れる。Zedが自動生成する本体・キャッシュで、管理に向かない。

### ACPエージェントは `agent_servers` の記録だけで管理する（2026-10-01）

- 根拠: `agent_servers` はセットアップ時に `settings.json` へ記録済みで、本体は必要なときに自動取得される。
- 却下案: `external_agents\` をGit管理する。自動生成のキャッシュなので不要。

## 仮説（未検証）

- 新しいPCで `auto_install_extensions` により `powershell` が自動で入る。
- 新しいPCで `agent_servers` から2つのエージェントが自動取得される。ClaudeとCodexへのログインはPCごとに必要と思われる。

## Open Questions

- `%APPDATA%\Zed\AGENTS.md` もdotfilesで管理するか。

## Next Actions

- 別のPC、またはextensionを消した状態で、`powershell` が自動インストールされるか確認する。

## Related

- [[zed-acp]]
- [[zed-vim]]
- [[fonts]]
- [[claude-code-storage]]
- [[vscode-workspace]]
