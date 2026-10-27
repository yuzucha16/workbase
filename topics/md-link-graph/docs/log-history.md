# 経緯（log-history）

## Log

### 2026-10-28（wrap の新しい規則で log.md を掃除）
- `wrap` の新しい規則で、済んだ部分を移した。NA3: 道具（`mdgraph.py` `mdreach.py` `mdrank.py`）と場面の一覧を kit へ移した（10-27。`mktriggers.py` は `mdreach.py --table` に統合、`graph.html` と `triggers-prototype.md` は都度生成にして削除）。
### 2026-10-25（実機なしでできる分: 盲検に近い再測定、論点 C、索引の自動生成の案）
- ユーザーの依頼「MD-link-graph の続き、実機なしでできるアイテム」。Next Actions のうち、1（11-08 の引き当て率）と 6（完了の判断）は日付待ち、5 は方針どおり何もしない。実機（PC1/PC2）が要る項目は、このトピックには無い（dotfiles `42c7c6a` の push は dotfiles 側の作業）。
- 2: `triggers` を読まずに依頼文 18 件（B01〜B18）を書き、本番の `find_knowledge.py --triggers` で引いた。上位 5 件 17/18、1 位 12/18。取りこぼし B07。S01〜S26 を依頼の文で引くと S16 が 6 位（`Zed` の 1 語で同点）。IDF の重みの試算は悪くなった。
- 3・4: `mdgraph.py` で再計測（178 ファイル、未到達 6 = 入次数 0 の 6）。6 件の中身と案、`exmem-index.md` のずれ（67/67、title と違う行 9）を `records/c-and-index-proposal.md` にまとめた。どちらもユーザーの判断待ち。
- 窓口の「いま」「次の一手」が本実装の前のままだったので直した。
- ユーザーの質問で、dotfiles のフックの push を dotfiles 側の AI に頼むプロンプトを渡した（範囲の確認、`docs-rules.md` の push 1〜5、履歴のユーザー名の件は別作業）。
- ユーザーの指摘で、`review` の入力 9 をこのトピックの測り方と同じにした（`graph.html` の作り直し、未到達の名前、`mdrank.py`、場面の追加。root の `decisions.md` の同日の項）。記録に未到達のパスを書くと未到達が 0 に見える落とし穴に当たり、記録ではパスを囲まないことにした。

### 2026-10-25（本実装: 言葉の索引、dotfiles のフック、review の定期チェック）
- ユーザーが案 1（言葉の索引を検索スクリプトで引く）を選び、「stock ナレッジ」「integrate」にも索引が作られるか、既存は今・これからのナレッジはどこで索引化されるかをまとめて設計するよう依頼。設計案（`records/design-triggers.md`）を出し、3 点（表をコミットしない、`guides/explain/` を含める、`stock` で必須・`integrate` で合わせる）をユーザーが承認。
- 実装（`b49b65e`）: `find_knowledge.py` に `--triggers` `--check-triggers` `--list-triggers`、`guides/explain/` 9 本と `exmem/inbox/` 3 本に付与、`check_inbox` に `triggers` の点検、`stock` `integrate` の手順書と見本、root `AGENTS.md` と `exmem/AGENTS.md`。人用の表は `stock 理解` の下書き（`exmem/inbox/2026-10-25-triggers-knowledge-index.md`、未追跡）にし、表自体は `--list-triggers` で毎回出す形にした。
- dotfiles のフック: `triggers_hook.py`（`80f15e5`）と dotfiles `home/.claude/settings.json` の `UserPromptSubmit`（`42c7c6a`）。`workbase` が無い PC で依頼が止まらないよう `Test-Path` で守る。このセッション内で発火を確認（出力は文脈に入る）。
- `review` の入力 9（`4e1250d`）: 引当率（`triggers_stats.py`。会話記録のフック出力と、その依頼で読まれたファイルを突き合わせる）とコールグラフ。初日の記録は 1 依頼で 0/5（依頼が `review` の話で、ノイズの可能性）。初回の本測定は 11-08。
- `log.md` が 4KB の予算を超えていたため、現在状態だけに書き直した。

### 2026-10-25（論点 A〜D の計測と、`triggers:` の全 lesson への付与）
- グラフが空だった不具合を直した（`const top` が `window.top` と衝突。`topN` に改名）。ユーザーが表示を確認。
- 論点 A（`--kinds` で辺の種類を絞る。189 ファイル）: wikilink のみ（辺 544、起点から到達 3、最大の循環 61、入次数 0 が 72）、バッククォートのみ（927、118、97、53）、すべて（1,461、177、167、7）。起点に wikilink が無く、パスはバッククォートで書いてあるため、AI の到達を見るにはバッククォートを数える。ユーザーが決定（`decisions.md`）。
- 論点 B: `decisions.md`（出次数 83）と `log-history.md`（75）は、経緯の引用の集まりで、到達の経路ではない（この 2 つを通らなくても到達 177 件が 175 件。さらに `exmem-index.md` も通らないと 173 件。lessons 67 件のうち届かなくなるのは 1 件）。
- 論点 D: 深さ・入次数は「名前がある」しか測れない。場面（作業の言葉と期待ノート）ごとに、起点から、言葉が書かれた行のリンクだけを辿る到達を測る（`tools/mdreach.py`、場面は `records/scenarios.md`）。ユーザーが場面を承認（今後 pptx などに広げれば場面は増える）。初回（12 件）: 届かない 8/12。原因は、自動で読まれる起点に「作業の前に `exmem-index.md` を引く」の指示が無いこと（`exmem/AGENTS.md` にあるが、cwd が `exmem/` のときだけ読まれる）。
- ユーザーの方針: 今の構造は前提にしない。`exmem/lessons/` へのたどり方を構造レベルで変えてよい。一時的な修正でなく抜本的な改善。→ `triggers:` と押し出し型の方向で試作することを承認（`decisions.md`）。
- 試作: lessons 8 本に `triggers:` → 表（`tools/mktriggers.py`）→ 届かない 8/12 が 2/12。場面を 26 件に増やすと、表なし 20/26、8 本のみ 13/26、18 本で 5/26（語彙の穴 S14 を同義語で直して 4/26）、67 本で 1/26（S11＝`exmem/AGENTS.md` の規則）。
- ユーザーが `triggers` の質・量を了承し、1 本 15 語までに決めた。全 67 本に付与（AI の下書き。大きいノートは本文を読まず、題・別名・タグから）。測定は盲検でない（語も場面も同じ AI が書いた）。
- 表は 11KB（約 4,000 トークン）で、毎回読ませるには重い。

- 2026-10-25: root の `review 消化` で Next Actions 9 に着手すると決め、トピックを立てた。`tools/mdgraph.py` で初回の計測と `records/graph.html` を作った（結果は `docs/log.md`）。
