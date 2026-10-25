# 作業ログ（log）

`md-link-graph`（Markdown の参照構造の可視化と論点整理）の現在状態と次にやること。経緯と計測の詳細は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。

## 状態

- 道具（`tools/`）: `mdgraph.py` が `records/graph.html` を作る（`--kinds` で辺の種類を絞れる）。`mdreach.py` が場面ごとの到達を数える（`--table` で作業の言葉の表を起点に足す）。`mktriggers.py` が lessons の `triggers:` から `records/triggers-prototype.md` を作る。使い方は窓口。
- 計測の要点（2026-10-25、189 ファイル、すべての辺）: 辺 1,461、最大の循環 167、起点から到達 177、入次数 0 が 7。バッククォートのパスも辺に数える（決定）。`decisions.md` と `log-history.md` は経路でなく引用の集まりで、通らなくても到達はほぼ変わらない。深さ・入次数は「届きやすさ」の指標にしない（決定）。
- 届きやすさの測り方（決定）: `records/scenarios.md` の場面（26 件。実際 3、案 23。pptx などに派生すれば増える）ごとに、起点（`AGENTS.md` `README.md` `docs/log.md`）から、作業の言葉が書かれた行のリンクだけを辿って、期待ノートに着くかを数える。
- 原因: 自動で読まれる起点に「作業の前に `exmem-index.md` を引く」の指示が無い（`exmem/AGENTS.md` にあるが、cwd が `exmem/` のときだけ読まれる）。今の構造は前提にしない。
- 試作の結果: 全 67 本の lesson に `triggers:`（作業の言葉。15 語まで。同義語を含む）を付け、表を毎回読む前提で測ると、届かない場面は 20/26（表なし）から 1/26（S11＝`exmem/AGENTS.md` の規則）になった。測定は盲検でない（語も場面も同じ AI が書いた）。本当の確認は、実際の作業での引き当て率。
- 未確認: 大きいノート（`ai-isolated-work-room`、`obsidian-vault`、`workflow-kit` など）の `triggers` は、本文を読まず、題・別名・タグから書いた。語彙の抜けは気づいたときに直す。
- 表は 11KB（約 4,000 トークン）で、毎回読ませるには重い。

## Next Actions

0. 実装済み（2026-10-25、未コミット）: `find_knowledge.py` に `--triggers` `--check-triggers` `--list-triggers`、`guides/explain/` 9 本に付与、`check_inbox` の点検、`stock` `integrate` と見本・inbox README・`exmem/AGENTS.md`・root `AGENTS.md` の記述。人用の理解ガイドの下書き（`exmem/inbox/2026-10-25-triggers-knowledge-index.md`、未追跡のまま）。残りは dotfiles のフック（下の 1-3）と、実作業での引き当て率の確認（2）。設計は `records/design-triggers.md`。
1. 本実装の設計（下は元の論点。1-1・1-2・1-4 の一部と 1-5 は 0 で済み）:
  1. 表の大きさの扱い: 言葉の索引（言葉 → ノートの 1 行ずつ）にして、依頼文や拡張子から行を引く検索スクリプトにする、など。
  2. 起点の `AGENTS.md` への 1 行の入口（「作業の前に、作業の言葉を表で引く」。root `AGENTS.md` の変更。承認が要る）。
  3. 押し出し型のフック（dotfiles 側。編集するファイルの拡張子や依頼文の言葉を表と照合し、該当ルールの要点を作業中の AI に出す。このリポジトリには表と点検だけを置く）。
  4. 索引（`exmem-index.md`）を `triggers:` や題から自動で生成する。`triggers:` の書き方の規則（15 語まで、同義語を含む）を `exmem/AGENTS.md` に写す。
  5. S11 の扱い（`AGENTS.md` や kit の規則にも `triggers` を付けるか）。
2. 盲検に近い再測定: 場面を、`triggers` を見ずに追加して測る（ユーザーが書く場面を足すと確かさが上がる）。実機の確認（フック導入後）は、場面の依頼を新しいセッションで出して、読んだファイルを見る。
3. 論点 C（未到達と入次数 0 の扱い。窓口の `README.md` を起点から見えるようにするか）は、上の入口を決めた後に見直す。
4. 定期の見直しの頻度と指標（案: `review` の入力に、場面の届かない件数・最大の循環の割合・未到達・入次数 0 の件数を足す。決めるまで足さない）。

## 論点（Open Questions）

- A: 決定済み（バッククォートも数える）。B: 計測済み（`decisions.md` と `log-history.md` は経路でなく引用の集まり）。D: 方針は決定済み、本実装は上の Next Actions 1。
- C. 未到達 12 件と入次数 0 の 7 件の扱い（起点を増やすか、リンクを足すか、そのままでよいか）。
