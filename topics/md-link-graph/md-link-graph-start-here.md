# 窓口: md-link-graph

- 型: Project 型。完了条件: 「ルールが見つかりにくい構造」（root の Next Actions 9）について、構造の問題点を数字で示し、直す案を1つ以上、ユーザーが決める。
- 何の取り組みか: Markdown の参照を呼び出しグラフとして見て、深さ・入れ子・ハブ・循環・孤立を調べる。知識が作業の最中に届くか（索引、ノートの分け方、`AGENTS.md` への写し）の議論の材料にする。起点は 2026-10-20 の `.bat` の見落とし（root の `docs/log.md` 9）。

## いま

本実装と再測定は済み（2026-10-25）。次は引き当て率の初回（11-08）。

## あなた待ち

なし（2〜4 は 2026-10-25 に決定・実装済み）

## 次の一手

「md-link-graph の続き」で、`docs/log.md` の Next Actions を見る。11-08 以後なら 1（引き当て率の初回。どこでも）。

## 使い方

- 再生成: リポジトリのトップで `python -I topics/md-link-graph/tools/mdgraph.py`。出力は `records/graph.html`（1枚、外部通信なし。ブラウザで開く）。
- 場面ごとの到達: `python -I topics/md-link-graph/tools/mktriggers.py` で表を作り、`python -I topics/md-link-graph/tools/mdreach.py --table topics/md-link-graph/records/triggers-prototype.md`。場面は `records/scenarios.md`。`mdgraph.py` は `--kinds wiki md include tick` で辺の種類を絞れる。
- 数える辺: `[[wikilink]]`、`[](x.md)`、行頭の `@x.md`、バッククォート内の `x.md`。起点（`AGENTS.md` `README.md` `docs/log.md`）からの最短の深さ、強連結成分（循環）、入次数 0、未到達を出す。

## 読む順

1. `docs/log.md`（現在状態と論点。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）

## 触るもの

`exmem/lessons/` の全ノートの frontmatter に `triggers:`（作業の言葉）を足した。ここは本実装の前の試作。

## リポジトリに無いローカルの状態

なし
