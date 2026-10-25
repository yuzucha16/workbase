# review 入力 9: 知識の引き当てと参照構造の測り方

`review-hook.md` の入力 9 の詳細（2026-10-25 に本文から移した。2026-10-25 ユーザーの指示。設計は `topics/md-link-graph/records/design-triggers.md`）。workbase で実行したときに、次の2つを実行し、数字を前回と比べる（読むだけ。ノートは直さない）。

## 引当率

`python -I workflow-kit/tools/triggers_stats.py --since <前回の見直しの日付> --detail`

索引（`triggers_hook.py`）が出したノートが、同じ依頼の間に読まれた割合と、上位 1 件の割合、取りこぼし候補（知識ノートを読んだのに索引が出していなかったもの）を見る。取りこぼしは、読んだ理由を見て、`triggers:` に足す語を案にする（足すのは承認制。語の追加は「1つ直す」の枠に数える）。記録が無い（フック未導入の PC など）週は「記録が少ない」と報告し、結論を出さない。この数字は「読まれた」であって「使われた」ではない。

## 参照構造（コールグラフ）

`python -I topics/md-link-graph/tools/mdgraph.py --out <一時ファイル>`（ファイル数・辺・起点からの未到達・入次数 0・最大の循環の割合）と、`python -I topics/md-link-graph/tools/mktriggers.py` の後に `python -I topics/md-link-graph/tools/mdreach.py --table topics/md-link-graph/records/triggers-prototype.md`（場面のうち届かない件数）。

未到達と入次数 0 が増えた、最大の循環の割合が上がった、届かない場面が増えたときは、原因のノート（増えた分）を挙げ、リンクを足すか畳む案にする。`mktriggers.py` は `records/triggers-prototype.md` を作り直す（差分は見直しのコミットに含めてよい）。

トピック `md-link-graph` を閉じるときは、この3つの道具（`mdgraph.py` `mdreach.py` `mktriggers.py`）と `records/scenarios.md` を kit に移し、このコマンドを直す。

## 指標の見方

引当率が低いのは語の不足か、AI が出力を読んでいないかのどちらか。取りこぼしが多ければ語、出したのに読まれなければフックの出し方（件数・表示）を疑う。
