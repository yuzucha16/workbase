# 作業ログの経緯（log-history）

## Log

### 2026-10-21（room: `init` に git を足し、部屋の AI への git の案内を強める）
- ユーザーの相談: 部屋に git を手で入れたが、部屋の AI が「リポジトリを作ってよいか」を分かっていない。`/mnt/room/` の下を、自由に使えるローカルリポジトリにしたい。調べると、部屋の git（`start` が `/home/ai/gitdirs/<Project>` に作る、`df4ff0d`）は実装済みで、足りないのは案内が AI に届くことだった。ユーザーは `room init` に git が入っていると思っていたが、apt の段は `curl ca-certificates ripgrep` だけだった。
- ユーザーの依頼で実装（承認済み。`adb7fce`、`90df7d9`、push 済み）: ① `init` の apt の段に `git` を足した（手順書 `guides/howto/ai-room-setup.md` と `-manual.md` の apt の行も）。② 部屋の `~/.claude/CLAUDE.md` の案内（`POINTER_TEXT`）に、git は許可なしで使ってよい・`git init` `git config` はしない（`.git` が works に回収されるため）・コミットは部屋の中だけ、を足した。`ROOM.md` の「部屋の git」と `room-context.md` も同じ内容にした。
- 却下: `/mnt/room/` 自体を 1 つのリポジトリにする案（`.git` が各 Project の `ai/`＝works の実体に漏れる）。
- 確認: 単体テスト 117 件が通った（skip 3）。実機は未確認。既存の部屋への反映は `room init <Area> --only apt` → `room start <名>`。

### 2026-10-21（room: `init --only` で、既存の部屋に道具の段だけを入れ直す）
- ユーザーの相談: `init` に apt などを足すたびに Area（部屋）を作り直していて面倒。既存の部屋に、足した分だけ適用したい。調べると `init --resume` が全段を入れ直せる（各段は冪等）が、取得の重い段（Chromium、LibreOffice）も毎回走る。
- ユーザーの依頼で実装: `init <Area> --only apt,pwsh`（`--resume` を含む）。段の名前は `INIT_STEPS`（`base` `apt` `cacert` `node` `convert` `chromium` `pwsh` `npm` `uv` `claude` `path`）。不明な名前・部屋なしは、何も触らずに止まる。`--only` 無しは従来どおり全段。
- 確認: 単体テスト 117 件が通った（新規 2 件。skip 3）。実機は未確認。変更: `room/room.py`、`room/tests/test_room.py`、`room/README.md`。未コミット。
- 質問への回答: 「差分すべて」は、`Room-Rev`（トレーラー）から `git diff <Room-Rev>..HEAD -- workflow-kit/room/room.py` で足された段を見て `--only` に渡す。迷ったら `--resume`（全段）。差分の自動判定は無い（Open Questions に積んだ）。

### 2026-10-21（room: 部屋に pwsh 7 を入れ、ps1 の静的チェッカーを足した。束ねる役も ps1 にする規約）
- ユーザーの相談: 部屋（WSL）で bat と ps1 を作ると、エラーとデバッグが多く、効率が悪い。pwsh を入れる案と `room run` の案を比べた結果、bat はそもそも ps1 を束ねて 1 回で実行するための入口で、価値は無いと分かった。`room run` は今回の用途には過剰（結果を AI に戻す経路も案に無い）。
- ユーザーの決定: 束ねる役も ps1 にし、bat は起動用の 3 行だけ許す。部屋の AI が従うよう文書に書く。静的チェッカーは部屋に pwsh 7 を入れる案にする（pwsh は 7 に固定）。決定の全文と確認は `decisions.md` の同日の項。
- 変更: `workflow-kit/tools/check-ps1.ps1`（新規）、`room/room.py`（`PWSH_INSTALL`、`init` の手順、道具の確認）、`room/tests/test_room.py`、`dev-deliverable-guide.md`（節「Windows で実行するスクリプト」）、`room-context.md`、`workflow-kit/README.md`、`room/README.md`。
- 確認: Windows と、Ubuntu 24.04 の一時ディレクトリの Linux 版 pwsh 7.6.7 で、チェッカーが良い例を通し、悪い例を検出した。Warning の検出と Pester の実行も確認した。room の単体テスト 115 件が通った。
- 追加（ユーザーの依頼。出力先は、ユーザーの訂正で `ai/work/` に直した。成果物に混ざるのを避けるため）: 束ねる ps1 が `ai/work/<名前>.log` の 1 本にログを出す型を、ガイドに足した（`Start-Transcript`、`catch` でエラーとスタックを書く）。`check-ps1.ps1` に、起動用 bat の呼び先のログ出力の点検（WARN）を足した。試験で `$LASTEXITCODE` の未設定エラーを直した。
- 方針（ユーザーの依頼）: bat・ps1・Python のどれにするかの相談から、部屋の AI には「部屋で完結できるなら、すべて部屋で実行する」「Excel・COM などの Windows 依存部は、できるだけ小さくし、人の手数を少なくする」と依頼を出せる形にした。実機の部屋（`room-pilot2`）の道具を読み取りで調べ（python3 3.14.4、uv、git、pwsh 7.6.7 ほか）、`dev-deliverable-guide.md` に節「実行の方針」を足した。`room-context.md` と `ROOM.md` に案内を足した。
- 再訂正（ユーザー）: ログは `ai/` の中だと AI から読めるのを失念していた。機能は残し、既定では出さず、`-Log`（`-LogDir`）を付けたときだけ出す形にした。`check-ps1.ps1` の点検も合わせた。
- 遠回り・直したもの: 試験で、Warning だけなのに FAIL が 1 件増える二重計上が見つかり、直した。部屋（Ubuntu 26.04）での `init` は未確認（Next Actions 16）。

### 2026-10-21（room: `start` の自動コミットと、部屋ローカルの git）
- ユーザーの相談: 部屋（WSL）では Windows の git が使えず不便。解消案を7つ挙げ、ユーザーが「部屋で `ai/out/` のコミットまでしてほしい」ため案1（部屋ローカルの git）+ 案2（基準コミット）を選んだ。部屋のコミットは works に届かないため、ユーザーが「`start` の回収で自動コミット」も選んだ（works の git はそもそも機能していないので部屋に閉じ込めればよい、という発言があり、works の git の部屋から見たメリットを挙げて整理した）。
- 実装（`df4ff0d`）: `start` は既定でコミット（`--no-commit`）。マウントの後に部屋の git（`/home/ai/gitdirs/<Project>`）を作り、アンマウントの後に捨てる。ラッパー `/usr/local/bin/git`。単体テスト 95 件通過（3 スキップ）。シェルは `bash -n` のみ。実機は未確認。
- 他セッションの未コミットの変更（`routes` / `deliverable_dir` など）が `room.py` とテストに混ざっていたので、自分の hunk だけを `git apply --cached` でステージした。
- 残り: 部屋の AI が git を使うかは、`room-context.md`（「コミットは AI が行わない」）と `ROOM_GUIDE` の案内次第（Next Actions 15）。

### 2026-10-21（`stock 理解`・`stock ナレッジ`・`wrap`: room のデータ設計）
- `exmem/inbox/` に 2 件のメモを作った（コミットしない）: `2026-10-21-area-data-layout-flow`（`kind: explain`。原本・成果物・知識の置き場と流れ。統合先の候補: `guides/explain/` の新規。近い既存 `cross-area-shared-knowledge` の設計の軸が古くなる点は、要確認事項に書いた）、`2026-10-21-state-derived-switches-and-boundary`（統合先の候補: `lessons/ai-isolated-work-room.md`。設定でなく状態で決める設計と、秘匿の境界を親に寄せる配置）。点検スクリプトは PASS 45 / FAIL 0 / WARN 0。room の決定と経緯は `decisions.md` と本日の各項が正本なので、メモには一般化した原則だけを残した。
- 改善の迷った点を Open Questions に 1 件足した（`stock-hook.md` の重なり確認で、近い既存ガイドが古くなる場合の扱い）。

### 2026-10-21（room: `open` が `mask.toml` のひな形を作る）
- ユーザーが示した内容（書式の注記、`[terms.CUST]`、`[terms.PERSON]`。語はコメントアウト）を、`open` が `projects/<名>/_noai/mask.toml` に書く。`init` の Area の置き場（`source` `knowledge` `deliverable` `inbox.md`）の作成は、先のコミットで済み。単体テスト 115 件が通る。

### 2026-10-21（room: 成果物置き場 `_noai/deliverable/`）
- `restore` が `ai/out/deliverable/` の下を、`areas/<Area>/_noai/deliverable/<Project 名>/` にも書くようにした。書き出しの規則（プレースホルダー名・外を指す拒否、人の変更で止める、`--force`、`_prev` への退避）は知識と同じ。`room.py` の書き出しを `Route` の表（知識・成果物）で共通にした。`init` が `deliverable/` を作る。単体テスト 114 件が通る（実機は未確認）。これで Area の `_noai/` の `source`・`knowledge`・`deliverable` が揃った。決定は `decisions.md` の同日の項。

### 2026-10-21（room: 原本置き場 `_noai/source/` と `pull --from source`）
- 旧 `knowledge/` の確認: works の `areas/` では `pilot2` だけが持っていた（試験用のダミー。git に一度も入っていない）。ユーザーが自分で移す。
- ユーザーが選んだ設計: 原本は Area の `_noai/source/` に置き、Project の `_noai/raw/` は pull の出力だけ。`room pull <Project> --from source --path <パス or glob>` で選ぶ。`init` が `source/` を作る。`raw/` に人が置いた原本があれば `mask` が注意を出す（止めない）。`deliverable/` は別に足す。単体テスト 108 件が通る（実機は未確認）。決定は `decisions.md` の同日の項。

### 2026-10-21（room: Area の知識置き場を `_noai/knowledge/` に移した）
- 知識（share）・原本（source）・成果物（deliverable）を役割で分け、実名を含む Area のデータを `areas/<Area>/_noai/` の下にまとめる案（C）をユーザーが選んだ。旧 `areas/<Area>/knowledge/` が `_noai` の外で守られていなかったため、まず `knowledge/` を移した（`room.py` の `KNOWLEDGE_DEFAULT`、`init` の旧置き場の警告、`room/README.md`、`guides/howto/ai-room-setup-script.md`、テスト）。単体テスト 105 件が通る。決定は `decisions.md` の同日の項。`source/` と `deliverable/` は未実装（Next Actions 14）。

### 2026-10-21（room: `data:` を廃止し、マスクと復元を状態で決める）
- `room pull` の新設で実質 `restore` だけが使われることから、ユーザーと検討し、Project の `data:`（none / mask / restore）を廃止した。マスクは `_noai/raw/` に原本があるとき、復元は `_noai/map/mapping.json` があるときだけ行う。`open` は `type` に関係なく `_noai/{raw,map,final,user}` を作る。`mask`（復元しない）は `restore` に統一。変更: `room.py`、`room/README.md`、`templates/project/README.template.md`、`project-structure.md`、テスト（`DataModeTest` を `NoDataModeTest` に置換）。単体テスト 104 件が通る（スキップ 3）。実機は未確認。決定は `decisions.md` の同日の項。
- 検討で分かったこと: 「窓口が2つ」に見えたのは、`areas/<Area>/knowledge/`（Project から循環した成果物）と `_noai/raw/`（作業の原本）の2つが入力元だったため。マスクの窓口は `_noai/raw` の一つ。知識と原本・成果物は別物なので置き場を分ける方針。置き場の設計は Next Actions 14。

### 2026-10-21（`stock ナレッジ`: 部屋の変換の道具と room run の設計）
- `exmem/inbox/` に 2 件のメモを作った（クラウドのセッションなので、コミットして push した）: `2026-10-21-room-convert-tools-gotchas`（統合先: `ai-isolated-work-room.md`。道具の入れ方、Chromium・フォントの実機の落とし穴）、`2026-10-21-ai-run-record-design`（同。依頼と実行の記録の分離、気づく場所、スコープ、実データ実行の条件、最小の版から上げる進め方。進め方の 1 例は型にするには早い）。`stock 理解` は 10-20 に `guides/explain/ai-room-convert-tools.md` で済み。点検スクリプトは FAIL 0 / WARN 0。`decisions.md` の 2 項に `→` を足した。

### 2026-10-21（`usage-viz` を閉じた）
- ユーザーが選び、削除に賛成した（条件: stock と wrap が済んでいること）。stock は `guides/howto/claude-usage-report.md` に反映済み（落とし穴2件を含む）、経緯は 10-20 の項にある。決定の【この件】2件を root の `decisions.md` に移し、`topics/usage-viz/` を削除、索引と窓口の行を消した。`records/` を閉じるときの扱い（移す・消す）は規則が無かったので、移さず削除にした。10-28 の仕訳の正式化と一緒に、規則にするかを決める。

### 2026-10-21（room のテストが PC1 だけ失敗する件）
- ユーザーの報告: PC1 で `uv run python -m unittest discover -s tests` が4件失敗（`CaCertTest` 2件は変更前から。`PullKnowledgeTest` の2件は PC2 では通る）。トレースバックから、原因は Windows の 8.3 短縮名（一時ディレクトリが短縮名、`knowledge_dir` が長い名前）で、`publish_knowledge` の表示用 `relative_to` が `ValueError` になることと判明した。ユーザー名が長い PC だけで起きる。
- 修正: `room.py` の `publish_knowledge` で両側を `resolve()` してから `relative_to`。`CaCertTest` は `openssl` が PATH に無ければスキップ（ユーザーの指示）。コミット `9a9c8d2`（push 済み）。PC1 でスキップを含む全件パスをユーザーが確認した。知識は `exmem/inbox/2026-10-21-windows-short-path-relative-to.md`（未コミット。統合前）。

### 2026-10-21（room のコミットにトレーラー）
- ユーザーの依頼「room 処理一式にトレーラーをつけたい。既存のルームを使った area / projects に対して、差分確認と update が可能かの判断材料として」を受け、`room.py` の 6 つのコミット（`init` `open` `rename-area` `start` `readme` `close`）に `Room-Op` `Room-Rev` `Room-Area` `Room-Project` を付けた。`kit_rev()` と `room_trailers()` を追加し、`commit_paths` に `trailers` 引数を足した。README に使い方、テストを 1 件追加。
- 結果: 104 件中、新テストは通った。失敗 2 件（`CaCertTest`）は変更前から同じ（無関係）。コミットしない操作（`mask` `restore` `pull` `stock`）には付かない。判断は `decisions.md` の同日の項。
- コミット: 下の終了処理のコミット。

### 2026-10-21（`stock-modes` の続き: `stock 理解` の実装、`start 計画` へのフィードバック、`private-knowledge` との整理）
- ユーザーが設計の【提案】を一括承認し、全工程を進めた。`workflow-kit/` に `stock` のモード「理解」（`kind: explain`）を実装（`stock-explain.md` 新規、`stock-hook.md`、`integrate-hook.md`、`check_inbox.py` / `check-inbox.ps1`、見本、整合10ファイル、`room.py` の古さの印、単体テスト）。点検は FAIL 0、lesson は回帰なし。実機（`integrate`、`room stock`）は未実施。設計からの差分4件はユーザーが承認。詳細は `topics/stock-modes/docs/`。
- `start 計画` へのフィードバック案8件を `topics/planning-method/planning-method-feedback-stock-modes-m1.md` に記録（未承認）。`private-knowledge` との重なりは整理済み（`topics/private-knowledge/docs/decisions.md`）。
- コミット: `8292322`（kit）、`1875603`（topics）。

### 2026-10-21（`planning-method` の続き: 試行のフィードバックの反映、品質チェック1回目、Area を跨ぐ共有知の実装）
- 試行の3題材のフィードバックをユーザーの承認で `workflow-kit/start-plan.md` に反映した（詳細は `topics/planning-method/docs/log-history.md`）。題材の計画の置き場の仮決め（題材のトピックの `records/`）を `start-plan.md` の置き場の表に反映した（正式化の判断は 10-28 のまま）。
- 品質チェック1回目は `private-knowledge`（`topics/kit-growth/records/planning-method-record.md`）。
- `private-knowledge` の設計と実装（`topics/private-knowledge/docs/decisions.md` ⑧〜㉕）: `workflow-kit/room/room.py` に `pull` と `restore` の Area 書き出しを追加し（テスト `PullKnowledgeTest`）、`room/README.md`、`guides/howto/ai-room-setup-script.md`（4.1・6.1）、`guides/explain/cross-area-shared-knowledge.md`、`guides/guides-index.md` を更新。実機の通し試験（ダミーの Area `pilot2`）はユーザーが問題なしと報告。単体テスト全体は 102 件中、`openssl` が無い環境の `CaCertTest` 2 件が失敗（今回の変更と無関係。変更前から失敗していたかは未確認）。
- kit の変更はすべてユーザーが承認した（`start-plan.md` の追記、`room` の実装、差分 ㉑〜㉕）。`ai-room-setup.md` と `ai-room-setup-manual.md` は、ユーザーの指示で触っていない（あとでユーザーが調整）。

### 2026-10-21（`start 計画`: 会議録のナレッジ化を始め、題材ごとのトピックと `records/` の仕訳を仮決めにした）
- ユーザーの要求: 顧客を含む打合せ内容を知識化したい（AI 向け = lessons、私向け = explain と同じ扱い・方針・ルール）。すり合わせ4回で、置き場（規則だけ workbase、中身は works 側の Area。Project を跨げるため）、入力（自動の文字起こしと自分の議事録）、「同じ」の範囲（型・タグ・索引・昇格の流れまで）、2系統の扱い（手段だった。1ファイル2層 + Bases の一覧）、顧客名（Area 内は書く、AI に渡すときはマスク）を決めた。6R・憲章・WBS・マイルストーンは作成済みで、ユーザーの反対なし。
- 置き場は、ユーザーの記憶の曖昧さで2回動いた（`kit-growth/plans/` → `planning-method/records/` → 各トピックの `records/`）。結果として `topics/private-knowledge/` を作り、`usage-viz/` と `stock-modes/` を `planning-method` から切り出した。仕訳は2か所（測ったことは `kit-growth/records/`、各トピックの出力はそのトピックの `records/`）。仮決め 〜2026-10-28（`decisions.md` の同日の項）。`start-plan.md` の置き場の表は、正式化のときに直す（kit の変更で承認が要る）。
- 裏づけ5件の確認（`topics/private-knowledge/records/private-knowledge-checks.md`）: works の `stock` / `integrate` は広げにくく、既存の `data: mask` の型（議事録の要約・抽出）と Area の `ai/docs/inbox.md` に載せる案が有力。Bases は1行が1ファイルのため、ToDo を1件ずつ並べる一覧は別の形が要る（仮説）。最大の未決は、Area の知識をマスクして部屋の AI に見せる経路。
- 遠回り: トピックの置き場を、記憶に頼って最初の指示どおり `kit-growth/` の下に作った。既存の決定（`planning-method` の 10-20、案④は保留）を先に突き合わせれば、移動を2回避けられた。
- 変更した kit 外のファイル: `exmem/lessons/planning-method.md` と `guides/howto/claude-usage-report.md` のパスだけ。`workflow-kit/` は書き換えていない。

### 2026-10-20（`review 消化`: Next Actions 4「room の改善 3 件の実機確認」を、確認せずに閉じた）
- ユーザーが各機能の役割と確認工数を尋ね、AI が実装を読んで答えた（工数は見積もりで、実測ではない）: ① `ROOM.md` の指示で `⟦CUST_nnn⟧` を書かなくなるか（`room.py:848`。約10〜15分、AI の挙動で2〜3回試す）、② `room start` が `hasTrustDialogAccepted` を書いて信頼の確認を省くか（`room.py:960`。約3〜5分）、③ `reap` が `-home-ai` の残りを警告するか（`room.py:1451`。約5分）。合計は約20〜25分。ユーザーは項目 3 と同じ扱いで「使うときに行う」として、項目を閉じた。**3件とも実機では未確認のまま**（② ③ は単体テストのみ。`test_room.py:467`、`:1109`）。
- 閉じた項目の全文: 「4. room の改善 3 件の実機確認（旧 37。10-19 に実装、テストは `CaCertTest` の 2 件（`openssl` 無し）以外 OK）: ① `ROOM.md` の指示で、AI が `⟦CUST_nnn⟧` を書かなくなるか ② `room start` で信頼の確認が出ないか。`~/.claude.json` の `projects["/mnt/room/<名>"].hasTrustDialogAccepted` が効くか ③ `reap` が `-home-ai` の残りを警告するか。」

### 2026-10-20（部屋の変換の道具: v1 を実装し、room run の案を決めた）
- ユーザーの相談: 部屋の中で pwsh・pandoc（HTML 化、スクリプト実行、Excel）を使いたい。作る側が最後まで持つ方針で、Windows が要る部分だけ人が実行する形にしたい。議論の結果は `decisions.md` の同日の項（v1・v2・v3、`room run` の方針）。
- 実装: `room.py` の `init` に、変換の道具（LibreOffice の calc・writer・impress、`fonts-noto-cjk`、pandoc、unzip）、日本語優先の `local.conf`、Chromium（Playwright 1.64.1、`/opt/ms-playwright`）と mermaid-cli 12.0.0、`room-mmdc` と `room-chrome` を足した（`73d8089`、`be1808e`、`1b4ef86`、`89f66ba`、`f15d513`）。PlemolJP は実装したが、試験が安定するまで外した。単体テスト 81 件が通る。
- 実機（PC2 の使い捨ての部屋）: v1 の試験 1〜4 と、`init` の通しが通った。Chromium は、apt が snap のため Playwright 版にした。PC1 は未確認。
- 遠回り: 叩き台の `room run` のスクリプトの置き場を `ai/out/win/` にしていたが、ユーザーの指摘で `ai/work/` の使い捨てのスクリプトの置き場に直した。Chromium の試験で、`data:` URL の文字コードの指定漏れを失敗と読みかけた（原因は試験の書き方）。
- 記録: `guides/explain/ai-room-convert-tools.md`（理解ガイド。索引に 3 行）。クラウド側の控えは Project の共有フォルダ `notes/room-tools/`（PC 環境からは見えない）。

### 2026-10-20（`review 消化`: Next Actions 3「room の実機の確認の残り」を、確認せずに閉じた）
- ユーザーが各機能の役割と確認工数を尋ね、AI が実装を読んで答えた（工数は見積もりで、実測ではない）: ① 実データで `mask` の警告量（約15〜30分）、③ `base_stale`（約15分）、⑤ `restore` が `mapping.json` の欠け・食い違いで止まるか（約20〜30分。対応表のバックアップが先）、⑧ 部屋の AI が `stock` の下書きを書けるか（約30分〜1時間）。合計は約1.5〜2.5時間。ユーザーは「実際に使うときになったら聞く」として、項目を閉じた。**4件とも実機では未確認のまま**（③ は単体テストのみ、① は合成データのみ）。
- 閉じた項目の全文: 「3. room の実機の確認の残り（旧 39）: ① 実データで `mask` の警告量 ③ `base_stale` ⑤ `restore` が `mapping.json` の欠け・食い違いで止まるか ⑧ 部屋の AI が `stock` の下書きを書けるか。共有知の送付のサイズ（1.5MB、120 ファイル）は、増えたら測り直す。」

### 2026-10-20（Next Actions 2 ②: Area 共通のマスク表を実際に使い始めた）
- ユーザーが `areas/office/_noai/mask-common.toml` に実在の語を書き、新しい Project でコピーして使った（ユーザーの申告。AI は中身を読んでいない）。表の存在と、語の無い雛形の状態は、書く前に確認した（ヘッダーの「AI は読まない」に反して一度開いたが、中身はコメントだけだった）。
- 同日、`data: mask` の txt を実データで確認した（ユーザー。文字コード・改行・語の漏れに問題なし）。最初の実行では、Project の `mask.toml` の語の行がコメントアウトのままで、「対応表の版 0」のまま原本が `ai/in/` にそのまま入った（ユーザーが直して再実行し、正しく動いた）。再発防止に、`mask_files` が語も列の指定も無いときに警告を出すようにした（止めない。`maskkit.py`、テスト `test_empty_config_warns`、`test_maskkit` 16 件 OK）。手順書 `ai-room-mask-summary.md` に追記した。
- pptx は実データが無いので未確認。項目 2 はこれで閉じた（pptx の実データでの確認は、データが手に入ったときに行う）。
- Area 共通表は `room` が読まない（`<Project>/_noai/mask.toml` だけ）。手でコピーする運用は仕様どおり。自動で取り込む案は、安全面の検討が要るので見送り。

### 2026-10-20（`start 改善4`: 第3回の日次の振り返り）
- 10-20 00:09〜20:22 の 25 コミットを、活動のみで振り返った（`retrospective-daily-record.md`）。手戻り 4 件、施策 R-2026-10-20-02（2 回再発した規則は検出にする。承認待ち）。字数は 495 字（空白を除く）で、500 字に収まった。実測は `retrospective-method-record.md` に足した。次の daily は 10-21。
- 遠回り: 1回目の草稿は 675 字で、版の行と施策の説明を畳んで収めた。

### 2026-10-20（`review 消化`: 待ち行列4件の判断と `Wsl.push` の代入検出）
- 待ち行列の4件を、サブエージェントのスクリーニングを経てユーザーが判断した: `token-matrix` の第5観点「温存」は却下、`Wsl.push` の代入検出は正式化、計画のやり方の試験運用での昇格は正式化（実装は別セッション）、改善4への計画の入力は保留（〜2026-11-11）。判断は `decisions.md` の同日の項。
- `workflow-kit/room/room.py` の `Wsl.push` に、スクリプト内の代入を弾く検査（`SCRIPT_ASSIGN`）を足し、`PushAssignTest` の 2 件を足した。テストは 96 件中、既知の `CaCertTest` の 2 件（`openssl` 無し）以外 OK。Next Actions 8（計画の取り込みへのポインタ）は、`topics/planning-method/docs/log.md` に同じ内容があるので消した。
- ユーザーの申告で Next Actions 10（`room rename-area` の実機確認）と 7（「変更のやり方」の業務での使用）を閉じた（10-20）。これで `remote` の type の判断（Open Questions）の前提の実使用が済んだ。Stop フックに `"shell": "powershell"` を足した（dotfiles `43a7192`。Git Bash の無い PC で警告が出ていた）。

### 2026-10-20（`workflow-kit/tools/` に使用量の集計ツールを足した）
- ユーザーの依頼（計画の試行の題材「トークン・コスト可視化」の実装）で、`usage_report.py`、`usage_report_html.py`、`usage_prices.json` を `workflow-kit/tools/` に置いた（置き場はユーザーが承認）。手順書は `guides/howto/claude-usage-report.md`。10-19 以降の合計トークンが ccusage と一致（79,675,204）。詳細は `topics/planning-method/docs/log-history.md` の同日（3）。HTML の見た目の確認と自動テストは未了。

### 2026-10-20（`room rename-area` を足した: Area の名前を変える）
- ユーザーの依頼「areas/<area> の rename 機能がほしい。ルームは手動で作り直す」を受けて、`workflow-kit/room/room.py` に `rename-area <旧> <新> [--no-commit]` を実装した。`areas/<旧>/` を `areas/<新>/` に移し（追跡外のファイルも）、`projects/` と `archives/` の該当 Project の README の `area:` と `[[areas/<旧>/…]]`、`ai/records/manifest.json` の来歴 `area` を書き換える（manifest を直さないと次の `start` の来歴チェックが止まる）。新しい名前は英数字・`_`・`-` だけ。新名がある・旧 Area が無い・旧の部屋にマウントが残る、のいずれかなら何も変えずに止まる。部屋（WSL）は触らない。`room-log.md` の過去の行は書き換えない。既定でコミットする。
- 確認: 新しいテスト `RenameAreaTest` の 2 件は OK。全体は 94 件中 2 件が失敗（`CaCertTest` の 2 件。`FileNotFoundError`。既知の `openssl` 無しと同じ原因と見ているが、今回の変更前の状態では測っていない）。実機（実際の `areas/` と部屋）では未確認。README（`workflow-kit/room/README.md`）の使い方と表に追記した。

### 2026-10-20（`integrate`: 写真のメモから、`.bat` の ASCII ルールが作業中に届かなかった構造の抜けが見つかった）
- ユーザーが `exmem/inbox/` に置いた写真（別環境の stock 形式のメモを画面ごと撮ったもの。初の試み）を、`integrate` で `exmem/lessons/shell-script-testing-wsl.md` に統合した（`3d99a9c`）。内容は「日本語を表示する `.bat` は UTF-8 に `chcp 65001` でなく cp932・CRLF で保存する」。写真は削除した。写し間違いの有無は、元データでの確認をユーザーに頼んだ。
- 経緯の調査: `.bat` の ASCII ルールは 2026-10-06 に dotfiles（`7b82d2c`）で、日本語コメントの文字化け対策として決まり、exmem へ転記された（`867be36`）。今回の `.bat` は works で作られ、AI がルールに届かなかった。原因は構造にある: 索引の1行に `.bat` の語が無い、ルールがノート後半の追記節にある、dotfiles の `AGENTS.md` にも無い。
- 決定（ユーザー、2026-10-20）: 暫定で全体 ASCII を正にし、cp932 の `.bat` は作らず、cp932 の試験もしない。cp932 の内容は草稿・優先度低として lesson に残した。先に採った「cp932 を例外に認める」案（`9361b2e`）は、同日に取り下げた。dotfiles は変更しない。索引の行に語を足した（補修）。「ルールが見つかりにくい構造」は、領域全体の論点として `docs/log.md` の Next Actions 9 に置いた（exmem の肥大化と合わせて議論する）。決定の記録先は lesson の Decisions。

### 2026-10-20（計画のやり方を records から切り出し、子トピック `topics/planning-method/` にした）
- `records/` が下書き・決定・次の一手まで抱えて見通しが悪いとのユーザーの指摘（kit-growth の整理）。records は測ったことだけに戻し、計画のやり方は Project 型のトピックにした（窓口、`docs/log.md`、`decisions.md`、`log-history.md`、下書き）。まず計画だけで様子を見る（ユーザー）。kit-growth は Area 型のまま残す。決定は `topics/planning-method/docs/decisions.md`。

### 2026-10-20（`review 消化` 項目 1: `room aws-key` の `touch` 失敗の原因を特定して直した）
- 旧 Next Actions 1（旧 40）: PC1 で `room aws-key` が、部屋の `~/.aws/credentials` への `touch` で失敗していた。原因は、`aws_credentials_script` を引数経路（`wsl.exe -- sh -c <スクリプト>`、`Wsl.push`）で渡したため、スクリプト内で代入した `$f` `$x` `$t` が部屋側の外側のシェルで空に展開され、`touch ""` になったこと。10-14 に `exmem` へ入れた規則と同じ原因の再発。`room-office` で、実コードと同じ関数を呼ぶ読み取り専用のプローブで再現した（`f=[]`、`cannot create : Directory nonexistent`）。`$HOME` は展開される。
- 切り分けの誤り: AI が、ユーザーのキャプチャ（直接実行の `touch` が終了コード 0）を「通過」と読み、失敗を取り違えた。ユーザーが「通過していない」と訂正した。直接実行と `room aws-key` では経路が違う。
- 直し: スクリプトと本文を標準入力（`sh -s`、`Wsl.script`）で渡し、本文は引用つきのヒアドキュメントにした。`room-office` で、権限 600、所有者 `ai`、`$` とバッククォートがそのまま入ることを確認。ユーザーが PC1 で push と動作確認まで完了した。コミット `08202a7`（メッセージの「`$HOME` を先に展開」は不正確。正しくは代入した変数。コメントは次のコミットで直した）。テストは 92 件中 `CaCertTest` の 2 件が失敗（既知。`openssl` 無し）。
- ナレッジ化: `exmem/inbox/2026-10-20-wsl-argv-expansion-recurrence.md`（点検 PASS 20）。`decisions.md` の Gotchas に同日の項。引数経路 `push` に検査を足す案を Open Questions に置いた（未承認）。
- 遠回り: 上の誤読の分。`review 消化` は項目 1 だけに絞って行った（待ち行列のスクリーニングと 3 つのリストは未実施）。

### 2026-10-20（振り返り改善4: 定例化と規模の Must）
- ユーザーの判断: 振り返りを daily / weekly / monthly の定例にした。規模を Must に足した（daily 3章・1分、weekly 4章・2分、monthly 5章・3分）。逆らう項は削除で畳む。monthly は最終営業日を含む最後の5営業日の初日。理由と見直しの条件は `decisions.md` の同日の項。手順書は `retrospective-method.md` の v6（【仮 〜10-26】）。
- 改善4 の使用回数 3/3 の後の Must の増減は、この決定で行った（Next Actions 5 から外した）。残り: 読み比べ、週次の使い方、改善5 の品質チェック3回。
- 洗い出し: 議論の場所と残件を `topics/kit-growth/records/` の週次・日次・取り組み単位の記録から整理した。日次の記録の 4.3- と章 6 の「合流」は、却下済みの R-03・R-04 を承認待ちと書いている（未修正）。

### 2026-10-19（計画のやり方: 6R から憲章・成果物 WBS・マイルストーンまでを、モバイル・クラウドで試行し、取り込みの論点を整理した）
- ユーザーが「6R ブランクから憲章・成果物 WBS・マイルストーンを作るお試し」を依頼した。題材は日報・週報・月報。本の図表と本文をキャプチャで共有してもらい、位置付け（憲章は手段の目的化を防ぐ資料）、憲章の欄、成果物分解の WBS、マイルストーンの4つの基準を、本の型に合わせて作った。ユーザーが他セッションで、works を複数、rename、room 操作の3題材を足した。決めたこと: 予算1週間、稼働日は平日のみ、バッファは土日2日、マイルストーンの期間は1・2・4週で上限3・5・9（開始の承認と終了の判断は数えない）、6R 1セット＝1 Project、今は期間の上限4週、出力と作り方のメモを別ファイルにする。試行の元ファイルは共有フォルダ（`notes/planning-method/`）。
- 4題材で、迷った点が重なった（指標が無い、戦略にあたる上位が未確認、リーダー兼任が仮、課題ログの置き先、日付が推測）。6R と作り方に戻した（`open-issues` の論点12〜14）。再現性の判定はまだ早い（4題材とも1週間・kit の題材、日付の並びが見本と同じ）。
- 取り込みの論点（形、置き場、呼び出し、既存フックとの関係、承認、品質チェック）を整理し、ユーザーが A1〜E2 を決めた。下書きを `topics/kit-growth/records/planning-method-record.md` に書いて push した（`0dc5aa5`）。Open Questions に取り込みを1件置いた（`7e04458`）。3層は未実施。判断は `decisions.md` の同日の項。
- ナレッジ化: `exmem/inbox/2026-10-19-mobile-first-method-iteration.md`（点検 PASS）。
- 遠回り: 下書きの置き場を、最初は共有フォルダのままにして取り込みの論点を進めかけた。ユーザーが「PC 環境からは見えない」と指摘して、リポジトリの records に置いた。コミットの身元は、終了時の確認が noreply への書き換えを求めたが、規約どおり agent のままにした（ユーザーが選択）。

### 2026-10-19（`review 消化` 項目5: 週次の施策 R-02〜05 の判断、AI 作業部屋の記録の整理）
- ユーザーの判断: AI 作業部屋の施策 R-07〜12 は close（判断済み）。AI 作業部屋の回を、v5 の材料集めの初実行として数える（読んで比べるのはユーザー）。改善4 の使用回数は 3/3（日次の第1回）。週次の R-02・03・04 は却下、R-05 は採用（スクリーニングはサブエージェント。理由は `decisions.md` の同日の項）。`retrospective-ai-room-record.md` の「承認待ち」の記述を判断済みに直した。
- 残り（項目5）: 読み比べ、週次の使い方（10-26 の週次）、改善5 の品質チェック3回、Must の増減の `review`。項目6は、記録が溜まるまで待ち（`sessions.jsonl` は 6 行）。
- 遠回り: 項目7と言い間違え（項目6のことだった）。最初のサブエージェントと編集の実行はユーザーが止めた（理由は聞いていない）。

### 2026-10-19（日次の振り返り（改善4）と、その施策 R-13・14 の `review 消化`）
- ユーザーが `start 改善4 本日のdaily振り返り` と言い、対象は活動のみ、出力先は `topics/kit-growth/records/` と選んだ。記録: `retrospective-daily-record.md`（手戻り 6 件、良い点 3、悪い点 3、新しい施策 2 件）。改善4 の使用回数は 3/3 になった。Must の増減は `review` で決める（ここでは決めていない）。
- `review 消化`: R-13・R-14 をサブエージェントでスクリーニングし、ユーザーがどちらも却下した（R-13 は、再現したときに検討する）。理由と見直しの条件は `decisions.md` の同日の項。実例の R-03・R-04 への合流は承認待ちのまま。
- 遠回り: 軸の宣言の前に、前回の記録と `log-history.md` の冒頭を読んだ（記録の章 7）。

### 2026-10-19（room の改善 3 件を実装）
- ユーザーが 3 行の案を承認（① と ③ は案どおり、② は「信頼済みにする」）。① `room.py` の `ROOM_GUIDE` に `⟦ ⟧` を説明文で書かない指示、`maskkit.py` の停止メッセージに「括弧を外す」。② `install_project_trust`: `room start` が部屋の `~/.claude.json` に `projects["/mnt/room/<名>"].hasTrustDialogAccepted` を書く（検査は緩めない。Claude Code の安全装置を外す決定なので、見直しの条件: 部屋に人が持ち込んだ設定ファイルが入る運用になったとき）。③ `reap_project` が `-home-ai` の残りを警告する（消さない）。
- テスト: 92 件中 `CaCertTest` の 2 件が失敗（変更前から。`openssl` 無し）。新規 5 件は OK。実機では未確認（`log.md` の項目 4）。

### 2026-10-19（Stop フックの 0 バイトの原因、補正策の kit 反映、項目 7 の整理）
- `replies/<日付>.md` が 0 バイト: 環境変数 `PYTHONIOENCODING=utf-8:surrogateescape` の下で標準入力に不正なバイトが入ると、`open` の後の `write` で例外になり空ファイルだけが残る（lone surrogate で再現）。`stop-record.py` の `open` に `errors="replace"` を足した（実機の次のターンで確認）。
- ユーザーが承認: `user-manual.md` の補正策のうち、commit 前の帰属の分離を `docs-rules.md` の「コミットと push」に、承認の添え書き（効果・期日・戻し方、推奨の最大の弱点）を `hook-common.md` の「承認」に、1項ずつ足した。残り4つ（目的の復唱、前提の確認、rename の副作用、見た目の omit）は、会話中の動き方なので `user-manual.md` のままにした。
- 部屋の `wrap` の差し替えは机上の点検（ユーザーの指示）: `room-context.md` と `wrap-hook.md` は食い違わない。実機での確認はしていない。`dev-env` / `dev-test` の最初の使用は、ユーザーが完了と申告したので項目 7 から消した。

### 2026-10-19（review 消化: Next Actions の整理と `room close` のひな形検査）
- ユーザーが完了と承認: 旧 4 ⑥（`SharedPermissionTest` は e9a2077 で直り、この PC で 3 件 OK）、旧 2 ②（済みの文を削除）、旧 3（R-08 の検証を確認した）。旧 5 ④ は同じセッションで実装: `room close` は、README に `README_TEMPLATE` の `<...>` が残っていれば止まる（`workflow-kit/room/room.py` の `readme_placeholders`。テスト `test_close_refuses_template_readme`）。項目番号を詰めた（旧 5→4、6→5、7→6、8→7）。Open Questions の参照も合わせた。
- テスト: 72 件中、`CaCertTest` の 2 件が失敗（変更前から。Windows に `openssl` が無い）。それ以外は OK。
- 待ち行列: 新しい決定は無く、スクリーニングは行わなかった（Open Questions の 5 件は期日つきの保留）。

### 2026-10-19（Next Actions 4 の ②④⑦ を完了として削除）
- ユーザーが完了と申告: ② Windows で Vault 側 deny `Read(./projects/**)` が効くか、④ `ai/ctx/area-README.md` を部屋の AI が読めるか、⑦ `ai-room-why.md` と `ai-room-setup.md` のレビュー。`log.md` の項目 4 からこの 3 つだけ消した。ガイド側の「草稿（未レビュー）」の注記（`ai-room-setup.md` の冒頭など）は、指示の範囲外なので残してある。

### 2026-10-19（review 消化: R-08 を採用）
- サブエージェントのスクリーニング: 型 D（弱）、覆す可能性は中、推奨は保留（代替案 1 に絞るなら正式化）。ユーザーが代替案 1 で採用した。`ai-room-setup.md` の 1 章の先頭に、環境の前提の 3 行（TLS 検査、`WSLENV`、Node.js）を足した。コードは変えない。検証は新しい PC か部屋の初回の `init`（Next Actions 3）。

### 2026-10-19（review 消化の続き: リスト 2 の 3 件）
- Open Questions の「`restore` の上書き保護が未試験」を、`restore_project` の行に統合した（同じ論点。どちらも `final-manifest.json` の実機を待つ）。
- 施策 R-2026-10-19-08 から、ベースのバージョンの件を切り離した（PC1 の通しは済み、Ubuntu 26.04 は確認済み）。前提の確認（TLS 検査、`WSLENV`、Node.js）だけに絞って出し直し、承認待ち。記録は `retrospective-ai-room-record.md`。
- Next Actions 2② を実施した。`ai-room-setup.md`、`ai-room-setup-script.md`、`ai-room-why.md` に `data:` の3つの型と `_noai/user/` を反映し、手順書 `ai-room-mask-summary.md` を足した（`guides-index.md` も同じコミット）。動作確認はユーザーが済み。

### 2026-10-19（log.md の整理前の全文。Next Actions 43）
- log.md が 25 KB になったため、現在状態と次にやることだけに縮めた。縮める前の「状態」「Next Actions」「Open Questions」の全文を、次の見出しの下にそのまま残す（見出しだけ `####` に下げた）。
- ユーザーの指示（2026-10-19）: 項目 44（`init` の `wsl --install` の早戻り）は、次に再現するまで保留にして log.md から消した（事実と案は、上の「room の Ubuntu 26.04 と data: 3型の実機確認」の項と、ここの全文にある）。項目 40 は `room shell` と Node の流れを確認済みで、残りは `aws-key` だけ。

#### 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`、`improvements.md` は凍結。自動採用は 2026-10-15 に畳んだ。
- cwd はリポジトリのトップだけ（`4997f7a`）。上の階層からの「続き」は AI が読みに行き、`wrap` は作業した単位の `docs/` を既定にする。フックを実行できる場所は、`hooks.md` の「領域とフックの権限」（領域 × r/w 表）が正本になった（2026-10-17。`hook-matrix.md` の cwd の 3 行は、この表との一致を見る 1 行に統合）。
- `review` は 3 リポジトリ（works の基準の「点検の対象」）の未統合メモ・トピック・機密を見る（`302fccb` `9b19540`）。終了時の 1 問は 2026-10-17 に廃止した。
- トークン消費は `token-matrix.md`（4観点）で自己採点する。基準値は合計 103。`again` `gap` の記録は廃止（`139091c`）。
- `review 消化`、`start 解決` / `start 改善`、`methods.md` を足した（`f395e34` `8242e1c` `28202d7`）。`start` のインタビューは残した。
- `wrap` を軽くし（`9fbf4e4`）、フックの重さの基準を `hook-matrix.md` に固定した（`dc2931d`）。3 リポジトリの規則を揃えた。経緯は `log-history.md`。
- init の項目 5 に `resources_p/`（PC ローカルの resources。ignore、検索の対象に含める）を足した（`6074995`）。works には反映済み（works の `2c9ffea`。ローカルのみ）。残り: なし。範囲外の案は `decisions.md` の同日の項（別リポジトリでの管理）。

- 「変更のやり方」(Must / Want。`methods.md` の「変更」、`change-method`)を足した(`266c361`)。中間成果物は「基準文書」に改称し、`areas/` `projects/` への適用を決めた(`40d8aa6`。置き場は `ai/out/<成果物名>/`、マスク後の語で書く)。
- `open-hook.md` の「Project の構造」を、`ai/` と `_noai/` への対応に書き直した(`7b2c515`。type 別の置き場、基準文書の置き場)。`_noai/` は残す。`close-hook.md` を削除し、トピックの終了は `topics/AGENTS.md` の節に、Project の終了の判断(`ai/out/close.md`)は `room-context.md` に移し、`open-hook.md` を判断部分に縮めた(`c86b4d6`)。
- init に `init 更新`（雛形の変更をワークスペースに反映。基点つきの3者マージ、`Template-Rev` トレーラー）を足し、ワークスペースの雛形に `README.md` を足した(`316840f` `8b74187`)。
- room の type に `dev-env`（主にテスト環境）と `dev-test` を足した(`ccfe968`)。`dev` の子でなく独立の type。`dev-env` は「環境の置き場」を立ち上げで聞く。`remote` という type の案は未決。
- 「調査のやり方1」(Must / Want。`methods.md` の「調査」、`research-method`、`start 調査`)を足した(`55438b6`)。新しい会話で4回実行して基準と比べ、手順書を直した(`fa18e20` `fa7531c` `9297023` `f628ab9` `608be79`)。確定版の置き場は `guides/explain/<主題>.md`(`a78ef3b`)。
- 「やり方の作り方」(`exmem/lessons/method-creation.md`。2ブロック、品質チェック3回、修正の取り込み。5〜12 は AI の追加で叩き台)を置き、`methods.md` の冒頭と各やり方のノートから辿れるようにした(`e43a04c`)。次にやり方を作るときに使う。
- 改善記録の置き場 `topics/kit-growth/records/` を作った（書式と索引は `kit-records-index.md`。やり方・モード共通）。調査のやり方1の品質チェック4回を `research-method-record.md` に移した。他のやり方・モードは、実施したときに足す。
- 「調査のやり方2」(手順を調べて、実行できる手順書にまとめる。`methods.md` の「調査」、`exmem/lessons/research-method-2.md`、`start 調査` でやり方を選ぶ)を足した。品質チェック3回の記録は `records/research-method-2-record.md`。`start-hook.md` は +22% のまま(増やしていない)。
- 取扱説明書（`exmem/lessons/user-manual.md`）に、思考の癖の補正策を Principles として足し、根拠の分析を `exmem/lessons/user-thinking-habits.md` に置いた(`aeb68e9`)。補正策(削る提案には今の役目を先に挙げる、推奨に最大の弱点を添える、wrap で撤回の回数を数える等)は、他のセッションで徐々に手順書へ反映する(ユーザー)。
- 「振り返りのやり方1」(業務の進め方・成果物を、評価軸を先に決めて、良い点と悪い点の各最大3個で評価する。`methods.md` の「改善」の改善4、`exmem/lessons/retrospective-method.md`、`start 改善`)を足した。品質チェック3回(迷った点 14 → 10 → 6)の記録は `records/retrospective-method-record.md`。`start-hook.md` は変更なし。
- topic-workflow を取り込んで close した。トピックの型の正本は `topics/AGENTS.md`（docs-rules に節は足さない）。`wrap` の依頼文は「<単位> の続き」の1行。
- 取扱説明書の「失敗の分析が薄い」に、失敗の振り返りの原則を足した(`user-manual.md`。cwd 前提の取り消しの件で試行)。撤回・取り消しの理由は事実と推測を分け、正本を1か所にする、を `docs-rules.md` に足した。施策1(実現方法を任せる依頼で、実装前に場所・手段・呼び出し元を3行で見せる)は後段に回した(`decisions.md`)。
- フックの報告の型を、共通の項目（最初に「ユーザーに求めること」「コミット」、最後に「次にやること」）と固有の項目に分けた。改善案は報告に載せず Open Questions に残す。`integrate` も push する。続ける・切るの数値は、間は TTL（サブスク1時間、API キー5分。2026-10-18 に直した）、約10万トークン、約2万トークン。正本は `hook-common.md` の「報告の型」「改善」、経緯は `decisions.md`（2026-10-17 の5項目）。
- `review` の前回の日付は `[review]` コミットから取る（`review-hook.md` の手順「コミットする」。初回は `846c3d7`）。`open`（2,924 字）・`start`（4,827 字）を、`project-structure.md` と `start-work-types.md` への分割で字数の目安内にした。点検スクリプトは FAIL なし。
- `pwsh` が無い環境用に、`tools/check_inbox.py` `find_knowledge.py` を足した。works を指す語は「works」に統一した（kit、ルート、`guides/`、`exmem/lessons/` の現在形の記述。`topics/` のノートは未）。部屋へ送る共有知から、`room/` のコード・テストを外した（`README.md` は送る）。施策1を `user-manual.md` に足した。
- `room init` に `--ca-cert`、Node.js 24、`aws-key`、`shell` を足した（2026-10-19、`80229a7` 前後。PC1 の TLS 検査・WSLENV・Zed の Agent への対応。決定は `decisions.md` の同日の項、手順は `ai-room-setup-script.md` の 2.1）。
- 2026-10-17 の作業は `807dd29` まで push 済み（`main`）。決定は `decisions.md` の同日の 4 項、経緯は `log-history.md`。
- 仕組みの決定は、作業中に承認を求めず、`review 消化` で待ち行列 → サブエージェントのスクリーニング → 最終判断の3段で承認する（2026-10-18。`approval-screening.md`、決定は `decisions.md` の同日の項）。仮決めは `【仮 〜日付】`（7日、延長1回）。
- キャッシュの実験をクラウドで実施した（Project の共有フォルダ `notes/token-saving/` の 2026-10-17 の 4 ファイルと `2026-10-18-cache-insights.md`）。5分TTL で6分あけると同じ作業が3.2倍、会話を分けても1.1倍、フック1回の読み込みは3〜6円。サブスクの主な会話の TTL は1時間、API キーは5分（公式 docs）。続ける・切るの数値の考え方（H − B、残りターン数）は実測と合った。決定は無し（改善案は Open Questions）。メモは `exmem/inbox/2026-10-18-prompt-cache-gap-cost.md`（`fb19ac2`）。

- `room init` が Area を作り（`--boundary` 必須。既定値なし）、`init` と `open` の初期状態を既定でコミットするようにした（2026-10-18。`--no-commit` で省く。`start` は対象外）。単体テストのみで、実機は未確認。次の実機で `init <新しい Area> --boundary internal` と `open` を試す。決定は `decisions.md` の同日の項、`room/README.md` に反映済み。
- `room` に Project の `data:`（`none` / `mask` / `restore`。`open` の省略時は `none`、無い既存の Project は `restore`）と `_noai/user/`（人だけの仮置き）を足し、マスクの対象に pptx と md・txt を足した（2026-10-19。`5f98702` `aef4dab`。`dev` は `none` だけが仕様）。型の実機の通しは済み（2026-10-19）。pptx・txt の実データの確認と文書の反映は Next Actions 42。
- room の実機の通しは済んだ（2026-10-18。`init`、`open`、`mask`、`start`（端末版と `--no-launch`）、`restore`、`readme`、`stock`、`close`、`reap`、Excel、手作業版）。直したバグは `d6c97d8`（待ちの Enter が `input()` に届かない。`keepalive` をコンソールから切り離した）と `086381c`（`reap` の確認の `ls` が、削除の成功を失敗と判定した）。未確認: 項目 20、10、`base_stale`、Zed を開いたままのアンマウント（今回は部屋に掴むプロセスが無く通っただけ）。

#### Next Actions

43. `docs/log.md` を整理する（2026-10-19。23 KB で、目安の 4 KB を大きく超える）。現在状態と次にやることだけに絞り、完了した項目と古い経緯は `log-history.md` へ移す（`docs-rules.md` の log.md の書式）。ユーザーの承認が要る削除は、移した先を示してから行う。別の作業として切り出す。
42. `room` の `data:`（none / mask / restore）と `_noai/user/`、pptx・md・txt のマスクを足した（2026-10-19。`5f98702` `aef4dab`）。3つの型の実機の通しは済んだ（ユーザー、2026-10-19）。残り: ① `data: mask` の pptx と txt の実データでの確認は、別のセッションで行う（ユーザー、2026-10-19。マスク → PowerPoint で開く → `start` が最後まで通る）。② 文書をまとめて直す: 古い `guides/howto/ai-room-setup.md`、`ai-room-setup-script.md`、`guides/explain/ai-room-why.md` に `data:` の3つの型と `_noai/user/` を反映する。「マスクだけで要約を出す」手順書を `guides/howto/` に足す（`guides-index.md` も同じコミットで）。**この使い方の仕様を使わずに省いた（omit）ときは、①②の文書化もしない**（ユーザー、2026-10-19）。③ Area 共通のマスク表の置き場を `areas/<Area>/_noai/` で試す（コピー元にする運用。仕様は足さない。Area の README には語を書かない: `ai/ctx/area-README.md` として部屋の AI に見えるため）。番号のずれや過去ログ検索で困ったら、Area 共通の対応表を仕様に起こすか決める。要約の戻し先は `areas/<Area>/ai/docs/`（仮置き）。
41. AI 作業部屋の取り組みの振り返り（改善4。2026-10-19。記録は `topics/kit-growth/records/retrospective-ai-room-record.md`）の施策 R-2026-10-19-07〜12 の承認。済み（10-19）: 7 は採用（`topics/AGENTS.md`）、8 は保留 〜2026-10-23（ベースの件を切り離し、前提の確認だけに絞って出し直す）、9・10・12 は却下、11 は採用（置き場は `session-handoff.md`。統合済み）。`exmem/inbox/2026-10-19-*` の 6 件は統合済み（10-19）。提案 2 件（行き先の表を `topics/AGENTS.md` に、恒常許可の書き方を `docs-rules.md` に）も承認して反映済み。この項目は、R-08 の出し直し（〜10-23。前提の確認だけに絞る）が残るだけ。統合先の Open Questions の 2 件は「解決」に直した。
44. `room init` で、`wsl.exe --install` が完了前に非ゼロで戻り、後続の設定が走らなかった（2026-10-19、PC1。`init office` で、進捗 0.0% のまま端末に戻り、後から「正常にインストールされました」。その時点で `wsl -l -v` には `room-office` が Running で見えた）。`--resume` で続きは通った（ユーザー）。事実: 戻りが早かったこと。推測: `room.py:606` の `distro not in distros()` の判定が、登録前に走った。戻り値と画面の全文は未取得。案: `install()` の後、`wsl -l` に出るまで数十秒待つ。原因を確かめてから、承認を得て直す（`workflow-kit/` なので承認が要る）。
40. `room aws-key` を、実機で通す（2026-10-19）。`init`（Ubuntu 26.04）は通った（ユーザー、2026-10-19）。残り: `aws-key`、`room shell`、Node を入れる流れの個別の確認。PC1 で、部屋の `~/.aws/credentials` への `touch` が `ai` で失敗する。原因は未特定（`~/.aws` の所有者が root だった可能性は、ユーザーが取り下げた）。確かめる: `wsl -d room-<Area> -- sh -c 'id; echo $HOME; ls -ld $HOME $HOME/.aws; touch $HOME/.aws/credentials; echo $?'` の出力と、`touch` のエラー文。直したら、`room shell`（`failed to translate` の解消）と、`init` から Node を入れる流れ全体も、実機で確かめる。手書きの `credentials` では、Zed の Agent の Bedrock 認証が通っている。
39. room の実機の確認の残りを、まとめて PC で行う（旧 `topics/ai-workspace-boundary/` の残件。2026-10-18 に root へ一本化し、トピックは削除した。ユーザーの方針: 作業をキリの良いところまで進め、まとめて確認する）。① 実データで `mask` の警告量を見る。② Windows で Vault 側 deny の書式 `Read(./projects/**)` が効くか（雛形は `templates/workspace/claude-settings.template.json`）。③ `base_stale`（`room.py` の frontmatter 更新）が、共有知の基準が古いときに付くか。④ `room start` が写す `ai/ctx/area-README.md` を、部屋の AI が開始時に読めるか。⑤ `room restore` が、`mapping.json` が無い・食い違うときに止まるか。⑥ `SharedPermissionTest` 2 件を Windows で実行して通るか（原因は Windows の `expanduser` が `HOME` でなく `USERPROFILE` を見ること。テストに足して Linux で通った）。⑦ `guides/explain/ai-room-why.md` と `guides/howto/ai-room-setup.md` のレビュー（「草稿（未レビュー）」の注記を外す。`why` は 2026-10-18 にトピックのノートと照らして更新済み。`setup` は未）。⑧ 部屋の AI が実際に `stock` の下書きを書き、先頭に基準コミットと観測日を付けられるか（`ROOM.md` に従うか。ダミーでは人が置いたファイルで確認済み）。共有知の送付のサイズ（1.5MB、120 ファイル、2026-10-14）は `guides/` と `lessons/` が増えたら測り直す。`review` が読む記録（`events` など）の置き場も未確認。20 と 37 は別項目。ユーザーは、10-18 の通しで通っていると見た 2 件（別の `wsl.exe` からのマウント、`ai/out/` のサブディレクトリの `restore`）と、omit した 3 件（部屋専用の SSH 鍵、Zed を開いたままのアンマウント、リポジトリ・remote の dev の案）を外した。設計と決定は `guides/explain/ai-room-why.md`、`docs/decisions.md`（「AI 作業部屋の決定」）、`exmem/lessons/ai-isolated-work-room.md`、仕様は `workflow-kit/room/mask-spec.md` に移した。
38. 改善4（振り返り）のモードの直しの続き。済み: 読後の指摘で手順書を v5 にし（【仮 〜10-26】。目標、活動/成果物の分離、具体は ID、11 → 8 章）、第1回の記録を組み直した（材料は集め直していない）。残り: ① v5 で材料を集め直す実行（同じ入力 10-12〜10-19 か、次週 10-26）を、新しい会話で行い、ユーザーが読んで比べる。② 週次の使い方（前回の目標・軸・施策の引き継ぎ。R-2026-10-19-06。引き継ぎの定義のみ反映）を仕上げる。③ 施策 R-2026-10-19-02〜05 の承認（01 は 10-19 に却下、06 は一部反映済み。02〜05 は保留。次の `review 消化` で、サブエージェントのスクリーニングにかける）。
37. 実機の通しで気づいた room の改善 4 件に対応する（2026-10-18 `review 消化` でユーザーが「やります」）。①`restore` が、AI が本文に書いた `⟦CUST_nnn⟧` の説明で止まる（AI への指示で防ぐか、`restore` が説明用の記述を許すか）。②新しい Project のたびに Claude Code の信頼の確認が出る。③Zed を `/home/ai` で使うと、履歴が `-home-ai` に残り、どの Project にも属さず `reap` されない。④`close` が、README がひな形のままでも通る。方法は決めていない（実装前に場所・手段・呼び出し元を 3 行で見せる）。
29. Stop フックで、セッションの費用と ID を記録する手順（`notes/stop-hook-record/2026-10-17-procedure.md`、プロジェクトの共有フォルダ）を、Zed を使う PC で実機確認する（端末の `claude -p` と、Zed の1往復。2026-10-17 時点）。確認の後に、キャッシュの間を記録に足す案（`2026-10-18-cache-insights.md` の S3）を決める。
24. 続ける・切るの暫定の数値（約10万トークン、約2万トークン）は、クラウドの実験（2026-10-17。1回ずつ）で考え方が合うと確かめた。「間」は TTL 基準に直した（2026-10-18。`hook-common.md`、`session-handoff.md` の Decisions）。TTL は確認した（2026-10-19、ユーザーの PC。`ephemeral_1h_input_tokens` 24,046・`ephemeral_5m` 0 → 1時間。実測）。新しい会話の土台 B は約 24k トークン（このときの cwd での値。cwd で変わる）で、「約2万未満なら続ける」の例外の数値より大きい。残り: 本物のフック列で3回以上再実験する。例外の数値（約2万）を B に合わせて直すかは、再実験の後に決める。
20. 領域 × r/w 表（`hooks.md`）を使いながら確かめる。部屋の AI が `wrap` の差し替え（コミットを行わない、知識化は `ai/out/stock/` の下書き）と、`ROOM.md` の stock の書き方（frontmatter）に従えるか。`check-hook-outline.ps1` は実行して FAIL なし(2026-10-17)。この項は別セッションに回した(ユーザーの指示)。
15. 振り返りを「定期（改善4。進め方・成果物）」と「突発・なぜなぜ（改善5）」に分けた(2026-10-17。`retrospective-method-2.md` は叩き台)。残り: 改善5 の品質チェック3回(基準は試行の出力 `notes/retrospective-method/2026-10-17-trial-this-thread.md`)、改善4 の「定期」としての使い方(前回の日付から今日まで、前回の軸の引き継ぎ)の反映、ID・検証項目の形の確認。
13. 「振り返りのやり方1」(`methods.md` の改善4、`retrospective-method.md`)を、次の振り返りの依頼から使う(題材 B = 業務の対象でも)。使った回数 2/3（2026-10-19。題材 A の週次と、AI 作業部屋の取り組み単位。後者は `retrospective-ai-room-record.md`）。評価軸の選び方の指針が要るか、各最大3個が適切かを、`records/retrospective-method-record.md` に足す。3回の `review` の後に Must の増減を決める。
12. `user-manual.md` の補正策(2026-10-17、2026-10-18)を、使いながら手順書に反映する。候補（`wrap` の集計は、終了時の1問の廃止で取り下げた）: 削除・統合の提案での役目の列挙、決定の推奨に弱点を添える、手段の依頼での目的の復唱、案の前提の確認、rename・移動の副作用の一覧、commit 前の変更の帰属の分離、見た目の調整の omit 提案、承認への効果・期日・戻し方の添付（項目 30 と合流できる）。施策1（実現方法を任せる依頼で、実装前に場所・手段・呼び出し元を3行で見せる。Principles に入れ済み）は、次にその依頼が出たとき、3行が見せられたか・効いたかを見る。PC1 の会話と 10-15 以降のローカルログからの同じ分析は、`user-thinking-habits.md` の Open Questions。2026-10-18 の分析は、この PC の 09-26〜10-14 だけ。

10. `dev-env` / `dev-test` を、最初の Project で1回使い、置き場の表と完了条件の例が合うかを見る(`dev-deliverable-guide.md` の末尾の節)。使った後に `remote` の type の要否を決める。
8. 「変更のやり方」(`methods.md` の「変更」、`exmem/lessons/change-method.md`)を、次の変更から使う。3回の `review` の後に、Must(基準文書3・変更6)が重すぎないか・足りないかを見て増減を決める。`areas/` `projects/` での適用は決定済み(2026-10-16。置き場は `ai/out/<成果物名>/`、マスク後の語で書く。`decisions.md`)。最初の業務で使って、置き場が合うかを見る。先送り: 新規作成のフックかモード、変更の伝播・軽重・廃止。


#### Open Questions

- 場所: 実機の通し（2026-10-18）で気づいた点 / 問題: `restore` の上書きの保護（`final-manifest.json`）は、今回試していない / 案: 次の実機で試す。
- 場所: Stop フックの記録の置き場 / 問題: 既定は `~/claude-records/`。部屋の中だけ `$CLAUDE_PROJECT_DIR/records`（`ai/records/`）にするかが未決 / 案: 実機確認（29）の後に決める。【保留 〜2026-10-25】（2026-10-19 `review 消化` でユーザーが保留。スクリーニング: `ai/records/` の用途とマスクの整合が未確認）。
- 場所: `open-hook.md` の未決の `remote` の type / 問題: WSL から SSH で user 権限のリモート(Docker を含む)を AI が操作する使い方を、`dev` でも使える type にするか。接続の安全(鍵、権限、記録)は `guides/explain/ai-room-why.md` の設計と重なる / 案: 実測の後に決める。【保留 〜2026-11-02】（2026-10-18 `review 消化` でユーザーが保留、期限 11/02。項目 10 の `dev-env` の実使用の後に決める）。
- 場所: `open-hook.md` の未決 / 問題: リポジトリが正の `src`、remote で動くものは、構造が新規のフルスクラッチ前提で、`ai/out/` に clone すると `restore` が止まる / 案: `repos/` に置いたまま、スナップショットと patch で受け渡す(未検証)。【保留 〜2026-11-05】（2026-10-19 `review 消化` でユーザーが保留。スクリーニング: 型の該当なし、覆す可能性は中。`remote` の type と `dev-env` の実使用の後に決める）。
- 場所: `room.py` の `restore_project` / 問題: AI が使えない間に人が `_noai/final/` を直すと、次の AI の終了時の復元で無条件に上書きされる(別の話にする、とユーザー。2026-10-16) / 案: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束、上書き前の警告。【保留 〜2026-11-05】（2026-10-18 `review 消化` でユーザーが保留。`_noai/final/` は最終調整で人が触る想定だが、git 管理下にあるので戻せる。次の実機で `final-manifest.json` の保護を試してから決める）。
- 場所: `token-matrix.md` と `review` の入力 5（重い会話） / 問題: 4観点に、間と先頭の安定が無い。入力 5 は大きい会話を見るだけで、書き直した量が見えない / 案: 第5の観点「温存」を足し、入力 5 を「TTL を超えて空いた後の書き込み量」に変える（Python スクリプト。費用を記録する Stop フックの inbox のメモと一緒に検討）。【保留 〜2026-10-25】（2026-10-19 `review 消化` でユーザーが保留。スクリーニング: 型 B・D・E。入力 5 の今の役目の引き継ぎと基準値 103 の再設定を付け、分割して出し直す）。

### 2026-10-19（`room` の Ubuntu 26.04 と `data:` の3つの型の実機確認）
- ユーザーが PC1 で確認した: ベースの Ubuntu 26.04 の部屋（`init`）と、`data:` の none / mask / restore の通しは OK。`data: mask` の pptx・txt の実データは別セッションで行う（Next Actions 42 に残す）。
- 見つけた問題: `init office` で `wsl.exe --install` が完了前に戻り、設定が走らなかった。`--resume` で続きは通った。直しは未（Next Actions 44）。
- 手順書の「実機の通しは未了」の注記を直した（`ai-room-setup.md`、`ai-room-setup-script.md`、`ai-room-setup-manual.md`、`lessons/ai-isolated-work-room.md`）。`aws-key`、`shell` は未確認のまま（項目 40）。
- 単体テストは、全体で 2 分を超えるほど遅いだけで、止まってはいない（個別の実行で通った）。

### 2026-10-19（`review 消化`: 振り返りの施策と待ち行列の判断、inbox 6 件の `integrate`）
- スクリーニング（サブエージェント 3 回）とユーザーの最終判断: `repos/` の受け渡しは保留 〜11-05。R-01・09・10・12 は却下、R-07・11 は採用、R-08 は保留 〜10-23（ベースの件を切り離し、前提の確認だけに絞る）。理由は `decisions.md` の同日の 2 項。
- 反映: `topics/AGENTS.md` の「トピックを終わらせるとき」に突き合わせ（手順 0）と行き先の表（手順 1）を足した。`docs-rules.md` に恒常許可の書き方を足した（統合先の Open Questions の提案 2 件を、ユーザーが承認）。
- `integrate`: 6 件を `ai-isolated-work-room`、`claude-code-auth-providers`、`claude-code-permissions`、`session-handoff`、`workflow-kit` に統合（`f264725`）。実物との食い違いは、ベースが Ubuntu-26.04 に変わっていた 1 件（決定の記録なし）。
- 他セッションに回した: `aws-key` の `touch` 失敗の原因、`room shell` の実機確認（項目 40）。

### 2026-10-19（`room` のマスクに pptx と md・txt を足し、Project に `data:` を持たせた。PC1 での使い方の相談から）
- ユーザーの相談: PC1 で試すと、マスクを使う作業と使わない作業がある。使わないときの `ai/` `_noai/` の使い方が分からず、ディレクトリが深くなる。主な用途は、顧客情報を含む資料（議事録・戦略・設計書。pptx とテキストが主、xlsx も一部）の要点・課題・アクション抽出で、読み手が本人だけなのでマスクだけで復元は要らない。
- 調べた事実: マスクの対象は csv と xlsx だけ、復元は `start` の終わりに自動で、`ai/out/` の形式が未知だと止まる。`_noai/` の使い方は、マスクしない場合を想定していなかった。
- ユーザーの決定: ① pptx と md・txt を足す（docx は不要）。② `data:`（none / mask / restore）を持たせる。省略時は全 type で none。`dev` は none だけが仕様で、他は警告。③ `_noai` の名前は変えず、`user/` を予約名で足す。④ Area 共通のマスク表は `areas/<Area>/_noai/` に置いて、コピーで使う（仕様は足さない）。実機の確認と文書の反映は他のセッションで（Next Actions 42）。
- 実装: `5f98702`（`data:` と `_noai/user/`、pptx・md・txt、86 テスト）、`aef4dab`（省略時を none に）。pptx は run をまたぐ語を段落の先頭の run に寄せて置換し、縮小画像を削除する。
- 遠回り: 「Area の README に共通のマスク語を書く」案を出したが、Area の README は部屋の AI が読む写しになるので、語が漏れる。確認の途中で自分で取り下げた。

### 2026-10-19（PC1 で `room init` の `curl` が証明書エラー。`room` に `--ca-cert`、Node.js、`aws-key`、`shell` を足し、手順書を直した）
- ユーザーの報告: PC1 で `room init` の `curl` が SSL 証明書エラー（終了コード 60）。実機で切り分けた: `WSLENV` 経由の壊れた証明書パスの変数（`failed to translate`）が部屋に残り、部屋から見える証明書の発行元は勤務先名（TLS 検査）。変数を外しても失敗し、勤務先のルート証明書が部屋に無いのが主因。ユーザーの承認で、`WSLENV` を外す処理と `init --ca-cert`（`99d8f8d`）を足した。通った。
- Zed の Agent で Bedrock につなぐ過程: 部屋に Node.js が無く（apt は 18、Agent は 22 以上）、`init` に Node.js 24 の導入を足した（`b406e36`。公式の tarball、チェックサム確認つき。この環境で展開を実行して確認）。Zed の Agent に、手で `export` した環境変数が届かない仕組みを説明し、`agent_servers` の `env`（秘密なし）と `~/.aws/credentials`（秘密）に分けた。`aws-key`（秘密は標準入力、`80229a7`）と `shell`（`WSLENV` を外して入る、`94fa815`）を足した。ユーザーが Zed の認証を、手書きの `credentials` で通した。
- 未解決: `aws-key` の `touch` が失敗する（Next Actions 40）。所有者の件は、ユーザーが取り下げた。
- 手順書: `ai-room-setup-script.md` に 2.1（Bedrock）と 9 章の行を足し、`ai-room-setup.md` に注記と 9・10 章の行を足した。`ai-room-setup-manual.md` は更新していない（手作業版。`init` の追加分は反映していない）。
- 相談: 部屋を works 単位にする案は様子見。Ubuntu 26.04 LTS に上げたい（長く使うため）は、確認の途中でユーザーが調査を止めた。未回答（懸念点は、`wsl --list --online` に名前があるか、`room.py` の `ROOM_BASE`、新しい部屋への入れ替え）。
- 遠回り: 所有者の見立てを、確認前に断定に近い形で出し、取り下げになった 1 回。

### 2026-10-18（`topics/ai-workspace-boundary/` の残件を root に一本化した。クローズの確認）
- ユーザーの依頼で、トピックを close できるか確認した。完了条件の優先順位 1〜7 は、10-18 の通しでほぼ満たす。残りは Next Actions 39 に移した。ユーザーの決定: 無理に close せず、作業をキリの良いところまで進め、root の docs に一本化し、まとめて動作確認する。omit: 部屋専用の SSH 鍵、Zed を開いたままのアンマウント、リポジトリ・remote の dev の案。外した（通っていると見た）: 別の `wsl.exe` からのマウント、`ai/out/` のサブディレクトリの `restore`。
- トピックの `docs/log.md` を 10-18 の通しに合わせて直した（`4cc9f7a`）。`SharedPermissionTest` 2 件の原因は、Windows の `os.path.expanduser` が `HOME` でなく `USERPROFILE` を見ること。テストの環境変数に `USERPROFILE` を足し、Linux で全 55 件が通った（Windows は未確認）。
- ユーザーの承認（案 A）で、トピックの Markdown を移管して削除した。`ai-room-mask-spec.md` は `workflow-kit/room/mask-spec.md` に移し（参照 4 か所を直した）、設計の要点は `guides/explain/ai-room-why.md` に、決定は `docs/decisions.md` の「AI 作業部屋の決定」に統合した（`restore` の保護とマスクの一致の決定は `exmem/lessons/ai-isolated-work-room.md` にも足した）。設計ノート、handover 5 本、`ai-boundary-design`、`ai-room-local-state`、`log-history.md` は移さず削除した（履歴は git。`ai-room-start-here.md` と `topics-index.md` の行も削除）。handover の「PC で確認すること」の漏れは、Next Actions 39 の ⑧ に足した。

### 2026-10-19（AI 作業部屋の取り組みのナレッジ化と、改善4 の振り返り）
- ユーザーの依頼で、取り組みの知見を一般化して `exmem/inbox/` に3件足した（端末をまたぐ作業の進め方、取り組みの閉じ方、クラウドの書き込み権限。`1c8d045`）。kit への追記（`topics/AGENTS.md`、`docs-rules.md`）は、各メモの Open Questions の提案にとどめ、承認待ち。
- 続けて `start 改善` の改善4 を、AI 作業部屋の取り組み（10-12〜10-19）に当てた。記録: `topics/kit-growth/records/retrospective-ai-room-record.md`（手戻り 13 件、良い点 3、悪い点 3、施策 6 件で承認待ち）。使った回数は 2/3。10-17 より前の git は無く、旧トピックの経緯を `git show` で読み直した。
- 遠回り: 手戻りの母数を定義できず、率を出せなかった。本スレッドの誤判断 2 件（H12、H13）を、手戻りに数えた。

### 2026-10-19（改善4 の読後の指摘を受け、手順書を v5 に直した。Next Actions 38 の前半）
- ユーザーが第1回の記録を読み、「分析は芯を食っているが、のっぺりしている（目標が無く、現状・ギャップ・次の行動につながらない。活動と成果物が混じる）」「構造化されていない（抽象の仕組みと具体の事象が混じる）」「事実の一覧は分かりやすい（手戻りが一目瞭然）」「詰め込みすぎ」と評した。
- `retrospective-method.md` を v5（【仮 〜2026-10-26】）にした: 目標を仕込みの Must に足し、章を 11 → 8 にし、活動の章と成果物の章を分け、悪い点に所在（目標 / 行動 / 仕組み）を付け、具体は章 3 の ID だけにした。決定は `decisions.md` の同日の項。
- 第1回の記録を v5 の章立てに組み直した（材料は集め直していない）。施策 R-2026-10-19-01〜06 の ID と内容は変えず、対応する節の列を足した。R-06 は一部反映。次週（10-26）が、v5 で材料を集める初めての実行になる。

### 2026-10-19（改善4 の振り返りを、直近1週間で初めて実施した）
- ユーザーが `start 改善4 振り返り` と言い、期間を「システム時刻の1週間前から本日まで」（10-12〜10-19）に限定、毎週積み重ねると指示した。対象は進め方と成果物の両方（ユーザーが選択）。決定は `decisions.md` の同日の項。
- 評価軸 5 個（手戻り、判断、再現性、成果物の出来、記録）を材料の前に決め、256 コミットを読んだ。手戻り 16 件（6.3%）。良い点: 実機の通しで欠陥を発見、承認 3 段、型での品質向上。悪い点: 決めた規則の数日での廃止・決め直し（4 組）、記録の長文化、検証待ちの積み上がり（9 件中 8 件）。施策 R-2026-10-19-01〜06 は承認待ち。記録は `topics/kit-growth/records/retrospective-weekly-record.md`、索引は `kit-records-index.md`。
- ユーザーは、この回の入力を固定して改善4 のモードを直すと言った（Next Actions 38）。
- 遠回り: 質問の選択肢が1つで拒否された 1 回。期間が最初の提案からユーザーの指示に変わった。

### 2026-10-19（`review 消化` 6 回目: 6・35・36 を閉じ、N を決め直し、Open Questions の 2 件を保留にした）
- サブエージェントで 2 件をスクリーニングした。「温存」の観点を足し入力 5 を書き直し量に変える案（`token-matrix.md`）は型 B・D・E、覆る可能性は中、推奨は保留。Stop フックの記録の置き場は型なし、覆る可能性は低、推奨は保留。ユーザーが両方を【保留 〜2026-10-25】にした（Stop フックの TTL 記録の案 S3 と実機確認 29 の後に出し直す）。
- ユーザーの申告で、Next Actions 36（実名の手順書 2 本のレビュー）と 35（同 2 本の動作確認）を完了として消した。35 の完了に合わせ、`ai-room-setup-script.md` の「実機で確認していないこと」と「手で Area を作る場合」を外した。
- Next Actions 6 を完了とした: `hook-matrix.md` の N を、字数 +20% → +50%、項目数 +2 → +3 に決め直した（`review` 3 回の後の見直し。ユーザーの決定）。`wrap` の読み込み字数の測り直しと reviews の記録先は、ユーザーが完了としたので追わない。
- Next Actions 24（続ける・切るの数値の再実験）は、ユーザーが続けて行う。

### 2026-10-19（全フックの横並びの揃えの残りを実施した）
- ユーザーが、どこまで対応したか分からなくなったため、共有フォルダの候補一覧（`2026-10-18-candidates.md`）と現行ファイルを突き合わせ、未実施 9 件を確かめた。ユーザーが承認し、3-4、3-1b、2-3、2-2、1-10 を実施し、1-7、1-9、N9 は足さないと決めた。決定は `decisions.md` の同日の項。`check_hook_outline.py` は FAIL なし（`review-hook.md` の字数の NOTE のみ）。残りは 2-11/3-3 と 1-8。
- ユーザーが、全フックの改善表を完了とした（残りの 2-11/3-3 と 1-8 は見送り）。`init-hook.md` の「Claude 用スキル（未作成。TODO）」は、`guides/explain/claude-skills-overview.md` を置いたので、そこを指す形にした。`review-hook.md` の字数（5,056）は問題なしと確認した。candidates と matrix の 2 ファイルは、定期的に見直すので残す。置き場は、共有フォルダ（リポジトリの外で追えない）から `topics/kit-growth/records/` に移した（索引に 1 行）。同じ表を更新し、増やさない。`init-hook.md` の TODO は、ユーザーの勘違いの訂正で、残した。

### 2026-10-18（`review 消化` 4 回目: 7 を閉じ、重複を整理し、実機の通しの改善 4 件を Next Actions 37 にした）
- 承認待ちの決定は無く、サブエージェントは起動しなかった（Open Questions は判断を聞く質問のみ）。ユーザーの指示で、Next Actions 7（`init 更新` を PC1・PC2 で使う）を完了として消した。Open Questions「キャッシュの実験」は Next Actions 24 の残りと同内容なので消した。35 の「残り: ユーザーのレビュー」は 36 と重複するので外した。
- 実機の通しで気づいた点 ①〜④（`restore` の説明用 `⟦CUST_nnn⟧`、信頼の確認、Zed の `-home-ai` の履歴、`close` の README ひな形）は、ユーザーが「やる」と決め、Next Actions 37 に移した。⑥（`restore` の上書きの保護）は Open Questions に残した。
- Next Actions 31 の残りを 1 件ずつ聞いた。`remote` の type は【保留 〜2026-11-02】（項目 10 の `dev-env` の実使用の後に決める）。`init-update.md` の大きさ（7.9k 字。`init-workspace.md` の約 3 倍）は閉じた。理由: 使用頻度が低く、大きくても実害は少ない。`start` のモード管理が固まったときに、`init` もそれに倣う形にする（ユーザーの方針。いまは行動なし）。restore の上書きは【保留 〜2026-11-05】（`_noai/final/` は最終調整で人が触る想定。git 管理下なので戻せる。次の実機で `final-manifest.json` の保護を試してから決める）。これで Next Actions 31 を閉じた。
- ユーザーの申告で、Next Actions 30（承認プロセス。直前の `review 消化` でサブエージェントが動いた）と 11（調査のやり方 1・2 の使用）を完了として消した。ユーザーは「40」と言ったが、該当する項目は無く、内容から 30 と読んだ。

### 2026-10-18（`init` `open` のコミットを、取り残しのステージで止めない。手順書のレビューを Next Actions 36 に積んだ）
- ユーザーが改善案を承認し、`commit_paths` に `only=True` を足した。`init` と `open` は、対象外のステージ済みの変更があっても止まらず、対象のパスだけをコミットする（対象外はステージに残る）。`start` `readme` `close` は、従来どおり止まる（既存のテストと意図を保つ）。単体テスト 1 本を足し、66 本中の失敗は同じ 2 本（`SharedPermissionTest`）。手順書のスクリプト版（3 章、9 章）と `room/README.md` を合わせて直した。決定は `decisions.md` の同日の項の追補。実機は未確認。
- 手順書 2 本のレビューは、ユーザーの指示で別のセッションに回した（Next Actions 36）。

### 2026-10-18（実名の手順書 2 本を草稿として書いた。`init` の既定コミットが、取り残しのステージで止まった件）
- ユーザーが、`init pilot3` と `open pilot3-1` を実機で試した。ステージはされたが、コミットされなかった。原因（確認済み）: 前の `close`（`pilot2-1`）で、`projects/pilot2-1/ai/records/room-log.md` の削除がステージされたまま残っていて、`commit_paths` の対象外チェック（並行する作業のステージ済みの変更を巻き込まない）が止めた。設計どおりの停止で、バグではない。ただし、`init` `open` の「戻る起点」が、取り残しのステージで黙って作れなくなる。改善案（未承認）: 対象外のステージがあっても、`git commit -- <パス>` で対象のパスだけをコミットする。
- ユーザーの決定（置き場と名前、内容）で、`guides/howto/ai-room-setup-script.md`（スクリプト版。`pilot2`）と `ai-room-setup-manual.md`（手動版。`pilot`。マウント・アンマウント、アンマウントできないとき、Zed の接続、`close` の副作用のコマンドを含む）を、今回の実機の通しの内容で書いた。`guides-index.md` に足した。`init --boundary` の Area 作成と既定コミットは、実機未確認と明記した。

### 2026-10-18（`room init` に Area の作成、`init` と `open` の初期状態の既定コミット。Next Actions 33・34 を閉じた）
- ユーザーが、コミットの範囲を `init` と `open` に決めた（`start` は複雑になるので対象外。AI は `start` の起動前に新しい追跡ファイルだけをコミットする案と、`ai/in/` の除外を勧めたが採らなかった）。決定は `decisions.md` の同日の項。
- 実装（`room.py`）: `init <Area> --boundary <印>` が `areas/<Area>/README.md` を作る（印が無ければ止まる。Area があり `boundary:` があれば何もしない）。`init` は終わりに Area の README だけを、`open` は Project のひな形と Area の README だけを、既定でコミットする（`--no-commit` で省く。`open` の `--commit` は互換のため残した）。`commit_paths` が、ファイルそのものを指すパスを許すようにした。単体テスト 5 本を足し、65 本中の失敗は直前から変わらない 2 本（`SharedPermissionTest`。この変更と無関係）。実機は未確認。
- `room/README.md` の使い方、コミットの記述、`init` の行を直した。

### 2026-10-18（実機の通しの後始末と、要望 3 件の決定）
- ユーザーの承認で、試験の部屋 `room-pilot` と `room-pilot2` を `wsl --unregister` で消し（`Ubuntu-24.04` は残る）、未追跡の試験メモ `exmem/inbox/2026-10-18-masking-notes.md` を消した。`room/README.md` の古い記述（`init` の実機未確認、`sleep infinity` の未確認、「未実装」の節、状態の行）を直した。
- 要望 3 件の方針を決めた（`decisions.md` の同日の項）: `room init` に Area の作成（`--boundary` 必須）、`init` が作ったものはコミットして起点にする（範囲は確認中）、実名で1手ずつ説明する手順書。Open Questions の3項は、決まったので `log.md` から外し、Next Actions 33〜35 に書き換えた。

### 2026-10-18（room の実機の通しと、バグ 2 件の修正。ユーザーの要望 3 件）
- ユーザーが、room の実機確認をまとめて行った。手作業版（部屋 `room-pilot`、Project `pilot-1`。`ai-room-setup.md` の第2・5・7章）と、スクリプト版（部屋 `room-pilot2`、`room init pilot2` から。Project `pilot2-1`、`pilot2-2`）。AI は `room` を実行せず、手順のサンプルを出し、出力を読んだ（`room/README.md` の「AI には実行させない」）。
- 通ったもの: `init`（分離の確認、道具の導入、ログインは人）、`open`、`mask`（ダミーの xlsx・csv）、`start`（端末版、`--no-launch` + Zed の WSL リモート）、`restore`、`readme`、`stock`、`close`（Zed を開いたままでも。部屋にマウントが残っていなければ通る）、`reap`、Excel（ピボットの更新、シート名、コメント。問題なし）。項目 26（`~/shared/workflow-kit/room/` に `README.md` だけ。`~/.claude/settings.json` に `Read(~/shared/**)`）と、項目 9（`close.md` の書き方で足りた）を閉じた。
- 直したバグ: ① `--no-launch` の待ちで Enter が戻らない（`d6c97d8`。`keepalive` をコンソールから切り離す。ユーザーが承認）。② `reap` が、削除に成功しても「消せなかった（）」と判定する（`086381c`。ユーザーが承認。テストに `|| true` の形を足した）。Gotchas に3件（`decisions.md`）。
- 手順の誤解: Zed を Windows のローカルのフォルダで開いていて、Agent が Windows 側で動いた。ユーザーの操作の取り違えで、`room start` の経路の不具合ではない。見分け方を Gotchas に足した。
- 未確認: 項目 20、10、`base_stale`、`restore` の上書き保護（`final-manifest.json`）、Zed を開いたままのアンマウント（今回は掴むプロセスが無かった）。`pilot2-2` の1・2回目の `start` の履歴が部屋に残っていない件（原因不明。3回目以降は `-mnt-room-pilot2-2` ができた）。
- ユーザーの要望 3 件を Next Actions 33〜35 に、「やる必要があるのか」の点を Open Questions に足した。①`room init` に Area の作成（`boundary:` を含む）、②`room init` の初回コミット、③スクリプト版・手動版の実例のコマンド集（`guides/howto/`）。AI の候補 6 件も同じ項に足した。
- 試験の後始末は未実施: 部屋 `room-pilot` と `room-pilot2`（`wsl --unregister`）、`exmem/inbox/2026-10-18-masking-notes.md`（未追跡の試験メモ）。いずれもユーザーの確認が要る。

### 2026-10-18（Next Actions 28 を閉じた: 画面に出る量の抑制）
- ユーザーが、Zed の agent では `/focus` を入力できず、端末でも使えなかった（実機）ので、28 を閉じると決めた。画面に出る量を減らす手段は、これ以上追わない（`bashEditDiffEnabled: false` の検討も打ち切り）。Stop フックの記録（保存側）には影響しない。S3（キャッシュの間を記録に足す案）は 29 に移した。`exmem/lessons/claude-code-storage.md` の Next Actions の `/focus` の項と Open Questions の `/focus` の項は、更新していない（`wrap` は exmem に書かない）。
### 2026-10-18（`rebase` の許可: Next Actions 32 を閉じた）
- ユーザーの依頼で、スクリーニングのサブエージェントを1回起動した（推奨は保留。弱点は deny の置き場が未確認）。ユーザーが、禁止が2つの論点（履歴の整理と、分岐の解消）を一緒にしていたと指摘し、分岐の修正と衝突の解消に限り許可すると決めた（型 D）。`docs-rules.md` に「`rebase` の許可」を足し、push 条件 3 の食い違いを直した。deny は dotfiles の `home/.claude/settings.json` にあり、エージェントは自分の権限設定を書き換えられない（分類器が止めた）ので、ユーザーが `git rebase*` の 4 行を、`-i` `--interactive` `--exec` `-x` `--root` 付きの 20 行に直し、AI が diff を確かめた（1 回目は `--interactive` のダッシュが 1 本足りず、`--x*` のタイプミスがあった）。実機で `rebase --continue` は通り、`rebase --abort -i` は止まった。決定は `decisions.md` の同日の項。
### 2026-10-18（Stop フックを1つにまとめる決定）
- ユーザーが、費用・トークンの推定と応答本文の保存を1つの Stop フックのスクリプトにまとめると決めた。理由は、モバイルの2セッション（保存と標準出力、キャッシュ・費用の実験）がどちらも Stop フックにたどり着いたこと。共有フォルダの `stop-record.py` が、すでに両方を行う。決定は `decisions.md` の同日の項。画面に出る量を減らす話は Stop フックの範囲外なので、Next Actions 28 に分けて残した。
### 2026-10-18（`review 消化` の 2 回目: 閉じた項目と統合）
- ユーザーの承認で、Next Actions 18（用語の置き換え。残りの `topics/` のノートは「使うときに直す」方針で足りる）、25（移した先を読み忘れないか。次に使うときに見る性質）、27（今回の揃えの確認。`pwsh` の部分は、この PC で `check-hook-outline.ps1` と Python 版がどちらも全 OK・exit 0 で済んだ）を `log.md` から消した。
- 12 と 14（どちらも `user-manual.md` の補正策の反映）を 12 に統合した。24 の「`exmem/inbox/` に未統合のメモが 1 件」（`465bd86` で統合済み）と、Open Questions の全フック改善表の「`pwsh` 版と Python 版の結果が同じか見る」を削った。31 の対象から 18・12・14 を外した。
### 2026-10-18（承認プロセスの仕様化）
- ユーザーの素案（3層: チャット内の仮決め、他 AI のスクリーニング、最終確認）を、過去の覆し5件（cwd 前提、`.obsidian` の置き場、`_noai` 廃止、跨ぎ、kit-growth の docs）の分析をもとに検討した。型 A〜E を分け、型 A（先行する決定を示さない）と型 D（論点の混同）は、作業中に仕組みの承認へ頭を切り替えたことが原因というユーザーの見立てを採った。
- 決定: 対象は `decisions.md` に残る決定だけ（案 A）。仮決めは見出しの印（案 A）。期限切れは自動で変えず、延長1回で保留（案 A。拾うのは `start` でなく `review`）。2層目は、決定の直後でなく `review 消化` でまとめて動かす（ユーザーの提案。頭を冷やす時間を確保）。決定は `decisions.md` の同日の項、手順は `workflow-kit/approval-screening.md`。`20f4393`。
- 同日、`origin/main` が先に進んでいて rebase が必要になり、エージェントの `rebase` は deny で止まった。ユーザーが端末で完了した。`rebase` の許可は Next Actions 32。
### 2026-10-18（取扱説明書に、ローカルログからの 2 回目の分析の補正策を足した）
- ユーザーの依頼で、この PC のローカルログ（2026-09-26〜10-14、重複を除いて約 820 発言）から、思考の癖・悪影響・補正策を分析した。新しい癖 5 つ（手段で頼む、前提を言わない、名前と置き場の変更が連発、作業ツリーの帰属が混ざる、見た目の調整が反復）と、既存項目の範囲の補正（削る、推奨、失敗の分析、頭を冷やす、理解してから決める）を見つけた。AI の推測。
- 書き込み先: ユーザーが「補正策は公開側、評価は auto-memory」を選んだ。取説は公開リポジトリにあるため。`exmem/lessons/user-manual.md` の Principles に補正策、`user-thinking-habits.md` に追補、評価と個人的事情は auto-memory（公開しない）。決定は `decisions.md` の同日の項。
- 残り: Next Actions 12（補正策を手順書へ反映）。PC1 と 10-15 以降のログは未分析。
- 起票が古い 1（PC1 の印象。キャプチャで移行済みで、次回も同じやり方。ユーザー）を閉じた。実機の確認項目は別チャットで行う（ユーザー）。`origin/main` が先に進んでいたため、ユーザーの承認で `rebase` が必要になったが、エージェントの `rebase` は deny で止まり、ユーザーが端末で `rebase --continue` を実行した。`rebase` の許可は Next Actions 32 に足した。承認プロセスの見直し（30）は、ユーザーの素案で検討を始めた。
### 2026-10-18（`review 消化` の出力を3リストの順に固定した）
- ユーザーの指示で、`review-hook.md` の「消化モード」を、「すでに close していそうなアイテム」「すぐに close できそうなアイテム」「起票が古いアイテム」の順のリストに直した（旧: 3区分と「それ以外」の2分割）。決定は `decisions.md` の同日の項。
### 2026-10-18（`review 消化`: 完了項目の整理と「間」の TTL 基準化）
- ユーザーの承認で、Next Actions 3（token-matrix の初回採点。`70b8e22`）と 23（`[review]` コミットの日付取得。`846c3d7` `48c1e27` で取れている）を消し、6 と 9 の済んだ部分を削った。6 の「入力 8 の基準がまだ無い」は事実と違った（基準は `docs/alignment-baseline.md`）。Open Questions の全フック改善表は、残りだけを書く形に縮めた。
- 続ける・切るの「間5分」を TTL（サブスク1時間、API キー5分）基準に直した。`workflow-kit/hook-common.md` の「次にやること」、`token-matrix.md` の「切る」の定義、`exmem/lessons/session-handoff.md` の Principles と Decisions（切る式 H − B と残りターン数を含む）。Open Questions 2 件（間5分、理由の文言）を閉じた。決定の根拠は `session-handoff.md` の Decisions。
- 残り: 項目 24 のローカル TTL の実機確認と再実験。
### 2026-10-18（kit 改善の docs を直下の `docs/` に統合した）
- `topics/kit-growth/docs/` の `log.md` `decisions.md` `log-history.md` を、直下の `docs/` に統合した（案 A。ユーザーの決定。圧縮は別作業）。きっかけは、`review 消化` が `topics/` に届かないという質問。調べると、kit-growth を `topics/` に置いた理由（窓口）と docs の置き場を区別していなかったことが原因だった。判断は `decisions.md` の「kit 改善の docs を … 統合した」。以降の項（2026-10-18 以前）は、統合前の kit-growth の経緯と直下の経緯を、日付順に並べたもの。
- 統合の後、ユーザーの依頼で Next Actions 30「承認プロセスの見直し」を足した。ユーザーはモバイルの小さい画面で読むため承認項目を見逃しやすく、見落としによる決定の覆し（今回の docs 統合が一例）を減らしたい。調査と案は未着手。
### 2026-10-18（キャッシュの実験と費用の考察）
- ユーザーの依頼で、フックの読み込み量を円に換算し（7フックを1回ずつで約27円。Sonnet 5.5、1ドル158円）、キャッシュとバッチ実行を調べ、クラウドで4条件の実験を実行した（同じ読み取りだけの3ステップ。続けて $0.121、別会話 $0.130、6分あけ・1時間TTL $0.276、6分あけ・5分TTL $0.387）。結果と考察は Project の共有フォルダ `notes/token-saving/` の 2026-10-17 の 4 ファイルと `2026-10-18-cache-insights.md`。
- 分かったこと: 主な会話の TTL はサブスクで1時間、API キーで5分。間が TTL を超えると会話の大半を書き直す。実セッションの費用は書き込みが5〜7割。続ける・切るの数値（約10万、約2万）の考え方は合う。「間5分」はサブスクでは1時間にそろえる。
- 決定は無し。改善案は `log.md` の Open Questions に4行。知識は `exmem/inbox/2026-10-18-prompt-cache-gap-cost.md`（`fb19ac2`。点検は FAIL なし）。`lessons/` と kit の手順書は、承認前なので変えていない。
### 2026-10-17（inbox の選別、振り返りを定期と突発に分けた）
- `68cc932`: inbox の未選別 2 件（画像の取り込みの型、`sessions`）を見送り。`dc7a598`: 改善4 を「振り返り（定期）」に改称し、改善5「振り返り（突発。なぜなぜ）」の叩き台 `retrospective-method-2.md` を足した。施策に ID と検証項目を付ける。決定は `decisions.md` の先頭の項。
- 未実施: 改善5 の品質チェック 3 回、改善4 の「定期」としての使い方の反映。`exmem/lessons/workflow-kit.md` の未コミット差分は、このセッションの変更ではないので含めていない。
### 2026-10-17（初回の review）
- 初回の `[review]` コミット `846c3d7`。点検スクリプトは FAIL なし。機密の点検は、ヒットがすべて説明文かテストの固定文字列で、機密なし。未統合メモ 0 件、30日更新の無いトピックなし。`hook-matrix.md` の字数の行と、共有ファイルの基準（`docs-rules.md` 10,000、`hook-common.md` 4,435、`hooks.md` 4,552）を更新し、`token-matrix.md` の点の履歴に簡易採点（103、下がった列なし）を足した。ユーザーが案をすべて承認。
- 未実施: 入力 7（変更・調査・振り返りのやり方の Must）の点検、入力 8（リポジトリ間の整合の基準）、`reviews` の記録先。`kit-growth` の `decisions.md` に、`→` の無い【汎用】が 73 件ある。
### 2026-10-17（start のやり方・モードの項目の整理）
- 決定は `decisions.md` の先頭の項。項目 11 の解決済みの記述を外し、Open Questions の 2 件（`method-creation.md` の 5〜12、調査1の 4 回目の効果）を閉じ、項目 15 の案 B を承認した。

### 2026-10-17（施策1の採用、部屋の共有知から room のコードを外した、用語の置き換えの続き）
- 決定と確認は `decisions.md` の同日の項（先頭）。施策1を `user-manual.md` に足した。`room.py` が `workflow-kit/room/` の `README.md` 以外を送らないようにし、単体テストを足した（変更前から失敗している 2 件を除き通過）。`exmem/lessons/` の現在形の記述 5 ファイルで、「Vault」「ワークスペース」を works にした。
- 未実施: `topics/ai-workspace-boundary/` のノートの語（約 80 件）。そのトピックは 2026-10-18 に削除した（移管のとき `ai-room-why.md` は新しい語で書いた）。

### 2026-10-17（review の消化モードの対象を明記した。点検スクリプトを pwsh で実行した）
- `review-hook.md` の消化モードの対象を、「このセッションで作業した単位（「<名前> の続き」で読みに行った単位を含む。無ければ呼び出し元）の `docs/log.md`」に直した。ユーザーが承認（本日）。Open Question を解消。
- `tools/check-hook-outline.ps1` を `pwsh` で初めて実行した（確認: 実行出力）。FAIL 4 件: ① `init-hook.md` の見出しが「目的 → 契機 → モード」で、スクリプトは「前提」しか許さない。② `wrap-hook.md` の「事前確認」の参照にフックのファイル名が無い（`start` の手順を指す）。③④ `room-context.md:21` の手順「コミットする」「昇格の案を出す」にも同様。NOTE: `open-hook.md` 5,596 字、`start-hook.md` 5,637 字が目安 5,000 字超。いずれも手順書・スクリプトは未変更(承認待ち)。
- 23 は、ユーザーが `review` のコミット日を有力と判断。決定は未確定。

### 2026-10-17（Python 版の点検スクリプト、用語を works に統一、窓口は2つのまま）
- 決定と数値は `decisions.md` の同日の 2 項。`check_inbox.py` `find_knowledge.py` を足し、ps1 版と出力が一致することを確認。works を指す語は「works」に変更し、kit・ルート・`guides/` で置き換えた。点検スクリプトは FAIL なし（exit 0）。
- 14 の調査: `.obsidian` の 2 件（`app-config-placement.md` の Gotchas＝前提の見落とし、`human-ai-decision-loop.md`＝先行する決定の見落とし）。前者が cwd の件と同型の候補。判断はユーザー。
- 16 の説明（メリット・デメリット）: 外すと、部屋へ送る tar が約 142 KB（`room.py` 58 KB、`maskkit.py` 27 KB、テスト 68 KB のうち、README を除く分）小さくなり、部屋の AI の検索に出るノイズが減る。デメリットは、`room/README.md`（10 KB）へ張った参照が部屋の中で切れること、部屋の AI が `room` コマンドの挙動を読んで答えられなくなること。中間案: コードとテストだけ外し、`README.md` は残す。決定は未了。

### 2026-10-17（`open` と `start` を分割して畳んだ。works を指す語を「個人ワークスペース」にした）
- ユーザーの決定と数値は `decisions.md` の同日の項。`project-structure.md` と `start-work-types.md` を新設（原文のまま）、`open` 2,924 字・`start` 4,827 字、点検スクリプトは FAIL・NOTE なし（確認: pwsh の実行出力、exit 0）。`log.md` の Open Question（`start-hook.md` の字数）を解消。push は未実施（ユーザーが後でまとめて行う）。

### 2026-10-17（review のコミット日の約束、点検スクリプトの FAIL の解消、用語「領域」）
- ユーザーの決定（`decisions.md` の同日の項）: 前回の `review` の日付は `[review]` コミットから取る。点検スクリプトの FAIL は案Aで直す。用語は「領域」。21/20 の残りと 20 の部屋の確認は別セッションへ。
- 直したもの: `review-hook.md` の手順「コミットする」（`[review]` 接頭辞、`--allow-empty`、日付の取り方）、`start-hook.md` `wrap-hook.md` の日付の元、`check-hook-outline.ps1`（「モード」の許可、他フック参照の除外）、`room-context.md` `wrap-hook.md` の手順参照。pwsh で再実行し FAIL なし（確認: 実行出力）。NOTE は `open` 5,596 字、`start` 5,681 字。
- `open` と `start` を畳む案を出した（案のみ。未承認。内容は同日の会話）: open は「Project の構造」2,241 字を `project-structure.md` へ原文のまま移し、「未決」888 字のうち log.md の Open Questions と重複する項を削る。start は「作業の種類の差分」998 字を別ファイルへ移す。弱点: 移すだけでは総量は減らず、字数の目安を満たすだけになりうる。

### 2026-10-17（フックの報告の型を共通の項目と固有の項目に分けた）

- ユーザーが、7フックの報告の型の比較表（プロジェクトのファイル `notes/hook-report-forms/2026-10-17-comparison.md`）の見直しを依頼し、推奨を承認した。共通の項目（ユーザーに求めること、コミット、次にやること）を `hook-common.md` に一本化し、各フックは追記と固有の項目だけにした（`52de581` `044aa54` `1ec375e` `9c7a012` `edb9b9a`）。
- 改善案は報告に載せず、Open Questions に残す形に全フックを揃えた。`integrate` も push する。`wrap` の「終了時の1問」（2026-10-08 の案E の入力）と `stock` の「終了処理の案内」を廃止し、`wrap` の依頼文は共通の「次にやること」に移した。続ける・切るの暫定の数値を置いた。
- 点検スクリプトは書き換えたが、`pwsh` が無く実行していない。報告の型の番号、改善案の不在、共通の項目への参照は、同じ規則で手で確かめた。`open`・`start` は字数の目安 5,000 字を超えたまま。
- 「ナレッジ化して」で、続ける・切るの数値の目安を `exmem/inbox/2026-10-17-session-cut-cache-thresholds.md` に残した。

### 2026-10-17（フックを領域 × r/w 属性で管理した）

- ユーザーが、AI 作業部屋の中のフックの制約（実行、出力ファイル）の調査から、フックの実行単位を人が覚えられない問題へ進み、領域（works、workbase、dotfiles、room）× r/w 属性での管理を選んだ。跨ぎは型3つ、`init` の初回は例外、dotfiles にも `docs/`、遠回りの答えは窓口に直接書いてよい。
- 重複の整理も依頼され、実施した: `hooks.md` に表を足し、`hook-matrix.md` の cwd の3行を1行に、`open-hook.md` `init-hook.md` `room-context.md` の実行場所の記述を表を指す形に、`wrap-hook.md` の遠回りの答えと昇格の案の部屋の扱いを更新した。決定は `decisions.md`。
- `pwsh` が無い環境で作業したため、`check-hook-outline.ps1` は実行していない（章の見出しは変えていない。表の一致は目視）。`room` の単体テスト 59 件は通った。

### 2026-10-17（「振り返りのやり方1」を足した）

- ユーザーが思考の癖の分析の手順を「振り返りのやり方1」にするよう依頼した。違いは2点: 対象が個人でなく業務の進め方・成果物、良い点と悪い点の両方を出す。叩き台に、ユーザーが他のモードを参照して出力の章立てを固定するよう求め、区分は改善、呼び出しは `start 改善`、良い点・悪い点は各最大3個(仮)、評価軸の設計を章立てに含める、冒頭にサマリを置く、と決めた。
- 新しい会話で3回実行して(題材 A = workbase 自身)迷った点を 14 → 10 → 6 に減らし、手順書(v4)を登録した。3回目で、AI が数えた手戻り14件と、遠回りの自己申告の差が出た。記録は `records/retrospective-method-record.md`。
- 遠回りの答え: なし(ユーザー回答、2026-10-17)。

### 2026-10-17（取扱説明書に思考の癖の補正策を足した）

- クラウドのスレッド18本のユーザーの発言から、思考の癖12項目、悪影響、AI の補正策を分析した(AI の解釈。PC1・PC2 の会話は未確認)。ユーザーが「下書きは問題ない」と承認し、補正策9行を `user-manual.md` の Principles に、分析の本体を `user-thinking-habits.md` に置いた(`aeb68e9`)。悪影響への対応は、他のセッションで徐々に進める(ユーザー)。遠回りの答え: 未回答。

### 2026-10-17（「調査のやり方2」を足した）

- ユーザーが SSH 鍵の手順書を3回の指摘で仮決めし、「やり方のやり方」に沿ってその要因を型にするよう依頼した。後から「調査のやり方2は手順を調べること。技術的なインストールやルール・仕組みに沿うこと」と定義された。叩き台を新しい会話で3回実行して基準と比べ、直した（1回目: 日常の使い方・移行元・管理・分量の換算、2回目: 手順を調べる段、3回目: 線引きの細部）。3回目に一次情報の確認と Linux での試行が働き、基準にない落とし穴が見つかった。
- 「やり方のやり方」の手順6が、品質チェックの記録を `records/` に残す形に更新されたので、`research-method-2-record.md` に残した。承認後、`methods.md`・`start 調査`・`hook-matrix.md`・`exmem-index.md`・lesson を、調査1の登録に合わせて足した。決定は `decisions.md` の同日の項。

### 2026-10-17
- Zed（ACP 経由）の Claude Code で、`/status` と `--output-format json` の session_id・費用が取れるかを調べ、代わりに Stop フックで記録する手順書とスクリプトを作った（共有フォルダ `notes/stop-hook-record/` と `notes/token-saving/2026-10-17-zed-session-cost.md`）。端末相当の `claude -p`（クラウド、Haiku）で、Stop の入力と集計が動くことを確かめた。Zed と WSL2 の実機は未確認。知識は `exmem/inbox/2026-10-17-claude-code-session-cost-record.md` に残した（ユーザーの依頼による手順作成、stock、wrap）。
### 2026-10-16（「調査のやり方1」と `start 調査` を足した）

- Claude スキルの調査が、ユーザーの評価で「ほぼ完璧」の出来だった（冒頭の3行、経緯の表、事実と所感の分離、一次と二次の分離。改善点は具体例の不足）。背景の推測を振り返り、「調査のやり方」を変更と同じ2ブロック（仕込み + 調査プロセス）で足した。ユーザーの入力の問い（9項目）と最終形の章立てを、ひな形として `research-method.md` に置いた。`start 調査` は、やり方を選ぶ1問を省き、仕込みの宣言から始める。
- ユーザーの整理（推測1と2が仕込み、3以降がプロセス）を一部変え、4を想定読者として仕込みに移した（品質チェックの後にユーザーが承認）。決定は `decisions.md` の同日の項。

### 2026-10-16（room の type に dev-env と dev-test を足した）

- ユーザーの依頼で、`open-hook.md` の type 別の表、`room.py` の `--type`、README の雛形、`dev-deliverable-guide.md`(末尾に節)を更新した(`ccfe968`)。
- ユーザーの指摘で、GitHub / GitLab のようなサービスは権限が無く AI に頼れないと分かった。`dev-env` は type を増やさず「環境の置き場」を聞く項目にし、`remote` の type は未決に残した。

### 2026-10-16（`review 消化` を初めて使い、Next Actions 3件を完了にした）

- ユーザーの答えで、NA 0（入力 8 の残りのギャップ）、NA 2（`start` のモードを試す）、NA 5（`start 解決` / `start 改善` と `review 消化` を使う）を完了にして消した。NA 3（重い会話の確認）は、まだ見ていないので残した。「選ぶ基準・10件超の目安が合うか」は、使った結果、合わない点は出なかった（ユーザーの答えに指摘なし）。

### 2026-10-16（topic-workflow を取り込み、close した）

- 止まっていた TODO 5 を見直した。足す側（docs-rules の読む順・「続き」、窓口の雛形）は済んでいたので、正本を `topics/AGENTS.md` にして、畳む側だけを行った。並行セッションの `close-hook.md` の削除（`c86b4d6`）と `topics/AGENTS.md` で重なり、マージした。
- topic-workflow は新しい「トピックを終わらせるとき」の最初の利用。【汎用】の Q4（共有フォルダ）だけ未反映だったので `topics/AGENTS.md` に足した。差分は `notes/topic-workflow/2026-10-16-kit-intake.diff`（プロジェクトの共有フォルダ）。

### 2026-10-16（`open` / `close` を畳む議論。`open` の Project の構造を `ai/` と `_noai/` に対応させた）

- ユーザーの問い「`open` と `close` は `room` に統合されて不要では」から始め、両手順書の役割を洗い出した。ひな形・状態更新・`archives/` への移動・コミットは `room` が担う。残るのは、部屋の AI の判断（`readme-draft.md`、`close.md`）、「Project の構造」の表、トピックの close だった。ユーザーは `close` をトピック専用にして `topics/AGENTS.md` に吸収する、`open` は構造に限定する、と決めた。
- `open` で、type 別の構造（`drafts/` `refs/` `src/` `sources/`）と `ai/` `_noai/` の対応を調べた。`_noai/` を外す案（直下にベタ置き）は、影響を調べて見送り、`_noai/` を残す（理由: type ごとの割り当てが要らず、追跡しない領域を一段で分けられる）。`ai/in/` へのシンボリックリンクは成り立たない（部屋から行き先が見えない）。
- 途中で出た前提: AI が使えなくなる（トークン制限）ケース。`restore` が `final/` を無条件に上書きする点を確認したが、別の話にした。リポジトリが正の `src` は、`restore` が `.git` の中身で止まることを確認し、残件にした。
- 差分は `notes/open-structure/2026-10-16-ai-mapping.diff`（プロジェクトの共有フォルダ）。コミットは `7b2c515`。
- 続けて、ユーザーの「キットに反映お願い」で `close-hook.md` の削除、`topics/AGENTS.md` への節、`room-context.md` への `close.md` の書き方の移動、`open-hook.md` の縮小を行った（`c86b4d6`）。`open-hook.md` は 6,748 字から 4,687 字、手順は 8 から 6、報告は 5 から 3。`hook-matrix.md` の基準の `open` 3,320 字は、実測と合っていなかったので下げ直した。

### 2026-10-16（「変更」を areas/projects に適用し、「基準文書」に改称した）

- 部屋の構成（`ai/work/`、`mask` `restore` `--adopt`、`close`）と突き合わせ、論点を2つ見つけた。①「中間成果物」が `ai/work/` の下書きの意味と衝突する。②繰り返す成果物は、次の変更が別の Project で起きるので、`close` の後も基準を渡す必要がある。ユーザーとのすり合わせで、①を役割で名づけ直し（向きによらず、変更の入力と検証の物差しになる文書。「基準文書」）、②を `ai/in/` + `--adopt` で解いた。置き場と機密の決まりは `decisions.md` と `change-method.md`。ユーザーの仮説「人と AI は工程を分割し、その境界が基準文書」も記録した。コミットは `40d8aa6`。

### 2026-10-16（「変更のやり方」を Must / Want で足した）

- `init 更新` が一撃で通った要因を振り返り、「変更のやり方」を解決・改善のやり方の延長に足した。ブロックA（仕込み。中間成果物）とB（変更）に分け、プレイブックの3文書（要求仕様・機能仕様・運用マニュアル）を中間成果物の出どころとして格下げした。ユーザーの条件は「ガッチリ定義しない。Must と Want で小さく始め、`review` の対象にする」。`methods.md`、`exmem/lessons/change-method.md`、`hook-matrix.md` の「review の点検」7、`exmem-index.md` を更新。決定は `decisions.md` の同日の項。

### 2026-10-16（init に `init 更新` を足した）

- ユーザーの依頼で、雛形の更新を works に反映するモードを検討し、案 B（基点つきの3者マージ。案を出して承認後に反映）を選んだ。`init-update.md` を新設し、`init-hook.md`・`hooks.md`・`docs-rules.md`（`Template-Rev` トレーラー）・`hook-matrix.md` を合わせた。決定は `decisions.md` の同日の項。`git merge-file` で、埋めた行が残ることと、旧版 → 新版の雛形の変更が当たることを一時ディレクトリで確認した（衝突 0）。
- 同日の追加（ユーザーの指摘）: 雛形の読む順番が指す `README.md` を項目 5 が生成していなかったので、`templates/workspace/README.md` を足し、生成物と初回コミットに含めた。`init-hook.md` の自己点検のトレーラーを2行（`Workflow-Kit` は廃止済み）に直した（`8b74187`）。`hook-matrix.md` の `init-update` の字数を 7.9k に直した（初出の 3.9k は誤り）。
- 続けて、`init 更新` が一撃で通った要因を話し合い、「変更のやり方」を解決・改善のやり方の延長で足す案が出た。議論は次のセッションへ(log.md の Next Actions 8）。

### 2026-10-16（各フックの cwd の期待を点検し、review の点検対象を 3 リポジトリに広げた）

- 各フックが期待する cwd と書き込み先を突き合わせた。`review` は起動した単位 1 つの記録だけを見ており、works から起動すると resources の `exmem/inbox/`・`topics/` と、公開リポジトリ（resources、dotfiles）の機密が点検されなかった。works の基準に「点検の対象」の一覧を置き、入力 3・4・6 がその全リポジトリを見るようにした（`302fccb` `9b19540`。ユーザーの決定、案 A）。
- 見つかった食い違い 4 件を直した（`9b19540`）: `wrap` の終了時の 1 問は起動した単位に記録、`exmem/AGENTS.md` と `exmem/README.md` の「exmem で起動する」を「`resources/` で起動し exmem の続きで扱う」に、`open` と `close` に実行場所（部屋の中。副作用は人が `room` で行う）を明記。
- 各フックの cwd の期待を `hook-matrix.md` の Must の 3 行に記録し、`review` の点検に含めた（`53c3771`）。あわせて、手順「網羅度を確認する」の本文を `hook-matrix.md` の「review の点検」に移し、`review-hook.md` を 4,623 → 4,183 字にした。入力の数は増やしていない。次回の `review` が初回の比較になる。

### 2026-10-16（wrap を軽くした、フックの重さの基準）

- `start 改善`（改善3: 星取り表）で `wrap` を軽くした（`9fbf4e4`）。`docs-rules.md` は「コミットと push」の節だけ読む（約4k字減の見込み。実測は未）、報告を6項目から5項目、改善案は Open Questions に足して `review 消化` で承認を取る。見送り: push 条件の `gh repo view` を毎回やめる案、手順1の対象特定を縮める案、「このフックの改善」章を畳む案（改善案の移し方で代替）。
- 各フックの字数・手順の項目数・報告の項目数を `hook-matrix.md` の「重さの基準」に固定し、`review` が比べる形にした（`da81042`、ユーザーが設計を採用した記録は `dc2931d`）。字数 +20%、項目数 +2 以上で見直し対象。N は3回の `review` の後に決め直す。判断は `decisions.md` の同日の2項目。
- 終了時の1問: 遠回りなし。

### 2026-10-16（review の消化モードと start の引数つきモード）

- 並行作業で完了済みの Next Actions / Open Questions が残る問題に、フックを増やさず対応した。`review` に消化モード（`review 消化`。完了の可能性・すぐ完了・それ以外に、根拠つきで分ける。完了の判断はユーザー）を足し、`start` が合計10件超のとき一度だけ勧める（`f395e34`）。「10件」は仮置きで、実測していない。
- `start` に `start 解決` / `start 改善` を足した（`8242e1c`、名称は `c0a46cb` で「問題解決」から「解決」に変更）。インタビューの代わりに、ゴールを聞いて、やり方を選んで始める。引数なしの `start` は残した。
- やり方の置き場を検討し、案 C を採った(`28202d7`、ユーザーの承認): 選ぶ基準と骨子は `workflow-kit/methods.md`、理由・実例・落とし穴は `exmem/lessons/` に残す。`lessons/` は統合や改名で参照が切れやすく、手順の入口には不安定なため。
- 決定記録に追記したとき、PowerShell の二重引用符内のバッククォートが制御文字に化けた（`` `review` `` の `` `r `` が改行、`` `again` `` の `` `a `` がベル）。元の版から書き直した（`c0a46cb`）。追記は単一引用符で行う。

### 2026-10-16（共有側から works への名指しを外した）

- 共有側（resources）が works をリポジトリとして名指しする説明を、「ワークスペースのルート」に言い換えた（窓口、手順書、`room.py` のヘルプ文、設計・引継ぎ 5 本）。works 固有の運用記録 `guides/explain/agent-safety-rules.md` は works の `docs/explain/` へ移し、`guides-index.md` と `review-hook-why.md` の参照を外した。kit の `init` フックと `room` が works の PARA 構造を前提にすることは許容。判断は works の `docs/decisions.md` の先頭の項（ユーザーの決定）。コミット `6d8f427` `b50bab2`。遠回りの答え: なし。

### 2026-10-16

- works、resources、dotfiles の `AGENTS.md`・README・`docs/log.md` の規則を揃える作業をした（フェーズ1〜3。一律に kit を正とはしない方針で、明らかなずれは事前にユーザーへ確認した）。kit の変更: `docs-rules.md` を読む時機の統一、階層化の規則、機密の項の畳み、workspace 雛形の写しの除去、`review` の入力 6（機密の点検）と入力 8（リポジトリ間の整合）。判断は `docs/decisions.md` の「2026-10-16」。dotfiles 側は README を 34.8KB から 16KB に分割し、`log.md` を 17.9KB から 3.8KB に縮めた。コミット: resources `9c87f10` `2156d92` `2a35149` `3cdeeb1` `286d714`、dotfiles `cc20299` `71e326d` `000125e` `a404711` `293c0a3`、works `142c226`。遠回りの答え: なし。

### 2026-10-16
- `docs/log.md` の Next Actions 3件を、ユーザーが完了と確認して消した。① 「push はユーザーが行う（許可リストなし）」: 同日に公開リポジトリのまま、エージェントが `main` に push してよいと決定済み（`decisions.md` の「cwd はリポジトリのトップだけ…」）。`git fetch` 後に `origin/main..HEAD` が空であることも確認した。② 「`guides/` の `CLAUDE.md` は本文を持つ」: `bda9216` で `AGENTS.md` へ改名し、`CLAUDE.md` は `@AGENTS.md` の1行になった。③ 「`handson/` は削除予定」: `8b9222f` で削除済み（`ad3e966` で README の行も除去）。Open Questions は元から「なし」。`decisions.md` の該当行に、変更後の状態を補足した。
- 3リポジトリ（works、resources、dotfiles）の cwd の扱いを揃えた。resources に `README.md`（窓口）と `docs/`（`log.md` `decisions.md` `log-history.md`）を新設し、`AGENTS.md` の「読む順番」を追加した。kit の `docs-rules.md` に「上の階層で起動して『〜の続き』と言われたら」を足し、`hooks.md` の「起動する場所（cwd）」はそこへのポインタに畳んだ。判断は `decisions.md` の「cwd はリポジトリのトップだけ…」。
### 2026-10-15

- cwd の明文化（topic-workflow の TODO）を、ユーザーがカードで5問選んで決めた（起動場所、読む順番、上の階層からの続き、部屋、`wrap` の書き込み先）。kit 5ファイルを変え（`4997f7a`）、判断は `docs/decisions.md` の「2026-10-15 cwd を明文化した」。
- トークン消費を抑える改善を、改善のやり方3（観点のランキング → 星取り表 → 修正・削除・追加の案 → 優先度 → 実施項目の確定）で進めた。12観点から上位4点、さらに切る・絞るに絞り込み、ユーザーが選んだ13件を反映した（`d1150f2`、`a74a017`、`a46cf2e`）。星取り表の点は、切る 10 → 16、絞る 18 → 24。判断は `docs/decisions.md` の「2026-10-15 会話を『切る』と出力を『絞る』の対応を入れた」。やり方は exmem の `lessons/improvement-coverage-matrix.md`（`fbbefa0`）。
- `review` の入力に、トークン消費の自己採点を足した（`4a294b2`、`6bd1a2a`）。星取り表は `workflow-kit/token-matrix.md`（4観点、基準値 103）。
- 既存のワークスペースの `AGENTS.md` の読む順番は、ユーザーが各 PC で直した（2026-10-15、ユーザーの申告）。
