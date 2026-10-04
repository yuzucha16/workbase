---
type: project
title: dotfiles・PC環境の再現 Project Context
status: active
tags:
  - dotfiles
  - setup
aliases:
  - dotfiles Project Context
  - PC環境の再現
created: 2026-10-03
updated: 2026-10-04
---

# dotfiles・PC環境の再現 Project Context

## Current State

- `yuzucha16/dotfiles` を再編した（2026-10-02〜03）。履歴を単一コミットに作り直し、`scripts/{windows,linux}/`・`manifests/`・`home/`（`~` の鏡）・`windows/`・`templates/` の構成にした。スクリプトは `NN_<内容>` の命名（十の位=層、一の位=固有ツール）で、WSL とネイティブ Linux は `scripts/linux/` に1本化した（[[dotfiles]]）。
- 手順書は `resources/cheatsheets/env/`（`win11.md`、`debian-family.md`、`fonts.md`）。実機での通し確認は未実施（[[pc-setup-manuals]]）。
- メインフォントは PlemolJP Console NF の Light（1週間の試用中）。Zed・Windows Terminal・Notepad++ に反映済み（[[fonts]]）。
- Office テンプレと `.obsidian` は `notes` リポジトリへ移管済み（[[obsidian-vault]]）。
- 2026-10-03 に、inbox のメモ6件（dotfiles の再編・複雑度削減・スクリプト命名・手順書・フォント導入・フォント選定）を統合した。実物との照合で次を確認した。
  - 一致: `scripts/` と `manifests/` の構成、`links.map` の Notepad++ の追跡範囲、Zed のフォント設定、インストール済みフォント4種、`cheatsheets/env/` の3ファイル。
  - 食い違い・未反映: `git bundle` のバックアップがメモのパスに無い。`.wslconfig` はこのPCに未リンク。dotfiles README に `areas_shared` の記載は無い（解消済み）。`gh` は scoop に入っている。
  - 未 push: dotfiles は `origin/main`（`e1e4ac7`）より3コミット先（`8f1f885` `dda8e75` `b9af34a`）。リモートには `main` と `202509` が両方ある。

- 2026-10-04: 両PCの履歴を分析してユースケースを整理し、「履歴の種」の方針を決めた（exmem に傾向と種の本文、dotfiles に種ファイル。[[shell-command-usecases]]）。
- 2026-10-04: zfz/cdg を `Alt+j`/`Alt+k` で3シェル共通にした（コミット済み）。zsh で ListView 相当の自作一覧を試し、zsh/bash の ListView 相当は作らず、fzf の `Ctrl+R`（履歴）・`Ctrl+T`（ファイル）に切り替えた（コミット・push 済み。[[dotfiles]] の Decisions）。pwsh にも同じキーで fzf を入れ（`ListView` は残す。実機で動作確認済み）、bash の `.bashrc` 末尾の `cd ~` を削除した。zsh/bash 向けの履歴の種と配置スクリプトも作った。目的はコマンド履歴のベースを dotfiles 側で管理して、PC 移行時の調べ直しを減らすこと。

## Next Actions

- シェルの3シェル共通化（fzf とキーバインドの現仕様の表は [[dotfiles]] の Facts）:
  - 済: `zfz` = `Alt+j`、`cdg` = `Alt+k`、3シェルの `Ctrl+R`/`Ctrl+T`（fzf）、bash の `cd ~` の削除。pwsh の `Ctrl+R`/`Ctrl+T` は実機で動作確認済み。WSL に `ghq` を入れたら `cdg`（zsh/bash）も実機で確認する。
  - その他、3シェルの差を洗い出して共通化する。
- ヒストリの種（案a）を進める。方針と種の本文は [[shell-command-usecases]]。種ファイル `windows/powershell/history.seed.txt`（92行）と、配置スクリプト `scripts/windows/31_history_seed.bat`（履歴が無い/空のときだけコピー）は作成・検証済み。zsh/bash 向けは `manifests/history.seed.sh.txt`（77行）と `scripts/linux/31_history_seed.sh` を作成・テスト済み（未コミット）。残り: 新しいPCで通し実行、数週間使って間引き（後日。置換した apt などの行を優先して見直す）。
- （旧）コマンド履歴の管理を設計する: 重複排除、`ls`/`cd` など短い行の除外、秘匿パターンと会社固有・ユーザー名入りパスの除外、共有（Git）とローカル専用（`_local/`）の分け方。参照用の他PC生ヒストリは `resources/_local/ConsoleHost_history.txt` に退避済み（Git 対象外。使い終わったら削除）。

- GitHub の既定ブランチを `main` にし、問題が無ければ `202509` をリモート・ローカルで削除する（ユーザーの確認待ち）。
- 各PC（家・会社）で `git pull` → Windows は `30_link.bat`（家は `link home`）、Linux/WSL は `30_link.sh` を再実行する。新しいシェルで zsh の `lt` / `ll` / `l`、`cdg` を確認する。
- このPCで `.wslconfig` を反映する: `30_link.bat` → `wsl --shutdown` → 開き直して `vmmemWSL` を観察する。
- `git config user.name` / `user.email` を `~/.gitconfig_local` にPCごとに設定済みか確認する（仮値 `user <user@example.com>` のままコミットしない）。
- 既に入っている不要な VS Code 拡張を `code --uninstall-extension` で外す（Windows 6件、WSL 4件）。古い Notepad++ のリンク切れ（`stylers.xml` `contextMenu.xml` `NppExec.ini`）と `~/vimfiles` の旧プラグイン（`:PlugClean`）を掃除する。
- 新しいPC（または VM）で `10` → `50` を通し実行し、手順書どおり進むか確認する。MX Linux 25.3 と Win11 の「要確認」を潰す。
- `gh auth login` を済ませ、`24_fonts.*` で実際にダウンロードしてフォントを入れる。1週間使って「Light で続ける / Text に上げる / HackGen に戻す」を決める。
- `30_link.sh` の最後に `chsh` 後の再ログインの案内を足す。`50_repos.sh` の前提（`source ~/.profile`、`ghq` が PATH にある）を整理する。`50_repos.bat` に取得したいリポジトリを足す。
- `git bundle` のバックアップの所在を確認する（見つからない）。必要なら保管場所を決める。
- 古い WSL では `fdfind` → `fd` のリンクが無いので、`20_packages.sh` を再実行するか手でリンクを張る。

## Goal

Windows 11 + WSL2 とネイティブ Linux で、家PCと会社PCの作業環境を、手順書とスクリプトで同じように再現できる状態を保つ。軽く、ポータブルに。

## Source of Truth

- 設定とスクリプト: dotfiles リポジトリ。構成と判断の根拠は [[dotfiles]]。
- 手順書: `resources/cheatsheets/env/`（[[pc-setup-manuals]]）。スクリプトと手順書で一覧を重複させない。

## Open Questions

[[dotfiles]]、[[pc-setup-manuals]]、[[fonts]] の Open Questions を見る。

## Related

- [[ai-development-workflow/context]]
