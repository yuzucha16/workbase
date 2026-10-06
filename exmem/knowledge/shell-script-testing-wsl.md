---
type: knowledge
title: WSL でシェルスクリプトを試験する
status: active
tags:
  - tool/wsl
  - dotfiles
  - shell
  - testing
  - tool/stow
aliases:
  - シェルスクリプトの試験
  - 偽の HOME
  - 環境判定の差し替え
created: 2026-10-06
updated: 2026-10-06
sources:
  - Claude Code conversation "dotfiles の Linux 対応と WSL での試験" (2026-10-05)
  - "dotfiles の scripts/linux/lib.sh（2026-10-05 に確認）"
---

# WSL でシェルスクリプトを試験する

## Purpose

WSL とネイティブ Linux で分岐するシェルスクリプト（dotfiles の `30_link.sh`、`50_repos.sh` など）を、ネイティブ Linux の実機が無くても、実環境を壊さずに試験する方法。項目の頭の【汎用】は他のスクリプトにも使える内容、【この件】は dotfiles の Linux 対応（2026-10-05）に固有の内容。手順書側は [[pc-setup-manuals]]。

注: 以下の Facts は 2026-10-05 の作業時の確認で、2026-10-06 の統合時には dotfiles の実物が見つからず再確認していない。

## Principles

- 【汎用】環境の判定（WSL かネイティブか）は1つの関数にまとめ、差し替え用の環境変数（例: `/proc/version` の場所を指す変数）を用意する。理由: ネイティブ Linux の実機が無くても、WSL 上で両方の分岐を試験できる。
- 【汎用】試験は、一時ディレクトリ（`mktemp -d`）、偽の HOME、スクリプトの上書き用の指定（`--dst` や環境変数）に閉じ込め、実環境の `~` を変更しない。理由: 試験の失敗が普段使いの設定を壊さないようにする。
- 【汎用】外部コマンドと通信は偽物に差し替える。コマンド（例: `ghq`）は PATH の先頭に置いた偽の実行ファイルで、clone 元はローカルの bare リポジトリにする。理由: ネットワークや本物の副作用に依存せず、再現できる。
- 【汎用】リンクや clone を扱うスクリプトは、「新規作成」「再実行（冪等）」「dry-run は何も作らない」「元に戻す（unlink）」「実体が既にあれば止まって変更しない」「リンク切れの置き換え」「元が無ければ skip」を最低限の観点にする。理由: リンク配置の事故（上書き、消し過ぎ）の主な入口がこの7つ。
- 【汎用】差し替えた試験に加えて、本物の環境で動く確認を1項目は入れる。理由: 差し替えが本物と食い違うと、試験が通っても実機で動かない。

## Facts

- 【汎用】構文は `bash -n` で、`.profile` は `/bin/sh -n` で確認できる。Ubuntu 24.04 の `/bin/sh` は dash なので、POSIX の範囲で書けているかも分かる（確認: 2026-10-05、根拠: `readlink -f /bin/sh` が dash を指した）。
- 【汎用】Windows から WSL のスクリプトは `wsl -e bash /mnt/c/<パス>/test.sh` で実行できる。スクリプトは LF で書く（確認: 2026-10-05、根拠: 実行した。CRLF で失敗するかは未実施で、仮説。改行の規則は [[git-line-endings]]）。
- 【汎用】`stow` は展開先の指定（`-t`）で偽の HOME に展開できる。展開から `unlink` までの往復も試験できる（確認: 2026-10-05、根拠: `30_link.sh` の `link` → `unlink` を偽の HOME で通した）。
- 【汎用】`git clone --bare <ローカルのリポジトリ>` で、試験用のリモートを作れる。`/mnt/c` 上のリポジトリでも所有者の警告（dubious ownership）は出なかった（確認: 2026-10-05、根拠: 実行した。WSL2 Ubuntu 24.04）。
- 【汎用】結果を PASS / FAIL で数える小さな `check` 関数（条件式を `eval` して判定）と、失敗数を終了コードにする末尾で、1ファイルの試験スクリプトにできる（確認: 2026-10-05、根拠: 35項目を1つのスクリプトで実行した）。
- 【汎用】WSL の `~/.profile` などが stow で dotfiles リポジトリへの symlink になっていると、リポジトリ内の編集は、試験の前から実環境に効く（新しいログインシェルから）。初期化ファイルを直すときは、先に構文を確認する（確認: 2026-10-05、根拠: `ls -l ~/.profile` が dotfiles への symlink だった）。
- 【汎用】存在しないファイルを `source` すると、`set -e` の非対話の bash スクリプトは終了する（仮説: bash の仕様から。試験では偽の HOME に空の `.profile` を最初から置いたので、実際には遭遇していない）。
- 【この件】試験は35項目で、観点は次のとおり: 構文4、`.profile` の `NOTES_DIR` の分岐4（WSL / ネイティブ / 明示 / export）、`notes_dir` 4、clone 4、`.obsidian` のリンク9、`30_link.sh` の通し5、`50_repos.sh` 5。すべて合格し、実環境の `~` は変更していない（確認: 2026-10-05、根拠: 試験スクリプトの出力が `failures=0`）。
- 【この件】試験のために、`is_wsl()` と `home/.profile` に、環境変数 `PROC_VERSION_FILE`（`/proc/version` の差し替え）を足した。未設定なら本番の挙動は変わらない（確認: 2026-10-05、根拠: 実機の WSL で、未設定のまま `notes_dir` が WSL の値になった）。
- 【この件】ネイティブ Linux の実機は未確認。ネイティブの分岐は、差し替えで再現しただけ（仮説: 実機でも同じ結果になる）。

## Gotchas

- **PowerShell ツール経由で、シェルの断片（`rm -- "$x"`）や `rmdir /s /q`、`robocopy /E` を含むコマンドが拒否された**（2026-10-05 に複数回）。コマンド文字列中の `rm` や `/s` `/E` を、削除コマンドとその引数と誤認する安全チェックが働いた。スクリプトの本文はファイル書き込みのツールで直接書き、削除はパスを固定して `Remove-Item -LiteralPath` で、コマンドを分けて行う。

## Open Questions

- 試験スクリプトは、試験後に削除して保存していない。再利用できる形（例: dotfiles の `tests/`）にするか。AI の提案（未承認）は、35項目の観点がリンク配置スクリプトの変更のたびに使えるため置くこと。
- 差し替え用の環境変数（`PROC_VERSION_FILE`）を、本番のコード（`is_wsl` と `.profile`）に残すか、試験用の包みスクリプトで差し替えるか。
- ネイティブ Linux の実機で、`30_link.sh -n` → `link` → `unlink`、`50_repos.sh` を通して確認する（未実施）。

## Related

- [[pc-setup-manuals]]
- [[git-line-endings]]
- [[wsl-file-placement]]
