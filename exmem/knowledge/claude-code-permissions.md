---
type: knowledge
title: Claude Codeの権限制御と共通土台（自走期間を伸ばす）
status: active
tags:
  - ai/claude
  - harness
  - dotfiles
  - setup
  - tool/wsl
  - windows
aliases:
  - Claude Codeの権限設計
  - 権限移譲
  - allowlist
  - サンドボックス運用
  - 自走期間
created: 2026-10-02
updated: 2026-10-02
sources:
  - Claude Code conversation "Claude Code 権限制御の設計と dotfiles への共通土台の配備" (2026-10-02)
  - "dotfiles（claude/、_scripts/links.map、l1_copy_dotfiles.sh、コミット d4878a5 / b0cca61）、%USERPROFILE%\\.claude\\settings.json、WSLの ~/.claude/settings.json（2026-10-02 に確認）"
---

# Claude Codeの権限制御と共通土台（自走期間を伸ばす）

## Purpose

Claude Codeのyes/no確認（権限プロンプト）がブロッカーになり、自走できる期間が短い。権限の仕組みを理解し、Windows / WSL / Linux で同じポリシーを使えるようにして、確認を減らす。ハーネスの「権限とサンドボックス」要素の実装にあたる（[[ai-harness-concepts]]）。

## Principles

方針（リスクの方向と取返しやすさで決める）:

| 操作 | 扱い |
|---|---|
| read方向 | allow |
| write方向で取返し可（例: commit） | allow |
| write方向で取返し不可（例: push） | 確認（ルールに当たらない既定動作に任せる） |
| 壊してよいテスト環境（サンドボックス） | 「取返し可」扱いに緩める（プロジェクト側の `.claude/settings.json`） |

- 権限を緩めるときは、失敗時の回収手段（git、チェックポイント）を対で置く（[[ai-harness-concepts]]）。
- 禁止したいことは指示ファイルではなく、権限で強制する。絶対に外さないものだけ `deny` にする。
- 任意コード実行と等価なものは allow しない（`bun run *` などのタスクランナー、インタプリタのワイルドカード）。
- 共通の土台はユーザー階層に1つだけ置き、リポジトリごとの差分だけをプロジェクト側に置く。

## 権限の仕組み（メモ記載。判定順と階層は公式の仕様に沿う）

- ルール形式: `Tool` / `Tool(指定子)`。Bashは前方一致（`:*` または ` *` のワイルドカード）。複合コマンド（`&&`、`;`、`|`）は分解され、各部分が個別に判定される。
- 判定は deny → ask → allow の順で、スコープをまたいでも ask が allow に勝つ。どのルールにも当たらないものは確認になる。
- 設定階層: managed > コマンドライン > local > project > user。denyはどこかにあれば効く。
- 権限モード: default / acceptEdits / plan / bypassPermissions。

## Decisions

### 共通の土台は `~/.claude/settings.json` に置く（実体は dotfiles の `claude/user/settings.json`）（2026-10-02）

- 根拠: 全リポジトリ共通の read + 取返し可 write をユーザー階層に集約し、OS間で共有する。
- 却下案: 各プロジェクトの `.claude/settings.json` に個別配置（重複・同期漏れ）。dotfilesの `.claude/` はgitignore対象なので管理にも向かない。

### 土台に `ask` を書かない（「どのルールにも当たらない = 確認」に任せる）

- 根拠: askがallowに勝つため、ユーザー階層に `ask: git push` を書くと、サンドボックスのプロジェクト設定でallowに緩めても確認が出続ける。「属性で緩める」方針が成立しなくなる。
- 却下案: 取返し不可を `ask` で明示する。

### allowの中身

- read: `git -C * status / log / diff / show / ls-files / remote -v / branch --show-current / check-ignore / rev-parse`、`git status / log / diff / ls-files`、PowerShellの `Get-ChildItem` / `Get-Content` / `Get-Item` / `Test-Path` / `Resolve-Path` / `Select-String` / `Select-Object` / `Sort-Object` / `Measure-Object` / `Format-Table` / `Format-List` / `Out-String`。
- 取返し可write: `git add`、`git commit`（`git -C` 付きを含む）。
- `PowerShell(...)` と `Bash(...)`（bash / zsh共通）の両方を書く。Bash側は `git -C` と add / commit のみ（`ls` / `cat` / `grep` / `find` などはClaude Codeが標準で自動許可するため不要）。
- 却下案: `ForEach-Object` / `Where-Object` のallow（スクリプトブロック内に `Remove-Item` などを包めば素通りする恐れがあり、判定の挙動が未確認）。タスクランナー・インタプリタのワイルドカード。

### 配備方法

- Windows: `_scripts/links.map` の `claude\user\settings.json|%USERPROFILE%\.claude\settings.json`（`_scripts\w2a_copy_dotfiles.bat` で適用）。
- WSL / Linux: `_scripts/l1_copy_dotfiles.sh` で `do_stow "$SRC_DIR/claude" "$DST_DIR/.claude" "user"`。既存の `~/.claude/settings.json` の退避と `~/.claude` の作成も追加した。
- ディレクトリ構成: `claude/user/settings.json`（土台。リンク対象）と `claude/settings.sandbox.json`（テンプレ。リンク対象外）を分けた。stowは「パッケージ内の全ファイル」をリンクするため、`user/` サブディレクトリで分離した。

### リンク切れsymlinkの自動削除を `l1_copy_dotfiles.sh` に追加

- 根拠: 旧パスを指すリンク切れがstowの競合になり、`set -e` で後続のstow（`claude` を含む）が実行されなかった。
- 仕様: `home/` 直下のエントリとバックアップ対象のうち、リンク切れ（`-L` かつ `! -e`）のみ `rm`。dry-runは表示のみ、`--unlink` では何もしない。実体のあるリンクや実ファイルは触らない。
- 却下案: 手動でunlink（再発する）。`--reset`（競合のため効かない）。

### サンドボックスのテンプレ（`claude/settings.sandbox.json`）

- 取返し不可のものを含め、`git push`（`origin *` 含む）、`switch` / `checkout` / `restore` / `reset` / `clean` / `stash` / `merge`、`Remove-Item` / `Move-Item` / `Copy-Item` / `New-Item`（Bash側は `rm` / `mv` / `cp` / `mkdir`）をallowする。壊してよいリポジトリの `.claude/settings.json` に置く想定。
- 状態: テンプレはあるが、**対象リポジトリへの配置はまだ**。

## Facts

### 実物との照合（2026-10-02）

- dotfilesのコミット `d4878a5`（土台 + links.map + stow + サンドボックステンプレ）と `b0cca61`（リンク切れsymlinkの削除）は実在する。`claude/user/settings.json` の allow の内容はメモの記述どおり。ほかに `"theme": "dark-ansi"` が入っている（メモに記載なし）。
- `l1_copy_dotfiles.sh` に `do_stow ... "user"`（179行目）と、リンク切れの削除（117行目付近）がある。`links.map` に該当エントリがある。
- **WSL**: `~/.claude/settings.json` は dotfilesの `claude/user/settings.json` へのシンボリックリンク（確認済み。`~/.claude` にはこのファイルだけ）。
- **Windows**: `%USERPROFILE%\.claude\settings.json` は存在し、中身は土台と同じ（1569バイト）だが、**シンボリックリンクではなく実ファイル**。`links.map` 経由のリンクはまだ適用されていない。dotfiles側を編集してもWindows側に伝わらない状態。
- dotfilesは `.claude/` をgitignoreしている。`dotfiles/.claude/settings.local.json` には「Yes, don't ask again」で自動追記された1回きりの長い複合コマンドが約30件たまっていた（再利用されない。メモによれば削除済み）。
- `/fewer-permission-prompts` は履歴（直近50ファイル上限）から読み取り系を抽出するスキル。今回は7ファイル・ほぼPowerShellツール経由で、Bashツールの呼び出しは無かった。履歴の頻出は `git -C <path> status/log/diff`（約42回）、`Select-Object` 系（約70）、`Get-*` 系（約40）、`git add/commit`（約20）、`git push`（4）、`Remove-Item -Recurse/-Force`（約15）。

### 仮説・未確認

- `Bash(git -C * ...)` が、`git -C` 付きのコマンドが標準の自動許可に含まれない可能性があるため明示した。
- `PowerShell(...)` ルールがBashと同じ前方一致・ワイルドカード規則で評価されるか。スクリプトブロック内のコマンドが個別に判定されるか。いずれも実機で未確認。

## Gotchas

### WSLで `~/.claude` が空のままだった

- 状況: ドライラン（`-n`）でも `mkdir -p` は実行されるため、ディレクトリだけ作られる。
- 原因: 8月に張られた旧パス（`/mnt/c/Users/ck/vault/...`）を指すリンク切れ9本が `stow home` の競合になり、`set -e` で `claude` のstowまで到達しなかった。
- 解決: 旧リンクをunlinkした。再発防止にリンク切れの自動削除を追加した。

### stowは「パッケージ内の全ファイル」をリンクする

- 状況: `claude/` 直下にサンドボックステンプレを置くと、それもリンクされる。
- 解決: 土台を `claude/user/` に分離した。

### 作業ツリーに他の変更が混ざっていた

- 状況: `l1_copy_dotfiles.sh` にユーザーの別作業（`config/shell` 用の2行）が混ざっていた。
- 解決: HEADを元に自分の3か所だけを再構成して indexに入れ（`git update-index --cacheinfo`）、部分コミットした。

### 「Yes, don't ask again」の許可が溜まる

- 状況: 長い複合コマンドがそのまま `settings.local.json` に追記され、再利用されない。exmemの `settings.local.json` も同じ状態だった（[[claude-code-project-settings]]）。
- 対策: 繰り返し使うものは、手で書いた `settings.json` の許可にまとめる。

### ツール側の制約

- 既存ファイルはReadしてからWrite / Editする必要がある。セッション中断でPowerShell呼び出しの結果が記録されず、削除が未反映のことがあった（状態を再確認してから再実行する）。

## Open Questions

1. サンドボックス（壊してよい）リポジトリの選定と、`claude/settings.sandbox.json` の配置方法。
2. 土台への `deny` 追加の要否（`git push --force`、`Remove-Item C:\*` など）。
3. サンドボックステンプレの `git push origin *` が `--force` にもマッチする問題への対処（`deny` で塞ぐか、パターンを絞る）。denyは他のスコープのallowに勝つので、土台に置けば効く（上の判定順より）。
4. `defaultMode: "acceptEdits"` を併用するか（Edit / Writeの確認削減）。
5. `config/` 配下（`.config/git` など）にも、リンク切れの自動削除を広げるか。
6. 土台のルールが実運用で十分か（プロンプトが減ったかの再計測）。必要なら再度 `/fewer-permission-prompts` を回して追加する。
7. 土台の `PowerShell(...)` ルールは、実機で期待どおり効いているか（仮説の検証）。

## Next Actions

- [ ] Windowsで `_scripts\w2a_copy_dotfiles.bat` を実行し、`%USERPROFILE%\.claude\settings.json` が実ファイルからシンボリックリンクに置き換わることを確認する（現状は実ファイルのコピー。WSL側は確認済み）。
- [ ] サンドボックス運用の設計（Open Questions 1〜3 を決め、テンプレを対象リポジトリの `.claude/settings.json` に配置する）。
- [ ] 土台に `deny` を追加するか決める。
- [ ] 数日使ってから `/fewer-permission-prompts` を再実行し、追加すべきread系を拾う（Bashツールの利用が増えたらBash側も）。
- [ ] 必要に応じて `defaultMode: "acceptEdits"` を検討する。

## Related

- [[claude-code-project-settings]]
- [[claude-code-storage]]
- [[ai-harness-concepts]]
- [[ai-handson-framework]]
- [[zed-dotfiles]]
- [[ai-development-workflow/context]]
