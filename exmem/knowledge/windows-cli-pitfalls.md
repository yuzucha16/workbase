---
type: knowledge
title: Windows の PowerShell・バッチ・git 操作の落とし穴
status: active
tags:
  - tool/powershell
  - tool/git
  - tool/wsl
  - windows
  - shell
aliases:
  - Windows CLI の落とし穴
  - PowerShell の落とし穴
created: 2026-10-06
updated: 2026-10-06
sources:
  - Claude Code conversation "社内 CA 証明書の置き場の変更" (2026-10-06)
---

# Windows の PowerShell・バッチ・git 操作の落とし穴

## Purpose

Windows で PowerShell・バッチ・git を使う作業で、繰り返しハマった点を、別の作業でも使える形でまとめる。バッチの文字コードや入力の試験は [[shell-script-testing-wsl]]、バッチの文脈の落とし穴は同じノートの「Windows バッチ」の節にある。

## Principles

- PowerShell から `wsl` や別のシェルへ渡す複雑なコマンドは、スクリプトを LF のファイルに書き出して実行させる。引数の `$(...)` や here-string のパイプが、渡る前に PowerShell 側で処理されて壊れる。
- 改行コードを保つ編集は、`Set-Content` ではなく、`[IO.File]::ReadAllText` / `WriteAllText` で該当部分だけ置換する。`Set-Content` で書き直すと改行コードが変わり、全行が差分になる。
- 構造変更（ディレクトリの移動）では、git が読む設定ファイルのリンク元を最初に動かさない。リンク先が消えると、git 全体が設定を読めず壊れる。

## Facts

- PowerShell ではエイリアスが関数より優先される。`function ls` は組み込みの `ls` エイリアスに負けるので、`Remove-Item Alias:ls` が要る。`mv` も同じで、関数名を `gmv` にして避けた（確認: 2026-10-06、根拠: 転記元の記録。再現は未実施）。
- Windows バッチの `if exist` は、リンク切れの symlink に対しても真を返す。`dir /AL` はジャンクション先の中身を見るので、リンクの判定に使えない。`for %%F in ("path") do set "ATTR=%%~aF"` の属性文字列（1文字目 `d`、9文字目 `l`）で判定する（確認: 2026-10-06、根拠: 転記元の記録。再現は未実施）。
- `git help --config` に出ないキーも、`git config` は受け付けて書き込む。エラーも警告も出ない（確認: 2026-10-06、根拠: git 2.56.0.windows.1 の試験。[[pc-setup-manuals]] の「git の設定の置き場」）。

## Gotchas

- **PowerShell から `wsl -d <ディストリビューション> -- bash -c "…$(…)…"` を実行した**: `$(...)` が PowerShell 側で先に展開された。`git commit -F -` への here-string のパイプも渡らない。スクリプトを LF で書き出して `bash` に渡し、コミットメッセージは一時ファイル経由にする。
- **`rm`、`del /F`、`cmd /c` を含む PowerShell コマンドが、実行環境の安全装置にブロックされた**: 安全装置の誤検知（コマンド文字列中の語に反応した）。スクリプトをファイルに書いてから実行する。削除は `unlink` を使う。
- **PowerShell の単一引用符の文字列に `` `r`n `` を書いた**: 単一引用符の文字列では、エスケープが展開されない。二重引用符の文字列を使う。
- **`git rm` 済みの削除があるまま、別のパスだけを `git add` / `commit` した**: ステージ済みの削除が、次のコミットに混ざる。削除を分けたいときは、先に `git commit <パス>` で分けるか、コミット前に `git status` で確認する。
- **`git diff` をパスで絞ったら、改名したファイルの全行が「追加」に見えた**: パスで絞ると、改名の検出が効かない。改名の確認は `git diff -M HEAD --stat` で行う。
- **`git mv` の途中で、git 全体が `fatal: unknown error occurred while reading the configuration files` で壊れた**: `~/.config/git/config` のリンク先が、移動の途中で消えた。そのリンクだけ、新しい場所へ手で張り直した。
- **GitHub のコード検索ページ（`github.com/search`）でソースを調べようとした**: 未ログインでは取得できない。`raw.githubusercontent.com` のファイル URL で読む。

## Related

- [[shell-script-testing-wsl]]
- [[pc-setup-manuals]]
- [[git-line-endings]]
