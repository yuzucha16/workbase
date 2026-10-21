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

手順の確認日: 2026-10-18（実機。2.1 の Bedrock と `--ca-cert`・Node・`shell` は 2026-10-19、PC1 で一部を確認し、`aws-key` と `shell` は未確認）。Windows、WSL、Claude Code、uv、Zed のバージョンは、[[ai-room-setup]] の「対応バージョン表」を正とする（ここには書かない）。部屋のベースは Ubuntu 26.04（2026-10-19 に 24.04 から変更。実機で確認済み: 2026-10-19）（`room.py` の `ROOM_BASE`）。

## 全体の流れ

| 章 | 内容 | 区分 | 完了の目安 |
|---|---|---|---|
| 1 | 前提を確認する | 手動 | `.gitignore`、`uv`、WSL2 がそろう |
| 2 | 部屋を作る（`init`） | スクリプト + ログインは人 | 部屋が `claude -p` に `ok` を返す |
| 3 | Project を作る（`open`） | スクリプト + README は人 | `projects/pilot2-1/` ができ、README を書いた |
| 4 | マスクする（`mask`。任意）。4.1: Area の知識を取り出す（`pull`） | スクリプト | `ai/in/` にマスク済みのファイルが入る（4.1: `ai/in/area/`） |
| 5 | 部屋で使う（`start`） | スクリプト | 成果物が `ai/out/` に現れ、マウントが残らない |
| 6 | 回収する（`restore` `readme` `stock`）。6.1: 統合した知識を Area に戻す | スクリプト | 実名に戻った成果物が `_noai/final/` にある（6.1: Area の `knowledge/` にも） |
| 7 | 閉じる（`close`） | スクリプト + `close.md` は部屋の AI | `archives/pilot2-1/` に移った |
| 8 | 片付ける（`reap`、部屋の削除） | スクリプト | 会話履歴が消え、README に `reaped:` が付く |
| 9 | うまくいかないとき | | |

## 1. 前提を確認する

1. WSL2 が使える（`wsl -l -v` の `VERSION` が `2`）。部屋のベースの `Ubuntu-26.04` がある（無ければ `init` が `wsl --install` で入れる）
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
- 部屋 `room-pilot2` を作る（`Ubuntu-26.04` のダウンロードに数分かかる）。一般ユーザー `ai` を作り、`/etc/wsl.conf`（`C:` をマウントしない、Windows のプログラムを起動しない）を書き、分離を確認し、道具（curl、ripgrep、Node.js 24、uv、Claude Code）を入れる。Node は、Zed の Agent（`npx` で起動する）が 22 以上を要るため、公式の tarball をチェックサム確認つきで `/usr/local` に入れる（apt の版は 18 で足りない）。npm の `cafile` は、システムの証明書バンドルに向ける
- 分離の確認が `user=ai, c=0, cmd=no, sudo=no` から外れると、**道具を入れずに止まる**（想定の動作）
- 終わりに、Area の README だけを、既定でコミットする（`--no-commit` で省く）
- 途中で止まったら、同じコマンドに `--resume` を付ける（設定と道具の入れ直し）
- **TLS 検査のあるネットワーク（会社など）では、`--ca-cert` を付ける**: `curl` が「SSL certificate problem（終了コード 60）」で止まるときの対処。会社のルート証明書（PEM、5枚まで。秘密鍵が混ざると止まる）を指定すると、apt の後・uv の前に、root が `/usr/local/share/ca-certificates/` へ入れる。入れる前に SHA-256 を表示する。`ai` は読めるが書き換えられない。指定しなければ入れない。証明書は、このリポジトリに置かない（公開のため）

  ```powershell
  uv run room.py init pilot2 --resume --ca-cert <証明書ファイル>.crt
  ```
- `room.py` は、`wsl.exe` に `WSLENV` を渡さない。Windows の `WSLENV` に `/p` 付きの証明書パスがあると、`/mnt/c` を切った部屋では変換できず、壊れた `SSL_CERT_FILE` などが残って、curl が証明書エラーになる（実機で確認: 2026-10-19）

**ログイン（人の操作）**:

```powershell
uv run room.py shell pilot2    # wsl -d room-pilot2 の代わり
```
```bash
claude        # 表示された URL をブラウザで開いてログインし、コードを貼って /exit
```

`shell` は、`WSLENV` を外して部屋に入る。素の `wsl -d room-pilot2` だと、Windows の `WSLENV` に `/p` 付きのパスがあるとき、入るたびに「failed to translate」が出る（動作には影響しない）。

完了の目安:

```powershell
wsl -d room-pilot2 -- bash -ic 'cd ~ && claude -p "Reply with exactly: ok"'    # ok
wsl -d room-pilot2 -- sh -c "id -un; ls /mnt/c | wc -l; command -v cmd.exe || echo no-cmd"    # ai、0、no-cmd
```

### 2.1 Bedrock を使うとき（任意）

部屋の Claude Code を、Anthropic のログインでなく Amazon Bedrock につなぐ。AWS CLI は要らない（IAM ユーザーのアクセスキーを、環境変数かファイルで渡せば足りる）。

1. **Bedrock の設定は、Zed の設定の `agent_servers` の `env` に書く**。秘密を含まない値だけ（`CLAUDE_CODE_USE_BEDROCK`、`AWS_REGION`、`AWS_PROFILE`、モデルの ID、`AWS_CA_BUNDLE` と `NODE_EXTRA_CA_CERTS`（`/etc/ssl/certs/ca-certificates.crt`。TLS 検査のあるネットワークで、Node が会社のルート証明書を見るため））。エージェントは `command: npx`、`args: ["-y", "@agentclientprotocol/claude-agent-acp"]` の custom で定義する（実機で接続を確認: 2026-10-19）
2. **アクセスキーは、部屋の `~/.aws/credentials` に、プロファイルとして置く**:

   ```powershell
   uv run room.py aws-key pilot2 --profile <プロファイル名>
   ```

   アクセスキー ID は入力、秘密キーと `AWS_SESSION_TOKEN`（一時キーのときだけ）は画面に出さずに受け取り、標準入力で部屋へ渡す（コマンドラインにも履歴にも残さない）。同名の節だけを置き換え、権限は 600。**この手順の実機確認は未了**（次項）
3. `agent_servers` の `env` の `AWS_PROFILE` に、同じプロファイル名を書く。Zed を部屋に繋ぎ直して、Agent に話しかける

- **なぜ、シェルの `export` では Zed の Agent に届かないか**: 環境変数は、プロセスを作るときに親から子へコピーされるだけ。手で `export` した値は、その `bash` と、そこから起動した `claude` にだけある。Zed の Agent は、Windows の Zed が `wsl.exe` で部屋の `zed-remote-server` を起動し、そのサーバーが起動するので、その `bash` は祖先にいない。Zed の `env` に書いた値は、Zed が直接渡すので届く。秘密（アクセスキー）は、設定ファイルに書かず、`~/.aws/credentials` で渡す（SDK がファイルを読むので、起動のしかたに関係しない）
- **やってはいけないこと**: 長期のアクセスキーを、git 管理のファイル（dotfiles の Zed の設定を含む）やチャットに書かない。`op`（1Password CLI）を部屋に持ち込まない（[[ai-room-why]]）
- **よく忘れる点**: `~/.aws/credentials` は、AI から読める場所にある。IAM ユーザーには Bedrock の権限（`bedrock:InvokeModel*`、`ListInferenceProfiles`、`GetInferenceProfile`）だけを付け、予算アラートを置く。長期キーを部屋に置きたくなければ、Windows 側で一時キー（`aws sts get-session-token`）を作り、`AWS_SESSION_TOKEN` つきで入れる。AWS 側の準備は [[bedrock-first-hello]]
- 未解決（2026-10-19）: `aws-key` の `touch ~/.aws/credentials` が、`ai` で失敗した（原因は未特定。`~/.aws` の所有者が root だった可能性は、本人が取り下げた）。手で `~/.aws/credentials` を書けば、Zed の認証は通る

## 3. Project を作る（`open`）

```powershell
uv run room.py open pilot2-1 --area pilot2 --type doc
```

- `--data none|mask|restore` で、データの扱いを決める（省略は `none`。2026-10-19）。`_noai/` の中身が変わる: `none` は `user/` だけ、`mask` は `raw/` `map/` `user/`（復元しない）、`restore` は `raw/` `map/` `final/` `user/`。`user/` は人だけの仮置き（予約名）。`dev` は `none` だけが仕様。マスクだけで要約を出すときは [[ai-room-mask-summary]]。この章以降の `mask` `restore` の例は、`--data restore` で作った Project の話
- `projects/pilot2-1/` に、`README.md`、`ai/{docs,in,work,out,records}`、`_noai/`（`data:` による。以下は `restore` のとき `_noai/{raw,map,final,user}`）ができ、Area の README の「進行中の Project」に1行足される。`ai/ctx/` は `start` が作る
- 初期状態を、既定でコミットする（`--no-commit` で省く）。コミットされるのは、Project のひな形と、Area の README だけ（Area のほかのファイルは含めない）
- **README の本文を書く**（目的、完了条件、成果物、範囲外）。ひな形のままだと、`close` が通ってしまい、【案件】に「ひな形のまま」と出る

```powershell
notepad $HOME\works\projects\pilot2-1\README.md
git -C $HOME\works status --short      # _noai/ が出ない
```

- **よく忘れる点**: ステージ済みの別の変更（前の `close` の取り残しなど）があっても、`init` `open` は止まらず、対象のパスだけをコミットする。取り残しはステージに残るので、あとで別にコミットする（「注意: 対象外のステージ済みの変更は、コミットに含めない」と出る）。`start` `readme` `close` の `--commit` は、対象外のステージがあると止まる

## 4. マスクする（`mask`。任意）

原本（Excel、CSV、md、txt、pptx）を AI に見せず、置き換えた写しだけを渡すとき（`data: mask` か `restore` の Project。`none` は原本があると止まる）。ここでは、試験用の `pilot2-2` を使う。

```powershell
uv run room.py open pilot2-2 --area pilot2 --type doc --data restore
python tests/dummy_fixture.py $HOME\works\projects\pilot2-2     # _noai/raw/ にダミーの xlsx と csv、_noai/mask.toml
uv run room.py mask pilot2-2
Get-ChildItem $HOME\works\projects\pilot2-2\ai\in               # マスク済みの xlsx と csv
```

- 実際の運用では、`_noai/raw/` に原本を置き、`_noai/mask.toml` に語の表（`[terms.<種類>] キー = ["正式名", "表記ゆれ"]`、`[columns] "シート!列名" = "種類"`）を書く
- **辞書にない名前は、置き換わらない**。ダミーの CSV の担当「山田」が実例で、部屋の AI が気づいて報告した。列で指定する仕組みは `[columns]`
- 語が残っていれば止まる。`start` の最初にも、自動で行う

### 4.1 Area の知識を取り出す（`pull`。2026-10-21 追加。実機で確認済み: 2026-10-21、問題なし）

Area に溜めた知識（実名入りの会議録など）を、別の Project の部屋の AI に使わせるとき。Area の `knowledge/` から、条件に合うファイルを `_noai/raw/area/` に写し、`mask` で `ai/in/area/` にマスクした写しを作る。設計の理由は [[cross-area-shared-knowledge]]。**実名を読むので、人が実行する**（AI には実行させない）。ここでは、試験用の Project `pilot2-3` を使う（`data: restore` が前提）。

```powershell
uv run room.py open pilot2-3 --area pilot2 --type doc --data restore
```

以下の `Set-Content` は PowerShell 7（`pwsh`）で実行する。Windows PowerShell 5.1 だと UTF-8 に BOM が付き、frontmatter（先頭の `---`）と `mask.toml` を読めない。手で書くなら BOM なしの UTF-8 で保存する。

**手順1. マスクの指定を書く**（ひな形があれば上書きしてよい。試験用のダミー）:

```powershell
Set-Content -Path $HOME\works\projects\pilot2-3\_noai\mask.toml -Encoding utf8 -Value @'
[terms.CUST]
acme = ["アクメ商事株式会社", "アクメ商事"]

[terms.PERSON]
tanaka = ["田中太郎"]
'@
```

**手順2. Area に知識を置く**（ダミー。内容はすべて架空。`areas/<Area>/knowledge/` は `room init` が作る。`init` より前に作った Area は、`init <Area>` をもう一度実行すると足りない置き場だけ作る（部屋がすでにあるので止まるが、置き場は先に作られる）。下の `New-Item` は、`init` 前の Area の補い）:

```powershell
$k = "$HOME\works\areas\pilot2\knowledge"
New-Item -ItemType Directory -Force $k | Out-Null
Set-Content -Path "$k\2026-10-14-アクメ商事-定例.md" -Encoding utf8 -Value @'
---
type: area-note
kind: meeting
title: 在庫システム更新の定例
status: active
date: 2026-10-14
org:
  - アクメ商事
tags:
  - knowledge-management
created: 2026-10-14
updated: 2026-10-14
todo_open: 1
todo_due: 2026-10-21
---

# 在庫システム更新の定例

## 冒頭
- 決定: 切替は11月第2週。ToDo: 項目一覧をアクメ商事が10-21 までに出す。

## 決定
- 切替日を11月第2週にする。理由: アクメ商事の締め処理と重ならない。【案件】

## ToDo
| 内容 | 担当 | 期日 | 状態 |
|---|---|---|---|
| 移行データの項目一覧を出す | 田中太郎（アクメ商事） | 2026-10-21 | 未了 |
'@
Set-Content -Path "$k\2026-10-15-自社内の打合せ.md" -Encoding utf8 -Value "---`ntype: area-note`nkind: meeting`ntitle: 自社内の打合せ`nstatus: active`norg:`n  - 自社`n---`n`n# 自社内の打合せ`n`n自社だけの内容`n"
Set-Content -Path "$k\2026-10-01-古い定例.md" -Encoding utf8 -Value "---`ntype: area-note`nkind: meeting`ntitle: 古い定例`nstatus: superseded`norg:`n  - アクメ商事`n---`n`n# 古い定例`n`nアクメ商事の古い決定`n"
```

**手順3. 取り出す**:

```powershell
uv run room.py pull pilot2-3 --where org=アクメ商事     # 一覧を確認して y
Get-ChildItem $HOME\works\projects\pilot2-3\_noai\raw\area
```

**手順4. マスクする**:

```powershell
uv run room.py mask pilot2-3
Get-ChildItem $HOME\works\projects\pilot2-3\ai\in\area
Get-Content $HOME\works\projects\pilot2-3\ai\in\area\*.md      # ⟦CUST_001⟧、⟦PERSON_001⟧
Select-String -Path $HOME\works\projects\pilot2-3\ai\records\manifest.json -Pattern 'アクメ|田中'     # 何も出ない
```

- `--where <項目>=<値>` は、frontmatter の項目で絞る（複数指定は AND。リストの項目は要素に一致）。`status: superseded` のファイルは取り出さない（`status` が無ければ active 扱い）。`--yes` で一覧の確認を省く
- 部屋に渡るファイル名は、`<日付>-<元の相対パスのハッシュ>.md` にする（Area のファイル名は顧客名を含みうるため）。元の名前は `_noai/map/pull-sources.json`（部屋に渡らない）にある。manifest の `masked_from` にも名前は書かない
- Area の知識置き場は `areas/<Area>/knowledge/`。変えるときは Project の README の frontmatter に `knowledge_dest: <Area からの相対パス>` を書く（Area の外は拒否）
- **確認ポイント**:
  - 一覧が1件だけ（`org` 一致かつ active）。取り出した名前に `アクメ` が無い
  - `ai/in/area/` の本文と、frontmatter の `org:` の値に `アクメ` `田中` が残らない（`org:` の値の置換は、実機で確認済み: 2026-10-21。残るときは、語を足して設計を見直す）
  - `ai/records/manifest.json` に実名が無い
- **よく忘れる点**: 今回の条件に合わなくなった前回の取り出し分は、`_noai/raw/area/` に残る。手で消す。`data: mask` の Project には取り出せない（結果を Area に戻すため `restore` が要る）

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

`start` の終わりに、`restore` が自動で動く（`data: restore` のときだけ。`mask` は復元せず、`none` はマスクも復元もしない）。

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

### 6.1 統合した知識を Area に戻す（`ai/out/knowledge/`。2026-10-21 追加。実機で確認済み: 2026-10-21、問題なし）

4.1 で取り出した知識を、部屋の AI が統合し、実名に戻して Area に置く。`restore` が自動で行う（`start` の終わり）。**部屋の AI は実名を見ない**。

1. 部屋で起動し、AI に頼む:

   ```powershell
   uv run room.py start pilot2-3
   ```

   部屋の `claude` に: 「`ai/in/area/` を読み、`ai/out/knowledge/topic-cutover.md` に統合ノートを書いて。frontmatter は `kind: integrated`、`status: active`、`org` はそのまま。`⟦…⟧` の記号は変えない。ファイル名は英数字で」。`/exit` で戻る
2. 自動で `restore` が動き、`ai/out/knowledge/` の下が、実名に戻って Area に書かれる:

   ```powershell
   Get-Content $HOME\works\areas\pilot2\knowledge\topic-cutover.md      # アクメ商事株式会社、田中太郎
   Get-Content $HOME\works\projects\pilot2-3\_noai\final\knowledge\topic-cutover.md     # 同じ内容
   ```

3. **人の変更を守る停止を確かめる**（`start` をもう一度やり直す必要はない。`ai/out/` に前回の出力が残っている）:

   ```powershell
   Add-Content "$HOME\works\areas\pilot2\knowledge\topic-cutover.md" "`n人が追記した1行"     # Area 側を人が書き換える
   uv run room.py restore pilot2-3                                                          # 止まる
   ```

   「Area の知識が、前回の書き出しから変わっている（人の変更を上書きしてしまう）」と出て、何も書かずに止まる。Area のファイルは人の1行を保ったまま。確認して上書きしてよければ:

   ```powershell
   uv run room.py restore pilot2-3 --force
   Get-Content "$HOME\works\areas\pilot2\knowledge\topic-cutover.md"                          # 人の1行は消えている
   Get-Content "$HOME\works\projects\pilot2-3\_noai\final\_prev\knowledge\topic-cutover.md"   # 人の1行が残っている
   ```

   対照: 人が書き換えていないときは、止まらない（もう一度 `restore` するだけ）

- 書き出すのは、`ai/out/knowledge/` の下だけ（ほかの成果物は従来どおり `_noai/final/` にだけ書く）。書き出し先は `knowledge_dest`（既定 `areas/<Area>/knowledge/`）
- **止まる場合**: ファイル名にプレースホルダー（`⟦CUST_001⟧.md` など）が残る、置き場の外を指す名前、は何も書かずに止まる。直して `uv run room.py restore pilot2-3` を再実行する
- 前回の書き出し（`_noai/map/knowledge-manifest.json` のハッシュ）から人が変えた既存ファイルがあると、`restore` は何も書かずに止まる（`--force` で上書き。直前の版は `_noai/final/_prev/knowledge/` に退避される。2026-10-21 に、警告から止める仕様に変えた）。`start` の終わりで止まったときも、`ai/out/` は回収済みなので、直して `restore` を再実行する
- **確認ポイント**:
  - 部屋の AI が `ai/in/area/` を読める（`in/` は読み取り専用でマウントされる）。プレースホルダーを壊さない
  - Area の統合ノートに、`⟦…⟧` が残らず、実名に戻っている（`org:` の値も）
  - 人が Area 側を変えたあとの `restore` が止まり、`--force` で上書きされて、直前の版が退避される

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

- 部屋ごと消す: `wsl --unregister room-pilot2`（部屋の中の履歴と認証情報も消える。必要な履歴は先に `ai/records/` に写す）。ベースの `Ubuntu-26.04` には影響しない
- **よく忘れる点**: Zed を `/home/ai` で開いて使った履歴は、`-home-ai` に残り、どの Project にも属さないので `reap` では消えない

## 9. うまくいかないとき

| 症状 | 原因 | 対処 |
|---|---|---|
| `init` の `curl` が「SSL certificate problem」（終了コード 60）で止まる | TLS 検査のあるネットワークで、会社のルート証明書が部屋に無い。または、`WSLENV` 経由の壊れた `SSL_CERT_FILE` が残っている | `init --resume --ca-cert <ファイル>`（2 章）。`room.py` は `WSLENV` を渡さない |
| 部屋に入るたびに「failed to translate」が出る | Windows の `WSLENV` の `/p` 付きのパスが、`/mnt/c` の無い部屋で変換できない | `uv run room.py shell <Area>` で入る（動作には影響しない） |
| Zed の Agent が `npx` を知らない（PATH に無い） | 部屋に Node.js が無い（`init` の古い版は入れない） | `init --resume`（Node 24 を入れる。2 章）。入れる前の部屋には、手で入れてもよい |
| Zed の Agent で Bedrock の認証が通らない | `agent_servers` の `env` に、`AWS_PROFILE` などが無い。部屋の `~/.aws/credentials` にプロファイルが無い | 2.1 |
| `aws-key` の `touch` が失敗する | 未特定（2 章 2.1 の未解決） | `wsl -d room-<Area> -- sh -c 'id; echo $HOME; ls -ld $HOME $HOME/.aws'` の出力と、`touch` のエラー文を確かめる |
| `Area が無い: areas/...` | `init` の引数が Area 名でない（部屋の名前 `room-...` を渡した）、または Area が無い | 引数は Area 名（`pilot2`）。`room-` は付けない。Area が無ければ `--boundary` を付ける |
| `部屋がすでにある` | 同じ名前の部屋がある | 作りかけなら `--resume`。作り直すなら `wsl --unregister` |
| `start --no-launch` で Enter で戻らない | 待ちの `input()` に Enter が届かない（コンソールの共有。`d6c97d8` で直した） | `wsl --terminate room-pilot2`。再発したら記録する |
| `復元を止めた … 壊れたプレースホルダー` | AI が `⟦CUST_nnn⟧` のような説明を本文に書いた | `ai/out/` のその文を、記号を含まない表現に直し、`restore` を再実行する |
| `reap` が `消せなかった（）` | 古い `room.py` のバグ（`086381c` で直した） | 最新の `room.py` を使う |
| `Remove-Item` が `being used` | Windows 側の Zed の Agent などが、`projects\<名>\ai` を掴んでいる | Zed のウィンドウを閉じ、`claude-acp` のプロセスを終了する |
| `close --commit` / `start --commit` が「対象外のファイルがステージされている」で止まる | ステージ済みの別の変更がある | 先にそれをコミットするか、`git restore --staged <パス>` で戻す（`init` `open` は止まらない。3 章） |
| `pull` が「data: … の Project には取り出さない」 | `data: restore` でない Project | README の `data:` を `restore` にする（4.1） |
| `pull` が「Area の知識置き場が無い」 | `areas/<Area>/knowledge/` が無い | 作る（4.1 の 2）。別の場所なら README に `knowledge_dest:` |
| `pull` の一覧に何も出ない | `--where` が合わない、または `status: superseded` | frontmatter の項目名と値（リストは要素）を確かめる。`org:` の値は完全一致 |
| `restore` が「Area の知識が、前回の書き出しから変わっている」 | 人が Area 側の統合ノートを直したあとに、同じ Project が書き出そうとした | Area 側の変更を残したいなら、先に退避するか、ノートに取り込んでから `--force`。上書きしてよければ `restore --force`（直前の版は `_noai\final\_prev\knowledge\`） |
| `restore` が「ファイル名にプレースホルダーが残っている」 | AI が `ai/out/knowledge/` に `⟦…⟧` を含む名前を付けた | ファイル名を英数字に直し、`restore` を再実行する（6.1） |
| 統合ノートに `アクメ` などの実名が `ai/in/area/` に残る | `org:` の値や本文の語が `mask.toml` に無い、または frontmatter が置換の対象外 | `mask.toml` に語を足して `mask`。frontmatter が対象外なら、結果を記録して設計を見直す（4.1 の確認ポイント） |
| マウントが残る | `start` が途中で止まった | `uv run room.py umount --area pilot2`。残れば `wsl --terminate room-pilot2` |
