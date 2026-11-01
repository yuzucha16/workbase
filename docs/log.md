# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（実機で確認済み）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。
- Python の版: uv 管理が正本（`script-guide.md` の「Python の版と呼び方」）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-15・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（10-29 決定）。一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`）。参照構造の点検は `review` の入力 9（`mdgraph.py`。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4）。積み残しは `due.md` の 11-03・11-08。単体テストは `python -I -m unittest discover -s workflow-kit/tools/tests`。`exmem-index.md` は 1 ノート 1 行。

## Next Actions

1. 【起票 10-25、期日 11-09】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。未決は `release` の束ね先。
2. 【起票 11-01、期日 11-08】`review` の入力 2（開始時の読み込み字数）を測れるようにする仕込みを足す（ユーザーが行う。呼び出し元に計測が無く、`reviews.csv` の `load_chars` が `n/a` のまま）。
3. 【起票 11-01、期日 11-08】`wrap-hook.md` に、点検スクリプト（`check_hook_outline`）の FAIL が 2 項目残っている。固有の章「応答のまとめ方」が共通部の途中にあることと、「目的と契機」の項目の並びが規定と違うこと。出力が文字化けしたので、直す前に `-X utf8` などで内容を確かめる。
4. 【起票 11-01、別セッションで行う】基準表のギャップ 13: works と dotfiles の `AGENTS.md` で、コミット・push の前の読み先を `docs-rules.md` の「コミットと push」から、`commit-push-rules.md` と `push-rules.md` の直接指定に揃える（workbase に揃える。直したらギャップ 13 を解消にし、works の未 push の 1 件も確認する）。
5. 【11-01】`log.md` を 4KB 以内に保つ（ギャップ 9。11-01 の `wrap` で縮めた。超えたら状態を `log-history.md` へ）。

## Open Questions

- 【期日 11-16】`mdrank.py` の値が下がった理由: 11-01 は 1 位 24/40、上位 5 件 35/40（10-30 は 25/40、35/40）。場面の一覧か `triggers:` の変更の影響と見ているが、未調査。引当率は母数が 42 件から 1383 件に変わり、単純には比べられない。次回の `review` が本番の比較。
- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
