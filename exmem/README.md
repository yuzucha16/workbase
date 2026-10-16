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
updated: 2026-10-16
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

場所は `$HOME\works\resources\exmem`（共有リポジトリ `workbase` の一部。通常は Obsidian Vault の `resources/` として clone される。Vault の配置は [[obsidian-vault]]）。
AIエージェントはこのディレクトリを作業ディレクトリとして起動する。

```text
exmem/                 # resources/exmem/
├── README.md
├── AGENTS.md          # 全エージェント共通の入口・書き方ルール
├── CLAUDE.md          # @AGENTS.md を読み込むだけ
├── tags.md            # タグの語彙とルール
├── exmem-index.md     # 知識の索引（探すときの入口）
├── knowledge.base     # Obsidian Bases: 知識と inbox の一覧表
├── inbox/
│   └── README.md      # モバイル用の引き継ぎプロンプト
└── lessons/           # 1ファイル1トピック。一覧は `exmem-index.md`
```

exmem自体の設計（会話と知識の扱い、AIをまたぐ原則など）は `lessons/ai-development-workflow.md` にある。
Zed ACPは独立したプロジェクトではなく、AI開発ワークフローを構成する要素の一つとして `lessons/zed-acp.md` で扱う。

## 知識の索引

探すときは [[exmem-index]] から。1件1行。新しい知識ファイルを作ったら、そこに1行足す。

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
