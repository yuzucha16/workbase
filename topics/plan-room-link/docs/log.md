# 作業ログ（log）

計画と部屋の紐付け（`start 計画` の出力と、`room init` / `room open` が作る README の関連付け）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

名前の注記（2026-10-24）: フック `start` は `brief` に改名し（`brief 計画`、手順は `brief-plan.md`）、`init` / `open` のフックは廃止された（`room mkworks`、`room open` に一本化。`c771c01`）。このトピックの古い記述の `start 計画` `start-plan.md` `open-hook.md` は、その旧名（読み替える。新しい仕様が回りだしたら消す）。

案 D（雛形に固定のポインタ1行）で実装済み（`9b4db50`）。計画一式（6R・憲章・WBS・マイルストーン・作り方のメモ）は `records/` にある（後追いの計画。ユーザーが後で、後追いの 6R などと比較・分析する予定）。

## Next Actions

1. 【起票 10-21】`exmem/lessons/planning-method.md` に、計画の置き場の決定（案 D、実名なし、Project の `ai/in/plan/`）を足す（WBS 2.1。`stock` か `integrate` の流れで。M2、10-22）。
2. 【起票 10-21】実機確認（WBS 3.1）: 次に `room open` した Project の README に「計画:」の行があるかを見て、結果を `log.md` に1行書く。
3. 【起票 10-21】トピックを閉じるかの判断（M3、10-28）: `topics/AGENTS.md` の「トピックを終わらせるとき」の手順 0〜4（`records/` は移さず削除。ただし、ユーザーが後追いの比較に使うので、閉じる前に必要か確認する）。

## Open Questions

- 相談の型（事実→論点→叩き台→確認）の仮決めは5回まで。使った回: 4（論点 1〜3、4〜6、`review 消化` での代替案の比較）。5回目で判断する（`decisions.md` の同日の項。締めとケア9項目を足した）。
- `records/` の計画一式は、閉じるときに削除する決まり（`topics/AGENTS.md` の 1b）と、ユーザーの比較の予定が食い違う。閉じる前に、残す場所を決める。
