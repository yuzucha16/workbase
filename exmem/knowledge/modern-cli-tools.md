---
type: knowledge
title: modern CLIツールの役割整理
status: active
tags:
  - cli
  - tool/wsl
  - setup
  - ai/chatgpt
aliases:
  - modern CLI
  - eza fd ripgrep bat fzf zoxide
created: 2026-10-02
updated: 2026-10-02
sources:
  - ChatGPT conversation "modern CLIツールの役割整理" (2026-09-27)
  - "WSLのインストール状況を `wsl -e bash -lc 'command -v ...'` で確認（2026-10-02）"
---

# modern CLIツールの役割整理

## Purpose

Linux/WSL・Zsh・Git開発環境で、`ls` / `cd` / `find` / `grep` / `cat` を現代的なCLIツールへ置き換えるときの役割を整理し、ツールを増やしすぎずに構成する。

## Principles

- 「何を解決するツールか」で導入判断する。機能が重複するツールを足さない。
- `eza` / `lsd` と `broot` は同じ種類ではない。`eza` / `lsd` は `ls` の強化版、`broot` はファイルツリー探索のTUI。
- 速度差を主要な選定理由にしない。
- `ls` / `cat` / `find` / `grep` は、リモートや最小構成の環境で遭遇する。元のコマンドも覚えておく。
- `cat` を `bat` に完全置換しない。人間が読む用途だけ `bat` を使い、連結やパイプ処理は `cat` のまま。

## 役割

| ツール | 役割 | 置き換え対象 |
|---|---|---|
| `starship` | プロンプト | - |
| `ghq` | Gitリポジトリ管理 | - |
| `zoxide` | 過去に訪れたディレクトリへ少ない入力で移動。`fzf`・`ghq` と連携できる | `cd` |
| `eza` | ファイル一覧。Git状態表示とツリー表示が強い | `ls` |
| `fd` | ファイル・ディレクトリ検索。`.gitignore` を考慮 | `find` |
| `rg`（ripgrep） | ファイル内容の検索。再帰、`.gitignore` 対応、ファイル種別指定 | `grep` |
| `fzf` | 候補をインタラクティブに選ぶ（検索そのものではない） | - |
| `bat` | ファイル閲覧。シンタックスハイライト、行番号、Git差分、ページャー | `cat`（閲覧用途のみ） |
| `broot` | ファイルツリーの探索・操作。必要になったら追加 | - |

`fd + fzf + bat` で、ファイル検索・選択・プレビューがターミナル内で完結する。

## Decisions

### `eza` と `lsd` では、開発用途では `eza` を優先する（2026-09-27）

- 根拠: Git状態表示やツリー表示など、開発作業向けの情報表示が強い。
- `lsd` は見た目（アイコン・カスタマイズ）重視の場合の候補。

### `broot` は必須にせず、必要になったら追加する

- 根拠: `fzf + fd + rg + bat + zoxide` でファイル探索・検索・閲覧・移動がかなりカバーできる。`broot` は `zoxide` と競合しない（`eza` = 一覧、`broot` = ツリー探索・操作、`zoxide` = 過去の場所へ移動）。

## 実物との照合（2026-10-02）

WSLの既定ディストロでコマンドの有無を確認した。

| ツール | 状態 |
|---|---|
| `rg` / `fzf` / `zoxide` / `starship` / `zsh` | あり |
| `bat` | あり（`/usr/local/bin/bat` と `/usr/bin/batcat` の両方） |
| `fd` | `fd` は無く、`fdfind`（`/usr/bin/fdfind`）のみ |
| `lsd` | あり（メモの方針は `eza` 優先だが、入っているのは `lsd`） |
| `eza` / `broot` / `ghq` | なし |
| `nvim` | なし |

- Zedのターミナルは `pwsh.exe` になっている（2026-10-02 確認）。メモが前提にしていたWSL/Zshは、Zedの既定シェルではない（[[wsl-file-placement]]、[[zed-vim]]）。

## Gotchas

### Debian/Ubuntu系のパッケージ名

- `fd` は `fdfind`、`bat` は `batcat` の名前で入ることがある（上の確認結果）。`fd` として使うにはシンボリックリンクかaliasが要る。

### 機能重複

- ツールを追加しすぎると重複が増える。`broot` の導入効果は、`fd + fzf + bat` で探索体験を作れているかによる。

## Open Questions

- `eza` のalias設計（`ll` / `la` / `lt`）。既に入っている `lsd` を使い続けるか、`eza` に切り替えるか。
- `zoxide` のZsh設定（`zoxide` 自体は導入済み）。
- `fd + fzf + bat` のプレビュー環境をどこまで作り込むか。
- `ghq + fzf + zoxide` を組み合わせたリポジトリ移動フロー。`ghq` は未導入。
- WSLで導入したときのパフォーマンス・設定差。

## Next Actions

1. 不足分（`eza` または `lsd` の方針決定、`fd` のalias、`ghq`）をWSL/Zsh環境に整える。
2. aliasは最小限から始める。
3. `fd + fzf + bat` のプレビュー環境を作る。
4. `ghq + fzf + zoxide` でリポジトリ移動を試す。
5. ツリー探索が不足したときだけ `broot` を検討する。

## Related

- [[wsl-file-placement]]
- [[linux-distro-selection]]
- [[zed-vim]]
