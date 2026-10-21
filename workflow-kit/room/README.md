# room

AI 作業部屋の操作（`open` / `start` / `close` / `umount` / `mask` / `restore` / `pull`）。人が Windows で実行する。**AI には実行させない**（原本と対応表を読む工程（マスク・復元）を含むため）。設計の理由は `guides/explain/ai-room-why.md`、手作業の手順は `guides/howto/ai-room-setup.md`。

状態: v0（2026-10-12）に、マスク・復元（`maskkit.py`）を足した（2026-10-13、モバイルで実装。**合成データの単体テストのみ**。2026-10-18 に、実際の Excel と WSL の部屋で、ダミーのデータを使って確認した）。実際の WSL（部屋）で、`init → open → mask → start → restore → readme → stock → close → reap` を通した（2026-10-18）。

## 使い方

```powershell
cd <このディレクトリ>
uv run room.py init <Area> [--boundary <印>] [--resume] [--no-commit]
uv run room.py open <Project> --area <Area> [--type doc|dev|dev-env|dev-test|research] [--data none|mask|restore] [--boundary <印>] [--no-commit]
uv run room.py start <Project> [--cmd <部屋で実行するコマンド>] [--no-launch] [--adopt] [--commit]
uv run room.py close <Project> [--commit]
uv run room.py umount --area <Area>
uv run room.py rename-area <旧Area> <新Area> [--no-commit]
```

- works は `$ROOM_VAULT`、無ければ `~/works`。`--vault <パス>` で指定できる（`--vault` はサブコマンドの前に書く）。`close` から reap までの日数は `--reap-days`（既定 14。`$ROOM_REAP_DAYS` でも指定できる）。
- 部屋（WSL のディストリビューション）は `room-<Area>`。`room init <Area>` で作る（手作業の手順は `guides/howto/ai-room-setup.md` の 3・4 章）。
- トレーラー（2026-10-21）: room が作るコミット（`init` `open` `rename-area` `start` `readme` `close`）に、`Room-Op: <操作>`、`Room-Rev: <resources の短縮ハッシュ>`、`Room-Area: <Area>`、`Room-Project: <Project>`（Project の操作だけ）を付ける。既存の Area / Project が、どの版の room で作られ、変えられたかを引く印。差分は `git -C resources diff <Room-Rev>..HEAD -- workflow-kit/room`、一覧は `git log --format='%h %(trailers:key=Room-Op,key=Room-Rev,valueonly,separator=%x20)'`（works 側）。`Room-Rev` は `workflow-kit/` に未コミットの変更があると末尾が `-dirty`（その版は差分の基点にしない）、git で引けなければ `unknown`。コミットしない操作（`mask` `restore` `pull` `stock` など）には付かない。付いていない古いコミットは「版不明」。
- コミット: `init`（Area の作成）と `open`（Project のひな形と Area の一覧）は、**初期状態として既定でコミットする**（戻る起点。`--no-commit` で省く。2026-10-18）。`init` `open` は、対象外のステージ済みの変更があっても止まらず、対象のパスだけをコミットする（対象外はステージに残す）。`start` `readme` `close` は、`--commit` を付けたときだけで、対象のパス以外がステージされていたら、コミットしない。

| コマンド | すること |
|---|---|
| `init` | Area の部屋 `room-<Area>` を作る（実機で確認済み: 2026-10-18。Area の作成とコミットは単体テストのみ）: `areas/<Area>/README.md` が無ければ `--boundary <印>` で作る（既定値は無い。印が無ければ止まる）→ `boundary:` の確認 → `wsl --install Ubuntu-26.04 --name … --no-launch` → 一般ユーザー `ai` → `/etc/wsl.conf`（automount・interop 無効）→ 分離の確認（`ai` / `/mnt/c` 空 / `cmd.exe` 無し / sudo 不可。外れたら道具を入れずに止まる）→ curl・rg・Node.js 24（公式の tarball をチェックサム確認つきで `/usr/local` へ。Zed の ACP エージェントの `npx` が 22 以上を要るため。部屋での実機確認は未了）・変換の道具（LibreOffice の calc・writer・impress、日本語フォント `fonts-noto-cjk`（`/etc/fonts/local.conf` で日本語の字形を優先）、（等幅フォント PlemolJP（v3.1.0。版と SHA-256 を固定。約 220 MB の取得）は、試験が安定するまで `init` から外している: 2026-10-20。`room.py` の `PLEMOLJP_INSTALL` と、コメントアウトした `step_script` で戻せる。monospace の優先順位には PlemolJP が残っていて、無ければ Noto Sans Mono CJK JP になる）、pandoc、Chromium（Playwright 版。`/opt/ms-playwright`）と mermaid-cli（`mmdc`。`room-mmdc` と `room-chrome` の呼び出し用スクリプトが `/usr/local/bin` に入る）。root が入れる。部屋で xlsx・docx・pptx の変換や再計算、Markdown の HTML 化をするため。実機確認は未了: 2026-10-20）・npm の cafile・uv・Claude Code → 道具の確認。**ログインは人**（手順を表示する）。Area の置き場として `areas/<Area>/knowledge/` と `areas/<Area>/ai/docs/inbox.md` を、**無ければ作る**（あるものは触らない。2026-10-21。後続の `pull` `restore` `close` は、無ければ作らず警告する。単体テストのみ。部屋がすでにあって止まる場合も、この作成は先に行う）。部屋がすでにあれば止まる。作りかけは `--resume`（設定と道具の入れ直し）。終わりに、Area の README の変更だけをコミットする。TLS 検査のあるネットワークで curl が証明書エラー（60）になるときは、`--ca-cert <ファイル>`（勤務先のルート証明書、PEM、5枚まで）を付ける。apt の後に root が `/usr/local/share/ca-certificates/` へ入れる（`ai` は書き換えられない。SHA-256 を表示する）。付けなければ入れない。wsl.exe には `WSLENV` を渡さない（automount を切った部屋では、Windows のパスが変換できず、壊れた `SSL_CERT_FILE` などが残るため。実機で確認: 2026-10-19） |
| `aws-key` | `aws-key <Area> --profile <名前>`: 部屋の `~/.aws/credentials` に、Bedrock 用のキーを入れる（同名の節は置き換え、ほかの節は残す。権限 600）。アクセスキー ID は入力、秘密と `AWS_SESSION_TOKEN`（一時キーのときだけ）は画面に出さずに受け取り、標準入力で部屋へ渡す（コマンドラインにも履歴にも残さない）。AI からは読める場所なので、Bedrock の権限だけのユーザーにして、予算アラートを置く。Zed の `agent_servers` の `env` に `AWS_PROFILE=<名前>` を書いて使う（環境変数は Zed 経由では引き継がれないため。実機確認は未了） |
| `shell <Area>` | 部屋に入る（`wsl -d room-<Area>` の代わり）。`WSLENV` を外して入るので、Windows の `WSLENV` に `/p` 付きのパスがあっても、入るたびに「failed to translate」が出ない（automount を切った部屋では、そのパスを変換できないため） |
| `reap [名前]` | close から期限（`reap_after`。既定14日）が来て、まだ `reaped` の無い `archives/` の Project について、部屋の会話履歴（`~/.claude/projects/-mnt-room-<名>/`）と `~/tmp/<名>` を消し、README に `reaped: <日付>` を付ける。会話履歴は写さずに消す（復元は `exmem` や `ai/docs/` の記録で）。名前なしは期限切れの一覧を出して承認を求める（`--yes` で省略）。名前ありで期限前なら `--force`。名前が英数字・`_`・`-` 以外なら止まる。`close` の終わりにも一覧を出す（端末のときは承認を求める）。Windows 側の `archives/` は消さない |
| `open` | works の `.gitignore`（`**/_noai/` と `!**/ai/out/`）と Area の `boundary:` を確認し、`projects/<名>/` に `README.md`（`data:` つき）、`ai/{docs,in,work,out,records}`、`_noai/` の下は `data:` に応じたディレクトリ（下の表）を作り、Area の一覧に足す |
| `start` | `area:` とディストロ名の一致、`boundary:`、ほかのマウントが無いこと、`ai/in/` の来歴（manifest）を確認 → Project の README と所属する Area の README の写しを `ai/ctx/`（`README.md`、`area-README.md`）に置く（Area の README が 16 KiB を超えると知らせる）→ 部屋の `~/.claude.json` で `/mnt/room/<名>` を信頼済みにする（信頼の確認を省く。2026-10-19）→ `ai/` を `/mnt/room/<名>` に root でマウントし、`in/` を読み取り専用に → 部屋で AI を起動（一般ユーザー）→ **必ず**アンマウントして、マウント点を消し、残りを確認 → 変更の一覧と、追跡されずに無視されているファイルの警告 |
| （`start` の中） | 共有知の写し（方式 A）: `<Vault>/resources/` の `AGENTS.md`、`workflow-kit/`（`workflow-kit/room/` は `README.md` だけ。コード・テスト・設定は送らない。2026-10-17）、`exmem/{AGENTS.md,README.md,tags.md,lessons/}`、`guides/` を tar.gz にして、部屋の `~/shared` に読み取り専用で送る（起動のたびに入れ替え。途中では更新しない）。基準コミット（と未コミットの変更の有無）を manifest の `shared` に記録し、`~/shared/ROOM.md` に案内を置く。あわせて、部屋の `~/.claude/CLAUDE.md`（Claude Code が作業ディレクトリによらず読む）に `ROOM.md` への案内を、目印（`room-shared:begin`〜`end`）で囲んだ範囲だけ入れ替えて置く（ほかの内容は変えない）。`resources/` が無ければ送らない。部屋の `~/.claude/CLAUDE.md` に案内を、`~/.claude/settings.json` に `Read(~/shared/**)` の許可（読み取りだけ）を足す |
| `close` | マウントが無いこと、`ai/out/close.md`（部屋の AI が書く）を確認 → 【案件】を Area の `ai/docs/inbox.md` に追記（重複しない。inbox が無ければ作らず、警告して【案件】を画面に出す。`init` で作る）→ README を `status: done`、`closed`、`reap_after` に → Area の一覧を「完了した Project」に → ファイル単位の `git mv` で `archives/` へ（追跡外の `_noai/` も移す） |
| `mask` | `_noai/raw/` の新しい・変わった原本（csv・md・txt・xlsx・pptx）を、`_noai/mask.toml` に従ってマスクし `ai/in/` へ。manifest に原本・マスク後・`mask.toml` のハッシュと対応表の版を記録。語が残っていれば止める（`start` の最初でも自動で行う） |
| `restore` | `ai/out/` を復元して `_noai/final/` へ。戻らないプレースホルダー・未知の形式があれば、何も書かずに一覧を出して止める。`_noai/final/` を人が前回の復元から変えていたときも止める（`--force` で上書き。前回の書き出しのハッシュは `_noai/map/final-manifest.json`）。`start` の終わりでも自動で行う。**`ai/out/knowledge/` の下は、復元したあと Area の知識置き場にも書く**（知識置き場が無ければ作らず、警告して Area には書かない。`init` で作ってからやり直す。2026-10-21。単体テストと実機の通し試験で問題なし。部屋の AI が統合した知識を、実名に戻して Area に置く）。ファイル名にプレースホルダーが残る、置き場の外を指す、場合は何も書かずに止まる。前回の書き出し（`_noai/map/knowledge-manifest.json` のハッシュ）から人が変えた既存ファイルがあれば、何も書かずに止まる（`--force` で上書き。直前の版は `_noai/final/_prev/knowledge/` に退避する。2026-10-21 に、警告から止める仕様に変えた） |
| `pull` | `pull <Project> [--where <項目>=<値> …] [--yes]`（2026-10-21。単体テストと、実機の通し試験（ダミーの Area `pilot2`、ユーザー）で問題なし）: Area の知識置き場（`areas/<Area>/knowledge/`。README の `knowledge_dest:` で変える。Area の外は拒否）から、`status: active`（無ければ active 扱い）で、`--where` に全部合う（AND。リストの項目は要素に一致）ファイルの一覧を出し、人が確認して（`--yes` で省略）`_noai/raw/area/` に写す。**実名を読むので人が実行する**。ファイル名は実名を含みうるので、部屋に渡る名前は `<日付>-<元の相対パスのハッシュ>.md` にし、元の名前は `_noai/map/pull-sources.json`（部屋に渡らない）に置く。manifest の `masked_from` には名前を書かない。`data: restore` の Project だけ。マスクは `mask`（`start` でも自動）。今回の条件に合わなくなった前回の分は、`_noai/raw/area/` から手で消す |
| `readme` | 部屋の AI が書いた `ai/out/readme-draft.md`（本文だけ）を、`README.md` の本文に反映する（frontmatter は変えず、`updated` だけ今日にする。確認あり、`--yes` で省略）。`open` の判断部分（目的・完了条件）を AI が下書きする形 |
| `stock` | 部屋の AI の【汎用】の下書き（`ai/out/stock/*.md`）を、**1件ずつ人が確認して**（`--yes` で省略）`resources/exmem/inbox/` に運ぶ。frontmatter に `base_commit` と `observed` が要る。対応表の語を含む下書きは運ばない。基準以降に統合先の `lessons/` が変わっていれば、frontmatter に `base_stale` を足す（`kind: explain` の下書きは、`guides/explain/` への新規作成だけなので足さない。`kind` はそのまま運ぶ）。運んだものは manifest の `stock` に記録し（同じ内容は二度運ばない）、未追跡のまま残す（コミットしない: `stock-hook.md` の方針） |
| `rename-area` | `rename-area <旧> <新>`: `areas/<旧>/` を `areas/<新>/` に移し（追跡外のファイルも）、その Area の Project（`projects/` と `archives/`）の README の `area:` と `[[areas/<旧>/…]]` のリンク、`ai/records/manifest.json` の来歴の `area` を書き換える。新しい名前は英数字・`_`・`-` だけ（`room-<新>` になるため）。新しい名前がすでにある、旧 Area が無い、旧の部屋にマウントが残っている、のいずれかなら何も変えずに止まる。**部屋は触らない**: `room-<旧>` は不要なら手で消し（`wsl --unregister`）、`room init <新>` で作り直す。`room-log.md` の過去の行は書き換えない。既定でコミットする（`--no-commit` で省く） |
| `umount` | 部屋に残った `/mnt/room/*` のマウントを外す |

`start --adopt` は、`ai/in/` の現在のファイルを、この Project の入力として人が確認したと manifest に記録する（マスクを通さない入力用）。`start --yes` は、`mask.toml` が変わったときの `ai/in/` 作り直しの確認を省く。`--no-launch` は、起動せずにマウントしたまま待つ（Zed の WSL リモートで使うとき。Enter で、アンマウントと回収に進む）。待つ間、部屋が止まってマウントが消えないよう、部屋で `sleep infinity` を動かす（実機で確認済み: 2026-10-18。待つ間マウントは残り、Enter で戻る。`wsl.exe` はコンソールから切り離して起こす）。

## データの扱い（`data:`。2026-10-19）

Project の README の frontmatter `data:` で決める（`open --data`。既定は全 type で `none`。`data:` が無い既存の Project は、これまでの動きを保つため `restore`）。`type` とは別の軸。

| `data:` | 使う場面 | `_noai/` の中身 | `start` / `mask` / `restore` |
|---|---|---|---|
| `none` | 機密なし。実データを使わない | `user/` だけ | マスクも復元もしない。`_noai/raw/` に原本があれば止める |
| `mask` | 顧客情報を含む資料の要約・抽出（読むのは本人だけ） | `raw/` `map/` `user/` | マスクだけ。復元しない（`final/` は無い）。成果物は `ai/work/` でも `ai/out/` でもよい |
| `restore` | マスクして、あとで実データに戻す | `raw/` `map/` `final/` `user/` | マスクして、終了時に復元（今までどおり） |

- `user/` は人だけが使う仮置き（予約名。`room` は触らない）。`_noai/` 全体が追跡外で、AI にも見せない。
- `type: dev` は `data: none` だけが仕様。`dev` で `mask` / `restore` にすると、`open` と `start` が警告する（止めない）。

## 実装の決まり

- WSL へのコマンドは、標準入力で LF 固定で渡す（PowerShell の CRLF で、`umount` が壊れ、マウントが積み重なる）。値は `shlex.quote` で引用する。
- 標準ライブラリだけ。Python は uv で固定する（`.python-version`、`pyproject.toml` の `requires-python`、`uv.lock`）。
- Windows の読み取り専用ファイルは、`chmod` を戻してから消す（`rmtree` が黙って失敗するため）。

## テスト

```powershell
uv run python -m unittest discover -s tests
```

実機（Excel）でマスク・復元を確かめるための架空のダミー（ピボット、コメント、定義名、通常+太字の run をまたぐ語を含む xlsx と、cp932 の csv、`mask.toml`）は、`python tests/dummy_fixture.py <Project のディレクトリ>` で `<Project>/_noai/` に作る（単体テストの対象ではない）。

WSL は差し替えて、一時ディレクトリの git で行う（実際の部屋には触れない）。実際の部屋での通し（`open → start → close`）は、使い捨ての works で手動で行った（2026-10-12）。

## マスク・復元（`maskkit.py`）

仕様は `mask-spec.md`（同じディレクトリ）。ファイルは Project の中に置く。

| ファイル | 内容 | git |
|---|---|---|
| `_noai/mask.toml` | 人が書く。`[terms.<種類>] キー = ["正式名", "表記ゆれ", …]`、`[columns] "シート!列名" = "種類"` | しない |
| `_noai/map/mapping.json` | `room` が書く。番号の追記専用の対応表 | しない |
| `_noai/final/` | 復元済みの成果物 | しない |

- プレースホルダー: 本文は `⟦CUST_001⟧`、シート名・定義名は ASCII の `SHEET_001` / `NAME_001`。番号は自動採番で、一度振ったら変わらない。
- 一致は広い（部分一致、大文字小文字・全角半角を区別しない）。長い語を優先して1回で置換する。1文字の語は受け付けない。
- シート名・定義名が語と同じ・語を含むときは、名前全体を `SHEET_` / `NAME_` にする（本文の同じ語もそちらに置換される）。
- xlsx: zip の中の `.xml` / `.rels` / `.vml` を置換。作成者・最終更新者・会社・管理者は常に空にする。プリンタ設定（`printerSettings*.bin`）は削除する。語が複数の書式（run）にまたがる文字列は、1つの run にまとめてから置換する（警告に出る）。点検は全 part と、run を連結した文字列で行う。
- csv: `utf-8-sig` → `cp932` の順に読み、`utf-8-sig` で書く。
- 候補: 法人格・敬称・メール・電話・URL・郵便番号の形は、対応表に無くても警告に出す（止めない）。
- 復元: 説明文などで `⟦` `⟧` が壊れた形（例: `⟦CUST_nnn⟧`）で残ると止まる。部屋の `ROOM.md` に、書かないよう指示してある（2026-10-19）。
- 復元: csv・md・txt・bas・json・html は文字列、xlsx は zip。`ai/out/close.md` と `ai/out/stock/` は対象外。ピボットは Excel の「すべて更新」が要る（人が PC で）。

## 未実装

- reap で、消す前に会話履歴を記録に写す（今は写さずに消す）
- `/home/ai` を開いたときの会話履歴（`-home-ai`）は、Project に紐づかないので `reap` は消さない。残っていれば警告するだけ
- 部屋の作成のうち、ログイン（人の操作）の自動化
