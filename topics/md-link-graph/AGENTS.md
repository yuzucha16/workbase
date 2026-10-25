# AGENTS.md（md-link-graph）

Markdown の参照を呼び出しグラフとして測り、ルールや知識が作業の最中に届く構造かを調べるトピック（Project 型）。上位の規約は `topics/AGENTS.md` と、リポジトリ直下の `AGENTS.md`。

## 共通ルール

共通ルールの置き場は `$HOME\works\resources\workflow-kit`。ユーザーが合言葉を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する。`docs-rules.md` は、`docs/` を更新するときと、コミット・push の前に読む。読めないときは、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `md-link-graph-start-here.md`（窓口）
2. `docs/log.md`（開始時に読むのはここまで）
3. `docs/decisions.md`（何かを決める・変える前に検索する）。経緯が要るときだけ `docs/log-history.md`

## このトピック固有のルール

- スクリプトは、リポジトリのトップから `python -I topics/md-link-graph/tools/<名前>.py` で実行する（使い方は窓口）。
- `records/` はこのトピック自身の出力（グラフ、表、場面）。再生成できるので、手で直さず、スクリプトを直して作り直す。
- 完了は窓口の完了条件（構造の問題点を数字で示し、直す案をユーザーが決める）。閉じるときは `topics/AGENTS.md` の「トピックを終わらせるとき」に従う。

## コミット

- メッセージは `[topics] md-link-graph: 内容`。`git add` はパスを指定する。
