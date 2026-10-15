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

## 2026-10-15 会話を「切る」と出力を「絞る」の対応を入れた（ユーザーが対応案から選択。経緯は exmem の `lessons/improvement-coverage-matrix.md`）

- 【汎用】`wrap` の報告の型に「次の会話への依頼文」を足した。この会話はここで切り、`--resume` で続けず、新しい会話に貼る3行の下書きを出す。`start` の契機にも、再開は新しい会話で始めることを書いた。
- 【汎用】`wrap` の自動採用の仕組み（「自動採用の範囲」「自動採用の規則」の2節）を、2026-11-08 の判定を待たずに畳んだ（ユーザーの選択）。kit の書き換えの例外は無くなった（`workflow-kit/AGENTS.md`、`hook-common.md`、`review-hook.md` の手順「自動採用の規則」も削除）。規則 `R-20261008-1`（並行セッションの変更の混入を防ぐ）の中身は、`docs-rules.md` の「コミットの前に確認する」①（ステージの行数を見て、自分の変更だけに絞る）が担う。
- 【汎用】`docs-rules.md` に「読み方の共通ルール」（大きいファイルは節だけ、出力は絞ってから、スクリプトは要約と件数）を、`exmem/AGENTS.md` の読む順番に「10KB 超のノートは節だけ」を足した。
- 【汎用】`review` の入力に「重い会話」（入力の最大トークンが大きい会話を上位1〜2件）を足した。集計は呼び出し元にあるときだけ。
- 【汎用】`find-knowledge.ps1` は、ファイルの大きさ（KB）と、ヒットした見出しの節の行の範囲を返す。`check-inbox.ps1` は、既定で PASS の行を出さない（`-ShowPass` で出す）。
- 【この件】見送り: 雛形の workspace `AGENTS.md` の読む順番の修正（影響が大。既存のワークスペースを手で直す必要がある）、切る目安の数値、`lessons/` の字数の目安。
