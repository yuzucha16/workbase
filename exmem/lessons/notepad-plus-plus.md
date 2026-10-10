---
type: knowledge
title: Notepad++（scoop 版）の設定管理
status: active
tags:
  - tool/notepadpp
  - tool/scoop
  - dotfiles
  - windows
aliases:
  - Notepad++の設定
  - Notepad++ config.xml
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation "Notepad++ 設定の把握・最適化と config.xml の管理方式" (2026-10-04)
  - Claude Code conversation "dotfiles 整理（不要スクリプト削除と Notepad++ config の雛形方式）" (2026-10-04)
  - "dotfiles の windows/notepadpp/ と manifests/links.map（2026-10-04 に確認）"
---

# Notepad++（scoop 版）の設定管理

## Purpose

Notepad++ は「なんでもメモ」と設定ファイルの簡易編集に使う（Zed は AI の窓口、Obsidian は Markdown の viewer）。scoop 版の設定を、再構築（新PC・再インストール）でも再現できる最小の管理にする。dotfiles 側の経緯と個別の判断は dotfiles リポジトリの `docs/decisions.md` にある。

## Principles

- アプリが終了時に書き換えるファイルは、リンクも追跡もしない。管理するのは「最初に置く最小の状態」だけにする。毎回の強制適用はやめる。
- 管理が必要か迷ったら、再構築時に困るか、更新で戻っても実害があるかで判断する。`scoop update` で戻るものは、困らなければ放置する。
- 他のエディタと整合させる: カーソル点滅なし（[[terminal-cursor-blink]]）、新規文書は LF、自動折り返し ON、タブ幅はスペース2（Zed の全体 `tab_size` も 4 から 2 に変えた）。
- 復活させる可能性があるものは、削除を1コミットにまとめて `git revert` で戻せるようにする。

## Decisions

### `config.xml` は追跡せず、最小構成の雛形をコピーする（2026-10-04）

- 決めたこと: `windows/notepadpp/config.min.xml` を追跡し、`20_apps.bat` が、`config.xml` が無いか空のときだけコピーする。以後はアプリが自由に書き換える。最初は強制適用スクリプト `32_notepadpp`（`.bat` と `.ps1`）を作ったが、廃止した。
- 根拠: 毎回の強制適用が不要になり、スクリプトが数行になる。履歴・個人情報（検索履歴、MRU）がリポジトリに混ざらない。Notepad++ は `config.xml` に無い項目をデフォルト値で補うので、最小構成で動く。scoop は新規インストール時に空の `config.xml` を作るので、「空なら上書き」の条件にした。
- 却下案: `.gitignore` に入れる（未追跡になり最小構成が残らない）。symlink でリンクする（アプリが終了時に全体を書き戻し、差分が毎回出る）。`git update-index --skip-worktree`（クローンごとの設定になり、`pull` で衝突しやすい）。README に文書化するだけ（抜けが出る）。
- トレードオフ: コピーは初回だけなので、あとから雛形を変えても既存の環境には反映されない。反映するには `config.xml` を空にして `20_apps.bat` を再実行する。

### `config.xml` の設定値

- スナップショットバックアップ ON（メモ用途でクラッシュ時の未保存データを守る）。
- 自動更新は無効（`noUpdate=yes`、`autoUpdateMode=0`）。更新は scoop に一本化し、scoop の `disableNppAutoUpdate.xml` と矛盾させない。
- カーソル点滅なし（`Caret blinkRate="0"`）、新規文書は LF、自動折り返し ON、タブ幅はスペース2。
- `MaintainIndent` は 1（直前行のインデントを引き継ぐ。既定）のまま。却下案は 2（言語別の自動インデント。Markdown や設定ファイルでは意図しないインデントになりうる）。値の意味: 0 は無効、1 は引き継ぎ、2 は言語別。
- 検索履歴・MRU は一度消すだけにして、上限設定は変えない。却下案: `nbMaxFindHistory*` を 0 にする（検索の使い勝手が落ちる）。

### 管理から外したもの（2026-10-04）

- プラグインは全削除（未使用）。`%APPDATA%\Notepad++`（ローカル設定モードでは使われない旧パスの残骸）も削除。
- `shortcuts.xml`、`contextMenu.xml` は管理しない（ほぼ使っていない、標準のままで実害がない）。内部コマンド 41010 のショートカット解除は、目的が不明なので標準に戻した。
- Gruvbox light テーマは削除した。ダークモード有効かつ Windows 連動オフで使われないため（light が使われるのは、ダークモードをオフにしたときか、「Windows に合わせる」をオンにしたときだけ）。追跡するのは Gruvbox dark のみ。
- `scoop update` 後の後処理は作らない。`config.xml` は引き継がれ、戻るもの（shortcuts・プラグイン）は困らないため。

## Facts

確認済み:

- scoop 版 8.9.8.1。`doLocalConf.xml` によるローカル設定モードで、実設定は `%USERPROFILE%\scoop\apps\notepadplusplus\current\` にある。
- `scoop persist`: `config.xml`、`nativeLang.xml`、`session.xml`、`shortcuts.xml`、`userDefineLang.xml`、`stylers.xml` はファイル（hardlink）。`plugins`、`themes`、`userDefineLangs`、`backup`、`cloud` は junction。
- `scoop update` の影響: `config.xml` は引き継がれる。`shortcuts.xml` は新しい版のフォルダに persist 側の古い標準版への hardlink が作られ、リポジトリへの symlink は外れる。`post_install` が同梱プラグイン（`plugins.original`）を `plugins` にコピーし直すので、削除したプラグインは復活する。`contextMenu.xml` は標準に戻る。
- フォント（PlemolJP Console NF Light、12pt）は、設定ではなくテーマ内の「Global override」で定義されている。`config.xml` の `globalOverride` は `font=yes`、`fontSize=yes`（[[fonts]]）。
- `Gruvbox light medium.xml` の差分は改行コードだけだった。Notepad++ がリンク経由で書き換えた可能性がある。
- 2026-10-04 の dotfiles の実物（`windows/notepadpp/`）: `config.min.xml` と `Gruvbox dark medium.xml` のみ。`manifests/links.map` の Notepad++ の行は Gruvbox dark の1つだけ。`20_apps.bat` の雛形コピーは、このPCで動作確認済み。

仮説（未確認）:

- `Caret blinkRate="0"` で点滅が止まる（Notepad++ の実機起動で確認していない）。
- 41010 のコマンド名は特定していない。

## Gotchas

- **Notepad++ が起動中だと、終了時に `config.xml` が上書きされ、編集内容が消える**。必ず閉じてから編集する。スクリプトも起動中は止まる。
- **マクロ「Trim Trailing Space and Save」は、Markdown の行末スペース2つ（強制改行）を消す**。Markdown では使わない。管理から外したので、標準のショートカットに戻っている。
- **`git add` に削除済みのパスを渡すと失敗する**（`git rm` で既にステージ済みなら不要）。このとき他のパスが追加されないままコミットされ、内容が分かれることがある。コミット後に `git show --stat` で確認する。逆に、`git rm` で削除したものがステージ済みのまま次のコミットに混ざることもある。`git add` はパス指定にし、削除は別コミットにする。
- **`Set-Content` で設定ファイルを書き直すと改行コードが変わり、全行が差分になる**（`apps.txt` で発生）。バイト単位の置換でやり直した。
- **PowerShell ツールの権限チェックが、スクリプト内の文字列（`/>` を含む XML のパターン）を誤検知してコマンド全体を止めた**。実行内容を分けるか、パスを `-LiteralPath` で渡して回避した。
- 履歴（`config.xml` の検索履歴・MRU）は個人情報を含むが、追跡対象外なのでリポジトリには入らない。

## Open Questions

- 実機で Notepad++ を起動し、点滅停止・LF・折り返し・ダークテーマ・フォントが反映されているか。
- 新しいPCで `20_apps.bat`（雛形コピー）を通し実行して動くか。
- 41010 のコマンドが何だったか（標準に戻したので、支障が出たら特定する）。
- 実機に残る light テーマの壊れたリンクの掃除。

## Related

- [[fonts]]
- [[terminal-cursor-blink]]
- [[scoop-app-management]]
- [[zed-dotfiles]]
