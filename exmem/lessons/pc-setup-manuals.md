---
type: knowledge
title: 環境セットアップ手順書（Win11 / Debian系）
status: active
tags:
  - setup
  - dotfiles
  - windows
  - linux
  - tool/git
  - tls
aliases:
  - 環境セットアップ手順書
  - cheatsheets/env
  - guides/howto
  - PC再セットアップ
created: 2026-10-03
updated: 2026-10-16
sources:
  - Claude Code conversation "git の CA バンドルと schannel の判断" (2026-10-10。GIT_SSL_CAINFO の取りやめ)
  - Claude Code conversation "新しいPCの初回セットアップ設計" (2026-10-06。「初回の取得」)
  - Claude Code conversation "環境セットアップ手順書(Win11 / Debian系)の整備と scripts/linux の統合" (2026-10-03)
  - "resources/cheatsheets/env/（現 resources/guides/howto/）と dotfiles scripts/linux/（2026-10-03 に確認）"
---

# 環境セットアップ手順書（Win11 / Debian系）

## Purpose

PCを入れ替えても、手順書とスクリプトで同じ環境を再現できるようにする。手順書とスクリプトは dotfiles リポジトリにある（手順書は `docs/setup/`。2026-10-16 に workbase の `guides/howto/` から移した）。範囲は「インストール準備」から「エディタでテキストが見られる」まで。

## 場所

- 手順書は dotfiles の `docs/setup/` の `win11.md`、`debian-family.md`、`fonts-setup.md`（2026-10-03 に実物で確認。2026-10-10 に `cheatsheets/env/` から `guides/howto/` へ移動し、`fonts.md` は `fonts-setup.md` に改名した。2026-10-16 に dotfiles の `docs/setup/` へ移した）。
- 書き方のルールは dotfiles の `docs/setup/README.md`（dotfiles 固有の点）と、workbase の `resources/guides/AGENTS.md`（書式・文体。旧 `cheatsheets/CLAUDE.md`）。ルールを先に作ってから Win11、Debian系の順に書いた。ぶれを防ぐため。
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

- dotfiles 固有の決定なので、dotfiles の `docs/decisions.md` に移した（2026-10-16）。ここでの要点は、差分が3割を下回るなら系統で1本にする、という上の基準だけ。

## Facts

確認済み（Web 情報、2026-10-03 時点）:

- Windows 11 の最新は 25H2（ビルド 26200 系）。
- MX Linux 25.3 "Infinity" は Debian 13.7 "trixie" ベース。2026-09-20 公開。通常版は systemd が既定で、SysVinit 版は別。
- Ubuntu 26.04 LTS は 2026-04 公開。Wayland が既定で `~/.xprofile` は読まれない。Linux Mint 22.3 は Ubuntu 24.04 ベース。Mint 23 は 2026-12 予定で未公開。
- Ubuntu 24.04 以降の apt ソースは deb822 形式（`/etc/apt/sources.list.d/ubuntu.sources`）。旧メモの `sed ... sources.list` は効かない。
- Debian 13 は fcitx5 を使う。MX フォーラムの `fcitx`（v4）の手順は古い。
- MX のインストーラーは、指定のない ESP を触らない。ESP は FAT32 で、フラグは `boot` と `esp`。

実行して確認したこと（WSL Ubuntu 24.04）: `scripts/linux/` の構文チェックなどは、dotfiles の `docs/decisions.md`「`scripts/wsl/` を `scripts/linux/` に改名して1本化した」と `tests/README.md` が正。試験の方法は [[shell-script-testing-wsl]]。

仮説（未確認）: MX で Secure Boot を有効のまま入れられるか。各インストーラーのメニュー名（「カスタム」「Something else」など）。Debian 13 / MX で `os-prober` が既定で無効か。Rufus で MX を書き込むとき ISO モードで起動するか（DD モードが要るか）。`fcitx5-config-qt` が MX と Ubuntu にあるか（`23_ja.sh` はあるほうを選ぶ）。MX の Package Installer の日本語化の項目名。Mint の差分全般。

## Gotchas

- **Windows の EFI を触らない**: ESP は新しく作らず、Windows のものを再利用する。フォーマットしない。`/boot/efi` にマウントし、`boot` と `esp` のフラグを確認する。
- **起動メニューに他の OS が出ない**: `/etc/default/grub` の `GRUB_DISABLE_OS_PROBER=false` にして `update-grub`。
- **OS を切り替えると時計が9時間ずれる**: Windows のレジストリ `RealTimeIsUniversal=1`。
- **デュアルブート前の Windows 側の準備**: 高速スタートアップを OFF にし、BitLocker / デバイスの暗号化が無効であることを確認する。
- **Windows の symlink が失敗する**: 開発者モードが OFF のとき。設定 → システム → 開発者向け。
- **OneDrive がドキュメントを付け替える**: PowerShell プロファイルのリンク先がずれる。OFF にする。
- **`setx` 後のターミナル**: 現在のセッションに反映されない。新しいターミナルを開く。
- **手順書に、廃止した手順やスクリプトの行が残っていた**（2026-10-06）: スクリプトを変えたとき、手順書を同じ作業で更新していなかった。手順書とスクリプトは同じリポジトリに置き、同じコミットで直す。

## 初回の取得（新しいPC。2026-10-06）

dotfiles を、新しい PC で最初にどう取得し、git の名前・メールをどう用意するか。

### Principles（初回の取得）

- 初回の clone は、最初から最終の置き場所（ghq の場所）に行う。別の場所（zip の展開先など）に取ると、取得もリンクも二重になる。
- 設定リポジトリのスクリプトは、clone 前には使えない（private だと、clone 前にスクリプトを匿名で取れない）。clone の前に必要なものは、スクリプトではなく、貼り付けるだけの短い手順にする。
- git は、パッケージ管理の正本（scoop）で入れた1種類だけにする。別経路の git が併存すると、撤去の手間と、PATH の優先順位の問題（システムの PATH がユーザーの PATH より先に見つかる。仮説）が生じる。
- PC ごとの値（git の名前・メール）は、`git config --global` ではなく、リポジトリ外のファイルに `git config --file` で書く。`~/.gitconfig` が設定リポジトリへの symlink のとき、リンク前に `--global` を使うと実ファイルができてリンクが `[ERR]` で止まり、リンク後に使うとリポジトリ内のファイルが書き換わる。
- 運用が未定の前提（リポジトリの公開・非公開など）は、手順に両方を並べて書き、決まったら一方を削除する。未定の間に、手順書の前提が実態とずれ、読み替えを誤る。
- OS 間で対称にするのは「役割」（同じ番号は同じ役割）で、OS 固有の事情（Windows の Git Credential Manager、ダブルクリックでウィンドウが閉じる問題など）は対称にしない。

### Decisions・Facts（初回の取得）

- 初回の clone の手順（scoop の git だけで最終の場所に clone、クイックスタートの4行、`11_git_identity` で git の名前・メールを作る）と、その実機での確認は、dotfiles の `docs/decisions.md`「初回は scoop の git だけで最終の場所に clone する」が正（2026-10-16 に移した）。

## git の設定の置き場（SSL バックエンドと credential。2026-10-06）

Windows の git で、SSL バックエンドを schannel に切り替えるかを PC ごとに選べるようにし、credential の設定をどのファイルに持たせるかを決めた。

### Principles（git の設定）

- リポジトリ管理で全 PC に配られる設定ファイルには、全 PC で同じ値だけを書く。PC ごとに選ぶ値は、リポジトリ外の PC ローカルのファイルに置く。共通ファイルに選択肢の既定値を書くと、ローカル側で「何も書かない」を選んでも共通側の値が効き、選択が意味を失う。
- 選択肢が1つしかない値は、質問せずに固定値として共通ファイルに持たせる。PC ローカルのファイルは「既にあれば触らない」運用だと、既存の PC に新しい値が届かない。共通ファイルなら `git pull` だけで届く。
- 「使わない」の動作は、何かを書くのではなく、何も書かないことで既定値に落とす。既定値が変わっても、スクリプトを直さずに追随できる。

### Decisions（git の設定）

- schannel を PC ごとの選択（`.gitconfig_local`）にし、credential は共通ファイルに固定値で持たせる決定は、dotfiles の `docs/decisions.md`「git の SSL バックエンド（schannel）は PC ごとの選択として…」が正（2026-10-16 に移した）。設定キーは `http.sslVerify`（`https.sslVerify` は無効。下の Gotchas）。

### Facts（git の設定）

- `git help --config` の一覧に `http.sslBackend` と `http.sslVerify` はあるが、`https.sslVerify` は無い（確認: 2026-10-06、根拠: git 2.56.0.windows.1 で実行）。
- `git config --file <ファイル> https.sslVerify true` は、未知のキーでもエラーにならず `[https]` セクションに書き込む（確認: 2026-10-06、根拠: 当初の指定でスクリプトの試験が通った）。
- scoop の git の system gitconfig は、Git Credential Manager を `credential.helper` にしている（確認: 2026-10-06、根拠: `git config --system --list --show-origin`）。
- `http.sslVerify` の既定は true なので、`y` のときに明示しても挙動は変わらず、設定の意図を残す効果だけがある（仮説）。
- `credential.helperselector.selected` は、Git for Windows の credential helper 選択ツールが記録する選択結果で、`manager` は Git Credential Manager を指す（仮説）。共通ファイルにあっても、Linux の git は未知のセクションとして無視するはず（仮説）。

### git の CA を `GIT_SSL_CAINFO` で指すのを取りやめ、schannel のままにする（2026-10-10 追記）

社内プロキシの CA を git にも効かせるため、環境変数 `GIT_SSL_CAINFO` に CA ファイルを指す案を実装しかけ、取りやめた。上の schannel の決定の補強にあたる。

**Principles**

- 環境全体に効く設定（ユーザー環境変数など、全プロセスが引き継ぐもの）は、実装の前に、影響範囲と外れたときの症状を示してユーザーに確認する。理由: 間違うと git の HTTPS 通信がすべて同時に失敗し、GUI アプリにも及ぶ。今回は実装した後にユーザーが懸念を指摘した。
- 信頼する CA の一覧を置き換える設定は、置き換え先が完全だと保証できるかを先に確かめる。保証できなければ、OS の信頼ストアを見る方式を選ぶ。理由: 保証できない一覧は、足りない CA の分だけ、通信が失敗する形で障害になる。
- PC 固有の値（絶対パス）は、リポジトリを指す設定ファイルに `git config --global` で書かない。理由: `~/.gitconfig` がリポジトリ内のファイルへの symlink のとき、書いた値がコミット対象になる。環境変数か PC ローカルのファイルに置く。

**Decisions**

- **git の SSL は schannel のままにし、`GIT_SSL_CAINFO` は設定しない**（2026-10-10）。根拠: ユーザーの決定。会社 CA だけのバンドルでは、完全性も、プロキシが全通信を再署名するかも保証できない。schannel は Windows の証明書ストア（ブラウザと同じ）を見る。却下案: `GIT_SSL_CAINFO` に会社 CA だけのバンドルを指す（既定の CA 一覧を置き換え、外れると全通信が失敗）。git 同梱の `ca-bundle.crt` に会社 CA を足した結合ファイル（git の更新のたびに作り直しが要るため採用されなかった）。

**Facts**

- `GIT_SSL_CAINFO` は `http.sslCAInfo` を上書きし、git が信頼する CA の一覧をそのファイルの内容に置き換える（仮説）。公式ドキュメントの記憶に基づき、実行では未確認。
- schannel では、検査型プロキシの下で失効確認が失敗して `CRYPT_E_NO_REVOCATION_CHECK` が出ることがある。`http.schannelCheckRevoke=false` で逃がせるが、失効確認を外す設定になる（仮説）。
- schannel の設定は、PC ローカルの `~/.gitconfig_local` に置く。`~/.gitconfig` はリポジトリ内の `home/.gitconfig` への symlink で、`--global` で書くとリポジトリのファイルが書き換わる（確認: 2026-10-06、根拠: `11_git_identity.bat` の実装と試験）。
- 実物（2026-10-11 に照合）: この PC に `GIT_SSL_CAINFO` のユーザー環境変数は無く、`git config --show-origin` で `http.sslBackend` `http.sslCAInfo` `http.schannelCheckRevoke` はいずれも出力が無かった（この PC では SSL の設定が未設定）。決定のとおり、`GIT_SSL_CAINFO` は設定されていない。

**Open Questions**

- 会社 PC で、プロキシ下の schannel が失効確認で失敗するか（`git -c http.sslBackend=schannel ls-remote <URL> HEAD` で確認する。2026-10-10 時点）。

### Gotchas（git の設定）

- **SSL の検証設定として `https.sslVerify true` を指定した**: git に `https.sslVerify` というキーは無く、`git config` は未知のキーも受け付けるため、エラーも警告も出ずに無効な設定が残る。`git help --config` で本物のキー（`http.sslVerify`）を確認して直した。設定キーは、書く前に `git help --config` で確認する。

### Open Questions（git の設定）

- 既に PC ローカルのファイルがある PC では、スクリプトが何も書かないため、schannel を使いたい場合は手で追記が要る。スクリプトで追記する仕組みにするか。
- 実機で schannel に切り替えたときの通信（clone、証明書の検証）は未確認。schannel を使う PC で、`.gitconfig_local` に追記して `git ls-remote` が通ることを確認する（2026-10-06 時点）。

## Open Questions

- MX Linux 25.3 の実機または VM で、`10 → 20 → 23 → 30` が通るか。Secure Boot、`os-prober`、インストーラーの名称が合っているか。
- Win11 の OOBE 手順（Rufus のオプション）が実機で動くか。
- Mint を Ubuntu 列に含めるか、Mint 23 の公開後に独立させるか。
- Fedora を足すときの構成（パッケージ管理の包み方、`manifests/dnf.txt` を別に持つか）。足す場合は dotfiles の `docs/setup/` に手順書を足す。
- GRUB のメニューを持つディストロをどれにするか（最後に入れた1台か、固定か）。

## Related

- [[fonts]]
- [[linux-multiboot-setup]]
- [[linux-distro-selection]]
- [[shell-script-testing-wsl]]
- [[obsidian-vault]]
