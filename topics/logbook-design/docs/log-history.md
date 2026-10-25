# 作業ログの経緯（log-history）

## Log

### 2026-10-26
- ユーザーの相談: exmem は半永久のナレッジ。これとは別に、期限のあるナレッジ（review の記録、取扱説明書、時系列で変わる知識、改善の規準、週報・月報）の置き場と、捨てる・圧縮・昇格・降格の仕組みが欲しい。流用できる既存の仕組みで、データフローを複雑にしない。must ではない。
- AI が現状を調べ、置き場の案 A/B/C と運用の叩き台を出した（`records/2026-10-26-proposal.md`）。期限のある記録は、取扱説明書（lessons）、週報・月報（`kit-growth/records/`）、review の記録（`docs/metrics/`）に散り、畳む経路が無い。
- ユーザーが案 A を `logbook/` で仮決めし、ほかにも漏れがあるはずと依頼。AI が `exmem/lessons/` 69 件を仕分けた（`records/2026-10-26-exmem-leaks.md`。title・節の構成・「時点」の数からの推測で、全文は読んでいない）。
- ユーザーが 3 型を定義（個人の好み・1 回きりを除く）。AI は ② を logbook に移さず lessons に残す案へ練り直し（`records/2026-10-26-recommendation-v2.md`）、承認された。
- 第1陣 5 ファイルの本文確認（`records/2026-10-26-wave1-review.md`）。節が単位であること、古い ③ が残っていること、`ai-work-metrics` と `claude-code-storage` の重複、公開範囲の確認事項を見つけた。
