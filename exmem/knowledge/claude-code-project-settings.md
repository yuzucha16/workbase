---
type: knowledge
title: プロジェクトの .claude/ の管理方針
status: active
tags:
  - ai/claude
  - setup
  - workflow
aliases:
  - .claudeの管理方針
  - settings.local.json
  - Claude Codeのプロジェクト設定
created: 2026-10-02
updated: 2026-10-05
sources:
  - Claude Code conversation "inbox整理と.claude/の扱い" (2026-10-02)
  - "exmem/.claude/ の中身（2026-10-02 に確認）"
---

# プロジェクトの .claude/ の管理方針

## Purpose

プロジェクト直下の `.claude/` を、Gitで管理するものと管理しないものに分ける方針をまとめる。対象は exmem（共有リポジトリ `workbase` 内。2026-10-05 まで `notes` リポジトリ内、2026-10-02 まで `areas_shared` リポジトリ）。履歴とメモリの保存場所は別で、[[claude-code-storage]] にある。

## Principles

- ローカル専用のものはGitに入れない。共有したいルールと手順だけを管理する。
- 指示は `AGENTS.md` に一本化する。Claude固有の設定ファイルは、必要になってから足す（[[ai-development-workflow]] D6）。
- exmem はAIが毎回読み書きする場所なので、許可は読み取り専用に絞る。書き込み系は許可しない。

## 基本方針

| ファイル | Git | 理由 |
|---|---|---|
| `settings.local.json` | 管理しない（ignore） | 個人・端末ごとの許可設定。パスや過去のコマンドが入り、他の端末や人には意味がない。公式にもローカル専用で、自動的にgitignoreされる位置づけ |
| `settings.json` | 管理する | チーム共通のルール（許可・拒否、フック）を置く場所 |
| `skills/`、`agents/`、`commands/` | 管理する | プロジェクトで共有したい手順 |

## Decisions

### exmem では `.claude/` をまだ管理下に置かない（2026-10-02）

- 決定: 今回は `settings.local.json` をignoreするだけにする。`settings.json` と `skills/` は、もう少し運用が育ってから管理下に置く。
- 根拠: exmem の `.claude/` にあるのは `settings.local.json` だけで、中身はこの作業中に許可した一回限りのコマンド2つ（実在の確認用）だった。再利用できる設定ではなく、残す価値がない。
- ignoreの書き方: リポジトリのルート（`workbase`、旧 `notes`、旧 `areas_shared`）の `.gitignore` に `**/.claude/settings.local.json` を書く（exmem 配下の `.claude/` に限らず効く）。

### `settings.json` は今は作らない

- 根拠: 指示は `AGENTS.md` に一本化済みで、Codex / Copilot とも共通にできる。
- 作るときは、許可を読み取り専用に絞る。例: `git status`、`git diff`、`Get-ChildItem`。
- 許可が溜まって確認が多すぎるときは、`/fewer-permission-prompts` で、履歴から読み取り専用のコマンドを拾った許可リストの案を作れる。

### `skills/` は、運用手順が固まってから検討する

- 例: 「inbox整理」の手順。
- まず `AGENTS.md` に書く（他のエージェントも読める）。スキルにするのは、Claude固有で手順が長いときだけ。

## 権限の土台との関係

権限の共通ルールは、プロジェクトの `.claude/` ではなく**ユーザー階層**（`~/.claude/settings.json`、実体はdotfilesの `home/.claude/settings.json`）に置いている（[[claude-code-permissions]]）。プロジェクト側の `settings.json` を使うのは、壊してよい「サンドボックス」リポジトリで権限を緩めるときが最初の想定。したがって、exmemの `.claude/settings.json` を管理下に置くのは、読み取り専用の許可が土台に入ってもなお足りない場合に限る。

## Facts

- 2026-10-02 時点の exmem の `.claude/` は `settings.local.json` のみ（848バイト）。`allow` に PowerShell のコマンド2件が入っている。
- 履歴とメモリは、プロジェクト内の `.claude/` ではなく `%USERPROFILE%\.claude\projects\` にある。dotfilesには入れない方針（[[claude-code-storage]]）。

## Open Questions

- どの時点で `settings.json` を管理下に置くか（読み取り専用の許可が安定したら）。
- `skills/` にする手順があるか。「inbox整理」はAGENTS.mdのままでよいか。

## Next Actions

- 運用が育ったら、読み取り専用の許可を `settings.json` にまとめ、Gitで管理する。
- スキルにしたい手順が出たら、`.claude/skills/` に置いて管理下に入れる。

## Related

- [[claude-code-permissions]]
- [[claude-code-storage]]
- [[ai-development-workflow]]
- [[zed-acp]]
