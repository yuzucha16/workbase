---
type: knowledge
title: Git の改行コードを .gitattributes で決める
status: active
tags:
  - tool/git
  - line-endings
  - windows
  - dotfiles
  - setup
aliases:
  - 改行コード
  - gitattributes
  - autocrlf
created: 2026-10-06
updated: 2026-10-08
sources:
  - Claude Code conversation ".gitattributes を足したあとに index の CRLF が残る落とし穴" (2026-10-07)
  - Claude Code conversation "clone 直後の大量差分と改行コード" (2026-10-06)
  - "git config の実物（2026-10-06 に確認）"
---

# Git の改行コードを .gitattributes で決める

## Purpose

Windows で clone した直後に、64ファイル・約8,000行の改行だけの差分が出た件から、再発しない設定の決め方を残す。Obsidian Vault 側の LF 統一は [[obsidian-vault]]、設定ファイルの置き場の判断は [[app-config-placement]]。

## Principles

- 改行コードの規則は、マシンごとの git 設定（`core.autocrlf`）でなく、リポジトリ内の `.gitattributes` で決める。理由: `.gitattributes` はコミットされて clone した全員に効き、`.gitconfig` より優先されるので、PC の設定状態に結果が左右されない。
- 大量の差分が出たら、まず `git diff --ignore-cr-at-eol --stat` で改行以外の実質差分を切り分ける。理由: 改行だけの差分に、アプリが書き換えた本物の変更が埋もれる。
- `.gitattributes` を足したあとは、正規化した拡張子だけでなく、`git ls-files --eol` で `i/crlf` が残る全ファイルを確認する。理由: 正規化の対象を一部の拡張子に絞ると、それ以外の index が CRLF のまま残り、アプリが LF で保存し直した時点で全行が差分になる。
- 改行だけの変更と内容の変更は、別のコミットに分ける。理由: 改行だけのコミットは行数が多く、中身のレビューを埋もれさせる。`git diff --ignore-space-at-eol` で、実質の差分が小さいことを確認してから分ける。
- Windows 向けの形式のファイル（`.bat` `.cmd` `.reg` `.ahk`）は、作業ツリーを CRLF、index を LF にする（`text eol=crlf`）。理由: Windows の標準に合わせつつ、git の設定（`autocrlf` など）に結果が左右されない。

## Decisions

### `.gitattributes` を `* text=auto eol=lf`、`*.bat` と `*.cmd` は `text eol=crlf` にする（2026-10-06）

- 根拠: 既定を LF にそろえ、Windows のバッチだけ作業ツリーを CRLF にできる。`.bat` は既存8本のうち5本が CRLF（index）で多数派だった。
- 却下案: 全ファイル CRLF に統一する（WSL/Linux のスクリプトと AI の出力が LF のため）。`.gitignore` や `.gitconfig` の変更だけで済ませる（追跡済みファイルの改行や clone 先 PC の設定には効かないため）。

### `.bat` の index を LF に正規化し、改行だけのコミットにする（2026-10-06）

- 根拠: `text eol=crlf` の正規形は「index が LF、作業ツリーが CRLF」。index が CRLF のままだと、次の編集で全行が差分に見える。
- 却下案: 正規化せず放置する（動作には影響しないが、`git ls-files --eol` に `i/crlf` が残る）。

### `.ps1` は LF のままにする（2026-10-06）

- 根拠: 追跡している `.ps1`（1本）の index がもともと LF で、pwsh は LF でも動く。差分を出さない。
- 却下案: `*.ps1` を CRLF にする（変更する理由が無い。Windows PowerShell 5.1 で日本語を含む場合の文字コードは未確認）。

### 改行以外に実質差分があった4ファイルは、内容も破棄して `git restore .` で取り直す（2026-10-06）

- 根拠: 4ファイルのうち設定ファイルの差分は、アプリが書き換えた値か、別の場所へ移した設定だった。この作業の範囲は改行コードだけにした（ユーザーの指示）。
- 却下案: 4ファイルだけ退避して残す。

### `.reg` と `.ahk` に `text eol=crlf` を指定し、index を LF に再正規化した（2026-10-07）

- 根拠: `.bat` と同じ理由（Windows 向けの形式で、作業ツリーは CRLF が無難。index を LF にそろえると git の設定に左右されない）。ユーザーが、この案で進めると指示した。現在の dotfiles の `.gitattributes` は `* text=auto eol=lf` と、`*.bat` `*.cmd` `*.reg` `*.ahk` の `text eol=crlf`（確認: 2026-10-08）。
- 却下案: 全部 LF（`.reg` は Windows 標準の形式から外れる。`.ahk` は v1 や行継続の挙動への影響を未確認で、リスクが大きい）。

## Facts

- 設定ファイル 1 本（Windows Terminal の `settings.json`）だけ、index が CRLF で作業ツリーが LF だった。`git ls-files --eol` は `i/crlf w/lf attr/text=auto eol=lf`（確認: 2026-10-07、根拠: `git ls-files --eol`）。2026-10-08 の dotfiles では、`i/crlf` が残るのは 5 本だけで、この `settings.json` は含まれない。
- 同じファイルの差分は約200行だったが、`git diff --ignore-space-at-eol` では10行だった（確認: 2026-10-07、根拠: `git diff --stat` と `--ignore-space-at-eol --stat` の比較）。
- `git add --renormalize <パス>` で、index が LF になった（確認: 2026-10-07、根拠: 実行後の `git ls-files --eol` が `i/lf w/lf`）。
- `.reg` の 2 本は先頭が `Wind`（`Windows Registry Editor` の ASCII）で、BOM も UTF-16 でもなかった。`.ahk` も BOM なし（確認: 2026-10-07、根拠: `ReadAllBytes` の先頭4バイト）。UTF-16 の `.reg` なら git が `text` として扱わない可能性がある（仮説）。
- `-text` を付けたファイル（`.exportedUI` 4本）は、index が CRLF のままでも意図的な指定として残る（確認: 2026-10-07、根拠: `git ls-files --eol` が `attr/-text`。2026-10-08 にも同じ 4 本）。
- 追跡対象の XML（Notepad++ のテーマ 1 本、`windows/notepadpp/Gruvbox dark medium.xml`）は index も作業ツリーも CRLF（`attr/text=auto eol=lf`）で、LF にそろえるかは未決。Notepad++ が保存時に CRLF へ書き直すかを確認していない（仮説。2026-10-08 にも `i/crlf w/crlf`）。
- clone 直後は、index が LF、作業ツリーが CRLF だった（確認: 2026-10-06、根拠: `git ls-files --eol` が `i/lf w/crlf`）。
- 有効な設定は `core.autocrlf=false`（ユーザー設定）と `core.eol=lf`。システムの gitconfig（scoop 版 git 2.56.0）は `core.autocrlf=true`（確認: 2026-10-06、根拠: 整理時に `git config --show-origin --get-all core.autocrlf` を再実行し、システム側 `true`・ユーザー側 `false` を確認）。
- clone 時に `autocrlf=true` が効いて CRLF でチェックアウトされ、その後ユーザー設定の `false` が有効になった、という順序は推定（仮説）。
- `--ignore-cr-at-eol` を付けると、64ファイルの差分が実質4ファイルに減った（確認: 2026-10-06、根拠: `git diff --ignore-cr-at-eol --stat`）。
- `text eol=crlf` のファイルは、index が LF で作業ツリーが CRLF でも `git status` に出ない。index が CRLF のファイルは `git add --renormalize <パス>` で LF になる（確認: 2026-10-06、根拠: 再正規化のコミット後、全8本が `i/lf w/crlf attr/text eol=crlf`）。
- `.gitattributes` を足したあとの `git restore .` は、`.gitattributes` に従って作業ツリーを取り直す（確認: 2026-10-06、根拠: `git status` がクリーン、`.bat` は `w/crlf`、それ以外は `w/lf`）。

## Gotchas

- **clone 直後に `git status` へ数十ファイルが変更として並んだ。** 原因は、clone 時のシステム設定 `core.autocrlf=true` による CRLF 変換と、その後の `autocrlf=false` の食い違い（順序は推定）。`.gitattributes` を追加してから `git restore .` で取り直した。
- **`*.bat text eol=crlf` を足したあと、index が LF の `.bat` を `git add --renormalize` しても何も変わらなかった（コミットが空）。** index が LF で作業ツリーが CRLF の状態は、すでに正規形なので変更が検出されない。正規化の対象は index が CRLF のファイルだけと確認してから実行する。
- **差分を破棄する前に、退避が必要な変更があるか確認したかった。** 改行だけの差分は `git diff` の既定表示では実質差分と区別できない。`git diff --ignore-cr-at-eol --stat` で絞り、残った4ファイルを退避してから破棄した。

- **改行だけのコミットと内容のコミットに分けようと、先に index を LF にし、`git commit -m ... -- <パス>` でコミットしたら、2つの変更が1コミットにまとまった**: パスを指定した `git commit` は、index ではなく作業ツリーの現在の内容をコミットする。`git reset --soft HEAD~1` で戻し（未 push のコミットだけ）、`git hash-object -w --no-filters` で LF の blob を作り、`git update-index --cacheinfo` で index に直接入れ、パスを指定せずに `git commit` した。次に作業ツリーを `git add` して、内容のコミットを作った。
- **Windows の PowerShell 5.x / 7 で `Add-Content` により `.gitattributes` に2行を追記したら、LF 管理のファイルに CR が1つ混ざった**: `Add-Content` は行末に CRLF を付ける。`ReadAllText` / `WriteAllText`（BOM なしの UTF-8）で、`` `r`n `` を `` `n `` に置換して書き直した。追記のあとは、CR の個数（バイト 13 の数）を数えて確認する。

## Open Questions

- 解決（2026-10-07 の統合）: 既存の本ノートは `.bat` までの指定だった。`.reg` と `.ahk` への拡張と、「index が CRLF のまま残るファイルを `git ls-files --eol` で全件探す」手順を、上に足した。

- Windows PowerShell 5.1 で、日本語を含む `.ps1` を LF で読ませる場合の文字コードの扱いは、確認していない。
- 提案（AI の提案。未承認）: 新しい PC を clone する前に、ユーザー用の git 設定（`autocrlf=false`）を先に有効にする手順を、セットアップ手順書（[[pc-setup-manuals]]）に書く。
- 他の PC で `git pull` したあと、`git ls-files --eol` に `i/crlf` が残っていないか。`.reg` `.ahk` と Terminal の `settings.json` の `git status` がクリーンか（未確認）。
- Notepad++ のテーマ XML を LF にそろえてよいか（上の Facts のとおり未確認）。

## Next Actions

- `git ls-files --eol` で `i/crlf` が残るファイルを洗い出し、`-text`（意図的）か、正規化の対象かを仕分ける。2026-10-08 に dotfiles で実施: 5 本のうち 4 本が `-text`（意図的）、1 本が Notepad++ の XML（未決）。他のリポジトリは未実施。

## Related

- [[obsidian-vault]]
- [[app-config-placement]]
- [[pc-setup-manuals]]
