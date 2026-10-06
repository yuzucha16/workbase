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
updated: 2026-10-06
sources:
  - Claude Code conversation "新しいPCの初回セットアップ設計" (2026-10-06。「初回の取得」)
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

実行して確認したこと（WSL Ubuntu 24.04）: `scripts/linux/` の全 `.sh` の構文チェック、`lib.sh` の関数4つ（`dots_dir` / `is_wsl` / `distro_is` / `read_list`。2026-10-05 時点では8つ: `notes_dir` / `clone_workbase` / `link_obsidian` / `distro_ids` が加わった。確認: dotfiles の `lib.sh`。試験の方法は [[shell-script-testing-wsl]]）、`23_ja.sh` が WSL で何もせず終了、`30_link.sh -n` が `--src` なしで正しいリポジトリを指す、`apt.txt` と `apt.desktop.txt` が19パッケージの配列にまとまる。

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
- **初回を zip の展開先で番号順に実行し、その後 `50_repos` で ghq の場所に再取得して、`30_link` をもう一度実行していた**（2026-10-06）: 最初の置き場所が、最終の置き場所と違っていた。最初から最終の場所に clone する（下の「初回の取得」）。
- **手順書が「公開リポジトリなので HTTPS で取れる」と書いていたが、リポジトリは非公開だった**（2026-10-06）: 運用が未定のまま公開の前提で書かれ、直されていなかった。公開と非公開の両方の手順を併記した。
- **手順書に、使わないことにした `winget install Git.Git` と、削除済みスクリプトの行が残っていた**（2026-10-06）: スクリプトを変えたとき、手順書を同じ作業で更新していなかった。

## 初回の取得（新しいPC。2026-10-06）

dotfiles を、新しい PC で最初にどう取得し、git の名前・メールをどう用意するか。

### Principles（初回の取得）

- 初回の clone は、最初から最終の置き場所（ghq の場所）に行う。別の場所（zip の展開先など）に取ると、取得もリンクも二重になる。
- 設定リポジトリのスクリプトは、clone 前には使えない（private だと、clone 前にスクリプトを匿名で取れない）。clone の前に必要なものは、スクリプトではなく、貼り付けるだけの短い手順にする。
- git は、パッケージ管理の正本（scoop）で入れた1種類だけにする。別経路の git が併存すると、撤去の手間と、PATH の優先順位の問題（システムの PATH がユーザーの PATH より先に見つかる。仮説）が生じる。
- PC ごとの値（git の名前・メール）は、`git config --global` ではなく、リポジトリ外のファイルに `git config --file` で書く。`~/.gitconfig` が設定リポジトリへの symlink のとき、リンク前に `--global` を使うと実ファイルができてリンクが `[ERR]` で止まり、リンク後に使うとリポジトリ内のファイルが書き換わる。
- 運用が未定の前提（リポジトリの公開・非公開など）は、手順に両方を並べて書き、決まったら一方を削除する。未定の間に、手順書の前提が実態とずれ、読み替えを誤る。
- OS 間で対称にするのは「役割」（同じ番号は同じ役割）で、OS 固有の事情（Windows の Git Credential Manager、ダブルクリックでウィンドウが閉じる問題など）は対称にしない。

### Decisions（初回の取得。すべて 2026-10-06）

- **初回は最終の場所に直接 clone する。zip の取得は使わない**。根拠: 取得とリンクの二重が無くなり、番号の順序も変えずに済む。却下案: `50_repos` を前に出す（`ghq` と `GHQ_ROOT` に依存）、zip を最終の場所に展開して後で `.git` を付ける（複雑で、差分と改行の確認が要る）。
- **git は scoop だけにする。クイックスタートは、実行ポリシーの設定、scoop の導入、`scoop install git`、`git clone` の4行**。根拠: ユーザーの方針（scoop で完結したい）。管理者権限が要らず、PATH の優先順位の問題も起きない。却下案: winget の git で最初の clone をして、後で scoop の git に置き換える（git が2種類併存し、撤去と UAC が要る）。
- **手順1〜3（scoop と git の導入、clone）は、スクリプトにせず、README の冒頭の貼り付けブロックにする**。根拠: ユーザーの選択。private で、clone 前にスクリプトを取得できない。ファイルを介さないので、ダウンロードの印（`RemoteSigned` で止まる原因）も避けられる。却下案: ブラウザで Raw を保存して実行する `00_bootstrap.bat`（LF の `.bat` のラベルが壊れることがあり、受け渡しの手間もある）。
- **リポジトリの公開・非公開は未定のまま、手順書と README に両方の手順を併記する**。根拠: ユーザーの指示。決まったら、使わない方を削除する。却下案: 非公開だけを書く（公開にしたときに読み替えが要る）。
- **git の名前・メールは、新しいスクリプトで対話的に作る。無いときだけ作り、既にあれば触らない**。根拠: ユーザーの選択。リンクの前後どちらでも安全にするため `git config --file` を使う。却下案: 取得スクリプトの先頭で作る（リンクの後になる）、環境変数を設定するスクリプトの末尾で作る（git が必須になる）。

### Facts（初回の取得）

- リポジトリが private のとき、Raw の URL は匿名で 404 になり、匿名の `git ls-remote` は認証を求める（確認: 2026-10-06、根拠: `Invoke-WebRequest` が 404、`git ls-remote` が `could not read Username`）。
- scoop の git は、システムの `gitconfig` で `credential.helper` に Git Credential Manager を設定しており、clone でサインイン画面が開く（確認: 2026-10-06、根拠: `git config --system --list --show-origin`）。
- 新しい Windows アカウントで、クイックスタートの4行から `20_apps`、`30_link`、`50_repos` まで通った（確認: 2026-10-06、根拠: ユーザーの報告「問題なし」）。
- Ubuntu 24.04 の apt に `gh` 2.45.0 がある（確認: 2026-10-06、根拠: `apt-cache policy gh` の Candidate）。
- `winget list --id Git.Git -e` は、該当が無いと終了コード `-1978335212` を返す（確認: 2026-10-06、根拠: 実行した出力）。
- Linux で、非公開リポジトリを `gh auth login`（HTTPS、ブラウザ）と `gh auth setup-git` で clone する手順が通る（仮説）。新しい Linux の実機では未実行。
- 非公開から公開にしても、Windows の4行は変わらない。違いはサインイン画面が出るかどうかだけ（仮説）。

## git の設定の置き場（SSL バックエンドと credential。2026-10-06）

Windows の git で、SSL バックエンドを schannel に切り替えるかを PC ごとに選べるようにし、credential の設定をどのファイルに持たせるかを決めた。

### Principles（git の設定）

- リポジトリ管理で全 PC に配られる設定ファイルには、全 PC で同じ値だけを書く。PC ごとに選ぶ値は、リポジトリ外の PC ローカルのファイルに置く。共通ファイルに選択肢の既定値を書くと、ローカル側で「何も書かない」を選んでも共通側の値が効き、選択が意味を失う。
- 選択肢が1つしかない値は、質問せずに固定値として共通ファイルに持たせる。PC ローカルのファイルは「既にあれば触らない」運用だと、既存の PC に新しい値が届かない。共通ファイルなら `git pull` だけで届く。
- 「使わない」の動作は、何かを書くのではなく、何も書かないことで既定値に落とす。既定値が変わっても、スクリプトを直さずに追随できる。

### Decisions（git の設定。すべて 2026-10-06）

- **SSL バックエンド（schannel）は、`11_git_identity.bat` が `[y/N]` で聞き、`y` のときだけ PC ローカルの `.gitconfig_local` に `http.sslBackend = schannel` と `http.sslVerify = true` を書く。`n`・空は何も書かない**。根拠: ユーザーの依頼。schannel を使うかは PC ごとに選ぶものなので、PC ローカルに置く。何も書かなければ、暗黙に OpenSSL になる。却下案: 共通ファイル `home/.gitconfig` に直書き（`n` を選んでも schannel になり、Linux にも配られる）。
- **`credential.helperselector.selected = manager` は、共通ファイル `home/.gitconfig` に静的に持たせ、スクリプトからは書かない**。根拠: ユーザーの判断。Windows の全 PC で `manager`（Git Credential Manager）に固定で、選択肢が無い。却下案: `y/N` で聞く（選択肢が無い）、共通ファイルとスクリプトの両方に書く（どちらが効くか分かりにくい）。
- **設定キーは `https.sslVerify` ではなく `http.sslVerify` にする**。根拠: ユーザーの承認。`git help --config` に `https.sslVerify` は無い。却下案: 当初の指定どおり `[https] sslVerify`（効かない）。

### Facts（git の設定）

- `git help --config` の一覧に `http.sslBackend` と `http.sslVerify` はあるが、`https.sslVerify` は無い（確認: 2026-10-06、根拠: git 2.56.0.windows.1 で実行）。
- `git config --file <ファイル> https.sslVerify true` は、未知のキーでもエラーにならず `[https]` セクションに書き込む（確認: 2026-10-06、根拠: 当初の指定でスクリプトの試験が通った）。
- dotfiles に `scripts/windows/11_git_identity.bat` があり、共通の `home/.gitconfig` に `[credential "helperselector"]` の `selected = manager` がある（確認: 2026-10-06、根拠: ファイルの存在と内容）。この PC の `~/.gitconfig_local` に、SSL の設定はまだ無い。
- scoop の git の system gitconfig は、Git Credential Manager を `credential.helper` にしている（確認: 2026-10-06、根拠: `git config --system --list --show-origin`）。
- `http.sslVerify` の既定は true なので、`y` のときに明示しても挙動は変わらず、設定の意図を残す効果だけがある（仮説）。
- `credential.helperselector.selected` は、Git for Windows の credential helper 選択ツールが記録する選択結果で、`manager` は Git Credential Manager を指す（仮説）。共通ファイルにあっても、Linux の git は未知のセクションとして無視するはず（仮説）。

### Gotchas（git の設定）

- **SSL の検証設定として `https.sslVerify true` を指定した**: git に `https.sslVerify` というキーは無く、`git config` は未知のキーも受け付けるため、エラーも警告も出ずに無効な設定が残る。`git help --config` で本物のキー（`http.sslVerify`）を確認して直した。設定キーは、書く前に `git help --config` で確認する。

### Open Questions（git の設定）

- 既に PC ローカルのファイルがある PC では、スクリプトが何も書かないため、schannel を使いたい場合は手で追記が要る。スクリプトで追記する仕組みにするか。
- 実機で schannel に切り替えたときの通信（clone、証明書の検証）は未確認。schannel を使う PC で、`.gitconfig_local` に追記して `git ls-remote` が通ることを確認する（2026-10-06 時点）。

## Open Questions

- MX Linux 25.3 の実機または VM で、`10 → 20 → 23 → 30` が通るか。Secure Boot、`os-prober`、インストーラーの名称が合っているか。
- Win11 の OOBE 手順（Rufus のオプション）が実機で動くか。
- Mint を Ubuntu 列に含めるか、Mint 23 の公開後に独立させるか。
- Fedora を足すときの構成（`lib.sh` に `pkg_install` を包むか、`manifests/dnf.txt` を別に持つか）。足す場合は `env/fedora.md` を新設する。
- `env/` の手順書に、`workbase`（旧 `notes`）が公開になった場合に支障のある記述がないか（公開範囲は未定。[[obsidian-vault]] の Open Questions）。2026-10-06 に、clone の節が公開・非公開の併記になり、一部は解消した。
- dotfiles のリポジトリを公開にするか、非公開にするか。決まったら、README の冒頭と手順書の clone の節から、使わない方を削除する。
- Linux の非公開リポジトリの clone に、SSH 鍵を使う案と `gh` を使う案のどちらを標準にするか。新しい Linux の実機で、`gh auth login` から clone までを確認する（2026-10-06 時点）。
- GRUB のメニューを持つディストロをどれにするか（最後に入れた1台か、固定か）。

## Related

- [[fonts]]
- [[linux-multiboot-setup]]
- [[linux-distro-selection]]
- [[shell-script-testing-wsl]]
- [[obsidian-vault]]
