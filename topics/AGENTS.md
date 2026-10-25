# AGENTS.md（topics）

大きな取り組み（トピック）の置き場。入口は `topics-index.md`。

## 「<トピック名> の続き」と言われたら

`workflow-kit/docs-rules.md` の「上の階層で起動して…」に従う。トピックでの差分は、窓口が `*-start-here.md`（無ければ `*-handover.md`）であることと、`notes/` は必要なときだけ読むこと。

## 書くとき

- 窓口は `workflow-kit/templates/topic/start-here.template.md` から作る。- 状態は `docs/log.md` だけに置く（窓口には「いま」の1行だけ。ほかに写さない）。予算: 窓口 2KB、`log.md` 4KB。
- 例外: `kit-growth/`（Area 型）は `docs/` を持たない。kit の改善の状態・決定・経緯は workbase 直下の `docs/` に置く（2026-10-18。窓口と docs の置き場は別の論点）。
- Claude Projects の共有フォルダは議論の下書きの置き場。確定したらトピックへ移す。
- 決定は `docs/decisions.md`（ユーザーの発言を根拠に）。経緯は `docs/log-history.md`。
- 次の会話への依頼は「<トピック名> の続き」の1行（状態は窓口と `log.md` が持つ）。
- **題材ごとのトピックと `records/` の仕訳**（2026-10-25 に正式化。正本は workbase 直下 `docs/decisions.md` の同日の項）: 計画のやり方の題材は `topics/<名前>/`（kebab-case、1階層）に、窓口・`docs/`・`records/` の同じ構造で置く。`records/` は2か所だけ: `kit-growth/records/` は測ったこと（品質チェックと振り返り）、各トピックの `records/` はそのトピック自身の出力（計画・見本・確認メモ）。`kit-growth/plans/` は使わない。
- 反映が済んだトピックは、下の「トピックを終わらせるとき」に従って削除する（履歴は git）。

## トピックを終わらせるとき

ユーザーが言ったときだけ行う。完了条件の確認、暫定の決定の見直し、未解決の整理は、`review 消化` と `docs/log.md` の Next Actions / Open Questions で行う（専用の手順は持たない）。Area 型のトピックは消さない。

0. 閉じる・完了と判断する前に、トピックの `docs/log.md` の状態表と、上位（root）の `docs/log-history.md` の最新の経緯を突き合わせ、食い違いと結果を報告に書く（古い側で断定しない）。
1. `docs/decisions.md` の【汎用】が `exmem/lessons/`、kit、`guides/` に反映済みか見る（見るだけ。反映するかの判断はユーザー）。行き先は内容の種類で決める: 設計と理由は `guides/explain/`、決定は `docs/decisions.md`、仕様は実装の隣、原則は `exmem/lessons/`、経緯は git。移し終えたノートは元を削除する（二重管理を残さない）。実装前の設計を移すときは、未実装の部分に「未実装」と注記する。残件は上位の Next Actions に移す（2026-10-19 承認）。
1a. 消す前の条件（2026-10-21 ユーザーの決定。`usage-viz` で実施）: `stock`（知識の反映）と `wrap`（記録）が済んでいること。`wrap` で、トピックの `docs/decisions.md` の【この件】の決定を、root の `docs/decisions.md` に1項にまとめて移す（根拠はユーザーの発言のまま。【汎用】は手順1の行き先へ）。経緯は root の `docs/log-history.md` に追記し、root の `docs/log.md` の該当行を直す。未確認のことは root の `log.md` に1行残す。
1b. `records/`（計画・見本・確認メモ）は移さず、ディレクトリごと削除する（履歴は git。実行後のフィードバックは `brief-plan.md` などに反映済みであること）。`kit-growth/records/` へ移すのは「測ったこと」だけで、閉じたトピックの出力は移さない。
2. ディレクトリを削除し、`topics-index.md` の行を消す。窓口や他のノートの言及（`planning-method` の窓口など）も直す。
3. 残ったファイルに、消えたノートへの `[[リンク]]` が無いか、grep で確かめる。
4. 記録は `wrap` に任せる。
