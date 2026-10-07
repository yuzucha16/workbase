---
type: project
title: AI開発ワークフロー Project Context
status: active
tags:
  - workflow
  - knowledge-management
aliases:
  - AI開発ワークフロー Project Context
created: 2026-09-26
updated: 2026-10-06
---

# AI開発ワークフロー Project Context

## Current State

- ZedにCodexとClaude AgentをACPで接続済み（[[zed-acp]]）。
- ナレッジ構成を `inbox/` → `knowledge/` → `contexts/`（旧 `projects/`）の形に整理した。会話ログは常設しない（[[ai-development-workflow]] D2）。
- 各エージェントの入口として `AGENTS.md` を置いた（D6）。
- Obsidian向けの作法を追加した。タグは `tags.md` の統制語彙による階層タグ、`aliases` で日本語名を付ける、知識一覧は `knowledge.base` で見る（D5、D9）。
- inbox → knowledge の流れを3回通した。毎回、実物との照合でメモとの食い違いが見つかった。
  - 2026-09-26: ZedへのVim環境移行のメモ → [[zed-vim]]
  - 2026-10-01: このナレッジベース整備の会話メモ → [[ai-development-workflow]]（Principles、D6〜D9、Gotchas）と [[obsidian-vault]]
  - 2026-10-01: Zedのdotfiles管理とClaudeチャット履歴のメモ → [[zed-dotfiles]] と [[claude-code-storage]]
- 2026-10-01 に作業拠点を `C:\Users\ck\vault\notes` から `C:\vault\notes\areas_shared\exmem` へ移した。
  - ナレッジベースの名前を exmem（external memory、外部メモリ）とした。AIと人間が共有するナレッジ置き場というコンセプト。
  - `areas_shared` はGitリポジトリ（yuzucha16/areas_shared）で、ナレッジベースはGit管理になった（[[obsidian-vault]]）。
  - エージェントはexmemを作業ディレクトリとして起動する。exmemの `AGENTS.md` / `CLAUDE.md` がそのまま読まれる。
  - Claude Codeの履歴とメモリを `C--vault-notes-areas-shared-exmem` へコピーした（[[claude-code-storage]]）。
  - 古い場所（`C:\Users\ck\vault`）と、Downloadsにあった整理前のコピーは削除した。
- 2026-10-02 に、inbox のメモ21件（2026-09-26〜10-02）を統合した（4回目）。実物との照合で次の食い違いが見つかった。
  - Zedのターミナルは `pwsh.exe` で、メモ（2026-09-26）の `wsl.exe` と違う。`claude-acp` に既定モデル `sonnet` も入っていた（[[zed-vim]]、[[zed-dotfiles]]）。
  - ZedのClaude Agentが起動しない問題は、PowerShellプロファイルの非対話ガードで解消済み。ガードは `profile.ps1`（dotfilesへのシンボリックリンク）の2行目にある（[[zed-acp]]）。
  - メモの `ai-handson/` と `excel-aggregation` スキルは、実際にはまだ配置されていない（[[ai-handson-framework]]、[[claude-code-vs-cowork]]）。
  - vaultのバックアップ用タスクは見当たらない。「vaultの `.git` は1つ」という記述は実物と違う（[[obsidian-vault]]）。
  - WSLには `fd` / `eza` / `broot` / `ghq` / `nvim` が入っていない（[[modern-cli-tools]]）。
- 新しい知識ファイルは、AIの設計（[[ai-harness-concepts]]、[[ai-handson-framework]]、[[ai-business-adoption]]、[[human-ai-decision-loop]]）、Office / 自動化（[[office-ai-workspace]]、[[claude-code-vs-cowork]]、[[power-automate-office-automation]]）、環境（[[wsl-file-placement]]、[[vscode-workspace]]、[[modern-cli-tools]]）、Linux（[[linux-distro-selection]]、[[linux-multiboot-setup]]）、その他（[[keyboard-switches]]）。Linux移行は別のプロジェクトにした（[[linux-home-pc/context]]）。業務適用のプロジェクトの contexts は、2026-10-08 に削除した（知識は [[ai-business-adoption]] に残る）。
- 個人的な内容の3件（転職・EQ・入社計画）は、ユーザーがexmem外のローカルへ移した。inbox は空。
- 2026-10-02 に、Claudeの自走期間を伸ばす権限制御のメモを統合した（5回目）。共通の許可ルールをdotfilesの `claude/user/settings.json`（のち `home/.claude/settings.json` に移動）に置き、WSLにはリンク済み。Windowsは同じ内容の実ファイルがあるだけで、リンクは未適用だった（2026-10-04 に両OSともリンク済みを確認。[[claude-code-permissions]]）。サンドボックス運用と `deny` は未決。
- プロジェクトの `.claude/` は、`settings.local.json` だけをignoreし、`settings.json` / `skills/` は育ったら管理下に置く方針にした（[[claude-code-project-settings]]）。リポジトリのルートに `.gitignore` を追加した。
- 2026-10-02 に、Vaultの構造を見直した（[[obsidian-vault]] Decisions）。`notes` 自体を1つのGitリポジトリにし、共有は `resources/` だけ（`.gitignore` のホワイトリスト）にする。`areas_shared` の中身は `resources/` 配下へ移した（`exmem` `cheatsheets` `handson` `office` と、`obsolete` → `_archive/obsolete`）。`exmem/projects/` は Vaultの `projects/` と衝突するため `contexts/` に改名した。リポジトリ内の配置換えとドキュメント更新までは済み、実機の配置換えは未実施。
- 2026-10-03 に、実機の移行を進め、inbox のメモ（ディレクトリ構造の見直し）を統合した（6回目）。`C:\vault\notes` は実体へのジャンクションになり、`.obsidian` と Office テンプレは dotfiles から移管済み。`resources/` 内のローカル専用は `_local/` に置く規約を追加した（[[obsidian-vault]]）。実物との照合では、`notes.lnk` が既に無いこと、`_local/` コミットが未 push であること、旧クローンと `notes_old` が残っていることを確認した。

- 2026-10-03 に、dotfiles と手順書・フォントのメモ6件を統合した（7回目）。新しい知識は [[pc-setup-manuals]]、[[fonts]]。dotfiles 固有の記録は、2026-10-04 に dotfiles リポジトリの `docs/` へ移した（exmem は作業ログを持たない）。
- 2026-10-04 に、inbox のメモ7件（exmem と他リポジトリの役割分離、Zed の設定、カーソル点滅、Notepad++、scoop、シェル履歴と fzf）を統合した（8回目）。作業ログと知識を分ける方針に沿い、再利用できる知識だけを取り込んだ（新規は [[terminal-cursor-blink]]、[[notepad-plus-plus]]、[[scoop-app-management]]、[[shell-fzf-keybindings]]。追記は [[ai-development-workflow]]、[[zed-dotfiles]]、[[zed-acp]]、[[zed-vim]]、[[shell-command-usecases]]）。個別の経緯・Next Actions は dotfiles リポジトリの `docs/` に任せた。実物との照合では、Zed の `settings.json`、カーソル点滅の3シェルの記述、fzf のキー、Notepad++ の雛形方式、`%APPDATA%\zed\themes` のジャンクションがメモと一致した。
- 2026-10-04 に、inbox のメモ9件（共通機能 workflow-kit の設計と改善の受け皿、出力のブレ対策、提案と決定の区別、履歴からの作業ログの復元、設定の置き場の判断基準、Obsidian の設定、`gh release download`）を統合した（9回目）。新規は [[workflow-kit]]、[[ai-output-consistency]]、[[app-config-placement]]、[[gh-release-download]]。追記は [[obsidian-vault]]（設定の方針・Decisions・Gotchas）、[[human-ai-decision-loop]]、[[ai-development-workflow]]、[[fonts]]（`--dry-run` の記述を現状に直した）。実物との照合では、`.obsidian` の設定ファイル、`.gitattributes`、workflow-kit の構成、`24_fonts.*` に `--dry-run` / `gh auth` が無いことがメモと一致した。食い違いは、揺れの原因の数（8点と7点）で、数え方の違いとみられる（[[ai-output-consistency]]）。`contexts/` の位置づけが「`notes` から見えない場所の作業を引き継ぐコンテキスト」になった。
- 2026-10-04 に、inbox のメモ2件（アプリが自動で書き換えるファイルの追跡の判断基準、並行セッションと統合時の整合）を統合した（10回目）。前者は [[app-config-placement]] に5項目の基準として、後者は [[ai-development-workflow]] の新章に入れた。メモの Open Questions を作業ログ（`notes/docs/`）と照合し、「追記分を新しいタグのコミットに含める運用」が決定済みであることを確認した。`colored-tags` の `data.json` の78タグ・追跡状態・LF は実物と一致した。統合手順に照合の工程を足すかは、ユーザーの判断待ち（[[ai-development-workflow]] の Open Questions）。
- 2026-10-06 に、inbox のメモ3件（WSL でのシェルスクリプト試験、エージェントのコミットの身元とトレーラー、改行コードと `.gitattributes`）を統合した（11回目）。新規は [[shell-script-testing-wsl]]、[[git-line-endings]]。追記は [[workflow-kit]]（コミットの身元の Decisions、Gotchas、Open Questions）と [[pc-setup-manuals]]（`lib.sh` の関数が7つに増えた旨）。実物との照合では、kit の `docs-rules.md` のトレーラー規則と版 `2026-10-06.1`、`core.autocrlf` の設定（システム `true`、ユーザー `false`）がメモと一致した。dotfiles の実物は見つからず、試験メモの内容は未再確認（仮説扱いで記録）。
- 2026-10-05〜06 に、inbox のメモ9件を統合した（12回目）。Vault の構造変更の6件（共有とローカルの分離、検索の見える範囲、filter-repo での切り出し、Obsidian のファイル一覧の色、コミット権限の委譲、AI と構造変更を進める教訓）は、新規 [[git-subdirectory-split]]、[[obsidian-appearance]] と、追記 [[obsidian-vault]]（設計の原則、Gotchas）、[[modern-cli-tools]]（検索の見える範囲）、[[workflow-kit]]、[[claude-code-permissions]]、[[human-ai-decision-loop]]、[[wsl-file-placement]]。2026-10-06 の3件（Scoop 導入の失敗と実行ポリシー、Windows バッチの試験、rebase の時系列確認）は、新規 [[git-rebase-chronology]]、追記 [[scoop-app-management]]、[[shell-script-testing-wsl]]。実物との照合では、`.ignore` の `!/resources/`、`.gitattributes`、dotfiles の allow（`git add` / `git commit`、push なし）、スニペットの色指定、`20_apps.bat` の `PS_EXE` と実行ポリシーの条件、`tests/windows/` `tests/linux/` の存在、dotfiles の `AGENTS.md` の rebase の規則がメモと一致した。食い違いは `lib.sh` の関数の数（メモは7つ、実物は `distro_ids` を含めて8つ。[[pc-setup-manuals]] に注記）。

## Next Actions

- ユーザーが `git config --global user.name` / `user.email` を設定し、その後、作者 agent・コミッター人間の分離を採用するか決める（[[workflow-kit]]）。
- 他の PC で `git pull` したあと `git ls-files --eol` を確認する。clone 前の git 設定の順序を手順書に書くか判断する（[[git-line-endings]]）。
- シェルスクリプトの試験の置き場（dotfiles の `tests/` など）と `PROC_VERSION_FILE` の扱いを決める。ネイティブ Linux 実機で確認する（[[shell-script-testing-wsl]]）。

- 新しい業務用 PC で、dotfiles の `50_repos` から「workflowを導入して」までの順で Vault の構造を再現し、新しい Windows アカウントで `20_apps.bat` の Scoop 導入を確認する（[[obsidian-vault]]、[[scoop-app-management]]）。旧 `notes` のローカルのリポジトリとバックアップを、いつまで残すか決める。
- 他のプロジェクト（`linux-home-pc`、`zed-vim-migration`）の `contexts/` を、リポジトリ側に持つ形へ寄せるか、exmem 内で完結するものは残すかを決める（[[ai-development-workflow]] の「他リポジトリとの関係」）。
- **Vault構造の移行を完了する**（[[obsidian-vault]] 移行の状況）。順序の制約: GitHub rename → 配置換え。
  1. 済み（2026-10-02）: GitHub で `notes` に rename、リポジトリ内の配置換え。
  2. 済み（2026-10-03）: `C:\vault\notes` を実体 `C:\vault\repos\github.com\yuzucha16\notes` へのジャンクションにした（それまでは `notes.lnk` というショートカットで、パスとして使えなかった）。`.obsidian` の取り込み、dotfiles 側の `windows/office` `windows/obsidian` の削除、`links.map` の書き換え、Office のリンク張り直しも済み（[[obsidian-vault]]）。
  3. 済み（2026-10-06）: Obsidian で `$HOME\works`（`notes` から rename し、`C:\vault\works` から移した）を Vault として開き直した。確認事項: `knowledge.base` の一覧が表示されるか確認する。
  4. 旧 `exmem/`（`areas_shared` クローン側）は削除してよい。Claude Code の履歴とメモリを新しい作業パス（`$HOME\works\resources\exmem`）のフォルダへコピーし直す（[[claude-code-storage]]）。Zed のプロジェクトも開き直す。
  5. `C:\vault\notes_old` と旧クローン `C:\vault\repos\github.com\yuzucha16\areas_shared` を削除する（`notes.lnk` は削除済み。旧クローン内の `exmem\.claude\settings.local.json` は残す価値がない）。
  - `_local/` コミット（`27d1d08`）を push する（`origin/main` より1つ先、2026-10-03 確認）。
  6. `resources/fonts/` に HackGen Console NF Regular とライセンス文書を置いてコミットする（Git LFS、`README.md` の「版」を記入）。
  7. 済み（2026-10-03）: `resources/` 内のローカル専用データは `_local/`（どの階層でも）に置くと決めた。`resources/` `exmem/` `cheatsheets/` `handson/` `office/` に作成済み。残りは、`areas/` との使い分け基準だけ（[[obsidian-vault]]）。
- Zedで exmem をプロジェクトとして開き、Claude Agentが exmem の `AGENTS.md` を読んでいるか確認する（「exmemって何？」と聞く）。
- ターミナルで exmem に移動して `claude --resume` を実行し、コピーした履歴とメモリが引き継がれているか確認する（[[claude-code-storage]]）。
- `knowledge.base` をObsidianで開き、一覧が表示されるか確認する。
- モバイルで壁打ちし、Obsidianモバイルアプリで inbox に保存して、Sync経由でPCに届くか試す（D4の検証）。
- Obsidianの設定変更（新規ノートの保存先・日付型・テンプレート）を判断する（[[obsidian-vault]] Proposals）。
- Copilotを接続する。
- ZedのWSL連携方式と、開発リポジトリをWindows側（`C:\vault\repos`）に置くかWSL側に置くかを決める（[[wsl-file-placement]]）。
- vaultのバックアップ（robocopy + タスクスケジューラ）を設定する（[[obsidian-vault]]）。
- Zedで `claude-acp` が起動しない問題が再発したら、まずシェルのプロファイル出力を疑う（[[zed-acp]]）。
- サンドボックス運用、`deny`、`acceptEdits` を決める。数日使って `/fewer-permission-prompts` を再実行する（[[claude-code-permissions]]）。

## Goal

モバイルでのAI壁打ちをPC上のAI開発環境へ継続的に引き継ぐ。

## Current Architecture

```text
Mobile AI
  -> inbox (Markdown)
  -> knowledge / project context
  -> Obsidian / Git
  -> Zed
  -> ACP Agents
  -> Implementation / Validation
```

## Current Agents

- Codex via ACP
- Claude Agent via ACP
- 将来的にCopilot等も想定

## Source of Truth

AIサービスのチャット履歴ではなく、Markdownで管理するプロジェクト知識をSource of Truthとする。

## Current Decisions

- 会話ログは常設せず、根拠とハマりどころを知識へ統合する
- MarkdownをAI横断フォーマットとする
- Obsidianをナレッジ管理UIとして利用する
- ZedをPC側のAI開発UIとして利用する
- エージェントの入口は `AGENTS.md` に一本化する

## Open Questions

- GitとObsidian Syncをどう使い分けるか。exmemは `notes` リポジトリでGit管理され、VaultではObsidian Syncも有効になっている（`_local/` もSyncされるかは未検証）。
- Vault移行まわりの未決（`areas/` と `_local/` の基準、`notes` の公開範囲、バックアップ対象、`w2a` / `w4` の扱い）は [[obsidian-vault]] の Open Questions を見る。
- プロジェクトコンテキストをどこまで自動生成するか
