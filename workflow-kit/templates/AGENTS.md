# AGENTS.md

<このディレクトリが何のためのものかを1〜2行で。>

## 共通ルール

共通ルールの置き場は `$HOME\works\resources\workflow-kit`（WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources/workflow-kit`）。ユーザーが合言葉（手順書を呼ぶ短い言葉。日本語の別名つき）を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する。`docs-rules.md` は、作業を始める前と、`docs/` を更新するときに読む。

読めない場合（`workbase` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `docs/log.md`
2. <README など、このディレクトリ固有の入口>
3. `docs/decisions.md`

## このディレクトリ固有のルール

- <固有のルール。無ければ「なし」>

## コミット

- メッセージは `[対象] 内容`。`git add` はパスを指定する。
