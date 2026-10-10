---
title: apt クイックリファレンス
tags:
  - cheatsheet
  - apt
migrated_from: denisidoro/cheats (navi)
---

# apt クイックリファレンス

Debian 系の apt コマンド。root 権限が要るものは `sudo` を付ける。

## 調べる

| やりたいこと | コマンド | 注意 |
|---|---|---|
| パッケージ一覧を更新 | `apt update` | install / upgrade の前に実行する |
| 導入済みの一覧 | `apt list --installed` | |
| 更新できるものの一覧 | `apt list --upgradeable` | |
| 版の一覧 | `apt list -a <package>` | |
| 検索（名前と説明） | `apt search <query>` | |
| 詳細 | `apt show -a <package>` | |
| 依存先 | `apt depends <package>` | |
| 逆依存（何から使われているか） | `apt rdepends <package>` | |

## 入れる・更新する

| やりたいこと | コマンド | 注意 |
|---|---|---|
| 入れる | `apt install <package>` | |
| ローカルの deb を入れる | `apt install <path.deb>` | パス指定（`./` を付ける） |
| 全部更新 | `apt upgrade` | 依存の追加・削除はしない |
| 全部更新（依存の追加・削除あり） | `apt full-upgrade` | |
| 1つだけ更新 | `apt install --only-upgrade <package>` | |
| 版を指定して入れる（ダウングレード） | `apt install <package>=<version>` | 版は `apt list -a` で調べる |

## 消す

| やりたいこと | コマンド | 注意 |
|---|---|---|
| 消す | `apt remove <package>` | 設定ファイルは残る |
| 設定ファイルごと消す | `apt purge <package>` | |
| 不要な依存を消す | `apt autoremove` | |
