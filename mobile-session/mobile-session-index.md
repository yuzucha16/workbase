# mobile-session

モバイル（クラウド）のセッションで検討したことを、リポジトリのあるデバイス（PC）のセッションに引き継ぐ置き場。

## 使い方

- 話題ごとにディレクトリを作る（例: `ai-workspace-boundary/`）。
- 各ディレクトリの入口は `*-handover.md`（背景・決定・必要情報）と `*-next-steps.md`（次のステップ）の2つ。詳細な設計ノートは同じディレクトリに置く。
- 話題が長く続いて、引き継ぎが増えたら、**窓口 `*-start-here.md`** を1つ置く（読む順、最初にやること、リポジトリにないローカルの状態、作業の約束）。新しいセッションには、窓口だけを渡せば足りる。状態の正本は、窓口でなく roadmap や各引き継ぎに置き、窓口に写さない。
- ファイル名は、リポジトリ内で一意にする（wikilink が最短パスで解決されるため）。
- 引き継いだ内容を正式な場所（`exmem/lessons/`、`workflow-kit/` など）へ反映したら、その話題ディレクトリは削除してよい（履歴は git に残る）。

## 話題

| ディレクトリ | 内容 | 状態 |
|---|---|---|
| `ai-workspace-boundary/` | AI に見せる領域・見せない領域の境界（AI 作業部屋の設計）。**入口は [[ai-room-start-here]]** | 設計・実装は大半が済み、PC での実機の確認と実 Project での試行が残る（2026-10-14。正本は [[ai-room-roadmap]]） |
| `dotfiles-boundary/` | workbase と dotfiles の切り分け（dotfiles の挙動を書いた手順書を dotfiles へ移す） | 方針と洗い出しを終え、PC で反映へ（2026-10-12） |
| `improvement-methods/` | 作業の進め方の型（やり方集、取扱説明書、`start` のモード） | inbox と kit まで反映済み。PC で点検・試用・統合へ（2026-10-14） |
| `kit-growth/` | workflow-kit の育て方（PC1 と PC2 が別の前提で、改善の受け皿を `topics/` に置く）。入口は [[kit-growth-handover]] | 方向は合意。ai-workspace-boundary と `topics/` への改名の後に着手（2026-10-15） |
