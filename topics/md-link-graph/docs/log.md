# 作業ログ（log）

`md-link-graph`（Markdown の参照構造の可視化と、知識の引き当て）の現在状態と次にやること。経緯と計測の詳細は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、設計は `records/design-triggers.md`。

## 状態

- 本実装は済み（2026-10-25）。索引の正本は各ノートの `triggers:`（15 語まで）。表はコミットせず、`workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"` が毎回 frontmatter を読む（`--check-triggers` `--list-triggers` もある）。対象は `exmem/lessons/`、`guides/explain/`、未統合の `exmem/inbox/`。
- 付く時点: 既存は付与済み（lessons 67、explain 9、inbox 3）。`stock` はメモに必須（`check_inbox` が点検）、`integrate` は統合先に合わせて 15 語に収める。入口は root `AGENTS.md` の 1 節と `exmem/AGENTS.md`。
- 押し出し: dotfiles の `UserPromptSubmit` フックが `workflow-kit/tools/triggers_hook.py` を呼ぶ（dotfiles `42c7c6a`、未 push。push はユーザーが dotfiles 側の AI に頼む。2026-10-25 にプロンプトを渡した）。発火は確認済み。
- 定期チェック: `review` の入力 9（引当率 = `triggers_stats.py`、コールグラフ = `mdgraph.py` `mdreach.py` `mktriggers.py`、依頼の文での順位 = `mdrank.py`。`graph.html` の作り直しと場面の追加も含む。2026-10-25 にトピックと同じ測り方にした）。
- 計測の数字（2026-10-25 の再計測）: 167 ファイル、辺 1,490、最大の循環 95%（158/167）、未到達 0、入次数 0 が 0（雛形と shim を数えない定義に変えた後。前は 6 件）、届かない場面 1/26（S11。語の列で測った数）、依頼の文での順位（`mdrank.py`）1 位 30/43、上位 5 件 40/43。
- 盲検に近い再測定（`records/scenarios.md` の B01〜B18。`triggers` を読まずに書いた依頼文を、本番の `--triggers` で引いた）: 上位 5 件 17/18、1 位 12/18。S01〜S26 を依頼の文で引くと 1 位 17/24、上位 5 件の外は S16 だけ。並べ方を IDF に変える試算は悪くなった（変えない）。
- 未確認: 大きいノートの `triggers` は本文を読まず、題・別名・タグから書いた。

## Next Actions

1. 実作業での引き当て率: 初回は 2026-11-08（root `docs/log.md` の期日）。`python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。以後は `review` の入力 9。取りこぼしは `triggers:` の語を足す案にする。初日は 1 依頼だけで、判断できない。
2. （見送り・閉じた。2026-10-25 ユーザー: 対象のノートはそんなに重要ではなかった。B07 `linux-multiboot-setup` と S16 `zed-vim` の語は足さない）
3. （済み。2026-10-25）`mdgraph.py` は雛形と `@` だけの `CLAUDE.md` を数えない。root `README.md` に topics と guides の窓口を書いた。未到達 0、入次数 0 が 0。
4. （済み。2026-10-25）索引は生成せず、`find_knowledge.py --check-index` を `integrate` の最後と `review` の入力 9 に足した。
5. S11（`AGENTS.md` や kit の規則にも `triggers` を付けるか）は、入口 1 節とフックで届くので付けない方針。実測で届かなければ見直す。
6. 完了の判断: 完了条件（構造の問題点を数字で示し、直す案をユーザーが決める）は満たした。引き当て率の初回（11-08）の後に、閉じるかをユーザーに聞く。閉じるときは、`mdgraph.py` `mdreach.py` `mktriggers.py` `mdrank.py` と `records/scenarios.md` `records/graph.html` を kit に移し、`review-hook.md` の入力 9 のコマンドを直す。

## 論点（Open Questions）

- なし（論点 C は 2026-10-25 に解決）。
