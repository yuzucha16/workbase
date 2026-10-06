---
type: knowledge
title: modern CLIツールの役割整理
status: active
tags:
  - cli
  - tool/ripgrep
  - tool/wsl
  - setup
  - ai/chatgpt
aliases:
  - modern CLI
  - eza fd ripgrep bat fzf zoxide
created: 2026-10-02
updated: 2026-10-05
sources:
  - ChatGPT conversation "modern CLIツールの役割整理" (2026-09-27)
  - "WSLのインストール状況を `wsl -e bash -lc 'command -v ...'` で確認（2026-10-02）"
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05。「検索の見える範囲」)
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
| `rg`（ripgrep） | ファイル内容の検索。再帰、`.gitignore` 対応、ファイル種別指定。ジャンクションは既定で辿らない（`--follow` で辿る）。`.ignore` で `.gitignore` を打ち消せる（下の「検索の見える範囲」） | `grep` |
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

## 検索の見える範囲（2026-10-05 追記）

AI の検索ツール（Claude Code の Grep / Glob）と `rg` が、リンクと `.gitignore` によって何を辿るか。Vault の構造変更（[[obsidian-vault]]）の中で実測した。

### Principles（検索）

- AI の検索ツール（Grep / Glob）と `rg` の見える範囲は、`.gitignore` とリンクの種類で、エラーも警告も無く変わる。ディレクトリ構成やリンクを変えたら、既知の語で検索して、結果に出るかを実測する。検索から抜けても、結果が空になるだけで、気づけない。
- 別リポジトリの clone を、AI に検索させたい場所に置くときは、リンク（ジャンクション、symlink）でなく、実ディレクトリにする。検索ツールはリンクを辿らない。
- 外側のリポジトリが `.gitignore` で除外した入れ子の clone を、検索に含めたいときは、`.ignore`（`.gitignore` より優先される）で打ち消す。`.gitignore` は、git の追跡だけでなく、ripgrep の検索範囲にも効く。

### Decisions（検索）

- **共有リポジトリの clone を、`ghq` の位置からのジャンクションでなく、Vault の中に直接 `git clone` する**（2026-10-05）
  - 根拠: ジャンクション越しは、Grep / Glob / `rg` が辿らない。Obsidian でのジャンクション越しの動作も未検証だった。
  - 却下案: `ghq` の位置に clone して、ジャンクションで Vault に出す（検索から黙って外れる。`ghq` で一元管理できる利点より、検索できることを優先した）。

### Facts（検索）

- ジャンクション越しのディレクトリは、Claude Code の Grep と Glob、`rg`（既定）、PowerShell の `Get-ChildItem -Recurse` が辿らない。`rg --follow` は辿る。ジャンクション自体をパスに指定した Grep は検索できる（結果は実体のパス）（確認: 2026-10-05、根拠: 使い捨ての一時ディレクトリに、通常のディレクトリとジャンクションを並べて実測。Windows 11、pwsh 7）。
- トップの `.gitignore` が `/resources/`（別リポジトリの clone）を除外すると、トップからの Grep で `resources/` の中が出なかった（同じ語の検索が3件）。トップの `.ignore` に `!/resources/` を置くと、`resources/` 配下を含む8件以上になった（確認: 2026-10-05、根拠: Grep の結果の件数を、置く前後で比較）。トップの `.ignore`（現在は `$HOME\works\.ignore`）に `!/resources/` が置かれている（確認: 2026-10-06、根拠: ファイルの読み取り）。
- Glob は、`.ignore` を置いた後に、`resources/workflow-kit/*.md` で期待どおりの結果だった。置く前の挙動は未確認（仮説: Glob も `.gitignore` の影響を受ける）。

### Gotchas（検索）

- **トップで Grep したら、`resources/` の中が結果に出なかった**: ripgrep が、トップの `.gitignore`（`/resources/`）を尊重した。トップに `.ignore`（`!/resources/`）を置いた。
- **PowerShell で、バッククォートを含む `git grep -E "..."` のパターンを二重引用符で渡したら、全行がヒットして、出力が約670KBになった**: 二重引用符の中のバッククォートは PowerShell のエスケープ文字で、パターンが壊れた。単一引用符で渡すか、Grep ツールを使う。

### Open Questions（検索）

- Claude Code の Grep に、リンクを辿らせる指定（`rg --follow` 相当）があるか（未確認）。
- Glob が `.gitignore` の影響を受けるかを、`.ignore` が無い状態で確認する。

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
- [[obsidian-vault]]
