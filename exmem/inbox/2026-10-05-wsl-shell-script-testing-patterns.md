---
type: inbox
title: WSL でシェルスクリプトを試験する（環境判定の差し替えと偽の HOME）
tags:
  - tool/wsl
  - dotfiles
  - shell
  - testing
  - stow
created: 2026-10-05
kit: 2026-10-05.5
sources:
  - Claude Code conversation "dotfiles の Linux 対応と WSL での試験"
---

# WSL でシェルスクリプトを試験する（環境判定の差し替えと偽の HOME）

## Goal
WSL とネイティブ Linux で分岐するシェルスクリプト（dotfiles の `30_link.sh` や `50_repos.sh` など）を、ネイティブ Linux の実機が無くても、実環境を壊さずに試験する方法をまとめる。項目の頭に【汎用】（他の WSL / Linux のスクリプトでも使える）と【この件】（dotfiles の Linux 対応、2026-10-05 に固有）を付けて分ける。
統合先の候補: 新規トピック（キーワード: wsl, test, shell, stow, dotfiles）。【この件】の部分は、狭い候補として knowledge/pc-setup-manuals.md（キーワード: scripts/linux, dotfiles, wsl）

## Principles
- 【汎用】環境の判定（WSL かネイティブか）は1つの関数にまとめ、差し替え用の環境変数（例: `/proc/version` の場所を指す変数）を用意する。理由: ネイティブ Linux の実機が無くても、WSL 上で両方の分岐を試験できる。
- 【汎用】試験は、一時ディレクトリ（`mktemp -d`）、偽の HOME、スクリプトの上書き用の指定（`--dst` や環境変数）に閉じ込め、実環境の `~` を変更しない。理由: 試験の失敗が、普段使いの設定を壊さないようにする。
- 【汎用】外部コマンドと通信は、偽物に差し替える。コマンド（例: `ghq`）は PATH の先頭に置いた偽の実行ファイルで、clone 元はローカルの bare リポジトリにする。理由: ネットワークや本物の副作用に依存せず、再現できる。
- 【汎用】リンクや clone を扱うスクリプトは、「新規作成」「再実行（冪等）」「dry-run は何も作らない」「元に戻す（unlink）」「実体が既にあれば止まって変更しない」「リンク切れの置き換え」「元が無ければ skip」を最低限の観点にする。理由: リンク配置の事故（上書き、消し過ぎ）の主な入口がこの7つ。
- 【汎用】差し替えた試験に加えて、本物の環境で動く確認を1項目は入れる。理由: 差し替えが本物と食い違うと、試験が通っても実機で動かない。

## Decisions
なし

## Facts
- 【汎用】構文は `bash -n` で、`.profile` は `/bin/sh -n` で確認できる。Ubuntu 24.04 の `/bin/sh` は dash なので、POSIX の範囲で書けているかも分かる（確認: 2026-10-05、根拠: `readlink -f /bin/sh` が dash を指した）。
- 【汎用】Windows から WSL のスクリプトは `wsl -e bash /mnt/c/<パス>/test.sh` で実行できる。スクリプトは LF で書く（確認: 2026-10-05、根拠: 実行した。CRLF で失敗するかは未実施で、仮説）。
- 【汎用】`stow` は展開先の指定（`-t`）で偽の HOME に展開できる。展開から `unlink` までの往復も試験できる（確認: 2026-10-05、根拠: `30_link.sh` の `link` → `unlink` を偽の HOME で通した）。
- 【汎用】`git clone --bare <ローカルのリポジトリ>` で、試験用のリモートを作れる。`/mnt/c` 上のリポジトリでも、所有者の警告（dubious ownership）は出なかった（確認: 2026-10-05、根拠: 実行した。WSL2 Ubuntu 24.04）。
- 【汎用】結果を PASS / FAIL で数える小さな `check` 関数（条件式を `eval` して判定）と、失敗数を終了コードにする末尾で、1ファイルの試験スクリプトにできる（確認: 2026-10-05、根拠: 35項目を1つのスクリプトで実行した）。
- 【汎用】WSL の `~/.profile` などが、stow で dotfiles リポジトリへの symlink になっていると、リポジトリ内の編集は、試験の前から実環境に効く（新しいログインシェルから）。初期化ファイルを直すときは、先に構文を確認する（確認: 2026-10-05、根拠: `ls -l ~/.profile` が dotfiles への symlink だった）。
- 【汎用】存在しないファイルを `source` すると、`set -e` の非対話の bash スクリプトは終了する（仮説: bash の仕様から。試験では偽の HOME に空の `.profile` を最初から置いたので、実際には遭遇していない）。
- 【この件】試験は35項目で、観点は次のとおり: 構文4、`.profile` の `NOTES_DIR` の分岐4（WSL / ネイティブ / 明示 / export）、`notes_dir` 4、clone 4、`.obsidian` のリンク9、`30_link.sh` の通し5、`50_repos.sh` 5。すべて合格し、実環境の `~` は変更していない（確認: 2026-10-05、根拠: 試験スクリプトの出力が `failures=0`）。
- 【この件】試験のために、`is_wsl()` と `home/.profile` に、環境変数 `PROC_VERSION_FILE`（`/proc/version` の差し替え）を足した。未設定なら本番の挙動は変わらない（確認: 2026-10-05、根拠: 実機の WSL で、未設定のまま `notes_dir` が WSL の値になった）。
- 【この件】ネイティブ Linux の実機は未確認。ネイティブの分岐は、差し替えで再現しただけ（仮説: 実機でも同じ結果になる）。

## Gotchas
- 状況: PowerShell ツール経由で、シェルの断片（`rm -- "$x"`）や `rmdir /s /q`、`robocopy /E` を含むコマンドを実行しようとしたとき、実行が拒否された
  - 原因: コマンド文字列中の `rm` や `/s` `/E` を、PowerShell の削除コマンドとその引数と誤認する安全チェックが働いた（複数回、2026-10-05 に遭遇）
  - 解決: スクリプトの本文は、ファイル書き込みのツールで直接書く。削除は、パスを固定して `Remove-Item -LiteralPath` で行い、コマンドを分けて実行する

## Open Questions
- 試験スクリプトは、試験後に削除して保存していない。再利用できる形（例: dotfiles の `tests/` に置く）にするか。
- 提案: 試験スクリプトを dotfiles に置く（AI の提案。未承認）。理由は、35項目の観点が、リンク配置スクリプトの変更のたびに使えるため。
- 差し替え用の環境変数（`PROC_VERSION_FILE`）を、本番のコード（`is_wsl` と `.profile`）に残すか、試験用の包みスクリプトで差し替えるか。
- 統合時の修正: knowledge/pc-setup-manuals.md の「`lib.sh` の関数4つ（`dots_dir` / `is_wsl` / `distro_is` / `read_list`）」の記述は、現在は7つ（`notes_dir` / `clone_workbase` / `link_obsidian` が増えた）。

## Next Actions
- ネイティブ Linux の実機で、`30_link.sh -n` → `link` → `unlink`、`50_repos.sh` を通して確認する。
- 試験スクリプトの置き場を決める。
