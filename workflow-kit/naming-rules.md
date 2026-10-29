# ファイル名の規則

ファイルを作る・改名する前に読む。読み手は主に AI（Glob・Grep・`[[リンク]]` で引く）。2026-10-29 ユーザーの決定。根拠と実測は `docs/decisions.md` の同日の項。

## 適用の範囲

これから作るファイルに当てる。既存のファイルは、規則に反していても、触るついでに直すまで改名しない（`[[リンク]]` と本文中のパスの付け替えが要るため）。例外は、一意の規則に反する重複で、見つけたら直す。

## 規則

1. **文字種**: 英小文字・数字・`-`（kebab-case）。`.md`、ps1、ディレクトリに適用する。例外は 3 つ。①固定名（`README.md` `AGENTS.md` `CLAUDE.md`、`.gitignore` など）。②Python は snake_case（`-` は import できないため）。対の ps1 は kebab（`find_knowledge.py` ↔ `find-knowledge.ps1`）。③外部ツールが決める名前（`pyproject.toml` `uv.lock`）。
2. **一意**: ファイル名（拡張子を除く）はリポジトリ内で一意にする（wikilink が最短パスで解決されるため）。作る前に `git ls-files | grep '/<名前>\.md$'` が空であることを確かめる。重ねてよいのは、役割で決まる名前（`README` `AGENTS` `CLAUDE` `log` `decisions` `log-history` `due`）だけで、これらは `[[log]]` のように裸で指さず、パスで書く。衝突したら、あとから作る側に置き場や種別の語を足す（例: `ai-room-data-layout` と `ai-room-data-layout-explain`）。
3. **語の並び**: 主題を先、種別を後（`<主題>-<中身>-<種別語>`）。前方一致の Glob（`ai-room-*`）で同じ主題がまとまるため。名前だけで主題が分かること。ディレクトリ名を当てにした 1 語（`proposal` `draft` `run1`）にしない。目安は 2〜5 語。
4. **種別の語**: 末尾の種別の語は下の表から選ぶ。表に無い語が要るときは、表に足してから使う（タグの `tags.md` と同じ運用）。

   | 語 | 意味 | 置き場 |
   |---|---|---|
   | `-start-here` | トピックの窓口 | `topics/<名前>/` |
   | `-index` | 区分の索引 | 各区分の直下 |
   | `-output` | <やり方> の出力の型 | `exmem/lessons/` |
   | `-record` | 品質チェック・振り返りの記録 | `topics/kit-growth/records/` |
   | `-log` | lesson の節を移した記録（`<lesson 名>-log`） | `logbook/` |
   | `-explain` | 理解ガイドが `exmem/lessons/` の同名のノートと重なるときの区別 | `guides/explain/` |
   | `-rules` | 手順書が従う規則 | `workflow-kit/` |
   | `-hook` | 合言葉の手順書 | `workflow-kit/` |

5. **日付**: `YYYY-MM-DD-` の接頭辞は、時点の記録（`records/`）だけに付ける。知識（`exmem/lessons/` `guides/`）と規則には付けない。日付の後に主題の語を 1 つ以上置き、日付を除いても名前として成り立たせる（`2026-10-26-logbook-proposal`。`2026-10-26-proposal` は不可）。
6. **版**: 名前に入れず、上書きして履歴は git に任せる。旧版と新版を並べる必要があるときだけ `-v2` を付ける。名前の一部になっている `-2`（`research-method-2`）は残す。
