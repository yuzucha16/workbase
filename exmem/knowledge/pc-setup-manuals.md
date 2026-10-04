---
type: knowledge
title: 環境セットアップ手順書（Win11 / Debian系）
status: active
tags:
  - setup
  - dotfiles
  - windows
  - linux
aliases:
  - 環境セットアップ手順書
  - cheatsheets/env
  - PC再セットアップ
created: 2026-10-03
updated: 2026-10-03
sources:
  - Claude Code conversation "環境セットアップ手順書(Win11 / Debian系)の整備と scripts/linux の統合" (2026-10-03)
  - "resources/cheatsheets/env/ と dotfiles scripts/linux/（2026-10-03 に確認）"
---

# 環境セットアップ手順書（Win11 / Debian系）

## Purpose

PCを入れ替えても、手順書とスクリプトで同じ環境を再現できるようにする。手順書は `resources/cheatsheets/env/` にあり、スクリプトは dotfiles リポジトリが正。範囲は「インストール準備」から「エディタでテキストが見られる」まで。

## 場所

- `resources/cheatsheets/env/win11.md`、`debian-family.md`、`fonts.md`（2026-10-03 に実物で確認）。
- 書き方のルールは `resources/cheatsheets/CLAUDE.md`（`handson/` や `exmem/` の慣例に合わせて `cheatsheets/` 直下）。ルールを先に作ってから Win11、Debian系の順に書いた。ぶれを防ぐため。
- 旧メモ3つ（`win_setup` / `linux_setup` / `setup_alma`）は削除した（古く、会社PC由来の情報が多い。履歴から復元できる）。

## Principles

- 個人情報（メール、社員番号、アカウント名、会社名・VPN）は手順書に残さない。git の名前・メールは `~/.gitconfig_local` に置く。
- バージョン依存の情報は、冒頭の**対応バージョン表**にだけ書く。ディストロ差分は各章末の**差分表**に書き、本文に `[MX]` タグを散らさない。差分が全体の3割を超えたらファイルを分ける。
- 手順書とスクリプトで一覧を重複させない（パッケージは `manifests/` に外出し）。

## Decisions

### 手順書はパッケージ系統で分ける（2026-10-03）

- 決めたこと: `win11.md` と `debian-family.md` の2本。Alma Linux はスコープ外（ユーザー判断）。Mint は Ubuntu 列に準ずる扱いで、差分が出たら独立の列にする（未検証）。MX は systemd 版前提。
- 根拠: MX / Ubuntu / Mint は apt 系でほぼ同じ。将来の版追加は表の更新で済む。
- 却下案: ディストロごとに1ファイル。

### パーティションは Windows + Linux のマルチブート（ユーザー指定）

- EFI 共有、swap 8GB 共有、`/` はディストロごと、非暗号化、`/home` 分離なし。詳細な構成と実績は [[linux-multiboot-setup]]。
- Windows を先に入れ、Linux 用の領域はインストール後に C: を縮小して作る。Linux 側の GRUB が Windows を拾いやすい。
- 却下案: LUKS / LVM、`/home` 共有（設定が衝突する）、OS ごとの ESP、Linux を先に入れる。

### Win11 のネット無しセットアップは Rufus の「オンライン Microsoft アカウントの要件を削除する」（2026-10-03）

- 根拠: 25H2 では `oobe\bypassnro` が廃止され、`start ms-cxh:localonly` も新しいビルド（26220.6772 以降）で修正された（Web 情報。参考: Winaero、Thurrott）。
- **手順の実機確認は未実施**。

### `scripts/wsl/` を `scripts/linux/` に改名して1本化（2026-10-03）

- 決めたこと: WSL とネイティブ共通。違いは `lib.sh` の `is_wsl` などで分岐する。パッケージ一覧は `manifests/apt.txt`（共通）と `apt.desktop.txt`（ネイティブのみ）。日本語入力・フォントは `23_ja.sh` に分離（WSL では何もしない）。`30_link.sh` の `--src` の既定は、スクリプトの位置から自動判定する。
- 根拠: WSL 固有の差分は約3か所（1割強）で、3割基準を下回る。Windows の `apps.txt` と対称にできる。
- 却下案: `wsl/` と `linux/` に分離（約240行が重複）、`linux/` を本体にして `wsl/` を薄いラッパーにする。

## Facts

確認済み（Web 情報、2026-10-03 時点）:

- Windows 11 の最新は 25H2（ビルド 26200 系）。
- MX Linux 25.3 "Infinity" は Debian 13.7 "trixie" ベース。2026-09-20 公開。通常版は systemd が既定で、SysVinit 版は別。
- Ubuntu 26.04 LTS は 2026-04 公開。Wayland が既定で `~/.xprofile` は読まれない。Linux Mint 22.3 は Ubuntu 24.04 ベース。Mint 23 は 2026-12 予定で未公開。
- Ubuntu 24.04 以降の apt ソースは deb822 形式（`/etc/apt/sources.list.d/ubuntu.sources`）。旧メモの `sed ... sources.list` は効かない。
- Debian 13 は fcitx5 を使う。MX フォーラムの `fcitx`（v4）の手順は古い。
- MX のインストーラーは、指定のない ESP を触らない。ESP は FAT32 で、フラグは `boot` と `esp`。
- dotfiles の `GHQ_ROOT` の既定値は、Linux で `~/vault/repos`。

実行して確認したこと（WSL Ubuntu 24.04）: `scripts/linux/` の全 `.sh` の構文チェック、`lib.sh` の関数4つ（`dots_dir` / `is_wsl` / `distro_is` / `read_list`）、`23_ja.sh` が WSL で何もせず終了、`30_link.sh -n` が `--src` なしで正しいリポジトリを指す、`apt.txt` と `apt.desktop.txt` が19パッケージの配列にまとまる。

仮説（未確認）: MX で Secure Boot を有効のまま入れられるか。各インストーラーのメニュー名（「カスタム」「Something else」など）。Debian 13 / MX で `os-prober` が既定で無効か。Rufus で MX を書き込むとき ISO モードで起動するか（DD モードが要るか）。`fcitx5-config-qt` が MX と Ubuntu にあるか（`23_ja.sh` はあるほうを選ぶ）。MX の Package Installer の日本語化の項目名。Mint の差分全般。

## Gotchas

- **Windows の EFI を触らない**: ESP は新しく作らず、Windows のものを再利用する。フォーマットしない。`/boot/efi` にマウントし、`boot` と `esp` のフラグを確認する。
- **起動メニューに他の OS が出ない**: `/etc/default/grub` の `GRUB_DISABLE_OS_PROBER=false` にして `update-grub`。
- **OS を切り替えると時計が9時間ずれる**: Windows のレジストリ `RealTimeIsUniversal=1`。
- **デュアルブート前の Windows 側の準備**: 高速スタートアップを OFF にし、BitLocker / デバイスの暗号化が無効であることを確認する。
- **`30_link.sh` が `[ERR]` で止まる**: 展開先に実ファイル（初期の `.bashrc` など）があるため。自動退避はしない。手で `mv` してから再実行する。
- **Windows の symlink が失敗する**: 開発者モードが OFF のとき。設定 → システム → 開発者向け。
- **OneDrive がドキュメントを付け替える**: PowerShell プロファイルのリンク先がずれる。OFF にする。
- **`setx` 後のターミナル**: 現在のセッションに反映されない。新しいターミナルを開く。
- 旧スクリプト名（`w1a_*`, `w2a_*`）が `apps*.txt` と `links.map` のコメントに残っていた。現在の名前に直した。

## Open Questions

- MX Linux 25.3 の実機または VM で、`10 → 20 → 23 → 30` が通るか。Secure Boot、`os-prober`、インストーラーの名称が合っているか。
- Win11 の OOBE 手順（Rufus のオプション）が実機で動くか。
- Mint を Ubuntu 列に含めるか、Mint 23 の公開後に独立させるか。
- Fedora を足すときの構成（`lib.sh` に `pkg_install` を包むか、`manifests/dnf.txt` を別に持つか）。足す場合は `env/fedora.md` を新設する。
- `env/` の手順書に、`notes` リポジトリが公開だった場合に支障のある記述がないか（公開範囲は [[obsidian-vault]] の Open Questions）。
- GRUB のメニューを持つディストロをどれにするか（最後に入れた1台か、固定か）。

## Related

- [[fonts]]
- [[linux-multiboot-setup]]
- [[linux-distro-selection]]
- [[obsidian-vault]]
