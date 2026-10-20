# 作業ログ（log）

計画のやり方（`start 計画`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. （済 2026-10-20）取り込み: 3層は 2026-10-20 に通り、試験運用で `workflow-kit/` に取り込んだ。`start-plan.md`、`methods.md` の区分「計画」、`start-hook.md` の `start 計画`、`hooks.md`、`hook-matrix.md`、`exmem/lessons/planning-method.md` ほか（root `docs/decisions.md` の同日）。コミット・push は未了ならユーザーに確認。
2. PC1 で品質チェック3回（2週間の実務の題材、見本なし、短い題材）を行い、[[planning-method-record]] に足す。
3. 振り返りへの入力（計画を基準にする案）は、直下 `docs/log.md` の Open Questions にある。10-20 に保留にした（2026-11-11 まで。品質チェック3回の後に出し直す）。承認した計画の置き場の案（`topics/kit-growth/plans/`）は、このトピックの置き場と合わせて見直す。
4. 試行の題材は、2026-10-21 にトピックへ切り出した: `topics/usage-viz/`（トークン・コスト可視化。実装まで終わった）、`topics/stock-modes/`（`stock` のモード追加。M1 の途中）、`topics/private-knowledge/`（会議録のナレッジ化）。各トピックの状態はそれぞれの `docs/log.md`。

## Open Questions

- workbase の題材の計画の置き場（トピックを明示する経路、トピックの要否を含む）。ユーザーの決定（2026-10-20）: 案④の `topics/kit-growth/plans/` と合わせて、`planning-method` の昇格のときに決める。2026-10-21 に、各題材の計画は題材のトピックの `records/` に置くことにした（`records/` は2か所: 測ったことは `kit-growth/records/`、各トピックの出力はそのトピック。`topics/private-knowledge/docs/decisions.md`）。案④（承認した計画を `kit-growth/plans/` に置く）は保留のまま。

- 上限3つを守るために、終わる日の違うマイルストーンを束ねてよい条件が未決（試行の題材では、この1件に限り可と決めた。一般の条件は未決）。ただし試行では、実行が1セッションで終わり、マイルストーンの日付は意味が薄かった（束ねるかより、ゲートの置き方の論点）。
- 2週・4週の上限（マイルストーン5・9）は使っていない。日付の並びが題材によらず同じで、見本の写しの疑いがある。
- 小さな題材（AI が1セッションで作る道具）で、欄と葉の数をどう減らすか。試行では、憲章の体制の欄、WBS の葉の多くが、実態と合わなかった。
