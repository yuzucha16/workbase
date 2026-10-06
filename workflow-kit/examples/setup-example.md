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

共通ルールの置き場は `C:\vault\works\resources\workflow-kit`（WSL: `/mnt/c/vault/works/resources/workflow-kit`）。次の時機に、該当のファイルを読む。

- `docs-rules.md`: 作業を始める前と、`docs/` を更新するときに読む。`docs/` の運用。作業の終わりに `docs/log.md` と `docs/decisions.md` を更新する。
- `knowledge-hook.md`: ユーザーが「ナレッジ化して」と言ったときに読み、実行する（言われたときだけ）。書き込みは `exmem/inbox/` の新規ファイルだけ（例外は `knowledge-hook.md`）。

上のファイルが読めない場合（`workbase` を clone していないPCなど）は、記憶で代用せず、ユーザーに伝えて止まる。

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

## ワークスペースの生成（項目 5）の例

**内容は架空。** 業務用 PC で、Vault のトップを新しく作る場合。`resources/`（`workbase` の clone）は、dotfiles の `50_repos` が作成済みで、`workbase` の中で、「workflowを導入して」とだけ言った（対象の指定なし）ので、入力はすべて既定値になった。

入力: 1. 対象ディレクトリ `C:\vault\works`。2. 目的: 業務用 PC の作業場。この PC のローカルの作業を PARA で管理し、共有ナレッジを参照する。3. 読む順番の固有項目: なし。4. 固有ルール: なし。5. PC の役割: 業務用。6. remote の方針: なし。7. 初回コミット: する。

生成物:

- `.gitignore`: `templates/workspace/gitignore.template` のまま。
- `.ignore`: `templates/workspace/ignore.template` のまま（`!/resources/`）。
- `.gitattributes`: `templates/workspace/gitattributes.template` のまま（LF 統一）。
- `AGENTS.md`: `templates/workspace/AGENTS.md` の `< >` を埋めたもの。冒頭は「業務用 PC の作業場。…」、remote は「なし」、固有ルールの1項目目は「このリポジトリに remote を足さない。push しない（…`.git/hooks/pre-push` で止めてある）」。「共通ルール」の節は雛形のまま。固有ルールの最後は「なし」。
- `CLAUDE.md`（`@AGENTS.md`）、`docs/log.md`、`docs/decisions.md`、`areas/.gitkeep`、`projects/.gitkeep`、`archives/.gitkeep`。
- `git init` 済み。`git remote -v` は空。`.git/hooks/pre-push` がある。初回コミット済み（agent の身元とトレーラー3行つき。生成物の10ファイルだけ（`docs/` の2ファイルを含む）。`areas/` `projects/` `archives/` の既存の中身は追跡していない）。

報告の例:

1. **対象**: `C:\vault\works`
2. **条件**: 対象 `C:\vault\works`（既定値）。目的「業務用 PC の作業場。…」（既定値）。PC の役割: 業務用（既定値）。remote: なし（既定値）。初回コミット: する（既定値）。変えたいとき: 役割と目的は `AGENTS.md` の冒頭を直す。remote を足すときは `git remote add origin <URL>` と、`.git/hooks/pre-push` の削除。
3. **変更したファイル**: 新規に上記のファイルと `.git/` を作った。`resources/` と `.obsidian/` は触っていない。
4. **追跡状況**: この PC だけのローカルなリポジトリ（remote なし）。`resources/` は別リポジトリ（`workbase`）なので除外した。
5. **承認が必要なこと**: 初回コミットは行った（`[vault] initial commit: …`。作者は `agent <agent@agent.local>`）。git の身元の設定を促す: `git config --global --get user.name` と `user.email` が未設定（または `example.com` を含む仮値）なら、現在値を示して設定を促す（エージェントのコミットには要らない。ユーザー自身の手動のコミット用）。remote が無いので push の案内は無い（remote があるときは、`git push -u origin main` と、既存のコミットがあるときの `git pull --rebase origin main` を書く）。未追跡の既存ファイルは、あれば一覧する（今回は無し）。`.obsidian` は未リンク（dotfiles の `30_link.bat` を実行する。実ディレクトリがあれば先に退避する）。
6. **改善案**: 改善案なし。
