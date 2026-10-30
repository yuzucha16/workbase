# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（旧 `mksub`。10-30）。`mkworks --sub` は実機で確認済み（10-30、ユーザー）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。各 PC の works への反映は済み（10-30、ユーザー）。
- Python の版: uv 管理を正本（`workflow-kit/room/.python-version`）。呼び方は `script-guide.md` の「Python の版と呼び方」（10-29 決定）。部屋の `python3` は `room init` の段 `python` が入れる（10-30 実装、実機の部屋で 3.13.14 が入ることを確認）。
- ファイル名: `workflow-kit/naming-rules.md`（kebab、Python だけ snake。10-29 決定）。既存の名前は触るついでに直し、一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`topics/md-link-graph/`）。単体テストは `workflow-kit/tools/tests/`（`python -I -m unittest discover -s workflow-kit/tools/tests`。10-30）。`exmem-index.md` は 1 ノート 1 行で書く（`--check-index` は行頭の先頭の `[[]]` だけ数える）。相談の型の本文は `exmem/lessons/consultation-pattern.md`（「相談」で引ける。10-29）。

## Next Actions

2. 【起票 10-25、期日 11-03】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。未決は `release` の束ね先。
13. 【起票 10-29】`triggers:` の誤爆と引き当て率: 部分一致の誤爆（例: 「ログイン」が札「ログ」に当たる）への備え（短い札の禁止、完全一致の書き方、現状維持）を、引き当て率の初回（11-08）を見て決める。現状（部分一致で誤爆する）は単体テスト `test_substring_match_false_positive_is_current_behavior` で固定してある。方針を変えるときはこのテストも直す。

11. 【起票 10-29】期日の移し替えの動作確認: 次の `review 消化` で `due.py` が動き、期日が来た行（最初は 11-01 の weekly）が Next Actions に上がるか。上がらない・遅れるなら、手順（`review-hook.md` の消化モード）を直す。

## Open Questions

- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
