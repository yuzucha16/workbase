---
type: knowledge
title: VS Codeの拡張機能とWorkspace運用
status: active
tags:
  - tool/vscode
  - tool/wsl
  - setup
  - dotfiles
aliases:
  - VS Codeライトユーザー向け運用
  - VS Code Workspace
  - extensions.json
created: 2026-10-02
updated: 2026-10-02
sources:
  - ChatGPT conversation "VS Codeライトユーザー向け拡張機能とWorkspace運用" (2026-10-02)
  - "`code --list-extensions`（2026-10-02 に確認）"
---

# VS Codeの拡張機能とWorkspace運用

## Purpose

ライトユーザー向けにVS Code拡張機能を絞り、プロジェクト / Workspace / 設定ファイルの役割を整理する。特に、通常インストールした拡張機能がどこに記録されるかを押さえる。

## Principles

- 拡張機能は少数から入れ、必要に応じて足す。
- 個人の好みはUser Settings（やdotfiles）、プロジェクト固有の設定は各リポジトリの `.vscode/` に分ける。個人設定をプロジェクトに埋め込むと、Git共有時に意図しない設定まで共有される。
- formatterは言語・プロジェクトの規約に合わせる（C/C++はclang-format、PythonはRuffやBlack、JS/TSはPrettierなど）。
- 「拡張機能をインストールした」ことと「プロジェクトが推薦している」ことは別。
- WSLでは拡張機能がローカル側かリモート側かを確認する。`~/.vscode/extensions/` だけで全環境の導入状況を判断しない。

## Decisions

### 基本運用はGitリポジトリのルートを `code .` で開く（2026-10-02）

- 根拠: 単一プロジェクトでは `.code-workspace` が要らず、リポジトリ全体をVS Codeで扱える。
- 却下案: 最初からMulti-root Workspaceや専用Workspaceファイルを使う。複数の独立したフォルダを1ウィンドウで扱う必要が出たときに限る。

### 設定の責務分離

| ファイル | 役割 |
|---|---|
| User Settings | テーマ、フォント、Vim操作、UIなど個人の環境設定 |
| `.vscode/settings.json` | プロジェクト固有の編集・動作設定 |
| `.vscode/extensions.json` | 拡張機能の推薦リスト |
| `tasks.json` / `launch.json` | ビルドタスクやデバッグ設定が必要になったとき |

### 導入候補の拡張機能（採用決定ではない）

- Vim、GitLens（VS Code標準のGit機能もあるので必須ではない）、EditorConfig、Error Lens。
- 必要に応じて: 言語別拡張（YAMLなど）、Prettier、Path Intellisense、Material Icon Theme。

## Facts

- 通常インストールした拡張機能は、基本的にユーザー環境側に入る。ローカル配置の例は `~/.vscode/extensions/`。WSL利用時は、Windows側とWSL側で実行環境・インストール先が分かれうる。
- `.vscode/extensions.json` はインストール済みの自動記録ではなく、推奨する拡張機能の宣言。IDを書いても自動インストールされるわけではない。
- `code --list-extensions` で、現在の環境にインストール済みの拡張機能IDを列挙できる。
- `.code-workspace` は主にMulti-root Workspaceで使う。単一リポジトリでは必須ではない。

### 実物との照合（2026-10-02）

Windows側の `code --list-extensions` の結果は次の12個。メモの導入候補（Vim / GitLens / EditorConfig / Error Lens）は**入っていない**。

- テーマ: `cocopon.iceberg-theme`、`jdinhlife.gruvbox`、`sainnhe.everforest`
- 日本語化・アイコン: `ms-ceintl.vscode-language-pack-ja`、`pkief.material-icon-theme`
- リモート: `ms-vscode-remote.remote-containers`、`remote-ssh`、`remote-ssh-edit`、`remote-wsl`、`ms-vscode.remote-explorer`
- その他: `plorefice.devicetree`、`wayou.vscode-todo-highlight`

- 実際の用途はテーマ、リモート接続（WSL / SSH / Dev Containers）、Devicetree。組み込み系の用途がうかがえる。エディタ操作の主戦場はZed（[[zed-vim]]）なので、VS CodeでVim拡張を入れるかは別の判断。
- WSL側にインストールされている拡張機能は、この確認では見ていない。

## Gotchas

### `extensions.json` に現在のインストール一覧は反映されない

- 必要なら `code --list-extensions` の結果を見て、推薦対象を手動で選ぶ。

### User SettingsとWorkspace Settingsの混同

- 個人の好みをプロジェクトに埋め込まない。

## Open Questions

- 実際に使う言語・用途（C/C++、Python、YAML、Markdownなど）に合わせた最小構成。
- WindowsとWSLのどちらを主な開発環境にするか（[[wsl-file-placement]]）。
- `code --list-extensions` の出力をdotfilesで管理するか、プロジェクトごとの `extensions.json` に必要分だけ書くか。

## Next Actions

- 上の12個から、常用するものだけ残す。言語別拡張は実際の編集対象に応じて足す。
- 複数ルートをまとめて開く必要が出たら `.code-workspace` を検討する。

## Related

- [[zed-vim]]
- [[zed-dotfiles]]
- [[wsl-file-placement]]
