---
title: フォント セットアップ手順
tags:
  - cheatsheet
  - env
  - fonts
---

# フォント セットアップ手順

使うフォントは PlemolJP と Moralerspace（どちらも 1:2 の等幅。Nerd Fonts のグリフ入り）。
取得はスクリプト、インストールは手動。スクリプトは [dotfiles](https://github.com/yuzucha16/dotfiles) の `scripts/*/24_fonts.*` が正。

## 対象アプリ

Zed / Notepad++ / Obsidian / Windows Terminal

## インストール対象

| ファイル | 役割 |
|---|---|
| `PlemolJPConsoleNF-Light.ttf` | **main** |
| `PlemolJPConsoleNF-Regular.ttf` | sub |
| `PlemolJPConsoleNF-Text.ttf` | sub |
| `PlemolJPConsoleNF-Bold.ttf` | |
| `PlemolJPConsoleNF-Italic.ttf` | |
| `MoralerspaceNeonHW-Regular.ttf` | sub |

- PlemolJP は `PlemolJP_NF_v*.zip`、Moralerspace は `MoralerspaceHW_v*.zip` に入っている（Moralerspace は v2 以降、NF のグリフが HW に含まれる。NF 用の別 zip はない）。

## 手順

1. `gh` を入れる（`20_apps.bat` / `20_packages.sh` が `manifests` の一覧から入れる）。初回は `gh auth login`
2. 取得する。先に `--dry-run` で内容を確認する（dry-run は `gh` が未ログインでも動く）

   ```powershell
   scripts\windows\24_fonts.bat --dry-run
   scripts\windows\24_fonts.bat
   ```

   ```bash
   scripts/linux/24_fonts.sh --dry-run
   scripts/linux/24_fonts.sh
   ```

   - 保存先は `~/download`（Windows は `%USERPROFILE%\download`）。WSL で取ると WSL 側の `~/download` に入る。Windows のフォントとして使うなら、Windows 側のスクリプトで取る
   - 一覧は `manifests/fonts.txt`（`owner/repo:asset glob`）
3. zip を展開し、上の表の `.ttf` を選んで右クリック →「現在のユーザーにインストール」（Linux は `~/.local/share/fonts/` に置いて `fc-cache -f`）
4. 各アプリを再起動してから、フォント名を設定する
