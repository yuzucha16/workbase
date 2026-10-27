# 本実装の設計案: 作業の言葉の索引（2026-10-25。案 1。未承認）

## 方針

- 正本は各ノートの frontmatter の `triggers:`（30 語まで、同義語を含む）。表は**コミットしない**。検索スクリプトが、実行のたびにノートの frontmatter を直接読む（ノート数は 76 本。十分速い）。生成物が無いので、古くならない。
- 返すのは当たった行だけ（既定で上位 5 件）。毎回読むものは `AGENTS.md` の 1 行だけになり、表の 11KB 問題が消える。
- 検索スクリプトは新設せず、既存の `workflow-kit/tools/find_knowledge.py` に `--triggers "<依頼文や語>"` を足す。依頼文に `triggers` の語が部分一致で含まれるノートを、一致した語つきで出す。`exmem/inbox/` の未統合メモも対象にして「未統合」と印を付ける（作った直後の知識も届く）。
- 対象: `exmem/lessons/`（AI 用）と `guides/explain/`（理解ガイド。`integrate` が同じ流れで作るため）。

## 既存のナレッジ（今作る）

| 対象 | 状態 | やること |
|---|---|---|
| `exmem/lessons/` 67 本 | `triggers:` 付与済み（試作） | 変更なし。語彙は気づいたときに直す |
| `guides/explain/` 9 本 | 未付与 | 同じ規則で付与する |

## これから作られるナレッジ（どこで索引化されるか）

索引は「別に作る表」ではなく、ノートの `triggers:` そのもの。付与は作る工程の中で行う。

| 工程 | 索引に関わること | 変更先（要承認） |
|---|---|---|
| `stock ナレッジ` / `stock 理解` | メモの frontmatter に `triggers:` を必須で書く（書き手が作業の言葉を一番知っている）。`check_inbox.py` が、無い・16 語以上を FAIL にする。書いた直後から、検索は未統合メモも引く | `stock-hook.md`（frontmatter・自己点検）、`check_inbox.py` / `.ps1`、`examples/inbox-example.md`、`exmem/inbox/README.md` |
| `integrate` | 統合先が既存の lesson: メモの語を足して合わせ、30 語を超えたら弱い語を落とす（報告の「照合」に落とした語を載せる）。新規ファイル: メモの `triggers:` をそのまま引き継ぐ。`kind: explain` は、外す項目に `triggers` を入れない（残す）。最後に点検（全ノートに `triggers:` がある・30 語以内）を実行する | `integrate-hook.md`（細則 5・7、explain の変換）、`find_knowledge.py --check-triggers` |
| 人が直接編集 | 点検が見つける（`review` の入力に、`triggers:` の無いノートの件数を足す案は Next Actions 4） | — |

`exmem-index.md`（人向けの手書き索引）はそのまま。`triggers:` から自動生成する案は別の論点（Next Actions 1-4）として残す。

## 作業中に届ける仕組み

1. root `AGENTS.md` に 1 行（要承認）: 「作業を始める前に、依頼の言葉で `python -I workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"` を実行し、出たノートを読む」。
2. `exmem/AGENTS.md` の「読む順番」と「Frontmatter」に、`triggers:` の規則（30 語まで、同義語を含む、作業の言葉で書く）を写す（要承認）。
3. 押し出し型のフック（dotfiles 側。別のセッションで設計）: 依頼文の送信時に 2 のスクリプトを呼び、出力を AI に渡す。このリポジトリは、スクリプトと点検だけを持つ（依存は dotfiles → workbase の一方向）。
4. S11（`exmem/AGENTS.md` の規則）: 1 と 3 で届くので、`AGENTS.md` や kit の規則には `triggers:` を付けない。

## 順序

1. （承認不要・このトピック内）`guides/explain/` 9 本に付与、`find_knowledge.py --triggers` の試作を `tools/` に置いて到達を再測定。
2. 承認後: kit（stock・integrate・点検・見本）と `exmem/AGENTS.md`、root `AGENTS.md` を一度に変える。
3. dotfiles のフックは別途。実機の引き当て率は、導入後の実作業で測る。

## 承認してほしいこと

- 表をコミットせず、スクリプトが frontmatter を直接引く方式でよいか。
- 対象に `guides/explain/` を含めてよいか。
- `stock` で `triggers:` を必須にし、`integrate` で語を合わせる運用でよいか。
