---
type: howto
title: AI 作業部屋 導入手順
tags:
  - setup
  - security
  - tool/wsl
  - ai/claude
  - windows
---

# AI 作業部屋 導入手順

顧客データ・社外秘を AI に見せないための「AI 作業部屋」を、Windows 11 + WSL2 に導入する手順書。Area ごとに WSL の専用ディストリビューション（部屋）を作り、作業中の Project の `ai/` フォルダだけを部屋に渡して、Claude Code（または Zed の Claude Agent）で作業する。なぜこの形にしたかは [[ai-room-why]]。

> **状態: 草稿（未レビュー）。別のセッションでレビューする予定。** 手順は、2026-10-12 に実機で通した内容（手作業）。レビュー前の記述は、確認と見直しの対象。

- **ゴール（完了の目安）**: 部屋の中の Claude Code が、Project の `ai/` の中のファイルだけを読み書きでき、`/mnt/c` や works の他の場所が見えないこと。作業の成果物が、works（Windows 側）にそのまま現れること
- 範囲: 部屋の作成から、Project の作業、`close`、片付けまで。マスク・復元の操作（`room.py`）は範囲外（未実装。付録）
- **スクリプトとの関係**: 操作を自動化する `room.py`（`open` / `start` / `close` / `umount`。置き場は `workflow-kit/room/`）は、**v0 を実装して、使い捨ての works で通した**（2026-10-12）。ただし**マスク・復元は未実装**で、実運用はこれから。このため、5・7 章の手作業を残している（`room.py` の動作の説明も兼ねる）。スクリプトの実運用が安定したら、スクリプトが正になり、この手順書はスクリプトの前後（手動の作業）と注意点だけにする
- 固有情報（勤務先名、顧客名、ユーザー名）は書かない。パスは `$HOME` と `<Area>` `<Project>` で書く

## 対応バージョン表

手順の確認日: 2026-10-12（すべて実機で確認）。バージョンが変わったら、表の更新と手順の再確認を行う。

| 項目 | 確認したバージョン | 備考 |
|---|---|---|
| Windows | 11（Home、ビルド 10.0.26200） | |
| WSL | 3.0.1.0（Linux カーネル 6.18.40.1） | `wsl --install --name` を使う。古い WSL では使えない可能性がある（**要確認**）。その場合は `wsl --import` |
| 部屋のディストリビューション | Ubuntu 26.04 LTS | 2026-10-19 に 24.04 から変更。実機で確認済み（2026-10-19、`room init`） |
| Claude Code | 2.1.296（公式のネイティブインストーラ） | |
| uv | 0.13.0 | Windows 側と部屋の両方。Python のバージョンは uv で固定する |
| Zed | 1.22.0（scoop 版） | WSL リモートで使う |
| Excel | Windows 版（COM 操作の確認のみ） | |

## 全体の流れ

| 章 | 内容 | 区分 | 完了の目安 |
|---|---|---|---|
| 1 | 前提を確認する | 手動 | WSL2 と Claude のアカウントがある |
| 2 | works 側の準備 | 手動 | `.gitignore`、Area の印、Project のひな形ができた |
| 3 | 部屋を作る（Area ごとに1回） | 手動 | `/mnt/c` が空、`cmd.exe` が無い |
| 4 | 部屋に道具を入れ、ログインする（部屋ごとに1回） | 手動 | 部屋で `claude` が応答する |
| 5 | Project を部屋で使う（作業のたびに） | 手動（将来は `room start`） | `ai/` だけが見え、成果物が Windows 側に現れる |
| 6 | Zed から使う | 手動 | Agent が部屋の中で動く |
| 7 | Project を閉じる | 手動（将来は `room close`） | `archives/` に移り、Area に未解決が渡った |
| 8 | 任意設定 | 手動 | （なくても、ゴールに届く） |
| 9 | 戻し方・片付け | 手動 | 部屋が消えた |
| 10 | うまくいかないとき | | |

## 1. 前提を確認する

0. 環境の前提（`room.py init` が扱うもの。2026-10-19）。新しい PC や部屋で、先に見る
   - **TLS 検査のあるネットワーク**か: `openssl s_client -connect claude.ai:443 -servername claude.ai </dev/null 2>/dev/null | openssl x509 -noout -issuer` の発行元が、公開の認証局でなければ検査あり。`init --ca-cert <ファイル>` で検査用のルート証明書を渡す（[[ai-room-setup-script]] の 2 章）
   - **`WSLENV`**: Windows 側に `/p` 付きのパスがあると、部屋に入るたびに「failed to translate」が出る（無害）。`room.py shell <Area>` で入る
   - **Node.js**: Zed の Agent に要る。`init` が Node.js 24 を入れるので、手作業では入れない
1. WSL2 が使える

   ```powershell
   wsl --version
   wsl -l -v
   ```

   - 目安: `VERSION` が `2`
2. Claude のアカウントがある（部屋の Claude Code は、ブラウザ認証（OAuth）でログインする）。Bedrock などの別経路は、未検証（**要確認**）
3. works（PARA 構成）が `$HOME\works` にあり、`areas/` `projects/` `archives/` がある

## 2. works 側の準備

works（ローカルの git）に、1回だけ行う。

### 2.1 `.gitignore` を許可リスト方式にする

works の `.gitignore` は許可リスト方式（2026-10-29）。雛形は `workflow-kit/templates/workspace/gitignore.template`（`room mkworks` が置く）。最初に `*` で全部除外し、追跡するものだけ `!` で戻す。

- **追跡する**: dotfile（`.gitignore` `.ignore` `.gitattributes` `.claude/settings.json`）、`AGENTS.md` `CLAUDE.md`、README（深さを問わず）、`docs/`（深さを問わず）、Project と Area の `ai/docs/`、ディレクトリ固定の `.gitkeep`
- **追跡しない**: `ai/` の `in` `work` `out` `records`、`_noai/`、`resources/` `resources_p/` `repos/`、成果物のバイナリ。`room` が必須とする行は `**/_noai/` だけ
- **既存の works**（旧方式: `**/_noai/` と `!**/ai/out/` などの行）: `room mkworks --update` で雛形の変更を3者マージで当てるか、雛形を手で写す。`init` は既存の `.gitignore` を上書きしない
- **すでに追跡に入っているファイル**: `.gitignore` を変えても追跡は外れない。履歴は書き換えず残し、今後の追跡だけ外す（`git rm -r --cached -q -- <パス>`。ファイルは消えない。対象は `git ls-files | grep '/ai/'` で確かめ、`ai/docs/` は残す）
- 改行は LF にする（`.gitattributes` で統一している場合、CRLF が混ざると警告が出る）
- 目安: `git check-ignore -v projects/<Project>/ai/out/x.xlsx` が `*` の行で無視される。`projects/<Project>/ai/docs/log.md` と README は無視されない

### 2.2 Area に境界の印を付ける

Area の `README.md` の frontmatter に、`boundary:` を足す。

```yaml
boundary: internal   # 例: internal（顧客データなし）、顧客を表す名前など
```

- **Area は、顧客・機密度の境界と一致させる**。顧客の違う Project は、別の Area に置く
- Project の `README.md` の frontmatter には `area: <Area>` を必ず書く

### 2.3 Project のひな形を作る

```powershell
$p = "$HOME\works\projects\<Project>"
foreach ($d in 'ai\docs','ai\in','ai\work','ai\out','ai\records','_noai\raw','_noai\map','_noai\final') {
  New-Item -ItemType Directory -Force "$p\$d" | Out-Null
}
foreach ($d in 'in','work','records') { New-Item -ItemType File "$p\ai\$d\.gitkeep" -Force | Out-Null }
```

| フォルダ | 役割 | 部屋から |
|---|---|---|
| `ai/docs/` | 作業ログ・決定（AI が書く） | 読み書き |
| `ai/in/` | マスク済みの入力 | 読み取り専用にする |
| `ai/work/` | AI のスクリプト（再現に要るので追跡する） | 読み書き |
| `ai/out/` | 成果物（マスク済み） | 読み書き |
| `ai/records/` | 実行記録、AI への指示の記録 | 読み書き |
| `_noai/raw` `map` `final` | 原本、対応表、実データ入りの成果物 | **見えない** |
| `_noai/user/` | 人だけの仮置き（予約名。`room` は触らない） | **見えない** |

- **`_noai/` は `type` に関係なく `raw/` `map/` `final/` `user/` を作る**（`room.py` を使うなら自動。上の `mkdir` の一覧）。マスクと復元は状態で決まる（原本が `raw/` にあればマスクし、対応表ができたら終了時に復元する）。仕様の正本は `workflow-kit/room/README.md` の「マスクと復元は状態で決まる」。マスクした資料を要約させる手順は [[ai-room-mask-summary]]
- 既存の Project がある場合は、`docs/` の中身を `ai/docs/` に、成果物を `ai/out/` に、ファイル単位の `git mv` で移す（ディレクトリごとだと `Permission denied` で失敗することがある）。README の中の旧パスは、`grep` で探して直す。過去の作業記録の中の旧パスは、当時の事実なので直さない
- 完了の目安: `_noai/` が `git status` に出ない

## 3. 部屋を作る（Area ごとに1回）

部屋の名前は `room-<Area>`。

1. ディストリビューションを作る（ダウンロードがあり、数分かかる）

   ```powershell
   wsl --install Ubuntu-26.04 --name room-<Area> --no-launch
   wsl -l -v
   ```

   - 目安: 一覧に `room-<Area>` が出る
2. **一般ユーザーを先に作る**（root のままだと、C: をマウントできてしまう。設定ファイルより先に作る。ユーザーが無いまま既定ユーザーに指定すると、起動できなくなる）

   ```powershell
   wsl -d room-<Area> -u root -- sh -c "useradd -m -u 1000 -s /bin/bash ai; id ai"
   ```

3. `/etc/wsl.conf` を書く（標準入力で渡す。`echo` でシェルに渡すと、バックスラッシュが解釈される）

   ```powershell
   $conf = "[automount]`nenabled=false`nmountFsTab=false`n`n[interop]`nenabled=false`nappendWindowsPath=false`n`n[user]`ndefault=ai`n"
   $conf | wsl -d room-<Area> -u root -- tee /etc/wsl.conf
   wsl --terminate room-<Area>
   ```

   | 設定 | 意味 |
   |---|---|
   | `automount.enabled=false` | C: などをマウントしない |
   | `mountFsTab=false` | `fstab` も使わない（マウントは、作業のたびに行う） |
   | `interop.enabled=false` | Windows のプログラムを起動しない |
   | `appendWindowsPath=false` | PATH に Windows 側を入れない |
   | `[user] default=ai` | 既定を一般ユーザーにする |

4. 確かめる

   ```powershell
   wsl -d room-<Area> -- sh -c "id -un; ls /mnt/c | wc -l; command -v cmd.exe || echo no-cmd; sudo -n true 2>&1 | head -1"
   ```

   - 目安: `ai`、`0`、`no-cmd`、`sudo: a password is required`
   - `/mnt/c` というディレクトリ自体は、空のまま存在する（正常）

**判断の分かれ目**

| 場面 | 選ぶもの |
|---|---|
| 顧客・機密度が同じ Project | 同じ Area、同じ部屋 |
| 顧客が違う Project | 別の Area、別の部屋 |
| 検証・試験 | `room-<Area>` とは別の名前（例: `ai-room-test`）で作り、終わったら `wsl --unregister` |

## 4. 部屋に道具を入れ、ログインする（部屋ごとに1回）

> `room.py init` は、この章の道具に加えて、Node.js 24（Zed の Agent の `npx` 用）と、TLS 検査のあるネットワーク向けの `--ca-cert` も扱う。手作業で進めて `curl` が証明書エラー（終了コード 60）になったら、`init` を使う方が早い（[[ai-room-setup-script]] の 2 章）。

1. 道具を入れる

   ```powershell
   wsl -d room-<Area> -u root -- sh -c "apt-get update -qq && apt-get install -y -qq curl ca-certificates ripgrep git"
   ```

2. `uv` と Claude Code を、一般ユーザーで入れる

   ```powershell
   wsl -d room-<Area> -- bash -lc 'curl -LsSf https://astral.sh/uv/install.sh | sh'
   wsl -d room-<Area> -- bash -lc 'curl -fsSL https://claude.ai/install.sh | bash'
   ```

   - 配布元のスクリプトをそのまま実行する。内容を確認してから実行したい場合は、いったんファイルに保存して中身を読む
3. PATH を通す（新しいシェルで有効）

   ```powershell
   'export PATH="$HOME/.local/bin:$PATH"' | wsl -d room-<Area> -- tee -a /home/ai/.bashrc
   wsl -d room-<Area> -- bash -ic 'claude --version; uv --version; rg --version | head -1'
   ```

4. ログインする（**人の操作**）

   ```powershell
   wsl -d room-<Area>
   ```
   ```bash
   claude
   ```

   - 表示される URL を、Windows のブラウザで開いてログインし、表示されたコードを貼り付ける。`interop` を切っているので、ブラウザは自動では開かない（正常）
   - 終わったら `/exit`
   - 認証情報は、部屋のホーム（`/home/ai/.claude/`）だけにあり、works には出ない
5. 完了の目安

   ```powershell
   wsl -d room-<Area> -- bash -ic 'cd ~ && claude -p "Reply with exactly: ok"'
   ```

   - `ok` が返る

## 5. Project を部屋で使う（作業のたびに）

`room.py start <Project>` が、下の 1〜6 を行う（チェック、README の写し、マウント、AI の起動、アンマウント、回収の一覧。コミットは `--commit` のときだけ）。使い方は `workflow-kit/room/README.md`。以下は、何をしているかの説明を兼ねた、手作業の手順。

1. **チェック**（人が確認する）
   - Project の `README.md` の `area:` が、部屋の名前の `<Area>` と一致している
   - Area の `README.md` に `boundary:` がある
   - `ai/in/` に、他の Project や Area から持ってきたファイルが混ざっていない
2. README の写しを、部屋用に置く（AI が完了条件を読めるように。派生物なので、毎回上書きする）

   ```powershell
   $p = "$HOME\works\projects\<Project>"
   New-Item -ItemType Directory -Force "$p\ai\ctx" | Out-Null
   Copy-Item "$p\README.md" "$p\ai\ctx\README.md" -Force
   (Get-Item "$p\ai\ctx\README.md").IsReadOnly = $true
   ```

3. `ai/` だけをマウントする（root で行う。**他の Project がマウントされていないことを確認してから**）

   ```powershell
   $win = "$HOME\works\projects\<Project>\ai"
   $mp  = "/mnt/room/<Project>"
   wsl -d room-<Area> -u root -- sh -c "grep -c ' /mnt/room/' /proc/mounts"
   wsl -d room-<Area> -u root -- sh -c "mkdir -p $mp && mount -t drvfs -o metadata,uid=1000,gid=1000 '$win' $mp"
   wsl -d room-<Area> -- sh -c "ls $mp; ls /mnt/c | wc -l"
   ```

   - 目安: `ai/` の中身（`docs` `in` `out` `records` `work` `ctx`）だけが見え、`/mnt/c` は空
   - 入力を読み取り専用にする: `wsl -d room-<Area> -- sh -c "find $mp/in -type f -exec chmod a-w {} +"`（ファイル単位。Windows 側でも読み取り専用の属性になる。ディレクトリへの `chmod` は未確認（**要確認**））
   - **よく忘れる点**: `-o` は、デバイス名（Windows のパス）の前に書く。後ろに書くと失敗する
4. 部屋で AI を使う

   ```powershell
   wsl -d room-<Area> -- bash -ic "cd /mnt/room/<Project> && claude"
   ```

   - 非対話で使うとき（`claude -p`）は、許可するツールを `--allowedTools` で指定する。許可されていないコマンドは実行されない
   - AI への指示は、`ai/records/` に書いておくと、再現できる（例: `claude -p 'records/<指示>.md の指示に従って…'`）
5. 回収を確認する（成果物は、Windows 側にそのまま現れる）

   ```powershell
   git -C $HOME\works status --short
   ```

   - `ai/out/` の新しいファイルは、`git status` に出ない（許可リスト方式。回収の報告に `ai/out` のファイル数が出る）
   - `~$*`（Excel のオーナーファイル）は、`ai/` に出ても、git に出ない
6. 後片付け（**マウントを必ず外し、マウント点のディレクトリも消す**）

   ```powershell
   wsl -d room-<Area> -u root -- sh -c "umount /mnt/room/<Project> && rmdir /mnt/room/<Project>"
   Start-Sleep 3
   wsl -d room-<Area> -u root -- sh -c "grep -c ' /mnt/room/' /proc/mounts; ls /mnt/room | wc -l"
   ```

   - 目安: `0`、`0`
   - **よく忘れる点**: `rmdir` を忘れると、空のマウント点に Project 名が残り、別の Project の作業中に AI の `ls` で見える。アンマウント直後は、数秒待ってから確認する（直後だと、マウントが1つ残って見えることがある）
   - **PowerShell から `sh` に複数行を標準入力で渡さない**（改行が CRLF になり、`umount` が失敗して、マウントが積み重なる）。1行ずつ `-c` で渡す
7. 変更を確認して、works にコミットする（コミットの規則は works の `AGENTS.md` に従う）。`ai/ctx/` は追跡されない

## 6. Zed から使う

初回は、次の手順で開く。

1. Zed を一度完全に終了し、起動する
2. `Ctrl+Shift+P` で、`projects: open remote` を実行する
3. WSL の項目を選び、ディストリビューションは **`room-<Area>`**（普段使いの環境ではない）を選ぶ
   - 初回は、Zed のサーバーが部屋に自動で入る（ネットワークが要る）
4. フォルダは、`/mnt/room/<Project>`（5 章でマウントしたもの）を指定する
5. Agent パネルで、新しいスレッドの種類に Claude を選ぶ
6. 確認する
   - 目安: ウィンドウに WSL の接続が表示され、ファイルツリーに `docs` `in` `out` `records` `work` だけが見える。ターミナルのプロンプトが、`ai@...:/mnt/room/<Project>$` になる
   - 部屋の中で確認する

     ```powershell
     wsl -d room-<Area> -- sh -c "ps -eo pid,user,args | grep -E 'zed|claude' | grep -v grep | cut -c1-120"
     ```

     `zed-remote-server` と Claude のプロセスが、ユーザー `ai` で動いている
- **やってはいけないこと**: 機密を扱う Project を、Zed で**ローカルのフォルダとして**開かない。Agent も Windows 側で動き、works 全体が見える状態に戻るため
- 入力（`in/`）の保存は、`Permission denied` になる（読み取り専用にしたため。正常）

## 7. Project を閉じる

判断を部屋の AI が、副作用を人が（`room.py close <Project>` が）行う。`room.py close` は、下の 2 の 1〜7 のうち、README の更新、Area への転記と一覧の更新、実行記録、`archives/` への移動を行う（1 の AI の判断で `ai/out/close.md` ができていることが前提）。以下は、何をしているかの説明を兼ねた、手作業の手順。

1. **部屋の AI が判断する**（5 章のようにマウントして行う）: 完了条件の確認、暫定の見直し、未解決の振り分け（Area に渡す【案件】、破棄）、ナレッジ化の候補（【汎用】の一覧）、`docs/log.md` の更新。結果は `ai/out/close.md` に書かせる。指示は `ai/records/` に残す
2. **人が副作用を行う**
   1. Project の `README.md` の frontmatter を `status: done`、`closed: <日付>`、`reap_after: <日付>`（既定は14日後）にする。完了条件の結果を1段落で足す
   2. 【案件】を、Area の `ai/docs/inbox.md` に追記する（Project 名と連番の識別子つき）。Area の `README.md` の一覧を「完了した Project」に移す
   3. 実行記録を、`ai/records/` に残す
   4. **アンマウント**し、マウント点を消し、`ai/ctx/` を消す（5 章の後片付け）
   5. 新しいファイルをステージする（`git add -A <Project>`）。そうしないと、追跡されていない成果物が `archives/` に移らない
   6. `archives/<Project>/` に、**ファイル単位で** `git mv` する（`git ls-files` を回す）。追跡しない `_noai/` は、ディレクトリごと移す
   7. 空になった `projects/<Project>/` を消し、コミットする
- **よく忘れる点**: アンマウントの前に移動すると、`Permission denied` で失敗する
- 完了の目安: `projects/<Project>/` が無く、`archives/<Project>/` に `ai/` と `_noai/` がある。Area の `inbox.md` に項目がある
- 部屋の会話履歴（`~/.claude/projects/-mnt-room-<Project>/`）は、やり直しの余地として残す。`reap_after` を過ぎたら、履歴を `ai/records/` に写して消す（手順は未整備。付録）

## 8. 任意設定

| 設定 | 内容 | 状態 |
|---|---|---|
| works 側の許可設定 | works の `.claude/settings.json` で、`projects/` `areas/` `archives/` を `Read` と `Edit` の deny にする。works 側の AI が、うっかり読むのを防ぐ安全網。境界の保証は部屋が担う（`grep -r` やスクリプトは止まらない） | **未導入**。Windows ネイティブで、絶対パスの deny が効くかは要確認 |
| ネットワークの絞り込み | 部屋から出られる先を、必要なサイトだけにする | 未検証 |
| Codex・Copilot | 部屋の中に導入すれば、同じ境界が効く。規約は `AGENTS.md` を正本に、`CLAUDE.md` は `@AGENTS.md` の1行にする | 未検証。エディタ内蔵の Copilot は部屋の外で動くので、機密を扱う Project では使わない |
| Python のバージョン固定 | 部屋の Python も、`room/.python-version` の版を `uv python install <バージョン>` で入れて固定する（`python3` で呼べる形にする方法は実機で確認する。`decisions.md` 2026-10-29） | 案あり（`room init` の段は未実装） |

## 9. 戻し方・片付け

- 部屋を消す: `wsl --unregister room-<Area>`（部屋の中の履歴と認証情報も消える。**消す前に、必要な履歴を `ai/records/` に写す**）
- 他の部屋・普段使いの環境（例: `Ubuntu-24.04`）には影響しない
- works 側の変更（`.gitignore`、`boundary:`）は、通常の git で戻せる

## 10. うまくいかないとき

| 症状 | 確認すること |
|---|---|
| `curl` が「SSL certificate problem」（終了コード 60）で止まる（4 章） | TLS 検査のあるネットワークで、検査用のルート証明書が部屋に無い。または、Windows の `WSLENV` 経由で、壊れた `SSL_CERT_FILE` が残っている | `room.py init --resume --ca-cert <ファイル>`。手作業なら、証明書を `/usr/local/share/ca-certificates/` に root で置き、`update-ca-certificates` を実行する（[[ai-room-setup-script]] の 9 章） |
| 部屋に入るたびに「failed to translate」が出る | `WSLENV` の `/p` 付きのパスが、`/mnt/c` の無い部屋で変換できない（無害） | `room.py shell <Area>` で入る |
| 部屋が起動しない | `wsl.conf` の `[user] default=` のユーザーが、存在するか（`wsl -d room-<Area> -u root -- id ai`） |
| `/mnt/c` が空でない | `wsl.conf` の `automount.enabled` と、`wsl --terminate` をしたか |
| 部屋に C: が見える | root で実行していないか。既定ユーザーが `ai` か |
| `mount` が「オプションを解釈できない」で失敗する | `-o` が、デバイス名の前にあるか |
| `umount` が「マウント点が指定されていない」で失敗し、マウントが積み重なる | 標準入力で渡して、改行が CRLF になっていないか。`for i in 1 2 3; do umount <マウント点>; done` で片付ける |
| 成果物がコミットに入らない | 許可リスト方式なので、`ai/` の `in` `work` `out` `records` は追跡しない仕様（2.1）。残したい文書は `ai/docs/` か `docs/` に置く |
| `ai/in/` に書けない | 仕様（読み取り専用）。変更は `work/` か `out/` に書く |
| Zed で、works 全体が見える | ローカルのフォルダとして開いていないか。WSL リモートで開く |
| Excel で開いているファイルを上書きできない | Excel の共有ロック。Excel を閉じてから行う |
| `rg` が何も検索しない | `rg <pattern> .` と、パスを書く |
| 処理が遅い | 小さいファイルが多い処理は、マウント上で遅い。大量の一時ファイルは、部屋のローカル（`~/tmp/`）に置く |
| `Remove-Item` が「保護されたパス」で止まる（PowerShell） | 空のディレクトリは `[IO.Directory]::Delete(<パス>)` で消す |

## 付録: 課題（未了・要確認）

- **`room.py` の残り**: マスク・復元、【汎用】の下書きの回収、reap、部屋の作成の自動化（`workflow-kit/room/README.md` の「未実装」）。実運用で安定したら、5・7 章を、スクリプトの呼び出しに差し替える
- workflow-kit の手順書（`start` `wrap`。`open` `close` は 2026-10-24 までに `room` のコマンドに移った）が、`docs/` を Project 直下と想定している。`ai/docs/` への読み替えと、部屋の中の AI が行う部分・人が行う部分の分担を、手順書に書く
- workflow-kit の works の雛形（`gitignore.template`、`AGENTS.md`）への反映（2.1 の `.gitignore`、AI は部屋で使うこと、Zed は WSL リモートで使うこと、AI が書くスクリプトに標準ライブラリと同名を付けないこと）
- マスク・復元（`mask.toml`、zip レベルの置換、置換後の点検）は、ダミーデータでの試験が未了
- 部屋の会話履歴の片付け（reap）の手順と、期限の設定の置き場
- 対応表の保護（works が漏れた場合の対策）は、運用しながら決める
- docx・pptx のマスク、ネットワークの絞り込みは、未検証。Bedrock 経由の接続は、Zed の Agent で通した（2026-10-19、PC1）。手順は [[ai-room-setup-script]] の 2.1。`aws-key` の実機確認は未了
