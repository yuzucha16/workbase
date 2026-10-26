---
type: logbook
title: ターミナルのコマンド利用傾向（2026-10-04 時点の履歴の分析）
source: "[[shell-command-usecases]]"
created: 2026-10-26
updated: 2026-10-26
review_by: 2026-12-25
budget: 8KB
---

# ターミナルのコマンド利用傾向（2026-10-04 時点の履歴の分析）

## いま

元: [[shell-command-usecases]]。PSReadLine の履歴 2か所（このPC 629行、他PC 5,436行）を 2026-10-04 に分析した結果。履歴の種に何を載せるかを決めた根拠で、載せた結論は lesson の「履歴の種」にある。件数は 2026-10-04 時点の値で、更新していない。

- 履歴の主体は、環境の立ち上げ、パッケージの調査と導入、git のリリース作業、設定の編集。
- 載せなかったもの: ナビゲーション、案件固有のビルド、API 呼び出し（URL に秘匿情報）、ノイズ。

## 明細

### 2026-10-04 の分析

| # | ユースケース | 根拠（件数は履歴の行数） | 種に載せるか |
|---|---|---|---|
| 1 | 新PC・環境の立ち上げ | このPCの履歴の主体。`wsl --install/--unregister/--shutdown`、`ghq get`、`uv tool install/update-shell`、`git config --global ...` | 載せる |
| 2 | パッケージの調査と導入 | `scoop` は install 168、search 119、uninstall 97、list 73。`cargo install`、`winget` | 載せる |
| 3 | git のリリース作業 | `git checkout main` 91、`git push --tag` 65、`git tag -a/-d`、`rebase` 37、`merge --squash`、`archive` | 載せる |
| 4 | 設定の編集と再読み込み | `vim ~/.vimrc` 99、`$PROFILE` の編集と `. $PROFILE`、PSReadLine の設定確認 | 載せる |
| 5 | ナビゲーション | `cd ../` 97、`cd -` 28、`cdg`/`zfz`/`z` | 載せない（`..`・`b`・`zoxide` に任せる） |
| 6 | 案件固有のビルド・書き込み | 社内のリリーススクリプト（引数に日付や版数）、`gmake`、書き込みツール、`ctags`/`gtags` | 載せない（案件側の README やスクリプトへ） |
| 7 | API 呼び出し | `Invoke-WebRequest -Method POST ...`（複数行） | 載せない（URL に秘匿情報を含む） |
| 8 | コマンドの再確認 | `--help`、`Get-Command`、`Get-PSReadLineOption` など約120行 | 一部（4 に含む） |
| 9 | ノイズ | `ll` 294、`vim` 単独61、`wsl` 単独25、打ち間違い（`r`、`ie`、`cdr`、`cdz`） | 載せない |

- 他PCは開発用の履歴（約5,400行、重複を除くと約2,200行）。このPCは環境構築が中心（約630行）。このPCでは `rye` が `uv` に置き換わった。
- 同じ行が5回以上繰り返された行は、他PCで約2,700行（約半分）を占める。`ll` や案件固有のスクリプト行が多い。
