---
type: knowledge
title: 256GB SSDのマルチブートLinux構成（MX Linuxインストール）
status: active
tags:
  - linux
  - setup
  - ai/claude
aliases:
  - マルチブートLinux
  - 共有ESP構成
  - MX Linuxインストール
created: 2026-10-02
updated: 2026-10-10
sources:
  - Claude conversation "256GB SSD マルチブートLinux環境構築(MX Linuxインストール)" (2026-10-02)
---

# 256GB SSDのマルチブートLinux構成（MX Linuxインストール）

## Purpose

256GBのSSDに複数のLinuxディストロを共存させる。共有ESP + 共有swap + ディストロごとに独立したrootパーティションという「お手軽」構成で、ディストロ追加時は未割り当て領域から新しいrootを切り出す。第一弾としてMX Linuxを入れた（[[linux-distro-selection]]）。

## Principles

- 「お手軽」を優先する。管理が複雑になる機構（個別ESP、swapファイル併用、Zram）は足さない。
- UEFIのESPはFAT32でなければならない。
- 2つ目以降のディストロでは、既存のESPとswapを指定し、新しいrootだけを作る。

## パーティション構成（確定）

`/dev/nvme0n1`、256GB（実測238.5GB）、GPT。

| パーティション | サイズ | 種類 | 用途 |
|---|---|---|---|
| `nvme0n1p1` | 1.0GB | ESP、FAT32 | 全ディストロ共有 |
| `nvme0n1p2` | 8.0GB | linux-swap | 全ディストロ共有 |
| `nvme0n1p3` | 64.0GB | ext4 | MX Linuxのroot |
| 残り | 約165GB | 未割り当て | 今後のディストロ追加用 |

`/home` は分離せず、rootのみ（「お手軽」重視）。

## Decisions

### 共有ESP方式を採用（2026-10-02）

- 根拠: 個別ESPは管理が煩雑。「お手軽」重視の方針に合う。
- 却下案: ディストロごとに個別ESPを作る（確実だが面倒）。

### swapは既存のパーティション（8GB）を使い、インストーラのswapファイル追加は使わない

- 根拠: 専用swapパーティションがあるので、swapファイル（3GB）やZramを併用しても管理が複雑になるだけ。
- 却下案: swapファイル併用、Zram swap（メモリが潤沢なので不要と判断）。

### GRUBのインストール先はESP（`nvme0n1p1`）

- UEFIブートなのでMBR / PBRは選ばない。「LinuxおよびWindows向けにGRUBをインストール」（os-prober相当）はチェックのまま。複数ディストロを追加するので、検出機能をオンにしておく。

## Facts

- MX Linuxインストーラのブートローダー設定は MBR / PBR / ESP の3択。
- swap設定画面には、パーティション型swapとは別に「swapファイルを作成する」オプション（デフォルトでオン、`/swap/swap` に3072MB）がある。既存のswapパーティションとは独立した追加のswap。
- Zram swapは、RAM上に圧縮領域を確保してswap代わりに使う。ディスクI/O削減・SSD延命の利点があり、CPU負荷とRAM消費がトレードオフ。
- 対象機は中古の ThinkPad X13 Gen1 の想定。ただし、上の 256GB SSD がこの機体のものかは未確認（2026-10-02 時点。`contexts/linux-home-pc` から移した）。
- インストーラのESPの「フォーマット」欄にある「(FAT32)を確保」は、「既存のファイルシステムを保持しフォーマットし直さない」という意味と解釈した。仮説（表記のみでの判断）。

## Gotchas

### ESPをext4で作ってしまった

- 状況: GPartedで最初に作ったESP用パーティション（#1）がext4でフォーマットされていた。UEFIのESPはFAT32必須なので起動できない。
- 解決: FAT32で作り直し、`esp` フラグを付けた。

### swapが合計11GBになりかける

- 状況: 8GBのswapパーティションがあるのに、MX Linuxインストーラがデフォルトでswapファイル作成にチェックを入れていた。見落とすと意図しない構成になる。
- 解決: swapファイルのチェックを外す。

## Open Questions

- ESPが実際にFAT32のままか（「(FAT32)を確保」の表記だけでは断定できない）。インストール完了後に確認する。
- 2つ目以降のディストロで、既存のESPとswapをどう選択・共有させるか（インストーラごとに挙動が違う可能性）。
- os-proberが、複数ディストロ混在で各OSのブートエントリを正しく検出・維持できるか（追加のたびに要検証）。
- `/home` を将来分離するか。
- MX Linux 25 での Zed の導入方法（公式スクリプトか debian.griffo.io か）。
- Windows とのデュアルブートにするか、Linux のみにするか。

## Next Actions

- インストール完了後、再起動してGRUBメニューから起動できるか確認する。
- 2つ目のディストロでは、未割り当て領域（約165GB）から新しいrootを切り出し、既存のESP（FAT32）とswap（8GB）を指定して入れる。
- ディストロ追加後、os-proberが全ディストロを検出しているか確認する。
- Zed を公式インストールスクリプトまたは Flatpak で導入する。Neovim は当面 apt 標準版（0.10.4 系）で使う。
- Mozc（fcitx5 + fcitx5-mozc）と udev ルールを、勉強用に手動で構築する（お題は未決）。
- 慣れたら Mint 22 への移行を検討する（[[linux-distro-selection]]）。

## Related

- [[linux-distro-selection]]
