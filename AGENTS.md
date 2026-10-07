# AGENTS.md

`workbase` 全体の規約。汎用ナレッジと共通機能を育てる共有リポジトリ。Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。
各ディレクトリに固有のルールがある場合は、そのディレクトリの `AGENTS.md` / `CLAUDE.md` が優先される（例: `exmem/AGENTS.md`）。

ノートの読み書きは、エージェントがファイルを直接行う。人間は Obsidian で閲覧・編集する。

## 構成

| ディレクトリ | 内容 |
|---|---|
| `exmem/` | AI をまたいで再利用するナレッジ（external memory） |
| `workflow-kit/` | 作業ディレクトリに導入する共通機能（`docs/` の運用と、合言葉で呼ぶフック。呼び出し表は `hooks.md`）の正本 |
| `cheatsheets/` | コマンド・設定のチートシート |
| `handson/` | ハンズオンの課題とテンプレート |

- このリポジトリは単独で clone しても自己完結する。外のファイルに依存しない。
- 通常は、Obsidian Vault の `resources/` として clone して使う（Windows: `$HOME\works\resources`、WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources`）。Vault 全体（PARA の各区分、PC ごとのローカルの作業）は、このリポジトリの外にある。

## 共通ルール

共通ルールの置き場は `workflow-kit/`（上の場所なら `$HOME\works\resources\workflow-kit`）。ユーザーが合言葉（手順書を呼ぶ短い言葉。日本語の別名つき）を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する（言われたときだけ）。`docs-rules.md` は、作業を始める前と、`docs/` を更新するときに読む。読めない場合は、記憶で代用せず、ユーザーに伝えて止まる。

## 共有の範囲

- このリポジトリの内容は、すべて共有（Git 管理）する。機密、会社固有の情報、PC ごとのデータを入れない。公開範囲は未定なので、公開されうる前提で書く。
- ローカルのデータ（会社・個人の作業）は、このリポジトリの外に置く。このリポジトリのノートから、外のファイルへ `[[リンク]]` を張らない。他の PC でリンク切れになる。
- `git add -f` で、ignore 済みのファイルを追加しない。
- `.claude/settings.local.json` は端末ごとの許可設定なので、追跡しない（`.gitignore` 済み）。

## リンク

- ノート間のリンクは wikilink（`[[名前]]`）。ファイル名はリポジトリ内（Vault 内）で一意に保つ（最短パスで解決されるため）。

## 書式とコミット

- 改行コードは LF（`.gitattributes` で統一）。
- コミットメッセージは `[領域] 変更内容` の形式（例: `[exmem] ...`、`[workflow-kit] ...`、`[cheatsheets] ...`）。
