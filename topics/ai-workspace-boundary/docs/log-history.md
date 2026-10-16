# ai-workspace-boundary: 経緯（開始時に読まない）

旧 `ai-room-next-steps.md` の実測の結果・手作業の巡回・実装の状況と、旧 TODO 全文（2026-10-15 時点）。現在状態は `log.md`、決定は `decisions.md`。

## Log

### 2026-10-16
- 別スレッドの変更（`7b2c515` open の構造、`c86b4d6` close-hook 削除）と、トピックの残件を突き合わせた。`ai-room-handover.md` の close-hook への参照を直した。
- `room restore` が人の変えた `_noai/final/` を上書きせず止める（`1a037f9`）。`room init`（`e12209e`）、`room reap`（`3c838c1`）を実装。項目 5 の保留を解除。`room intake` は見送り（`e96c511`）。単体テストは59件で全部通る。
- 未決のまま: リポジトリが正の `src`・remote の扱い（kit-growth の Open Questions）。
- 遠回り: なし。

### 2026-10-15
- 他環境（旧 kit で `projects/` の下に Area と Project を重ねていた PC）の AI 開発環境プレイブック（画像）を、この環境の `areas/` `projects/` に当てはめた。固有名と作業固有の仕組みは省き、共通部と Excel VBA 固有部を `exmem/lessons/` の2ノートにした（コミット `e051cc1`、判読残件の反映は `91fb76b`）。決定は `decisions.md` の 2026-10-15。
- 当てはめで見つかった穴を塞いだ。(1) 部屋の AI から Area の共通ルールが見えない → `room start` が Area の README を `ai/ctx/area-README.md` に写す。(2) `type: dev` の `src/` `tests/` `tools/` の置き場 → `ai/out/<成果物名>/`、`open-hook.md` と `dev-deliverable-guide.md`。コミット `b6c3199`。
- 確認: `room` の単体テストは51件で、新しい2件は通る。元からの失敗2件（`SharedPermissionTest`）は残る。実際の WSL での通しは未実施。
- 遠回り: 少し（画像で渡された他環境の文書の読み取りに手間取った）。

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

- マスク前の値が残る箇所: セルの値（`sharedStrings.xml`、シートの XML）、シート名と定義名（`workbook.xml`）、ピボットのキャッシュ（`pivotCacheDefinition*.xml` に値の一覧）、コメント、ヘッダー・フッター、隠しシートの中身、プロパティ（`docProps/core.xml` の作成者、`app.xml` の会社名）、`printerSettings*.bin`（未検査）。
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
- 共有側に、会社固有の情報（実際の Project 名、顧客名）を書かない。

## 5. 1つの Project で試す

- 実際の Project 1つを、`room open` から `room close` まで1巡する。測るもの: 手数、マスクの漏れ、復元の失敗、ピボットのキャッシュ、点在（ファイルが散らばっていないか）、作業記録で再現できるか。
- 結果で、P1〜P8 と workflow-kit の手順を直す。安定したら、他の Project へ展開する。

## 6. 後回し（別の論点）

- `areas/dev-env/certs` など、いま Vault の中にある鍵・証明書の `works-secret` への移し替え。
- 対応表の保護（Vault の中の private 領域の扱い。今回の AI 分離とは別の論点とした）。
- Obsidian で使う AI プラグインの扱い（部屋の外にいるので、機密を扱う Project には使わない決まりにする）。
- Codex・Copilot の個別の設定。


## 旧 TODO 全文（2026-10-15 時点。`(R<n>)` は優先順位の番号）

- [x] ルートの `AGENTS.md` の構成表に `topics/` を足す（反映済み）
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
- [x] `~/shared` の許可の確認が毎回出る件: `room start` が部屋の `~/.claude/settings.json` に `Read(~/shared/**)` を足す（既存の項目は残す。冪等）。書式は公式ドキュメントで確認（permissions の `Read(~/path)`）。**実機で、確認が出なくなるか未確認**（2026-10-15、単体テストまで）。`blockReadsOutsideWorkingDirectories` が有効だと allow が効かない可能性があるので、実機で見る
- [ ] マウントが別の `wsl.exe` セッションから見えない件: 仮説 = 待っている間に `wsl.exe` のセッションが無く、部屋が止まってマウントが消えた（空のマウント点だけが残る）。対策を実装: `--no-launch` の待機中は `sleep infinity` を部屋で動かして止まらないようにする（2026-10-15、単体テストまで）。**実機で、別セッションから `/proc/mounts` と `ai/` が見えるか、Zed の WSL リモートから `ai/` が見えるか確認する**。見えれば済み
- [x] 単体テスト `test_push_records_base_commit_and_sends_tar` が間欠的に落ちる件: `build_share_tar` の gzip を `GzipFile(mtime=0)` で作り、同じ内容なら同じバイト列にした（2026-10-15。1秒空けて2回作って一致することを確認）
- [x] (R6) Area の切り方の指針（`ai-room-why.md` に判断表を追加。2026-10-13）
- [ ] (R7) 雛形の実機確認（Vault 側の deny の書式 `Read(./projects/**)` が Windows ネイティブで効くか）
- [ ] (R8) 顧客データのある実 Project で `open` から `close` まで1巡する（手数、マスク漏れ、復元の失敗、再現性）
- [ ] 文書2本（`guides/explain/ai-room-why.md`、`guides/howto/ai-room-setup.md`）を別のセッションでレビューし、「草稿（未レビュー）」の注記を外す
- [ ] 後回しの論点: `areas/dev-env/certs` の移し替え、対応表の保護、Obsidian の AI プラグイン、Codex・Copilot の設定（下の「6」）
- [ ] 反映と確認が終わったら、検証用の環境（`ai-room-test`、`_spike-room`、`%TEMP%\s5\`）を消し、`topics/ai-workspace-boundary/` を削除する（履歴は git に残る。[[ai-room-start-here]] の「完了したときの片付け」）



## 旧 roadmap 全文（2026-10-15 に log.md へ状態を移した）

（元の題: 対応の優先順位と進め方）

- 次のセッションの入口は [[ai-room-start-here]]（読む順とローカルの状態）。この文書が、優先順位と各項目の状態の正本。
- 作成: 2026-10-13（モバイルのセッション）。ユーザーの指示: 「マスクと復元が先。論点を優先度として1つずつやる」「Obsidian の AI は、ツール都合でやむを得ないので優先度を下げる」。
- 前提: [[ai-room-handover]]、ai-room-next-steps（旧。このファイルに分けた）、[[ai-room-hook-taxonomy]]、[[ai-room-shared-knowledge-sync]]。
- 状態: 優先順位は提案。1番は着手を合意済み。以降は、前の項目が終わるごとに、順序を見直す。

## 進め方（毎回同じ）

1. **1項目ずつ**。前の項目が「完了の目安」を満たしてから、次へ進む。
2. 項目ごとに、(a) 設計の未決を詰める（ユーザーに1つずつ確認。必要なら「一般化 → 類似問題 → 適用」の流れで解く。`exmem/inbox/2026-10-13-problem-solving-by-analogy.md`（統合後は lessons へ））、(b) 実装、(c) 検証、(d) 文書の更新、の順に行う。
3. 場所の分担:
   - **モバイル（クラウド）のセッション**: 設計、実装（標準ライブラリの Python）、合成データでの単体テスト、文書、コミット。WSL と Excel は動かせない。
   - **PC のセッション**: 実機（WSL、Excel）での検証、部屋の作成、実 Project での試行。
4. kit（`workflow-kit/`）の変更は、`workflow-kit/AGENTS.md` の規則どおり、ユーザーの承認を得てから行う。コミットは main に直接（ユーザーの指示）。コミットメッセージは `[領域] 変更内容`。
5. 項目が終わったら、`ai-room-next-steps.md` の TODO と、この文書の状態を更新する。実機の確認が残るものは、「未検証」と明記して PC に引き継ぐ。

## 優先順位

| # | 項目 | 完了の目安 | 主な場所 | 依存 |
|---|---|---|---|---|
| 1 | **マスク・復元**（実装・単体テスト済み 2026-10-13。PC のダミーでの確認 1〜4・6 は済み 2026-10-14、5（`room start` の通し）と 7（実データ）は未確認: [[ai-room-mask-handover]]）（`room.py`: `mask.toml`、プレースホルダー、対応表、zip 置換、置換後の点検、復元、戻らなかったものの一覧、manifest への記録）。対象は csv と xlsx | 合成データ（csv と、ピボット・コメント・定義名・プロパティを含む xlsx）で、マスク → 部屋での作業（模擬）→ 復元の往復が一致し、マスク後に対応表の語が 0 件。PC で、Excel が開き「すべて更新」が通る | 設計・実装・単体テストはモバイル。Excel での確認は PC | なし |
| 2 | **共有知を部屋へ入れる**（実装・単体テスト済み 2026-10-13。PC の実機で送付・読み取り専用・manifest の確認 1〜3 は済み 2026-10-14、4（案内は `~/.claude/CLAUDE.md`）は実装・確認済み、5 は AI が手順書を読むところまで確認（実行の完遂は未）。未解決: `~/shared` の読み取りの許可の確認が毎回出る: [[ai-room-shared-push-handover]]）（方式 A: 起動のたびに workbase の写しを `~/shared` に読み取り専用で送る。基準コミットを manifest に記録）と、部屋の `AGENTS.md` からの案内 | 部屋の AI が、フックの手順書と `lessons/` を読める。manifest に基準コミットが入る | 実装はモバイル、実機確認は PC | 1 と並行可 |
| 3 | **フックの整理**（文書と `room readme` は実装済み 2026-10-13。`room init` は PC。結果: [[ai-room-hook-taxonomy]]）（[[ai-room-hook-taxonomy]] の論点）: README の書き手（下書き方式）、部屋の作成 `room init`、`hooks.md` の運用コマンドの節、kit の手順書の `ai/docs/` への読み替え | `open` から `close` までを、2層の役割どおりに1巡できる | モバイル（文書）＋ PC（1巡の確認） | 2 |
| 4 | **出る方向（`stock`）**（`room stock` は実装・単体テスト済み 2026-10-13。`integrate` の手順書の対応も反映済み。PC のダミーでの `room stock` の確認は済み 2026-10-14、部屋の AI に下書きを書かせる通しは未: [[ai-room-stock-handover]]）: 下書きの回収（基準コミットと観測日を持たせる）、`integrate` の rebase の検出と解決、点検スクリプトの対応 | 部屋で書いた【汎用】の下書きが、人の確認を経て `exmem/inbox/` に入り、基準が古ければ印が付く | モバイル＋ PC | 2、3 |
| 5 | **部屋の運用**（**保留中**: 別セッションのディレクトリ構造の議論と合流してから。決定済み 2026-10-14: 対応表のバックアップは `archives/` の `_noai/` を PC のバックアップに任せる、会話履歴は写さず期限で消すだけ。案: `room init`、reap（消すだけ）、`room intake`）（モバイルでできる分は無し。実装には実際の WSL が要る。設計メモ: [[ai-room-ops-handover]]）: 部屋の作成の自動化、更新、reap、会話履歴のバックアップ、Area 数ぶんのログイン | 新しい Area の部屋を、手順書どおりに短時間で作れる。期限切れの履歴が整理される | PC | 3 |
| 6 | **Area の切り方の指針**（`ai-room-why.md` に判断表を追加済み 2026-10-13）（顧客の境界は Area で切る。`boundary:` の使い方） | 新しい Project を作るとき、どの Area に置くかを迷わない | モバイル（文書） | 5 |
| 7 | **雛形と記録への反映**（雛形・lessons・ルート `AGENTS.md`・`init-workspace.md` は反映済み 2026-10-13。`topics/` の削除は PC の確認後）: ワークスペースの雛形（`AGENTS.md`、`gitignore.template`、Vault 側の deny を入れた `.claude/settings.json`）、`exmem/lessons/` への決定の記録、ルート `AGENTS.md` の構成表への `topics/`、`topics/` の整理 | 新しい PC に導入するとき、手順書と雛形だけで同じ構成になる | モバイル＋ PC | 1〜5 の安定 |
| 8 | **顧客データのある実 Project での試行**（手数、マスク漏れ、復元の失敗、再現性を測る） | 実 Project を `open` から `close` まで1巡し、問題が一覧になる | PC | 1〜4 |

優先度を下げるもの（バックログ）:
- **Obsidian の中で AI と話す**: Claudian は部屋に繋がらない。ツールの都合でやむを得ないので、AI は Zed で使う。やるなら、Linux 版の Obsidian を部屋の中（WSLg）で動かす案を実機で試す（[[ai-room-hook-taxonomy]] とは別）。
- 小さいファイルが多い処理の遅さ（約50倍）: 規則（大量の一時ファイルは `~/tmp/`）で対処済み。
- Codex・Copilot の設定: 必要になってから。

## 1番（マスク・復元）の次の一手

設計の未決を詰める。確認する点（1つずつ聞く）:
1. `mask.toml` の形（語の表 `[terms]`、列の指定 `[columns]`、マスクしないものの指定）。
2. 対応表の置き場と形式（`_noai/map/`、1ファイルか種類別か）。
3. 復元の対象（`ai/out/` の xlsx・csv・md か、拡張子の範囲）。
4. 置換の規則（長い語から。大文字小文字・全半角・部分一致の扱い）。
5. 対応表に無い固有名詞の候補を洗い出す方法（最小限でよいか）。
6. `room start` との組み込み方（マスクは `start` の最初、復元は回収で）。

