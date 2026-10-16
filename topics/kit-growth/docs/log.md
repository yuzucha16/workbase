# kit-growth: 現在状態

更新: 2026-10-16

## 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`、`improvements.md` は凍結。自動採用は 2026-10-15 に畳んだ。
- cwd はリポジトリのトップだけ（`4997f7a`）。上の階層からの「続き」は AI が読みに行き、`wrap` は作業した単位の `docs/` を既定にする。各フックの cwd の期待は `hook-matrix.md` の 3 行に記録した（`53c3771`、確認日 2026-10-16）。
- `review` は 3 リポジトリ（works の基準の「点検の対象」）の未統合メモ・トピック・機密を見る（`302fccb` `9b19540`）。終了時の 1 問は起動した単位に記録する。
- トークン消費は `token-matrix.md`（4観点）で自己採点する。基準値は合計 103。`again` `gap` の記録は廃止（`139091c`）。
- `review 消化`、`start 解決` / `start 改善`、`methods.md` を足した（`f395e34` `8242e1c` `28202d7`）。`start` のインタビューは残した。
- `wrap` を軽くし（`9fbf4e4`）、フックの重さの基準を `hook-matrix.md` に固定した（`dc2931d`）。3 リポジトリの規則を揃えた。経緯は `log-history.md`。
- init の項目 5 に `resources_p/`（PC ローカルの resources。ignore、検索の対象に含める）を足した（`6074995`）。works には反映済み（works の `2c9ffea`。ローカルのみ）。残り: なし。範囲外の案は `decisions.md` の同日の項（別リポジトリでの管理）。

## Next Actions

6. 次の `review` で、重さの基準と比べる初回と、各フックの cwd の期待の点検（`hook-matrix.md` の cwd の3行。確認日 2026-10-16）の初回を実施する。3回後に N（字数 +20%、項目数 +2）を決め直す。`wrap` の読み込み字数（`docs-rules.md` の節だけ読む効果）も測り直す。

0. 入力 8 は 2026-10-16 に初回を実施済み。deny 設定は dotfiles に入れ、凍結の対として 3 つの `AGENTS.md` の禁止コマンドの列挙を畳んだ（ユーザーの決定）。残るギャップは、`pre-push`（works の 11-08 の判定の項目⑧。git 周りは後日まとめて見直す）、works の `docs/log.md` の超過、dotfiles の `docs/setup/` の案（`topics/dotfiles-boundary/`）との置き場の整合。規則を足したので、凍結の対（畳むもの）は機密の項で足りたが、入力 8 の分は未対（次の `review` で畳む候補を挙げる）。

1. PC1 の印象を `inbox.md` に入れ始める（モバイル。随時）。
2. `start` のモード（確定型・探索型）を次の2〜3セッションで試し、`review` で `goal_change` を見る（`again`・`gap` は 2026-10-15 に廃止）（improvement-methods の close で受け継いだ。詳細は `exmem/lessons/session-goal-modes.md`）。
3. `token-matrix.md` の初回の採点し直しは済んだ（`70b8e22` で 103、下がった列なし）。入力「重い会話」は、会話履歴の集計がある端末の `review` で見る。見送った2件（切る目安の数値、`lessons/` の字数の目安）は、その結果を見て決める。
4. topic-workflow の kit への取り込み（docs-rules の「トピック」の節）が済んだら、`topics/` の型の記述をそちらへ寄せる。

5. `start 解決` / `start 改善` と `review 消化` を実際に使い、選ぶ基準・「10件超」の目安が合うか見る。使われなければ、`start` のインタビューを畳むか、`start` の「作業の種類の差分」を畳むかを、次の `review` で決める（凍結の対）。`again` `gap` 廃止の原因（進め方のサンプルの影響）は未分析。

## Open Questions

- Area の担い手: topic-workflow の Q3 の会話で、AI は「kit の改善という Area は kit 本体・`improvements.md`・`review` が担う」と述べたが、本トピックの決定は「トピックが担う」。後者（ユーザーの合意）を採った。
