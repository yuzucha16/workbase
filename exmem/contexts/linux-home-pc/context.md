---
type: project
title: 自宅PCのLinux移行 Project Context
status: active
tags:
  - linux
  - setup
aliases:
  - 自宅PCのLinux移行 Project Context
created: 2026-10-02
updated: 2026-10-02
---

# 自宅PCのLinux移行 Project Context

## Current State

- ディストロは MX Linux 25（Debian 13 trixie、Xfce）に決めた。Fedora 44は運用負荷で見送り、Mint 22は次点（[[linux-distro-selection]]）。
- 256GB SSDは、共有ESP（1GB、FAT32）+ 共有swap（8GB）+ MX Linuxのroot（64GB）+ 未割り当て（約165GB）の構成で、MX Linuxのインストールを進めていた（[[linux-multiboot-setup]]）。インストール完了・再起動後のGRUB起動は、メモの時点で未確認。
- 対象機は中古のThinkPad X13 Gen1の想定。ただし、上の256GB SSDがこの機体のものかは未確認。
- Windowsとのデュアルブートにするかは未決定。
- Mozc（日本語入力）とUSBデバイス（udev）は、勉強用に手動構築する方針で、未着手。

## Next Actions

- 再起動してGRUBから起動できるか確認する。ESPが実際にFAT32かも確認する。
- Zedを公式インストールスクリプトまたはFlatpakで導入する。
- Neovimは当面apt標準版（0.10.4系）で運用する。
- Mozc（fcitx5 + fcitx5-mozc）とudevルールの学習用お題を決める。
- 2つ目のディストロを入れる場合は、未割り当て領域から新しいrootを切り出し、既存のESPとswapを指定する。os-proberの検出を確認する。
- 慣れたらMint 22への移行を検討する。

## Goal

Windowsのメモリ消費を避け、文書作成・ブラウジング・簡単なプログラミング用途のLinux環境を自宅PCに作る。

## Open Questions

- MX Linux 25でのZed導入方法（公式スクリプトかdebian.griffo.ioか）。
- デュアルブートにするか、Linuxのみにするか。
- 複数ディストロ混在で、os-proberが各エントリを維持できるか。

## Related

- [[linux-distro-selection]]
- [[linux-multiboot-setup]]
- [[modern-cli-tools]]
