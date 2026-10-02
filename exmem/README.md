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
updated: 2026-10-02
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

## ディレクトリ構造

場所は `C:\vault\notes\resources\exmem`（Obsidian Vault `C:\vault\notes` の中）。`C:\vault\notes` 全体が `notes` リポジトリで、共有対象は `resources/` だけ（[[obsidian-vault]]）。
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
│   ├── ai-handson-framework.md          # ハンズオン設計・情報ダイジェスト
│   ├── ai-harness-concepts.md           # モデルとハーネス
│   ├── claude-code-permissions.md       # 権限制御と共通土台（自走期間）
│   ├── claude-code-project-settings.md  # .claude/ の管理方針
│   ├── claude-code-storage.md
│   ├── claude-code-vs-cowork.md
│   ├── human-ai-decision-loop.md
│   ├── keyboard-switches.md
│   ├── linux-distro-selection.md
│   ├── linux-multiboot-setup.md
│   ├── modern-cli-tools.md
│   ├── obsidian-vault.md
│   ├── office-ai-workspace.md
│   ├── power-automate-office-automation.md
│   ├── vscode-workspace.md
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
