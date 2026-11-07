# 作業ログ（log）

`workbase` 全体の現在状態と次にやること。トピック固有の Next Actions は置かない（各トピックの `docs/log.md` だけが持つ）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`、期日は `docs/due.md`（kit 全体の項目だけ。開始時には読まない。`review 消化` が拾う）。

## 状態

- 経路: 受け皿 = トピック、入力 = `inbox.md`、見直し = `review`（記録 `docs/metrics/reviews.csv`、基準 `docs/alignment-baseline.md`、星取り `workflow-kit/token-matrix.md` は 11-01 に 110 点）。仕組みの決定は `review 消化` の3段で承認。仮決めは `【仮 〜日付】`。
- やり方は `methods.md`。`plan`（11-04 新設、11-06 本採用）と `brief` に分けた。実機は未確認。1 セッション 2〜3 依頼のときの書き方は `guides/quickref/ai-work-prompts.md` の「brief 即」。
- room: type は `dev` と `inv`。検証用の works は `mkworks --sub`。仕様と実機確認の経緯は `decisions.md` の【room】の項（11-02〜11-06）と `workflow-kit/room/README.md`。**実機未確認**: `room close` の「別名フォルダ」警告（11-05 実装）。通し試験 `workflow-kit/room/room-split-test-procedure.md`（結果は `logbook/room-split-test-log.md`）は、手順を起こしただけで未実行。room の手順書・案内文を直したときに回す。
- works の git 追跡は許可リスト方式（10-29 決定）。
- room の試験用ダミー Project: 名前が `myinv*` / `mydev*`（11-07 決定）。git 追跡外で、`open` / `close` / `start` / `rm` はコミットも Area の一覧も触らない。AI が room の試験で Project を作るときはこの名前を使う（`AGENTS.md` の共通ルールに 1 行）。手順は `ai-room-lifecycle.md` の 7 章、経緯は `decisions.md`。
- `_noai/` 直下の予約名は `mask.toml` だけ（11-07。`user/` `raw/` `map/` `source/` `deliverable/` は廃止。それ以外は人が自由に置く）。`room clean` と `close` の成果物の引き渡しも廃止（11-07）。掃除は人が cleankit で行い `--adopt` で通す。
- Python の版: uv 管理が正本（`script-guide.md`）。人が叩くスクリプトは `run` / `verify` / `release`（Windows は未確認）。
- `logbook/`（期限のあるナレッジ）: 型は `logbook/README.md`。残りは `due.md` の 11-08・11-29。ファイル名は `workflow-kit/naming-rules.md`。
- 項目の移し替え・期日の持ち上げ: `workflow-kit/tools/na_apply.py`（呼び方は `docs-write-rules.md`）。当面は、処理の漏れがあるものとして読み、見つけたら報告する。漏れなし 3 回連続で外す（現在 0/3）。
- 索引（triggers）: `guides/explain/triggers-knowledge-index.md`。参照構造の点検は `review` の入力 9（`mdgraph.py`）。積み残しは `due.md` の 11-03・11-08。
- 論点出しの型: `exmem/lessons/issue-extraction-output.md`（v4、本採用 11-06。合言葉 `frame`、`workflow-kit/frame-hook.md`）。
- kit・規則の変更案（11-06 決定）: `wrap` の報告には出さず、直下の Open Questions に置き、`review 消化` が承認にかける。置き場の表は `topics/AGENTS.md` の「データの置き場」。
- 承認のスクリーニング（サブエージェント）の測定（11-03 開始）: 結果は `decisions.md` に 1 行（`approval-screening.md`）。見直しは `due.md` の 11-30。
- kit 変更のコミット前のサブエージェントレビュー案（11-08 保留）: 再判断は `due.md` の 11-15。

## Next Actions

- 【起票 11-07】room 廃止（`767273f`）の後始末を人が行う。既存 Project の `_noai/raw/` `_noai/map/` と、Area の `_noai/source/` `_noai/deliverable/` の中身を、必要なら手で移す（`room` はもう読まない。`_noai/` 直下に置き直すか、掃除済みなら `ai/in/` に置いて `start --adopt`）。完了条件: 旧置き場に実データが残っていない。
- 【起票 11-07（revealjs-slides から移管）、期日 11-14】PC1 で `python -I workflow-kit/tools/excalidraw-viewer/excalidraw_view.py <.excalidraw> --no-open` を試す（初回の `npm install` が SSL 検査で通るかも見る。失敗したら出力を貼る。キャッシュの実測も: 冒頭の説明は約 40MB、`topics/revealjs-slides/docs/log.md` は約 210MB で食い違う）。閲覧ページは Windows で人が見る用。AI は `--export` を部屋でも使う（PC1 の room でも `npm install` が通る必要がある。同じ確認に含める）。理解ガイドの下書き `exmem/inbox/2026-11-07-excalidraw-viewer-js-npm-explain.md`（未統合。`inboxを整理して` で `guides/explain/` へ）。担当: ユーザー。

期日のある項目は `due.md`。

## Open Questions

- 出力側の点検（AI の出力に実名や金額の形が無いか）を `cleankit` に足すか。未実現の案で、必要が見えるまで保留（ooxml-clean 由来、11-06）。
