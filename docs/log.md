# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-01 | 定例 | weekly の振り返り（7日周期、日曜。材料は `topics/kit-growth/records/`）。仮決めの期限切れを数える | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-04 | 単発 | 返答の並び（求めること・確認を最下段、結論をその直前。`AGENTS.md`）の 1 週間の試行を続けるか判断 | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める | ユーザー（AI が実行） |
| 2026-11-09 | 単発 | 振り返りの仮決め2件（字数の数え方、v6）をまとめて判断。規模をもっと縮められるかも決める | ユーザー |
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
4. 【起票 10-20、10-26 に 11-08 まで延長】ルールが見つかりにくい構造（`topics/md-link-graph/`。完了条件は満たした。道具は 10-27 に `workflow-kit/tools/` へ移した。引き当て率の初回 11-08 の後に、閉じるかを聞く。`triggers:` の上限は 10-27 に 30 語へ。誤爆が増えていないかも 11-08 に見る）。
5. 【起票 10-25】期限のあるナレッジの置き場 `logbook/`（`topics/logbook-design/`）: 残りは引当率の確認（NA4 と同じ 11-08）と、トピックの Next Actions。
6. 【起票 10-26】xlsx・pptx の点検・掃除（`room/cleankit.py`、`topics/ooxml-clean/`）: 次は、列挙して消す方式から、汎用の「見えないものをすべて落とす」許可方式のスクリプトへ（他セッションに引き継ぎ。案は 10-28 のスレッドの返信: 許可した部品の種類だけ残す＋出力の文字が見えているセル値・シート名・固定語に当たるかを調べる。まず `check` に文字の検査だけ足す案）。今の `cleankit.py` で残るのは、見た目・数式が崩れていないかの人の確認、`mask` への組み込み、pptx の実ファイル確認。
7. 【起票 10-26】【最優先】トークン削減の見直し（`topics/token-cap/`。月次上限 2億トークン）。残り: room の 107k の確認（トピックの NA 1）。規則側の削減と lessons の分割の効果を、10-28 以降の `cap_meter.py` で確かめる。`exmem/` の 2 か所と `templates/workspace/AGENTS.md` の参照文は未変更。
8. 【起票 10-27】公開リポジトリの文言の整理（`topics/wording-neutralize/`）: 残りは段階 4（履歴の書き換え。ユーザーが後日、急がない）。
9. 【起票 10-28】`wrap` の済／一部済／未の分け方（`workflow-kit/wrap-hook.md` の手順 2）の確認: 次の数回の `wrap` で、済んだ項目が移されるか、誤って閉じていないか、報告に閉じた数と聞く項目が出るかを見る。ずれたら `review` の入力に足す。
10. 【起票 10-28】トピックを閉じる手順（`topics/close-procedure.md`）の残り 2 件（ユーザーが後で行う）: (a) すでに切れたリンク 2 か所（`docs/log-history.md` → `private-knowledge/records/private-knowledge-checks.md`、`topics/kit-growth/records/planning-method-record.md` → `private-knowledge/records/`）の修復。(b) 閉じたトピックで git の履歴にだけ残る有益なデータ・スクリプト・見本（`private-knowledge` の通し試験の手順 `pull-e2e-test.md` と会議メモの見本、`usage-viz` `stock-modes` `plan-room-link` の 6R・憲章・WBS の実例など）のサルベージ。行き先は `close-procedure.md` の表。新しい手順を最初に当てはめる対象は、外から指される records が多い `topics/token-cap/`。

## Open Questions

- 相談の型（`decisions.md` の 2026-10-21）: 4回使った。5回目で、残す・格上げする・やめるを決める。
- 【起票 10-27】会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【起票 10-27】【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- 【起票 10-27】`brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0。
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
