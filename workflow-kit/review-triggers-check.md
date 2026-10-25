# review 入力 9: 知識の引き当てと参照構造の測り方

`review-hook.md` の入力 9 の詳細（2026-10-25 に本文から移した。2026-10-25 ユーザーの指示。設計は `topics/md-link-graph/records/design-triggers.md`）。workbase で実行したときに、次の2つを実行し、数字を前回と比べる（ノートは直さない。書くのは、下の測定の出力と場面の追加だけ）。

## 引当率

`python -I workflow-kit/tools/triggers_stats.py --since <前回の見直しの日付> --detail`

索引（`triggers_hook.py`）が出したノートが、同じ依頼の間に読まれた割合と、上位 1 件の割合、取りこぼし候補（知識ノートを読んだのに索引が出していなかったもの）を見る。取りこぼしは、読んだ理由を見て、`triggers:` に足す語を案にする（足すのは承認制。語の追加は「1つ直す」の枠に数える）。記録が無い（フック未導入の PC など）週は「記録が少ない」と報告し、結論を出さない。この数字は「読まれた」であって「使われた」ではない。

## 参照構造（コールグラフ）

リポジトリのトップで、次の 4 つを実行する（2026-10-25 に、トピック `md-link-graph` での測り方と同じにした）。

1. `python -I topics/md-link-graph/tools/mdgraph.py`（雛形 `templates/` と、`@` だけの `CLAUDE.md` は数えない）: ファイル数・辺・起点からの未到達・入次数 0・最大の循環の割合と、未到達と入次数 0 のファイル名。`topics/md-link-graph/records/graph.html`（1 枚、外部通信なし）を作り直す。差分は見直しのコミットに含める。
2. `python -I topics/md-link-graph/tools/mktriggers.py` の後に `python -I topics/md-link-graph/tools/mdreach.py --table topics/md-link-graph/records/triggers-prototype.md`: 場面の「作業の言葉」の列で、起点から辿って届かない件数（`unreachable` 列）。`triggers-prototype.md` の差分もコミットに含めてよい。
3. `python -I topics/md-link-graph/tools/mdrank.py`: 場面の依頼の文（S 行と B 行）を本番の `find_knowledge.py --triggers` で引き、期待ノートが 1 位・上位 5 件に入った件数と、1 位でない場面（`scene_top1` `scene_top5` 列）。2 は「経路があるか」、3 は「本番で上に出るか」を見る。

4. `python -I workflow-kit/tools/find_knowledge.py --check-index`: 索引（`exmem-index.md`）の抜け・存在しない行・重複。FAIL は件数と名前を挙げ、直す案にする（説明文は手書きなので比べない）。

前回（`docs/metrics/reviews.csv` の最後の行）と比べる。未到達と入次数 0 が増えた、最大の循環の割合が上がった、届かない場面が増えた、1 位・上位 5 件が減ったときは、原因のノート（1 の名前の一覧、3 の 1 位でない場面）を挙げ、リンクを足す・畳む・`triggers:` に語を足す案にする（足すのは承認制）。

場面を足す（確かさを保つため）: 前回から `exmem/lessons/` か `guides/explain/` のノートが増えたら、そのノートの `triggers:` を読まずに、依頼の文を B 行として `topics/md-link-graph/records/scenarios.md` の「盲検に近い再測定」の表に 1 件以上足し、3 で測る。期待ノートはファイル名と題だけから選ぶ。

測るときの注意: 記録（トピックの `records/` や `docs/`）に、未到達のファイルのパスをバッククォートや wikilink で書くと、その記録からの辺として数えられ、未到達が減って見える（2026-10-25 に、論点 C の記録で 6 件が 0 件に見えた）。記録では、未到達のファイルのパスを囲まずに書く。

トピック `md-link-graph` を閉じるときは、この 4 つの道具（`mdgraph.py` `mdreach.py` `mktriggers.py` `mdrank.py`）と `records/scenarios.md` `records/graph.html` を kit に移し、このコマンドを直す。

## 指標の見方

引当率が低いのは語の不足か、AI が出力を読んでいないかのどちらか。取りこぼしが多ければ語、出したのに読まれなければフックの出し方（件数・表示）を疑う。
