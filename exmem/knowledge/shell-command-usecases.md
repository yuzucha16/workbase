---
type: knowledge
title: ターミナルのコマンド利用傾向とヒストリの種
status: active
tags:
  - dotfiles
  - setup
  - cli
  - tool/powershell
  - keymap
aliases:
  - コマンドヒストリの種
  - シェル履歴のユースケース
  - history seed
created: 2026-10-04
updated: 2026-10-05
sources:
  - PSReadLine の履歴 2か所の分析（このPC 629行、他PC 5,436行。2026-10-04）
---

# ターミナルのコマンド利用傾向とヒストリの種

## Purpose

PC を移行するたびに、定型処理のコマンドを調べ直す時間がかかる。実際に使ってきたコマンドから傾向とユースケースを整理し、移行先で最初から履歴検索（`↑`・`Ctrl+R`・ListView）に出る「種」を用意する。チートシートを見る機会を減らすのが目的。

## Principles

- **正本はこのノート。** 下の「履歴の種」のコードブロックが元で、dotfiles の種ファイルはここから機械的に作る（案a。生成手順は「種ファイルの作り方」）。
- **種は生の履歴を載せない。** 手で選んだ行だけを、個人・機密・案件固有の値を `<…名>` に置き換えて載せる。ユーザー名、メール、リポジトリ名、タグ名、パス、URL、ID、環境変数の値が対象。
- **プレースホルダーは `<xxx名>`（山かっこ）で、空白で区切られた語の先頭に置く。** PowerShell では、`<` で始まる語があるとパースエラーになり、候補を確定してそのまま Enter を押しても実行されない。bash/zsh でもリダイレクトの構文エラーかファイルなしで止まる。`"<xxx名>"`（引用符の中）や `origin/<xxx名>`（語の途中）はパースエラーにならず実行されるので、引用符なし・語の先頭にする（`git commit -m <メッセージ>`、`<リモート名>/<ブランチ名>`）。`[xxx名]`（角かっこ）も実行されるので使わない（2026-10-04 に実機でパーサーを使って確認）。
- **プレースホルダーが無い行は、そのまま実行して安全なものだけを載せる**（`git status`、`scoop list` など）。破壊的な行（`git reset --hard`、`git tag -d`、`wsl --unregister`、`scoop uninstall`）は必ずプレースホルダーを含める。
- **エイリアスやキーバインドを増やす基準**（後述）。履歴検索で呼べるものは増やさない。

## 傾向（2026-10-04 時点）

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

## 履歴の種

コードブロックは種ファイルへそのまま写す。`#` で始まる説明行は種ファイルに含めない（コードブロックの外に書く）。順序は上から古い履歴の扱い。

### 1. 環境・初回セットアップ

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Get-ExecutionPolicy -List
wsl --status
wsl --update
wsl --list --online
wsl --list --verbose
wsl --install -d <ディストロ名>
wsl --set-default <ディストロ名>
wsl --unregister <ディストロ名>
wsl --shutdown
ghq root
ghq get <owner名>/<repo名>
git config --global ghq.root <パス>
git config --global user.name <ユーザー名>
git config --global user.email <メールアドレス>
git config --global core.autocrlf <値>
git config --global core.symlinks
git config --list
git submodule sync
git submodule update --init --recursive
winget search <名前>
winget install --id <ID> -e
winget list
winget uninstall --id <ID>
uv tool install <ツール名>
uv tool update-shell
uv python install <バージョン>
uv python list
uv python pin <バージョン>
gh release download -R <owner名>/<repo名> -p "<ファイルパターン>" -D "$HOME\Downloads"
setx <変数名> "<値>"
code --list-extensions > extensions.txt
Get-Content .\extensions.txt | ForEach-Object { code --install-extension $_ }
```

- `wsl --install` の打ち間違い（`wsl install`）が履歴にあった。`wsl --install -d <ディストロ名>` が正しい。ディストロ名は `wsl --list --online` で確認する。
- `git config --global core.symlinks` は値を指定せず、設定を読むだけの形（Windows でシンボリックリンクを使えるかの確認）。

### 2. パッケージの調査と導入

```powershell
scoop bucket add extras
scoop search <名前>
scoop info <名前>
scoop install <名前>
scoop uninstall <名前>
scoop list
scoop list | Select-String <パターン>
scoop update *
scoop update <名前>
scoop cleanup *
cargo install <クレート名>
cargo install --locked <クレート名>
rustup update
which <コマンド>
where <コマンド>
<コマンド> --version
```

- 傾向: `search` → `install` → 使ってみて `uninstall`、の試行錯誤が多い。履歴には成功と失敗が混ざる（PSReadLine は終了コードを記録しない）ので、`install` が多いことは「定番」を意味しない。
- `rye`（他PC）は、このPCでは `uv` に置き換わったので種に載せない。`rye sync` / `rye run` は `uv sync` / `uv run` に当たる（このPCの履歴にあるのは `uv run python --version` だけで、未検証）。
- Windows の PowerShell で `which` を使うには、`scoop` の `which` が入っている前提（`apps.txt` に `which` がある）。

### 3. git の日常とリリース

```powershell
git status
git fetch
git pull
git pull origin main
git branch
git branch -a
git branch -r
git branch -a --no-merged
git checkout main
git switch main
git switch -c <ブランチ名>
git push origin main
git push origin <ブランチ名>
git push --tag
git push origin main --tag
git push -d origin <tag名>
git tag
git tag -a <tag名> -m "<メッセージ>"
git tag -d <tag名>
git rebase main
git rebase main <ブランチ名>
git rebase <ブランチ名>
git rebase --continue
git rebase --abort
git rebase -i main
git merge <ブランチ名>
git merge --squash <ブランチ名>
git merge --abort
git branch -d <ブランチ名>
git branch -D <ブランチ名>
git log --oneline --graph
git add .
git commit -m <メッセージ>
git reset --hard <リモート名>/<ブランチ名>
git switch -C main origin/main
git gc --prune=now
git archive --format=zip <tag名> <パス> -o <出力ファイル名>.zip
```

- タグの運用（他PCで多い）: `git tag -a <tag名> -m "<メッセージ>"` → `git push --tag`。作り直すときは `git tag -d <tag名>` と `git push -d origin <tag名>` の両方が要る。
- `git push --tag` は `--tags` の短縮（git が前方一致で受け付ける）。
- `git archive --format=zip <tag名> <パス> -o <出力>` は、タグ時点の一部のファイルだけを zip にする使い方。作業ツリーの状態ではなく、タグのコミットの中身が入る。
- **rebase の向き（忘れやすい）。** 引数は「土台（付け替え先）」で、動くのは今いるブランチ。
  - topic ブランチにいて `git rebase main` → topic のコミットを、main の先端の後ろに付け替える。main は動かない。
  - `git rebase main <ブランチ名>` は、`git switch <ブランチ名>` してから `git rebase main` するのと同じ（履歴にある `git rebase main topic_297` の形）。
  - 付け替えたあと main へ取り込むときは、main に戻って `git merge <ブランチ名>`（main は先に進んでいないので、履歴が一直線のままになる）。
  - 途中でコンフリクトしたら、直して `git add` → `git rebase --continue`。やめるなら `git rebase --abort`。`git rebase -i main` は、main から分かれた後のコミットを対話的に整理する。
- **`git merge --squash <ブランチ名>` は main（取り込む側）で実行する。** topic の変更を1つにまとめてステージするだけで、コミットは作られず、マージとしても記録されない。続けて `git commit -m ...` が要る。topic は「マージ済み」と見なされないので、消すときは `git branch -d` ではなく `git branch -D`（`git branch -a --no-merged` にも出続ける）。通常の `git merge` のあとなら `-d` で消せる。

### 4. 設定の編集と再読み込み

```powershell
notepad $PROFILE.CurrentUserAllHosts
. $PROFILE.CurrentUserAllHosts
Get-PSReadLineOption
Get-PSReadLineOption | Select-Object EditMode, PredictionSource, PredictionViewStyle
(Get-PSReadLineOption).HistorySavePath
vim ~/.vimrc
```

- 元の履歴は `notepad $PROFILE` と `. $PROFILE.CurrentUserCurrentHost` だった。いまの構成では `Microsoft.PowerShell_profile.ps1` を廃止して `profile.ps1`（全ホスト共通）だけにしたので、`CurrentUserAllHosts` に直した。`$PROFILE` は `CurrentUserCurrentHost`（存在しないファイル）を指す。

## 履歴の種（zsh/bash・素案）

Windows の種を zsh/bash 向けに置き換えた素案（2026-10-04、試験用）。コードブロックは `bash`（Windows 側の `powershell` ブロックとは別扱い）。履歴ファイルは zsh・bash とも1行1コマンドの平文でよい（zsh は拡張形式でなくても読める。実機で `fc -R` / `history -r` に読み込めることを確認）。

置き換えの判定（Windows → zsh/bash）:

| Windows の行 | 判定 | zsh/bash |
|---|---|---|
| `wsl ...`、`Set-ExecutionPolicy` / `Get-ExecutionPolicy` | 削除 | 対応するものが無い（`wsl` は Windows 側のコマンド） |
| `winget ...`、`scoop ...` | 置換 | `apt`（`manifests/apt.txt` と `20_packages.sh` が apt）。`scoop bucket add` は対応無しで削除、`winget list` は `apt list --installed` と重なるので削除 |
| `where <コマンド>` | 置換 | `type -a <コマンド>` |
| `setx <変数名> "<値>"` | 削除 | Linux では `~/.config/profile.local` に書く運用で、1行では表せない |
| `Get-Content ... ForEach-Object { code --install-extension $_ }` | 置換 | `xargs -n 1 code --install-extension < extensions.txt` |
| `gh release download ... -D "$HOME\Downloads"` | 置換 | `-D ~/download`（`24_fonts.sh` と同じ置き場） |
| `notepad $PROFILE...`、`. $PROFILE...` | 置換 | `vim ~/.zshrc` / `vim ~/.bashrc` / `vim ~/.config/shell/common.sh`、`source ~/.zshrc` / `source ~/.bashrc` |
| `Get-PSReadLineOption` 系 | 削除（`HistorySavePath` だけ置換） | `echo $HISTFILE` |
| `git ...`、`uv ...`、`cargo ...`、`rustup ...`、`ghq ...`、`code --list-extensions`、`which`、`vim ~/.vimrc` | 流用 | そのまま |

- 置換した apt の行や `vim ~/.zshrc` は、Windows の行を機械的に置き換えたもので、実際の履歴にあった行ではない（このPCの WSL 履歴にあるのは `sudo apt install zsh` と `source ~/.zshrc` のみ）。
- プレースホルダーは Windows 側と同じ規則（引用符なし・語の先頭）。bash/zsh では、先頭の `<…>` が入力リダイレクトとして失敗して、コマンド本体が実行されない。

### 1. 環境・初回セットアップ（zsh/bash）

```bash
ghq root
ghq get <owner名>/<repo名>
git config --global ghq.root <パス>
git config --global user.name <ユーザー名>
git config --global user.email <メールアドレス>
git config --global core.autocrlf <値>
git config --global core.symlinks
git config --list
git submodule sync
git submodule update --init --recursive
uv tool install <ツール名>
uv tool update-shell
uv python install <バージョン>
uv python list
uv python pin <バージョン>
gh release download -R <owner名>/<repo名> -p "<ファイルパターン>" -D ~/download
code --list-extensions > extensions.txt
xargs -n 1 code --install-extension < extensions.txt
```

### 2. パッケージの調査と導入（zsh/bash）

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
apt search <名前>
apt show <名前>
sudo apt install <パッケージ名>
sudo apt remove <パッケージ名>
apt list --installed
apt list --installed | grep <パターン>
cargo install <クレート名>
cargo install --locked <クレート名>
rustup update
type -a <コマンド>
which <コマンド>
<コマンド> --version
```

### 3. git の日常とリリース（zsh/bash）

Windows 側の 3 と同一（コマンド仕様が同じなので流用）。

```bash
git status
git fetch
git pull
git pull origin main
git branch
git branch -a
git branch -r
git branch -a --no-merged
git checkout main
git switch main
git switch -c <ブランチ名>
git push origin main
git push origin <ブランチ名>
git push --tag
git push origin main --tag
git push -d origin <tag名>
git tag
git tag -a <tag名> -m "<メッセージ>"
git tag -d <tag名>
git rebase main
git rebase main <ブランチ名>
git rebase <ブランチ名>
git rebase --continue
git rebase --abort
git rebase -i main
git merge <ブランチ名>
git merge --squash <ブランチ名>
git merge --abort
git branch -d <ブランチ名>
git branch -D <ブランチ名>
git log --oneline --graph
git add .
git commit -m <メッセージ>
git reset --hard <リモート名>/<ブランチ名>
git switch -C main origin/main
git gc --prune=now
git archive --format=zip <tag名> <パス> -o <出力ファイル名>.zip
```

### 4. 設定の編集と再読み込み（zsh/bash）

```bash
vim ~/.zshrc
vim ~/.bashrc
vim ~/.config/shell/common.sh
source ~/.zshrc
source ~/.bashrc
echo $HISTFILE
vim ~/.vimrc
```

- 検証（2026-10-04）: プレースホルダーを含む34行を、スタブコマンドを置いた空のディレクトリで bash と zsh の両方で実行した。コマンド本体は0回しか実行されず、余計なファイルも作られなかった。`xargs ... < extensions.txt` は `extensions.txt` があれば実際にインストールする（意図どおり）。

## エイリアス・キーバインド化の考え方

次の順に判断する。

1. **2〜3文字の前方一致で、履歴検索から呼べるか。** 呼べるなら何も足さない。種を入れることが、エイリアスを増やさない手段になる。
2. **固定の文字列で、頻度が高く、前方一致では区別しにくいか。** エイリアスの候補。
3. **変わる部分（タグ名、版数、日付）があるか。** エイリアスではなく、引数を取る関数か `<…名>` 入りのひな形にする。
4. **「選ぶ」操作か。** キーバインド（`Alt+j` の `zfz`、`Alt+k` の `cdg` など。空きキーは dotfiles リポジトリの `docs/decisions.md` の Facts）。固定コマンドの実行には使わない。

制約:
- 追加するものは `profile.ps1` と `common.sh` の両方に要る（3シェルの同期義務。dotfiles リポジトリの `docs/decisions.md`）。「基本エイリアスのみ」「標準コマンドの置換エイリアスは追加しない」の方針があるので、数は絞る。
- `sl`（`scoop list` の短縮）は PowerShell の `Set-Location` と衝突するので使えない。
- 頻度の数字には限界がある。PSReadLine の履歴にはタイムスタンプも終了コードも無いため、「同じ日に連続した試行錯誤」と「毎日使う定型」を区別できない。

現時点の判断（2026-10-04）:

| 候補 | 判断 |
|---|---|
| `git checkout main`（91）、`git push --tag`（65） | 種を入れれば前方一致で足りる。エイリアスは作らない |
| `git tag -a`/`-d`、`git push -d` | ひな形（種）。関数化は使い方が固まってから |
| `vim ~/.vimrc`（99） | 他PCの旧構成の回数かもしれない。種を入れて数週間使ってから見る |
| `cd ../`（97）、`cd -`（28） | `..`・`b` が既にある |
| `cdg`、`zfz` | 関数はある。キーバインドは3シェル共通で割り当てる（dotfiles リポジトリの `docs/log.md` の Next Actions） |

## 種ファイルの作り方

- 種ファイル: dotfiles の `windows/powershell/history.seed.txt`（PSReadLine の履歴ファイルと同じ形式。1行1コマンド、LF）。
- 作り方: このノートの「履歴の種」にある ` ```powershell ` ブロックを、上から順に連結する。コードブロックの外の説明は含めない。
- 初回セットアップでの使い方: `scripts\windows\31_history_seed.bat [-n]`（層 30 の固有ツール枠。`30_link.bat` の後）。履歴ファイルが無い、または空のときだけコピーする。既存の履歴は上書きしない（`-n` は確認のみ）。新しい pwsh を開く前に実行する。シンボリックリンクにしない（PSReadLine が実行のたびに追記するので、作業ツリーが毎回汚れる）。
- zsh/bash の種: 「履歴の種（zsh/bash・素案）」の ` ```bash ` ブロックを同様に連結して、dotfiles の `manifests/history.seed.sh.txt` に置く。履歴ファイルは `~/.local/state/{zsh,bash}/history`（`XDG_STATE_HOME` があればその下。1行1コマンドの平文。zsh も読める）。
- zsh/bash の配置: `scripts/linux/31_history_seed.sh [-n]`（Windows の `31_history_seed.bat` と同じ番号・同じ方針）。zsh と bash の履歴を別々に見て、無い/空のものだけコピーする（権限は 600）。既存の履歴は上書きしない。最初のシェルを開く前に実行する。

## Gotchas

- **秘匿情報の検出漏れ。** 2026-10-04 に、他PCの履歴を `token`/`secret`/`password` などの語で検索して「秘匿情報なし」と報告したが誤りだった。Teams の Webhook URL（IDが URL に埋め込まれている）を含む行が約50行あった。語ではなく、URL 中の長いID（`/[0-9a-f-]{20,}`）や `webhook` でも検索する。生の履歴は `resources/_local/` に置いた（Git 対象外。2026-10-05 に `_local/` を廃止し、このファイルは削除した）。
- 他PCの生履歴には、会社のユーザー名（Windows のアカウント名）入りの絶対パスと、案件固有のリポジトリ名・タグ名がある。種には載せない。
- このPCの履歴には、`git config --global user.email "<実際のアドレス>"` の行がある。種ではプレースホルダーに置き換えた。
- PowerShell では `[xxx]` はプレースホルダーにならない（`Write-Output [tag]` は成功して出力する）。`<xxx>` も、引用符の中や語の途中だと実行される（最初の版の種に `git config --global user.email "<メールアドレス>"` などが6行あり、パーサーで検出して直した）。語の先頭に置く。

- 2026-10-04 に、`ListView`（予測表示）と fzf の履歴検索の食い違いを確認した: 同日の前半は fzf を移動用に限定していたが、後半で `Ctrl+R` / `Ctrl+T` に戻し、pwsh の `ListView` は残した（`profile.ps1` に `PredictionViewStyle ListView` がある）。キー割り当てと測定値は [[shell-fzf-keybindings]]。
- zsh の履歴サイズが `HISTSIZE` の既定（30）のままだと `fc -l` の件数が少なく見える（`zsh -f` で試験するときの罠。rc では 50000）。

## Open Questions

- 種の件数は多すぎないか。ListView は10件固定のはずなので、先頭数文字で絞れる行が多いほど使いやすい。数週間使ってから間引く。
- 種の間引き（後日）。zsh/bash の種（`manifests/history.seed.sh.txt`）は素案のまま運用に入れた。置換した `apt` や `vim ~/.zshrc` の行は、実際の履歴にあった行ではないので、使わないものを間引く。
- 新しいPC（または VM）での `31_history_seed.sh` の通し実行は未確認（このPCは既に履歴があるので、ドライランと、一時ディレクトリでのコピー・スキップ・空ファイル・不正引数のテストまで）。
- 履歴ファイルの場所は既定の `%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt` を前提にしている（このPCで一致を確認）。`Set-PSReadLineOption -HistorySavePath` で変えた環境では合わない。
- このPCの履歴の中で、2 のパッケージのうち実際に残っているもの（`scoop list` の結果）と、種の記述の食い違い。

## Related

- [[modern-cli-tools]] — CLI ツールの役割整理
- [[shell-fzf-keybindings]] — fzf とキー割り当て
- dotfiles リポジトリ（`docs/decisions.md`: シェル設定の根拠、fzf とキーバインドの現仕様。`docs/log.md`: 次にやること）。リンクではなく参照のみ
