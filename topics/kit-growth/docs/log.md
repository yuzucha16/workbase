# kit-growth: 現在状態

更新: 2026-10-16（wrap: open の Project の構造を ai/ と _noai/ の対応に書き直すまで。close の整理は決定のみ）

## 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`、`improvements.md` は凍結。自動採用は 2026-10-15 に畳んだ。
- cwd はリポジトリのトップだけ（`4997f7a`）。上の階層からの「続き」は AI が読みに行き、`wrap` は作業した単位の `docs/` を既定にする。各フックの cwd の期待は `hook-matrix.md` の 3 行に記録した（`53c3771`、確認日 2026-10-16）。
- `review` は 3 リポジトリ（works の基準の「点検の対象」）の未統合メモ・トピック・機密を見る（`302fccb` `9b19540`）。終了時の 1 問は起動した単位に記録する。
- トークン消費は `token-matrix.md`（4観点）で自己採点する。基準値は合計 103。`again` `gap` の記録は廃止（`139091c`）。
- `review 消化`、`start 解決` / `start 改善`、`methods.md` を足した（`f395e34` `8242e1c` `28202d7`）。`start` のインタビューは残した。
- `wrap` を軽くし（`9fbf4e4`）、フックの重さの基準を `hook-matrix.md` に固定した（`dc2931d`）。3 リポジトリの規則を揃えた。経緯は `log-history.md`。
- init の項目 5 に `resources_p/`（PC ローカルの resources。ignore、検索の対象に含める）を足した（`6074995`）。works には反映済み（works の `2c9ffea`。ローカルのみ）。残り: なし。範囲外の案は `decisions.md` の同日の項（別リポジトリでの管理）。

- 「変更のやり方」(Must / Want。`methods.md` の「変更」、`change-method`)を足した(`266c361`)。中間成果物は「基準文書」に改称し、`areas/` `projects/` への適用を決めた(`40d8aa6`。置き場は `ai/out/<成果物名>/`、マスク後の語で書く)。
- `open-hook.md` の「Project の構造」を、`ai/` と `_noai/` への対応に書き直した(`7b2c515`。type 別の置き場、基準文書の置き場)。`_noai/` は残す。`close` はトピック専用に畳む方針を決めた(未実施。Next Actions 9)。
- init に `init 更新`（雛形の変更をワークスペースに反映。基点つきの3者マージ、`Template-Rev` トレーラー）を足し、ワークスペースの雛形に `README.md` を足した(`316840f` `8b74187`)。

## Next Actions

9. `open` / `close` の整理の続き(ユーザーの方針、2026-10-16。`decisions.md`)。① `close-hook.md` を削除し、`topics/AGENTS.md` に「トピックを終わらせるとき」の節(`decisions.md` の【汎用】が反映済みか見る、ディレクトリと `topics-index.md` の行を削除、`[[リンク]]` の grep、記録は `wrap`)を足す。`hooks.md` の表と連鎖、`workflow-kit/README.md`、`review-hook.md` の参照を直す。② `open-hook.md` を構造と判断部分だけに縮める(ひな形・Area の一覧・コミットは `room open` の責務)。③ `room close` が要る `ai/out/close.md` の書き方の置き場を、`room-context.md` の `close` の行に移す。①〜③は一緒に差分で出して承認を取る。
8. 「変更のやり方」(`methods.md` の「変更」、`exmem/lessons/change-method.md`)を、次の変更から使う。3回の `review` の後に、Must(基準文書3・変更6)が重すぎないか・足りないかを見て増減を決める。`areas/` `projects/` での適用は決定済み(2026-10-16。置き場は `ai/out/<成果物名>/`、マスク後の語で書く。`decisions.md`)。最初の業務で使って、置き場が合うかを見る。先送り: 新規作成のフックかモード、変更の伝播・軽重・廃止。

7. `init 更新`（`init-update.md`）を PC1 と PC2 で一度ずつ使い（初回は README の追加も案に出るはず）、衝突の出方と、基点なし（初回）の2者の差分が読めるかを見る。works の既存の `AGENTS.md` は雛形の古い版から作られているので、初回は基点なしになる見込み。

6. 次の `review` で、重さの基準と比べる初回と、各フックの cwd の期待の点検（`hook-matrix.md` の cwd の3行。確認日 2026-10-16）の初回を実施する。3回後に N（字数 +20%、項目数 +2）を決め直す。`wrap` の読み込み字数（`docs-rules.md` の節だけ読む効果）も測り直す。

0. 入力 8 は 2026-10-16 に初回を実施済み。deny 設定は dotfiles に入れ、凍結の対として 3 つの `AGENTS.md` の禁止コマンドの列挙を畳んだ（ユーザーの決定）。残るギャップは、`pre-push`（works の 11-08 の判定の項目⑧。git 周りは後日まとめて見直す）、works の `docs/log.md` の超過、dotfiles の `docs/setup/` の案（`topics/dotfiles-boundary/`）との置き場の整合。規則を足したので、凍結の対（畳むもの）は機密の項で足りたが、入力 8 の分は未対（次の `review` で畳む候補を挙げる）。

1. PC1 の印象を `inbox.md` に入れ始める（モバイル。随時）。
2. `start` のモード（確定型・探索型）を次の2〜3セッションで試し、`review` で `goal_change` を見る（`again`・`gap` は 2026-10-15 に廃止）（improvement-methods の close で受け継いだ。詳細は `exmem/lessons/session-goal-modes.md`）。
3. `token-matrix.md` の初回の採点し直しは済んだ（`70b8e22` で 103、下がった列なし）。入力「重い会話」は、会話履歴の集計がある端末の `review` で見る。見送った2件（切る目安の数値、`lessons/` の字数の目安）は、その結果を見て決める。
4. topic-workflow の kit への取り込み（docs-rules の「トピック」の節）が済んだら、`topics/` の型の記述をそちらへ寄せる。

5. `start 解決` / `start 改善` と `review 消化` を実際に使い、選ぶ基準・「10件超」の目安が合うか見る。使われなければ、`start` のインタビューを畳むか、`start` の「作業の種類の差分」を畳むかを、次の `review` で決める（凍結の対）。`again` `gap` 廃止の原因（進め方のサンプルの影響）は未分析。

## Open Questions

- 場所: `init-update.md`（7.9k 字） / 問題: 同じ任意の章 `init-workspace.md`（2.6k）の約3倍で、`hook-matrix.md` の重さの基準でも大きい / 案: 使ってみて、手順 1・2 の確認コマンドを `init-update.md` から外せるか見る（`review` で比べる）。
- 場所: `open-hook.md` の未決 / 問題: リポジトリが正の `src`、remote で動くものは、構造が新規のフルスクラッチ前提で、`ai/out/` に clone すると `restore` が止まる / 案: `repos/` に置いたまま、スナップショットと patch で受け渡す(未検証)。
- 場所: `room.py` の `restore_project` / 問題: AI が使えない間に人が `_noai/final/` を直すと、次の AI の終了時の復元で無条件に上書きされる(別の話にする、とユーザー。2026-10-16) / 案: 正本の宣言、`raw/` → `mask` → `ai/in/` の戻り方の約束、上書き前の警告。
- Area の担い手: topic-workflow の Q3 の会話で、AI は「kit の改善という Area は kit 本体・`improvements.md`・`review` が担う」と述べたが、本トピックの決定は「トピックが担う」。後者（ユーザーの合意）を採った。
