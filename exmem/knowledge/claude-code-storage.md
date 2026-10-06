---
type: knowledge
title: Claude Codeのチャット履歴とメモリの保存場所
status: active
tags:
  - ai/claude
  - tool/zed
  - dotfiles
  - setup
aliases:
  - Claude Codeの履歴の保存場所
  - Claudeチャット履歴の移行
created: 2026-10-01
updated: 2026-10-06
sources:
  - Claude (Claude Code via Zed ACP) conversation "Claudeチャット履歴の保存場所" (2026-10-01)
  - "C:\\Users\\ck\\.claude\\projects（2026-10-01 に確認）"
  - Claude Code conversation "Vault のトップの rename と certs の移動" (2026-10-06。履歴コピーと `--resume` の結果)
---

# Claude Codeのチャット履歴とメモリの保存場所

## Purpose

Claude Code（ZedのACP経由を含む）のチャット履歴とメモリがどこに保存され、プロジェクトを移動したときにどう引き継ぐかをまとめる。

## 保存場所

2026-10-01 時点で確認済み。

| 中身 | 場所 |
|---|---|
| チャット履歴 | `%USERPROFILE%\.claude\projects\<プロジェクト名>\<session-id>.jsonl` |
| メモリ | `%USERPROFILE%\.claude\projects\<プロジェクト名>\memory\` |
| プロジェクトごとの許可設定 | `<プロジェクト>\.claude\settings.local.json` |

- `<プロジェクト名>` は、プロジェクトの絶対パスの英数字以外（`:` `\` `.` など）を `-` に置き換えたもの。
  - `C:\Users\ck\vault\github.com\yuzucha16\notes` → `C--Users-ck-vault-github-com-yuzucha16-notes`（確認済み）
  - `C:\vault\repos\github.com\yuzucha16\areas_shared` → `C--vault-repos-github-com-yuzucha16-areas-shared`（`_` も `-` になる。確認済み）
- ジャンクション経由のパスは、実体のパスに解決されてから名前になる可能性がある（仮説）。exmemの場合、`C--vault-notes-areas-shared-exmem` と `C--vault-repos-github-com-yuzucha16-areas-shared-exmem` のどちらになるかは未確認のため、2026-10-01 に両方へ履歴とメモリをコピーした。
- 1チャット = 1ファイル。隠しファイルではない。
- プロジェクト直下の `.claude\` にあるのは `settings.local.json` だけで、履歴は入っていない。
- ZedのACP経由のチャットも、Zedの `threads.db` ではなくここに保存される（[[zed-dotfiles]]）。
- Claude Desktop の Projects はクラウド（アカウント側）に保存され、`~/.claude` のローカル履歴とは独立している。
- `.jsonl` の構造（1応答が複数行に分かれ、同じ `message.id` と `usage` が繰り返される、など）と、履歴から作業の指標を取る方法は [[ai-work-metrics]]。

## プロジェクトを移動したとき

履歴とメモリはプロジェクトの絶対パスごとに分かれるため、プロジェクトを移動すると前のチャットやメモリが見えなくなる。

引き継ぐ方法の候補は、`projects\<旧プロジェクト名>\` の `.jsonl` と `memory\` を `projects\<新プロジェクト名>\` にコピーすること。ただし、**コピーした履歴は `claude --resume <ID>` で再開できなかった**（確認: 2026-10-06、根拠: Vault のトップを `C:\vault\notes` から `C:\vault\works` へ移したときのユーザーの発言。エラーの内容は未取得）。再開の条件は未特定。移動後は、新規のセッションを始める運用を基本にする。
- 旧キーは消さず、コピーで行う。旧キーが唯一の確実な履歴になる。
- コピーした `.jsonl` には、旧パスの `"cwd"`（`C:\\vault\\notes\\...` と `/c/vault/notes/...` の2形式）が入っている。`"cwd"` を新パスに書き換えて再コピーしても、再開できなかった。「`cwd` の不一致が原因」は、`cwd` だけでは足りないことが分かった。
- `cwd` を書き換えた後も、旧パスが約 1180 件残っていた。内訳は、user メッセージ 941（ほぼツールの出力）、assistant 188、`attachment` 14（`edited_text_file` 8、`instructions` 4、`environment` 2）、`last-prompt` 7。構造的な情報にあたるのは `attachment` の `environment` と `instructions` の約6件で、残りは会話の中身。再開の可否にどれが関わるかは未検証。
- 履歴全体の置換はしない。会話の内容が「`works` を `works` に」のように壊れ、記録として不適切になる。試すなら、コピーした一時キーで、構造的な部分だけを書き換える。
- 旧パスが本文に残ったまま再開できた場合の実害は、モデルが旧パスを現在のパスと取り違えて、旧ディレクトリを作り直すこと（仮説）。
- 旧パスのディレクトリを残して（または作り直して）、そこを cwd にすれば旧キーの履歴は再開できる（仮説。未試験）。旧 clone のディレクトリを削除すると、その cwd での再開ができなくなる。

2026-10-01 に、作業拠点を `C:\Users\ck\vault\notes` から `C:\vault\notes\areas_shared\exmem` へ移すときにこの方法を使った（`C--Users-ck-vault-notes` → `C--vault-notes-areas-shared-exmem`）。コピーした履歴が新しい場所で表示されるかは、未確認のまま（上の 2026-10-06 の結果から、再開は通らない可能性が高い。仮説）。

Claude Codeを起動して `projects\` に別の名前のフォルダができた場合は、プロジェクト名の仮説が外れている。そのフォルダへ `.jsonl` と `memory\` をコピーし直す。

## Decisions

### チャット履歴（`.jsonl`）はdotfilesに含めない（2026-10-01）

- 根拠: サイズが大きくなりやすく、会話の中身がそのまま入っている。
- 却下案: `~/.claude` 全体をdotfilesに入れる。

## Gotchas

### `.claude` をコピーしたのに、移動先でチャットが見えない

- 原因: コピーしたのはプロジェクト直下の `.claude`（設定のみ）だった。履歴はユーザーフォルダ直下の `%USERPROFILE%\.claude\projects\` にある。名前が同じ別のフォルダ。
- 解決: ユーザーフォルダ側の `projects\<旧プロジェクト名>\*.jsonl` を `projects\<新プロジェクト名>\` にコピーする。

### `.jsonl` が見つからない

- 原因: プロジェクト内の `.claude` を見ていた。隠し属性ではない。
- 解決: エクスプローラーのアドレスバーに `%USERPROFILE%\.claude\projects` を入力して開く。

### Zedで exmem のセッションを立てても、exmem として動かない

- 状況: Zedのワークスペースが `C:\vault` のまま、Claude Agentのチャットに exmem のパスや `cd notes/areas_shared/exmem` と書いた。セッションは `C:\vault` を作業フォルダとして動き、履歴は `C--vault` に保存された。exmemの `CLAUDE.md` も読まれなかった。
- 原因: ZedのClaude Agentは、Zedで開いているプロジェクトのルートを作業フォルダにして起動する。チャットでの `cd` では変わらない。
- 解決: exmemをZedのプロジェクトとして開き直す（`zed C:\vault\notes\areas_shared\exmem`、または File > Open で exmem フォルダを選ぶ）。その上で新しいThreadを作る。

### Zedで `/resume` が使えない

- 原因: `/resume` はターミナル版Claude Codeのコマンドで、ZedのACP経由では使えない。
- 解決: 過去のチャットを再開するときは、ターミナルで作業フォルダに移動してから `claude --resume` を実行する。

### コピーした履歴が、新しいパスで `claude --resume` できない

- 状況: Vault のトップを `C:\vault\notes` から `C:\vault\works` に rename したとき、履歴を新キー（`C--vault-works-*`）へコピーして `claude --resume <ID>` したが、再開できなかった。`"cwd"` を書き換えて再コピーしても同じだった（2026-10-06）。
- 原因: 不明。`cwd` の不一致だけではない。`cwd` 以外のフィールドの旧パス（上の「プロジェクトを移動したとき」）、キーの付け方、セッションの索引が候補（未調査）。
- 解決: なし。新しいパスでは、新規のセッションを始める。旧キーの履歴は残してある。

### Claude Desktop の Projects に履歴が出ない

- 原因: 不具合ではない。Desktop の Projects はクラウド、Claude Code の履歴はローカルで、保存先が別。

## Open Questions

- `~/.claude` の手書き設定のうち、`settings.json` は管理済み（dotfilesの `home/.claude/settings.json` へリンク。WSL・Windowsとも適用済み、2026-10-04 に確認。[[claude-code-permissions]]）。`CLAUDE.md` と `projects\<プロジェクト名>\memory\` をdotfilesで管理するかは未決。
- Claude Desktop の Code 機能から、ローカルの履歴が見えるか。
- `claude --resume` が通らない原因は何か（`cwd` の書き換えだけでは通らなかった）。

## Next Actions

- `--resume` が通らない原因を調べる（任意）。調べないなら、移動後は新規のセッションを始める運用にする。調べるなら、失敗時のエラー文面を取り、コピーした一時キーで、構造的な旧パス（`attachment` の約6件）だけを書き換えて試す（2026-10-06 時点）。
- ターミナルで `$HOME\works\resources\exmem`（2026-10-06 以前は `C:\vault\works\resources\exmem`）に移動して `claude --resume` を実行し、コピーした履歴が表示されるか確認する。あわせて、`projects\` のどちらのフォルダに書き込まれるかを確認し、使われなかった方を削除する。

## Related

- [[zed-dotfiles]]
- [[zed-acp]]
- [[obsidian-vault]]
- [[claude-code-project-settings]]
- [[ai-work-metrics]]
