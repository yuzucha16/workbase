# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-01 | 定例 | weekly の振り返り（7日周期、日曜。材料は `topics/kit-growth/records/`）。仮決めの期限切れを数える。v7 の検証もここで | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める | ユーザー（AI が実行） |
| 2026-11-09 | 単発 | 振り返りの仮決め3件（字数の数え方、v6、v7）をまとめて判断。規模をもっと縮められるかも決める | ユーザー |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断 | ユーザー |

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。`mkworks` などの新機能は単体テストまで（`room/README.md`）。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`topics/md-link-graph/`）。

## Next Actions

1. 【起票 10-25】整合の基準のギャップ 8: works と dotfiles の履歴にユーザー名入りのパス（`docs/alignment-baseline.md`）。
2. 【起票 10-25】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（同上）。未決は `release` の束ね先。
4. 【起票 10-20、10-26 に 11-08 まで延長】ルールが見つかりにくい構造（`topics/md-link-graph/`。完了条件は満たした。引き当て率の初回 11-08 の後に、閉じるかを聞く）。
5. 【起票 10-25】期限のあるナレッジの置き場 `logbook/`（`topics/logbook-design/`）: 型は入れた。lessons から 4 件を移した（10-26）。残りは `user-thinking-habits`（公開範囲の確認）と `user-manual`（対応表が先）。
6. 【起票 10-26】xlsx・pptx の点検・掃除（`room/cleankit.py`）: PC1 の実ファイルで `check`。結果で掃除の既定と `mask` への組み込みを決める。
7. 【起票 10-26】【最優先】トークン削減の見直し（`topics/token-cap/`。月次上限 2億トークン）: `/context` は取れた（Zed 19.4k、端末 36.4k）。伸びの主因はファイルの全文読みと判明（10-26）。`docs-rules.md` の切り出し（`commit-push-rules.md`）と、読み込みを抑える規則（`AGENTS.md`）は完了（10-26）。次は `exmem-index.md` の読み方。PC1 の集計（10-27）で削減量を見積もる。

## Open Questions

- 相談の型（`decisions.md` の 2026-10-21）: 4回使った。5回目で、残す・格上げする・やめるを決める。
- 会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- `brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0。
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
