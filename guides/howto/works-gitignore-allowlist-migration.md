---
type: howto
title: 既存の works を許可リスト方式の .gitignore に移す（Python の版の変更とまとめて取り込む）
tags:
  - setup
  - windows
  - tool/git
---

# 既存の works を許可リスト方式の `.gitignore` に移す

2026-10-29 の 2 つの変更を、すでに使っている works（PC1・PC2）に取り込む手順書。範囲は「`resources/`（workbase）を最新にする」から「works の追跡が許可リストどおりになり、`room start` が通る」まで。上から順に実行する。

- **Python の版をそろえる変更**（`39571f7`）: 文書と `cleankit.py` の `requires-python`（`==3.13.*`）だけ。正本の `workflow-kit/room/.python-version`（3.13.14）は前から同じなので、works 側で直すものは無い。3 章で、uv にその版が入っていることだけ確かめる。WSL の `python3` を正本の版にする段（`room init`）は未実装なので、今回は何もしない。
- **works の git 追跡を許可リスト方式にする変更**（`48e6fc3`）: works ごとに `.gitignore` と `AGENTS.md` を新しい雛形に合わせ、追跡済みで今後は追跡しないファイルを `git rm --cached` で外す。ファイルも履歴も消えない。
- 背景と決定は `docs/decisions.md` の 2026-10-29 の 2 項、`.gitignore` の中身は [[ai-room-setup]] の 2.1。

**実機は未確認**。git の手順（4〜7 章）は、模擬の works（Linux の git 2.53）で通した。Windows の git と PowerShell では未確認なので、PC2 のリハーサル（5 章）で先に確かめる。

## 対応バージョン表

| 項目 | 版・条件 | 状態 |
|---|---|---|
| git（Windows） | 2.26 以上（`--pathspec-from-file` を使う） | 要確認（2 章で見る） |
| uv の Python | 3.13.14（`workflow-kit/room/.python-version`） | room が動いていれば入っている |
| PowerShell | 5.1 / 7 のどちらでもよい。ファイル名を壊さないよう、一覧と削除は `cmd /c` の中で行う | — |
| workbase の版 | `48e6fc3` 以降（雛形の `~$*` の追記を含む版） | — |
| 手順の確認日 | 2026-10-29（模擬の works のみ） | — |

## 全体の流れ

| 章 | 内容 | 区分 | 完了の目安 |
|---|---|---|---|
| 0 | 事故りやすい点を知る | 読むだけ | — |
| 1 | 適用の順番を決める | 読むだけ | 順番の表のどこから始めるか分かる |
| 2 | 事前確認（works ごと） | 手動 | 全部の目安どおり |
| 3 | `resources/` を最新にする（PC ごと） | 手動 | `uv run room.py --help` が出る |
| 4 | バックアップ（works ごと） | 手動 | `works.bundle` と `.gitignore` の写しがある |
| 5 | リハーサル（PC2 で 1 回） | 手動 | 写しの works で 6〜8 章が通る |
| 6 | `.gitignore` と `AGENTS.md` を雛形に合わせる | スクリプト + 手動 | 判定の 4 行が目安どおり |
| 7 | 追跡から外す | 手動 | `git ls-files -ci --exclude-standard` が空 |
| 8 | 完了の確認 | 手動 | `room start` の報告に許可リスト方式の行が出る |
| 9 | 戻し方 | 必要なときだけ | — |

## 0. 事故りやすい点

| 事故 | 起きること | この手順での防ぎ方 |
|---|---|---|
| `git rm` に `--cached` を付け忘れる | 作業ファイルが消える | 7 章のコマンドを写して使う。消えても、コミット済みの版は `git restore` で戻る（2 章で「未コミットなし」を確かめてあるので、失うものは無い） |
| `git rm -r --cached projects/*/ai` のように、パスを手で書く | `ai/docs/` や `ai/README.md` まで外れる。git のパスの `*` は `/` もまたぐ | 外す対象は手で書かず、新しい `.gitignore` が無視すると判定した追跡済みファイル（`git ls-files -ci --exclude-standard`）だけにする |
| `resources/` で、ふつうの `git pull` をする | workbase は 10-29 に履歴を書き換えた。まだ追従していない clone では、古い履歴と新しい履歴がマージされ、消した語が戻る | 3 章で、先にローカルの変更とコミットが無いことを見てから、早送りか `reset --hard origin/main` |
| `.gitignore` を雛形で上書きして、その works だけの行を失う | 追跡したくないファイルがまた出る、または追跡したいものが外れる | 4 章で写しを取り、6 章の `mkworks --update`（3 者マージ。衝突なら何も書かずに止まる）を先に試す |
| `mkworks --update` に `--yes` を付ける | 確認なしで全部の雛形が反映される | `--yes` を付けない。差分を見て、ファイルごとに `y` / `N` |
| `room start` の最中に作業する | 回収のコミットとぶつかる（`index.lock`） | 2 章で、部屋が動いていないことを確かめる |
| 移行の後に `git clean -X` / `-x`、古いコミットへの `checkout` | `ai/` の中身は「無視されたファイル」になり、git は消してよいものとして扱う。成果物が消える・古い版で上書きされる | 9 章の「やってはいけないこと」 |
| remote がある works を、別の PC で `git pull` する | 外したファイルが、その PC の作業ツリーから消える | 2 章で remote を確かめる。ある場合は 7.5 の手順で取り込む |
| 雛形の古い版（`48e6fc3` そのもの）を使う | `docs/` と `ai/docs/` の中の `~$*`（Office のオーナーファイル。Windows のユーザー名が入る）や `Thumbs.db` が追跡の候補に出る | 3 章で最新の workbase にしてから始める（雛形の末尾に 3 行を足した版） |

## 1. 適用の順番

works ごとに 2〜8 章を回す。1 つ終えて 8 章を確かめてから、次へ進む。

| 順 | PC | 対象 | 理由 |
|---|---|---|---|
| 1 | PC2 | `resources/` を最新に（3 章） | ネットにつながり、失敗してもやり直しやすい |
| 2 | PC2 | 本物の works の写しでリハーサル（5 章） | Windows の git・PowerShell での挙動を、本物を触らずに確かめる |
| 3 | PC2 | 本物の works（6〜8 章） | — |
| 4 | PC2 | ほかの works（`works_sub<N>` など）があれば | 検証用なら、移さずに消してもよい |
| 5 | PC1 | `resources/` を最新に → works（3〜8 章） | 実務で使う works なので最後。部屋を使わない時間帯に行う |

- PC1 は works を手で直す（works は PC 間で同期していない前提。2 章の `git remote -v` で確かめる）。PC2 で作ったコミットを PC1 に運ぶ必要は無い。

## 2. 事前確認（works ごと）

PowerShell で、対象の works のルートに移る。以下、`$W` は対象の works。

```powershell
$W = "$HOME\works"
Set-Location $W
git --version
git status --porcelain
git remote -v
wsl -l --running
git ls-files | Measure-Object -Line
git ls-files | Select-String '/ai/' | Measure-Object -Line
git ls-files | Select-String '_noai/' | Measure-Object -Line
Get-Content .gitignore -TotalCount 3
```

| 確かめること | 目安 | 外れたら |
|---|---|---|
| `git --version` | 2.26 以上 | Git for Windows を更新する |
| `git status --porcelain` | 何も出ない | 先にコミットする（`room start` の回収漏れなら、内容を見てから） |
| `git remote -v` | 何も出ない（ローカル専用） | 出たら、7.5 も行う。その remote を clone している PC を書き出しておく |
| `wsl -l --running` | `room-` で始まる名前が無い | `room start` を終わらせる |
| `/ai/` の数 | 0 より大きい（外す対象がある） | 0 なら、6 章だけ行う |
| `_noai/` の数 | **0** | 0 でなければ**止まる**。AI に見せない原本が履歴に入っている。外すだけでは履歴に残るので、扱いを相談する |
| `.gitignore` の先頭 | `*` で始まらない（旧方式） | すでに `*` なら移行済み。8 章の確認だけ行う |

## 3. `resources/` を最新にする（PC ごとに 1 回）

`$R` は works の `resources/`（workbase の clone）。

1. ローカルの変更とコミットが無いことを確かめる（**fetch の前に**行う。後だと比べる相手が変わる）

   ```powershell
   $R = "$HOME\works\resources"
   git -C $R status --porcelain
   git -C $R log --oneline '@{u}..HEAD'
   ```

   - 両方とも何も出ない。出たら止まる（PC1 の `resources/` は pull だけの約束なので、出るのは想定外）
2. 今の版を控える（戻すとき用）

   ```powershell
   $B = "$HOME\works-migrate"
   New-Item -ItemType Directory -Force $B | Out-Null
   git -C $R rev-parse HEAD | Set-Content "$B\resources-head-before.txt"
   ```

3. 取ってきて、つながり方を見る

   ```powershell
   git -C $R fetch origin
   git -C $R merge-base --is-ancestor HEAD origin/main; $LASTEXITCODE
   ```

   | `$LASTEXITCODE` | 意味 | 次のコマンド |
   |---|---|---|
   | `0` | 履歴の書き換えには追従済み | `git -C $R merge --ff-only origin/main` |
   | `1` | 書き換え前の履歴のまま | `git -C $R reset --hard origin/main`（1 で変更もコミットも無いことを確かめたので、失うものは無い） |

   - **よく忘れる点**: `git pull`（`--ff-only` なし）を使わない。古い履歴とマージされる
4. 版を確かめる

   ```powershell
   git -C $R log -1 --oneline
   Select-String -Path "$R\workflow-kit\templates\workspace\gitignore.template" -Pattern '^~\$\*$'
   ```

   - `~$*` の行が出る（出なければ、まだ古い。1 からやり直す）
5. Python と room を確かめる

   ```powershell
   Set-Location "$R\workflow-kit\room"
   Get-Content .python-version
   uv python find 3.13.14
   uv run room.py --help
   ```

   - `uv python find` がパスを出す。出なければ `uv python install 3.13.14`（ネットが要る。勤務先のネットワークで通るかは未確認。通らなければ、9 章で `resources/` を戻し、この PC は後回しにする）
   - PC2 だけ、任意で `uv run python -m unittest discover -s tests`（OK で終わる）

**完了の目安**: `uv run room.py --help` が出る。`resources/` を新しくしても、旧方式の works の `room start` はそのまま通る（`room` が必須とする行は `**/_noai/` だけになった）。急ぎの作業があれば、ここで止めて、4 章以降は別の日でもよい。

## 4. バックアップ（works ごと）

コミット済みの全部を 1 ファイルにする。作業ファイルは `--cached` では触らないので、ここでは写さない。

```powershell
Set-Location $W
$B = "$HOME\works-migrate\" + (Split-Path $W -Leaf)
New-Item -ItemType Directory -Force $B | Out-Null
git bundle create "$B\works.bundle" --all
git bundle verify "$B\works.bundle"
Copy-Item .gitignore "$B\gitignore.before"
Copy-Item AGENTS.md "$B\AGENTS.md.before"
git rev-parse HEAD | Set-Content "$B\works-head-before.txt"
```

- `git bundle verify` が `is okay` で終わる
- 置き場所は works の外（`$HOME\works-migrate\<works 名>`）。works の中に置かない（Obsidian と `room` が拾う）

## 5. リハーサル（PC2 で 1 回だけ）

本物の works を clone した写しで、6〜8 章の git の部分を通す。写しは追跡済みのファイルだけを持つので、本物には影響しない。

```powershell
git clone -q $HOME\works $HOME\works-rehearsal
Set-Location $HOME\works-rehearsal
Copy-Item "$HOME\works\resources\workflow-kit\templates\workspace\gitignore.template" .gitignore
```

1. 6 章の「判定の 4 行」と、7 章の 1〜5 を、`$W = "$HOME\works-rehearsal"` として行う（`mkworks --update` は写しでは使えないので、上の `Copy-Item` で代える）
2. 7 章の一覧と件数が、2 章の `/ai/` の数と見合うか、ファイル名（日本語・空白）が化けていないかを見る
3. 終わったら写しを消す。**パスを必ず確かめてから**消す

   ```powershell
   Set-Location $HOME
   Remove-Item -Recurse -Force $HOME\works-rehearsal
   ```

## 6. `.gitignore` と `AGENTS.md` を雛形に合わせる

1. `mkworks --update` で、雛形の変更を 3 者マージで当てる（**`--yes` は付けない**）

   ```powershell
   Set-Location "$W\resources\workflow-kit\room"
   uv run room.py --vault $W mkworks --update
   ```

   | 出力 | 意味 | すること |
   |---|---|---|
   | ファイルごとの差分と `反映する? [y/N]` | マージできた | `.gitignore` と `AGENTS.md` は差分を読んで `y`。ほかの雛形も、自分で足した行が消えていなければ `y`。終わると `[works] mkworks --update: …` でコミットされる |
   | `基点（前に反映した版）が分からない` | works のコミットの `Room-Rev` が、書き換え前の workbase のハッシュ | `--base 1d1a17b` を付けて、もう一度（許可リスト化の直前の版） |
   | `衝突` で止まる | 手で作った `.gitignore` など。何も書いていない | 2 へ |
   | `未コミットの変更がある` | 2 章の確認漏れ | コミットしてから、もう一度 |

2. （1 が衝突で止まったときだけ）手で写す

   ```powershell
   Set-Location $W
   Copy-Item "$W\resources\workflow-kit\templates\workspace\gitignore.template" .gitignore
   git diff --no-index "$B\gitignore.before" .gitignore
   ```

   - 差分の `-` の行のうち、雛形の旧版に無かった、この works だけの行を確かめる。追跡しないための行（`*.bak` など）は、末尾の `~$*` の 3 行の後に足す。追跡するための `!` の行は、`# 追跡するもの` の並びに足す（`*` より前に置くと効かない）
   - `AGENTS.md` の `` `.gitignore` に `**/_noai/` …と `!**/ai/out/` を入れる `` の 1 行を、雛形（`resources\workflow-kit\templates\workspace\AGENTS.md`）の同じ箇所の 1 行に置き換える
   - コミットする

     ```powershell
     git add -- .gitignore AGENTS.md
     git diff --cached --stat
     git commit -m "[works] .gitignore を許可リスト方式にする（雛形 gitignore.template）"
     ```

3. 判定の 4 行（`<Project>` は実在の Project 名）

   ```powershell
   Set-Location $W
   git check-ignore -v "projects/<Project>/ai/out/x.xlsx"
   git check-ignore -v "projects/<Project>/ai/docs/log.md"; $LASTEXITCODE
   git check-ignore -v 'docs/~$a.xlsx'
   git status --short
   ```

   - 1 行目: `.gitignore:<行>:**/ai/*` が出る（無視される）
   - 2 行目: 何も出ず、`1`（追跡される）
   - 3 行目: `~$*` の行が出る
   - 4 行目: `ai/` の下の `??` が出ない（`D` もまだ出ない）

## 7. 追跡から外す

外す対象は、手で書かない。「追跡済みで、新しい `.gitignore` では無視されるファイル」を git に出させて、それをそのまま渡す。一覧と削除は `cmd /c` の中で行う（PowerShell を通すと、日本語のファイル名や区切りの NUL が変わることがあるため）。

1. 一覧をファイルに出す

   ```powershell
   Set-Location $W
   $env:B = $B
   cmd /c 'git -c core.quotepath=false ls-files -ci --exclude-standard > "%B%\untrack-list.txt"'
   (Get-Content -Encoding utf8 "$B\untrack-list.txt").Count
   Get-Content -Encoding utf8 "$B\untrack-list.txt" | ForEach-Object { ($_ -split '/')[0..2] -join '/' } | Group-Object | Sort-Object Count -Descending | Format-Table Count, Name
   ```

2. 一覧を見る（`notepad "$B\untrack-list.txt"`）

   | 一覧に出たもの | 判断 |
   |---|---|
   | `projects/*/ai/` の `in` `work` `out` `records`、`ai/ctx` | 外す（今回の目的） |
   | `archives/*/src` `tests` `Makefile` など | 外す（10-29 にユーザーが決定） |
   | `areas/` や `projects/` の直下の個別のファイル（会議録など） | 外してよいか判断する。残したいなら `docs/` に移すか、`.gitignore` に `!` の行を足してから、1 をやり直す |
   | `_noai/` を含む行 | **止まる**（2 章の `_noai/` の数が 0 でなかった。相談する） |
   | `ai/docs/` を含む行、`README.md` | 出ないはず。出たら `.gitignore` が雛形どおりでない。6 章へ戻る |

3. 空打ち（何を外すかを表示するだけ）

   ```powershell
   cmd /c 'git ls-files -ci --exclude-standard -z | git --literal-pathspecs rm --cached -n --pathspec-from-file=- --pathspec-file-nul > "%B%\untrack-dryrun.txt"'
   (Get-Content -Encoding utf8 "$B\untrack-dryrun.txt").Count
   ```

   - 件数が 1 の件数と同じ
4. 外す（`--cached` があることを、もう一度目で見てから）

   ```powershell
   cmd /c 'git ls-files -ci --exclude-standard -z | git --literal-pathspecs rm --cached -q --pathspec-from-file=- --pathspec-file-nul'
   ```

5. 確かめる

   ```powershell
   git ls-files -ci --exclude-standard | Measure-Object -Line
   git status --porcelain | Select-String -NotMatch '^D  ' 
   Test-Path (Join-Path $W ((Get-Content -Encoding utf8 "$B\untrack-list.txt" -TotalCount 1) -replace '/', '\'))
   ```

   - 1 行目が 0、2 行目が何も出ない（`D ` だけ）、3 行目が `True`（ファイルは残っている）
6. コミットする（ステージ済みの削除だけが入る。`-a` を付けない）

   ```powershell
   git commit -m "[works] 許可リスト方式: 無視の対象になった追跡済みファイルを、追跡から外す（ファイルと履歴は残す）"
   git show --stat HEAD | Select-Object -Last 3
   ```

   - 変更の件数が、1 の件数と同じ

### 7.5 remote がある works だけ

この works を clone している別の PC では、`git pull` をしない（外したファイルが、その PC の作業ツリーから消える）。別の PC では次のように取り込む。

```powershell
git status --porcelain              # 何も出ない
git log --oneline '@{u}..HEAD'      # 何も出ない
git fetch origin
git reset origin/main               # --hard を付けない。作業ツリーは触らず、HEAD とステージだけ動かす
git restore -- :/                   # 追跡しているファイル（.gitignore など）を新しい版にする。外したファイルは触らない
git status --short                  # 何も出ない
```

- この works を push するかは、その works の `AGENTS.md` の方針に従う（ローカル専用なら `pre-push` が止める）

## 8. 完了の確認

```powershell
Set-Location $W
git ls-files -ci --exclude-standard | Measure-Object -Line
git ls-files | Select-String '/ai/' | Select-String -NotMatch '/ai/docs/|/README\.md$'
git log --oneline -3
```

- 1 行目が 0、2 行目が何も出ない（`ai/` で追跡するのは `ai/docs/` と README だけ）、3 行目に 6 章と 7 章のコミット
- 次の `room start <Project>` の回収の報告に `（許可リスト方式: ai/ は docs/ 以外を追跡しない。ai/out は N ファイル。…）` が出て、`警告: 追跡されずに無視されているファイル` が出ない
- 全部の works が終わったら、`$HOME\works-migrate` は 1 週間ほど残してから消す

## 9. 戻し方

| 状況 | 戻し方 |
|---|---|
| 7 章の 4 の後、コミット前 | `git restore --staged -- :/`（ステージを `HEAD` に戻す。作業ファイルは触らない）。続けて `.gitignore` も戻すなら `Copy-Item "$B\gitignore.before" .gitignore` |
| 7 章のコミットの後（その後に別のコミットが無い） | `git reset --soft HEAD~1` の後に `git restore --staged -- :/`。**`git revert` は使わない**（外したファイルを、コミット時点の古い中身で上書きする） |
| 6 章のコミットの後 | `git checkout HEAD~1 -- .gitignore AGENTS.md`（7 章を戻した後に行う）してコミットする |
| works を丸ごと前に戻したい | `git clone "$B\works.bundle" $HOME\works-restore` で中身を確かめ、要るファイルを手で写す（本物の works の上には clone しない） |
| `resources/` を前の版に戻す | `git -C $R reset --hard (Get-Content "$HOME\works-migrate\resources-head-before.txt")`。書き換え前の履歴に戻るので、次は 3 章からやり直す |

**やってはいけないこと**

- `git rm` を `--cached` なしで使う。作業ファイルが消える
- 外す対象のパスを手で書く（`projects/*/ai` など）。`ai/docs/` まで外れる
- 移行の後に `git clean -X` / `git clean -x` を使う。`ai/` の中身は無視されたファイルなので、成果物ごと消える
- 移行の後に、移行前のコミットを `git checkout` / `git switch --detach` する。無視されたファイルは、確認なしに古い版で上書きされる
- `resources/` で `git pull` を（`--ff-only` なしで）使う。書き換え前の履歴とマージされる
- WSL の `python3` を uv の版で置き換える。システムの `python3`（3.14）は apt の道具が使う。正本の版にする段は `room init` に足す予定（未実装。`docs/log.md`）
- 複数の works を並行して作業する。1 つずつ 8 章まで確かめる
