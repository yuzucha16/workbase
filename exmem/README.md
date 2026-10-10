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
updated: 2026-10-10
---

# exmem

exmem は external memory（外部メモリ）の略。AIと人間が共有するナレッジ置き場。

## 目的

AIとの壁打ちや作業から得た知識をここに蓄え、モバイル / PC、ChatGPT / Claude / Codex / Copilot と環境が変わっても、同じ知識を引き継いで使えるようにする。
AIサービスの会話履歴やメモリに知識を閉じ込めず、Markdownの外部メモリとして持つ。

基本方針は、**会話ログを溜めずに、知識として育てる**こと。
会話の根拠（なぜそう決めたか）とハマりどころは、知識ファイルの中に残す。

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する
- `lessons/`: AI が今後の参考にする、判断・原則・落とし穴の記録。1ファイル1トピック（旧名 `knowledge/`。2026-10-10 に改名）

人が手順や仕組みを思い出すための文書は、exmem の外の `guides/`（`howto/` 手順書、`explain/` 理解ガイド、`quickref/` クイックリファレンス）に置く。作り方は [[reference-doc-types]]。

exmem はナレッジの置き場で、他リポジトリの作業ログは置かない。dotfiles は exmem を基本は読み取り専用で参照するだけ（例外は、ユーザーの指示で `inbox/` に知識メモを置くことだけ）で、dotfiles の作業の経緯・決定・次にやることは dotfiles リポジトリの `docs/` が持つ（2026-10-04 に `knowledge/dotfiles.md`（現 `lessons/`）と `contexts/dotfiles/` を移して削除した）。`contexts/`（作業の引継ぎ用）自体も 2026-10-10 に廃止した（[[ai-development-workflow]] D10）。

## ディレクトリ構造

場所は `$HOME\works\resources\exmem`（Obsidian Vault `$HOME\works` の `resources/` に clone した、共有リポジトリ `workbase` の一部）。`$HOME\works`（Vault のトップ）は別の、PC ローカルのリポジトリ（[[obsidian-vault]]）。
AIエージェントはこのディレクトリを作業ディレクトリとして起動する。

```text
exmem/                 # resources/exmem/
├── README.md
├── AGENTS.md          # 全エージェント共通の入口・書き方ルール
├── CLAUDE.md          # @AGENTS.md を読み込むだけ
├── tags.md            # タグの語彙とルール
├── knowledge.base     # Obsidian Bases: 知識と inbox の一覧表
├── inbox/
│   └── README.md      # モバイル用の引き継ぎプロンプト
└── lessons/           # 1ファイル1トピック。一覧は下の「知識の索引」
```

exmem自体の設計（会話と知識の扱い、AIをまたぐ原則など）は `lessons/ai-development-workflow.md` にある。
Zed ACPは独立したプロジェクトではなく、AI開発ワークフローを構成する要素の一つとして `lessons/zed-acp.md` で扱う。

## 知識の索引（探すときは、ここから）

1件1行（タイトルは各ファイルの frontmatter の `title`）。新しい知識ファイルを作ったら、1行足す。

- [[ai-business-adoption]]: AI活用の業務負荷削減と習得工程
- [[ai-development-workflow]]: AI開発ワークフロー
- [[abstract-concrete-matrix-review]]: 抽象と具体の手順書群を、横並びの表で整理し、揃える範囲を決める
- [[accretion-without-pruning]]: 足す経路と畳む経路の非対称を防ぐ
- [[ai-handson-framework]]: AI活用ハンズオンの設計と情報ダイジェスト
- [[ai-harness-concepts]]: AIエージェントのモデルとハーネス
- [[ai-output-consistency]]: AIの出力のブレを抑える設計と校正の進め方
- [[ai-work-metrics]]: AI 活用の指標を会話履歴から測る
- [[app-config-placement]]: アプリの設定ディレクトリを置くリポジトリの判断基準
- [[claude-code-permissions]]: Claude Codeの権限制御と共通土台（自走期間を伸ばす）
- [[claude-code-project-settings]]: プロジェクトの .claude/ の管理方針
- [[claude-code-storage]]: Claude Codeのチャット履歴とメモリの保存場所
- [[claude-code-vs-cowork]]: Claude CodeとCoworkの使い分け（Windows）とExcelスキル
- [[dotfiles-shell-tuning]]: dotfiles の起動時間・WSL の見た目・追跡方針
- [[embedded-c-constraint-checks]]: 組込み C の制約を機械で検査する
- [[fonts]]: フォントの選定と導入
- [[gh-release-download]]: gh release download は未ログインでも使える
- [[git-line-endings]]: Git の改行コードを .gitattributes で決める
- [[git-rebase-chronology]]: rebase の前にコミットの時系列を確認する
- [[git-subdirectory-split]]: 履歴を保ってサブディレクトリを別リポジトリに切り出す（git filter-repo）
- [[human-ai-decision-loop]]: 人間とAIの意思決定ループ（Decision Loop）
- [[keyboard-switches]]: キーボードのスイッチの好みとスタビラトル対策
- [[layered-third-party-review]]: 仕組みの層別・第三者レビューの進め方
- [[linux-distro-selection]]: 自宅PCのLinuxディストロ選定
- [[linux-multiboot-setup]]: 256GB SSDのマルチブートLinux構成（MX Linuxインストール）
- [[modern-cli-tools]]: modern CLIツールの役割整理
- [[notepad-plus-plus]]: Notepad++（scoop 版）の設定管理
- [[obsidian-appearance]]: Obsidian のファイル一覧の色分けと、CSS で変えられない範囲
- [[obsidian-vault]]: Obsidian Vault
- [[office-ai-workspace]]: Office成果物をAIで作る作業環境とデータ配置
- [[para-operations]]: PARA の運用と、AI の質問・提案の指標
- [[pc-setup-manuals]]: 環境セットアップ手順書（Win11 / Debian系）
- [[power-automate-office-automation]]: Power Automate / Office Scriptsによる業務自動化
- [[reference-doc-types]]: 人が見る文書の3種類（手順書・理解ガイド・クイックリファレンス）の作り方
- [[scoop-app-management]]: Windows のアプリを scoop で管理し、管理外を最小にする
- [[shell-command-usecases]]: ターミナルのコマンド利用傾向とヒストリの種
- [[shell-fzf-keybindings]]: シェルの fzf とキー割り当て（pwsh / zsh / bash）
- [[shell-script-testing-wsl]]: WSL でシェルスクリプトを試験する
- [[terminal-cursor-blink]]: ターミナルのカーソル点滅を止める（DECSCUSR）
- [[vscode-workspace]]: VS Codeの拡張機能とWorkspace運用
- [[windows-cli-pitfalls]]: Windows の PowerShell・バッチ・git 操作の落とし穴
- [[workflow-kit]]: 作業ログとナレッジ化フックの共通機能（workflow-kit）
- [[wsl-file-placement]]: ZedとWSLのファイル配置方針
- [[zed-acp]]: Zed ACP
- [[zed-dotfiles]]: Zedのdotfiles管理
- [[zed-vim]]: Zed Vim環境

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
2. inbox のメモから決定・根拠・ハマりどころ・未決事項を `lessons/` に統合し、メモは削除する。
3. 未完の項目は、該当する `lessons/` のノートの `Open Questions` / `Next Actions` に書く（作業ディレクトリの作業ログは、各ディレクトリの `docs/` が持つ）。
4. AIを変更しても読めるよう、Markdown + YAML frontmatter + 通常の見出しを基本とする。

詳しい書き方は `AGENTS.md` を参照。
