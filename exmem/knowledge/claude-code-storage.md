---
type: knowledge
title: Claude Codeのチャット履歴とメモリの保存場所
status: active
tags:
  - ai/claude
  - tool/zed
  - dotfiles
  - setup
  - harness
  - windows
aliases:
  - Claude Codeの履歴の保存場所
  - Claudeチャット履歴の移行
created: 2026-10-01
updated: 2026-10-08
sources:
  - Claude Code conversation "Claude Code のセッション履歴の復元" (2026-10-07。「履歴の移行と再開」)
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
- ZedのACP経由のチャットも、Zedの `threads.db` ではなくここに保存される（[[zed-dotfiles]]）。会話の中身はここだが、Zed 側にも `db.sqlite` の `sidebar_threads` があり、スレッドの一覧と作業フォルダはそこにある（2026-10-07 の補足。[[zed-acp]]）。
- Claude Desktop の Projects はクラウド（アカウント側）に保存され、`~/.claude` のローカル履歴とは独立している。
- `.jsonl` の構造（1応答が複数行に分かれ、同じ `message.id` と `usage` が繰り返される、など）と、履歴から作業の指標を取る方法は [[ai-work-metrics]]。

## プロジェクトを移動したとき

履歴とメモリはプロジェクトの絶対パスごとに分かれるため、プロジェクトを移動すると前のチャットやメモリが見えなくなる。

引き継ぐ方法の候補は、`projects\<旧プロジェクト名>\` の `.jsonl` と `memory\` を `projects\<新プロジェクト名>\` にコピーすること。ただし、**コピーした履歴は `claude --resume <ID>` で再開できなかった**（確認: 2026-10-06、根拠: Vault のトップを `C:\vault\notes` から `C:\vault\works` へ移したときのユーザーの発言。エラーの内容は未取得）。再開の条件は未特定。移動後は、新規のセッションを始める運用を基本にする。（2026-10-07 に解決: 原因は、picker が SDK 経由のセッションを除外していたことと、`cwd` が旧パスだったことの2つ。手順は下の「履歴の移行と再開」。）
- 旧キーは消さず、コピーで行う。旧キーが唯一の確実な履歴になる。
- コピーした `.jsonl` には、旧パスの `"cwd"`（`C:\\vault\\notes\\...` と `/c/vault/notes/...` の2形式）が入っている。`"cwd"` を新パスに書き換えて再コピーしても、再開できなかった。「`cwd` の不一致が原因」は、`cwd` だけでは足りないことが分かった。（2026-10-07 の注: 当時は一覧から開いていて、`claude --resume <ID>` で直接開けば通っていた可能性がある。仮説。未確認。）
- `cwd` を書き換えた後も、旧パスが約 1180 件残っていた。内訳は、user メッセージ 941（ほぼツールの出力）、assistant 188、`attachment` 14（`edited_text_file` 8、`instructions` 4、`environment` 2）、`last-prompt` 7。構造的な情報にあたるのは `attachment` の `environment` と `instructions` の約6件で、残りは会話の中身。再開の可否にどれが関わるかは未検証。
- 履歴全体の置換はしない。会話の内容が「`works` を `works` に」のように壊れ、記録として不適切になる。試すなら、コピーした一時キーで、構造的な部分だけを書き換える。
- 旧パスが本文に残ったまま再開できた場合の実害は、モデルが旧パスを現在のパスと取り違えて、旧ディレクトリを作り直すこと（仮説）。
- 旧パスのディレクトリを残して（または作り直して）、そこを cwd にすれば旧キーの履歴は再開できる（仮説。未試験）。旧 clone のディレクトリを削除すると、その cwd での再開ができなくなる。

2026-10-01 に、作業拠点を `C:\Users\ck\vault\notes` から `C:\vault\notes\areas_shared\exmem` へ移すときにこの方法を使った（`C--Users-ck-vault-notes` → `C--vault-notes-areas-shared-exmem`）。コピーした履歴が新しい場所で表示されるかは、未確認のまま（上の 2026-10-06 の結果から、再開は通らない可能性が高い。仮説）。

Claude Codeを起動して `projects\` に別の名前のフォルダができた場合は、プロジェクト名の仮説が外れている。そのフォルダへ `.jsonl` と `memory\` をコピーし直す。

## 履歴の移行と再開（2026-10-07 追記）

作業フォルダを別のパスへ移したあと、旧パスで作った約56本のセッション（jsonl）を、新しい構成で `claude --resume` から再開できるようにした。上の「プロジェクトを移動したとき」で未解決だった原因と、安全な手順。

### Principles（履歴の移行）

- 移動後に再開できないときは、「一覧（picker）に出ない」と「ID 指定でも読めない」を分けて調べる。理由: 今回の「再開できない」は、picker が一部のセッションを除外していたことと、`cwd` が旧パスだったことの2つが重なっていた。
- 内部形式の書き換えは、先に履歴フォルダ全体をバックアップし、書き換えるのは `cwd` や `entrypoint` などのメタ項目だけにする。理由: jsonl の形式は公式の手順ではなく、会話本文のパスを置換すると記録が壊れる。
- 履歴の復元は、非対話の `claude -p --resume <ID> --fork-session` で、読み込めるかを先に確かめる。理由: 元のセッションを変えずに、一覧に出ない原因と、読み込めない原因を切り分けられる。

### Decisions（履歴の移行。すべて 2026-10-07）

- **旧パスのセッションの `cwd` を、現在の構成に対応するパスへ書き換え、対応する保存先ディレクトリに置く**。根拠: 保存先ディレクトリ名は `cwd` から計算され、再開はそのディレクトリだけを探す。ユーザーが「できるだけ、現構造に `cwd` を一致させたい」と指示した。却下案: 旧パスのディレクトリを作り直して、そこを `cwd` にする（旧構成が残り、現在の構成と一致しない）。
- **対応先が現在の構成に無いセッションは、共有の知識置き場（exmem）の `cwd` に寄せる**。根拠: ユーザーが「寄せてください。だめならあきらめます」と指示した。一覧に出す場所が必要だった。却下案: 対応先が無いものは諦める（会話が読めなくなる）。
- **`entrypoint` を `sdk-ts` から `cli` に書き換える（1本で試してから全件）**。根拠: CLI の picker は SDK 経由のセッションを出さないため。ユーザーが1本で picker に出ることを確認してから、全件の書き換えを指示した。却下案: 毎回 `claude --resume <ID>` で指定する（一覧から選べず、ID の控えが要る）。

### Facts（履歴の移行）

- CLI の picker と `--continue` は、`claude -p` と Agent SDK で作ったセッションを除外する。ID を直接指定すれば再開できる（確認: 2026-10-07、根拠: 公式ドキュメント `code.claude.com/docs/en/sessions`）。
- Zed の ACP 経由のセッションは SDK 経由で、jsonl の `entrypoint` は `sdk-ts` だった。調べた54本すべてが `sdk-ts`（確認: 2026-10-07、根拠: jsonl の `entrypoint` を集計）。統合時（2026-10-08）の集計では、先頭付近の `entrypoint` が `sdk-ts` のファイルが62、`cli` が55（`projects` 全体のファイル数で、旧キーのコピーを含む。新しい Zed のセッションは `sdk-ts` で作られるとみられるが、再現は未実施）。
- 一覧に何も出なくても、`claude -p --resume <ID> --fork-session` は応答した（確認: 2026-10-07、根拠: 実行して `OK` が返った）。テストで増えたフォーク用の jsonl は削除した。
- `entrypoint` を `cli` に1本書き換えたら picker に出た。全件を `cli` にしたあとも、Zed のスレッド履歴から開けた（確認: 2026-10-07、根拠: ユーザーの報告）。
- 保存先ディレクトリ名は、`cwd` の英数字以外（`:` `\` `.` `_`）を `-` に置換したもの。`.obsidian` は `--obsidian` になる（確認: 2026-10-07、根拠: 移行後に picker と Zed で開けた。2026-10-08 に `projects` の一覧で `…-windows-obsidian--obsidian` を確認）。
- `claude --resume <ID>` は、現在のプロジェクト、他のプロジェクトの順に ID を探す。他のプロジェクトに同じ ID の transcript が複数あると、どれも選ばず not found になる（確認: 2026-10-07、根拠: 公式ドキュメント。実機では、重複がある状態の検証は未実施）。
- `cwd` が `.jsonl` の JSON 行ごとに入っていて、`"cwd":"C:\\..."` の形（バックスラッシュ2重）と `/c/...` の形の2通りがある（確認: 2026-10-07、根拠: jsonl の集計）。
- `projects` の保存先に、コピー前後の同じセッション ID が複数ディレクトリにあると、ディスク上のセッション数が水増しされる。ユニークな ID は56本だった（確認: 2026-10-07、根拠: ファイル名の集計）。

### Gotchas（履歴の移行）

- **作業フォルダを移したあと、`claude --resume` の画面に何も出ない（`No conversations found in this project`、または検索欄だけ）**: セッションが SDK 経由（`entrypoint: sdk-ts`）で、picker の対象外。`cwd` の不一致とは別の原因。`claude --resume <ID>` で開く。一覧から選びたいときは、`entrypoint` を `cli` に書き換える。
- **コピーしたセッションが、新しい場所で再開できない**: jsonl の `cwd` が旧パスのまま。旧パスが存在しないと、作業ディレクトリを決められない（仮説）。`cwd` の値だけを、新パスに書き換える。会話本文のパスは触らない。

### Open Questions（履歴の移行）

- 旧ディレクトリに同じセッションが残っている状態で、別のディレクトリから ID 再開すると not found になるか（公式の記述だけ。未検証）。

### Next Actions（履歴の移行）

- 数日使って問題が無ければ、履歴のバックアップと、旧ディレクトリの重複を削除する（2026-10-07 時点。旧 `C--vault-works*` のキーが残っていることを 2026-10-08 に確認）。

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
- 原因: 不明（2026-10-06 時点）。`cwd` の不一致だけではない。`cwd` 以外のフィールドの旧パス（上の「プロジェクトを移動したとき」）、キーの付け方、セッションの索引が候補（未調査）。
- 解決: 2026-10-06 時点はなし。新しいパスでは、新規のセッションを始める。旧キーの履歴は残してある。2026-10-07 に解決した（原因は picker が SDK 経由のセッションを除外していたこと。上の「履歴の移行と再開」）。

### Claude Desktop の Projects に履歴が出ない

- 原因: 不具合ではない。Desktop の Projects はクラウド、Claude Code の履歴はローカルで、保存先が別。

## Open Questions

- `~/.claude` の手書き設定のうち、`settings.json` は管理済み（dotfilesの `home/.claude/settings.json` へリンク。WSL・Windowsとも適用済み、2026-10-04 に確認。[[claude-code-permissions]]）。`CLAUDE.md` と `projects\<プロジェクト名>\memory\` をdotfilesで管理するかは未決。
- Claude Desktop の Code 機能から、ローカルの履歴が見えるか。
- 解決（2026-10-07）: `claude --resume` が通らない原因は何か。picker が SDK 経由のセッションを除外していたことと、`cwd` が旧パスだったこと（「履歴の移行と再開」）。

## Next Actions

- （2026-10-07 に解消）`--resume` が通らない原因は特定できた。上の「履歴の移行と再開」の手順を使う。構造的な旧パス（`attachment` の約6件）の書き換えは、結局試していない。
- ターミナルで `$HOME\works\resources\exmem`（2026-10-06 以前は `C:\vault\works\resources\exmem`）に移動して `claude --resume` を実行し、コピーした履歴が表示されるか確認する。あわせて、`projects\` のどちらのフォルダに書き込まれるかを確認し、使われなかった方を削除する。

## Related

- [[zed-dotfiles]]
- [[zed-acp]]
- [[obsidian-vault]]
- [[claude-code-project-settings]]
- [[ai-work-metrics]]
