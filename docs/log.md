# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（実機で確認済み）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。
- Area の改名は `room mv <旧> <新>`（旧 `rename-area`。11-02 作り直し。部屋は `wsl --export`/`--import` で改名、履歴は追わない。ee が実機で動作確認済み）。
- Python の版: uv 管理が正本（`script-guide.md` の「Python の版と呼び方」）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-15・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（10-29 決定）。一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`）。参照構造の点検は `review` の入力 9（`mdgraph.py`。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4）。積み残しは `due.md` の 11-03・11-08。単体テストは `python -I -m unittest discover -s workflow-kit/tools/tests`。`exmem-index.md` は 1 ノート 1 行。

## Next Actions

なし。

期日のある項目は `due.md`。

## Open Questions

なし。
