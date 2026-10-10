---
type: knowledge
title: dotfiles の起動時間・WSL の見た目・追跡方針
status: active
tags:
  - dotfiles
  - shell
  - tool/wsl
  - tool/powershell
  - windows
aliases:
  - シェルの起動時間
  - WSL の配色とメモリ
  - dotfiles の追跡方針
created: 2026-10-06
updated: 2026-10-06
sources:
  - Claude Code conversation "社内 CA 証明書の置き場の変更" (2026-10-06)
---

# dotfiles の起動時間・WSL の見た目・追跡方針

## Purpose

dotfiles の運用で得た、シェルの起動時間の短縮、WSL の見た目とメモリ、設定ファイルを追跡する方針の知見を、別の環境でも使える形で残す。

## Principles

- 複雑さを生む仕様（フォールバック、モード、自動退避）は、仕様ごと削り、運用（手動手順と README）へ移す。読まない複雑なコードより、3か所の同期義務のような複雑さのほうが害が大きい。
- アプリが自動生成・書き換えるファイルは、リポジトリで追跡しない。リンク越しに差分が出続け、初期状態としての価値が薄い。
- シェルの起動時間は、原因を測って特定してから直す。zsh は `compinit -C` だけでは速くならず、ディストリビューションの全体設定が先に検査つきの `compinit` を実行していたことが原因だった。

## Facts

- zsh の起動は、`~/.zshenv` に `skip_global_compinit=1`、`.zshrc` に `compinit -C` を置くと、約 0.15 秒から約 0.06 秒になった（確認: 2026-10-06、根拠: 転記元の記録。Ubuntu、5回計測）。
- pwsh の starship は、`Invoke-Expression (& starship init powershell --print-full-init | Out-String)` で初期化すると、プロファイル全体が約 190 ms から約 148 ms になった（確認: 2026-10-06、根拠: 転記元の記録）。`starship init powershell` はスタブを返し、starship を2回起動する。
- WSL の `/mnt/c` 配下は権限が 777 に見えるため、dircolors の `ow=34;42`（緑背景）が `lsd` にも効き、Gruvbox の配色で文字が読めなかった。`LS_COLORS` の `ow` `tw` `st` を `01;34` に上書きして解消した（確認: 2026-10-06、根拠: 転記元の記録。再現は未実施）。
- WSL のメモリは、既定でホストの RAM の50%まで使える。実使用 0.7 GB に対し、`vmmemWSL` は 1.6 GB を保持していた（確認: 2026-10-06、根拠: 転記元の記録。WSL 2.7.14）。

## Gotchas

- **Claude Code の設定ファイル `~/.claude/settings.json` を symlink で配っていた**: Claude Code が、symlink を実ファイルに置き換えることがある（内容は同一だった）。対処の記録は無い。リンクが実ファイルになっていないかを、リンクの再実行時に確認する（[[claude-code-permissions]]）。
- **AutoHotkey の実行中に、`autohotkey/` ディレクトリを rename した**: 実行中のプロセスがディレクトリを掴み、`Permission denied` になる。ファイル単位で `git mv` した（使用中ディレクトリの rename 拒否は [[obsidian-vault]] の Gotchas にもある）。

## Related

- [[shell-fzf-keybindings]]
- [[pc-setup-manuals]]
- [[wsl-file-placement]]
- [[claude-code-permissions]]
