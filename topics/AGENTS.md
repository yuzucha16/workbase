# AGENTS.md（topics）

大きな取り組み（トピック）の置き場。入口は `topics-index.md`。

## 「<トピック名> の続き」と言われたら

`workflow-kit/docs-rules.md` の「上の階層で起動して…」の節（24 行付近の 3 行。`offset` 24・`limit` 5 で読む。Grep と全文読みはしない）に従う。トピックでの差分は、窓口が `*-start-here.md`（無ければ `*-handover.md`）であることと、`notes/` は必要なときだけ読むこと。

## 書くとき

- 窓口は `workflow-kit/templates/topic/start-here.template.md` から作る。
- 状態は `docs/log.md` だけに置く（窓口には「いま」の1行だけ。ほかに写さない）。予算: 窓口 2KB、`log.md` 4KB。
- 例外: `kit-growth/`（Area 型）は `docs/` を持たない。kit の改善の状態・決定・経緯は workbase 直下の `docs/` に置く（2026-10-18。窓口と docs の置き場は別の論点）。
- Claude Projects の共有フォルダは議論の下書きの置き場。確定したらトピックへ移す。
- トピック固有の Next Actions は、トピックの `docs/log.md` だけに置く。リポジトリ直下の `docs/log.md` に同じ項目を写さない（二重管理になる。2026-10-29）。期日は直下の表に置く。
- 決定は `docs/decisions.md`（ユーザーの発言を根拠に）。経緯は `docs/log-history.md`。
- 次の会話への依頼は「<トピック名> の続き」の1行（状態は窓口と `log.md` が持つ）。
- **題材ごとのトピックと `records/` の仕訳**（2026-10-25 に正式化。正本は workbase 直下 `docs/decisions.md` の同日の項）: 計画のやり方の題材は `topics/<名前>/`（kebab-case、1階層）に、窓口・`docs/`・`records/` の同じ構造で置く。`records/` は2か所だけ: `kit-growth/records/` は測ったこと（品質チェックと振り返り）、各トピックの `records/` はそのトピック自身の出力（計画・見本・確認メモ）。`kit-growth/plans/` は使わない。
- 反映が済んだトピックは、下の「トピックを終わらせるとき」に従って削除する（履歴は git）。

## トピックを終わらせるとき

ユーザーが言ったときだけ行う。手順は `close-procedure.md`（言われたときだけ読む。ふだんは読まない）。Area 型のトピックは消さない。
