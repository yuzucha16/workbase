# 作業ログの経緯（log-history）

## Log

### 2026-11-06(マウントが残る件を期日へ移管)
- ユーザーの決定: マウントが残る件の NA を `docs/due.md` へ移し、期日 11-13 で 1 週間様子を見る。期日までに再発したら、`room-log.md` のつかむプロセスで調査する。再発しなければ、`unmount()` の再試行と記録の追加を今回の対応として close する。トピックの Next Actions は空になった(`due.md` に 11-11、11-12、11-13 の 3 件が残る)。11-13 は割り付けの上限(1 日 2 件)を超えるが、ユーザーの指定を優先した。

### 2026-11-06(マウントが残る件の原因調査。NA は調査中のまま残す)
- ユーザーの見立て(Zed の remote server が、プロセスをつかむ)を仮説として調べた。`room-myenv` に使い捨てのマウントを作って試すと、cwd がマウント上の子プロセスが生きている間は `umount: target is busy`(rc=32)で残り、子が終われば外れた。`unmount()` は `2>/dev/null || break` で、この失敗を黙って捨てていた。
- Zed だけが原因ではない。全 Project の `room-log.md` に「マウントが残っている」が 9 件あり、10-25(Zed 以前)の `sample_inv` `sample_dev` ほかと、11-05〜06 の `claude -p` の回を含む。調査の時点で、残ったマウント(`sample_inv` `sample_inveg1`)をつかむ実プロセスは無く、`zed-remote-server` は defunct のみだった。一時的な busy と整合する。
- 直した: `unmount()` を 1 秒おき 10 回の再試行にし、残ったらつかむプロセス(cwd・fd)を `room-log.md` と標準出力に出す(`room.py`、テスト追加。部屋のテスト 243 件 OK、実機で再試行と検出を確認)。コミット `be1a7e4`(`room.py` 本体は並行セッションの `0f6632f` に含まれた)。原因の確定は、次に残ったときの記録による。

### 2026-11-06(「quarto/revealjs で」の追試。NA 3 を閉じる)
- 「pptx で」と同じ依頼で、形式の言葉だけ「quarto/revealjs で」に変えて試験。初回は `out/` 直下に `.qmd` と html が出た(`publish/` なし、`report.md` なし)。原因は、`claude -p` の部屋のエージェントが `~/shared` の手順書を読まないこと。規則を常に読まれる案内文(`room.py` の `POINTER_TEXT`)に置き、`project-structure.md` の `inv` の補足に「形式によらず `report.md` を本体、清書物は `publish/`。軽い依頼は `question.md` を作らない。情報源は 1〜2 件なら `sources.md`、3 件以上なら `sources/sources.md`」を足した(ユーザーの指示)。再試 8 回のうち、基準の文を強めた後の quarto・pptx 各 1 回は同じ構成。知見は `exmem/inbox/2026-11-06-claude-p-ignores-shared-docs.md`(未統合)。結果は `records/2026-11-06-inv-quarto-explicit-result.md`(コミット `0f6632f` ほか)。

### 2026-11-06(並行 room start の競合。NA 2 を閉じる)
- 原因は、並行する 2 つの start が同じ `~/shared.new` と `~/shared.old` を消し合うこと。`room.py` の `push_shared` で、送付を部屋の `flock`(`~/.shared.lock`)の下で直列にした(単体テスト 188 件通過)。ユーザーが実機で 2 Project の同時 `room start` を確認し、起動できた。NA 4(人の確認: `umount --area` の失敗)は対応済みとして閉じた。

### 2026-11-06(分割して進める試験)
- `dev`(csvinfo)と `inv`(uv と pip-tools)で、新しいセッション 6 回(6R → 論点出し → 判断と承認 → 工程 → 工程 → 終える)を実施。同じ観点で動けた。足りない点 3 つ(成果物名、`inv` の `src/`、承認後の 6R の書き換え)を `project-structure.md` などに反映し、新 Project で 3 回目まで再試験して解消を確認。結果は `records/2026-11-06-split-test-result.md`。ユーザーが反映と `env/` の扱いを承認。コミット 08b8fd0。

### 2026-11-05(eg2 の room 版。NA 1 を閉じる)
- `myenv`(internal)の `sample_inveg2` で、`mask`(cp932 が通り、UTF-8 に変換)→ `start --adopt --cmd`(`claude -p`)→ `restore` を実行。聞き返し 0、構成は部屋なしと同じで過不足なし、結論の数字も一致(`records/2026-11-05-inv-eg2-room-result.md`)。AI の改善提案 5 点は反映未決。`close` は非対話で警告(README ひな形、`close.md` 無し)に止まり、ユーザーが端末から実行した。
- ユーザーが、複数工程を分割して進めるときの初手プロンプトの試験を NA に追加(別セッションで行う)。
- ユーザーが eg2 の指摘 5 点の反映を承認。`project-structure.md` の `inv` の補足に追記(`decisions.md`)。

### 2026-11-05(「pptx で」の追試)
- C の追試(`records/2026-11-05-inv-pptx-explicit-result.md`)。部屋 `room-myenv` の `sample_invP` で「報告資料にして、pptx で」と明示すると `publish/` に pptx と `deck.js` が出た(聞き返し 0)。quickref の清書の行に反映(a757975)。NA 「C の追試」を閉じた。ユーザーが次の追試(quarto/revealjs)を NA に起票。
- 取り違え: 最初に Area を env-external で作り、works で revert した(`env-external` の `ai/` の未追跡はユーザーが処理)。

### 2026-11-05(`inv` の工程の組み合わせ試験。NA 2 を閉じる)
- 部屋 `room-myenv` で `sample_invA/B/C` を `claude -p`(`room start --cmd`)で通した。重さの言葉だけで頼み、A は `report.md` のみ、B は＋`sources/` `findings/`、C は＋`checks/`。置き場は 3 件とも `ai/out/<Project 名>/`、聞き返し 0(`records/2026-11-05-inv-combo-test-result.md`、設計は同日の `-design.md`)。`claude -p` は `--permission-mode acceptEdits --allowedTools ...` とプロンプトの stdin 渡しが要る。
- ユーザーが指摘 3 点を採用(`decisions.md`)。`project-structure.md` に反映。`sample_inv*` を削除。依頼の書き方を `guides/quickref/ai-work-prompts.md` に追加。C の「pptx で」追試を NA に起票(11-18)。コミット `f40966d` ほか。

### 2026-11-05（eg2: 社内 Excel 想定の CSV 分析。NA 1 を閉じる）
- 国勢調査の男女別人口 c01.csv を、部屋なしで `inv` の構成要素を再現して分析→示唆まで 1 周した（`records/2026-11-05-inv-eg2-population-csv.md`）。マスクは、公開データで対象が無く、ユーザーが「不要」と判断。
- ユーザー「良いです」: 構造への提案 4 点を `project-structure.md` に反映（`checks/` の取り込みの落とし穴、台帳の URL 無しの書き方、スクリプトの置き場 `ai/work/scripts/`、仮定の書き方）。
- ユーザーが、部屋ありで eg2 をもう一度行う案を挙げた（実施は未定）。

### 2026-11-04（oq1 を omit、oq2 の手順の叩き台）
- oq1（`inv` の基準文書は仮決め）: ユーザー「omit。na の中で修正していく」。
- oq2（Quarto の `reference-doc`）: ユーザー「ここで具体化したい。基準のマスタースライドとサンプルレイアウトは持っている」。手順 7 段の叩き台を作ったが、同日にユーザーの指示で `topics/office-output-types` に移管した（`records/` と NA 7）。

### 2026-11-04（na2・na4 を閉じた）
- na2（比較の結果を office-output-types に渡す）: ユーザー「quarto を主、marp 規定を副とした。どちらも room init で導入できる」。`topics/office-output-types` の `docs/decisions.md` と `docs/log-history.md` に追記して close。
- na4（部屋に残る Slidev の削除）: ユーザーが削除済みと報告。close。

### 2026-11-04（`inv` の工程の組み合わせ試験を起票した）
- ユーザーの依頼: office-output-types の NA 6（Quarto で 1 サンプル）の続きとして、`dev` の a) `src` のみ、b) `env`+`src`、c) `src`+`env`+`tests` と同じ形の組み合わせ試験を `inv` 版で行う。Next Actions に起票（期日 11-11）。
- `docs/due.md` の「Marp と Slidev を人が導入して比較」の行（比較は済み）を、この試験の行に置き換えた。eg2 は別の項目のまま。

### 2026-11-04（`init` に Marp CLI の段を追加した）

- `room.py` に `MARP_INSTALL`（`marp-cli@4.5.1` を root が npm で固定、`PUPPETEER_SKIP_DOWNLOAD=1`）と段 `marp`（Quarto の後）を追加。`/usr/local/bin/room-marp` が `room-chrome` を `--browser-path` で指す包み。呼ぶ側は `</dev/null`。`room/README.md` と単体テストも更新。
- 確認: 単体テスト 183 件 OK。`init myenv --only marp` の実機で、日本語 md → pptx（76KB）、`--version` 4.5.1。`python -I -m unittest` は `tests` を import できず、`uv run python -m unittest tests.test_room` で実行する。
- 完了した Next Action: 「`init` に Marp CLI の段を足す」（根拠: 上のコミット）。

### 2026-11-04（Marp・Slidev・Quarto の実機比較を済ませた）

- 部屋に Marp CLI 4.5.1 と Slidev 53.0.0 を、人が root で入れた（`ai` は `/usr/local` に書けない。PowerShell の二重引用符で `$d` が空になり 1 回やり直し）。Marp は `--browser-path /usr/local/bin/room-chrome` が要る。Slidev は、テーマ・`playwright-chromium`（リビジョン 1248 で部屋と一致）・Vite のキャッシュ用フォルダ（`.vite`）が要った。
- 結果と示唆は `records/2026-11-04-slide-tools-live-compare.md`: 編集できる pptx は Quarto だけ。Marp・Slidev の pptx は画像（ノートは入る）。Marp の `--pptx-editable` は表・ノート・日本語の字形に問題。見た目は Marp の組み込みテーマが整い、Slidev は既定だと素朴。Quarto は素の Office 風で、人の微修正向き。
- ユーザーの方針: Quarto と Marp 既定を部屋に入れて使い分ける。`init` への Marp 追加を承認。Slidev を含む不要物は消す（`~/cmp` は消した。グローバルの Slidev は root が要るので人へ）。
- 完了した Next Action: 「Marp と Slidev を部屋に入れて Quarto と横並びで実機比較する」（根拠: 上の records）。結果の引き渡し（`office-output-types`）は残した。

### 2026-11-04（eg1 の結果を確認し、`inv` の構造を直した）
- 部屋の成果物（`out/compare-slide-tools/`）と工程ログを読んだ。調査は筋が通り、6 工程の構成要素は使われた（所要は約 25 分）。弱い点は、Marp と Slidev が文書のみ、裏取りが語句の grep まで、report の出典欄に S3・S13 が無いこと。記録は `records/2026-11-04-inv-slide-tools-compare-result.md`。
- ユーザーの承認で、提案 1・3・4（台帳に「実測」と取得失敗の欄、findings の行 ID、checks を 1 ファイル）を `project-structure.md` に反映。提案 2・5 は実験の依頼文で対応。`ai/in/` が空に見えたのはマウントポイントの差。
- npx の拒否は「人が事前に導入する」と決めた。Marp・Slidev の横並び比較を Next Actions に足した。決定は `decisions.md`。

### 2026-11-04（`inv` の工程別構造の素案を採用した）
- `dev` が `env/` `src/` `tests/` `docs/` と工程別なので、`inv` も工程別にする素案を出し、ユーザーが承認した（`decisions.md`）。構成要素は `question.md` `sources/` `findings/` `checks/` `report.md`、清書の `publish/`（ユーザーの追加。pptx まで成果物に含む）。`project-structure.md` に反映（コミット済み、叩き台）。
- 実験のお題を決めた: プレゼン資料作成ツールの比較（Marp、Quarto、Slidev）。AI 活用を想定した選定軸と作成時間短縮の方法。`topics/office-output-types` の markdown → pptx の検討のインプットになる。実験は別セッションで観点別に行う（`log.md` の Next Actions）。
- 【同日の後半】eg1 の依頼文と `question.md` 初稿を `records/2026-11-04-inv-slide-tools-compare-request.md` に保存し、ユーザーが部屋へ渡した（Project `compare-slide-tools`、external。`ai/in/` に Quarto の調査と雛形 pptx を置いた）。返答は別セッションで見せてもらう。

### 2026-11-04（案 A の実機確認と置き場の実測。別セッション `claude -p` を `room start --cmd` で起動して測った）
- 【同日の後半】実測を受けた判断 3 点を決めた（`decisions.md`）。`project-structure.md` に予約名 `deliverable` と逃げ道（専用サブディレクトリ＋README の記録）を足し、`git -C` を「望ましい」に緩めた（`room.py` の `ROOM.md` 雛形も）。成果物名の衝突は `routes()` が Project 名の下に固定するので起きない。`due.md` の 11-11 の行を消した。
- 方法: 部屋 `room-myenv` に使い捨てのローカル bare と clone（`~/src/probe-repo`。`CLAUDE.md` に合言葉）を作り、Project `rtc-probe`（`repos:` 付き）で ①〜⑤、`rtc-calc-*`（`repos:` なし）でケース A・B・C を通した。依頼に置き場は書かない。`--cmd` の中の `$(cat …)` は cwd が移る前に展開されるので絶対パス（`/mnt/room/<名>/work/prompt.txt`）で渡す。マウントが残ったら `room umount --area myenv`。
- 案 A（`due.md` の 5 点）: ① `--add-dir` と `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` が付き、`CLAUDE.md` の合言葉を AI が引用した（OK）。② `git -C` の commit は clone の `main` に入り、`ai/` 側に化けない（OK。回収の変更にコードは出ない）。③ `ROOM.md` が届き、置き場の取り違えは A・B・C 計 5 回中 1 回（A で `ai/` 直下）。④ `room close` は未 push の clone で止まる（OK）。⑤ 対話で `cd … && git` が承認なしで通り、cwd は `~/src/probe-repo` に移って持続した（`claude -p` では承認待ちで止まる）。AI は `ROOM.md` の「`git -C` を使う」を守っていない。
- ケース A・B・C（規則なし）: 成果物名は 3 件とも `calc`、置き場は `ai/out/calc/`。A は 1 ファイル、B は平ら（`calc.py` `test_calc.py` `README.md`）、C は `src/` `tests/` `pyproject.toml` `uv.lock` `README.md` `report.md`（`env/` `docs/` は使わない）。聞き返し 0 件。`dev-deliverable-guide.md` だけに規則を書いても AI は読まず、効かなかった（ユーザー承認で書いた）。
- 規則を `ROOM.md` の雛形（`room.py`）に足して再測（ユーザー承認）: A は `ai/calc.py`（誤配置）、B は `ai/out/calc/src` `tests`（名前は `calc`）、C は `ai/out/rtc-calc-c/`（Project 名と同じ）。A の追試 2 回は `ai/out/calc/`（名前 `calc`）。規則あり 5 回中、Project 名と同じは 1 回。`ai/` 直下はばらつきの範囲と見る。
- ユーザーの決定: A の追試後に測定を切る。使い捨ての Project 6 つ、部屋の clone と bare を削除した。works 側に `rtc-probe` の削除が未コミットで残る（works の git）。費用は 1 回 $0.05〜$0.32。
- 変更（kit）: `workflow-kit/dev-deliverable-guide.md` に `<成果物名>` の既定、`workflow-kit/room/room.py` の `ROOM.md` 雛形に同じ文。

### 2026-11-04（Vault 2 分割の実装を close した）
- `git -C` 緩和の反映を確かめた: `ROOM.md` は `room start` ごとに `ROOM_GUIDE`（`room.py`）から作り直されるので、既存の部屋は次の `start` で反映される。`mkworks --update` は不要。`templates/workspace/` に `git -C` の記述は無く、`room/README.md` 43 行は緩和後の文。実機の `start` は未確認。
- PC2 でも `30_link.bat` を実機で実行し、問題なし（ユーザー）。PC1（11-02）と合わせて両 PC で確認済み。`docs/due.md` の 11-09 の行（Vault 2 分割の実装）は消した。

### 2026-11-02（Vault の 2 分割の前提を確認し、正式化して dotfiles に実装した）
- PC1 の実機（ユーザー）: 除外フィルタで resources は検索・リンクから外れる（エクスプローラーには残る。受け入れ）。入れ子の `.obsidian` は独立。pc1 のリンク調査は `resources/` を指すもの 0 本。`30_link.bat` が止まるのは実ファイルがあるときだけ（ジャンクションは上書き）。dotfiles の `.obsidian` の写し先は works（決定）。
- 正式化（ユーザー）。workbase は `.gitignore` に `/.obsidian`。文面直しは NA に分けて積んだ（一覧は `decisions.md`）。コミット `edc30d6` `9522a09` `2acc516` `3b0be80`。
- dotfiles（`yuzucha16/dotfiles`）に実装（`3946432`）: `windows/obsidian/{resources,works}/.obsidian`、`scripts/obsidian_sync.py`（正本から works の共通分を生成。`--check` `-n`）、`links.map` の 2 本（resources 側は `|noparent`）、`30_link.bat` `30_link.sh`、`.gitignore`、試験 75 項目（Linux で通過）、README と `docs/`。`30_link.bat` の新分岐は Windows の実機で未確認。
- 追加（ユーザーの依頼）: works のエクスプローラーから `resources` `resources_p` `repos` を CSS スニペットで隠し（dotfiles `f39f625`）、実機で消えたことを確認。重さは感じないので `resources_p/` も除外フィルタに足した。

### 2026-11-01（`<成果物名>` の決め方を案 1 にし、置き場の実測を 11-05 に統合した）
- Open Questions の「サーバー側で AI を動かす形」を外した（ユーザー: 不要）。
- 論点（AI が置き場を認識しているか、工程の組み合わせで正しく使えるか、聞き返すか）と進め方（ケース A・B・C、判定 3 点、規則なし→規則あり）をユーザーが承認した。実測の入口で「`ai/out/<成果物名>/` の階層は 1:1 なら要らないのでは」と出て、階層は `ai/out/` 直下の予約物との混在と `restore` の置換単位のために残すと確認し、名前は「外部にそのまま出せる形」、既定は Project 名と同じに決めた。
- 「Project 名と同じ」で AI が grep・find で迷うかは、推論では問題なし(パスに `ai/out/` が挟まるので区別できる。`find -name` で 2 件当たるだけ)で、未測。11-05 の実測の観察点に足した。
- 期日: 旧 11-07 の「聞き返すか」を 11-05 に統合(`docs/due.md`)。コミット `2c47047`。

### 2026-11-01（`target:` の書式と `ai/in/target/` の一覧を決めた）
- ユーザーの前提: 接続先が room の WSL でも別の Linux 機でも、ssh で繋ぐかどうかの差でしかない。素案（`name`、`via: ssh|wsl`、`os`、`note`。`ai/in/target/` は `env.md`、`run-YYYY-MM-DD.md`、秘匿値抜きの設定サンプル）をユーザーが承認した（「私のイメージ通り」）。
- `workflow-kit/project-structure.md` の「開発リポジトリ」の節に反映した。根拠は `decisions.md` の同日の項。処理する側（`room.py`）は作っていない。Open Questions の該当の行は消した。コミット `8ce141f`。

### 2026-11-01（`review 消化`: Vault 2 分割を【保留】にし、works の再定義を `obsidian-vault-structure.md` に反映した）
- スクリーニング（サブエージェント 1 回）の結果、ユーザーが 3 論点とも保留（期日 11-08）。内容は `decisions.md` の同日の項の先頭。
- `exmem/lessons/obsidian-vault-structure.md` に、works の再定義（10-31）と、2 分割が保留であることを足した。図は 1 Vault のまま。
- Next Actions の `src/` 実測と案 A の実機確認は、ユーザーの指定で期日 11-05 になり、`docs/due.md` に移した。log 先頭の段落は縮めた（経緯はこの履歴にある）。

### 2026-11-01（Obsidian の Vault を 2 つに分ける案を仮決めした。記録のみで、実装は未着手）
- ユーザーの相談: pc2 は resources（workbase）の改良が主、pc1 は areas・projects が主なので、`works/.obsidian` を `resources/.obsidian` と `projects/.obsidian` に分けたい。事実の確認: `.obsidian` は dotfiles へのジャンクション、プラグインは 3 つ（`colored-tags` `html-viewer` `xlsx-viewer`、約 240KB）、`workspace.json` は dotfiles で追跡対象外。pc2 で `resources/` の外の md 92 ファイルの `[[リンク]]` 47 件を数え、`resources/` を指すものは 0 件。
- 仮決め: Vault は `resources/`（md のみ）と `works/`（projects・areas・`resources_p/`。`resources/` `archives/` `repos/` を除外）の 2 つ。`areas/` が works 直下で `projects/` と並ぶため、`projects/` だけの Vault にはしなかった。実体は両方 dotfiles に置き、ジャンクションで張る（ユーザーの補足で、私が「workbase が追跡するか」と読み違えた点を直した）。resources 用が正本で、works 用の共通ファイルは派生物として生成し、追跡しない。works だけ違う項目は `app.override.json`。リンク適用時に自動、手動でも可、`--check` で点検（ユーザー「この形はいいですね」）。根拠は `decisions.md` の同日の項。
- 未着手: 入れ子の Vault の実機確認、今の `.obsidian` の移し先の決定、dotfiles の実装（別コミット）。

### 2026-11-01（deploy key の手順書を作り、ユーザーが手で通して確認した。Next Action「deploy key の再実施」を閉じた）
- 作成: `guides/howto/room-github-deploy-key-setup.md`（`howto` の型。構成案をユーザーが了承。リポジトリ名などは `<owner>` `<repo>` のプレースホルダー）。`guides/guides-index.md` に 2 か所追記。
- ユーザーの確認で直した点: 指紋の照合は、`/tmp/gh_hostkey`（公開鍵そのもの）でなく、`ssh-keygen -lf` が出した `SHA256:…` を、`gh api meta` の ED25519 の値と比べる（HTTPS 経由で SSH と独立）。read only の確認は `gh repo deploy-key list` でなく `gh api repos/<owner>/<repo>/keys --jq '.[] | {title, read_only}'`（`true`）。
- 閉じた根拠: ユーザーが章 4〜7（指紋、`read_only`、clone と push の拒否、片付け）を実機で通し、「na3 は close」と指示。`deploy-key add` の read only 登録と、公開鍵の受け渡しも通った。

### 2026-10-31（案 A の実装。実機の確認は 1 Project の実測にまとめる）
- `a9d03cc`: `room start` が `claude` のとき `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` と、README の `repos:`（`where: wsl`）の `~/src/<repo>` への `--add-dir` を渡す（`read_repos` `claude_extra_args`。clone が無ければ注意して渡さない）。
- `721f3f9`: `ROOM_GUIDE` に `git -C ~/src/<repo>` と push 不可、`project-structure.md` に `repos:` の節、`ai-isolated-work-room.md` の Decisions に案 A、`room open` の README 雛形に `repos:` の案内。`room close` が `repos:` の clone の未コミット・未 push で止まる（`unpushed_repos`）。単体テストは 143 件 OK（3 件スキップ）。
- 動作確認は単体テストまで。実機の確認は、ユーザーが「1 Project で `env/` `tests/` `docs/` を通す実測」の Next Action に `src/`（コード開発）を含めてまとめて行う（「上の na には src/ に関する実測が無かったので、今回のコード開発も含めてやってみます」）。

### 2026-10-31（案 A の実測。git ラッパーを直し、cwd 固定の案 A に決定）
- 実測（`room-myenv`、`claude -p`、cwd=`/mnt/room/sample_dev`、使い捨ての `~/src/probe-repo`）: `--add-dir` あり→読み書きできる、なし→拒否。`records` は cwd が `/mnt/room/` のままなので `ai/records` に出る。追加ディレクトリの `CLAUDE.md` は既定では読まれず、`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` で読まれる。
- 見つけた問題: `ROOM_GIT_WRAPPER` が `$PWD` だけで判定し、cwd が `/mnt/room/` のとき `git -C ~/src/<repo>` が部屋用 git（`~/gitdirs/<Project>`）に化けた（AI の commit が `ai/` に入る）。`cd ~/src/<repo> && git` は正しいが、承認待ちで止まる（非対話）。
- 議論: 私は案 B（コード作業は cwd=`~/src/<repo>`）を推したが、ユーザーが「`ai/<成果物>/env` のように `~/src` より前の工程では cwd が変わるのは違和感」「`records` を一か所に纏めたい」と指摘。ジレンマ（コード開発なら B、ソフト開発全般と room の設計思想なら A）を整理し、A の影響範囲（変更は `ROOM_GIT_WRAPPER` の 1 か所、Area 共有の `/usr/local/bin/git` なので不具合は全 Project に出る）とリスクを示して、ユーザーが A を選択（「a にしましょう。すすめて」）。
- 実施（`83ecc18`）: ラッパーの判定を git の対象（cwd に `-C` を順に当てる）に変更。`--git-dir` `--work-tree` `--bare`、`GIT_DIR` 設定済み、`clone`、読み取れない引数は素通し。`RoomGitWrapperTest` を新設（偽 git で 15 ケース）、全 140 件 OK。実機で `git -C` の add/commit、ローカル clone、AI の commit が clone 側にだけ入ることを確認。実機の `/usr/local/bin/git` は新版に差し替え済み。計測用の clone・退避・一時ファイルは削除。
- 罠: PowerShell から `wsl` へ渡す文字列は CRLF になり、`/usr/local/bin/git` が壊れた（`/bin/sh^M`）。base64 で渡して直した。`claude -p` は標準入力を読むので、`bash -s` でスクリプトを渡すと食われる（`</dev/null` を付ける）。非対話では、`cd` 後の git と `--allowedTools` の書式（`"Bash(git:*)"` を 1 つずつ引用）で止まる。
- 区切り: 残りの実装（`room start` の環境変数、`repos:` の `--add-dir`）は別セッションで行う（ユーザー）。

### 2026-10-31（WSL からの認証の確認を受けて、works の再定義と置き場を決めた）
- 確認: ユーザーが、WSL から認証が要る clone を通せることを確認した。WSL にリポジトリを置く前提の仕様の確認。
- 決定（`decisions.md` の「works の再定義と開発リポジトリの置き場」）: works（Vault）と workbase は 1:1。works と projects は 1:N の PC ローカルの台帳。`dev` のリポジトリは、開発環境（IDE）のある OS に置く（今は WSL だけ）。`repos:` に `where: wsl|win|linux` を持たせる。clone は `~/src/<repo>`、git で管理しないコードは `ai/out/<成果物名>/src/`。`ai/` のマウントは続け、cwd は `/mnt/room/<Project>` のまま `~/src/<repo>` を追加ディレクトリで渡す（案 A、実測前）。room から開発サーバーへ SSH しない。人が SSH して、窓口は `ai/in/target/` と README の `target:`。サーバー側で AI を動かす形は対象外。
- 閉じた論点: 旧 Open Questions 1〜6（3 は 10-31 に決定済み、4 は pc2 を非公開にして削除するので閉じた）。`ai/src` と呼んでいた置き場は `ai/out/<成果物名>/src/` で合っている（`project-structure.md` の `dev` の構成）。
- 補足: Obsidian の Vault は works 全体なので、`inv` の markdown を Obsidian で開くのは矛盾しない。「Obsidian が見るのは `resources/`」とは書かず、「works の中に workbase が `resources/` として入る」と書く。
- ユーザーの指示: deploy key の再実施は優先度を下げる（手すきで）。手順書にするかは置いておく。次は案 A の実測を別セッションで行う。

### 2026-10-31（room の非公開リポジトリの認証を実機で通した）
- 手順: ホストの `gh` で空の非公開リポジトリ `yuzucha16/room-auth-check` を作成。`room-myenv` の中で ed25519 の鍵を生成（`~/.ssh/id_room_authcheck`、パスフレーズなし、権限 600）。`~/.ssh/config` に別名 `github-authcheck`（`IdentitiesOnly yes`）を置き、known_hosts は `ssh-keyscan` の結果の指紋が GitHub 公開の値（`SHA256:+DiY3wvv…`）と一致することを見て採用。公開鍵を `gh api` で deploy key（read_only）として登録。
- 結果: room の中で `git clone git@github-authcheck:…` が通り、`push` は「The key you are authenticating with has been marked as read only」で拒否された（期待どおり）。
- 罠: PowerShell の here-string は CRLF。`wsl.exe … -- sh -s` に渡す前に `\r\n` を `\n` にする。
- `room close` は GitHub に触れない（`cmd_close` は remote を使わない）ため、認証の有無で結果は変わらない。「room 内の clone が全部 push 済み」の検査は未実装（Open Questions 3）。
- 部屋の内部 git（`~/gitdirs/<Project>`、`ROOM_GIT_WRAPPER`）との関係: ラッパーは `/mnt/room/<Project>` の下だけ `GIT_DIR` を差し替える。`~/src/<repo>` の clone と remote は影響を受けない。`room close` の `--commit` は works の git へのコミットで、部屋の内部 git ではない。3 者（works の git、部屋の内部 git、clone と remote）は無関係。
- ユーザーの決定: 確認用リポジトリは消す（作成は自分でもう一度やる）。C 案の却下理由の更新は了承。push は room に許さない（個人開発は許す・チーム開発は許さないの 2 パターンがあるので許さない方に倒す）。close の検査は足す。works の再定義と `repos:` は別トピックにする。
- 片付け: room 側の鍵、`~/.ssh`、clone は削除。GitHub 側の `room-auth-check` は `delete_repo` の権限が無く未削除（ユーザー作業）。
- 反映: `exmem/lessons/ai-isolated-work-room.md` の Decisions に 10-31 の決定を追記、10-13 の C 案の項に更新を指す注を付けた。
- 後続（ユーザー、同日）: 「別トピック」は「別セッションで続ける」の言い間違いで、トピックはここで続ける。Open Questions は見送る。GitHub の `room-auth-check` は削除済み。見送った論点（元の文）: ① works の再定義（works と workbase は 1:1、works と projects は 1:N の PC ローカルの台帳、成果物は `inv` が Office・`dev` が WSL 内の git リポジトリ N 個）。② Project の README に `repos:`（`url` `where` `branch`）を持たせるか。③ 閉じる条件に「room 内の clone が全部 push 済み」（決定済み、実装は ②⑤ の後だった）。④ pc2 の works の公開 remote を外すとき、公開済み成果物の切り出し先。⑤ clone の置き場（`~/src/<repo>`、`ai/src` との関係）。⑥ 影響する文書（`obsidian-vault-structure.md`、`room.py` の `open`、`project-structure.md`）。⑦ 置き場と対象環境を依頼に書かないとき AI が聞き返すかは未測。

### 2026-10-31（works の再定義の相談と、Zed から room の ext4 を扱えることの確認）
- ユーザーの問題提起: `open --type` の整理が発端。works が GitHub に公開・非公開どちらにもなり（pc1 は非公開、pc2 は公開）、リポジトリが works の 1 つに固定される。`inv`（Windows Office）と `dev`（Windows/Linux/WSL）の成果物があり、リポジトリ情報が Windows 側で、room のある WSL からファイルシステムを跨ぐ。複数のリポジトリを触る要望が pc1 で実際にあった。案は、works を remote なしの PC ローカルにし、開発用リポジトリを room 側で clone して 1:N にする。
- AI の初回の提案: 台帳（works、remote なし）／コード（room の `~/src/<repo>`、リポジトリごとの remote）／`inv` の成果物（works、公開するなら別リポジトリ）の 3 層。認証は room に読み取りだけ置き push は人、の案を推した（未決）。
- ユーザーの補足: works は Vault の写しとして始まった（`resources/` を参照するため）。今は Vault として要るのは `resources/` で、works 配下の markdown は主でない。works と workbase は 1:1、works と projects は 1:N の PC ローカルの台帳、という表現は正しい。今のルールに適合させるのでなく、この考えに既存のルールを合わせに行く。
- Zed の WSL 対応（公式 docs: `projects: open wsl`）。リモートの分担（UI はローカル、LSP・タスク・ターミナルはサーバー側）が WSL にも当てはまるとは docs に無かった。
- 実機の確認（ユーザー、10-31）: Windows の Zed から `room-myenv` に接続し、`ai` の `~` で `git clone` した `~/dotfiles`（公開リポジトリ）を読めた。`df -T` で ext4（`/dev/sdd`、マウント `/`）。続けて編集、LSP のハイライト、git の表示、Agent も動いた。「ext4 に置いたコードが Zed から見えない」懸念は解消。
- 未確認は、認証が要る（非公開の）リポジトリの clone / push。ユーザーが次回、SSH か `gh` かのベストプラクティスを聞くところから始める。
- 決定は書いていない（works の再定義は方針の整理の段階）。

### 2026-10-28（`dev` の成果物が `ai/work/` に出る件を、再現待ちで閉じた）
- ユーザーの判断で、10-26 起票の Next Actions（`dev` の成果物が `ai/work/` に出る件の原因の特定）を `log.md` から外した。理由: その後、部屋の AI が急に `ai/out/` に出すようになり、当時のセッションの情報を探すのが手間なため。原因は未特定のまま（候補は 10-26 の項の 3 つ）。
- 再現したら再開する。そのとき確かめること: ① 部屋の `~/shared/ROOM.md` の基準コミット（cfd3b81 より前か）。② その Project の README の成果物の行。③ 部屋の AI に「`ai/work/` に置いた理由と、そのとき読んだ手順書」を聞く。(1) 写しが修正前か (3) `script-guide.md` の `ai/work/` の記述が原因なら、`ROOM.md`（`room.py`）と `brief-work-types.md` に「コードやスクリプトも成果物は `ai/out/<成果物名>/`。`ai/work/` は捨ててよい下書きだけ」を明記する。
### 2026-10-28（wrap の新しい規則で log.md を掃除）
- `wrap` の新しい規則で、決まった Open Questions を移した。置き場の取り違え 5 回の原因は特定し（`ROOM.md` と `room-context.md` の `ai/out/deliverable/` の記述が `dev-deliverable-guide.md` と食い違う。`decisions.md`）、手順書は 10-25 に直した（再発の確認は Next Actions に残る）。`sample_devenv` への不具合の返却はしない（ユーザーの判断、10-25）。
### 2026-10-27（済みの Next Actions を log.md から移した）
10-25 に済んだ 7 件の詳細。(1) `report.md` の置き場: コードは `ai/out/deliverable/` だけ Area に、それ以外は `_noai/final/` に戻す。食い違いは `methods.md` の書き方だけだったので `ai/out/<成果物名>/report.md` に直した(決定は不要)。(2) 単一の問いの章立て(`brief-hook.md`、`research-method.md`)。(3) `dev` の「テスト」に文書と実装の食い違いを機械で検査する型を足した(ユーザー承認)。(4) `dev-deliverable-guide.md` の旧名(`dev-env` `dev-test`)の説明を削った(承認)。(5) `sample_devenv`: ENV-001〜010 全件 PASS、SET-001(root で中止)も確認。型は機能した。静的検査は shellcheck と ruff が部屋に無く `bash -n` まで。uv の版は固定していない。(6) `sample_devtest`(`ai/out/devenv-tests/`): 要求 14 ID に対応、65 件実行で PASS 62・FAIL 3・SKIP 1。観察は、質問の推奨の置き場が `work/` でガイドの `ai/out/<成果物名>/` と食い違った(人が正した)、テストを実装に合わせて緩めた件は変更前後と理由を `report.md` に書かせる依頼が要った、`tests/t_static.sh` が(3)の起票の 2 例目。同日、サブエージェントでループを回す案を見送りと決めた(トークン使用量を抑えるため。`decisions.md`)。(7) `sample_devdoc`: 「文書作成」の項は残す。基準文書の形を仮決め(`project-structure.md` の未決)。あわせて `room.py:1197`(`ROOM.md` の元)と `room-context.md:67` を「Area に実名で戻したい最終版だけ `deliverable/`。Project の成果物は `ai/out/<成果物名>/`」に直し、`brief-work-types.md` に `dev` の最初の `brief` で `project-structure.md` と `dev-deliverable-guide.md` を読む指示を足した(単体テスト 139 件 OK、skip 3)。

### 2026-10-26（`dev` の成果物が `ai/work/` に出る件の起票）
ユーザーが、PC1 の `dev` の部屋の AI が成果物をすべて `ai/work/` に出したと報告(一貫して `work/` だったので読み替えられたが、`work/` と `out/` が混ざると困る)。手順書を調べ、原因の候補を 3 つ挙げた(写しが修正前、`work` と `out` の線の曖昧さ、`script-guide.md` の `ai/work/` の記述の多さ)。PC1 の部屋は見られないため特定できず、ユーザーが「部屋の AI に聞くやり方で最適化しましょう」と決め、Next Actions に積んだ。同日、メモリの「次は考え方の文書」は、10-24 に済んでいたため直した(`project-structure.md` の「type の考え方」)。

### 2026-10-25（`env/` だけ・`tests/` だけ・`docs/` だけの実測と、置き場の取り違えの修正）
ユーザーが手元で 3 本を作り、AI の質問と成果物を見て手順書を直した。`sample_devenv`(Ubuntu 24.04 実機で ENV-001〜010 全件 PASS、SET-001 も中止を確認)、`sample_devtest`(要求 14 ID に対応、65 件実行で不具合 3 件と仕様の曖昧さ 2 件。`ai/in/` は不変)、`sample_devdoc`(骨子と図の要否を聞いた。基準文書の形を仮決め)。置き場の取り違えが 5 回(`work/`、`deliverable/` 3 回、README、レビュー版を `ai/docs/`)。部屋の AI に読んだ手順書を聞き、原因は `ROOM.md`/`room-context.md` の「人が読む最終版は `deliverable/`」と、`project-structure.md` を読んでいないことと分かった。直した(単体テスト 139 件 OK)。旧名の説明の削除、`dev` の「テスト」に文書と実装の整合の検査の型、`brief-work-types.md` に `project-structure.md` を読む指示も同日。決定は `decisions.md`。確認待ちは、直した `ROOM.md` で次の `dev` が取り違えないか。

### 2026-10-25（最初の実利用の観察を受けた手順書の修正）

`sample_dev`（`src/ env/ tests/ tools/ docs/` の CLI）と `sample_inv`（Obsidian の wikilink の調査）で観察した。両方で出た指摘を直した: `room open` が `docs/` の 3 つの雛形を置く（テスト 123 件合格）、`ai/X` の読み替え（`room-context.md`）、`docs/` の中身を 3 つに揃える（`project-structure.md`）、先に全部渡されたときの要約の省略（`brief-hook.md`）、ユーザーが書いた完了条件の扱い（`room-context.md`）。`dev` 側は、構成要素の聞き方（`brief-work-types.md`）、表の組み合わせ・環境要求の置き場（`dev-deliverable-guide.md`）。`ai-room-why.md` の `start` の記述を `brief` の改名に合わせた。残件は `log.md`。

### 2026-10-24（続き: type の考え方を記載）
- ユーザーが、考え方・方針は叩き台で十分と判断。`project-structure.md` の冒頭に節「type の考え方」を置いた。前回の `project-structure.md` に重複が混入していたのを直した（原因: 文字列置換で、先に出る同じ語に当たった。置換後に見出しと行数を確認していなかった）。

### 2026-10-24（続き: guide の見直し）
- `dev-deliverable-guide.md` の不整合 7 件の叩き台を出し、ユーザーが論点 1〜5、活動の表の程度、`script-guide.md` の名前に OK。実装して反映した（決定は root の `decisions.md`）。ユーザーが、「方針の文書が無い」と指摘し、Next Actions に起票。

### 2026-10-24
- ユーザーの依頼で議論を開始。`room.py` は type を読まず、違いは手順書だけと確認し、叩き台（事実の表、論点8件）を出した。ユーザーが別セッションの分類（investigation と development）を持ち込み、2 type 案に改訂。新値は `dev` と `inv`、既定は `dev`、旧値は受け付けない、曖昧な例は成果物の名前で決める、で承認。同日に実装して反映した（`decisions.md` は root の同日の項）。
