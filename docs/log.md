# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。kit の改善（旧 `topics/kit-growth/docs/`）も、2026-10-18 からここに置く。トピックの中身は各トピックの `docs/`。作業の終わりに Next Actions と Open Questions を更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。定例は実行したら次回の期日に書き換える。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| なし | | | |

更新: 2026-10-19（改善4 の手順書を読後の指摘で v5 に直し、第1回を組み直した。項目 38 は残り 3 点。経緯は `log-history.md` の 2026-10-19）

## 状態

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
- 2026-10-17 の作業は `807dd29` まで push 済み（`main`）。決定は `decisions.md` の同日の 4 項、経緯は `log-history.md`。
- 仕組みの決定は、作業中に承認を求めず、`review 消化` で待ち行列 → サブエージェントのスクリーニング → 最終判断の3段で承認する（2026-10-18。`approval-screening.md`、決定は `decisions.md` の同日の項）。仮決めは `【仮 〜日付】`（7日、延長1回）。
- キャッシュの実験をクラウドで実施した（Project の共有フォルダ `notes/token-saving/` の 2026-10-17 の 4 ファイルと `2026-10-18-cache-insights.md`）。5分TTL で6分あけると同じ作業が3.2倍、会話を分けても1.1倍、フック1回の読み込みは3〜6円。サブスクの主な会話の TTL は1時間、API キーは5分（公式 docs）。続ける・切るの数値の考え方（H − B、残りターン数）は実測と合った。決定は無し（改善案は Open Questions）。メモは `exmem/inbox/2026-10-18-prompt-cache-gap-cost.md`（`fb19ac2`）。

- `room init` が Area を作り（`--boundary` 必須。既定値なし）、`init` と `open` の初期状態を既定でコミットするようにした（2026-10-18。`--no-commit` で省く。`start` は対象外）。単体テストのみで、実機は未確認。次の実機で `init <新しい Area> --boundary internal` と `open` を試す。決定は `decisions.md` の同日の項、`room/README.md` に反映済み。
- room の実機の通しは済んだ（2026-10-18。`init`、`open`、`mask`、`start`（端末版と `--no-launch`）、`restore`、`readme`、`stock`、`close`、`reap`、Excel、手作業版）。直したバグは `d6c97d8`（待ちの Enter が `input()` に届かない。`keepalive` をコンソールから切り離した）と `086381c`（`reap` の確認の `ls` が、削除の成功を失敗と判定した）。未確認: 項目 20、10、`base_stale`、Zed を開いたままのアンマウント（今回は部屋に掴むプロセスが無く通っただけ）。

## Next Actions

39. room の実機の確認の残りを、まとめて PC で行う（旧 `topics/ai-workspace-boundary/` の残件。2026-10-18 に root へ一本化し、トピックは削除した。ユーザーの方針: 作業をキリの良いところまで進め、まとめて確認する）。① 実データで `mask` の警告量を見る。② Windows で Vault 側 deny の書式 `Read(./projects/**)` が効くか（雛形は `templates/workspace/claude-settings.template.json`）。③ `base_stale`（`room.py` の frontmatter 更新）が、共有知の基準が古いときに付くか。④ `room start` が写す `ai/ctx/area-README.md` を、部屋の AI が開始時に読めるか。⑤ `room restore` が、`mapping.json` が無い・食い違うときに止まるか。⑥ `SharedPermissionTest` 2 件を Windows で実行して通るか（原因は Windows の `expanduser` が `HOME` でなく `USERPROFILE` を見ること。テストに足して Linux で通った）。⑦ `guides/explain/ai-room-why.md` と `guides/howto/ai-room-setup.md` のレビュー（「草稿（未レビュー）」の注記を外す。`why` は 2026-10-18 にトピックのノートと照らして更新済み。`setup` は未）。⑧ 部屋の AI が実際に `stock` の下書きを書き、先頭に基準コミットと観測日を付けられるか（`ROOM.md` に従うか。ダミーでは人が置いたファイルで確認済み）。共有知の送付のサイズ（1.5MB、120 ファイル、2026-10-14）は `guides/` と `lessons/` が増えたら測り直す。`review` が読む記録（`events` など）の置き場も未確認。20 と 37 は別項目。ユーザーは、10-18 の通しで通っていると見た 2 件（別の `wsl.exe` からのマウント、`ai/out/` のサブディレクトリの `restore`）と、omit した 3 件（部屋専用の SSH 鍵、Zed を開いたままのアンマウント、リポジトリ・remote の dev の案）を外した。設計と決定は `guides/explain/ai-room-why.md`、`docs/decisions.md`（「AI 作業部屋の決定」）、`exmem/lessons/ai-isolated-work-room.md`、仕様は `workflow-kit/room/mask-spec.md` に移した。
38. 改善4（振り返り）のモードの直しの続き。済み: 読後の指摘で手順書を v5 にし（【仮 〜10-26】。目標、活動/成果物の分離、具体は ID、11 → 8 章）、第1回の記録を組み直した（材料は集め直していない）。残り: ① v5 で材料を集め直す実行（同じ入力 10-12〜10-19 か、次週 10-26）を、新しい会話で行い、ユーザーが読んで比べる。② 週次の使い方（前回の目標・軸・施策の引き継ぎ。R-2026-10-19-06。引き継ぎの定義のみ反映）を仕上げる。③ 施策 R-2026-10-19-01〜06 の承認。
37. 実機の通しで気づいた room の改善 4 件に対応する（2026-10-18 `review 消化` でユーザーが「やります」）。①`restore` が、AI が本文に書いた `⟦CUST_nnn⟧` の説明で止まる（AI への指示で防ぐか、`restore` が説明用の記述を許すか）。②新しい Project のたびに Claude Code の信頼の確認が出る。③Zed を `/home/ai` で使うと、履歴が `-home-ai` に残り、どの Project にも属さず `reap` されない。④`close` が、README がひな形のままでも通る。方法は決めていない（実装前に場所・手段・呼び出し元を 3 行で見せる）。
29. Stop フックで、セッションの費用と ID を記録する手順（`notes/stop-hook-record/2026-10-17-procedure.md`、プロジェクトの共有フォルダ）を、Zed を使う PC で実機確認する（端末の `claude -p` と、Zed の1往復。2026-10-17 時点）。確認の後に、キャッシュの間を記録に足す案（`2026-10-18-cache-insights.md` の S3）を決める。
24. 続ける・切るの暫定の数値（約10万トークン、約2万トークン）は、クラウドの実験（2026-10-17。1回ずつ）で考え方が合うと確かめた。「間」は TTL 基準に直した（2026-10-18。`hook-common.md`、`session-handoff.md` の Decisions）。TTL は確認した（2026-10-19、ユーザーの PC。`ephemeral_1h_input_tokens` 24,046・`ephemeral_5m` 0 → 1時間。実測）。新しい会話の土台 B は約 24k トークン（このときの cwd での値。cwd で変わる）で、「約2万未満なら続ける」の例外の数値より大きい。残り: 本物のフック列で3回以上再実験する。例外の数値（約2万）を B に合わせて直すかは、再実験の後に決める。
20. 領域 × r/w 表（`hooks.md`）を使いながら確かめる。部屋の AI が `wrap` の差し替え（コミットを行わない、知識化は `ai/out/stock/` の下書き）と、`ROOM.md` の stock の書き方（frontmatter）に従えるか。`check-hook-outline.ps1` は実行して FAIL なし(2026-10-17)。この項は別セッションに回した(ユーザーの指示)。
15. 振り返りを「定期（改善4。進め方・成果物）」と「突発・なぜなぜ（改善5）」に分けた(2026-10-17。`retrospective-method-2.md` は叩き台)。残り: 改善5 の品質チェック3回(基準は試行の出力 `notes/retrospective-method/2026-10-17-trial-this-thread.md`)、改善4 の「定期」としての使い方(前回の日付から今日まで、前回の軸の引き継ぎ)の反映、ID・検証項目の形の確認。
13. 「振り返りのやり方1」(`methods.md` の改善4、`retrospective-method.md`)を、次の振り返りの依頼から使う(題材 B = 業務の対象でも)。使った回数 1/3（2026-10-19。題材 A の週次）。評価軸の選び方の指針が要るか、各最大3個が適切かを、`records/retrospective-method-record.md` に足す。3回の `review` の後に Must の増減を決める。
12. `user-manual.md` の補正策(2026-10-17、2026-10-18)を、使いながら手順書に反映する。候補（`wrap` の集計は、終了時の1問の廃止で取り下げた）: 削除・統合の提案での役目の列挙、決定の推奨に弱点を添える、手段の依頼での目的の復唱、案の前提の確認、rename・移動の副作用の一覧、commit 前の変更の帰属の分離、見た目の調整の omit 提案、承認への効果・期日・戻し方の添付（項目 30 と合流できる）。施策1（実現方法を任せる依頼で、実装前に場所・手段・呼び出し元を3行で見せる。Principles に入れ済み）は、次にその依頼が出たとき、3行が見せられたか・効いたかを見る。PC1 の会話と 10-15 以降のローカルログからの同じ分析は、`user-thinking-habits.md` の Open Questions。2026-10-18 の分析は、この PC の 09-26〜10-14 だけ。

10. `dev-env` / `dev-test` を、最初の Project で1回使い、置き場の表と完了条件の例が合うかを見る(`dev-deliverable-guide.md` の末尾の節)。使った後に `remote` の type の要否を決める。
8. 「変更のやり方」(`methods.md` の「変更」、`exmem/lessons/change-method.md`)を、次の変更から使う。3回の `review` の後に、Must(基準文書3・変更6)が重すぎないか・足りないかを見て増減を決める。`areas/` `projects/` での適用は決定済み(2026-10-16。置き場は `ai/out/<成果物名>/`、マスク後の語で書く。`decisions.md`)。最初の業務で使って、置き場が合うかを見る。先送り: 新規作成のフックかモード、変更の伝播・軽重・廃止。


## Open Questions

- 場所: 実機の通し（2026-10-18）で気づいた点 / 問題: `restore` の上書きの保護（`final-manifest.json`）は、今回試していない / 案: 次の実機で試す。
- 場所: Stop フックの記録の置き場 / 問題: 既定は `~/claude-records/`。部屋の中だけ `$CLAUDE_PROJECT_DIR/records`（`ai/records/`）にするかが未決 / 案: 実機確認（29）の後に決める。【保留 〜2026-10-25】（2026-10-19 `review 消化` でユーザーが保留。スクリーニング: `ai/records/` の用途とマスクの整合が未確認）。
- 場所: `open-hook.md` の未決の `remote` の type / 問題: WSL から SSH で user 権限のリモート(Docker を含む)を AI が操作する使い方を、`dev` でも使える type にするか。接続の安全(鍵、権限、記録)は `guides/explain/ai-room-why.md` の設計と重なる / 案: 実測の後に決める。【保留 〜2026-11-02】（2026-10-18 `review 消化` でユーザーが保留、期限 11/02。項目 10 の `dev-env` の実使用の後に決める）。
- 場所: `open-hook.md` の未決 / 問題: リポジトリが正の `src`、remote で動くものは、構造が新規のフルスクラッチ前提で、`ai/out/` に clone すると `restore` が止まる / 案: `repos/` に置いたまま、スナップショットと patch で受け渡す(未検証)。
- 場所: `room.py` の `restore_project` / 問題: AI が使えない間に人が `_noai/final/` を直すと、次の AI の終了時の復元で無条件に上書きされる(別の話にする、とユーザー。2026-10-16) / 案: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束、上書き前の警告。【保留 〜2026-11-05】（2026-10-18 `review 消化` でユーザーが保留。`_noai/final/` は最終調整で人が触る想定だが、git 管理下にあるので戻せる。次の実機で `final-manifest.json` の保護を試してから決める）。
- 場所: `token-matrix.md` と `review` の入力 5（重い会話） / 問題: 4観点に、間と先頭の安定が無い。入力 5 は大きい会話を見るだけで、書き直した量が見えない / 案: 第5の観点「温存」を足し、入力 5 を「TTL を超えて空いた後の書き込み量」に変える（Python スクリプト。費用を記録する Stop フックの inbox のメモと一緒に検討）。【保留 〜2026-10-25】（2026-10-19 `review 消化` でユーザーが保留。スクリーニング: 型 B・D・E。入力 5 の今の役目の引き継ぎと基準値 103 の再設定を付け、分割して出し直す）。
