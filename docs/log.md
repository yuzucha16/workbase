# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ。2026-10-29）。作業の終わりに更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。日付で浮上する項目は `docs/due.md`（kit 全体の項目だけ。トピック固有の期日は各トピックの `docs/due.md`。11-06。開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`plan` は本採用（11-06 決定）。`plan`（11-04 新設。`room open` 直後の 6R → 論点出し → 憲章以降）と `brief`（`room start` 直後）に分けた。実機は未確認。1 セッション 2〜3 依頼のときの `brief` の書き方は `guides/quickref/ai-work-prompts.md` の「brief 即」。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`（実機で確認済み）。11-02 の room 変更（boundary の 2 値、start の自動マスク・復元の廃止、stock --dst）の既存 works への適用は、11-03 に ee が実機で通した（既存の Area は internal の 1 つ。手順と止まった所は `log-history.md` の 11-03）。
- room の通し試験（11-06、トピック room-type-consolidation を閉じた）: 分割して進める 6 回の手順は `workflow-kit/room/room-split-test-procedure.md`（結果は `logbook/room-split-test-log.md`）。room の手順書・案内文を直したときに回す。手順は未実行（前回のスクリプトから起こしただけ）。
- works の git 追跡は許可リスト方式（10-29 決定。`decisions.md`）。
- Area の改名は `room mv <旧> <新>`（旧 `rename-area`。11-02 作り直し。部屋は `wsl --export`/`--import` で改名、履歴は追わない。ee が実機で動作確認済み）。
- room open --from（11-04 実装。閉じた Project の成果物・close.md・正式な計画を、新しい Project の `ai/in/from-<前>/` に引き継ぐ。11-05: 写すものが無くても止めず、来歴だけ付けて開く。実機確認済み 11-06、PC1）。
- room close が Area へ渡す成果物は `ai/out/<Project 名>/`（11-05 変更。旧名 `deliverable/` も可。`decisions.md` 同日。実機確認済み 11-06）。部屋の AI が別名のフォルダに置くと渡らない問題は、`close` が警告して `[y/N]` で確かめる（11-05 実装。実機は未確認）。
- Area の log・decisions・inbox は持たない（11-05 決定）。`room close` は【案件】【決定】を Area へ運ばず、記録は `archives/` に残る。引くのは `room trace --area <Area> <語>`（横断検索。実機確認済み 11-06）。Area は `room close --area` で終える（11-05 実装。実機確認済み 11-06）。
- 実機確認済み（11-04、PC1）: `room restore` / `close` の成果物の Area への書き出し、計画の承認の検知（`status: 正式` → 変更で `仮` に戻る）。
- Python の版: uv 管理が正本（`script-guide.md` の「Python の版と呼び方」）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-29。
- ファイル名: `workflow-kit/naming-rules.md`（10-29 決定）。一括改名はしない。
- 人が叩くスクリプトは `run` / `verify` / `release`（`script-guide.md`）。Windows は未確認。
- 項目の移し替え・期日の持ち上げ: `workflow-kit/tools/na_apply.py`（close / due-up。呼び方は `docs-write-rules.md`）。実行は AI（人は介在しない）。当面は、処理の漏れがあるものとして読み、見つけたら報告する。漏れなし 3 回連続で外す（11-04 の review 消化で漏れが見つかり 0/3 に戻した）。
- 索引（triggers）: dotfiles のフックが依頼ごとに出す（`guides/explain/triggers-knowledge-index.md`）。参照構造の点検は `review` の入力 9（`mdgraph.py`。基準値は循環 91%、最大の深さ 5、辺/ファイル 7.4）。積み残しは `due.md` の 11-03・11-08。単体テストは `python -I -m unittest discover -s workflow-kit/tools/tests`。`exmem-index.md` は 1 ノート 1 行。

- 論点出しの型: `exmem/lessons/issue-extraction-output.md`（v4、本採用 11-06。合言葉は `frame`＝「論点出し」「課題設定」。`workflow-kit/frame-hook.md`）。フィードバックは、ユーザーが「フィードバック」と言うと 1 行が出て、`docs/inbox.md` へ手で運ぶ。
- kit・規則の変更案（11-06 決定）: `wrap` の報告には出さず、直下の Open Questions に置き（トピックで出たものも）、`review 消化` が直下を読んで承認にかける。過去分は移さない。置き場の全体の表は `topics/AGENTS.md` の「データの置き場」（11-06 に NA 6 を閉じた）。
- 承認のスクリーニング（サブエージェント）の効果と費用の測定（11-03 開始）: 結果は 1 行で `decisions.md` に残す（`approval-screening.md` の「結果の記録」）。費用は `usage_report.py` の「うちサブエージェント」行。見直しは `due.md` の 11-30。最初の対象は承認プロセスのみで、works の実務のレビューへの拡充は見直しの後。

## Next Actions

- 【起票 11-06、期日 11-13】`mask` / `restore` 削除で書き換えた文書類の第三者確認（`/code-review` などで別の目に通す。ooxml-clean を閉じたので、ここへ移した）。対象: `workflow-kit/room/README.md`、`room-context.md`、`hooks.md`、`project-structure.md`、`guides/howto/{ai-room-setup,ai-room-setup-script,ai-room-lifecycle,ooxml-clean}.md`、`guides/explain/{ai-room-why,ooxml-residue,cross-area-shared-knowledge}.md`。見る点: 削除済みの `mask` `restore` `final/` `mask-spec.md` への言及の取りこぼし、リンク切れ、手順の飛び。履歴の `exmem/lessons/` は対象外。担当: ユーザー。

期日のある項目は `due.md`。

## Open Questions

- 出力側の点検（AI の出力に実名や金額の形が無いか）を `cleankit` に足すか。未実現の案で、必要が見えるまで保留（ooxml-clean 由来、11-06）。
