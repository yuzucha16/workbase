# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

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

2. 【起票 10-25】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。未決は `release` の束ね先。
9. 【起票 10-28】相談の型の次の判断: PC で `cap_meter.py --latest` を「相談したい」から結論までの前後で測ってから決める（候補と経緯は `decisions.md` の 2026-10-21）。
10. 【起票 10-28】フックの合言葉を `triggers:` 索引に統一するか、フックに合わせて個別最適にするか。材料は、`hooks.md` の表、引き当て率の初回（11-08）、部分一致の誤爆（例: 「ログイン」が札「ログ」に当たる）。相談の型の札づけ（NA 9）が最初の実例になる。
13. 【起票 10-29】`room` コマンドを削除し、`uv run room.py` に統一する（PC1。`room init …` が無出力で、フックを入れ直せなかった。原因は未特定）。`Get-Command room -All` で実体を見て消し、`room <サブコマンド>` の書き方が残る文書（`guides/`、`workflow-kit/room/README.md`）を直す。その後、古い `ai/records/` を `records/` へ統合するかを決める。切り替え 3〜5 分の主因は PC1 の監視ソフトで、コマンド数を減らす案は効きにくい（ユーザー、10-28）。

## Open Questions

- 【起票 10-27】会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【起票 10-27】【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- 【起票 10-27】`brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0。
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
