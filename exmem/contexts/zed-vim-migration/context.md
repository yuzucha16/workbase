---
type: project
title: ZedへのVim環境移行 Project Context
status: active
tags:
  - tool/zed
  - tool/vim
  - keymap
aliases:
  - ZedへのVim環境移行 Project Context
created: 2026-09-26
updated: 2026-10-02
---

# ZedへのVim環境移行 Project Context

## Current State

- 基本設定（行番号、インデント、タブ、クリップボード、smartcase、テーマ、ターミナル）はZedの `settings.json` へ移行済み（[[zed-vim]]）。
- Vim Pluginは破棄し、Zed標準機能へ置き換える方針が決まった。個々の操作の対応はまだ試していない。
- `keymap.json` にはターミナル内で `Ctrl-P` / `Ctrl-N` / `Ctrl-Shift-M` をシェルへ送る設定だけがある。
- Leaderは未変更。
- 2026-10-02 の再確認で、Zedのターミナルのシェルは `wsl.exe` から `pwsh.exe` に変わっていた。上記の設定キーは同じ値で残っている（[[zed-vim]]、[[wsl-file-placement]]）。

## Next Actions

1. Project Panelを使い、Fern相当のディレクトリ操作を確定する。
2. Go to Fileを使い、fzfなしでファジー検索の目的を満たせるか確認する。
3. Status Barを基本とし、Airline相当の追加設定を最小限にする。
4. gtagsの代わりに、LSPの定義・参照・Symbol検索を使う。
5. Zed Git + Vim modeの標準操作で、GitGutter / Fugitiveの操作を試す。
6. 不足した操作だけ `keymap.json` へ追加する。
7. 最後に、Neovimとの共通化を目的としてSpace leaderを設計する。

## Goal

`.vimrc` の編集環境を、Zed標準機能 + Vim modeを基本とした構成へ移行する。

## Open Questions

1. `Space` をleaderとしてZedの一部操作をNeovimと共通化するか。
2. leaderをZed側で変更するか、キーボード側で `Ctrl+Shift` を1キー化するか。
3. Fern時代に使っていたディレクトリ操作を、どこまでZed標準のまま使うか。
4. gtagsの操作をLSP / Symbol検索へ具体的にどう置き換えるか。
5. GitGutterで使っていた操作を、Zed Gitのどの標準操作へ対応させるか。
6. 会話メモでは「`keymap.json` は空」としていたが、実際にはターミナル用の設定がある。この設定は残す意図か。
