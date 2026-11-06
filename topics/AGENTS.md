# AGENTS.md（topics）

大きな取り組み（トピック）の置き場。入口は `topics-index.md`。

## 「<トピック名> の続き」と言われたら

`workflow-kit/docs-rules.md` の「上の階層で起動して…」の節（24 行付近の 3 行。`offset` 24・`limit` 5 で読む。Grep と全文読みはしない）に従う。トピックでの差分は、窓口が `*-start-here.md`（無ければ `*-handover.md`）であることと、`notes/` は必要なときだけ読むこと。

## データの置き場（正本。2026-11-06 ユーザーの承認）

`topics/` は Project 型のトピックだけを置く。kit 全体のものは直下の `docs/`、トピック固有のものはトピックの `docs/` に置く。`wrap` は作業した単位に書き、`review 消化` は作業した単位と直下を読む。

| 種類 | 置き場 | `wrap` の書き先 | `review 消化` の読み先 |
|---|---|---|---|
| トピック固有の Next Actions、Open Questions、期日 | `topics/<名>/docs/log.md`、`due.md` | 作業した単位 | 作業した単位 |
| トピック固有の decisions、経緯 | `topics/<名>/docs/decisions.md`、`log-history.md` | 作業した単位 | 検索のみ |
| kit 全体の Next Actions、期日 | 直下の `docs/log.md`、`due.md` | 直下 | 直下 |
| kit・規則の変更案（トピックで出たものも） | 直下の `docs/log.md` の Open Questions | 直下 | 直下 |
| kit に効く決定（`【汎用】`） | 直下の `docs/decisions.md` | 直下（トピックの決定を運ぶかは未決） | 検索のみ |
| 測ったこと、kit の改善の印象 | 直下の `docs/records/`、`docs/inbox.md` | 直下 | `review` の入力 1 |
| 知識への昇格の案 | 報告に 1 行 | 報告 | なし |

未決（NA 6）: 閉じるトピックに残った期日の扱い、トピックの `【汎用】` 決定を直下へ運ぶか、トピックをまたぐ期日の割り付け。
## 書くとき

- 窓口は `workflow-kit/templates/topic/start-here.template.md` から作る。
- 状態は `docs/log.md` だけに置く（窓口には「いま」の1行だけ。ほかに写さない）。予算: 窓口 2KB、`log.md` 4KB。
- Claude Projects の共有フォルダは議論の下書きの置き場。確定したらトピックへ移す。
- トピック固有の Next Actions は、トピックの `docs/log.md` だけに置く。リポジトリ直下の `docs/log.md` に同じ項目を写さない（二重管理になる。2026-10-29）。日付で浮上する項目（期日）も、直下の `docs/due.md` に置かず、トピックの `docs/due.md` に置く（直下は kit 全体の項目だけ。2026-11-06 ユーザーの決定）。
- トピックの Next Actions で期日の指定が無いものは、起票日から 1 週間後を期日とする（2026-11-01 ユーザーの決定。`docs/decisions.md`）。起票日の無い項目は、次に触るときに付ける。
- 決定は `docs/decisions.md`（ユーザーの発言を根拠に）。経緯は `docs/log-history.md`。
- 次の会話への依頼は「<トピック名> の続き」の1行（状態は窓口と `log.md` が持つ）。
- **題材ごとのトピックと `records/` の仕訳**（2026-10-25 に正式化。正本は workbase 直下 `docs/decisions.md` の同日の項）: 計画のやり方の題材は `topics/<名前>/`（kebab-case、1階層）に、窓口・`docs/`・`records/` の同じ構造で置く。`records/` は2か所だけ: 直下の `docs/records/` は測ったこと（品質チェックと振り返り）、各トピックの `records/` はそのトピック自身の出力（計画・見本・確認メモ）。`docs/plans/` は使わない。
- 反映が済んだトピックは、下の「トピックを終わらせるとき」に従って削除する（履歴は git）。

## トピックを終わらせるとき

ユーザーが言ったときだけ行う。手順は `close-procedure.md`（言われたときだけ読む。ふだんは読まない）。
