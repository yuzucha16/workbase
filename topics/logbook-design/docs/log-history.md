# 作業ログの経緯（log-history）

## Log

### 2026-10-26（review 消化）
- 待ち行列 8 件をサブエージェントでスクリーニングし（`records/2026-10-26-queue-screening.md`）、ユーザーが 1 件ずつ判断した（`decisions.md`）。消した Next Actions: 「次の `review 消化` で待ち行列 8 件を判断する」（完了）。`obsidian-vault` の未設定を残す項は、畳みの列挙（Next Actions 4）に合流した。
- 7(a) を kit に反映した（`review-hook.md` の消化モード、04ac4c7）。

### 2026-10-26（続き）
- ユーザー: `para-operations` と `session-handoff` の Next Actions は置き換わり。畳んだ。
- ユーザー: 旧 `C:\vault` は消してよい。第3陣（`para-operations` `session-handoff`）の本文確認を `records/2026-10-26-wave3-review.md` に記録。降格は測定値だけで、残りは古い ③ の畳みと印。
- 第2陣の現況をユーザーが回答: MX Linux 導入済み、auth の Next Actions 完了、vault のバックアップは未了。
- 第1陣の 5 項目を、ユーザーの選択でこのトピックの Open Questions の待ち行列に置いた。`review 消化` の 3 段チェックの 1 段目。
- `ai-work-metrics` の ③ は、ユーザーが「続けていない、置き換わっている」と答え、畳んだ（`decisions.md`）。
- 第2陣 6 ファイルの本文確認（`records/2026-10-26-wave2-review.md`）。logbook に移すものはほぼ無く、1 回きりの移行の記録と古い ③ の畳みが主と分かった。仕組みの候補 2 つ（AI が古い ③ を見つける経路、追記の型）を待ち行列に置いた。

### 2026-10-26
- ユーザーの相談: exmem は半永久のナレッジ。これとは別に、期限のあるナレッジ（review の記録、取扱説明書、時系列で変わる知識、改善の規準、週報・月報）の置き場と、捨てる・圧縮・昇格・降格の仕組みが欲しい。流用できる既存の仕組みで、データフローを複雑にしない。must ではない。
- AI が現状を調べ、置き場の案 A/B/C と運用の叩き台を出した（`records/2026-10-26-proposal.md`）。期限のある記録は、取扱説明書（lessons）、週報・月報（`kit-growth/records/`）、review の記録（`docs/metrics/`）に散り、畳む経路が無い。
- ユーザーが案 A を `logbook/` で仮決めし、ほかにも漏れがあるはずと依頼。AI が `exmem/lessons/` 69 件を仕分けた（`records/2026-10-26-exmem-leaks.md`。title・節の構成・「時点」の数からの推測で、全文は読んでいない）。
- ユーザーが 3 型を定義（個人の好み・1 回きりを除く）。AI は ② を logbook に移さず lessons に残す案へ練り直し（`records/2026-10-26-recommendation-v2.md`）、承認された。
- 第1陣 5 ファイルの本文確認（`records/2026-10-26-wave1-review.md`）。節が単位であること、古い ③ が残っていること、`ai-work-metrics` と `claude-code-storage` の重複、公開範囲の確認事項を見つけた。
- 第1陣の仕分けを 3 段チェックに載せる前に、ユーザーが `wrap` を指示。辿れるかの確認（引当率）は別セッションに分けると決めた。記録は `topics/logbook-design/` に残し、`9f7a22b` で push 済み。
