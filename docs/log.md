# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。2026-10-25 に 18KB から縮めた（縮める前の全文は `log-history.md` の同日の項）。

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

- 経路は整備済み: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録は `docs/metrics/reviews.csv`、基準は `docs/alignment-baseline.md`）。フックの権限は `hooks.md` の「領域とフックの権限」が正本。仕組みの決定は `review 消化` の3段で承認する。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。計画のやり方（`brief 計画`）は試験運用中（Open Questions）。
- room（`workflow-kit/room/`）: 実機の通しは済み。type は `dev` と `inv`。`mkworks`、並行 start、Area を跨ぐ共有知、部屋の git とトレーラーは、単体テストまで（実機は一部未確認）。使い方は `room/README.md`、経緯は `log-history.md` の 2026-10-18〜25 の項。
- 人が叩くスクリプトの名前は `run` / `verify` / `release`（`script-guide.md`）。Linux で確認、Windows は未確認。
- 索引（triggers）: `exmem/lessons/` に `triggers:` を付け、dotfiles の `UserPromptSubmit` フックが依頼ごとに出す。参照構造は `topics/md-link-graph/`。

## Next Actions

1. 振り返り（改善4・5）: 材料と施策は `topics/kit-growth/records/` と `decisions.md`（2026-10-25 の項）。次は週次 11-01、月次 11-29。
2. 整合の基準のギャップ 8（公開リポジトリの履歴にユーザー名入りのパス）は、書き換えが force push で禁止のため未着手。
3. `review`: `review-hook.md` が 5,455 字で目安超過。次回に畳む候補。`token-matrix.md` の行 25 と 24 の順を直す。
4. 会議録のナレッジ化の残り: 指標（冒頭の行数の上限 10 行、人が直した箇所の数）のスクリプト。新規に作り直して試した分から数える（ユーザー、10-21）。
5. フックと room の整合（`topics/hook-room-alignment/`）: `mkworks` の実機確認、旧名（`init` `open` `start`）の注記を消す、dotfiles の Claude 用スキルの入口。
6. 人が叩くスクリプト: PC2 の Windows で `verify.bat` を 1 回実行して確かめる。未実装は `run.py` の型、ps1 版、原因の台帳、`release` の束ね先。
7. ルールが見つかりにくい構造（`topics/md-link-graph/`。完了は同窓口の条件）。
8. 未 push: workbase、works、dotfiles（`review` の変更と整合の基準の移動、`UserPromptSubmit` フック）。

## Open Questions

- 相談の型(3段と締め。決定の項は `decisions.md` の 2026-10-21)の仮決めは、`plan-room-link` で4回使って閉じた。5回目で、残す・格上げする・やめるを決める。次に論点の多い相談をするときに数える。
- 会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し（スナップショットと patch。未検証）: `dev` の `env/` の実使用の後に決める(`env/` だけの実測は 10-25 に済んだが、`repos/` の受け渡しは測っていない)。【保留 〜2026-11-05】
- 計画のやり方（`brief 計画`）を、試験運用のままにするか正式化するか。案 = 当面は試験運用のまま、次に実務で使った回の所見で判断する。場所 = `workflow-kit/brief-plan.md`、`methods.md`。
- `restore_project` が `_noai/final/` の人の変更を上書きする件: 正本の宣言と上書き前の警告を、次の実機で `final-manifest.json` の保護を試した後に決める。【保留 〜2026-11-05】
