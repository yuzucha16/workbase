# 作業ログ（log）

計画のやり方（`start 計画`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. （済 2026-10-20）取り込み: 3層は 2026-10-20 に通り、試験運用で `workflow-kit/` に取り込んだ。`start-plan.md`、`methods.md` の区分「計画」、`start-hook.md` の `start 計画`、`hooks.md`、`hook-matrix.md`、`exmem/lessons/planning-method.md` ほか（root `docs/decisions.md` の同日）。コミット・push は未了ならユーザーに確認。
2. 品質チェック3回（2週間の実務の題材、見本なし、短い題材）を [[planning-method-record]] に足す。1回目は `private-knowledge`（2026-10-21、計画の質だけ。1週間の題材で、2週の検証はできなかった。実行後の項目は未了）。
2a. （2026-10-21 承認）`start-plan.md` に反映済み: stock-modes の所見6件、works の置き場、上限3つの数え方、規模の測り方。次は、定期的に使う側（`stock-modes` の実使用）のフィードバックをユーザーが書く。
2b. （済 2026-10-21 承認）WBS の第2層は成果物の種類で分ける。中間の記録は、読み手がいれば葉、読み手のいない本当の中間物（テスト、作業用スクリプト）だけ親に含める。`start-plan.md` に反映済み。効果は次の題材で見る。
2c. （2026-10-21 記録、未承認）stock-modes の設計・実装・通し試験を通した、憲章・WBS・マイルストーンへのフィードバック: [[planning-method-feedback-stock-modes-m1]]（削除候補7、粒度5、足りない5、`start-plan.md` への案8件）。`review 消化` で扱う。前回の6件（`stock-modes-6r.md` の末尾）は 2a で反映済み。
3. 振り返りへの入力（計画を基準にする案）は、直下 `docs/log.md` の Open Questions にある。10-20 に保留にした（2026-11-11 まで。品質チェック3回の後に出し直す）。承認した計画の置き場の案（`topics/kit-growth/plans/`）は、このトピックの置き場と合わせて見直す。
4. 試行の題材は、2026-10-21 にトピックへ切り出した: `topics/usage-viz/`（トークン・コスト可視化。実装まで終わった）、`topics/stock-modes/`（`stock` のモード追加。M1 の途中）、`topics/private-knowledge/`（会議録のナレッジ化）。各トピックの状態はそれぞれの `docs/log.md`。

## Open Questions

- （済 2026-10-21）題材の計画の置き場、束ねる条件、小さな題材の規模の測り方は、ユーザーが承認し、`start-plan.md` に反映した。置き場は仮決め 〜10-28（root の `docs/log.md` の期日）。
- 2週・4週の上限（マイルストーン5・9）は使っていない。日付の並びが題材によらず同じで、見本の写しの疑いがある。品質チェック1回目は1週間で検証できなかった。2週間の題材で確かめる。
- 2b の直し（第2層の分け方、葉の数え方）で、葉とファイル数のずれが減るか。次の題材で測る。
