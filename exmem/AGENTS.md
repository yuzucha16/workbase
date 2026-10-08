# AGENTS.md

このディレクトリは exmem（external memory、外部メモリ）。AIと人間が共有するナレッジ置き場で、AIとの壁打ちや作業から得た知識を、AI・端末をまたいで引き継ぐ。
Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。
人間はObsidianで閲覧・編集する。

- 場所: `$HOME\works\resources\exmem`（Obsidian Vault `$HOME\works` の `resources/` に clone した、共有リポジトリ `workbase`（GitHub: `yuzucha16/workbase`）の一部）
- `workbase` のルートは `resources/` で、`$HOME\works`（Vault のトップ）は別の、PC ローカルのリポジトリ。変更は `resources/` の中で `git diff` で確認できる。
- エージェントはこのディレクトリを作業ディレクトリとして起動する。
- 履歴: 2026-10-02 に `areas_shared` リポジトリから `notes` リポジトリへ移し、2026-10-05 に `notes` から `workbase` として切り出した。旧 `exmem/projects/` は、Vault の PARA の `projects/` と区別するため `contexts/` に改名した。

## Vault での位置づけ

- `workbase`（`resources/`）の内容は、すべて共有（Git管理）する。機密、会社固有の情報、PC ごとのデータを入れない。ローカルのデータ（PARA の `areas/` `projects/` `archives/`）は、Vault のトップのリポジトリにあり、`workbase` の外にある。
- 共有側（`workbase`）のノートから、ローカル側（`areas/` など）へ `[[リンク]]` を張らない。他のPCでリンク切れになる。
- `contexts/` は、`works` から見えない場所の作業の引継ぎコンテキストの置き場で、Vault 直下の `projects/` とは別物。
- **`contexts/` に業務の文脈（会社固有・案件固有の内容、会社環境の制約や設定）を書かない**（2026-10-08 ユーザーの決定。共有側は公開されうる前提で書く。公開の予定はあるが未決定）。業務の引継ぎが必要なときは、作業側の `docs/`（非公開の remote か、ローカルの git）に書く。書いてしまったら、公開前に削除する（`ai-business-adoption` と `office-deliverable-workflow` は、この方針で 2026-10-08 に削除した）。
- ローカル専用の置き場（旧 `_local/`）は、2026-10-05 に廃止した。ローカルのデータは、`workbase` の外（Vault のトップの PARA）に置く。

## 読む順番

1. `contexts/<project>/context.md` の `Current State` と `Next Actions`
2. そこからリンクされている `knowledge/*.md`
3. 全体像が必要なら `README.md`、タグの一覧は `tags.md`

## ディレクトリの役割

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する（`inbox/README.md` は除く）。
- `knowledge/`: AIをまたいで再利用する知識。1ファイル1トピック。
- `contexts/<project>/context.md`: `works` から見えない場所の作業の、現在状態と次にやること（引継ぎ用。旧 `projects/`。作業ログの置き場ではない）。

## Frontmatter

```yaml
---
type: knowledge          # knowledge / project / index / inbox
title: Zed Vim環境
status: active           # active / superseded
tags:
  - tool/zed
  - keymap
aliases:
  - ZedへのVim環境移行
created: 2026-09-26
updated: 2026-09-26
sources:
  - ChatGPT conversation "ZedへのVim環境移行" (2026-09-26)
---
```

- `type` / `title` / `status` / `tags` / `created` / `updated` は必須。
- `aliases` には日本語名や別名を入れる。Obsidianのリンク補完・検索で使われる。
- 日付は `YYYY-MM-DD`。知識ファイルを変更したら `updated` を今日の日付にする。

## タグ

タグは「何についての知識か」を表す横断的な分類。ルールと語彙は `tags.md` にある。

- frontmatter の `tags` にリストで書く。`#` は付けない。本文中にタグを書かない。
- 英小文字の kebab-case。スペース不可。
- `tags.md` の語彙から選ぶ。新しいタグが必要なら `tags.md` に追記してから使う。
- `type` や `status` の値（`project`、`knowledge` など）をタグにしない。プロパティと重複するため。
- 特定のノートとの関係はタグではなく `[[リンク]]` で表す。

## 本文の書き方

- Markdown + 通常の見出しで書く。AI固有の形式は使わない。
- 確認済みの事実と仮説を区別する。バージョンなど変わりやすい値には「YYYY-MM-DD 時点」を付ける。
- 古くなった記述は削除せず、`status: superseded` にして新しいファイルへリンクする。

知識ファイルは、該当する内容があれば次の見出しを使う。

| 見出し | 書くこと |
|---|---|
| `## Principles` | 判断の拠り所になる方針・原則。「〜しない」「〜を優先する」など |
| `## Decisions` | 個別の決定。決めたこと、根拠、却下案、日付をそろえる |
| `## Gotchas` | 実際に遭遇したエラーや詰まった点。状況、原因（わかれば）、解決の順 |

注意点や方針のうち、実際に遭遇したエラーでないものは `Gotchas` ではなく `Principles` に書く。

## リンク

- ノート間のリンクは `[[ファイル名]]` で書く（例: `[[zed-vim]]`）。
- `context.md` は複数あるため、`[[zed-vim-migration/context]]` のようにフォルダ名を付ける。
- 知識ファイルには、関係する知識・プロジェクトへのリンクを `## Related` にまとめる。

## inbox を整理するとき

1. inbox のメモから Principles / Decisions / Gotchas / 事実 / Open Questions を抜き出す。
2. **実物と照合する。** メモの内容は会話から生まれたもので、実物と食い違うことがある。設定ファイル・コード・コマンド出力など確認できるものは実際に見て、一致すれば「確認済み」、食い違えば実物を正として記録し、食い違いを `Open Questions` に残す。確認できないものは仮説として書く。
3. タグを `tags.md` の語彙に正規化する。
4. 該当する `knowledge/*.md` に統合する。該当がなければ新しいファイルを作る。
5. `context.md` の `Current State` / `Next Actions` / `Open Questions` を更新する。
6. 新しいファイルを作ったら `README.md` の構成図を更新する。
7. 統合したメモを inbox から削除する。**削除の前に、メモと統合先の照合（メモに無い記述、メモから落ちた記述）をユーザーに示して承認を得て、台帳 `integrated.md` に1行足す**（`| 日付 | 統合 | <メモ名> | <統合先> | 承認済（日付） |`。統合・台帳・削除は1コミットにする。作業ディレクトリ側の `転記済` への確定は、`review` が台帳を読んで行う。手順: `resources/workflow-kit/integrate-hook.md`）。

## 作業を終えるとき

`contexts/<project>/context.md` の `Current State` と `Next Actions` を更新する。
次に作業するAI・端末は、ここから再開する。

exmem には、作業ディレクトリ（dotfiles など）の作業ログを置かない。作業ディレクトリの経緯・決定・次にやることは、各ディレクトリの `docs/` が持つ（運用は `resources/workflow-kit/docs-rules.md`）。`contexts/<名前>/context.md` は、`works` から見えない場所（モバイルや他環境での壁打ちなど）の作業を引き継ぐためのコンテキストで、作業ログの置き場ではない。`inbox/` のメモの Open Questions と Next Actions を、統合の手順で反映する。この引継ぎコンテキストを消化する手段は未定（`resources/workflow-kit/improvements.md`）。

作業ディレクトリは exmem を基本は読み取り専用で参照するだけで、書き込みの例外は、ユーザーが「ナレッジ化して」と指示したときに `inbox/` へ新規メモを1つ置くことだけ（手順と形式の正本は `resources/workflow-kit/stock-hook.md`。`inbox/README.md` のプロンプトはその写し。`tags` は語彙外のものが入ることがあるので、統合のときに正規化する）。`inbox/` のメモは、上の「inbox を整理するとき」の手順で `knowledge/` へ統合する。ユーザーが「inboxを整理して」と言ったときは、この手順に、統合したメモを指す作業ディレクトリの `docs/` の `転記待ち` を `転記済` に進める案の作成（承認制）を足した `resources/workflow-kit/integrate-hook.md` に従う。ソース側の「終了処理して」（`wrap-hook.md`）は、未統合のメモの件数を報告して、この統合を勧める。
