# kit-growth: 現在状態

更新: 2026-10-16（wrap: 「調査のやり方1」と start 調査を足し、新しい会話で4回、品質を確かめた。確定版の置き場は guides/explain）

## 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`、`improvements.md` は凍結。自動採用は 2026-10-15 に畳んだ。
- cwd はリポジトリのトップだけ（`4997f7a`）。上の階層からの「続き」は AI が読みに行き、`wrap` は作業した単位の `docs/` を既定にする。各フックの cwd の期待は `hook-matrix.md` の 3 行に記録した（`53c3771`、確認日 2026-10-16）。
- `review` は 3 リポジトリ（works の基準の「点検の対象」）の未統合メモ・トピック・機密を見る（`302fccb` `9b19540`）。終了時の 1 問は起動した単位に記録する。
- トークン消費は `token-matrix.md`（4観点）で自己採点する。基準値は合計 103。`again` `gap` の記録は廃止（`139091c`）。
- `review 消化`、`start 解決` / `start 改善`、`methods.md` を足した（`f395e34` `8242e1c` `28202d7`）。`start` のインタビューは残した。
- `wrap` を軽くし（`9fbf4e4`）、フックの重さの基準を `hook-matrix.md` に固定した（`dc2931d`）。3 リポジトリの規則を揃えた。経緯は `log-history.md`。
- init の項目 5 に `resources_p/`（PC ローカルの resources。ignore、検索の対象に含める）を足した（`6074995`）。works には反映済み（works の `2c9ffea`。ローカルのみ）。残り: なし。範囲外の案は `decisions.md` の同日の項（別リポジトリでの管理）。

- 「変更のやり方」(Must / Want。`methods.md` の「変更」、`change-method`)を足した(`266c361`)。中間成果物は「基準文書」に改称し、`areas/` `projects/` への適用を決めた(`40d8aa6`。置き場は `ai/out/<成果物名>/`、マスク後の語で書く)。
- `open-hook.md` の「Project の構造」を、`ai/` と `_noai/` への対応に書き直した(`7b2c515`。type 別の置き場、基準文書の置き場)。`_noai/` は残す。`close-hook.md` を削除し、トピックの終了は `topics/AGENTS.md` の節に、Project の終了の判断(`ai/out/close.md`)は `room-context.md` に移し、`open-hook.md` を判断部分に縮めた(`c86b4d6`)。
- init に `init 更新`（雛形の変更をワークスペースに反映。基点つきの3者マージ、`Template-Rev` トレーラー）を足し、ワークスペースの雛形に `README.md` を足した(`316840f` `8b74187`)。
- room の type に `dev-env`（主にテスト環境）と `dev-test` を足した(`ccfe968`)。`dev` の子でなく独立の type。`dev-env` は「環境の置き場」を立ち上げで聞く。`remote` という type の案は未決。
- 「調査のやり方1」(Must / Want。`methods.md` の「調査」、`research-method`、`start 調査`)を足した(`55438b6`)。新しい会話で4回実行して基準と比べ、手順書を直した(`fa18e20` `fa7531c` `9297023` `f628ab9` `608be79`)。確定版の置き場は `guides/explain/<主題>.md`(`a78ef3b`)。
- topic-workflow を取り込んで close した。トピックの型の正本は `topics/AGENTS.md`（docs-rules に節は足さない）。`wrap` の依頼文は「<単位> の続き」の1行。

## Next Actions

11. 「調査のやり方1」(`methods.md` の「調査」、`exmem/lessons/research-method.md`、`start 調査`)を、次の調査から使う。3回の `review` の後に、Must(仕込み3・プロセス6)の増減を決める。仕込みとプロセスの境目(4を想定読者として仕込みに移した案)は承認済み。pwsh のある PC で `tools/check-hook-outline.ps1` を実行する。先送り: 読者が変わる業務の調査(`research` type)、値の更新。確定版の置き場は `guides/explain/<主題>.md`(決定済み)。最初の確定(Claude スキルの成果物を移すか)は未定。品質チェック(新しい会話で3回実行し、基準と比較)は実施済み。3回目の直しは未検証で、`start-hook.md` は +17%(+20% の手前)なので、次に足すときは畳む。

10. `dev-env` / `dev-test` を、最初の Project で1回使い、置き場の表と完了条件の例が合うかを見る(`dev-deliverable-guide.md` の末尾の節)。使った後に `remote` の type の要否を決める。
9. `open` / `close` の整理は実施済み(`c86b4d6`)。次に `room close` を実機で通すとき、`room-context.md` の `close.md` の書き方で足りるかを見る。`open-hook.md` の基準を縮小後の 4,687 字に下げたので(`hook-matrix.md`)、次の `review` で比べる。
8. 「変更のやり方」(`methods.md` の「変更」、`exmem/lessons/change-method.md`)を、次の変更から使う。3回の `review` の後に、Must(基準文書3・変更6)が重すぎないか・足りないかを見て増減を決める。`areas/` `projects/` での適用は決定済み(2026-10-16。置き場は `ai/out/<成果物名>/`、マスク後の語で書く。`decisions.md`)。最初の業務で使って、置き場が合うかを見る。先送り: 新規作成のフックかモード、変更の伝播・軽重・廃止。

7. `init 更新`（`init-update.md`）を PC1 と PC2 で一度ずつ使い（初回は README の追加も案に出るはず）、衝突の出方と、基点なし（初回）の2者の差分が読めるかを見る。works の既存の `AGENTS.md` は雛形の古い版から作られているので、初回は基点なしになる見込み。

6. 次の `review` で、重さの基準と比べる初回と、各フックの cwd の期待の点検（`hook-matrix.md` の cwd の3行。確認日 2026-10-16）の初回を実施する。3回後に N（字数 +20%、項目数 +2）を決め直す。`wrap` の読み込み字数（`docs-rules.md` の節だけ読む効果）も測り直す。


1. PC1 の印象を `inbox.md` に入れ始める（モバイル。随時）。
3. `token-matrix.md` の初回の採点し直しは済んだ（`70b8e22` で 103、下がった列なし）。入力「重い会話」は、会話履歴の集計がある端末の `review` で見る。見送った2件（切る目安の数値、`lessons/` の字数の目安）は、その結果を見て決める。

## Open Questions

- 場所: `open-hook.md` の未決の `remote` の type / 問題: WSL から SSH で user 権限のリモート(Docker を含む)を AI が操作する使い方を、`dev` でも使える type にするか。接続の安全(鍵、権限、記録)は `topics/ai-workspace-boundary/` の設計と重なる / 案: 実測の後に決める。
- 場所: `init-update.md`（7.9k 字） / 問題: 同じ任意の章 `init-workspace.md`（2.6k）の約3倍で、`hook-matrix.md` の重さの基準でも大きい / 案: 使ってみて、手順 1・2 の確認コマンドを `init-update.md` から外せるか見る（`review` で比べる）。
- 場所: `open-hook.md` の未決 / 問題: リポジトリが正の `src`、remote で動くものは、構造が新規のフルスクラッチ前提で、`ai/out/` に clone すると `restore` が止まる / 案: `repos/` に置いたまま、スナップショットと patch で受け渡す(未検証)。
- 場所: `room.py` の `restore_project` / 問題: AI が使えない間に人が `_noai/final/` を直すと、次の AI の終了時の復元で無条件に上書きされる(別の話にする、とユーザー。2026-10-16) / 案: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束、上書き前の警告。
- 場所: `review-hook.md` の消化モード（60行目）/ 問題: 対象が「呼び出し元の `docs/log.md`」で、「<名前> の続き」で読みに行った単位を含むか書かれていない（`wrap` は明記済み）。「続き」なしで言うとリポジトリ直下の `docs/log.md` と読まれうる / 案: 対象を「このセッションで作業した単位の `docs/log.md`」と1行で明記する（`review 消化` で承認を取る）。
- Area の担い手: topic-workflow の Q3 の会話で、AI は「kit の改善という Area は kit 本体・`improvements.md`・`review` が担う」と述べたが、本トピックの決定は「トピックが担う」。後者（ユーザーの合意）を採った。
- 場所: `method-creation.md` / 問題: 5〜12 の AI の追加は叩き台で、ユーザー未確認 / 案: 次にやり方を作るときに使い、足りない点・重い点を記録する
- 場所: `start-hook.md` / 問題: 12,870 字で基準の +19%。次に足すと +20% を超える / 案: 次に足すとき、引数つきモード(解決・改善・調査)の共通の手順を1つの表にまとめて畳む
- 場所: 調査のやり方1の品質チェック / 問題: 4回目の効果が、具体例の条件の言い切りと3回目の直しで分けられず、実行も1回 / 案: 次の調査で、条件を変えて1回ずつ比べる(`review` の点検 7 に載せる)
