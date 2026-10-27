---
type: procedure
title: トピックを終わらせる手順
tags:
  - workflow
  - knowledge-management
created: 2026-10-28
updated: 2026-10-28
---

# トピックを終わらせる手順

`topics/AGENTS.md` から指される。ユーザーが言ったときだけ行う。完了条件の確認、暫定の決定の見直し、未解決の整理は、`review 消化` と `docs/log.md` の Next Actions / Open Questions で行う（専用の手順は持たない）。Area 型のトピックは消さない。

0. 閉じる・完了と判断する前に、トピックの `docs/log.md` の状態表と、上位（root）の `docs/log-history.md` の最新の経緯を突き合わせ、食い違いと結果を報告に書く（古い側で断定しない）。
1. `docs/decisions.md` の【汎用】が `exmem/lessons/`、kit、`guides/` に反映済みか見る。【汎用】の印には頼らない。AI が、トピックの決定と `records/`・共有フォルダの結論から、経験則の候補を全部挙げ、行き先の案を付けて見せる。採否はユーザーが決め、採ったものだけを移す。行き先は内容の種類で決める: 設計と理由は `guides/explain/`、決定は `docs/decisions.md`、仕様は実装の隣、原則は `exmem/lessons/`、経緯は git。移し終えたノートは元を削除する（二重管理を残さない）。実装前の設計を移すときは、未実装の部分に「未実装」と注記する。残件は上位の Next Actions に移す（2026-10-19 承認）。
1a. 消す前の条件（2026-10-21 ユーザーの決定。`usage-viz` で実施）: `stock`（知識の反映）と `wrap`（記録）が済んでいること。`wrap` で、トピックの `docs/decisions.md` の【この件】の決定を、root の `docs/decisions.md` に1項にまとめて移す（根拠はユーザーの発言のまま。【汎用】は手順1の行き先へ）。経緯は root の `docs/log-history.md` に追記し、root の `docs/log.md` の該当行を直す。未確認のことは root の `log.md` に1行残す。
1b. `records/` と、Claude Projects の共有フォルダの `notes/<題材>/` は、中身の種類で振り分ける（2026-10-28 ユーザーの決定。正本は root の `docs/decisions.md` の同日の項）。AI が一覧にして見せ、採否はユーザーが決める。共有フォルダのファイルは、採否のあとにユーザーが消す。このリポジトリのノートから共有フォルダへはリンクを張らない。

| 中身の種類 | 行き先 |
|---|---|
| 測定値、観測（時系列で古くなるもの） | `logbook/`（型は `logbook/README.md`） |
| 道具（スクリプト） | `workflow-kit/tools/`。先頭の説明（docstring）を必須にし、使い方、入力、出力、数えないもの、設計の理由（短く）、実行例（数個）を書く。`workflow-kit/README.md` には行を足さない |
| 再び実行する手順（通し試験など） | 関係する手順書の隣（例: `workflow-kit/room/`） |
| 型の見本（6R、憲章、WBS、会議メモなど） | `workflow-kit/examples/`。1つの型につき、良い例を1件 |
| 検討の過程（案、比較、レビュー、計画、品質チェックの run ログ） | 削除（履歴は git） |
| 上のどれでも、トピックの外から根拠として指されている（`grep` で確かめる） | 上の行き先に移し、指す側のリンクを書き換えてから閉じる |

`kit-growth/records/` へ移すのは、これまでどおり「測ったこと」（やり方・モードの品質チェックと振り返り）だけ。
2. ディレクトリを削除し、`topics-index.md` の行を消す。窓口や他のノートの言及（`planning-method` の窓口など）も直す。
3. 残ったファイルに、消えたノートへの `[[リンク]]` が無いか、grep で確かめる。
4. 記録は `wrap` に任せる。
