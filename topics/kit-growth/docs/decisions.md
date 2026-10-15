# kit-growth: 決定

## 2026-10-15（ユーザーの合意。経緯は [[kit-growth-handover]]）

- 【汎用】改善の受け皿は workbase の `topics/` に置く。理由: モバイルと PC2 の両方から届く。PC2 の works には置かない。
- 【汎用】workbase の改善を Area 型のトピック（`topics/kit-growth/`）にし、壁打ちで出た印象は inbox に入れる。育った話は Project 型の子トピックに切り出し、PC2 で直して close する。
- 【汎用】今の仕組み（トピックの docs 型、open / close、review）を流用して改善の経路をつなぐ。足すより畳む。
- 【汎用】`improvements.md` は追記をやめて凍結する。`hook-common.md` の「改善」の「1行足す」は、「`topics/kit-growth/docs/decisions.md` に書く」に変えた（2026-10-15 実施。ユーザーの依頼「取り込みたい」による）。
- 【汎用】`review` の入力に、トピックの置き場の点検（30日動かないトピック、終わったのに残るトピック、inbox の未選別）を足した（2026-10-15 実施）。

## 2026-10-15 improvement-methods を close した（出口の手順の最初の試行）

- 【この件】やり方集・取扱説明書・A/B とモードは `exmem/lessons/`（`problem-solving-methods` ほか、`user-manual`、`session-goal-modes`）と kit の `start-hook.md` に反映済みで、ディレクトリを削除した（履歴は git）。残りの「`start` のモードを試す」は、`docs/log.md` の Next Actions 2 へ移した。

## 2026-10-15 cwd（起動する場所）を明文化した（ユーザーがカードで5問を選択）

- 【汎用】Claude は `AGENTS.md` を置いた単位（リポジトリ・Project・Area）で起動する。上の階層で「<名前> の続き」と言われたら、AI がその単位の `AGENTS.md` を読みに行く（起動し直しを勧める案は、クラウドとモバイルで使えないので却下）。`hooks.md` の契約に「起動する場所（cwd）」の節。
- 【汎用】開始時に読む順番を、トピックと同じ「窓口 → `docs/log.md`」にそろえた（`docs-rules.md`、`templates/AGENTS.md`）。`decisions.md` は決める前に検索。雛形を変えた理由: 引き継ぎの読み込みを最小にする（topic-workflow の Q6）。既存の各ディレクトリの `AGENTS.md` は書き換えていない。
- 【汎用】AI 作業部屋は例外として文書だけで書く（`room-context.md`）。`ai/AGENTS.md` を作る案は、部屋の動作確認中のため見送り。
- 【汎用】`wrap` の書き込み先の既定に、このセッションで作業した単位（起動した単位、または「続き」で読みに行った単位）の `docs/` を加えた。

## 2026-10-15 improvements.md を指す残りの記述を向け直した

- 【この件】`workflow-kit/AGENTS.md` と `examples/` の2つの見本で、記録先を `improvements.md` から `topics/kit-growth/docs/decisions.md` に変えた（ユーザーの承認）。`wrap-hook.md` の自動採用の手順は、2026-11-08 の判定で節ごと畳む想定なので残した。
