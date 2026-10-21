# 判断の記録（decisions）

## Principles

## Decisions

### 【この件】stock のモード追加: 出力先・モード名・引数なし・更新・重複確認の範囲を決めた（2026-10-20）
- 決めたこと（ユーザー）: ①`exmem/inbox/` を唯一の窓口として維持し、frontmatter で区別する（`workbase/inbox/` と `guides/inbox/` は却下）。②モード名は `stock 理解` と `stock ナレッジ`。③引数なしの `stock` は1問でモードを選ばせる。選択肢に「両方」は入れない。④既存の理解ガイドの更新（追記・上書き）は対象外。⑤`find-knowledge` の `guides/` 対応は不要（WBS 1.3.2 を取り下げ）。
- 根拠: ユーザーの回答。①は「煩雑」「影響の割に動作が同じ」（約25ファイルの参照と `room.py` の書き換えが要る）が理由。
- 却下案: `guides/inbox/`（窓口が3か所に増え、点検の形が2系統になる）、`workbase/inbox/`（上記）、`stock` の選択肢に「両方」（ユーザーが不要と判断）。
- 未決: 下の【提案】のうち、提案1・3・4（更新の対象外を除く）・5・7 は、ユーザーが個別には確認していない（M1 の残り）。

### 【この件】設計の【提案】を承認し、実装と通し試験まで進めた（2026-10-21）
- 決めたこと（ユーザー、2026-10-21）: 下の【提案】は、すべて承認する（取り下げた2・6を除く）。M1〜M3 の全工程を進めてよい。`private-knowledge` との重なりの整理は、仕様の追加・削除を含めてよい。
- 実装（`workflow-kit/`）: `stock-hook.md`（モード、引数なしの1問、固有の事実）、新規 `stock-explain.md`（理解ガイドの書き方）、`integrate-hook.md`（`kind: explain` の節）、`tools/check_inbox.py` と `check-inbox.ps1`（`kind` で分岐）、`examples/inbox-example-explain.md`、整合（`hooks.md`、`README.md`、`room-context.md`、`room/README.md`、`hook-matrix.md`、`exmem/AGENTS.md`、`exmem/inbox/README.md`、`guides/AGENTS.md`）、`room/room.py`（`kind: explain` に古さの印を付けない）と単体テスト1件。
- 設計からの差分（AI の判断。**確認を求める**）: ①書き方を `stock-hook.md` に足さず `stock-explain.md` に分けた（理由: `stock-hook.md` が字数の例外枠の 7.5k で、足すと +20% を超える。実際は 8.2k + 別に約2k）。②モバイル用プロンプト（`exmem/inbox/README.md`）は lesson だけにした（explain は kit だけ）。③`room stock` は、explain に `base_stale` を付けない（`integrate` が新規作成だけで、古さが意味を持たないため）。④重複確認は `find-knowledge` を使わず、`guides/guides-index.md` を見る（⑤の決定どおり、`guides/` 対応はしない）。
- 確認: 点検スクリプト（py・ps1）は、見本の explain と、既存の理解ガイド1本（`review-hook-why.md`）を6見出しに直した下書きで FAIL 0。壊した版（見出し名、`（仮説: …）`、根拠なしの確認）では、両方が同じ4件の FAIL。lesson の見本は、変更の前後で FAIL・WARN が同じ（PASS は `kind` の1項目だけ増えた）。`StockTest` 4件が合格。`check-hook-outline` は FAIL なし。**未実施**: 実機の `room stock`、`integrate` の実行（`guides/explain/` には何も作っていない）。
- 根拠: ユーザーの承認（2026-10-21）。

### 【提案→承認 2026-10-21】stock のモード追加の設計（2026-10-20。AI の提案。提案2の「両方」と提案6は取り下げ）
- 計画: `records/stock-modes-plan.md`（WBS 1.1.1）。ユーザーの決定済みの部分は次の3点だけ。①出力先は `exmem/inbox/` を唯一の窓口として維持し、frontmatter で区別する。②モード名は `stock 理解`（`guides/explain`）と `stock ナレッジ`（`exmem/lessons`）。③引数なしの `stock` は1問でモードを選ばせる。`integrate` は分けず、`check-inbox` の分岐で区別する案も、ユーザーの示唆。以下は、その具体化の提案。
- 提案1 `kind`: frontmatter に `kind: lesson | explain` を足す（`type: inbox` は変えない）。省略は `lesson`（既存のメモは直さない）。
- 提案2 引数なしの1問: 選択肢は「理解（人向け）」「ナレッジ（AI 向け）」「両方」。「両方」は、話題が別なら2ファイル（`stock` の手順「話題を分ける」と同じ扱い）。Recommended は、会話の中心が「なぜ・どう動く」なら理解、「判断・原則・落とし穴」ならナレッジ。
- 提案3 理解ガイドの下書きの形: `reference-doc-types` の理解ガイドの型に合わせた6見出し（冒頭 / ダイジェスト / 基礎知識 / チェックリスト / 補足 / 要確認事項）。「基礎知識」の末尾に「自分で説明するときの一言」。該当が無い見出しは `なし`。確認・仮説の表記（`（確認: …）` `（仮説）`）、機微の禁止、単体で読める書き方は `lesson` と同じ。見本: `workflow-kit/examples/inbox-example-explain.md`（2026-10-21 に `records/` から移した）。
- 提案4 `integrate` の分岐: `kind: explain` は `guides/explain/<name>.md` に新規作成し、frontmatter を `type: explain`、`title`、`tags`（`exmem/tags.md` の語彙に正規化）に変換する（`kind` `created` `sources` は外す。`checked` は調査の成果物だけ）。`guides/guides-index.md` に1行足す。ファイル名はリポジトリ内で一意にする。実物との照合と、メモの削除は `lesson` と同じ。既存の `explain/` への追記・上書きは対象外（6R の対象外）。
- 提案5 点検: `check-inbox` は `kind` で項目を切り替える。`explain` は、6見出しの存在と順序、文章の規則、機微の禁止を見る。`lesson` の Decisions の3点セットなどは見ない。
- 提案6 重複確認: `explain` のとき、`find-knowledge` で `guides/` も検索する（WBS 1.3.2。要否は確認してから決める）。
- 提案7 窓口と権限: `hooks.md` の窓口（`exmem/inbox/` と `kit-growth/inbox.md`）と権限表は変えない。別名（日本語）は、`stock 理解`＝「理解ガイドにして」、`stock ナレッジ`＝「ナレッジ化して」と同じ。
- 未確認: 部屋の `room stock` が `kind` をそのまま運ぶか（`room.py` を読んでいない）。
- 見直しの条件と戻し方: 通し試験（M3）で FAIL が出る、または使われなければ、`kind: explain` の分岐を外して戻す（履歴は git）。
