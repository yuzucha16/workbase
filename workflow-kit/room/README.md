# room

AI 作業部屋の操作（`mkworks` / `init` / `open` / `start` / `close` / `umount` / `mask` / `restore` ほか）。人が Windows で実行する。**AI には実行させない**（原本と対応表を読む工程（マスク・復元）を含むため）。設計の理由は `guides/explain/ai-room-why.md`、手作業の手順は `guides/howto/ai-room-setup.md`。

状態: v0（2026-10-12）に、マスク・復元（`maskkit.py`）を足した（2026-10-13、モバイルで実装。**合成データの単体テストのみ**。2026-10-18 に、実際の Excel と WSL の部屋で、ダミーのデータを使って確認した）。実際の WSL（部屋）で、`init → open → mask → start → restore → readme → stock → close → reap` を通した（2026-10-18）。

## 使い方

流れ: `mkworks`（works のトップ。PC に1回）→ `init <Area>`（Area の部屋）→ `open`（Project）→ `start` ⇄ 作業 → `close`。

```powershell
cd <このディレクトリ>
uv run room.py mkworks [--role 業務用|個人用] [--remote none|<URL>] [--no-commit]
uv run room.py mkworks --update [--yes] [--base <resources のハッシュ>] [--no-commit]
uv run room.py mkworks --sub [--role 個人用|業務用] [--rev <resources のハッシュ>] [--no-commit]
uv run room.py init <Area> [--boundary external|internal] [--resume] [--only <段,…>] [--no-commit]
uv run room.py open <Project> --area <Area> [--type dev|inv] [--boundary external|internal] [--no-commit]
uv run room.py start <Project> [--cmd <部屋で実行するコマンド>] [--no-launch] [--gateway] [--adopt] [--no-commit]
uv run room.py close <Project> [--commit]
uv run room.py clean <Project> [--path <glob>]      # internal のみ
uv run room.py mask <Project>                         # internal のみ
uv run room.py restore <Project> [--force]
uv run room.py readme <Project> [--yes] [--commit]
uv run room.py stock <Project> [--dst kit|area] [--yes]
uv run room.py reap [<Project>] [--yes] [--force]
uv run room.py trace <Project>#<番号>
uv run room.py aws-key <Area> --profile <名前>
uv run room.py shell <Area>
uv run room.py umount --area <Area>
uv run room.py mv <旧Area> <新Area> [--no-commit]
```

- works は `$ROOM_VAULT`、無ければ `$WORKS_DIR`、無ければ `~/works`。`--vault <パス>` で指定できる（`--vault` はサブコマンドの前に書く）。`close` から reap までの日数は `--reap-days`（既定 14。`$ROOM_REAP_DAYS` でも指定できる）。
- `mkworks --sub`（2026-10-25 に `mksub` として足し、2026-10-30 に別コマンドを忘れるため `mkworks` のオプションに移した。`mksub` は廃止）: works と同じ親ディレクトリに、検証用の `works_sub1`、`works_sub2`、…（空いている最小の番号）を作る。`resources/` は今の `resources/` のコミット済みの複製（origin は本来の workbase の URL）で、作ったあとに `mkworks`（remote なし。既定の役割は個人用）まで行う（本物の works には触らない。`--update` `--base` `--remote` とは一緒に使えない）。使うときは `WORKS_DIR`（または `ROOM_VAULT`、`--vault`）をその `works_sub<N>` に差し替える。`--rev`（`--sub` のときだけ）は古い版の `resources/` で作る（`mkworks --update` の試験用。`git -C works_sub<N>/resources checkout main` の後に `mkworks --update`）。WSL の部屋は本物の works と共有するので、`init` `open` `start` を試すときは Area と Project の名前を重ねない（`mkworks` と `mkworks --update` は WSL を使わない）。
- `open` の `--type` は、作業の特性で選ぶ2つ。`dev`（既定）は作って保守する成果物（`src/` `env/` `tests/` `tools/` `docs/` から必要なものを選ぶ。文書だけの成果物も含む）、`inv` は調べて結論を出す成果物（`report.md`）。`room` は `type` で動きを変えない（README の frontmatter に書くだけ）。違いは手順書（`workflow-kit/project-structure.md`）が持つ。
- 部屋（WSL のディストリビューション）は `room-<Area>`。`room init <Area>` で作る（手作業の手順は `guides/howto/ai-room-setup.md` の 3・4 章）。
- トレーラー（2026-10-21）: room が作るコミット（`mkworks` `init` `open` `mv` `start` `readme` `close`）に、`Room-Op: <操作>`、`Room-Rev: <resources の短縮ハッシュ>`、`Room-Area: <Area>`（works の操作 `mkworks` には付かない）、`Room-Project: <Project>`（Project の操作だけ）を付ける。既存の Area / Project が、どの版の room で作られ、変えられたかを引く印。差分は `git -C resources diff <Room-Rev>..HEAD -- workflow-kit/room`、一覧は `git log --format='%h %(trailers:key=Room-Op,key=Room-Rev,valueonly,separator=%x20)'`（works 側）。`Room-Rev` は `workflow-kit/` に未コミットの変更があると末尾が `-dirty`（その版は差分の基点にしない）、git で引けなければ `unknown`。コミットしない操作（`mask` `restore` `pull` `stock` など）には付かない。付いていない古いコミットは「版不明」。
- Stop フックの記録（2026-10-21。単体テストのみ。決定は `docs/decisions.md` の同日）: `init`（段 `stophook`）が、部屋の ai ユーザーの `~/.claude/hooks/room-stop-record.py` を置き、`~/.claude/settings.json` に Stop フックとして登録する。記録先は、cwd が `/mnt/room/<Project>` なら Project の `ai/records/sessions.jsonl`（費用の推定。session ごとに1行）と `ai/records/replies/<日付>.md`（応答本文）。記録するとき、`C:\Users\<名>`・`/mnt/c/Users/<名>` を `%USERPROFILE%` に置換する。既存の部屋は `init <Area> --only stophook` で足す。
- 既存の部屋に道具を足す（2026-10-21。単体テストのみ）: `init <Area> --only apt,pwsh` は、指定した段だけを入れ直す（`--resume` を含む。部屋は作らない）。段の名前: `base`（一般ユーザー・`wsl.conf`・分離の確認。部屋を terminate する）、`apt` `cacert` `node` `convert` `chromium` `pwsh` `npm` `uv` `python` `claude` `stophook` `path`。名前が違う・部屋が無いときは、何も触らずに止まる。`init` に道具を足したら、その段の名前も `INIT_STEPS`（`room.py`）に足す。`cacert` は `--ca-cert` も要る。`--only` 無しの `--resume` は、従来どおり全段。
- コミット: `init`（Area の作成）と `open`（Project のひな形と Area の一覧）は、**初期状態として既定でコミットする**（戻る起点。`--no-commit` で省く。2026-10-18）。`init` `open` は、対象外のステージ済みの変更があっても止まらず、対象のパスだけをコミットする（対象外はステージに残す）。`start` も、回収の後に既定でコミットする（`--no-commit` で省く。2026-10-21。`ai/out/` の成果物を人が毎回コミットする手間をなくすため。2026-10-29 から許可リスト方式の works では `ai/docs/` の変更だけが入る）。`readme` `close` は、`--commit` を付けたときだけ。`start` `readme` `close` は、対象のパス以外がステージされていたら、コミットしない。
- 同じ Area の Project の並行（2026-10-21。単体テストのみ。実機は未確認）: 同じ部屋に、別の Project を同時に `start` してよい（既定。フラグは無い）。止まるのは、**自分の Project のマウントが残っているとき**だけ。アンマウントの確認と `close` の確認も、自分のマウント点だけを見る。並行中は、`start` が「同じ部屋で開いている Project」を表示する。部屋の共有ファイルは、動いている AI に空の瞬間を見せないよう、置き換え方式で更新する（`~/shared` は `~/shared.new` に展開して入れ替え、`/usr/local/bin/git` と信頼・許可の設定も同様）。使う側の約束: ① `~/shared` が最新になるよう、`start` は同じタイミングで行う ② 後から Project を足すときは、動いているセッションを止める ③ `room umount --area` は部屋の全マウントを外すので、並行中は使わない ④ 部屋の AI は、ほかの Project の `ai/` も読める・書ける（同じ Area は同じ境界という前提）。Windows 側のコミットが `index.lock` でぶつかったら、`start` の回収は済んでいるので、あとでコミットし直す。
- `start --gateway`（2026-10-29）: 組織の LLM ゲートウェイ（OIDC）で起動する。前提は Windows 側で dotfiles の `claude-gateway-setup.cmd` と `claude-gateway-token.cmd -Login` が済んでいること。`start` が、(1) マウントの前に設定とトークンを確かめ（取れなければ止まる）、(2) 部屋の `~/.claude-gateway/` に `settings.json`（`env` `model` `theme` と、`cat` するだけの `apiKeyHelper`。hooks と permissions は写さない）と `token`（ID トークン。権限 600）を置き、(3) `CLAUDE_CONFIG_DIR=$HOME/.claude-gateway`（`CLAUDE_CODE_USE_BEDROCK` と `ANTHROPIC_API_KEY` は外す）を `--cmd` の前に付けて起動し、(4) 起動の間、約50分ごとに Windows 側で ID トークンを取り直して `token` を置き換え（`-MinValidSec` で、残りが55分より短ければ Windows 側が保管したリフレッシュトークンで無音更新する。この引数の無い古い dotfiles では、50分後に約10分で切れるトークンを押していた。2026-10-30）、(5) 終わりに `token` を消す。リフレッシュトークンは Windows の DPAPI に置いたまま、部屋に渡るのは約1時間で切れる ID トークンだけ（部屋は interop を切っているので、部屋から Windows は呼べない。だから Windows から押す）。更新の失敗は端末を乱さないよう、終了後にまとめて知らせる。`--no-launch`（Zed）では、部屋側の `CLAUDE_CONFIG_DIR` を `$HOME/.claude-gateway` にするのは利用者（`agent_servers` の `env`）。aws-key と違い単独のコマンドは無い（寿命が約1時間なので、`start` が受ける）。実機は未確認（単体テストは WSL を差し替え）。
- 部屋の git（2026-10-21）: works の `.git` はマウントの外なので、部屋では見えない。`start` はマウントの後に、部屋のローカル（`/home/ai/gitdirs/<Project>`）に独立した git を作り、回収済みの `ai/` を基準としてコミットする。`/usr/local/bin/git` の薄いラッパーが、git の対象（cwd に `-C` を順に当てたディレクトリ）が `/mnt/room/<Project>` の下のとき `GIT_DIR` と `GIT_WORK_TREE` を自動で設定する（2026-10-31 に cwd だけの判定から直した。cwd が `/mnt/room/<Project>` のままでも、`git -C ~/src/<repo>` は clone の git を使う。`--git-dir` `--work-tree` `--bare`、`GIT_DIR` 設定済み、`clone` は素通し）ので、部屋の AI は普通に `git diff` `git commit` `git log` が使える（Zed の Agent でも効く）。アンマウントの後に捨てるので、部屋のコミットは works には届かない（works の履歴は、回収ごとの 1 コミット）。用意に失敗しても `start` は続く（警告のみ）。実機は未確認（単体テストは WSL を差し替え）。

| コマンド | すること |
|---|---|
| `mkworks` | works のトップを作る（2026-10-24。旧 `init` フックの項目 5。単体テストのみ。実機は未確認）: `resources/` が workbase の clone であることを確認（clone はしない）→ `workflow-kit/templates/` から `.gitignore` `.ignore` `.gitattributes` `.claude/settings.json` `README.md` `AGENTS.md` `CLAUDE.md` `docs/log.md` `docs/decisions.md` を置く（**既存は上書きしない**。`--role` と `--remote` で役割と remote の欄を埋める）→ `areas/` `projects/` `archives/` の `.gitkeep`、`resources_p/` → `git init`（`--remote none` は `.git/hooks/pre-push` で push を止める。URL は `origin` を足すだけで push しない）→ 生成物だけを初回コミット（git の身元が未設定なら、コミットせずに知らせる。`Room-Op: mkworks` `Room-Rev`）。works の場所は `--vault` か `$ROOM_VAULT`（既定 `~/works`）。**`--update`**: 前に反映した版（基点）から最新の雛形への変更だけを、ローカルのファイルに3者マージで当てる。基点は、最新の `mkworks` / `mkworks --update` の `Room-Rev`、無ければ `Template-Rev`、無ければ最初のコミットの `Kit-Rev`（どれも使えなければ `--base` で指定）。差分を見せてファイルごとに確認（`--yes` で省略）。**衝突、未コミットの変更があるファイル、`resources/` の未コミットの変更があるときは、何も書かずに止まる**。`.claude/settings.json` は `deny` の集合で合わせ（足すだけ。雛形から消えた項目は残して知らせる）、反映後に `Room-Op: mkworks-update` でコミットする |
| `init` | Area の部屋 `room-<Area>` を作る（実機で確認済み: 2026-10-18。Area の作成とコミットは単体テストのみ）: `areas/<Area>/README.md` が無ければ `--boundary external|internal` で作る（省くと `external`。2026-11-03 に実装に合わせて直した。止まらない）→ `boundary:` の確認（Area に `boundary:` が無いときは、`--boundary` があれば付け、無ければ付けずに `external` として扱うと知らせる）→ `wsl --install Ubuntu-26.04 --name … --no-launch` → 一般ユーザー `ai` → `/etc/wsl.conf`（automount・interop 無効）→ 分離の確認（`ai` / `/mnt/c` 空 / `cmd.exe` 無し / sudo 不可。外れたら道具を入れずに止まる）→ curl・rg・Node.js 24（公式の tarball をチェックサム確認つきで `/usr/local` へ。Zed の ACP エージェントの `npx` が 22 以上を要るため。部屋での実機確認は未了）・変換の道具（LibreOffice の calc・writer・impress、日本語フォント `fonts-noto-cjk`（`/etc/fonts/local.conf` で日本語の字形を優先）、（等幅フォント PlemolJP（v3.1.0。版と SHA-256 を固定。約 220 MB の取得）は、試験が安定するまで `init` から外している: 2026-10-20。`room.py` の `PLEMOLJP_INSTALL` と、コメントアウトした `step_script` で戻せる。monospace の優先順位には PlemolJP が残っていて、無ければ Noto Sans Mono CJK JP になる）、pandoc、Chromium（Playwright 版。`/opt/ms-playwright`）と mermaid-cli（`mmdc`。`room-mmdc` と `room-chrome` の呼び出し用スクリプトが `/usr/local/bin` に入る）、PowerShell 7（2026-10-21。公式の tarball を `/opt/microsoft/powershell/7` へ、版 7.6.7 と SHA-256 を固定。`/usr/local/bin/pwsh` は globalization を invariant にしてテレメトリと更新確認を切る薄い包み。PSScriptAnalyzer 1.25.0 と Pester 5.9.1 を PSGallery から AllUsers に版を固定して入れる。部屋の AI が書く ps1 を、`workflow-kit/tools/check-ps1.ps1` で実行せずに点検するため。単体テストと、Ubuntu 24.04 の一時ディレクトリでの pwsh・モジュール・チェッカーの試験のみ。**部屋（Ubuntu 26.04）での `init` は未確認**）。root が入れる。部屋で xlsx・docx・pptx の変換や再計算、Markdown の HTML 化をするため。実機確認は未了: 2026-10-20）・npm の cafile・uv・Python（正本の版 `.python-version` を `uv python install --default` で ai に入れ、`~/.local/bin/python3` で呼べるようにする。システムの `python3` は上書きしない。2026-10-30、実機の部屋で確認済み。既存の部屋は `--only python`）・Claude Code → 道具の確認。**ログインは人**（手順を表示する）。Area の置き場として `areas/<Area>/_noai/deliverable/`（成果物置き場）、`areas/<Area>/_noai/source/`（共通の原本。人が置く）、`areas/<Area>/ai/docs/inbox.md`（知識は `areas/<Area>/ai/knowledge/`。`stock --dst area` が作る） を、**無ければ作る**（あるものは触らない。2026-10-21。後続の `pull` `restore` `close` は、無ければ作らず、何も変えずに止まる。単体テストのみ。部屋がすでにあって止まる場合も、この作成は先に行う）。部屋がすでにあれば止まる。作りかけは `--resume`（設定と道具の入れ直し）。終わりに、Area の README の変更だけをコミットする。TLS 検査のあるネットワークで curl が証明書エラー（60）になるときは、`--ca-cert <ファイル>`（TLS 検査用のルート証明書、PEM、5枚まで）を付ける。apt の後に root が `/usr/local/share/ca-certificates/` へ入れる（`ai` は書き換えられない。SHA-256 を表示する）。付けなければ入れない。wsl.exe には `WSLENV` を渡さない（automount を切った部屋では、Windows のパスが変換できず、壊れた `SSL_CERT_FILE` などが残るため。実機で確認: 2026-10-19） |
| `aws-key` | `aws-key <Area> --profile <名前>`: 部屋の `~/.aws/credentials` に、Bedrock 用のキーを入れる（同名の節は置き換え、ほかの節は残す。権限 600）。アクセスキー ID は入力、秘密と `AWS_SESSION_TOKEN`（一時キーのときだけ）は画面に出さずに受け取り、標準入力で部屋へ渡す（コマンドラインにも履歴にも残さない）。AI からは読める場所なので、Bedrock の権限だけのユーザーにして、予算アラートを置く。Zed の `agent_servers` の `env` に `AWS_PROFILE=<名前>` を書いて使う（環境変数は Zed 経由では引き継がれないため。実機確認は未了） |
| `shell <Area>` | 部屋に入る（`wsl -d room-<Area>` の代わり）。`WSLENV` を外して入るので、Windows の `WSLENV` に `/p` 付きのパスがあっても、入るたびに「failed to translate」が出ない（automount を切った部屋では、そのパスを変換できないため） |
| `reap [名前]` | close から期限（`reap_after`。既定14日）が来て、まだ `reaped` の無い `archives/` の Project について、部屋の会話履歴（`~/.claude/projects/-mnt-room-<名>/`）と `~/tmp/<名>` を消し、README に `reaped: <日付>` を付ける。消す前に、会話履歴を Windows 側の `~/.claude/room-history/<部屋>/` へ写す（リポジトリの外。集計は `cap_meter.py --root ~/.claude/room-history`）。写せなければ消さずに止まる。名前なしは期限切れの一覧を出して承認を求める（`--yes` で省略）。名前ありで期限前なら `--force`。名前が英数字・`_`・`-` 以外なら止まる。`close` の終わりにも一覧を出す（端末のときは承認を求める）。Windows 側の `archives/` は消さない |
| `open` | works の `.gitignore`（必須は `**/_noai/`。許可リスト方式なら `ai/` の `in` `work` `out` `records` は追跡外）と Area の `boundary:` を確認し、`projects/<名>/` に `README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final,user}` と `_noai/mask.toml` のひな形（`[terms.CUST]` `[terms.PERSON]` の見出しと書式の例だけ。語はコメントアウト。2026-10-21）を作り、Area の一覧に足す |
| `start` | `area:` とディストロ名の一致、`boundary:`、ほかのマウントが無いこと、`ai/in/` の来歴（manifest）を確認 → Project の README と所属する Area の README の写しを `ai/ctx/`（`README.md`、`area-README.md`）に置く。external の Area は、`areas/<Area>/ai/{knowledge,docs}/**.md`（`docs/inbox.md` を除く）の写しも `ai/ctx/area/` に読み取り専用で置く（2026-11-02。`cleankit` の検出に当たるファイルと、合計 1 MiB を超える分は写さない。止めない）（Area の README が 16 KiB を超えると知らせる）→ 部屋の `~/.claude.json` で `/mnt/room/<名>` を信頼済みにする（信頼の確認を省く。2026-10-19）→ `ai/` を `/mnt/room/<名>` に root でマウントし、`in/` を読み取り専用に → 部屋で AI を起動（一般ユーザー）→ **必ず**アンマウントして、マウント点を消し、残りを確認 → 変更の一覧（許可リスト方式の works では、`ai/` は `docs/` 以外が git に出ないので `ai/out` のファイル数を添え、無視ファイルの警告はしない。旧方式では警告する） |
| （`start` の中） | 共有知の写し（方式 A）: `<Vault>/resources/` の `AGENTS.md`、`workflow-kit/`（`workflow-kit/room/` は `README.md` だけ。コード・テスト・設定は送らない。2026-10-17）、`exmem/{AGENTS.md,README.md,tags.md,lessons/}`、`guides/` を tar.gz にして、部屋の `~/shared` に読み取り専用で送る（起動のたびに入れ替え。途中では更新しない）。基準コミット（と未コミットの変更の有無）を manifest の `shared` に記録し、`~/shared/ROOM.md` に案内を置く。あわせて、部屋の `~/.claude/CLAUDE.md`（Claude Code が作業ディレクトリによらず読む）に `ROOM.md` への案内を、目印（`room-shared:begin`〜`end`）で囲んだ範囲だけ入れ替えて置く（ほかの内容は変えない）。`resources/` が無ければ送らない。部屋の `~/.claude/CLAUDE.md` に案内を、`~/.claude/settings.json` に `Read(~/shared/**)` の許可（読み取りだけ）を足す |
| `trace <Project>#n` | Area の inbox・`decisions.md` の項目の根拠を引き、閉じた Project の `ai/docs/` の該当節を表示する（部屋の AI には出さない） |
| `close` | マウントが無いこと、push していない clone が無いことを確認 → README がひな形のまま（`<...>` が残る）か `ai/out/close.md`（部屋の AI が書く）が無いときは、警告して `[y/N]` で確かめる（y で続ける。close.md が無ければ inbox に渡す【案件】【決定】は 0 件。N と非対話の実行は、何も変えずに止まる。2026-11-04 に停止から緩めた。動作確認や小さな作業で重いため） → **`ai/out/deliverable/` の下を Area の成果物置き場へ渡す点検**（マスクした Project は実名に戻して、していなければそのまま。置き場が無い・ファイル名にプレースホルダーが残る・人が Area 側を変えている、のどれかで、何も変えずに止まる。2026-11-04。`restore` とは別に持つ処理で、`restore` が無くなっても close に残る）→ 【決定】行（根拠の実在と cleankit の点検に通らなければ移動前に止まる）と【案件】を Area の `ai/docs/inbox.md` に追記（重複しない。inbox が無ければ作らず、何も変えずに止まる。`init` で作る）→ README を `status: done`、`closed`、`reap_after` に → Area の一覧を「完了した Project」に → ファイル単位の `git mv` で `archives/` へ（追跡外の `_noai/` も移す） |
| `clean` | `clean <Project> [--path <glob>]...`（internal だけ。2026-11-03。`pull` は 2026-11-03 に廃止。原本の置き場は共通性で分ける: Project 固有は `_noai/raw/` に人が直接置く、Project 共通の xlsx・pptx は Area の `_noai/source/` に置いて `--path` で読む。共通の md は Area の `ai/docs/` に置けば `ctx/area/` に自動で写る）: `_noai/raw/` の xlsx・pptx を `cleankit` の `strict` で掃除して `ai/in/` へ（xlsx・pptx 以外は注意だけ出して通さない）。報告（実データの抜粋入り）は、raw 経由なら `_noai/raw/tmp/`（原本に数えない）、`--path` なら `_noai/source/tmp/`（原本の隣。`--path` の対象に入れない）。どちらも部屋に渡らない。整合の問題があれば `ai/in/` へ渡さない。`--path` を付けると、Area の `_noai/source/` を直接読み（`pull` と raw への写しは不要）、`ai/in/area/<相対パス>` に出す（`source/` は実名を置かない運用なので名前はそのまま。名前に検出・`mask.toml` の語が当たれば止める。2026-11-03）。manifest は `pending`、人が読んで `start --adopt` で通す。語のマスクは要らない（`mask` は任意の補助。削除は使ってから決める） |
| `mask` | `_noai/raw/` の新しい・変わった原本（csv・md・txt・xlsx・pptx）を、`_noai/mask.toml` に従ってマスクし `ai/in/` へ。manifest に原本・マスク後・`mask.toml` のハッシュと対応表の版を記録。語が残っていれば止める（人が実行する。`start` は自動でマスクせず、原本があれば案内だけ出す。2026-11-02） |
| `restore` | `ai/out/` を復元して `_noai/final/` へ。戻らないプレースホルダー・未知の形式があれば、何も書かずに一覧を出して止める。`_noai/final/` を人が前回の復元から変えていたときも止める（`--force` で上書き。前回の書き出しのハッシュは `_noai/map/final-manifest.json`）。`start` は自動で行わず、案内だけ出す（2026-11-02）。マスクしていない Project（`clean` だけ）でも、`ai/out/deliverable/` の下だけはそのまま Area の成果物置き場へ渡す（戻す語が無いので書き換えない。ほかの `ai/out/` は触らない。2026-11-04）。（`ai/out/knowledge/` の知識の経路は 2026-11-03 に外した。知識の出口は `stock --dst`）**`ai/out/deliverable/` の下も、復元したあと Area の成果物置き場（`areas/<Area>/_noai/deliverable/<Project 名>/`。Project 名の下に置くので、Project どうしで名前が衝突しない。`init` が `deliverable/` を作る。2026-10-21。単体テストのみ）に書く**（前回の書き出しは `_noai/map/deliverable-manifest.json`、退避は `_noai/final/_prev/deliverable/`）。`_noai/final/` にも残る。ファイル名にプレースホルダーが残る、置き場の外を指す、場合は何も書かずに止まる。前回の書き出し（`_noai/map/deliverable-manifest.json` のハッシュ）から人が変えた既存ファイルがあれば、何も書かずに止まる（`--force` で上書き。直前の版は `_noai/final/_prev/deliverable/` に退避する）。 |
| `stock` | **`--dst` を省くと、各下書きの `scope:` に従って両方へ運ぶ（`area` → Area の `ai/`、`public` → `exmem/inbox/`。2026-11-04）。`scope:` が無い・不明な下書きが 1 つでもあれば、何も運ばず止まる。`kit` 側は `exmem/inbox/` に置くだけで、コミットも push もしない（room の `commit_paths` は works の `projects/` `areas/` だけを対象にし、`exmem/inbox/` は触らない）。`--dst kit|area` を付けると、その行き先だけ（従来どおり）。**move**（2026-11-04）: 運んだ下書きは、運び先を読み直して書いた内容と一致したら `ai/out/stock/` から消す（一致しない・消せないときは元を残して警告。記録は消す前に manifest に保存するので、元が無くても運んだことが分かる）。運ばなかった下書き（scope 違い、点検・衝突・frontmatter で止まった、確認で N）は残る。copy の頃に残った元で、同じ内容を運んだ記録（Area に同じ内容）があるものは、運び直さず消す。`--dst area`: external・internal 共通（`_noai/mask.toml` の語は任意。2026-11-03 に必須を外した。語が無ければ形の検出だけ）。`ai/out/stock/*.md` のうち `scope: area` のもの（`dest: knowledge|docs`、既定 knowledge）を、運ぶ前に `cleankit` の検出（金額・メール・電話・大きな数・割合の形、`_noai/mask.toml` の語）に全ファイル通し、1 つでも当たれば何も運ばず止まる。通れば確認なしで `areas/<Area>/ai/<dest>/` に運ぶ（1 件ごとの y/N は 2026-11-04 に廃止。`--yes` は互換のため残るが何もしない。運んだ後に、ファイル名と移動先を表で出す）（コミットしない）。運んだ版から人が変えた先は上書きしない。manifest の `area_stock` に記録。`--dst kit`: 部屋の AI の【汎用】の下書き（`ai/out/stock/*.md`）を、確認なしで（1 件ごとの y/N は廃止。運んだ後に表を出す）`resources/exmem/inbox/` に運ぶ。frontmatter に `base_commit` と `observed` が要る。対応表の語を含む下書きは運ばない。`scope: area` の下書きも運ばず、同じ下書きを `--dst area` で運ぶよう案内する（2026-10-24、11-02 改、11-03 に internal も同じ道にした）。基準以降に統合先の `lessons/` が変わっていれば、frontmatter に `base_stale` を足す（`kind: explain` の下書きは、`guides/explain/` への新規作成だけなので足さない。`kind` はそのまま運ぶ）。運んだものは manifest の `stock` に記録し（同じ内容は二度運ばない）、未追跡のまま残す（コミットしない: `stock-hook.md` の方針） |
| `mv` | `mv <旧> <新>`: Area と部屋を改名する（旧 `rename-area`。2026-11-02、履歴は追わない・部屋も改名する方針に作り直した）。`areas/<旧>/` を `areas/<新>/` に移し（追跡外のファイルも）、その Area の Project（`projects/` と `archives/`）の README の `area:`、`areas/` `projects/` `archives/` の `.md` の `[[areas/<旧>/…]]` と `\|<旧>]]`（`_noai/` と `ai/` の `docs/` 以外は触らない。来歴の sha256 を壊さないため）、`ai/records/manifest.json` の `area` と `masked_from` を書き換える。**部屋は公式の手順で改名する**: `room-<旧>` を終了 → `wsl --export` → `wsl --import room-<新>`（置き場は `%LOCALAPPDATA%\room-wsl\room-<新>`）→ 既定ユーザーが `ai` か確認 → `wsl --unregister room-<旧>`。ログイン、`~/.aws`、会話履歴は中身ごと写る（ext4 の大きさ分の時間とディスクを使う）。export と import の失敗、既定ユーザーの不一致は、旧の部屋とファイルをそのままにして止まる。部屋が無ければファイルだけ改名する。新しい名前が不正・すでにある（部屋も）、旧 Area が無い、旧の部屋にマウントが残っている、のいずれかなら何も変えずに止まる。`room-log.md` の過去の行は書き換えない。既定で、1 コミットにする（`--no-commit` で省く。対象の Project の書きかけの変更も入る） |
| `umount` | 部屋に残った `/mnt/room/*` のマウントを外す |

`start --adopt` は、`ai/in/` の現在のファイルを、この Project の入力として人が確認したと manifest に記録する（マスクを通さない入力用）。`start --yes` は何もしない（互換のため残す）。`mask.toml` が変わったときの `ai/in/` 作り直しの確認を省くのは `mask --yes`。`--no-launch` は、起動せずにマウントしたまま待つ（Zed の WSL リモートで使うとき。Enter で、アンマウントと回収に進む）。開くフォルダは `/mnt/room/<Project>`（`/mnt/room` を開かない。記録・git・会話履歴が壊れる）。待つ間、部屋が止まってマウントが消えないよう、部屋で `sleep infinity` を動かす（実機で確認済み: 2026-10-18。待つ間マウントは残り、Enter で戻る。`wsl.exe` はコンソールから切り離して起こす）。

## boundary（Area の属性。2026-11-02）

Area の `README.md` の `boundary:` は `external`（外向け相当。**既定**）か `internal`。無印や、それ以外の値は `external` として扱う（厳しい側に倒す）。

- `external`: 業務データを AI の入力にしない。`clean`、`_noai/raw/` の原本のマスク、`start --adopt` は止まる。AI に入れるのは、ユーザー自身が作るもの（論点整理、課題設定、プロジェクト管理、治具ツールなど）だけ。
- `internal`: 人が通したファイルだけを入れる（ファイル単位。`ai/in/` に置き、`start --adopt` で manifest にハッシュを記録する）。`cleankit`（`strict` が向く）と `pptxtext`・`exceltext` は、通す前の一次スクリーニング。マスクは補助で、通すかどうかは人の目で決める。
- 顧客ごとの違いが要るときは、`boundary:` の値を増やさず、別のキーで足す。

## マスクと復元は状態で決まる

設定は無い。`type` に関係なく、`_noai/` は常に `raw/` `map/` `final/` `user/` を作る。

- マスク（`mask`。2026-11-02 から `start` は自動で行わない）: `_noai/raw/` に原本があるときだけ行う。無ければ何もしない。マスクの出力は「未確認」（manifest の `pending`）で、人が `ai/in/` を読んで `start --adopt` で通すまで、`start` は止まる。マスクしないデータは `raw/` に置かず、`ai/in/` に直接置いて `start --adopt` する。
- 復元（`restore`。2026-11-02 から `start` は自動で行わない。`ai/out/` があれば案内だけ出す）: `_noai/map/mapping.json` があるとき（その Project でマスクしたことがあるとき）だけ行う（語を戻す処理）。マスクしたことが無い Project の `ai/out/` は戻すものではないので触らないが、`ai/out/deliverable/` の下だけは、そのまま Area の成果物置き場へ渡す（2026-11-04。`close` も同じ点検で渡す）。
- `user/` は人だけが使う仮置き（予約名。`room` は触らない）。`_noai/` 全体が追跡外で、AI にも見せない。

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

## クリーン化（`cleankit.py`）

xlsx・xlsm・pptx・pptm の、消したつもりで残っている情報（非表示シート、グラフ・ピボットのキャッシュ、定義名、コメント、文書プロパティ、ノート、埋め込みなど）を点検し、掃除した別ファイルを書く（2026-10-26。ダミーの単体テストと、LibreOffice で開き直す確認まで。Excel・PowerPoint 本体は未確認）。仕組みは `guides/explain/ooxml-residue.md`。**人が実行する**（原本と、残っていた実データを読むため）。room への組み込みは未定（実ファイルの点検の結果を見て決める）。

```powershell
uv run --script cleankit.py check <ファイル> [--terms <mask.toml>]  # 点検だけ。報告は <ファイルのフォルダ>/tmp/<ファイル>-report.md（見出しの末尾が (check)）（2026-11-04 に room clean と同じ置き方に揃えた）。見えている文字の中の金額・メール・電話・割合の形と、--terms の語を警告する（置換はしない。2026-11-02）
uv run --script cleankit.py clean <ファイル>     # 掃除。入力の位置に掃除したファイルを置き、元は <フォルダ>/tmp/<名前>_org<番号><拡張子> に退避（番号は 1 から。2026-11-04）。報告も退避した元と対（<名前>_org1<拡張子>-report.md）。<出力先> を足すと従来どおり別ファイルに書く（元は動かさない）。報告は <ファイルのフォルダ>/tmp/<ファイル>-report.md（見出しの末尾が (clean)。出力の隣ではなく原本の隣。2026-11-04）。整合の問題があれば出力を書かず止まる（2 を返す。room clean と同じ）
uv run --script cleankit.py clean <ファイル> <出力先> --keep notes,comments   # 動作を外す
```

- 出力先を省いた clean は、元を `tmp/` に退避してから入力の位置を置き換える（退避を確かめてから置換。整合の問題があれば何も動かさない）。退避した元には実データが残るので AI に見せない場所に置く。出力先ありのときは元を変えない。出力が元と同じ・既にあるときは止まる（`--force` で上書き）。
- 報告には実データの抜粋が載る。**報告は AI に見せない**（`_noai/` の下か、AI が読めない場所に置く）。画面には件数だけを出す。
- 出力と報告を、このリポジトリ（公開）の中に書こうとすると止まる（2026-10-27。`./` を指定して、実データ入りの報告が作業ツリーに出た事例から）。`.gitignore` にも報告のファイル名（`*-report.md`）を足した。
- 終了コード: 0 = 要確認なし、1 = 要確認あり（報告を見る）、2 = 実行できない。
- 掃除の既定（`--keep` で外せる）: `hidden-sheets`（非表示シートを消し、参照する数式は値に、定義名は削除）、`hidden-slides`、`notes`、`comments`、`props`、`abspath`、`printer`、`thumbnail`、`calcchain`、`revisions`、`ref-names`（`#REF!` の定義名）、`shared-strings`（使っていない共有文字列）、`orphans`（関係からたどれない部品）、`hidden-names`（非表示の定義名。AccessDatabase など。`_xl` で始まる内部の名前は残す）、`external-links`（外部ブックへのリンクを切る。数式は値に、外部パス・値の写し・外部を参照する定義名を消す）。
- 既定では行わず `--also` で足す動作（カンマ区切り）: `hidden-rows`（非表示の行のセルの値・数式を空にする。行は残る）、`hidden-cols`（非表示の列）。空にした後は、行・列が隠れたままでも点検の報告には出ない。
- プロファイル（2026-10-29）: `--profile standard` と `strict`（既定。2026-11-03 に standard から変えた）。`strict` は `standard` に加え、部品の種類（`charts` `images` `embeddings` `pivots` `connections`。参照元の図形・要素ごと外す）と非表示の行・列の値の消去を行う。`--allow images` のように、外す種類から残すものを選ぶ。`cleankit.py profiles` で一覧を出す。ダミーの単体テストまで。Excel・PowerPoint で開く確認は未。手順は `guides/howto/ooxml-clean.md`。
- 取りこぼしの網（2026-10-28）: 点検のたびに、ファイルの中の文字を、見えている文字（見えているセルの値と数式、シート名、ヘッダー・フッター、見えているシートの図形・グラフ。pptx は見えているスライドとそのレイアウト・マスター）と固定語に突き合わせ、当たらないものを `unseen-text` として部品ごとに出す。数・日付・番地・GUID・自動の名前・ふりがな・書式とテーマの部品は数えない。掃除の後に `unseen-text` が残れば、既知の残り方の外に文字が残っている。
- 消さずに報告だけするもの: グラフ・ピボットのキャッシュ（語は `mask.toml` のマスクで消す）、接続・データモデル、埋め込み・画像、マクロ、非表示の列、スライドの外や非表示の図形、代替テキスト、使っていないレイアウト。
- 掃除の後に、出力を点検し直し、整合（XML が読める、関係の先がある、型がある）を確かめる。整合の問題があれば、出力を AI に渡さない。

## pptx の取り出し（`pptxtext.py`、v0）

pptx を AI に**読ませる**用途では、掃除でなく取り出しを使う（2026-11-02 ユーザーの決定。読ませるだけに割り切る。分析・示唆の抽出、論点整理）。見えているスライドの文章と図解だけを markdown にするので、非表示・ノート・コメント・マスター・使っていないレイアウト・代替テキストは構造上出ない。標準ライブラリだけ。**人が実行する**。出力は実データを含むので、AI に見せない場所に書き、マスクしてから渡す（このリポジトリの中には書けない）。

```powershell
uv run --script pptxtext.py <入力.pptx> <出力.md>
```

- 出すもの: スライドごとの見出し（タイトル）、文章（階層は箇条書きのインデント。上から下、左から右）、表（markdown の表）、SmartArt（入れ子の箇条書き）、両端が図形につながった矢印（`A → B`）、グラフと画像は `[グラフ: タイトル]` `[画像]` だけ。
- v0 の割り切り: 画像の中の文字は取り出さない。つながっていない矢印・線は出さない。グラフの値、グループの入れ子の位置、プレースホルダーの位置（レイアウトを継ぐもの）は未対応（位置が分からない図形は最後に並ぶ）。実ファイルで見て仕様を足す。
- 掃除（`cleankit.py`）は、AI にファイルを直させて返してもらう用途のために残す（需要が見えるまで pptx の手直しはしない）。

## xlsx の取り出し（`exceltext.py`、v0）

`pptxtext` の xlsx 版（2026-11-03。用途・扱いは同じ: 読ませる用途、標準ライブラリだけ、**人が実行する**、出力はこのリポジトリの中に書けない）。見えているシートの見えているセルの値と図形だけを markdown にするので、非表示のシート・行・列、コメント、定義名、数式、プロパティ、外部リンク、キャッシュの写しは構造上出ない。room からは呼ばない（pptxtext と同じ。room の経路は `clean` の掃除）。

```powershell
uv run --script exceltext.py <入力.xlsx> <出力.md>
```

- 出すもの: シートごとの見出し（`## シート N: <名前>`。N はブックの中の順で、非表示のシートも数える）、セルの表（1 列目は行番号、見出し行は列の記号。値のある行・列だけに詰める。結合セルは左上だけ）、表示される値（数式は保存されている計算済みの値。日付の書式は `YYYY-MM-DD`、時刻つきは `hh:mm`、% の書式は百分率。改行は `<br>`）、図形（テキストボックスの文字、SmartArt、両端がつながった矢印 `A → B`、`[グラフ: タイトル]` `[画像]`。位置の上から順）、グラフシートは `[グラフシート: タイトル]`。
- 出さないもの: 非表示・とても非表示のシート、非表示の行（フィルターで隠れた行を含む）・列、非表示の図形、コメント・メモ、ヘッダー・フッター、定義名、数式そのもの、入力規則、ふりがな、代替テキスト、図形の名前、プロパティ。
- v0 の割り切り: 計算済みの値が保存されていない数式（一部のツールが書いた xlsx）は空になる。通貨・桁区切り・小数桁などの表示の書式は再現せず、数値のまま出す。白い文字・行の高さ 0 など、書式で見えなくしたものは出る（非表示の指定だけを見る）。大きな表を全部出すので、行数が多いシートは md も大きくなる。xls（旧形式）は扱わない。実ファイルで見て仕様を足す。

## `clean --path` の Tab 補完（2026-11-04）

`room-completion.ps1` を PowerShell のプロファイルから読み込むと、`uv run room.py clean <Project> --path <Tab>` で、Area の `_noai/source/` の中（`tmp/` は除く）が候補に出る。追加のインストールは要らない。Area は `projects/<Project>/README.md` の `area:` から引き、置き場は room.py と同じ順（`$env:ROOM_VAULT`、`$env:WORKS_DIR`、`~/works`）で探す。

```powershell
. "<works>\resources\workflow-kit\room\room-completion.ps1"   # プロファイルに1行足す（dotfiles 側）
```

状態: 実機未確認（作った環境に pwsh が無く、PC1 で試す）。2〜3日使って、正式に採るか判断する（ee、2026-11-04）。

## 未実装

- `/home/ai` を開いたときの会話履歴（`-home-ai`）は、Project に紐づかないので `reap` は消さない。残っていれば警告するだけ
- 部屋の作成のうち、ログイン（人の操作）の自動化
