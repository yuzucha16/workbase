# 導入フックの見本

`setup-hook.md` の入力・生成物・報告の型を、1つの完成例で示す。**内容は架空で、事実として扱わない。** 形式（入力の埋め方、生成物の姿、報告の順）だけを真似る。

見本を直すのは、`setup-hook.md` を直したときだけ。出力が揺れた箇所があれば、このファイルに見本を足す（`improvements.md` に記録する）。

## 入力の例

1. 対象ディレクトリ: `C:\work\sample-batch`
2. 目的: 夜間バッチのスクリプトと、その設定を管理する。
3. 読む順番の固有項目: `README.md`
4. 固有ルール: 本番の接続先は、`config/prod.local.yml`（追跡しない）にだけ書く。コミットは `[対象] 内容`。

## 生成物の例

`sample-batch/AGENTS.md`:

````markdown
# AGENTS.md

夜間バッチのスクリプトと、その設定を管理する。

## 共通ルール

共通ルールの置き場は `C:\vault\notes\resources\workflow-kit`（WSL: `/mnt/c/vault/notes/resources/workflow-kit`）。次の時機に、該当のファイルを読む。

- `docs-rules.md`: 作業を始める前と、`docs/` を更新するときに読む。`docs/` の運用。作業の終わりに `docs/log.md` と `docs/decisions.md` を更新する。
- `knowledge-hook.md`: ユーザーが「ナレッジ化して」と言ったときに読み、実行する（言われたときだけ）。書き込みは `exmem/inbox/` の新規ファイルだけ。

上のファイルが読めない場合（`notes` が無いPCなど）は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `docs/log.md`
2. `README.md`
3. `docs/decisions.md`

## このディレクトリ固有のルール

- 本番の接続先は、`config/prod.local.yml`（追跡しない）にだけ書く。

## コミット

- メッセージは `[対象] 内容`。`git add` はパスを指定する。
````

`sample-batch/CLAUDE.md`:

````markdown
@AGENTS.md
````

`sample-batch/docs/log.md` と `docs/decisions.md` は、`templates/` の雛形の冒頭の説明を、目的に合わせて書き換えたもの。

## 報告の例

1. **対象**: `C:\work\sample-batch`
2. **変更したファイル**: 新規に `AGENTS.md`、`CLAUDE.md`、`docs/log.md`、`docs/decisions.md` を作った。既存ファイルへの変更は無い。
3. **追跡状況**: Git 管理（`.gitignore` で除外されていない）。
4. **承認が必要なこと**: なし。
5. **改善案**: 改善案なし。
