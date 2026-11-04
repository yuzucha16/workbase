# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`brief 計画` は試験運用中。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（実機で確認済み）。11-02 の room 変更（boundary の 2 値、start の自動マスク・復元の廃止、stock --dst）の既存 works への適用は、11-03 に ee が実機で通した（既存の Area は internal の 1 つ。手順と止まった所は `log-history.md` の 11-03）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。
- Area の改名は `room mv <旧> <新>`（旧 `rename-area`。11-02 作り直し。部屋は `wsl --export`/`--import` で改名、履歴は追わない。ee が実機で動作確認済み）。
- room open --from（11-04 実装。閉じた Project の成果物・close.md・正式な計画を、新しい Project の `ai/in/from-<前>/` に引き継ぐ。実機は未確認）。
- 実機確認済み（11-04、PC1）: `room restore` / `close` の成果物の Area への書き出し、計画の承認の検知（`status: 正式` → 変更で `仮` に戻る）。
- Python の版: uv 管理が正本（`script-guide.md` の「Python の版と呼び方」）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-15・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（10-29 決定）。一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 項目の移し替え・期日の持ち上げ: `workflow-kit/tools/na_apply.py`（close / due-up。呼び方は `docs-write-rules.md`）。実行は AI（人は介在しない）。当面は、処理の漏れがあるものとして読み、見つけたら報告する。漏れなし 3 回連続で外す（11-04 時点 1/3）。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`）。参照構造の点検は `review` の入力 9（`mdgraph.py`。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4）。積み残しは `due.md` の 11-03・11-08。単体テストは `python -I -m unittest discover -s workflow-kit/tools/tests`。`exmem-index.md` は 1 ノート 1 行。

- 論点出しの型: `exmem/lessons/issue-extraction-output.md`（v4、試用中。合図は「論点出し」「論点抽出」）。フィードバックは、ユーザーが「フィードバック」と言うと 1 行が出て、`topics/kit-growth/inbox.md` へ手で運ぶ。
- 承認のスクリーニング（サブエージェント）の効果と費用の測定（11-03 開始）: 結果は 1 行で `decisions.md` に残す（`approval-screening.md` の「結果の記録」）。費用は `usage_report.py` の「うちサブエージェント」行。見直しは `due.md` の 11-30。最初の対象は承認プロセスのみで、works の実務のレビューへの拡充は見直しの後。

## Next Actions

4. **Area 側の運営の入口を決める（起票 11-04）**: ① Area の `ai/docs/inbox.md` の【案件】【決定】を Area の `decisions.md` に統合する「Area の AI」を動かす入口が無い（`room start` は Project しか開かない。Area の `decisions.md` も `init` は作らない）。② Area の終わり方（`archives/` へ移す契機と手順）が無い。方式は 11-04 に決定済み（状態はリンク、決定・知識は転記＋出典、Area の log.md は持たない。`decisions.md` 同日）。次回はここの決定から始める。残りは入口・decisions.md の置き場（`docs/` か `ai/docs/`）・終わり方で、決めるのは ee。調査は `notes/room-lifecycle/2026-11-04-current-flow.md`（プロジェクトの共有フォルダ）の 3-B。`room open --from` の案 C（Area に資産を置く）もこの入口が決まるまで見送り。

期日のある項目は `due.md`。

## Open Questions

なし。
