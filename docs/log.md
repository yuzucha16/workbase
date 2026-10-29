# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。`mkworks` などの新機能は単体テストまで（`room/README.md`）。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`topics/md-link-graph/`）。相談の型の本文は `exmem/lessons/consultation-pattern.md`（「相談」で引ける。10-29）。

## Next Actions

2. 【起票 10-25】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。未決は `release` の束ね先。
10. 【起票 10-28】フックの合言葉を `triggers:` 索引に統一するか、フックに合わせて個別最適にするか。材料は、`hooks.md` の表、引き当て率の初回（11-08）、部分一致の誤爆（例: 「ログイン」が札「ログ」に当たる）。相談の型の札づけ（10-29 済。`exmem/lessons/consultation-pattern.md`。測定は `topics/token-cap/records/2026-10-29-consultation-pattern-cost.md`）が最初の実例。相談は未実施（10-29 の会話で始める予定だったが、wrap で閉じた。次の会話で、型の①から）。

11. 【起票 10-29】期日の移し替えの動作確認: 次の `review 消化` で `due.py` が動き、期日が来た行（最初は 11-01 の weekly）が Next Actions に上がるか。上がらない・遅れるなら、手順（`review-hook.md` の消化モード）を直す。
12. 【起票 10-29】kit-growth の看板を下ろす（窓口と handover の削除、`topics/AGENTS.md` と `topics-index.md` の書き換え）: 仮決め済み（`decisions.md` の 2026-10-29）。`review 消化` で承認されたら実装する。

## Open Questions

- 【起票 10-27】会議録の Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 【起票 10-27】【案件】の行き先: `para-operations` は Area の `docs/decisions.md`、実装は Area の `ai/docs/inbox.md`。現行はどちらか。
- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- 【起票 10-27】`brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0。
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
