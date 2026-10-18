---
type: howto
title: AI 作業部屋 実例（スクリプト版 room.py）
tags:
  - setup
  - security
  - tool/wsl
  - ai/claude
  - windows
---

# AI 作業部屋 実例（スクリプト版 `room.py`）

`room.py` で、AI 作業部屋の作成から、Project の作業、`close`、片付けまでを、実際の名前（Area `pilot2`、部屋 `room-pilot2`、Project `pilot2-1`）で1手ずつ通す手順書。2026-10-18 に、この流れで実機を通した。仕組みと理由は [[ai-room-why]]、手順の説明（プレースホルダー版）は [[ai-room-setup]]、手作業で同じことをする実例は [[ai-room-setup-manual]]。

- **ゴール（完了の目安）**: 部屋の中の Claude Code が、`/mnt/room/pilot2-1`（Project の `ai/`）だけを読み書きでき、成果物が works に現れる。`close` で `archives/pilot2-1/` に移り、会話履歴を `reap` で消せる
- **実名について**: `pilot2` `pilot2-1` `pilot2-2` は試験用の名前。自分の Area と Project の名前に置き換えて読む。名前は英数字・`_`・`-` だけにする（`reap` が止まるため）
- パスは `$HOME` で書く。固有情報（会社名、顧客名）は書かない

## 対応バージョン表

手順の確認日: 2026-10-18（実機）。Windows、WSL、Claude Code、uv、Zed のバージョンは、[[ai-room-setup]] の「対応バージョン表」を正とする（ここには書かない）。部屋のベースは Ubuntu 24.04（`room.py` の `ROOM_BASE`）。

## 全体の流れ

| 章 | 内容 | 区分 | 完了の目安 |
|---|---|---|---|
| 1 | 前提を確認する | 手動 | `.gitignore`、`uv`、WSL2 がそろう |
| 2 | 部屋を作る（`init`） | スクリプト + ログインは人 | 部屋が `claude -p` に `ok` を返す |
| 3 | Project を作る（`open`） | スクリプト + README は人 | `projects/pilot2-1/` ができ、README を書いた |
| 4 | マスクする（`mask`。任意） | スクリプト | `ai/in/` にマスク済みのファイルが入る |
| 5 | 部屋で使う（`start`） | スクリプト | 成果物が `ai/out/` に現れ、マウントが残らない |
| 6 | 回収する（`restore` `readme` `stock`） | スクリプト | 実名に戻った成果物が `_noai/final/` にある |
| 7 | 閉じる（`close`） | スクリプト + `close.md` は部屋の AI | `archives/pilot2-1/` に移った |
| 8 | 片付ける（`reap`、部屋の削除） | スクリプト | 会話履歴が消え、README に `reaped:` が付く |
| 9 | うまくいかないとき | | |

## 1. 前提を確認する

1. WSL2 が使える（`wsl -l -v` の `VERSION` が `2`）。部屋のベースの `Ubuntu-24.04` がある（無ければ `init` が `wsl --install` で入れる）
2. Claude のアカウントがある（部屋の Claude Code は、ブラウザ認証でログインする）
3. works の `.gitignore` に、次の4行がある

   ```powershell
   Select-String -Path $HOME\works\.gitignore -Pattern '_noai|~\$|!\*\*/ai/out|ai/ctx'
   ```

   - 無ければ足す: `**/_noai/`、`~$*`、`!**/ai/out/`、`**/ai/ctx/`（理由は [[ai-room-setup]] の 2.1）
4. `room.py` の置き場で、以降のコマンドを実行する

   ```powershell
   cd $HOME\works\resources\workflow-kit\room
   uv run python -m unittest discover -s tests    # 任意。SharedPermissionTest の 2 本は、Windows では落ちる（既知）
   ```

- **よく忘れる点**: `uv run room.py ...` は、この `room` のディレクトリで実行する。works のルートでは動かない。`--vault <パス>` はサブコマンドの前に書く

## 2. 部屋を作る（`init`）

```powershell
uv run room.py init pilot2 --boundary internal
```

- `areas/pilot2/README.md` が無ければ作る（`boundary: internal`）。**印の既定値は無い**。`--boundary` を付けずに Area が無いと、止まる。顧客・機密度が同じ Project は同じ Area にする（印の決め方は [[ai-room-setup]] の 2.2）
- 部屋 `room-pilot2` を作る（`Ubuntu-24.04` のダウンロードに数分かかる）。一般ユーザー `ai` を作り、`/etc/wsl.conf`（`C:` をマウントしない、Windows のプログラムを起動しない）を書き、分離を確認し、道具（curl、ripgrep、uv、Claude Code）を入れる
- 分離の確認が `user=ai, c=0, cmd=no, sudo=no` から外れると、**道具を入れずに止まる**（想定の動作）
- 終わりに、Area の README だけを、既定でコミットする（`--no-commit` で省く）
- 途中で止まったら、同じコマンドに `--resume` を付ける（設定と道具の入れ直し）

**ログイン（人の操作）**:

```powershell
wsl -d room-pilot2
```
```bash
claude        # 表示された URL をブラウザで開いてログインし、コードを貼って /exit
```

完了の目安:

```powershell
wsl -d room-pilot2 -- bash -ic 'cd ~ && claude -p "Reply with exactly: ok"'    # ok
wsl -d room-pilot2 -- sh -c "id -un; ls /mnt/c | wc -l; command -v cmd.exe || echo no-cmd"    # ai、0、no-cmd
```

## 3. Project を作る（`open`）

```powershell
uv run room.py open pilot2-1 --area pilot2 --type doc
```

- `projects/pilot2-1/` に、`README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final}` ができ、Area の README の「進行中の Project」に1行足される。`ai/ctx/` は `start` が作る
- 初期状態を、既定でコミットする（`--no-commit` で省く）。コミットされるのは、Project のひな形と、Area の README だけ（Area のほかのファイルは含めない）
- **README の本文を書く**（目的、完了条件、成果物、範囲外）。ひな形のままだと、`close` が通ってしまい、【案件】に「ひな形のまま」と出る

```powershell
notepad $HOME\works\projects\pilot2-1\README.md
git -C $HOME\works status --short      # _noai/ が出ない
```

- **よく忘れる点**: ステージ済みの別の変更（前の `close` の取り残しなど）があっても、`init` `open` は止まらず、対象のパスだけをコミットする。取り残しはステージに残るので、あとで別にコミットする（「注意: 対象外のステージ済みの変更は、コミットに含めない」と出る）。`start` `readme` `close` の `--commit` は、対象外のステージがあると止まる

## 4. マスクする（`mask`。任意）

原本（Excel、CSV）を AI に見せず、置き換えた写しだけを渡すとき。ここでは、試験用の `pilot2-2` を使う。

```powershell
uv run room.py open pilot2-2 --area pilot2 --type doc
python tests/dummy_fixture.py $HOME\works\projects\pilot2-2     # _noai/raw/ にダミーの xlsx と csv、_noai/mask.toml
uv run room.py mask pilot2-2
Get-ChildItem $HOME\works\projects\pilot2-2\ai\in               # マスク済みの xlsx と csv
```

- 実際の運用では、`_noai/raw/` に原本を置き、`_noai/mask.toml` に語の表（`[terms.<種類>] キー = ["正式名", "表記ゆれ"]`、`[columns] "シート!列名" = "種類"`）を書く
- **辞書にない名前は、置き換わらない**。ダミーの CSV の担当「山田」が実例で、部屋の AI が気づいて報告した。列で指定する仕組みは `[columns]`
- 語が残っていれば止まる。`start` の最初にも、自動で行う

## 5. 部屋で使う（`start`）

**A. 端末で使う（既定）**:

```powershell
uv run room.py start pilot2-1
```

1. チェック（Project と Area の `area:`、`boundary:`、ほかのマウントが無いこと、`ai/in/` の来歴）→ README の写しを `ai/ctx/` に置く → 共有知を部屋の `~/shared` に送る
2. `ai/` を `/mnt/room/pilot2-1` にマウントし（`in/` は読み取り専用）、部屋で `claude` を起動する
3. 部屋の `claude` に作業を頼む（例: 「`ai/out/hello.md` を作って」）。`/exit` で戻る
4. 自動で、アンマウント、マウント点の削除、復元（`restore`）、変更の一覧が出る

- 目安: 「回収: 変更 N 件」の下に、`ai/out/` の新しいファイルが `??` で出る
- 信頼の確認（`Quick safety check: Is this a project you trust?`）が、新しい Project の最初に出る。内容を確認して進める

**B. Zed の WSL リモートで使う（`--no-launch`）**:

```powershell
uv run room.py start pilot2-1 --no-launch
```

1. 「マウントした」「終わったら Enter」が出るまで待つ（マウントしたまま待つ）
2. Zed を起動し、`Ctrl+Shift+P` → `projects: open remote` → WSL の `room-pilot2` を選ぶ
3. フォルダは、**部屋の中のパス** `/mnt/room/pilot2-1` を入力する（Windows のフォルダを選ばない）
4. 部屋の側で動いていることを確認する
   - ウィンドウに `WSL: room-pilot2` と出る。ターミナルのプロンプトが `ai@...:/mnt/room/pilot2-1$`
   - Agent に `uname -a; pwd; echo $SHELL` を実行させる → `Linux`、`/mnt/room/pilot2-1`、`/bin/bash`
5. 作業が終わったら、**Zed のウィンドウを閉じてから**、`start` の端末で Enter を押す（アンマウント、復元、回収に進む）

- **やってはいけないこと**: Windows のフォルダを、ローカルのプロジェクトとして Zed で開かない。Agent が Windows 側で動き（パスが `C:\...`、シェルが PowerShell になる）、works 全体が見える状態に戻る。手元の Windows 側の `claude-acp` が `projects\pilot2-1\ai` を掴むと、`close` のあとの削除が `being used` で失敗する
- **よく忘れる点**: Enter で戻らないときは、別の PowerShell で `wsl --terminate room-pilot2` を実行すると進む（2026-10-18 に `room.py` を直した。再発したら記録する）

## 6. 回収する（`restore` `readme` `stock`）

`start` の終わりに、`restore` が自動で動く。

- 成果物の中のプレースホルダー（`⟦CUST_001⟧` など）を、対応表で実名に戻し、`_noai/final/` に書く（実名入りなので、works のコミットの対象外）
- **止まる場合**: 戻らないプレースホルダー、未知の形式があると、何も書かずに一覧を出して止まる。AI が本文に `⟦CUST_nnn⟧` のような**書式の説明**を書いたときも止まる（番号が無いため）。直して、`uv run room.py restore pilot2-2` を再実行する
- `_noai/final/` を人が直したあとは、次の復元が止まる（`--force` で上書き。前回の書き出しのハッシュで判定。**この動作は未確認**）

```powershell
uv run room.py restore pilot2-2
uv run room.py readme pilot2-2          # 部屋の AI が書いた ai/out/readme-draft.md を README の本文に反映（確認あり）
uv run room.py stock pilot2-2           # ai/out/stock/ の【汎用】の下書きを、1件ずつ確認して resources/exmem/inbox/ に運ぶ
```

- `stock` の運び先は `resources/exmem/inbox/`（**公開リポジトリ**）。対応表の語を含む下書きは運ばれない。運んだメモは、未追跡のまま残る（コミットしない方針）
- Excel の成果物は、`_noai/final/` のファイルを Excel で開き、ピボットは「すべて更新」を押す。シート名・値・コメントが実名に戻っているか確認する

## 7. 閉じる（`close`）

1. 部屋の AI に、`ai/out/close.md` を書かせる（`room start` で入り、完了条件の確認、暫定の見直し、未解決の振り分け、【案件】の行、【汎用】候補を書かせる。書き方は `workflow-kit/room-context.md`）。`close.md` が無いと、`close` は止まる
2. マウントが無いことを確かめる

   ```powershell
   wsl -d room-pilot2 -u root -- sh -c "grep -c ' /mnt/room/' /proc/mounts"     # 0
   ```

3. 実行する

   ```powershell
   uv run room.py close pilot2-1
   ```

- Area の `ai/docs/inbox.md` に、【案件】が追記される（Project 名と連番の識別子つき。重複しない）。README が `status: done`、`closed`、`reap_after`（既定 14 日後）になり、Area の一覧が「完了した Project」に移り、`archives/pilot2-1/` に移る（追跡外の `_noai/` も）
- 完了の目安

  ```powershell
  Test-Path $HOME\works\projects\pilot2-1                                   # False
  Get-ChildItem $HOME\works\archives\pilot2-1 -Force | Select-Object Name   # ai、_noai、README.md
  Get-Content $HOME\works\areas\pilot2\ai\docs\inbox.md                     # 【案件】
  ```

- コミットは、`--commit` を付けたときだけ。付けなければ、作業ツリーに残る（`git status` を見て、意図してコミットする）

## 8. 片付ける（`reap`、部屋の削除）

- `reap`: `close` から期限（`reap_after`）が来た Project の、部屋の会話履歴（`~/.claude/projects/-mnt-room-pilot2-1/`）と `~/tmp/pilot2-1` を消し、README に `reaped: <日付>` を付ける。期限前は `--force`

  ```powershell
  uv run room.py reap pilot2-1 --force       # 確認に y
  wsl -d room-pilot2 -- sh -c 'ls ~/.claude/projects/'     # -mnt-room-pilot2-1 が消える
  Get-Content $HOME\works\archives\pilot2-1\README.md -TotalCount 12   # reaped:
  ```

- 部屋ごと消す: `wsl --unregister room-pilot2`（部屋の中の履歴と認証情報も消える。必要な履歴は先に `ai/records/` に写す）。ベースの `Ubuntu-24.04` には影響しない
- **よく忘れる点**: Zed を `/home/ai` で開いて使った履歴は、`-home-ai` に残り、どの Project にも属さないので `reap` では消えない

## 9. うまくいかないとき

| 症状 | 原因 | 対処 |
|---|---|---|
| `Area が無い: areas/...` | `init` の引数が Area 名でない（部屋の名前 `room-...` を渡した）、または Area が無い | 引数は Area 名（`pilot2`）。`room-` は付けない。Area が無ければ `--boundary` を付ける |
| `部屋がすでにある` | 同じ名前の部屋がある | 作りかけなら `--resume`。作り直すなら `wsl --unregister` |
| `start --no-launch` で Enter で戻らない | 待ちの `input()` に Enter が届かない（コンソールの共有。`d6c97d8` で直した） | `wsl --terminate room-pilot2`。再発したら記録する |
| `復元を止めた … 壊れたプレースホルダー` | AI が `⟦CUST_nnn⟧` のような説明を本文に書いた | `ai/out/` のその文を、記号を含まない表現に直し、`restore` を再実行する |
| `reap` が `消せなかった（）` | 古い `room.py` のバグ（`086381c` で直した） | 最新の `room.py` を使う |
| `Remove-Item` が `being used` | Windows 側の Zed の Agent などが、`projects\<名>\ai` を掴んでいる | Zed のウィンドウを閉じ、`claude-acp` のプロセスを終了する |
| `close --commit` / `start --commit` が「対象外のファイルがステージされている」で止まる | ステージ済みの別の変更がある | 先にそれをコミットするか、`git restore --staged <パス>` で戻す（`init` `open` は止まらない。3 章） |
| マウントが残る | `start` が途中で止まった | `uv run room.py umount --area pilot2`。残れば `wsl --terminate room-pilot2` |
