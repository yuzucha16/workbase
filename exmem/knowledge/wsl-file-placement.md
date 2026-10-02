---
type: knowledge
title: ZedとWSLのファイル配置方針
status: active
tags:
  - tool/wsl
  - tool/zed
  - windows
  - setup
  - backup
aliases:
  - WSLのファイル配置
  - Windows側とWSL側の置き場所
created: 2026-10-02
updated: 2026-10-02
sources:
  - ChatGPT conversation "ZedとWSLのファイル配置方針" (2026-10-02)
  - "%APPDATA%\\Zed\\settings.json、C:\\vault の構成（2026-10-02 に確認）"
---

# ZedとWSLのファイル配置方針

## Purpose

ZedからWSLを使う開発環境で、プロジェクトや各種ファイルをWindows側とWSL側のどちらに置くかを決める。

## Principles

- 開発用ファイルはWSL側に置く（暫定）。Linuxの開発ツール、Git、言語ランタイムを一貫して扱えるうえ、`/mnt/c` 越しの大量I/Oは遅くなりやすい。
- WindowsアプリやWindowsとの同期・共有が目的のデータ（Documents、Downloads、Pictures、OneDrive同期対象、Windows専用アプリの作業データ）はWindows側に置く。
- 受け渡しは必要なときだけ。`/mnt/c/...` か、エクスプローラーの `\\wsl.localhost\<Distro>\home\<user>\` を使う。
- ファイルを共有できることと、どちらを主配置先にするかは別の問題。

## Decisions

### 開発用ファイルはWSL側に置く（暫定、2026-10-02）

- 想定パス: `/home/<user>/src/<project>`。新規Gitリポジトリは原則WSL側にcloneする。
- 却下案: すべてWindows側に置く（WSLからの大量I/OとLinux開発ツールの整合性で不利）。OneDrive同期対象をWSLホームに直接構築する（同期・ファイル監視・権限の複雑さ）。

## Facts

- WSLからWindows側は通常 `/mnt/c/...`。WSL内のホームは通常 `/home/<user>/`。
- 仮説・環境依存: WSL側のファイルシステムは、Gitや依存管理が大量のファイルを扱う場面で `/mnt/c` より有利になりやすい。

### 実物との照合（2026-10-02）

メモの前提と、現在のこのPCの実態には食い違いがある。

- Zedのターミナルは `pwsh.exe`（`settings.json`）。2026-09-26 時点では `wsl.exe` だった（[[zed-vim]]）。現在、ZedのターミナルはWSLではない。
- リポジトリはWindows側にある: `C:\vault\repos\github.com\yuzucha16\`（`areas_shared`、`dotfiles`）。「開発用ファイルはWSL側」という暫定方針とは逆の配置。
- Zedのプロジェクトは、Windowsのパス（`C:\vault\notes\areas_shared\exmem` など）で開いている（[[claude-code-storage]]）。ZedのWSLプロジェクト連携（ファイルシステム・Language Server・ツール実行をWSL側に寄せる方式）を使っているかは、今回も確認できていない。
- WSLにはZsh、`rg`、`fzf`、`zoxide` などが入っているが、`nvim` と `ghq` は入っていない（[[modern-cli-tools]]）。

## Gotchas

### ターミナルだけWSLにしても、プロジェクトやLanguage ServerはWindows側のまま

- ターミナル設定と、リモート/WSLプロジェクト連携は別。どちらがWSL側で動いているか、区別して確認する。

### `/mnt/c` 上のリポジトリは遅くなることがある

- `git`、`rg`、`npm install` などは、ファイル数やI/Oパターンによって遅くなる。

## Open Questions

- ZedのWSL連携方式は何か。Zedのファイル操作、Language Server、Git統合、ターミナルが、それぞれWindows / WSLのどちらで動くか。
- 現在Windows側にあるリポジトリ（`C:\vault\repos`）を、この方針でWSL側へ移すのか。それとも「Windowsで編集するリポジトリ」と「WSL側の開発用リポジトリ」を分けるのか。vaultとdotfilesは、Windows側から使う前提（ジャンクション・シンボリックリンク）なので、移すと崩れる（[[obsidian-vault]]）。
- Windows側のアプリと頻繁に編集・同期するプロジェクトはあるか。
- WSLのディストロ名、ユーザー名、標準のプロジェクトディレクトリ。

## Next Actions

- ZedのWSL連携方式と、プロジェクトの実際のパスを確認する。
- WSL側に `~/src` など開発用ルートを作る。
- 代表的なプロジェクトで、Git操作・検索・ビルド・Language Serverの動作と速度を確認し、方針を確定する。

## Related

- [[zed-vim]]
- [[zed-dotfiles]]
- [[modern-cli-tools]]
- [[vscode-workspace]]
- [[claude-code-vs-cowork]]
