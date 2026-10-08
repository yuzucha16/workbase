# AGENTS.md

exmem（external memory、外部メモリ）は、AIと人間が共有するナレッジ置き場。AIとの壁打ちや作業から得た知識を、AI・端末をまたいで引き継ぐ。Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。人間はObsidianで閲覧・編集する。

場所は `$HOME\works\resources\exmem`（共有リポジトリ `workbase` の一部。Vault のトップ `$HOME\works` は別の、PC ローカルのリポジトリ）。エージェントはこのディレクトリを作業ディレクトリとして起動する。

## 共有の範囲

- `workbase` の内容は、すべて共有（Git管理）する。公開されうる前提で書く。機密、会社固有の情報、PC ごとのデータを入れない。ローカルのデータ（PARA の `areas/` `projects/` `archives/`）は、Vault のトップのリポジトリにあり、`workbase` の外にある。
- 共有側のノートから、ローカル側（`areas/` など）へ `[[リンク]]` を張らない。他のPCでリンク切れになる。
- **`contexts/` に業務の文脈（会社固有・案件固有の内容、会社環境の制約や設定）を書かない**（2026-10-08 ユーザーの決定。公開の予定はあるが未決定）。業務の引継ぎが必要なときは、作業側の `docs/`（非公開の remote か、ローカルの git）に書く。書いてしまったら、公開前に削除する。

## 読む順番

1. `README.md` の「知識の索引」で、該当する知識を探し、その `knowledge/*.md` を読む（全件は読まない）。
2. 作業を引き継ぐときは、`contexts/<project>/context.md` の `Current State` と `Next Actions`。
3. タグの一覧は `tags.md`。

## ディレクトリの役割

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する（`inbox/README.md` は除く）。
- `knowledge/`: AIをまたいで再利用する知識。1ファイル1トピック。
- `contexts/<project>/context.md`: `works` から見えない場所の作業の、現在状態と次にやること（引継ぎ用。作業ログの置き場ではない）。Vault 直下の `projects/` とは別物。

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

## 統合と書き込み

- 新しい知識ファイルを作ったら、`README.md` の「知識の索引」に1行足す。
- `inbox/` の統合は、ユーザーが「inboxを整理して」と言ったときに、kit の `integrate-hook.md`（統合の手順の正本）に従う。
- 作業ディレクトリは exmem を基本は読み取り専用で参照する。書き込みの例外は、ユーザーが「ナレッジ化して」と指示したときの `inbox/` への新規メモ1つだけ（正本は kit の `stock-hook.md`。`inbox/README.md` のプロンプトはその写し）。
- exmem に、作業ディレクトリの作業ログを置かない（経緯・決定・次にやることは、各ディレクトリの `docs/` が持つ）。`contexts/` の作業を終えるときは、`Current State` と `Next Actions` を更新する。この引継ぎコンテキストを消化する手段は未定。
