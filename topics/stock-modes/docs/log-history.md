# 作業ログの経緯（log-history）

## Log

### 2026-10-21
- ユーザーが設計の【提案】を一括承認し、全工程の実行と `private-knowledge` との整理を指示した。`workflow-kit/` に `stock 理解` を実装した（`stock-hook.md` のモードと1問、新規 `stock-explain.md`、`integrate-hook.md` の `kind: explain`、`check_inbox.py` と `check-inbox.ps1` の `kind` 分岐、見本 `examples/inbox-example-explain.md`、整合10ファイル、`room.py` の `kind: explain` は古さの印なし＋単体テスト）。通し試験: 既存の理解ガイド1本を6見出しに直した下書きで FAIL 0（py・ps1 が一致）。字数: `stock-hook.md` 7.5k → 8.2k、`integrate-hook.md` 2.7k → 3.4k（基準 +50% 未満）。
- フィードバックを `topics/planning-method/planning-method-feedback-stock-modes-m1.md` に書いた（削除候補7、粒度5、足りない5、案8件。未承認）。`private-knowledge` との整理: `kind` は `type` ごとの値で衝突しない、「冒頭」は型ごとに別物、固有の事実は仮名でも workbase に書かない（`stock-hook.md` に追加）。仕様の削除はなし。

### 2026-10-20（4）
- 2回目の題材 `stock` のモード追加（私用の `guides/explain` と AI 用の `exmem/lessons` を同じフックで動かす。`stock 理解` / `stock ナレッジ`）で `start 計画` を行い、6R・憲章・成果物 WBS・マイルストーン・作り方のメモ・理解ガイドの下書きの見本を作った（`records/stock-modes-6r.md`、`stock-modes-plan.md`、`stock-modes-plan-notes.md`、`explain-inbox-example.md`）。出力先は、`guides/inbox/`・`workbase/inbox/`・`exmem/inbox/` 維持を比べ、ユーザーが `exmem/inbox/` 維持（`kind` で区別）を選んだ（`workbase/inbox/` は約25ファイルの参照と `room.py` の書き換えが要るため却下）。決定は `docs/decisions.md`。
- 計画を書いた後のフィードバックを `stock-modes-6r.md` の末尾に足した（足りない情報: 予算の根拠、開始日と順序、承認者、変えないことの書き場所、変更先の洗い出し。再現性: 裏づけが葉につながらない、前提の表の書式と選択肢の名前の揺れ、〔資料〕の出典なし、憲章と他の表の矛盾。計画の不備として、完了時期とバッファの矛盾の修正と、`find-knowledge` の葉の追加（その後ユーザーが不要と決めて削除）を、WBS の変更の記録に残した）。`start-plan.md` への案6件は未承認。
- ユーザーが M1 の一部を確認した: 「両方」は選択肢に入れない、既存の理解ガイドの更新は対象外、`find-knowledge` の `guides/` 対応は不要。ユーザーの選択は「設計に進む」（計画で止めない）。`workflow-kit/` は書き換えていない。
