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

## Next Actions

- `guides/howto/ai-room-lifecycle.md` に `room rm`（テスト用の Project・Area を跡ごと消す。11-07 新設、`room/README.md` の表にも未記載）を反映する。完了条件: 両方に `rm` の行（Project・`--area`・止まる条件）があり、ゴールの「reap で会話履歴が消える」の節から指されている。`room/README.md` にはダミー Project（`myinv*` / `mydev*`、11-07）の 1 行も足す（`ai-room-lifecycle.md` の 7 章は書き済み）。

- 【起票 11-07】room の廃止（`767273f`。`room clean`・`close` の成果物の引き渡し・`_noai/raw` `map` `source` `deliverable`）の第三者確認を、別のセッションで行う（文書修正と削除の取りこぼしの防止）。対象リストを渡さず、削除した名前と周辺語（`room clean`、`clean --path`、`_noai/raw`、`_noai/map`、`_noai/source`、`_noai/deliverable`、`deliverable-manifest`、`pending`、`masked_from`、「Area へ渡す」「引き渡し」「成果物置き場」）で `resources/` 全体を検索する（`log-history.md` と `decisions.md` は除外し、件数から見る）。見るもの: 文書の本文（`room/README.md` の `start` `stock` `mkworks` の行、`exmem/lessons/`）、`room.py` のコメント・ヘルプ・部屋に渡す文書（`ROOM_GUIDE`）、`cleankit.py`、テストの名前。手順は `exmem/inbox/2026-11-07-deletion-audit-beyond-listed-scope.md`。既知の残り: `exmem/lessons/ai-room-data-layout.md` の 58・59 行（確認日つきの履歴なので未修正）、`room-completion.ps1`（dotfiles のプロファイルの 1 行を外すまで残す）。完了条件: 現行の文書とコードに旧仕様が残っていない（残してよいのは、履歴と「廃止前」と明記したものだけ）。

- 【起票 11-07】room 廃止（`767273f`）の後始末を人が行う。① 既存 Project の `_noai/raw/` `_noai/map/` と、Area の `_noai/source/` `_noai/deliverable/` の中身を、必要なら手で移す（`room` はもう読まない。`_noai/` 直下に置き直すか、掃除済みなら `ai/in/` に置いて `start --adopt`）。② PowerShell のプロファイル（dotfiles 側）の `room-completion.ps1` の読み込みの 1 行を外し、`workflow-kit/room/room-completion.ps1` を削除して `room/README.md` の「`clean --path` の Tab 補完（廃止）」の節を消す。完了条件: 旧置き場に実データが残っておらず、プロファイルの読み込みが無く、ファイルと節が消えている。

期日のある項目は `due.md`。

## Open Questions

- 出力側の点検（AI の出力に実名や金額の形が無いか）を `cleankit` に足すか。未実現の案で、必要が見えるまで保留（ooxml-clean 由来、11-06）。
