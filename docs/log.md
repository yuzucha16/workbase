# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（旧 `mksub`。10-30）。`mkworks --sub` は実機で確認済み（10-30、ユーザー）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。各 PC の works への反映は済み（10-30、ユーザー）。
- Python の版: uv 管理を正本（`workflow-kit/room/.python-version`）。呼び方は `script-guide.md` の「Python の版と呼び方」（10-29 決定）。部屋の `python3` は `room init` の段 `python` が入れる（10-30 実装、実機の部屋で 3.13.14 が入ることを確認）。
- `logbook/`（期限のあるナレッジの置き場）: 型と運用は `logbook/README.md`。トピック `logbook-design` は 10-30 に閉じ、残りは `due.md` の 11-08・11-15・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（kebab、Python だけ snake。10-29 決定）。既存の名前は触るついでに直し、一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`。参照構造の点検は `review` の入力 9。`mdgraph.py` は循環・階層・複雑度を文字で出す。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4。10-30 に HTML と `mdreach.py` をやめ、トピック `md-link-graph` と `hook-room-alignment` を閉じた。積み残しは `due.md` の 11-03 と 11-08）。単体テストは `workflow-kit/tools/tests/`（`python -I -m unittest discover -s workflow-kit/tools/tests`。10-30）。`exmem-index.md` は 1 ノート 1 行で書く（`--check-index` は行頭の先頭の `[[]]` だけ数える）。相談の型の本文は `exmem/lessons/consultation-pattern.md`（「相談」で引ける。10-29）。

## Next Actions

2. 【起票 10-25、期日 11-09（11-03 から延期。room-type-consolidation などで成果物の周辺を整えてから。11-01 ユーザー）】人が叩くスクリプト: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。未決は `release` の束ね先。

3. 【起票 11-01、期日 11-08】`review 消化` で、11-01 の `review` が飛ばした入力 7 と 8 を行う。入力 7 は、トークン消費の自己採点（前回 10-25 の 107 点。`workflow-kit` と `exmem` に 10-25 以降の差分が 133 ファイル）。入力 8 は、`docs/alignment-baseline.md` との比較。入力 7 は 2 回続けて飛ばしたので、次も飛ばすと 3 回連続の警告になる。
4. 【起票 11-01、期日 11-08】`review` の入力 2（開始時の読み込み字数）を測れるようにする仕込みを足す（ユーザーが行う。呼び出し元に計測が無く、`reviews.csv` の `load_chars` が `n/a` のまま）。
5. 【起票 11-01、期日 11-08】`wrap-hook.md` に、点検スクリプト（`check_hook_outline`）の FAIL が 2 項目残っている。固有の章「応答のまとめ方」が共通部の途中にあることと、「目的と契機」の項目の並びが規定と違うこと。出力が文字化けしたので、直す前に `-X utf8` などで内容を確かめる。

## Open Questions

- 【期日 11-16】`mdrank.py` の値が下がった理由: 11-01 は 1 位 24/40、上位 5 件 35/40（10-30 は 25/40、35/40。10-25 は 30/43、40/43 で場面の数も違う）。場面の一覧か `triggers:` の変更の影響と見ているが、未調査。11-01 の `review` で、引当率は母数が前回の 42 件から 1383 件に変わり、単純には比べられなかった。次回の `review` が本番の比較（11-01 のユーザーの見立て: 現時点では悪い数字に見える）。

- `repos/` の受け渡し: `dev` の `env/` の実使用の後に決める。【保留 〜2026-11-05】
- `restore_project` の `_noai/final/` の上書き: 実機で保護を試してから決める。【保留 〜2026-11-05】
