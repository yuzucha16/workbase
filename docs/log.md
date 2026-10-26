# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-01 | 定例 | weekly の振り返り（7日周期、日曜）。仮決めの期限切れを数える。v7 の検証もここで | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める | ユーザー（AI が実行） |
| 2026-11-09 | 単発 | 振り返りの仮決め3件（字数の数え方、v6、v7）をまとめて判断。規模をもっと縮められるかも決める | ユーザー |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断 | ユーザー |

## 状態

- 経路は整備済み: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録は `docs/metrics/reviews.csv`、基準は `docs/alignment-baseline.md`）。フックの権限は `hooks.md` の「領域とフックの権限」。仕組みの決定は `review 消化` の3段で承認する。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。計画のやり方（`brief 計画`）は試験運用中。
- room（`workflow-kit/room/`）: type は `dev` と `inv`。実機の通しは済み、`mkworks` などの新しい機能は単体テストまで（`room/README.md`）。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Linux で確認、Windows は未確認。
- 索引（triggers）: `exmem/lessons/` などの `triggers:` を、dotfiles のフックが依頼ごとに出す（`topics/md-link-graph/`）。

## Next Actions

1. 振り返り（改善4・5）: 材料は `topics/kit-growth/records/` と `decisions.md`（2026-10-25）。次は週次 11-01、月次 11-29。
2. 整合の基準のギャップ 8: works（26 コミット）と dotfiles（5 コミット）の履歴にユーザー名入りのパスが残る（`docs/alignment-baseline.md`）。他の PC の clone は `git fetch origin && git reset origin/main` で合わせる。
3. フックと room の整合: `mkworks` の実機確認、旧名の注記の削除、dotfiles のスキルの入口（`topics/hook-room-alignment/docs/log.md`）。
4. 人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（同上）。未決は `release` の束ね先。
5. ルールが見つかりにくい構造（`topics/md-link-graph/`。完了は同窓口の条件）。
6. 期限のあるナレッジの置き場 `logbook/`（`topics/logbook-design/`。仮決め、実装前）。
7. xlsx・pptx の点検・掃除（`workflow-kit/room/cleankit.py`）: PC1 の実ファイルで `check` を 1 回（報告は AI に見せない）。結果を見て、掃除の既定と room の `mask` への組み込みを決める。Excel・PowerPoint で掃除の出力が開くかも確かめる。

## Open Questions

- 相談の型（3段と締め。`decisions.md` の 2026-10-21）: 4回使った。5回目で、残す・格上げする・やめるを決める。
- 会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し（スナップショットと patch。未検証）: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- 計画のやり方（`brief 計画`）は、実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0。
- `restore_project` が `_noai/final/` の人の変更を上書きする件: 次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
