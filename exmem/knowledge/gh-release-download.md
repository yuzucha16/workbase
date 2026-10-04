---
type: knowledge
title: gh release download は未ログインでも使える
status: active
tags:
  - tool/gh
  - setup
  - font
aliases:
  - gh release download
  - gh未ログイン
  - GitHub Releasesの取得
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation "24_fonts スクリプトの簡素化と gh 未ログインの検証" (2026-10-04)
  - "dotfiles の scripts/{windows,linux}/24_fonts.*（2026-10-04 に確認）"
---

# gh release download は未ログインでも使える

## Purpose

GitHub の公開リリースの zip（フォントなど）を `gh release download` の数行で取得するスクリプトに、前提チェックや `--dry-run` が本当に必要かを、実機で確かめた結果。フォントの取得スクリプトは [[fonts]]。

## Principles

- 取得対象が公開リリースなら、`gh` のログインを前提にしない。ダウンロードは未ログインで通るので、ログイン確認を足すと通る操作を止めるだけになる。
- 前提チェックは、実機でその前提が必要だと確かめてから入れる。「認証が要るはず」という推測で入れた確認が、実際には不要で有害だった。
- 副作用が小さく中身が1行のコマンドのラッパーには、`--dry-run` を付けない。表示するコマンド自体が1行で、実行しても再実行できる（`--clobber`）ので、確認の価値より保守の手間が大きい。
- 動かして確かめていない挙動は、AI の説明でも断定しない。「未ログインだと失敗する」と断定した説明が誤りで、実機で覆った。

## Decisions

### 取得スクリプトから `gh auth status` の確認と `--dry-run` を削除し、`gh` の有無の確認だけ残す（2026-10-04）

- 根拠: 未ログインでも `gh release download` が成功した（Facts）。`--dry-run` は `gh` 1行の表示にすぎない。
- 却下案: `gh auth status` を残して案内だけ出す（通る操作を止める）。`curl` / `Invoke-WebRequest` に置き換える（アセット名にバージョンが入り、`*` の glob が使えない）。

## Facts

確認済み（2026-10-04、gh 2.102.0、Windows 11）:

- 空の `GH_CONFIG_DIR` を指定し、`GH_TOKEN` と `GITHUB_TOKEN` を未設定にして未ログインを再現した。`gh auth status` は「not logged into any GitHub hosts」と表示した。
- 未ログインで `gh release download -R yuru7/PlemolJP -p "PlemolJP_NF_v*.zip" -D <dir>` が成功し、約153MBの zip を取得した。`-R yuru7/moralerspace -p "MoralerspaceHW_v*.zip"` も成功し、約102MBを取得した（終了コード 0 と取得ファイルのサイズ）。
- 未ログインで `gh release list -R yuru7/PlemolJP -L 1` は失敗した。`gh auth login` を促すメッセージが出て、終了コードは 4。
- dotfiles の実物: `24_fonts.bat` と `24_fonts.sh` に `--dry-run` や `gh auth` の記述は無い（`dry` / `auth` の検索が0件）。

仮説（未確認）:

- 公開リポジトリでも、API を直接呼ぶコマンドは認証を要求する（`gh api` は未試験）。
- 未ログインのレート制限は、1回に2件程度のダウンロードなら問題にならない。

## Gotchas

- **`no assets match the file pattern`（終了コード 1）**: 存在しないパターン（`PlemolJP_console_v*.zip`）を指定した。認証の失敗ではない。実在するパターン（`PlemolJP_NF_v*.zip`）に直す。認証エラーとパターン不一致はメッセージで区別できる。
- **未ログインの挙動を、自分の環境で再現できない**: 手元の `gh` が既にログイン済みだと再現できない。`GH_CONFIG_DIR` を空のディレクトリにし、`GH_TOKEN` と `GITHUB_TOKEN` を未設定にして実行し、終わったらそのディレクトリを削除する。

## Open Questions

- 未ログインのレート制限は、どの程度の回数で効くか。
- `gh` の未ログインで使える操作と使えない操作の一覧（`release download` は可、`release list` は不可）を、どこまで広げて整理するか。
- リリースの一覧（`gh release view --json assets`）で、PlemolJP の Console NF に当たる実際のアセット名は何か。

## Related

- [[fonts]]
- [[pc-setup-manuals]]
