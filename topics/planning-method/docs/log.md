# 作業ログ（log）

計画のやり方（`start 計画`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. （済 2026-10-20）取り込み: 3層は 2026-10-20 に通り、試験運用で `workflow-kit/` に取り込んだ。`start-plan.md`、`methods.md` の区分「計画」、`start-hook.md` の `start 計画`、`hooks.md`、`hook-matrix.md`、`exmem/lessons/planning-method.md` ほか（root `docs/decisions.md` の同日）。コミット・push は未了ならユーザーに確認。
2. PC1 で品質チェック3回（2週間の実務の題材、見本なし、短い題材）を行い、[[planning-method-record]] に足す。
3. 振り返りへの入力（計画を基準にする案）は、直下 `docs/log.md` の Open Questions にある。10-20 に保留にした（2026-11-11 まで。品質チェック3回の後に出し直す）。承認した計画の置き場の案（`topics/kit-growth/plans/`）は、このトピックの置き場と合わせて見直す。
4. 試行の題材（トークン・コスト可視化）は実装まで終わった（2026-10-20。ツールと手順書は直下 `docs/log.md` の状態）。実行後のフィードバックは `records/usage-viz-*.md` の末尾にある。（済 2026-10-20）ユーザーの指示で `workflow-kit/start-plan.md` に反映した（足す候補は欄に足し、省く候補は省いてよい許可にした）。効果は品質チェックで見る。

5. 進行中: stock のモード追加の計画（`records/stock-modes-*.md`）。6R・憲章・WBS・マイルストーンは作成済み（2026-10-20）。M1（設計の確認）は途中: 出力先・モード名・引数なし（「両方」なし）・更新は対象外・`find-knowledge` 対応は不要、までユーザーが決めた（`docs/decisions.md`）。残りの【提案】（`kind` の値、6見出し、`integrate` の変換、`check-inbox` の分岐、権限は変えない）は未確認。見本は `records/explain-inbox-example.md`。その後 M2 で `workflow-kit/` を書き換える（承認が要る）。`room.py` が `kind` をそのまま運ぶかは未確認。
6. 6R へのフィードバック（`records/stock-modes-6r.md` の末尾。`start-plan.md` への案6件）は未承認。`review 消化` で扱う。

## Open Questions

- workbase の題材の計画の置き場（トピックを明示する経路、トピックの要否を含む）。ユーザーの決定（2026-10-20）: 案④の `topics/kit-growth/plans/` と合わせて、`planning-method` の昇格のときに決める。それまではトピックの運用自体が試行で、計画は都度ユーザーに聞く。

- 上限3つを守るために、終わる日の違うマイルストーンを束ねてよい条件が未決（試行の題材では、この1件に限り可と決めた。一般の条件は未決）。ただし試行では、実行が1セッションで終わり、マイルストーンの日付は意味が薄かった（束ねるかより、ゲートの置き方の論点）。
- 2週・4週の上限（マイルストーン5・9）は使っていない。日付の並びが題材によらず同じで、見本の写しの疑いがある。
- 小さな題材（AI が1セッションで作る道具）で、欄と葉の数をどう減らすか。試行では、憲章の体制の欄、WBS の葉の多くが、実態と合わなかった。
