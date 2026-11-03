# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（実機で確認済み）。11-02 の room 変更（boundary の 2 値、start の自動マスク・復元の廃止、stock --dst）の既存 works への適用は、11-03 に ee が実機で通した（既存の Area は internal の 1 つ。手順と止まった所は `log-history.md` の 11-03）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。
- Area の改名は `room mv <旧> <新>`（旧 `rename-area`。11-02 作り直し。部屋は `wsl --export`/`--import` で改名、履歴は追わない。ee が実機で動作確認済み）。
- Python の版: uv 管理が正本（`script-guide.md` の「Python の版と呼び方」）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-15・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（10-29 決定）。一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 項目の移し替え・期日の持ち上げ: `workflow-kit/tools/na_apply.py`（close / due-up。呼び方は `docs-write-rules.md`）。実行は AI（人は介在しない）。当面は、処理の漏れがあるものとして読み、見つけたら報告する。漏れなし 3 回連続で外す（11-02 時点 0/3）。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`）。参照構造の点検は `review` の入力 9（`mdgraph.py`。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4）。積み残しは `due.md` の 11-03・11-08。単体テストは `python -I -m unittest discover -s workflow-kit/tools/tests`。`exmem-index.md` は 1 ノート 1 行。

- 論点出しの型: `exmem/lessons/issue-extraction-output.md`（v4、試用中。合図は「論点出し」「論点抽出」）。フィードバックは、ユーザーが「フィードバック」と言うと 1 行が出て、`topics/kit-growth/inbox.md` へ手で運ぶ。
- 承認のスクリーニング（サブエージェント）の効果と費用の測定（11-03 開始）: 結果は 1 行で `decisions.md` に残す（`approval-screening.md` の「結果の記録」）。費用は `usage_report.py` の「うちサブエージェント」行。見直しは `due.md` の 11-30。最初の対象は承認プロセスのみで、works の実務のレビューへの拡充は見直しの後。

## Next Actions

1. **論点出しの型 v4 の実作業での確認（起票 11-03）**: 決定メモを貼った作業セッションで、手戻りが減ったかを見る。作業セッション側のフィードバック（inbox の「未選別」）が届いたら、型に反映するか `review` で選別する。実機・実案件でしか確かめられない。

2. **room の成果物の Area への書き出しの実機確認（起票 11-04）**: `clean` だけの Project（マスクしていない）で `ai/out/deliverable/` にファイルを置き、① `room restore <名>` と ② `room close <名>` が、Area の `_noai/deliverable/<Project>/` に書くかを見る。マスクした Project は実名に戻って書かれるか、Area 側を人が変えたあとは何も書かずに止まるか（close は何も変えずに止まる）も見る。実機でしか確かめられない。

3. **README の完了条件・範囲外・Open Questions を、6R と重複しない形に畳む（起票 11-03）**: Project の README の 3 項目は 6R（`ai/work/plan/`）の「期待する成果」「今回のスコープ」の対象外、「裏づけ・未決」と重なる。6R を指す 1 行に畳むか、今のまま残すか、README_TEMPLATE と `room-context.md` の読み方を含めて決める。決めるのは ee。

4. **`room readme` を `room stock --dst area` の考え方に揃える（起票 11-03）**: readme は cleankit の点検、start 後に人が直した README との衝突検出、manifest への記録が無く、`--commit` だけ持つ。案 A（推奨）は、コマンド 2 本のまま「運ぶ」部品（点検・衝突検出・記録）を共通にする。ee の決定待ち: `--commit` を外すか、衝突時に止めるか差分 y/N か。案の比較は `notes/room-readme-stock/2026-11-03-alignment.md`（プロジェクトの共有フォルダ）。

期日のある項目は `due.md`。

## Open Questions

なし。
