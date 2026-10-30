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
triggers: [コマンド履歴, ヒストリ, history, 利用傾向, シェル履歴, ターミナル, よく使うコマンド, エイリアス案, ヒストリの種]
created: 2026-10-04
updated: 2026-10-30
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

種に載せたのは、環境の立ち上げ、パッケージの調査と導入、git のリリース作業、設定の編集。載せなかったのは、ナビゲーション（`zoxide` に任せる）、案件固有のビルド、API 呼び出し（URL に秘匿情報）、ノイズ。件数つきの表は → [[shell-command-usecases-log]]（2026-10-26 に降格）。

## 履歴の種
<!-- 素材: 開始時に読まない / 確認: 2026-10-27 -->

コードブロックは種ファイルへそのまま写す。`#` で始まる説明行は種ファイルに含めない（コードブロックの外に書く）。

**追記のしかた（2026-10-11 に、使い方別からツール別に並べ替えた）。** ツールごとの節（`###`）をアルファベット順に並べ、節の中はサブコマンド順にしている。新しい行は、そのツールの節のサブコマンドの位置に足す。新しいツールは、節ごとアルファベット順の位置に足す。節に入らない cmdlet・環境変数・設定ファイルの編集は `PowerShell` に入れる。種ファイルは、上の節から順にブロックを連結して作る（履歴では、下の行ほど新しい扱いになり、`↑` で先に出る）。

- 2026-10-11 に、他PCの履歴（写真2枚）から、公式インストーラー、社内プロキシ配下の証明書まわり（`UV_SYSTEM_CERTS`、`http.sslBackend schannel`）、`aws`、`claude` を足した。載せなかったのは、`http.sslVerify false`（証明書検証の無効化）、ユーザー名入りのパス、社内の証明書パス、案件のディレクトリ、打ち間違い、`--version` 単独の行、`rnr regex ...`、`claude --teleport`（`uvx mcp-proxy-for-aws ...` は、いったん載せたが、使わないのでユーザーの指示で外した）。元の `set UV_SYSTEM_CERTS=true` は cmd の書き方で、PowerShell の `set` は `Set-Variable` のため環境変数にならない。`$env:` に直した。

### aws

```powershell
aws bedrock list-inference-profiles --region ap-northeast-1
aws configure
aws configure --profile <プロファイル名>
aws configure list-profiles
aws sts get-caller-identity
```

### cargo・rustup

```powershell
cargo install <クレート名>
cargo install --locked <クレート名>
rustup update
```

### claude

```powershell
claude
claude --help
claude --version
claude-api
claude-bedrock
claude-oauth
claude-pick
```

- `claude-api` / `claude-bedrock` / `claude-oauth` / `claude-pick` は、自作のランチャー（`profile.ps1` など。dotfiles の `windows/claude/`）。

### code

```powershell
code --list-extensions > extensions.txt
Get-Content .\extensions.txt | ForEach-Object { code --install-extension $_ }
```

### gh

```powershell
gh release download -R <owner名>/<repo名> -p "<ファイルパターン>" -D "$HOME\Downloads"
```

### ghq

```powershell
ghq get <owner名>/<repo名>
ghq root
```

### git

```powershell
git add .
git archive --format=zip <tag名> <パス> -o <出力ファイル名>.zip
git branch
git branch -a
git branch -r
git branch -a --no-merged
git branch -d <ブランチ名>
git branch -D <ブランチ名>
git checkout main
git clone <リポジトリURL> <クローン先パス>
git commit -m <メッセージ>
git config --global ghq.root <パス>
git config --global user.name <ユーザー名>
git config --global user.email <メールアドレス>
git config --global core.autocrlf <値>
git config --global core.symlinks
git config --global http.sslBackend schannel
git config --list
git config --show-origin --list
git config --show-origin --get-all credential.helper
git credential-manager version
git check-ignore -v <パス>
git diff --cached
git fetch
git fetch --prune
git gc --prune=now
git log --oneline --graph
git ls-files
git merge <ブランチ名>
git merge --squash <ブランチ名>
git merge --abort
git pull
git pull origin main
git pull --rebase
git push origin main
git push origin <ブランチ名>
git push --tag
git push origin main --tag
git push -d origin <tag名>
git rebase main
git rebase main <ブランチ名>
git rebase <ブランチ名>
git rebase --continue
git rebase --abort
git rebase -i main
git remote -v
git reset --hard <リモート名>/<ブランチ名>
git status
git status --short
git -C <リポジトリのパス> status --short
git -C <リポジトリのパス> log --oneline -10
git submodule sync
git submodule update --init --recursive
git switch main
git switch -c <ブランチ名>
git switch -C main origin/main
git tag
git tag -a <tag名> -m "<メッセージ>"
git tag -d <tag名>
```

- `git config --global core.symlinks` は値を指定せず、設定を読むだけの形（Windows でシンボリックリンクを使えるかの確認）。
- 注意（2026-10-06）: `user.name` / `user.email` を `--global` で書く行は、`~/.gitconfig` が設定リポジトリへの symlink のとき、リポジトリ内のファイルを書き換える（リンク前に使うと、実ファイルができてリンクが止まる）。PC ごとの値は `git config --file ~/.gitconfig_local` に書く（[[pc-setup-manuals]]）。履歴の種（`history.seed.txt` と `history.seed.sh.txt`）の同じ行は、未修正。
- タグの運用（他PCで多い）: `git tag -a <tag名> -m "<メッセージ>"` → `git push --tag`。作り直すときは `git tag -d <tag名>` と `git push -d origin <tag名>` の両方が要る。
- `git push --tag` は `--tags` の短縮（git が前方一致で受け付ける）。
- `git archive --format=zip <tag名> <パス> -o <出力>` は、タグ時点の一部のファイルだけを zip にする使い方。作業ツリーの状態ではなく、タグのコミットの中身が入る。
- **rebase の向き（忘れやすい）。** 引数は「土台（付け替え先）」で、動くのは今いるブランチ。
  - topic ブランチにいて `git rebase main` → topic のコミットを、main の先端の後ろに付け替える。main は動かない。
  - `git rebase main <ブランチ名>` は、`git switch <ブランチ名>` してから `git rebase main` するのと同じ（履歴にある `git rebase main topic_297` の形）。
  - 付け替えたあと main へ取り込むときは、main に戻って `git merge <ブランチ名>`（main は先に進んでいないので、履歴が一直線のままになる）。
  - 途中でコンフリクトしたら、直して `git add` → `git rebase --continue`。やめるなら `git rebase --abort`。`git rebase -i main` は、main から分かれた後のコミットを対話的に整理する。
- **`git merge --squash <ブランチ名>` は main（取り込む側）で実行する。** topic の変更を1つにまとめてステージするだけで、コミットは作られず、マージとしても記録されない。続けて `git commit -m ...` が要る。topic は「マージ済み」と見なされないので、消すときは `git branch -d` ではなく `git branch -D`（`git branch -a --no-merged` にも出続ける）。通常の `git merge` のあとなら `-d` で消せる。

### installer

```powershell
Invoke-RestMethod -Uri 'https://get.scoop.sh' | Invoke-Expression
irm https://astral.sh/uv/install.ps1 | iex
irm https://claude.ai/install.ps1 | iex
```

- 公式の配布元のインストーラー。プレースホルダーが無いので、選んで Enter を押すと、そのまま外部のスクリプトを実行する。

### PowerShell

```powershell
. $PROFILE.CurrentUserAllHosts
(Get-Command <コマンド>).Source
echo $env:<変数名>
(Get-PSReadLineOption).HistorySavePath
$env:UV_SYSTEM_CERTS = "true"
Get-ChildItem Env: | Where-Object Name -match 'AWS_'
Get-DnsClientCache | Where-Object Entry -match 'anthropic|bedrock|amazonaws'
Get-ExecutionPolicy -List
Get-Content (Get-PSReadLineOption).HistorySavePath
Get-Content (Get-PSReadLineOption).HistorySavePath | Select-String <パターン>
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
Get-PSReadLineOption
Get-PSReadLineOption | Select-Object EditMode, PredictionSource, PredictionViewStyle
Measure-Command { pwsh -Command "exit" }
Measure-Command { pwsh -NoProfile -Command "exit" }
notepad $PROFILE.CurrentUserAllHosts
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
setx <変数名> "<値>"
```

- 元の履歴は `notepad $PROFILE` と `. $PROFILE.CurrentUserCurrentHost` だった。いまの構成では `Microsoft.PowerShell_profile.ps1` を廃止して `profile.ps1`（全ホスト共通）だけにしたので、`CurrentUserAllHosts` に直した。`$PROFILE` は `CurrentUserCurrentHost`（存在しないファイル）を指す。
- `Measure-Command { pwsh -Command "exit" }` と `-NoProfile` 付きの差が、プロファイルの起動時間になる。

### scoop

```powershell
scoop bucket add extras
scoop cleanup *
scoop info <名前>
scoop install <名前>
scoop list
scoop list | Select-String <パターン>
scoop search <名前>
scoop uninstall <名前>
scoop update *
scoop update <名前>
```

- 傾向: `search` → `install` → 使ってみて `uninstall`、の試行錯誤が多い。履歴には成功と失敗が混ざる（PSReadLine は終了コードを記録しない）ので、`install` が多いことは「定番」を意味しない。

### uv

```powershell
uv init
uv pip list
uv pip install pandas
uv pip install django==4.2.0
uv pip install -r requirements.txt
uv python install <バージョン>
uv python install 3.13
uv python list
uv python pin <バージョン>
uv python pin 3.13
uv remove pandas
uv run python --version
uv run --script <スクリプトのパス>.py
uv sync
uv tool install <ツール名>
uv tool update-shell
uv venv <ディレクトリ名>
```

- `rye`（他PC）は、このPCでは `uv` に置き換わったので種に載せない。`rye sync` / `rye run` は `uv sync` / `uv run` に当たる（このPCの履歴にあるのは `uv run python --version` だけで、未検証）。

### vim

```powershell
vim ~/.vimrc
```

### volta

```powershell
volta install node
volta install node@latest
volta install node@22
volta install <パッケージ名>
volta list
volta pin node@22
volta pin npm@10
volta run <コマンド>
volta run node --version
volta uninstall <パッケージ名>
volta which <コマンド>
volta which npm
```

- 注意（2026-10-11）: `volta pin` で固定できるのは `node` / `npm` / `yarn` だけで、一般のパッケージは固定できない。`volta uninstall` が外すのはグローバルにインストールしたパッケージで、`node` 自体ではない（`node` は別の版を `volta install` して切り替える）。`node@<バージョン>` は語の途中の `<` で実行されてしまうため、具体的な版（`22`）にしてある。

### where・which

```powershell
where <コマンド>
which <コマンド>
```

- Windows の PowerShell で `which` を使うには、`scoop` の `which` が入っている前提（`apps.txt` に `which` がある）。

### winget

```powershell
winget install --id <ID> -e
winget list
winget search <名前>
winget uninstall --id <ID>
```

### workflow-kit

```powershell
uv run --script $env:WFKIT_DIR\room\room.py --help
uv run --script $env:WFKIT_DIR\room\room.py aws-key <Area名> --profile <プロファイル名>
uv run --script $env:WFKIT_DIR\room\room.py close <Project名>
uv run --script $env:WFKIT_DIR\room\room.py init <Area名> --boundary internal
uv run --script $env:WFKIT_DIR\room\room.py init <Area名> --boundary internal --only <段名>
uv run --script $env:WFKIT_DIR\room\room.py init <Area名> --boundary internal --resume
uv run --script $env:WFKIT_DIR\room\room.py init <Area名> --boundary internal --ca-cert <証明書のパス>
uv run --script $env:WFKIT_DIR\room\room.py mask <Project名>
uv run --script $env:WFKIT_DIR\room\room.py mkworks --update
uv run --script $env:WFKIT_DIR\room\room.py mkworks --sub
uv run --script $env:WFKIT_DIR\room\room.py open <Project名> --area <Area名> --type dev
uv run --script $env:WFKIT_DIR\room\room.py open <Project名> --area <Area名> --type inv
uv run --script $env:WFKIT_DIR\room\room.py open <Project名> --area <Area名> --type doc --data mask
uv run --script $env:WFKIT_DIR\room\room.py pull <Project名> --where <項目>=<値>
uv run --script $env:WFKIT_DIR\room\room.py readme <Project名>
uv run --script $env:WFKIT_DIR\room\room.py reap <Project名> --force
uv run --script $env:WFKIT_DIR\room\room.py rename-area <旧Area名> <新Area名>
uv run --script $env:WFKIT_DIR\room\room.py restore <Project名>
uv run --script $env:WFKIT_DIR\room\room.py shell <Area名>
uv run --script $env:WFKIT_DIR\room\room.py start <Project名>
uv run --script $env:WFKIT_DIR\room\room.py start <Project名> --no-launch
uv run --script $env:WFKIT_DIR\room\room.py start <Project名> --no-launch --adopt
uv run --script $env:WFKIT_DIR\room\room.py start <Project名> --gateway
uv run --script $env:WFKIT_DIR\room\room.py stock <Project名>
uv run --script $env:WFKIT_DIR\room\room.py umount --area <Area名>
uv run --script $env:WFKIT_DIR\tools\cap_meter.py
uv run --script $env:WFKIT_DIR\tools\cap_meter.py --latest
uv run --script $env:WFKIT_DIR\tools\check_inbox.py --show-pass
uv run --script $env:WFKIT_DIR\tools\check_py.py <パス> --run-tests
uv run --script $env:WFKIT_DIR\tools\decompose_session.py --session <会話ID>
uv run --script $env:WFKIT_DIR\tools\decompose_session.py --session <会話ID> --steps
uv run --script $env:WFKIT_DIR\tools\due.py --days 3
uv run --script $env:WFKIT_DIR\tools\find_knowledge.py <キーワード>
uv run --script $env:WFKIT_DIR\tools\find_knowledge.py --triggers <依頼文>
uv run --script $env:WFKIT_DIR\tools\find_knowledge.py --check-index
uv run --script $env:WFKIT_DIR\tools\find_knowledge.py --check-triggers
uv run --script $env:WFKIT_DIR\tools\heavy_sessions.py --since <YYYY-MM-DD> --top 5
uv run --script $env:WFKIT_DIR\tools\repeat_reads.py --detail
uv run --script $env:WFKIT_DIR\tools\requests_by_kind.py --detail
uv run --script $env:WFKIT_DIR\tools\triggers_stats.py --detail
uv run --script $env:WFKIT_DIR\tools\usage_report.py
uv run --script $env:WFKIT_DIR\tools\usage_report.py --by month --last 3 --top 10 --prices $env:WFKIT_DIR\tools\usage_prices.json
uv run --script $env:WFKIT_DIR\tools\usage_report.py --sort cost --prices $env:WFKIT_DIR\tools\usage_prices.json
uv run --script $env:WFKIT_DIR\tools\usage_report_html.py --by month --last 6
```

- 2026-10-30 に、Python の実行を `uv run --script <パス>.py` に統一し、`$env:WFKIT_DIR`（`10_env.bat` が `<works>\resources\workflow-kit` に設定）を使う形にした。作業ディレクトリに依存せず、`<…名>` を書き換えるだけで実行できる。`$env:WFKIT_DIR` は Tab 補完で実パスに変わらない（`profile.ps1` の Tab ハンドラ）。
- 自作スクリプトだけを載せる。`room.py` の引数は `room.py <サブコマンド> --help` が正本。`init`・`open` の `--boundary internal` と `--type dev` は、よく使う値を入れてある（適宜書き換える）。`reap --force` は期限前でも消すので、`<Project名>` を必ず確かめる。
- Linux（zsh/bash）側の種には載せない。`WFKIT_DIR` は Windows の `10_env.bat` だけが設定する。

### wsl

```powershell
wsl -d <ディストロ名>
wsl -d <ディストロ名> -e printenv <変数名>
wsl --install -d <ディストロ名>
wsl --list --online
wsl --list --verbose
wsl --set-default <ディストロ名>
wsl --shutdown
wsl --status
wsl --unregister <ディストロ名>
wsl --update
```

- `wsl --install` の打ち間違い（`wsl install`）が履歴にあった。`wsl --install -d <ディストロ名>` が正しい。ディストロ名は `wsl --list --online` で確認する。
## 履歴の種（zsh/bash・素案）
<!-- 素材: 開始時に読まない / 確認: 2026-10-27 -->

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

Windows 側の git の節と同一（コマンド仕様が同じなので流用）。

```bash
git status
git fetch
git pull
git pull origin main
git pull --rebase
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
- 他PCの生履歴には、勤務先のユーザー名（Windows のアカウント名）入りの絶対パスと、案件固有のリポジトリ名・タグ名がある。種には載せない。
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
