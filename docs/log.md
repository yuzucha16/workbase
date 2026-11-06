# 作業ログ（log）

`workbase` 全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`、期日は `docs/due.md`（kit 全体の項目だけ。開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`plan`（11-04 新設、11-06 本採用）と `brief` に分けた。実機は未確認。1 セッション 2〜3 依頼のときの書き方は `guides/quickref/ai-work-prompts.md` の「brief 即」。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`。仕様と実機確認の経緯は `decisions.md` の【room】の項（11-02〜11-06）と `workflow-kit/room/README.md`。**実機未確認**: `room close` の「別名フォルダ」警告（11-05 実装）。通し試験 `workflow-kit/room/room-split-test-procedure.md`（結果は `logbook/room-split-test-log.md`）は、手順を起こしただけで未実行。room の手順書・案内文を直したときに回す。
- works の git 追跡は許可リスト方式（10-29 決定）。
- Python の版: uv 管理が正本（`script-guide.md`）。人が叩くスクリプトは `run` / `verify` / `release`（Windows は未確認）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-29。ファイル名は `workflow-kit/naming-rules.md`。
- 項目の移し替え・期日の持ち上げ: `workflow-kit/tools/na_apply.py`（呼び方は `docs-write-rules.md`）。当面は、処理の漏れがあるものとして読み、見つけたら報告する。漏れなし 3 回連続で外す（現在 0/3）。
- 索引（triggers）: `guides/explain/triggers-knowledge-index.md`。参照構造の点検は `review` の入力 9（`mdgraph.py`）。積み残しは `due.md` の 11-03・11-08。
- 論点出しの型: `exmem/lessons/issue-extraction-output.md`（v4、本採用 11-06。合言葉 `frame`、`workflow-kit/frame-hook.md`）。
- kit・規則の変更案（11-06 決定）: `wrap` の報告には出さず、直下の Open Questions に置き、`review 消化` が承認にかける。置き場の表は `topics/AGENTS.md` の「データの置き場」。
- 承認のスクリーニング（サブエージェント）の測定（11-03 開始）: 結果は `decisions.md` に 1 行（`approval-screening.md`）。見直しは `due.md` の 11-30。

## Next Actions

- 【起票 11-06、期日 11-13】`mask` / `restore` 削除で書き換えた文書類の第三者確認（`/code-review` など別の目に通す）。対象の一覧と見る点は `due.md` の 11-13 の行。担当: ユーザー。

期日のある項目は `due.md`。

## Open Questions

- 出力側の点検（AI の出力に実名や金額の形が無いか）を `cleankit` に足すか。未実現の案で、必要が見えるまで保留（ooxml-clean 由来、11-06）。
