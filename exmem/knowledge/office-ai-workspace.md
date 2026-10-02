---
type: knowledge
title: Office成果物をAIで作る作業環境とデータ配置
status: active
tags:
  - office
  - tool/excel
  - workflow
  - context-engineering
  - ai/claude
  - ai/copilot
aliases:
  - Office成果物の作業環境
  - xlsx/pptxのAI作業設計
  - Master/view分離
created: 2026-10-02
updated: 2026-10-02
sources:
  - Claude conversation "Office成果物(xlsx/pptx)をAIで作る作業環境とデータ配置の設計" (2026-10-02)
---

# Office成果物をAIで作る作業環境とデータ配置

## Purpose

コードはZed / VS Code + ACPでAIを組み込めるが、最終形がxlsx / pptxになる業務（現状は既存Excelの再集計が中心、次に報告資料）で、AIを前提としたツール構成・手順・ディレクトリ設計を、我流ではなくベストプラクティスとして固める。AIエージェントはCopilotかClaudeが前提。

## Principles

- 「中身と見た目を分け、最後だけOffice側で仕上げる」一方向フローにする。
- 日常のアプリは「エディタ（Zed / Obsidian）・エージェント（Claude Code / Cowork）・Office」の3つに収める。
- 公式スキルは書き換えず、その上に自分用スキルを追加する（本家更新を取り込みやすい）。我流のスキルは作らない。
- CLAUDE.mdには常に守るルール、スキルには特定作業の手順（必要時のみ読み込み）。
- 真実の置き場は1か所にし、リンクで参照する。vault全体や `~` 全体をAIの作業範囲にしない（無関係なノートで精度・コストが悪化する）。

## Decisions

### 一方向フロー（2026-10-02）

- 流れ: 骨子・データをMarkdown / CSVで作る → テンプレ（.potx、書式済みxlsx）を用意 → エージェントでファイル化 → 最終微調整は人かOffice内AI。
- 根拠: pptx / xlsxはバイナリでdiff・レビューしづらく、AIに直接いじらせると再現性が落ちる。
- 却下案: pptx / xlsxを直してMarkdownに戻す往復運用（情報が二重化して破綻する）。
- 候補止まり: pptxをMarp / Slidevでテキスト管理して書き出す。デザイン自由度が落ちる。

### Excel業務は「Master / viewシート分離」を先に行い、Excel内のAIで完結させる

- Master: 生データ層（テーブル化、1行1レコード、書式・集計なし）。view: XLOOKUP / SUMIFS / FILTER やピボットでMasterを参照するだけ。
- 根拠: 現状は分かれておらず再利用性が低い。分離すればAIも数式を安定して書け、以降の指示が「viewを1枚追加して」で済む。
- 使い分け: 数式・ピボット・書式・既存表の整形は Claude in Excel / Excel内Copilot。毎回同じ変換や大量データの前処理だけClaude Code + Python（openpyxl等）でスクリプト化（[[claude-code-vs-cowork]]）。
- 却下案: Claude Desktopでプロンプト → 生成 → Excel反映の往復（アプリの行き来が多い）。
- 資料作成（pptx）も同じ考え方で、PowerPoint内のClaude / Copilotを最少構成とする。

### 作業記録をMarkdownで残す「フォルダ + エディタ + エージェント」構成

案件フォルダ:

```text
案件名/
  CLAUDE.md   # AIへの常設指示（ルール、命名、ログの書き方）
  log/        # 作業記録（日付ごとのMarkdown）
  notes/      # 骨子、集計方針、スライド構成などの途中成果物
  src/        # 元データ（既存Excelは原本として保管、触らない）
  out/        # 最終成果物（xlsx, pptx）
```

- 作業ログはCLAUDE.mdに「作業のたびにlog/へ目的・入力・実施内容・出力ファイルを追記」と書いてAIに自動記録させる。
- 運用ルール: 原本は `src/` に置きコピーで作業し、更新対象は `out/` のみ。Office内AIで手直しした場合はxlsx / pptxが正になるため、変更内容を一行だけlogに残す。

### anthropics/skillsをベースに拡張する

- 自分用スキル候補: ①master-view分離手順 ②作業ログ形式 ③社内テンプレ（potx / 書式済みxlsxの場所、命名規則、配色）。
- 最初に作るのはmaster-view分離スキル（今の集計業務に最も効く）。作成には `skill-creator` スキルを使える。

### データ配置: 物理統合せず、AIの作業ディレクトリ単位でつなぐ

- vault（PARA、Obsidian）は現状維持。案件フォルダはPARAの `Projects/案件名/` に置いてAIの作業場にする。
- コード / dotfilesはghq配下のまま。案件からはノートにパス・リポジトリ名を書いて参照する。横断参照が必要なときだけClaude Codeの `--add-dir` やエディタのワークスペース追加で範囲を広げる。
- vaultと案件に短い `CLAUDE.md`（Copilotも読むなら `AGENTS.md` で共通化）を置く。内容は構成説明と「原本は触らない」等のルールのみ。
- vaultのテキストはgit管理。xlsx / pptxはgitと相性が悪いため `src/` と `out/` は `.gitignore` し、バックアップ / クラウド同期に任せる（差分を残したいものだけGit LFSを検討）。
- 却下案: ghqリポジトリをvaultに入れる（`.git` やnode_modulesが検索・インデックスを汚す）。vaultをghq配下に混ぜる（`host/owner/repo` の規則と噛み合わない）。dotfilesまで含めて統合する（トークン混入のリスク。AIに見せる範囲は絞るほうが安全）。

## Facts

- 確認済み（ユーザー発言）: 現在は集計表の仕事が多く、既存Excelをさらに集計する業務。Master / viewが分かれていない。Obsidianでテキストを主にPARA構造で管理し、コード・dotfilesはghq + gitで別ディレクトリ管理。両者は別々に運用している。
- 確認済み（メモ記載）: Excelで開いているファイルはエージェントから書き換えられない（ロックされる）。
- 確認済み（メモ記載）: スキルはClaude側の仕組みで、Office内のCopilotには効かない。
- **実物との照合（2026-10-02）**: 実際の配置はメモの想定と少し違う。vaultは `C:\vault\notes`、リポジトリは `C:\vault\repos\github.com\yuzucha16\`（`areas_shared` と `dotfiles`）にあり、`areas_shared` と `.obsidian` はジャンクションでvaultに入っている（[[obsidian-vault]]）。「コードをvaultに入れない」の原則に対し、`areas_shared` は例外的にvaultへ入れたリポジトリ（exmem）。
- 仮説: anthropics/skillsのdocx / pptx / xlsx / pdfスキルは通常のOSSと異なるライセンス条件の可能性がある。改変・社内配布の前に要確認。
- 仮説: 会社のMicrosoft 365にCopilotライセンスがあるかで、Copilot統一かClaude併用かが変わる。

## Gotchas

- Excelで開いたままのxlsxにエージェントが書き込めない → 生成・保存してから開く順番にする。
- Office内AIで手直しすると記録が途切れる → xlsx / pptxを正とし、変更の要点を一行だけlogに追記する。
- vaultにコードリポジトリを混ぜると検索が汚れる → 物理統合せず、案件フォルダ単位で参照をつなぐ。
- Copilotにはスキルが効かない → 書式・配色・ルールはテンプレ側に埋め込む。

## Open Questions

- 会社のMicrosoft 365にCopilotライセンスがあるか。
- anthropics/skillsの各スキルのライセンス条件と、社内利用・改変時の扱い。
- xlsx / pptxの履歴管理（クラウド同期のバージョン履歴で足りるか、Git LFSを使うか）。
- 既存の集計ブックをMaster / viewへ分離する際、どのブックから着手するか。
- 将来の報告資料は、PowerPoint内AIで足りるか、Marp / Slidevに寄せるか。

## Next Actions

1. vaultに `Projects/<案件名>/` を1つ作り、`CLAUDE.md`（または `AGENTS.md`）・`log/`・`notes/`・`src/`・`out/` を用意してAIの作業場として試す。
2. 既存の集計ブック1つを `src/` に原本として置き、コピーをMaster / view分離する（Excel内AIで実施）。
3. `skill-creator` で、master-view分離スキルのたたき台を作る（[[claude-code-vs-cowork]] の `excel-aggregation` と整理する）。
4. 作業ログ形式（目的・入力・実施内容・出力ファイル）をCLAUDE.mdに書いて、実際に回して調整する。
5. anthropics/skillsのライセンス表記と、会社のCopilotライセンスの有無を確認する。

## Related

- [[claude-code-vs-cowork]]
- [[power-automate-office-automation]]
- [[ai-handson-framework]]
- [[obsidian-vault]]
- [[ai-business-adoption/context]]
