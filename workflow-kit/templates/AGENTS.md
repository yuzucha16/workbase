# AGENTS.md

<このディレクトリが何のためのものかを1〜2行で。>

## 共通ルール

共通ルールの置き場は `C:\vault\notes\resources\workflow-kit`（WSL: `/mnt/c/vault/notes/resources/workflow-kit`）。次の時機に、該当のファイルを読む。

- `docs-rules.md`: 作業を始める前と、`docs/` を更新するときに読む。`docs/` の運用。作業の終わりに `docs/log.md` と `docs/decisions.md` を更新する。
- `knowledge-hook.md`: ユーザーが「ナレッジ化して」と言ったときに読み、実行する（言われたときだけ）。書き込みは `exmem/inbox/` の新規ファイルだけ。

上のファイルが読めない場合（`workbase` を clone していないPCなど）は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `docs/log.md`
2. <README など、このディレクトリ固有の入口>
3. `docs/decisions.md`

## このディレクトリ固有のルール

- <固有のルール。無ければ「なし」>

## コミット

- メッセージは `[対象] 内容`。`git add` はパスを指定する。
