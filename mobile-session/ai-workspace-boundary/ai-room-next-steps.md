# 次のステップ: AI 作業部屋

前提と決定は [[ai-room-handover]]。詳細は [[ai-room-design]]。ここは PC のセッションで行う順序。各段階の終わりに、実測の結果を残して、次へ進むか判断する。

## TODO（忘れないための一覧。済んだら `[x]`）

- [ ] ルートの `AGENTS.md` の構成表に `mobile-session/`（モバイルから PC への引き継ぎ置き場）を足すか決めて、足す
- [x] 実機で確かめる S1〜S6（下の「1」）。全部合格（2026-10-12）。結果は「1」の「実測の結果」
- [ ] 未決9つをユーザーに1つずつ確認する（下の「2」）
- [ ] 検討の結果を `exmem/lessons/` に残す（下の「0」）
- [ ] `room` の最小版を作る（下の「3」）
- [ ] workflow-kit の手順書・雛形を更新する（下の「4」）
- [ ] 1つの Project で試す（下の「5」）
- [ ] 後回しの論点: `areas/dev-env/certs` の移し替え、対応表の保護、Obsidian の AI プラグイン、Codex・Copilot の設定（下の「6」）
- [ ] 反映が終わったら、`mobile-session/ai-workspace-boundary/` を削除する（履歴は git に残る）

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

## 2. 未決を決める（ユーザーに確認。1つずつ）

1. 部屋の単位: Project ごと（P1）でよいか。
2. スクリプトの言語と実行場所: Windows 側の Python 1本（P2）でよいか。Windows に Python（`uv` など）を入れてよいか。
3. 共有フォルダの置き場: Vault の中の `projects/<名>/ai/`（P3）か、Vault の外か。Project の `docs/` を `ai/docs/` に移してよいか。
4. コマンドの名前と構成: `room open` / `room start` / `room close`（P4）か、既存のフック名（`open` `start` `close`）に寄せるか。
5. Area への同期: 郵便受け（P5）でよいか。
6. マスクの規則: プレースホルダーの形式（例: `⟦CUST_001⟧`）、マスクしない列（数値の扱い）の指定方法、xlsx の隠れた情報の消し方。
7. reap の期限（14日は仮）。
8. 前の `_noai/` の deny 設定（Claude Code の `Read(_noai/**)`）を、Vault 側の安全網として残すか（既定は、全部屋にするので不要。ただし Vault 側で workbase の作業中に誤って読むのを防ぐ意味はある）。
9. Codex・Copilot の対応: 部屋の中で動かせば同じ境界が効く。追加の設定が要るか。

## 3. スクリプト（`room`）の最小版を作る

1. `room open`: Project のひな形（`README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final}`）と、`.gitignore`（`**/_noai/`）、Area の一覧の更新。
2. `room start` の fork 部: `_noai/raw/` の新しいファイルをマスクして `ai/in/` へ（csv と xlsx）。マスクの対応表を `_noai/map/` へ。部屋の規約（`AGENTS.md` / `CLAUDE.md`）と設定を生成。manifest（ハッシュ、版）を `ai/records/` へ。マスク漏れの点検（対応表の語が残っていないか）。
3. `room start` の exec 部: ディストリビューションの起動、`ai/` のマウント、Claude Code の起動。
4. `room start` の wait 部（回収）: `ai/out/` の成果物の復元（プレースホルダー → 実データ）→ `_noai/final/`、戻らなかったプレースホルダーの一覧（あれば止める）、【案件】の項目を Area の `inbox.md` へ、manifest の更新、コミット。
5. `room close`: 最後の回収、`README.md` の状態の更新、アンマウント、`archives/` への移動（追跡する部分はファイル単位の `git mv`。`_noai/` も一緒に移す）、zombie の印（`reap_after`）、reap。
- 先に、手作業でこの流れを1巡して（S1〜S6 の環境で）、どこが重いかを測ってからスクリプトにする。

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
