---
type: knowledge
title: 自宅PCのLinuxディストロ選定
status: active
tags:
  - linux
  - setup
  - tool/zed
  - tool/neovim
  - ai/claude
aliases:
  - Linuxディストロ選定
  - MX Linux採用
  - ThinkPad X13のLinux移行
created: 2026-10-02
updated: 2026-10-02
sources:
  - Claude conversation "自宅PC(ThinkPad X13 Gen1)のLinuxディストリ選定" (2026-10-02)
  - Claude conversation "Linuxディストロ選定(パッケージ鮮度比較)" (2026-10-02)
---

# 自宅PCのLinuxディストロ選定

## Purpose

自宅PCをWindowsからLinuxへ移行する（Windowsのメモリ消費に疲れたため）。中古のLenovo ThinkPad X13 Gen1に、文書作成・ブラウジング・簡単なプログラミング用途のディストロを選ぶ。勉強も兼ねて多少ハマるのは許容する。導入作業は [[linux-multiboot-setup]]。

## Principles

- ディストロ公式のパッケージ（apt / dnf）は安定性優先で更新が遅い。ZedやNeovimのように上流の開発が速いツールは、公式リポジトリでは新しさが追いつかない。
- Zedはディストロのパッケージではなく、公式インストールスクリプトで入れる。
- 比較はバージョン数値で行い、同名の別バージョンを混同しない（会話でMintとMXのNeovimを取り違えた）。
- DistroWatchのPage Hit Rankingは閲覧数であり、インストール数・実使用者数ではない。

## Decisions

### MX Linux 25を採用する（2026-10-02）

- 根拠: Xfceで軽い。sysVinit / systemdを選べる。Debian 13（trixie）ベースでNeovimが0.10.4系まで上がっており、実用上十分。以前MX Linuxを使って良い印象があったことも影響していると推測される（要本人確認）。MX Toolsの完成度も評価されている。
- 経緯: 当初はLinux Mint（Cinnamon）でほぼ決めかけていた（Windowsからの移行のしやすさ、情報量、Zed / Obsidianとの親和性）。

### Fedora Workstation 44は見送り

- パッケージは最も新しい（Neovim 0.12.4系）が、約13か月でサポートが終わるため半年ごとのメジャーアップグレードが事実上必須。運用負荷を理由に除外。

### Mint 22は次点

- ある程度MX Linuxに慣れた後の移行先候補。Ubuntuベースでaptの体系が共通なので、MXからの移行ハードルが低い。

### その他に検討して採用しなかった案

- Ubuntu本体: メモリ消費が移行の動機と矛盾する。
- Debian（素）: 教材的価値はあるが、初期セットアップの手間とドキュメントの少なさから母艦には積極採用しない。勉強用サブ機や仮想環境なら選択肢。
- Xubuntu / Lubuntu / EndeavourOS: 候補に挙げたが比較の中心にならなかった。

## Facts

### Neovimのバージョン比較（apt / dnf、2026年10月時点）

| ディストロ | ベース | Neovim |
|---|---|---|
| Linux Mint 22系 | Ubuntu 24.04 noble | 0.9.5-6ubuntu2 |
| MX Linux 23系 | Debian 12 bookworm | 0.7.2-7 |
| MX Linux 25系 | Debian 13 trixie | 0.10.4-8 |
| Fedora 43（現行安定版） | - | 0.11.6-1 |
| Fedora 44 | - | 0.12.4-3 |

- Fedora 46は2026年10月時点でRawhide（開発版）段階。安定版は2027年4月頃の見込み。
- Debian bookworm-backportsにneovimは来ていない（調査時点で未確認 = 提供なし）。
- ZedはDebian / Ubuntu / Mint / MX Linuxのいずれの公式aptリポジトリにもない（2026年10月時点）。公式インストールスクリプト、Flatpak、コミュニティAPTリポジトリ（debian.griffo.io）で導入する。
- Fedoraは約6か月サイクル。Ubuntu LTS（Mintの土台）はリリース後ツールチェーンをほぼ固定し、Mintは体感で最新から半年〜2年程度遅れうる（仮説寄りの目安）。
- MX LinuxはDebian stableをベースに、新しめカーネル選択肢（AHS）を提供し、SysVinit / systemdを選べる。
- apt系とdnf系はコマンドがほぼ1:1に対応するが、低レベルツール（dpkg ⇔ rpm）とサードパーティリポジトリの追加方法が異なる。
- Debian系で更新が比較的速い候補（仮説）: Siduction、SparkyLinux（Rolling）、Kali、Parrot OS。鮮度を安定性より優先する用途向け。

### 実物との照合（2026-10-02）

- 最初のメモは「Mint → MX Linuxへ変更。詳細は `dev-editor-setup.md` 側で更新済み」と書いていたが、`dev-editor-setup.md` はexmemに存在しない。変更理由は上のパッケージ比較メモで補えた。
- 参照されたNeovimの鮮度比較は、Claudeの `web_fetch` がpkgs.org / repology.org / debian.griffo.io を取得できず（robots.txtで拒否）、`web_search` のスニペットと packages.debian.org / packages.fedoraproject.org の検索結果で補った値。

## Gotchas

### robots.txtでクローラーが拒否されるサイトがある

- pkgs.org、repology.org、debian.griffo.ioのPackagesファイルは `web_fetch` で取れない。代替として、検索スニペットと公式のパッケージ検索ページから補った。

### バージョンの取り違え

- 「MX Linuxのneovimが0.7系」の話が、一時「Mintが0.7系」と混同された。MX Linux 23系が0.7.2、Mint 22は0.9.5。

## Open Questions

- MX Linux 25（trixie）でのZed導入方法: 公式インストールスクリプトか、debian.griffo.ioのtrixie対応か。
- Neovimを標準apt版（0.10.4系）のまま使うか、公式リリース版に切り替えるか（必要になったとき判断する）。
- Mozc（日本語入力）とUSBデバイス（udev）周りを、勉強用に手動構築したい要望への対応（選択肢の提示のみで未着手）。
- Windowsとのデュアルブートにするか、まるごとLinuxにするか。256GB SSDにLinuxを入れた記録（[[linux-multiboot-setup]]）はあるが、それがThinkPad X13のSSDかは未確認。

## Next Actions

- MX Linux 25をインストールし、Xfce環境に慣れる。
- Zedは公式インストールスクリプトまたはFlatpakで導入する（debian.griffo.ioのtrixie対応を事前に確認）。
- Neovimは当面apt標準版で運用し、不足を感じたら公式リリース版を検討する。
- Mozcセットアップ（fcitx5 + fcitx5-mozcなど）とUSBデバイス周り（`lsusb` / udevルール作成）の学習用お題を決める。
- 慣れたらLinux Mint 22への移行を検討する。必要ならMXを仮想環境やUSBブートで並行して試す。

## Related

- [[linux-multiboot-setup]]
- [[modern-cli-tools]]
- [[zed-acp]]
