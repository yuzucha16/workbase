---
type: index
title: exmem
status: active
tags:
  - knowledge-management
  - workflow
  - tool/obsidian
aliases:
  - external memory
  - 外部メモリ
created: 2026-09-26
updated: 2026-10-04
---

# exmem

exmem は external memory（外部メモリ）の略。AIと人間が共有するナレッジ置き場。

## 目的

AIとの壁打ちや作業から得た知識をここに蓄え、モバイル / PC、ChatGPT / Claude / Codex / Copilot と環境が変わっても、同じ知識を引き継いで使えるようにする。
AIサービスの会話履歴やメモリに知識を閉じ込めず、Markdownの外部メモリとして持つ。

基本方針は、**会話ログを溜めずに、知識として育てる**こと。
会話の根拠（なぜそう決めたか）とハマりどころは、知識ファイルの中に残す。

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する
- `knowledge/`: AIをまたいで再利用する知識。1ファイル1トピック
- `contexts/`: 個別プロジェクトの現在状態と次にやること（Vault の PARA の `projects/` とは別物）

exmem はナレッジの置き場で、他リポジトリの作業ログは置かない。dotfiles は exmem を基本は読み取り専用で参照するだけ（例外は、ユーザーの指示で `inbox/` に知識メモを置くことだけ）で、dotfiles の作業の経緯・決定・次にやることは dotfiles リポジトリの `docs/` が持つ（2026-10-04 に `knowledge/dotfiles.md` と `contexts/dotfiles/` を移して削除した）。

## ディレクトリ構造

場所は `C:\vault\works\resources\exmem`（Obsidian Vault `C:\vault\works` の `resources/` に clone した、共有リポジトリ `workbase` の一部）。`C:\vault\works`（Vault のトップ）は別の、PC ローカルのリポジトリ（[[obsidian-vault]]）。
AIエージェントはこのディレクトリを作業ディレクトリとして起動する。

```text
exmem/                 # resources/exmem/
├── README.md
├── AGENTS.md          # 全エージェント共通の入口・書き方ルール
├── CLAUDE.md          # @AGENTS.md を読み込むだけ
├── tags.md            # タグの語彙とルール
├── knowledge.base     # Obsidian Bases: 知識・プロジェクトの一覧表
├── inbox/
│   └── README.md      # モバイル用の引き継ぎプロンプト
├── knowledge/
│   ├── ai-business-adoption.md          # AI活用の業務適用（ROI・習得工程）
│   ├── ai-development-workflow.md       # exmem自体の設計
│   ├── ai-output-consistency.md         # AIの出力のブレを抑える設計と校正の進め方
│   ├── ai-handson-framework.md          # ハンズオン設計・情報ダイジェスト
│   ├── ai-harness-concepts.md           # モデルとハーネス
│   ├── app-config-placement.md          # アプリの設定ディレクトリを置くリポジトリの判断基準
│   ├── claude-code-permissions.md       # 権限制御と共通土台（自走期間）
│   ├── claude-code-project-settings.md  # .claude/ の管理方針
│   ├── claude-code-storage.md
│   ├── claude-code-vs-cowork.md
│   ├── fonts.md                         # メインフォントの選定と導入
│   ├── gh-release-download.md           # gh release download は未ログインでも使える
│   ├── git-line-endings.md              # 改行コードを .gitattributes で決める
│   ├── git-rebase-chronology.md         # rebase の前にコミットの時系列を確認する
│   ├── git-subdirectory-split.md        # 履歴を保ってサブディレクトリを別リポジトリに切り出す（git filter-repo）
│   ├── human-ai-decision-loop.md
│   ├── keyboard-switches.md
│   ├── linux-distro-selection.md
│   ├── linux-multiboot-setup.md
│   ├── modern-cli-tools.md
│   ├── obsidian-appearance.md           # ファイル一覧の色分けと、CSS で変えられない範囲
│   ├── obsidian-vault.md
│   ├── office-ai-workspace.md
│   ├── pc-setup-manuals.md              # Win11 / Debian系の環境セットアップ手順書
│   ├── notepad-plus-plus.md             # Notepad++（scoop版）の設定管理（config.xmlの雛形方式）
│   ├── power-automate-office-automation.md
│   ├── scoop-app-management.md          # scoopを正本にしたアプリ管理と管理外の最小化
│   ├── shell-command-usecases.md        # コマンド利用傾向とヒストリの種（dotfilesの種ファイルの正本）
│   ├── shell-fzf-keybindings.md         # fzfとキー割り当て（pwsh/zsh/bash）
│   ├── shell-script-testing-wsl.md      # WSL・Windowsバッチのスクリプトを試験する（偽のHOME・環境判定の差し替え・dry-run）
│   ├── terminal-cursor-blink.md         # カーソル点滅を止める（DECSCUSR）
│   ├── vscode-workspace.md
│   ├── workflow-kit.md                  # 作業ログとナレッジ化フックの共通機能の設計
│   ├── wsl-file-placement.md
│   ├── zed-acp.md
│   ├── zed-dotfiles.md
│   └── zed-vim.md
└── contexts/
    ├── ai-business-adoption/
    │   └── context.md
    ├── ai-development-workflow/
    │   └── context.md
    ├── linux-home-pc/
    │   └── context.md
    └── zed-vim-migration/
        └── context.md
```

exmem自体の設計（会話と知識の扱い、AIをまたぐ原則など）は `knowledge/ai-development-workflow.md` にある。
Zed ACPは独立したプロジェクトではなく、AI開発ワークフローを構成する要素の一つとして `knowledge/zed-acp.md` で扱う。

## AI横断性

これらのMarkdownは、特定AIの固有フォーマットを前提にしない。

- Claude
- Codex / GPT
- GitHub Copilot
- その他のMarkdownを読めるAI

が同じファイルをコンテキストとして利用できることを前提とする。

エージェント向けのルールは `AGENTS.md` に一本化する。AI固有の設定が必要な場合は、知識本文ではなく各ツール側の設定として分離する。

## 運用ルール

1. 壁打ちの最後に `inbox/README.md` のプロンプトで要点をまとめさせ、Obsidianモバイルアプリで `inbox/` に保存する。
2. inbox のメモから決定・根拠・ハマりどころ・未決事項を `knowledge/` に統合し、メモは削除する。
3. プロジェクト固有の現在状態は `contexts/<project>/context.md` に集約する。
4. 作業の終わりに `context.md` の `Current State` と `Next Actions` を更新する。
5. AIを変更しても読めるよう、Markdown + YAML frontmatter + 通常の見出しを基本とする。

詳しい書き方は `AGENTS.md` を参照。
