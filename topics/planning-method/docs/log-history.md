# 作業ログの経緯（log-history）

## Log

### 2026-10-20（4）
- 2回目の題材 `stock` のモード追加（私用の `guides/explain` と AI 用の `exmem/lessons` を同じフックで動かす。`stock 理解` / `stock ナレッジ`）で `start 計画` を行い、6R・憲章・成果物 WBS・マイルストーン・作り方のメモ・理解ガイドの下書きの見本を作った（`records/stock-modes-6r.md`、`stock-modes-plan.md`、`stock-modes-plan-notes.md`、`explain-inbox-example.md`）。出力先は、`guides/inbox/`・`workbase/inbox/`・`exmem/inbox/` 維持を比べ、ユーザーが `exmem/inbox/` 維持（`kind` で区別）を選んだ（`workbase/inbox/` は約25ファイルの参照と `room.py` の書き換えが要るため却下）。決定は `docs/decisions.md`。
- 計画を書いた後のフィードバックを `stock-modes-6r.md` の末尾に足した（足りない情報: 予算の根拠、開始日と順序、承認者、変えないことの書き場所、変更先の洗い出し。再現性: 裏づけが葉につながらない、前提の表の書式と選択肢の名前の揺れ、〔資料〕の出典なし、憲章と他の表の矛盾。計画の不備として、完了時期とバッファの矛盾の修正と、`find-knowledge` の葉の追加（その後ユーザーが不要と決めて削除）を、WBS の変更の記録に残した）。`start-plan.md` への案6件は未承認。
- ユーザーが M1 の一部を確認した: 「両方」は選択肢に入れない、既存の理解ガイドの更新は対象外、`find-knowledge` の `guides/` 対応は不要。ユーザーの選択は「設計に進む」（計画で止めない）。`workflow-kit/` は書き換えていない。

### 2026-10-20（3）
- 試行の題材（トークン・コスト可視化）を、ユーザーの指示で実装した。成果物: `workflow-kit/tools/usage_report.py`（週次・月次の集計）、`usage_report_html.py`（概要と詳細・分析の HTML）、`usage_prices.json`（公式の単価表、取得日 2026-10-20）、`guides/howto/claude-usage-report.md`（使い方）。突合: 10-19 以降の合計トークンが ccusage と完全一致（79,675,204）、費用は $26.17 対 $26.175。計画の指標（±5%）を満たした。M1・M2 に当たる作業と M3 の手順書が、同じ日の1セッションで終わった。
- 実行後のフィードバックを `records/usage-viz-6r.md`、`usage-viz-plan.md`、`usage-viz-plan-notes.md` の末尾に足した（足りない欄: 用語の定義、対象外の見直し条件、出力の置き場、承認が要る変更先、WBS の変更の記録、動作確認。薄い欄: 憲章の体制、仮説、状況。見積もりが日数で桁外れ）。決定は `docs/decisions.md`。
- 実装で見つかった落とし穴: 1つの API 応答がログの複数行に同じ usage で繰り返される（`message.id` と `requestId` で1回だけ数える）。キャッシュ作成が5分と1時間に分かれる。未確認: HTML の見た目（ブラウザで開いていない）、自動テストは無い。

### 2026-10-20（2）
- 計画のやり方の試行として、題材「セッション別トークン・価格・キャッシュの可視化（CLI、分析用途）」で、6R・憲章・成果物 WBS・マイルストーンを作った（`records/usage-viz-6r.md`、`usage-viz-plan.md`、`usage-viz-plan-notes.md`）。見えたこと: ①最初の6Rは、欄名が記録に無く仮置きになり、予算・体制を欄に入れ、検査も載せていた。欄名の追記（draft の A 節）の後、骨子に合わせて作り直した（欄名が文書に無いと、AI は仮置きにする）。②読みが割れ（既存ツール導入・自作・併用）、前提の表を出して併用を仮置きにした。ユーザーの選択は未了。③「検証」を「憲章」と読んだ（未確認）。④上限3つのため、10-23 以降の作業（運用の手順書）を 10-26 の節目に束ねた。⑤初の kit 以外の題材（1週間、見本なし）。正式な品質チェック3回には数えない（昇格前）。決定は `docs/decisions.md`（置き場）。
### 2026-10-20
- 計画のやり方を `topics/kit-growth/records/` から切り出し、`topics/planning-method/`（Project 型）を作った。下書き（骨子、Must と Want、登録の作業）は `planning-method-draft.md` に移し、records の `planning-method-record.md` は測ったことだけにした。決定は `docs/decisions.md`、次の一手は `docs/log.md` に置いた。ユーザーの指示（まず計画だけで様子を見る）。それ以前の経緯は直下の `docs/log-history.md` の 2026-10-19 の項。
