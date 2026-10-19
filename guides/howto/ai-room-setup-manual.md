---
type: howto
title: AI 作業部屋 実例（手作業版）
tags:
  - setup
  - security
  - tool/wsl
  - ai/claude
  - windows
---

# AI 作業部屋 実例（手作業版）

`room.py` を使わず、PowerShell と `wsl` のコマンドだけで、AI 作業部屋の作成から、Project の作業、`close`、片付けまでを、実際の名前（Area `pilot`、部屋 `room-pilot`、Project `pilot-1`）で1手ずつ通す手順書。2026-10-18 に、この流れで実機を通した。スクリプトが何をしているかを知りたいとき、スクリプトが使えないときに使う。スクリプト版は [[ai-room-setup-script]]、手順の説明（プレースホルダー版）は [[ai-room-setup]]、仕組みと理由は [[ai-room-why]]。

- **ゴール（完了の目安）**: 部屋の中の Claude Code が、`/mnt/room/pilot-1`（Project の `ai/`）だけを読み書きでき、`/mnt/c` が見えない。成果物が works に現れる。`close` で `archives/pilot-1/` に移る
- **実名について**: `pilot` `pilot-1` は試験用の名前。自分の Area と Project の名前に置き換えて読む。部屋の名前は `room-<Area>` で、Area の名前と一致させる
- **スクリプトとの違い**: マスク・復元、共有知（`~/shared`）の送付、`ai/in/` の来歴（manifest）、部屋の AI の起動の準備は、この手順書の範囲外（`room.py` が行う）。ここは、部屋の作成、マウント、AI の使用、アンマウント、`close` の副作用まで
- パスは `$HOME` で書く。固有情報（勤務先名、顧客名）は書かない

## 対応バージョン表

手順の確認日: 2026-10-18（実機）。Windows、WSL、Claude Code、uv、Zed のバージョンは、[[ai-room-setup]] の「対応バージョン表」を正とする（ここには書かない）。部屋のベースは Ubuntu 26.04（2026-10-19 に 24.04 から変更。実機の通しは未了）。

## 全体の流れ

| 章 | 内容 | 完了の目安 |
|---|---|---|
| 1 | 前提を確認する | WSL2 と Claude のアカウントがある |
| 2 | works 側の準備（`.gitignore`、Area、Project のひな形） | `_noai/` が `git status` に出ない |
| 3 | 部屋を作る | `ai`、`0`、`no-cmd`、`sudo: a password is required` |
| 4 | 道具を入れ、ログインする | 部屋の `claude -p` が `ok` を返す |
| 5 | マウントして使う | `ai/` の中身だけが見え、`/mnt/c` が空 |
| 6 | アンマウントする | マウントが `0`、マウント点が `0` |
| 7 | Zed から使う（任意） | `WSL: room-pilot`、部屋の側で Agent が動く |
| 8 | 閉じる | `archives/pilot-1/` に移った |
| 9 | 片付ける | 部屋が消えた |
| 10 | うまくいかないとき | |

## 1. 前提を確認する

```powershell
wsl --version
wsl -l -v          # VERSION が 2
```

- Claude のアカウントがある。works が `$HOME\works` にあり、`areas/` `projects/` `archives/` がある

## 2. works 側の準備

**2.1 `.gitignore`**: `$HOME\works\.gitignore` に、次の4行があるか確かめ、無ければ足す。

```
**/_noai/
~$*
!**/ai/out/
**/ai/ctx/
```

```powershell
Select-String -Path $HOME\works\.gitignore -Pattern '_noai|~\$|!\*\*/ai/out|ai/ctx'
```

- `!**/ai/out/` が無いと、個人のグローバル ignore の `out/` が成果物を無視し、成果物がコミットから黙って漏れる

**2.2 Area と境界の印**: `boundary:` は必須。顧客・機密度が同じ Project は、同じ Area にする。

```powershell
New-Item -ItemType Directory -Force "$HOME\works\areas\pilot" | Out-Null
"---`nboundary: internal`n---`n# pilot`n" | Set-Content "$HOME\works\areas\pilot\README.md" -Encoding utf8
```

**2.3 Project のひな形**:

```powershell
$p = "$HOME\works\projects\pilot-1"
foreach ($d in 'ai\docs','ai\in','ai\work','ai\out','ai\records','_noai\raw','_noai\map','_noai\final') { New-Item -ItemType Directory -Force "$p\$d" | Out-Null }
foreach ($d in 'in','work','records') { New-Item -ItemType File "$p\ai\$d\.gitkeep" -Force | Out-Null }
"---`narea: pilot`nstatus: active`n---`n# pilot-1`n目的: 手作業の通し確認`n完了条件: ai/out/hello.md ができる`n" | Set-Content "$p\README.md" -Encoding utf8
git -C $HOME\works status --short
git -C $HOME\works check-ignore -v projects/pilot-1/ai/out/x.xlsx
```

- 目安: `_noai/` が `status` に出ない。`check-ignore` は無出力（`ai/out/` は無視されない）
- README の `area:` は、部屋の名前の `<Area>`（`pilot`）と一致させる

## 3. 部屋を作る

```powershell
wsl --install Ubuntu-26.04 --name room-pilot --no-launch      # 数分かかる
wsl -l -v                                                      # room-pilot が出る
wsl -d room-pilot -u root -- sh -c "useradd -m -u 1000 -s /bin/bash ai; id ai"
$conf = "[automount]`nenabled=false`nmountFsTab=false`n`n[interop]`nenabled=false`nappendWindowsPath=false`n`n[user]`ndefault=ai`n"
$conf | wsl -d room-pilot -u root -- tee /etc/wsl.conf
wsl --terminate room-pilot
wsl -d room-pilot -- sh -c "id -un; ls /mnt/c | wc -l; command -v cmd.exe || echo no-cmd; sudo -n true 2>&1 | head -1"
```

- 目安: `ai`、`0`、`no-cmd`、`sudo: a password is required`
- **一般ユーザーを先に作る**。root のままだと `C:` をマウントできてしまう。ユーザーが無いまま `[user] default=ai` にすると、起動できなくなる
- `wsl.conf` は標準入力で渡す（`echo` だとバックスラッシュが解釈される）。`/mnt/c` というディレクトリ自体は、空のまま存在する（正常）

## 4. 道具を入れ、ログインする

```powershell
wsl -d room-pilot -u root -- sh -c "apt-get update -qq && apt-get install -y -qq curl ca-certificates ripgrep"
wsl -d room-pilot -- bash -lc 'curl -LsSf https://astral.sh/uv/install.sh | sh'
wsl -d room-pilot -- bash -lc 'curl -fsSL https://claude.ai/install.sh | bash'
'export PATH="$HOME/.local/bin:$PATH"' | wsl -d room-pilot -- tee -a /home/ai/.bashrc
wsl -d room-pilot -- bash -ic 'claude --version; uv --version; rg --version | head -1'
```

- 配布元のスクリプトをそのまま実行する。内容を確認したいときは、ファイルに保存して読んでから実行する

**ログイン（人の操作）**:

```powershell
wsl -d room-pilot
```
```bash
claude        # 表示された URL をブラウザで開いてログインし、コードを貼って /exit
```

```powershell
wsl -d room-pilot -- bash -ic 'cd ~ && claude -p "Reply with exactly: ok"'     # ok
```

- 認証情報は、部屋のホーム（`/home/ai/.claude/`）だけにあり、works には出ない

## 5. マウントして使う

`ai/` だけを、部屋の `/mnt/room/pilot-1` にマウントする。**マウントは root で行い、ほかの Project がマウントされていないことを先に確かめる**。

**5.1 事前の確認と、README の写し**:

```powershell
$p = "$HOME\works\projects\pilot-1"
New-Item -ItemType Directory -Force "$p\ai\ctx" | Out-Null
Copy-Item "$p\README.md" "$p\ai\ctx\README.md" -Force
(Get-Item "$p\ai\ctx\README.md").IsReadOnly = $true           # 派生物。毎回上書きする
wsl -d room-pilot -u root -- sh -c "grep -c ' /mnt/room/' /proc/mounts"     # 0（ほかのマウントが無い）
```

**5.2 マウントする**:

```powershell
$win = "$HOME\works\projects\pilot-1\ai"
$mp  = "/mnt/room/pilot-1"
wsl -d room-pilot -u root -- sh -c "mkdir -p $mp && mount -t drvfs -o metadata,uid=1000,gid=1000 '$win' $mp"
wsl -d room-pilot -u root -- sh -c "find $mp/in -type f -exec chmod a-w {} +"          # 入力を読み取り専用にする
wsl -d room-pilot -- sh -c "ls $mp; ls /mnt/c | wc -l"
wsl -d room-pilot -u root -- sh -c "grep ' /mnt/room/' /proc/mounts"
```

- 目安: `ai/` の中身（`docs` `in` `out` `records` `work` `ctx`）だけが見え、`/mnt/c` は `0`。`/proc/mounts` に `/mnt/room/pilot-1` の1行（`9p`）
- **`-o` は、デバイス名（Windows のパス）の前に書く**。後ろに書くと失敗する
- `uid=1000,gid=1000` は、部屋の一般ユーザー `ai` に合わせる。`in/` の `chmod a-w` はファイル単位（Windows 側でも読み取り専用の属性になる）
- **PowerShell から `sh` に複数行を標準入力で渡さない**。改行が CRLF になり、`umount` が失敗して、マウントが積み重なる。1行ずつ `-c` で渡す

**5.3 AI を使う**:

```powershell
wsl -d room-pilot -- bash -ic "cd /mnt/room/pilot-1 && claude"
```

- 部屋の `claude` に「`ai/out/hello.md` を作って」と頼み、`/exit` で戻る。新しい Project の最初に、信頼の確認（`Is this a project you trust?`）が出る。内容を確認して進める
- 非対話（`claude -p`）は、`--allowedTools` で許可するツールを指定する

**5.4 回収を確認する**（成果物は、Windows 側にそのまま現れる）:

```powershell
git -C $HOME\works status --short
```

- 目安: `projects/pilot-1/ai/out/hello.md` が `??` で出る。出なければ 2.1 の `!**/ai/out/` を確認する。`~$*`（Excel のオーナーファイル）は、出ても git には出ない

## 6. アンマウントする

**マウントを必ず外し、マウント点のディレクトリも消す**。`start` の終わりに自動で行うことを、手作業でする。

```powershell
wsl -d room-pilot -u root -- sh -c "umount /mnt/room/pilot-1 && rmdir /mnt/room/pilot-1"
Start-Sleep 3
wsl -d room-pilot -u root -- sh -c "grep -c ' /mnt/room/' /proc/mounts; ls /mnt/room | wc -l"      # 0 と 0
attrib -R "$HOME\works\projects\pilot-1\ai\in\*" /S          # 入力の読み取り専用を、Windows 側で戻す
Remove-Item "$HOME\works\projects\pilot-1\ai\ctx" -Recurse -Force
```

- **`rmdir` を忘れると**、空のマウント点に Project 名が残り、別の Project の作業中に AI の `ls` で見える
- アンマウント直後は、数秒待ってから確認する（直後だと、マウントが1つ残って見えることがある）

**アンマウントできないとき**:

| 症状 | 原因 | 対処 |
|---|---|---|
| `target is busy` | 部屋の中のプロセスが `/mnt/room/pilot-1` を掴んでいる | 掴んでいるものを探す: `wsl -d room-pilot -u root -- sh -c "ls -l /proc/[0-9]*/cwd 2>/dev/null \| grep room"`。Zed や `claude` を閉じる |
| 掴むプロセスが見つからない | | `wsl --terminate room-pilot` で部屋ごと止める（マウントも消える。認証情報と道具は残る）。再度 `grep -c ' /mnt/room/' /proc/mounts` で `0` を確認する |
| マウントが複数残る | `sh` に CRLF の複数行を渡した | `umount` を1行ずつ、残りの数だけ繰り返す。`wsl --terminate` でも消える |

## 7. Zed から使う（任意）

5.2 のマウントをしたまま、Zed で部屋に接続する。

1. Zed を一度終了し、起動する
2. `Ctrl+Shift+P` → `projects: open remote` → WSL の **`room-pilot`**（普段使いの環境ではない）を選ぶ
3. フォルダは、**部屋の中のパス `/mnt/room/pilot-1` を入力する**（Windows のフォルダを選ばない）
4. Agent パネルで、新しいスレッドの種類に Claude を選ぶ
5. 部屋の側で動いているか確認する

   ```powershell
   wsl -d room-pilot -- sh -c "ps -eo pid,user,args | grep -E 'zed|claude' | grep -v grep | cut -c1-120"
   ```

   - 目安: `zed-remote-server` と Claude のプロセスが、ユーザー `ai` で動く。ウィンドウに `WSL: room-pilot` と出て、ターミナルのプロンプトが `ai@...:/mnt/room/pilot-1$`。Agent に `uname -a; pwd` を実行させると、`Linux`、`/mnt/room/pilot-1` が返る
6. 作業が終わったら、**Zed のウィンドウを閉じてから**、6 章のアンマウントをする

- **やってはいけないこと**: Windows のフォルダを、ローカルのプロジェクトとして開かない。Agent が Windows 側（`AppData\Local\Zed\external_agents\...\claude-acp`）で動き、パスが `C:\...`、シェルが PowerShell になり、works 全体が見える。この `claude-acp` が `projects\pilot-1\ai` を掴むと、8 章の移動と削除が `being used` で失敗する
- `/home/ai` を開いた場合も、Project の中身は見えない（履歴は `-home-ai` に残る）。必ず `/mnt/room/pilot-1` を開く
- `in/` の保存は、`Permission denied` になる（読み取り専用にしたため。正常）

## 8. 閉じる

判断を部屋の AI が、副作用を人が行う。

**8.1 部屋の AI が判断する**: 5 章のようにマウントして、部屋の AI に `ai/out/close.md` を書かせる（完了条件の確認、暫定の見直し、未解決の振り分け、【汎用】候補。書き方は `workflow-kit/room-context.md`）。

**8.2 人が副作用を行う**:

1. アンマウントする（6 章）。**移動の前に行う**。Zed と `claude` が閉じていることを確かめる
2. README を更新する（`status: done`、`closed`、`reap_after` は14日後）

   ```powershell
   $p = "$HOME\works\projects\pilot-1"
   $t = Get-Content "$p\README.md" -Raw -Encoding utf8
   $t = $t.Replace("status: active", "status: done`nclosed: 2026-10-18`nreap_after: 2026-11-01")
   [IO.File]::WriteAllText("$p\README.md", $t, [Text.UTF8Encoding]::new($false))
   ```

3. Area の `ai/docs/inbox.md` に【案件】を追記する（Project 名と連番の識別子つき）。Area の README の一覧を「完了した Project」に移す

   ```powershell
   $inbox = "$HOME\works\areas\pilot\ai\docs\inbox.md"
   New-Item -ItemType Directory -Force (Split-Path $inbox) | Out-Null
   Add-Content $inbox "`n### pilot-1（2026-10-18、close で渡した）`n`n- ``pilot-1#1`` <close.md の【案件】の内容>`n"
   ```

4. 新しいファイルをステージする。そうしないと、追跡されていない成果物が `archives/` に移らない

   ```powershell
   cd $HOME\works
   $name = "pilot-1"; $src = "projects/$name"; $dst = "archives/$name"
   git add -A $src
   ```

5. 追跡しているファイルを、**1ファイルずつ** `git mv` する（ディレクトリごとだと `Permission denied` になることがある）。追跡しない `_noai/` は、ディレクトリごと移す

   ```powershell
   foreach ($f in (git ls-files $src)) {
     $to = $f -replace "^projects/", "archives/"
     New-Item -ItemType Directory -Force (Split-Path $to) | Out-Null
     git mv $f $to
   }
   Move-Item "$src/_noai" "$dst/_noai"
   ```

6. 空になった `projects/pilot-1/` を消す

   ```powershell
   Get-ChildItem $src -Recurse -Force -File     # 何も出ないこと。出たら、移し漏れ
   Remove-Item $src -Recurse -Force
   ```

7. 確認し、コミットする

   ```powershell
   Test-Path $src                               # False
   Get-ChildItem $dst -Force | Select-Object Name    # ai、_noai、README.md
   git status --short
   ```

- **`Remove-Item` が `being used` で失敗したら**: Windows 側の Zed の Agent などが `projects\pilot-1\ai` を掴んでいる。Zed のウィンドウを閉じ、`Get-Process claude` で `claude-acp` が残っていれば、他で使っていないことを確かめて `Stop-Process` する。`archives/` への移動が済んでいれば、残っているのは空の殻だけ
- **`git mv` が `Permission denied`**: `ai/in/` のファイルが読み取り専用の属性になっている。`attrib -R "$src\ai\in\*" /S` で外してから、やり直す
- 完了の目安: `projects/pilot-1/` が無く、`archives/pilot-1/` に `ai/` と `_noai/` がある。Area の `inbox.md` に項目がある

## 9. 片付ける

- 部屋の会話履歴（`~/.claude/projects/-mnt-room-pilot-1/`）は、`reap_after` まで残す。期限後に消す

  ```powershell
  wsl -d room-pilot -- sh -c 'rm -rf -- "$HOME/.claude/projects/-mnt-room-pilot-1" "$HOME/tmp/pilot-1"; ls ~/.claude/projects/'
  ```

  - 目安: `-mnt-room-pilot-1` が一覧に無い。`archives/pilot-1/README.md` に `reaped: <日付>` を足す（手で）
- 部屋ごと消す: `wsl --unregister room-pilot`（部屋の中の履歴と認証情報も消える。必要な履歴は先に `ai/records/` に写す）。ベースの `Ubuntu-26.04` には影響しない

## 10. うまくいかないとき

| 症状 | 原因 | 対処 |
|---|---|---|
| 部屋の AI から、Windows 形式のパスと PowerShell が見える | Zed の Agent が Windows 側で動いている（Windows のフォルダをローカルで開いた） | 7 章の「やってはいけないこと」。`WSL: room-pilot` と、`/mnt/room/pilot-1` を確かめる |
| `ls /mnt/c` が空でない | `wsl.conf` が効いていない | `wsl --terminate room-pilot` のあと、3 章の確認を再実行する |
| マウントで `Permission denied`、または失敗 | `-o` の位置、`uid`、CRLF | 5.2 の注意。1行ずつ `-c` で渡す |
| 成果物が `git status` に出ない | `.gitignore` の `!**/ai/out/` が無い | 2.1 |
| `git mv` が失敗する | 入力が読み取り専用、アンマウント前 | 8.2 の注意 |
