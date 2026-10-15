# 次のステップ: AI 作業部屋

前提と決定は [[ai-room-handover]]。詳細は [[ai-room-design]]。ここは PC のセッションで行う順序。各段階の終わりに、実測の結果を残して、次へ進むか判断する。

**次のセッションの入口は [[ai-room-start-here]]。** 優先順位と各項目の状態の正本は [[ai-room-roadmap]]。この文書の TODO は、roadmap の項目と対応させた一覧（2026-10-14 に整合させた）。

## TODO（忘れないための一覧。済んだら `[x]`。`(R<n>)` は roadmap の番号）

- [x] ルートの `AGENTS.md` の構成表に `mobile-session/` を足す（反映済み）
- [x] 実機で確かめる S1〜S6（下の「1」）。全部合格（2026-10-12）
- [x] 未決9つをユーザーに1つずつ確認する（下の「2」）。確定（2026-10-12）
- [x] 検討の結果を `exmem/lessons/` に残す（`exmem/lessons/ai-isolated-work-room.md`。2026-10-13）
- [x] `room` の v0（`open` / `start` / `close` / `umount`）を作る（下の「3」）。コミット済み（`7a9e7bc`）
- [x] (R1) マスク・復元を実装する（2026-10-13、モバイルのセッション。単体テストまで）。**この PC で単体テスト45件が通った**（2026-10-14）
- [x] (R1) マスク・復元の PC での確認 1〜4・6（ダミー。Excel で開く、ピボット、複数 run、cp932）。2026-10-14（[[ai-room-mask-handover]]）
- [ ] (R1) 残り: 5 `room start` の通し（マスク → AI → 復元）、7 実データでの候補の警告量
- [x] (R2) 共有知の写しを部屋へ入れる実装（方式 A。単体テストまで）
- [x] (R2) 実際の部屋で確認 1〜4（送付、読み取り専用、manifest、`~/.claude/CLAUDE.md` の案内の実装）。2026-10-14。不具合 1 件を修正（`wsl.exe` の二重解釈）（[[ai-room-shared-push-handover]]）
- [ ] (R2) 残り: 5 の実行の完遂（AI が `wrap` を最後まで通せるか、`pwsh` 製の道具が動かない場合）。`~/shared` の読み取り許可は当面手動（恒久対策の案は handover に）
- [x] (R3) フックの整理: 文書、`room readme`、`hooks.md` の運用コマンドの節（[[ai-room-hook-taxonomy]]）。雛形（`gitignore.template`、Vault 側の deny、`AGENTS.md`）と `init-workspace.md` も反映済み（2026-10-13。実機で未検証）
- [ ] (R3) `room init`（部屋の作成の自動化）と、`open` から `close` までの1巡の確認
- [x] (R4) `room stock`（下書きの回収）の実装、`integrate-hook.md` の対応（単体テストまで）
- [x] (R4) `room stock` の実機の確認（ダミーの下書き 4 件。運搬、`base_stale`、拒否 2 種、`check-inbox.ps1`）。2026-10-14（[[ai-room-stock-handover]]）
- [ ] (R4) 残り: 部屋の AI が実際に下書きを書き、`room stock` で運ぶ通し
- [ ] (R5) 部屋の運用（別セッションのディレクトリ構造の議論と合流してから進める。2026-10-14 にユーザーが保留）。決定済み（2026-10-14）: 対応表のバックアップ = `room close` で `archives/` へ移る `_noai/` ごと、Windows 側のバックアップに任せる（`_noai/` は追跡外なので、PC のバックアップ機能に依存する）。会話履歴 = 写さず、期限（close から 14 日）で消すだけ（復元は `exmem` や `docs/` でする）。案の順: 5-a `room init`（使い捨ての部屋で実装・確認。ログインは人）→ 5-b reap（消すだけ）→ 5-d `room intake`（人が置いた実環境の結果をマスクして `ai/in/` へ）。詳細は [[ai-room-ops-handover]]
- [ ] (R5) `room restore` が、`ai/out/<成果物>/` のサブディレクトリを復元できるか、`mapping.json` が無い・版が食い違うときに止まるかを、実機で確認する（2026-10-14 時点で未確認）
- [x] 決定の項目のラベルを【汎用】【案件】【この件】の 3 種類にそろえる（2026-10-14。`docs-rules.md` に【案件】を足した）
- [ ] `~/shared` の許可の確認が毎回出る件の恒久対策（`room start` が部屋の `~/.claude/settings.json` に `~/shared` だけの読み取り許可を足す案。キーの形は Claude Code のドキュメントで確認）
- [ ] マウントが別の `wsl.exe` セッションから見えない件（`room_mounts` の検査が別セッションから働くか、Zed の WSL リモートから `ai/` が見えるか）
- [x] 単体テスト `test_push_records_base_commit_and_sends_tar` が間欠的に落ちる件: `build_share_tar` の gzip を `GzipFile(mtime=0)` で作り、同じ内容なら同じバイト列にした（2026-10-15。1秒空けて2回作って一致することを確認）
- [x] (R6) Area の切り方の指針（`ai-room-why.md` に判断表を追加。2026-10-13）
- [ ] (R7) 雛形の実機確認（Vault 側の deny の書式 `Read(./projects/**)` が Windows ネイティブで効くか）
- [ ] (R8) 顧客データのある実 Project で `open` から `close` まで1巡する（手数、マスク漏れ、復元の失敗、再現性）
- [ ] 文書2本（`guides/explain/ai-room-why.md`、`guides/howto/ai-room-setup.md`）を別のセッションでレビューし、「草稿（未レビュー）」の注記を外す
- [ ] 後回しの論点: `areas/dev-env/certs` の移し替え、対応表の保護、Obsidian の AI プラグイン、Codex・Copilot の設定（下の「6」）
- [ ] 反映と確認が終わったら、検証用の環境（`ai-room-test`、`_spike-room`、`%TEMP%\s5\`）を消し、`mobile-session/ai-workspace-boundary/` を削除する（履歴は git に残る。[[ai-room-start-here]] の「完了したときの片付け」）

## 0. 反映の方針を決める（ユーザーに確認）

- 検討の結果を、どこに残すか。案: 決定と理由は `exmem/lessons/` の新しいノート（例: `ai-workspace-boundary.md`）、手順は `workflow-kit/`（新しいフック）、ワークスペースの規約は雛形（`workflow-kit/templates/workspace/`）。ノートの形式は `exmem/AGENTS.md` に従う。
- 検証は、まず使い捨ての Project で行う。実データは使わない。

## 1. 実機で確かめる（スパイク。作る前に、成立を確かめる）

| # | 確かめること | 合格の目安 |
|---|---|---|
| S1 | 部屋専用の WSL ディストリビューションを作る（`wsl --install` または `wsl --import`）。`/etc/wsl.conf` に `automount.enabled=false`、`interop.enabled=false`（`appendWindowsPath=false`）を書き、再起動する | `ls /mnt` に C: が無い。`cmd.exe` を起動できない |
| S2 | `automount` を切ったまま、`/etc/fstab` で Vault の `projects/<テスト>/ai/` **だけ**を drvfs でマウントできるか（`automount.mountFsTab` の挙動も） | 指定したフォルダだけが見える。親のフォルダは見えない |
| S3 | 部屋の中で Claude Code を導入し、ログインして、テストファイルを読み書きする。Windows の Excel で同じファイルを開いて、同時に編集しないことを確かめる | 動く。ロックなどの問題が無い |
| S4 | Zed で部屋のフォルダを WSL として開く。Zed の Claude Agent が WSL 側で動くか。動かなければ、Zed のターミナルで `wsl -d <部屋> claude` を使えるか | どちらかで使える |
| S5 | `openpyxl` で、ピボットとマクロを含む xlsx を読み書きして、壊れないか（ピボットは新規作成できない前提で、保持を確かめる）。シート名・コメント・プロパティ・隠しシート・名前の定義・外部リンク・ピボットのキャッシュに、マスク前の値が残る箇所を洗い出す | 残る箇所の一覧ができる |
| S6 | マウントしたフォルダの性能（Python で xlsx の読み書き、`rg`、`git` を使わない前提）と、ファイルの権限（`in/` を読み取り専用にできるか） | 作業に耐える |

S1・S2 が成立しなければ、案Yの形を見直す（代替: Windows 側の別フォルダを `\\wsl.localhost` 経由で受け渡す。前の「共有フォルダ」の節を参照）。

### 実測の結果（2026-10-12、PC のセッション）

S1〜S6 すべて合格。案Yの形（専用ディストリビューション＋`ai/` だけのマウント）は、そのまま成立する。環境: WSL 3.0.1.0 / Windows 11 / Zed 1.22.0 / Claude Code 2.1.296 / openpyxl 3.1.5。

| # | 結果 | 実測 |
|---|---|---|
| S1 | 合格 | `wsl --install Ubuntu-24.04 --name <名> --no-launch` で専用の部屋を作れる。`wsl.conf` の `automount.enabled=false` と `interop.enabled=false` で、`/mnt/c` は空のディレクトリ、`cmd.exe` と `powershell.exe` は見つからず、PATH に Windows 側は無い（`/usr/lib/wsl/drivers` の読み取り専用マウントと `/mnt/wslg` は残る） |
| S2 | 合格 | automount を切ったまま、`/etc/fstab` の drvfs で `ai/` だけをマウントできた（`mountFsTab=true`）。再起動後も自動。親の `_noai/` と `README.md` は見えない |
| S3 | 合格 | 部屋の中で Claude Code を導入（公式のネイティブインストーラ）、OAuth でログイン。認証情報は部屋のホーム（`/home/ai/.claude/`、権限 600）だけにあり、`ai/` と Vault には出ない。Excel で開いている xlsx は、部屋から読み取りと別名コピーが可能。同名の上書きは `PermissionError`（Excel を閉じると成功し、ファイルは壊れない） |
| S4 | 合格 | Zed の WSL リモートで部屋を `/mnt/room` として開ける。Claude Agent（ACP）は部屋の中（ユーザー `ai`）で動き、部屋の認証情報を使う。セッション履歴も部屋のホームに閉じる。`in/` の読み取り専用は、Zed の保存でも `Permission denied` で効く |
| S5 | 合格 | 下の「xlsx のマスク」 |
| S6 | 合格 | 下の「性能」 |

#### 設計に足すこと（実測から分かった）

- **部屋の中の root は、`mount -t drvfs C: ...` で C: 全体をマウントできる**。AI は必ず一般ユーザーで動かす（`wsl.conf` に `[user] default=<一般ユーザー>`）。一般ユーザーは mount も sudo もできない。
- fstab などをスクリプトから書くとき、バックスラッシュはシェルに解釈される。標準入力経由で書く。
- Zed は、Windows 側でローカルフォルダを開くと Agent も Windows 側で動き、Vault 全体が見える状態に戻る。**部屋のリモート接続（WSL）で開いたときだけ**、境界が効く。規約に明記する。
- `~$*`（Excel のオーナーファイル。Windows のユーザー名が入る）が、Excel で開いている間、`ai/` の中にできて部屋から見える。`.gitignore` に足し、回収と `room start` で無視する（ユーザー承認済み）。
- AI が書くスクリプトに、標準ライブラリと同名（`inspect.py` など）を付けない。同じディレクトリの import で標準ライブラリを覆い隠す。
- `rg` は、標準入力が読める状態でパスを省略すると標準入力を検索する。`rg <pattern> .` と書く。
- AI に境界を破るよう頼んでも、モデルが断るだけなので、検証にならない。境界の確認は、一般ユーザーでの直接の探索（`find /`、`mount`、`sudo`、`../`）で行う。

#### xlsx のマスク（S5）

- マスク前の値が残る箇所: セルの値（`sharedStrings.xml`、シートの XML）、シート名と定義名（`workbook.xml`）、ピボットのキャッシュ（`pivotCacheDefinition*.xml` に値の一覧）、コメント、ヘッダー・フッター、隠しシートの中身、プロパティ（`docProps/core.xml` の作成者、`app.xml` の勤務先名）、`printerSettings*.bin`（未検査）。
- openpyxl で読み書きすると、ピボットは保持され、Excel で開いて「すべて更新」もできた（ピボットの新規作成はできない。サンプルは Excel の COM で作った）。ただし `app.xml` と印刷設定は落ちる。
- **基本の方式: zip レベルの文字列置換**（xlsx の中の `.xml` `.rels` `.vml` 全部に、対応表の語を置換）。セル、コメント、ヘッダー、プロパティ、ピボットのキャッシュ、シート名、定義名を一括で置換でき、openpyxl を通さないのでピボットも壊れない。置換後のファイルは Excel で開け、`RefreshAll` も通った。
- 作り込みの注意: 長い語から先に置換する（`ACME` が先に当たると、`MARK_Name_ACME` のような定義名が壊れた）。シート名と定義名のプレースホルダーは ASCII にする（`⟦⟧` は、使えるか未確認。シート名は31文字までで `[]:*?/\` が使えない）。part を削除するときは `[Content_Types].xml` と `*.rels` も直す（`app.xml` は削除せず、置換だけにした）。
- 対応表に無い語は置換されない。置換後の点検（対応表の語が残っていないか）に加えて、対応表に無い固有名詞の候補を洗い出す工程が要る。

#### 性能（S6。マウント `/mnt/room` と、部屋のローカル ext4 の比較）

| 処理 | マウント | ext4 |
|---|---|---|
| 小さいファイル1000個の作成 | 5.25 秒 | 0.08 秒 |
| 同・読み取り | 3.92 秒 | 0.03 秒 |
| `grep -r`（1000ファイル） | 2.84 秒 | 0.02 秒 |
| `rg`（1000ファイル） | 0.68 秒 | 0.06 秒 |
| xlsx 5万行の書き込み | 3.25 秒 | 2.88 秒 |
| xlsx 5万行の読み込み | 3.50 秒 | 3.19 秒 |
| 50MB の書き込みとコピー | 2.49 秒 | 0.40 秒 |

- xlsx の読み書きは、マウントでも差が小さい。小さいファイルが多い処理は50倍以上遅い。
- 目安: `ai/` には作業ファイルを数百個以下に。数千ファイルになる処理（`node_modules`、`.venv`、大量の中間ファイル）は ext4（`~/`）に置く。部屋の `AGENTS.md` に「大量の一時ファイルは `~/tmp/`、成果物だけ `ai/out/`」と書く。検索は `rg`。Python の環境は ext4 に置く。
- `git` はマウント上では測っていない（部屋からは Vault の `.git` が見えず、使わない前提）。

#### 検証用の環境（片付けは未了）

- WSL のディストリビューション `ai-room-test`（削除は `wsl --unregister ai-room-test`）。
- `$HOME\works\projects\_spike-room\`（ダミーのファイルのみ。`projects/` はローカルの git 管理なので、コミットしない）。
- 一時スクリプト: `%TEMP%\s5\`。
- 未確認のまま残った点: `/mnt/wslg/distro` の中身、`printerSettings*.bin` の中身、`⟦⟧` がシート名・定義名に使えるか、`.wslconfig` の `[experimental] autoMemoryReclaim` の警告（部屋とは無関係）。

## 2. 未決を決める（確定。2026-10-12、ユーザーが1つずつ確認し、最後に一覧で確定）

最初はこれで開始する。使ってみて修正が入る可能性はある。ここで決めたことが、前の P1〜P8 と食い違うところは、この節が優先。

| # | 決定 |
|---|---|
| 1 | 部屋は **Area ごとのディストロ**、Project ごとにマウントする部屋（P1 を変更）。同じ Area の中では、会話履歴などを共有する。**顧客・機密度の境界は Area で切る**（顧客の違う Project は別の Area に置く）。理由: ライフサイクルが分かりやすく、ログインと導入が Area の数で済む |
| 1補 | 境界を守る歯止め: (a) Project の `README.md` に `area:` を必須にし、ディストロ名（`room-<Area>`）と一致しない Project は、マウントを拒否する。(b) Area の `README.md` に `boundary:`（顧客・機密度の印）を持たせ、`room open` で入力を必須にする。(c) 来歴チェック: `ai/in/` の各ファイルの由来（Area と Project）を manifest に記録し、記録のないファイルや由来の違うファイルがあれば止める。(d) 毎回の `room start` で、日時・Area・Project・ディストロ・マウントしたパス・manifest のハッシュ・チェック結果を `ai/records/` に追記する。(e) 同じディストロに、同時に複数の Project をマウントしない。(f) 顧客をまたぐ横展開は、汎用化した成果だけを【汎用】の経路（部屋の AI が `ai/out/stock/` に下書き → 人が確認して workbase の `exmem/inbox/` へ）で行う。限界: 人が Windows 側で Area をまたいでファイルをコピーすること自体は止められない（来歴チェックで検出して記録する） |
| 2 | スクリプトは Windows 側の Python 1本（`room.py`）。**uv 管理で、バージョンを pin 留め**（`.python-version`、`requires-python`、`uv.lock`。コミットする）。部屋の中の Python も uv で入れて pin する。標準ライブラリ中心。pwsh は薄いラッパーのみ。置き場は `workflow-kit/` 配下（手順書を書く段階で決める）。Windows には `uv` 0.13.0 と Python 3.13 が導入済み |
| 3 | `projects/<名>/ai/` だけをマウント（P3）。`_noai/` は `ai/` の外に置き、git で追跡しない。`docs/` は `ai/docs/` へ移す。**マウント点は `/mnt/room/<Project 名>`**（Claude Code の履歴が作業ディレクトリのパスごとに分かれるので、Project 単位で処理できる）。マウントは作業中の Project の `ai/` だけに限り、終わったらアンマウントする。既存: `archives/` の2件は移さない。`projects/` の1件は、最初の試行で移す。Area の `ai/` は、Area の部屋を初めて開くときに作る。Vault トップの `docs/` はそのまま（Vault 側の作業記録） |
| 4 | 人が言うコマンドは `room open` / `room start` / `room close`（P4）。既存のフック（`open` `start` `wrap` `close`）は、部屋の中で AI が判断の部分を行う |
| 5 | Area への同期は郵便受け（P5）。`room start` の回収で、同じ Area の【案件】の項目を Area の `ai/docs/inbox.md` へ（Windows 側の `room.py` が追記）。【汎用】は `exmem/inbox/` の経路 |
| 6 | マスク: (6-1) プレースホルダーは場所で2種類。定義名・シート名は ASCII（`SHEET_001`、`NAME_001`）、それ以外は `⟦CUST_001⟧` 形式（種類の接頭辞つき）。実測: `⟦⟧` はシート名には使えるが、定義名には使えない。(6-2) 数値は既定でマスクしない。語は `_noai/` の `mask.toml` の `[terms]`、列は `[columns]`（`シート名!列名`）で指定。(6-3) xlsx は zip レベルの置換を基本に、作成者・会社名のプロパティは無条件に空に、`printerSettings*.bin` は削除（`[Content_Types].xml` と `.rels` も直す）、置換後に全 part を点検して、対応表の語が残っていれば止める。**対象は csv と xlsx**。docx・pptx も同じ zip 方式で揃えるが、変更は xlsx を基準にし、まず小さく動かして決める |
| 7 | reap は close から14日を既定に、**設定で変更可能**（置き場は設定ファイルか Project の `README.md` の frontmatter。実装時に決める）。次の `room close` で期限切れを一覧にし、承認して実行する（`room reap <名>` でも可）。履歴は `ai/records/sessions/` に写してから消す。zombie の実体は、Project ごとの会話履歴（`~/.claude/projects/-mnt-room-<名>/`）と `~/tmp/<名>/` |
| 8 | Vault 側で `projects/` `areas/` `archives/` を丸ごと deny（`Read` と `Edit`）。ワークスペースの `.claude/settings.json` の雛形に入れる。安全網であって境界の保証ではない（`grep -r` やスクリプトの中は止まらない）。`room.py` は AI に実行させない（`AGENTS.md` に明記）。Windows ネイティブで絶対パスの deny が効くかは、雛形を作るときに実機で確認する |
| 9 | Codex・Copilot は今は設定しない。必要になったら部屋の中へ導入する（境界は物理分離なので、AI の種類に依存しない）。部屋の規約の正本は `AGENTS.md`、`CLAUDE.md` は `@AGENTS.md` で読ませる。エディタ内蔵の Copilot（部屋の外で動く）は、機密を扱う Project では使わない |

実測から決まった事項（上の「1」の実測結果の「設計に足すこと」）も、同じく確定: AI は一般ユーザーで動かす、Zed は WSL リモート接続でだけ使う、`~$*` は無視する、大量の一時ファイルは `~/tmp/`、`rg` はパスを明示する、AI が書くスクリプトに標準ライブラリと同名を付けない。

### 手作業の1巡（1巡目、2026-10-12）

Area の部屋 `room-office-admin`（`wsl --install Ubuntu-24.04 --name ... --no-launch`、`wsl.conf` は automount・interop 無効、`mountFsTab=false`、既定ユーザーは一般ユーザー。`curl` `rg` `uv` Claude Code を導入）を作り、既存の Project 1件（顧客データなし）で `mount → AI の作業 → 回収 → unmount` を通した。検証用の `ai-room-test` と `_spike-room` は、サンプルとして残している。

Vault 側の変更（ローカルの git）: Area の `README.md` に `boundary: internal`、ワークスペースの `.gitignore` に `**/_noai/` と `~$*`、Project の `docs/` を `ai/docs/` へ、成果物を `ai/out/` へ（ファイル単位の `git mv`）、`ai/{in,work,records}` に `.gitkeep`、`_noai/{raw,map,final}` は追跡外。README の成果物のパスを直した。`ai/docs/log.md`（過去の記録）の旧パスは、当時の事実なので直さない。

| 項目 | 実測 |
|---|---|
| マウント | 0.1 秒。部屋から見えるのは `ai/` の中身だけ。`/mnt/c` は空 |
| AI の作業 | 約33秒（`log.md` の要約、HTML のレビュー、`out/review-notes.md` の作成）。HTML は無変更 |
| 回収 | 成果物は、Windows 側にそのまま現れる（コピー不要） |
| 会話履歴 | `~/.claude/projects/-mnt-room-<Project 名>/` に Project ごとに分かれて残る（小さな作業1回で約180KB）。これが zombie の実体 |
| unmount | 成功 |

手作業は4手（マウント、起動、回収の確認、アンマウント＋`rmdir`）。重いのは AI の処理時間だけで、マウントと回収は無視できる。スクリプト化に向く。

#### 1巡目で見つかった問題と対応

1. **README が部屋から見えない。** AI が、`log.md` の参照先の README（完了条件と制約）が無いと報告した。`start` / `wrap` は README の完了条件を読む前提。対応案: `room start` が README の写しを `ai/docs/` に置く（Vault が正本、部屋は読み取りのみ。README を索引として残す決定 3 と整合）。または、完了条件を `ai/docs/` 側に移す。
2. **マウント点のディレクトリが残ると、Project 名が他の Project の AI に見える。** 過去のテストの空ディレクトリが `/mnt/room/` に残り、AI の `ls` に出た。`umount` のあとに `rmdir` する手順を、`room start` と `room close` に入れる。
3. `claude -p`（非対話）では、許可されていないコマンド（`ls` など）が実行されない。`room start` の起動は対話モードの想定なので、影響は小さい。
4. `mount` は `-o <オプション> <デバイス> <マウント点>` の順で書く。root が `wsl -u root` で行ったマウントは、別セッションの一般ユーザーから見える。PowerShell から標準入力でコマンドを渡すと、改行が CRLF になる（`umount` が引数なしのエラーになり、同じ場所にマウントが積み重なった）。`room.py` は、バイト列で LF を明示する。マウントが残っていないかを、`room start` の最初と `room close` の最後に点検する。

5. **個人のグローバル ignore（`~/.gitignore_global`）の `out/` が、`ai/out/` の新しいファイルを無視する。** 成果物が、回収のコミットから黙って漏れる（すでに追跡されているファイルの `git mv` は通るので、気づきにくい）。ワークスペースの `.gitignore` に `!**/ai/out/` を足して打ち消した（リポジトリの `.gitignore` は、グローバルより優先される）。`ai/` の他の名前（`in` `work` `records` `docs`）は衝突しない。雛形（`gitignore.template`）にも入れる。`room.py` の回収では、コミット後に「`ai/` に未追跡のファイルが残っていないか」を点検する。

### 手作業の2巡目: close（2026-10-12）

実在の Project 1件（顧客データなし）を、`close` まで通し、`archives/` へ移した（戻さない。ユーザーの指示: テスト版なので、未記入の欄は「完了扱い」にして閉じる）。流れは、判断が部屋の AI（`out/close.md` と `docs/log.md` の更新。約68秒。AI への指示は `ai/records/session-close-prompt.md` に記録）、副作用が Windows 側（`room close` の役を手作業で）。

- 部屋の AI: 完了条件の確認、暫定の見直し、未解決の振り分け（Area へ【案件】6件、破棄3件）、【汎用】候補3件（`stock` は実行しない）、`docs/log.md` の現在状態の更新。変更したのは2ファイルだけ。
- Windows 側: README の状態更新（`status: done`、`closed`、`reap_after`、完了条件の結果）、Area の一覧の更新、Area の `ai/docs/inbox.md` への【案件】の転記（Project 名と連番の識別子つき）、アンマウントと `rmdir`、`ctx/` の削除、ファイル単位の `git mv` で `archives/` へ、コミット、実行記録（`ai/records/room-log.md`）。
- 成立したこと: README の写し（`ai/ctx/README.md`。派生物なので `**/ai/ctx/` を ignore）で、AI が完了条件を読んで判断できた。郵便受け（P5）は、Windows 側から Area の `ai/docs/inbox.md` に追記する形で成立（Area の `ai/` は部屋にマウントされず、AI は Area の記録を直接触れない）。判断（AI）と副作用（スクリプト）の分担は、`close-hook.md` の手順1〜4と5〜7の境で分かれた。

#### 2巡目で見つかった問題と対応

6. アンマウント直後に `/proc/mounts` を数えると、マウントが1つ残って見えた（数秒後に消えた）。`room close` では、少し待って再点検する。
7. PowerShell の `Remove-Item` が、削除ガードで止まった。空ディレクトリは `[IO.Directory]::Delete` で消せる（`room.py`は Python なので影響しない）。
8. `git mv` の前に、`git add -A` で新規ファイルをステージする。そうしないと、追跡されていない成果物（`close.md` など）が `archives/` に移らない。
9. 旧ログの「総括は新しいスレッドで」のような、Project の外の作業の項目は、AI が Area へ渡さず、確認を求めた。この判断は、そのまま妥当（人が決める）。
10. 未検証のまま: manifest の記録と来歴チェックの自動化、呼び出し元の記録（Vault トップの `docs/log.md`）への close の記録、`wrap` 単独、Zed で `/mnt/room/<Project 名>` を開く操作、マスク（使い捨てのダミーデータで）、reap。

#### 未実施（3巡目以降）

`wrap`（`decisions.md` の【案件】ラベル）と Area の `inbox.md` への同期、manifest と来歴チェックとログ（`ai/records/`）、`close`（アンマウントを先に、ファイル単位の `git mv` で `archives/` へ）、Zed から `/mnt/room/<Project 名>` を開く操作、マスク（使い捨てのダミーデータで）。

## 3. スクリプト（`room`）の最小版を作る

1. `room open`: Project のひな形（`README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final}`）と、`.gitignore`（`**/_noai/`）、Area の一覧の更新。
2. `room start` の fork 部: `_noai/raw/` の新しいファイルをマスクして `ai/in/` へ（csv と xlsx）。マスクの対応表を `_noai/map/` へ。部屋の規約（`AGENTS.md` / `CLAUDE.md`）と設定を生成。manifest（ハッシュ、版）を `ai/records/` へ。マスク漏れの点検（対応表の語が残っていないか）。
3. `room start` の exec 部: ディストリビューションの起動、`ai/` のマウント、Claude Code の起動。
4. `room start` の wait 部（回収）: `ai/out/` の成果物の復元（プレースホルダー → 実データ）→ `_noai/final/`、戻らなかったプレースホルダーの一覧（あれば止める）、【案件】の項目を Area の `inbox.md` へ、manifest の更新、コミット。
5. `room close`: 最後の回収、`README.md` の状態の更新、アンマウント、`archives/` への移動（追跡する部分はファイル単位の `git mv`。`_noai/` も一緒に移す）、zombie の印（`reap_after`）、reap。
- 先に、手作業でこの流れを1巡して（S1〜S6 の環境で）、どこが重いかを測ってからスクリプトにする。

### 実装の状況（2026-10-12）: v0

`workflow-kit/room/`（`room.py`、`pyproject.toml`、`.python-version`、`uv.lock`、`tests/`、`README.md`）。標準ライブラリだけ。Python は uv で 3.13.14 に固定。**未コミット**（`workflow-kit/AGENTS.md` が、kit の変更は承認を得た後と定めているため、ユーザーの承認待ち）。

- 実装済み: `open`、`start`（チェック、README の写し、マウント、AI の起動、必ずアンマウント、回収の一覧、無視されているファイルの警告）、`close`（【案件】を Area の `inbox.md` へ、README の状態、Area の一覧、`archives/` へ移動）、`umount`。来歴チェック（manifest。`start --adopt` で人が記録）、`.gitignore` の必須行の点検、コミットのガード（対象外のステージ済みファイルがあれば止める）、`--no-launch`（Zed の WSL リモート用）。
- テスト: 23件（WSL は差し替え、一時ディレクトリの git）。加えて、**実際の部屋（`room-office-admin`）と使い捨ての Vault で、`open → start → close` を通した**。部屋の中で、一般ユーザー、`/mnt/c` が空、`../` の原本が見えない、`in/` に書けない、`out/` に書ける、を確認。アンマウントと残りの確認も OK。close では、追跡外の `_noai/`（原本）が `archives/` に移り、git には入らないことを確認した。
- e2e で見つかって直した不具合: (1) アンマウント後に `in/.gitkeep` が読み取り専用のまま残った（マウント時は `in/` の全ファイルを読み取り専用にするので、戻すのも全ファイル）。(2) 回収の一覧が、`?? .../ai/out/` とフォルダ単位でまとまり、新しいファイル名が見えなかった（`git status -uall` にした）。(3) wsl の出力と、`room.py` の表示の順序が前後した（行バッファにした）。
- 未実装: マスク・復元（`mask.toml`、zip レベルの置換、置換後の点検、manifest への記録）、【汎用】の下書きの回収、reap、部屋の作成の自動化、`start` の対話モードで `claude` の許可を求められる挙動の確認（`--cmd` でテストした。`claude` の対話は、あなたの端末で確認する）。
- 次の候補: マスク・復元の最小版（csv と xlsx。使い捨てのダミーデータで）。

## 4. workflow-kit に組み込む

- 新しい手順書（`room-hook.md` など）と `hooks.md` の呼び出し表への追加。既存の `open` / `start` / `wrap` / `close` との関係の整理（部屋の中で AI が行うのは判断の部分、副作用は `room` が行う）。
- ワークスペースの雛形の更新: `AGENTS.md`（AI は部屋で使う、Vault 側で Project の作業をしない、`_noai/` と `works-secret` の扱い）、`gitignore.template`（`**/_noai/`）。`init` の手順に、部屋専用のディストリビューションの用意を足す。
- 規約: AI が書くスクリプトは、入力のパスを明示する。部屋の `AGENTS.md` で、`in/` と `ctx/` を変えない、プレースホルダーをそのまま残すと定める。
- 共有側に、勤務先固有の情報（実際の Project 名、顧客名）を書かない。

## 5. 1つの Project で試す

- 実際の Project 1つを、`room open` から `room close` まで1巡する。測るもの: 手数、マスクの漏れ、復元の失敗、ピボットのキャッシュ、点在（ファイルが散らばっていないか）、作業記録で再現できるか。
- 結果で、P1〜P8 と workflow-kit の手順を直す。安定したら、他の Project へ展開する。

## 6. 後回し（別の論点）

- `areas/dev-env/certs` など、いま Vault の中にある鍵・証明書の `works-secret` への移し替え。
- 対応表の保護（Vault の中の private 領域の扱い。今回の AI 分離とは別の論点とした）。
- Obsidian で使う AI プラグインの扱い（部屋の外にいるので、機密を扱う Project には使わない決まりにする）。
- Codex・Copilot の個別の設定。
