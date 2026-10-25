# 作業ログの経緯（log-history）

## Log

### 2026-10-25（`env/` だけ・`tests/` だけ・`docs/` だけの実測と、置き場の取り違えの修正）
ユーザーが手元で 3 本を作り、AI の質問と成果物を見て手順書を直した。`sample_devenv`(Ubuntu 24.04 実機で ENV-001〜010 全件 PASS、SET-001 も中止を確認)、`sample_devtest`(要求 14 ID に対応、65 件実行で不具合 3 件と仕様の曖昧さ 2 件。`ai/in/` は不変)、`sample_devdoc`(骨子と図の要否を聞いた。基準文書の形を仮決め)。置き場の取り違えが 5 回(`work/`、`deliverable/` 3 回、README、レビュー版を `ai/docs/`)。部屋の AI に読んだ手順書を聞き、原因は `ROOM.md`/`room-context.md` の「人が読む最終版は `deliverable/`」と、`project-structure.md` を読んでいないことと分かった。直した(単体テスト 139 件 OK)。旧名の説明の削除、`dev` の「テスト」に文書と実装の整合の検査の型、`brief-work-types.md` に `project-structure.md` を読む指示も同日。決定は `decisions.md`。確認待ちは、直した `ROOM.md` で次の `dev` が取り違えないか。

### 2026-10-25（最初の実利用の観察を受けた手順書の修正）

`sample_dev`（`src/ env/ tests/ tools/ docs/` の CLI）と `sample_inv`（Obsidian の wikilink の調査）で観察した。両方で出た指摘を直した: `room open` が `docs/` の 3 つの雛形を置く（テスト 123 件合格）、`ai/X` の読み替え（`room-context.md`）、`docs/` の中身を 3 つに揃える（`project-structure.md`）、先に全部渡されたときの要約の省略（`brief-hook.md`）、ユーザーが書いた完了条件の扱い（`room-context.md`）。`dev` 側は、構成要素の聞き方（`brief-work-types.md`）、表の組み合わせ・環境要求の置き場（`dev-deliverable-guide.md`）。`ai-room-why.md` の `start` の記述を `brief` の改名に合わせた。残件は `log.md`。

### 2026-10-24（続き: type の考え方を記載）
- ユーザーが、考え方・方針は叩き台で十分と判断。`project-structure.md` の冒頭に節「type の考え方」を置いた。前回の `project-structure.md` に重複が混入していたのを直した（原因: 文字列置換で、先に出る同じ語に当たった。置換後に見出しと行数を確認していなかった）。

### 2026-10-24（続き: guide の見直し）
- `dev-deliverable-guide.md` の不整合 7 件の叩き台を出し、ユーザーが論点 1〜5、活動の表の程度、`script-guide.md` の名前に OK。実装して反映した（決定は root の `decisions.md`）。ユーザーが、「方針の文書が無い」と指摘し、Next Actions に起票。

### 2026-10-24
- ユーザーの依頼で議論を開始。`room.py` は type を読まず、違いは手順書だけと確認し、叩き台（事実の表、論点8件）を出した。ユーザーが別セッションの分類（investigation と development）を持ち込み、2 type 案に改訂。新値は `dev` と `inv`、既定は `dev`、旧値は受け付けない、曖昧な例は成果物の名前で決める、で承認。同日に実装して反映した（`decisions.md` は root の同日の項）。
