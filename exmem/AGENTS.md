# AGENTS.md

このディレクトリは exmem（external memory、外部メモリ）。AIと人間が共有するナレッジ置き場で、AIとの壁打ちや作業から得た知識を、AI・端末をまたいで引き継ぐ。
Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。
人間はObsidianで閲覧・編集する。

- 場所: `C:\vault\notes\resources\exmem`（Obsidian Vault `C:\vault\notes` の中）
- `C:\vault\notes` 自体が Gitリポジトリ（GitHub: `yuzucha16/notes`）のルート。変更は `git diff` で確認できる。共有するのは `resources/` と `.obsidian/` だけで、それ以外（`projects/` `areas/` `archives/`）は `.gitignore` によりローカル専用。
- エージェントはこのディレクトリを作業ディレクトリとして起動する。
- 2026-10-02 に `areas_shared` リポジトリ（ジャンクション経由）から `notes` リポジトリ直下へ移した。旧 `exmem/projects/` は、Vault の PARA の `projects/` と区別するため `contexts/` に改名した。

## Vault での位置づけ

- `resources/` は「共有（Git管理）」、それ以外の PARA 区分はローカル専用。共有するかどうかは名前ではなく `.gitignore` で決まる。
- 共有側（`resources/`）のノートから、ローカル側（`areas/` など）へ `[[リンク]]` を張らない。他のPCでリンク切れになる。
- `contexts/` は exmem のプロジェクト状態の置き場で、Vault 直下の `projects/` とは別物。
- `resources/` の中でもローカル専用にしたいもの（会社固有・個人的な内容）は、`_local/` に置く。名前が `_local` のディレクトリは、どの階層にあっても中身がGitに載らない（`.gitignore` の `**/_local/*`。`.gitkeep` だけ追跡して、clone でディレクトリが出来る）。`resources/_local/`、`resources/exmem/_local/` などがある。
  - `resources/` 直下の他のものは既定で共有になる。ローカル専用のものを `_local/` の外に置かない。
  - 共有側のノートから `_local/` のノートへ `[[リンク]]` を張らない。
  - `_` で始まるディレクトリはトピックではない管理用で、共有かどうかは別。`_archive/` は共有、`_local/` はローカル専用。

## 読む順番

1. `contexts/<project>/context.md` の `Current State` と `Next Actions`
2. そこからリンクされている `knowledge/*.md`
3. 全体像が必要なら `README.md`、タグの一覧は `tags.md`

## ディレクトリの役割

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する（`inbox/README.md` は除く）。
- `knowledge/`: AIをまたいで再利用する知識。1ファイル1トピック。
- `contexts/<project>/context.md`: プロジェクトの現在状態と次にやること（旧 `projects/`）。

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
7. 統合したメモを inbox から削除する。

## 作業を終えるとき

`contexts/<project>/context.md` の `Current State` と `Next Actions` を更新する。
次に作業するAI・端末は、ここから再開する。

exmem には他リポジトリ（dotfiles など）の作業ログを置かない。そうしたプロジェクトの経緯・決定・次にやることは、各リポジトリの `docs/` が持つ。他リポジトリは exmem を読み取り専用で参照するだけで、exmem へは書き込まない。
