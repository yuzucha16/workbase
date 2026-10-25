# 作業ログ（log）

`md-link-graph`（Markdown の参照構造の可視化と、知識の引き当て）の現在状態と次にやること。経緯と計測の詳細は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、設計は `records/design-triggers.md`。

## 状態

- 本実装は済み（2026-10-25）。索引の正本は各ノートの `triggers:`（15 語まで）。表はコミットせず、`workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"` が毎回 frontmatter を読む（`--check-triggers` `--list-triggers` もある）。対象は `exmem/lessons/`、`guides/explain/`、未統合の `exmem/inbox/`。
- 付く時点: 既存は付与済み（lessons 67、explain 9、inbox 3）。`stock` はメモに必須（`check_inbox` が点検）、`integrate` は統合先に合わせて 15 語に収める。入口は root `AGENTS.md` の 1 節と `exmem/AGENTS.md`。
- 押し出し: dotfiles の `UserPromptSubmit` フックが `workflow-kit/tools/triggers_hook.py` を呼ぶ（dotfiles `42c7c6a`、未 push）。このセッションで発火を確認した。
- 定期チェック: `review` の入力 9（引当率 = `triggers_stats.py`、コールグラフ = `mdgraph.py` `mdreach.py` `mktriggers.py`）。
- 計測の数字（2026-10-25）: 辺 1,585、最大の循環 88%（170/193）、未到達 14、入次数 0 が 9、届かない場面 1/26（S11）。測定は盲検でない（語も場面も同じ AI が書いた）。
- 未確認: 大きいノートの `triggers` は本文を読まず、題・別名・タグから書いた。

## Next Actions

1. 実作業での引き当て率: 初回は 2026-11-08（root `docs/log.md` の期日）。`python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。以後は `review` の入力 9。取りこぼしは `triggers:` の語を足す案にする。初日は 1 依頼だけで、判断できない。
2. 盲検に近い再測定: 場面を `triggers` を見ずに追加して測る（ユーザーが場面を足すと確かさが上がる）。
3. 論点 C（未到達と入次数 0 の扱い。窓口の `README.md` を起点から見えるようにするか）を見直す。
4. 索引（`exmem-index.md`）を `triggers:` や題から自動生成する案（別の論点。未決）。
5. S11（`AGENTS.md` や kit の規則にも `triggers` を付けるか）は、入口 1 節とフックで届くので付けない方針。実測で届かなければ見直す。
6. 完了の判断: 完了条件（構造の問題点を数字で示し、直す案をユーザーが決める）は満たした。引き当て率の初回（11-08）の後に、閉じるかをユーザーに聞く。閉じるときは、`mdgraph.py` `mdreach.py` `mktriggers.py` と `records/scenarios.md` を kit に移し、`review-hook.md` の入力 9 のコマンドを直す。

## 論点（Open Questions）

- C. 未到達 14 件と入次数 0 の 9 件の扱い（起点を増やすか、リンクを足すか、そのままでよいか）。
