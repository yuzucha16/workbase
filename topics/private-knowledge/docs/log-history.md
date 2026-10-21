# 作業ログの経緯（log-history）

## Log

### 2026-10-21（Area を跨ぐ共有知の設計・実装・実機確認）
- 設計の軸をユーザーと決めた（決定 ⑧〜⑳）: 渡し方は Area から取り出してマスクした写しを `ai/in/` へ、選び方は「絞って人が確認」（仮案）、マスクは渡すとき、戻りは既存の `room close` → `ai/docs/inbox.md`、統合は Area に置き**部屋の作業**にする（works の AI が実名を読まない。deny は `Read`/`Edit` だけを止める安全網で、シェルは止まらない）。知識は3層（事実 = Area、部屋用の写し、一般化した教訓 = workbase。固有の事実は仮名にしても workbase に切り出さない）。会議録の型を承認（`records/meeting-note-example.md`）。
- `room.py` に `pull` と、`restore` の Area 書き出し（`ai/out/knowledge/` → `areas/<Area>/knowledge/`）を実装。設計からの差分を4つ承認（`knowledge_dest`、manifest に Area のファイル名を書かない、`status: active` だけ、上書きの扱い）。その後、上書きを警告から停止に変更（決定 ㉕）。単体テスト追加（`PullKnowledgeTest` 5件）。
- 実機の通し試験（ダミーの Area `pilot2`、`guides/howto/ai-room-setup-script.md` の 4.1・6.1）で、ユーザーが「すべて問題なし」と報告（`org:` の値の置換、部屋の AI の読み取り、人の変更を守る停止を含む。個別の数字は未記録）。
- 見えたこと: 設計の途中で、「Area を読める AI が統合する」案が部屋の目的（実名を AI に見せない）と衝突することに気づき、統合を部屋の作業に変えた。manifest が部屋の AI から見える点を読み落とすと、Area のファイル名（実名を含みうる）が漏れる所だった。

### 2026-10-21（計画の開始）
- `start 計画` で、会議録のナレッジ化を始めた。ユーザーの条件は「AI 向け（lessons）と私向け（explain）と同じ扱い・方針・ルール」。置き場、入力の形、「同じ」の範囲、2系統の扱い、顧客名の扱いを、4回のすり合わせで決めた（`docs/decisions.md`）。
- 6R・憲章・成果物 WBS・マイルストーン・作り方のメモを作った（[[private-knowledge-6r]]、[[private-knowledge-plan]]、[[private-knowledge-plan-notes]]）。トピックは `topics/private-knowledge/`、計画はその `records/`。最初は `topics/kit-growth/` の下と `plans/` に置き、次に `planning-method/records/` にそろえ、最後に `records/` を2か所（`kit-growth/records/` は測ったこと、各トピックの `records/` は自分の出力）にする決定で、ここに置いた（`docs/decisions.md`）。
- 見えたこと: 最初の案（Project の `ai/work` → `ai/in`）は、Project を跨げず寿命が狭いとユーザーが指摘した。2系統は手段で、論点は「読者の違う1つの情報の管理」だった。
