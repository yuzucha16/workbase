# kit-growth: 現在状態

更新: 2026-10-16

## 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`（inbox の未選別と、動いているトピックを見る）、`improvements.md` は凍結。
- 自動採用（`wrap-hook.md` の節）は、2026-10-15 に畳んだ（判定を前倒し）。
- cwd（起動する場所）を明文化した（`4997f7a`）: `AGENTS.md` の単位で起動、上の階層からの「続き」は AI が読みに行く、読む順番は 窓口 → `log.md`、部屋は例外、`wrap` は作業した単位の `docs/` を既定に。
- トークン節約の対応を入れた。`review` が `token-matrix.md`（4観点）で自己採点する。基準値は合計 103（`6bd1a2a`、`70b8e22`）。
- `again` と `gap` の記録を廃止した（2026-10-16、`139091c`）。`goal_change` は残した。topic-workflow の kit 取り込みの時機は要再判断（`topics/topic-workflow/topic-workflow-next-steps.md` の5）。
- `wrap` の記録先は workbase の `AGENTS.md` の「wrap の記録先」に定めた（トピック外の kit 等の変更は kit-growth の `docs/`、遠回りは `inbox.md`）。
- 3 リポジトリの規則を揃えた（2026-10-16。`2156d92` `2a35149` `3cdeeb1` `286d714`）。経緯は `log-history.md`。
- `review` に消化モード（`review 消化`）、`start` に引数つきモード（`start 解決` / `start 改善`）を足した（2026-10-16 ユーザーの承認。`f395e34` `8242e1c` `c0a46cb`）。やり方の要点は `workflow-kit/methods.md`、詳細は `exmem/lessons/`（`28202d7`）。`start` のインタビューは残した。

- `wrap` を軽くした（`9fbf4e4`）。フックの重さの基準（字数・手順・報告の項目数）を `hook-matrix.md` に固定し、`review` が比べる（`da81042`、`dc2931d`）。

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
