---
type: index
title: タグ一覧
status: active
tags:
  - knowledge-management
aliases:
  - Tags
created: 2026-09-26
updated: 2026-10-06
---

# タグ一覧

タグは「何についての知識か」を表す。新しいタグは、ここに追記してから使う。

## ルール

- 英小文字の kebab-case。日本語・スペースは使わない。
- 1ノートあたり 3〜6 個を目安にする。
- ソフトウェアとAIは階層タグにする。Obsidianで `tag:#tool` と検索すると `tool/*` がすべて引っかかる。
- `type` や `status` の値はタグにしない。
- 「AI」「メモ」のように、ほぼ全ノートに付くタグは作らない。絞り込みに役立たないため。

## 語彙

### `tool/` — ソフトウェア

| タグ | 意味 |
|---|---|
| `tool/zed` | Zedエディタ |
| `tool/vim` | Vim |
| `tool/neovim` | Neovim |
| `tool/obsidian` | Obsidian |
| `tool/vscode` | Visual Studio Code |
| `tool/wsl` | WSL（Windows Subsystem for Linux） |
| `tool/powershell` | PowerShell（プロファイル含む） |
| `tool/excel` | Excel（Office Scripts含む） |
| `tool/power-automate` | Power Automate |
| `tool/notepadpp` | Notepad++ |
| `tool/scoop` | scoop（Windows のパッケージマネージャー） |
| `tool/winget` | winget |
| `tool/gh` | GitHub CLI（`gh`） |
| `tool/windows-terminal` | Windows Terminal |
| `tool/git` | Git（コミット規則・改行・設定） |
| `tool/stow` | GNU Stow（symlink 配置） |

### `ai/` — AIサービス・エージェント

| タグ | 意味 |
|---|---|
| `ai/chatgpt` | ChatGPT（モバイル・Webのチャット） |
| `ai/codex` | Codex |
| `ai/claude` | Claude / Claude Agent |
| `ai/copilot` | GitHub Copilot / Microsoft 365 Copilot |

### トピック

| タグ | 意味 |
|---|---|
| `workflow` | 作業の流れ・運用 |
| `knowledge-management` | 知識の整理・保存方法 |
| `context-engineering` | AIへ渡すコンテキストの設計 |
| `acp` | Agent Client Protocol |
| `keymap` | キーバインド |
| `setup` | インストール・初期設定の手順 |
| `dotfiles` | 設定ファイルのGit管理・別PCでの再現 |
| `mobile` | モバイル端末での利用 |
| `harness` | AIエージェントのハーネス（実行環境・権限・状態・検証） |
| `agent-design` | AIエージェント・人間とAIの役割分担の設計 |
| `automation` | 業務・定型作業の自動化 |
| `office` | Office成果物（Excel / PowerPoint / Word）を扱う業務 |
| `windows` | Windows環境固有の話題 |
| `backup` | バックアップ・データの置き場所 |
| `cli` | コマンドラインツール |
| `linux` | Linuxディストリビューション・導入 |
| `hardware` | 物理デバイス（キーボードなど） |
| `font` | フォントの選定・導入・設定 |
| `accessibility` | 目の負担・光の点滅など、身体の特性に合わせた環境設定 |
| `line-endings` | 改行コード（LF / CRLF） |
| `shell` | シェルスクリプト |
| `testing` | 試験の方法 |
| `traceability` | 誰が・どの規則で行ったかを後から追えること |
