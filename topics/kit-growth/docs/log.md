# kit-growth: 現在状態

更新: 2026-10-17（初回の review を実施した。`846c3d7`）

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
- フックの報告の型を、共通の項目（最初に「ユーザーに求めること」「コミット」、最後に「次にやること」）と固有の項目に分けた。改善案は報告に載せず Open Questions に残す。`integrate` も push する。続ける・切るの暫定の数値は、間5分、約10万トークン、約2万トークン。正本は `hook-common.md` の「報告の型」「改善」、経緯は `decisions.md`（2026-10-17 の5項目）。
- `review` の前回の日付は `[review]` コミットから取る（`review-hook.md` の手順「コミットする」。初回は `846c3d7`）。`open`（2,924 字）・`start`（4,827 字）を、`project-structure.md` と `start-work-types.md` への分割で字数の目安内にした。点検スクリプトは FAIL なし。
- `pwsh` が無い環境用に、`tools/check_inbox.py` `find_knowledge.py` を足した。works を指す語は「works」に統一した（kit、ルート、`guides/`、`exmem/lessons/` の現在形の記述。`topics/` のノートは未）。部屋へ送る共有知から、`room/` のコード・テストを外した（`README.md` は送る）。施策1を `user-manual.md` に足した。
- 2026-10-17 の作業は `807dd29` まで push 済み（`main`）。決定は `decisions.md` の同日の 4 項、経緯は `log-history.md`。

## Next Actions

24. 続ける・切るの暫定の数値（間5分、約10万トークン、約2万トークン）が実測に合うか、`review` の入力 5（重い会話）で見る。数値はユーザーが承認済み（2026-10-17。暫定）。`exmem/inbox/` に未統合のメモが1件（`2026-10-17-session-cut-cache-thresholds.md`）。
26. WSL の部屋で `room start` を実行し、`~/shared/workflow-kit/room/` に `README.md` だけが入ることを確かめる(2026-10-17 に `room.py` を変更。この環境では単体テストのみ。別セッション)。
25. 移した先（`project-structure.md`、`start-work-types.md`）を、次に `open` / `start` で type を決める・項目を埋めるときに読み忘れないか見る。
23. `[review]` のコミットが作られた（`846c3d7`）。次の `start` と `wrap` が、日付を取れて7日の判定ができるか確かめる。`wrap` の報告で、`review` を7日後に勧める。`review` の次回の目途は 2026-10-24。

20. 領域 × r/w 表（`hooks.md`）を使いながら確かめる。部屋の AI が `wrap` の差し替え（コミットを行わない、知識化は `ai/out/stock/` の下書き）と、`ROOM.md` の stock の書き方（frontmatter）に従えるか。`check-hook-outline.ps1` は実行して FAIL なし(2026-10-17)。この項は別セッションに回した(ユーザーの指示)。
18. 用語は決まった(2026-10-17): 「領域」、works を指す語は「works」。置き換えは、kit、ルート、`guides/`、`exmem/lessons/` の現在形の記述（`ai-isolated-work-room.md` `para-operations.md` など 5 ファイル）を済ませた。残り: `topics/ai-workspace-boundary/` のノート（約 80 件。設計時点の記述が多い）、`exmem/lessons/` の Obsidian の意味や日付つきの事実（旧パス `C:\vault\notes` など。これは置き換えない）、`room.py` の画面メッセージ、`improvements.md`（凍結）。次に `init 更新` を実行すると、雛形の語が works に反映される。ノートは、そのトピックを使うときに直す（まとめて直さない）。
15. 振り返りのやり方を、複数のパターンに分け、パターンごとに進め方と出力 Markdown の章立てを別物にする(別セッションで)。ユーザーの業務はリーダーの立ち位置で、定期の振り返りと、突発的なトラブルの振り返り(なぜなぜ分析)を求められる。出力 Markdown は基準文書として扱う(2026-10-17 ユーザーの指示)。材料: 振り返り1を失敗の件に当てはめた試行で、軸の先決めが合わなかった(核の「分担」が軸の外から出た)。分析の案(兄弟として置く案 B。2026-10-17 承認)は、プロジェクトの `notes/retrospective-method/` の `2026-10-17-one-mode-or-two.md`、試行の出力は `2026-10-17-trial-this-thread.md`、cwd の件の仕込みは `2026-10-17-cwd-case-prep.md`。パターンの候補(AI の案): 定期、突発の失敗(なぜなぜ)、進め方・成果物(振り返り1)。決めること: 呼び出しは `start 改善` の1問に入れるか、パターンごとの題材の選び方と聞き取りの型、基準文書として要る項目(ID、検証項目)。
14. 施策1（実現方法を任せる依頼で、実装前に場所・手段・呼び出し元を3行で見せる）を取扱説明書（`user-manual.md` の Principles）に入れた(2026-10-17)。次に実現方法を任せる依頼が出たとき、3行が見せられたか、効いたかを見る。
13. 「振り返りのやり方1」(`methods.md` の改善4、`retrospective-method.md`)を、次の振り返りの依頼から使う(題材 B = 業務の対象でも)。評価軸の選び方の指針が要るか、各最大3個が適切かを、`records/retrospective-method-record.md` に足す。3回の `review` の後に Must の増減を決める。
12. `user-manual.md` の補正策(2026-10-17)を、使いながら手順書に反映する。候補（`wrap` の集計は、終了時の1問の廃止で取り下げた）: 削除・統合の提案での役目の列挙、決定の推奨に弱点を添える。PC1・PC2 の会話からの同じ分析は、`user-thinking-habits.md` の Open Questions。
11. 「調査のやり方1」「調査のやり方2」(`methods.md` の「調査」、`exmem/lessons/research-method.md` / `research-method-2.md`、`start 調査`)を、次の調査・手順書から使う。調査2は事例が SSH 鍵の1つだけで、実機も未検証。3回の `review` の後に、Must(仕込み3・プロセス6)の増減を決める。仕込みとプロセスの境目(4を想定読者として仕込みに移した案)は承認済み。先送り: 読者が変わる業務の調査(`research` type)、値の更新。確定版の置き場は `guides/explain/<主題>.md`(決定済み)。最初の確定(Claude スキルの成果物を移すか)は未定。品質チェック(新しい会話で3回実行し、基準と比較)は実施済み。3回目の直しは未検証で、`start-hook.md` は +17%(+20% の手前)なので、次に足すときは畳む。

10. `dev-env` / `dev-test` を、最初の Project で1回使い、置き場の表と完了条件の例が合うかを見る(`dev-deliverable-guide.md` の末尾の節)。使った後に `remote` の type の要否を決める。
9. `open` / `close` の整理は実施済み(`c86b4d6`)。次に `room close` を実機で通すとき、`room-context.md` の `close.md` の書き方で足りるかを見る。`open-hook.md` の基準を縮小後の 4,687 字に下げたので(`hook-matrix.md`)、次の `review` で比べる。
8. 「変更のやり方」(`methods.md` の「変更」、`exmem/lessons/change-method.md`)を、次の変更から使う。3回の `review` の後に、Must(基準文書3・変更6)が重すぎないか・足りないかを見て増減を決める。`areas/` `projects/` での適用は決定済み(2026-10-16。置き場は `ai/out/<成果物名>/`、マスク後の語で書く。`decisions.md`)。最初の業務で使って、置き場が合うかを見る。先送り: 新規作成のフックかモード、変更の伝播・軽重・廃止。

7. `init 更新`（`init-update.md`）を PC1 と PC2 で一度ずつ使い（初回は README の追加も案に出るはず）、衝突の出方と、基点なし（初回）の2者の差分が読めるかを見る。works の既存の `AGENTS.md` は雛形の古い版から作られているので、初回は基点なしになる見込み。

6. 初回の `review` は済んだ（2026-10-17。重さの基準は +20% 以上が `hooks.md` と `hook-common.md` のみ、基準を更新）。次の `review` で、入力 7（変更・調査・振り返りのやり方の Must）の点検と、入力 8（3 リポジトリの基準。まだ無い）の作成と、reviews の記録先の決定を行う。元の項目: 重さの基準と比べる初回と、各フックの領域の権限の期待の点検（`hook-matrix.md` の1行。確認日 2026-10-17。旧: cwd の3行）の初回を実施する。3回後に N（字数 +20%、項目数 +2）を決め直す。`wrap` の読み込み字数（`docs-rules.md` の節だけ読む効果）も測り直す。


1. PC1 の印象を `inbox.md` に入れ始める（モバイル。随時）。
3. `token-matrix.md` の初回の採点し直しは済んだ（`70b8e22` で 103、下がった列なし）。入力「重い会話」は、会話履歴の集計がある端末の `review` で見る。見送った2件（切る目安の数値、`lessons/` の字数の目安）は、その結果を見て決める。

## Open Questions

- 場所: `open-hook.md` の未決の `remote` の type / 問題: WSL から SSH で user 権限のリモート(Docker を含む)を AI が操作する使い方を、`dev` でも使える type にするか。接続の安全(鍵、権限、記録)は `topics/ai-workspace-boundary/` の設計と重なる / 案: 実測の後に決める。
- 場所: `init-update.md`（7.9k 字） / 問題: 同じ任意の章 `init-workspace.md`（2.6k）の約3倍で、`hook-matrix.md` の重さの基準でも大きい / 案: 使ってみて、手順 1・2 の確認コマンドを `init-update.md` から外せるか見る（`review` で比べる）。
- 場所: `open-hook.md` の未決 / 問題: リポジトリが正の `src`、remote で動くものは、構造が新規のフルスクラッチ前提で、`ai/out/` に clone すると `restore` が止まる / 案: `repos/` に置いたまま、スナップショットと patch で受け渡す(未検証)。
- 場所: `room.py` の `restore_project` / 問題: AI が使えない間に人が `_noai/final/` を直すと、次の AI の終了時の復元で無条件に上書きされる(別の話にする、とユーザー。2026-10-16) / 案: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束、上書き前の警告。
