---
type: knowledge
title: AI活用の業務負荷削減と習得工程
status: active
tags:
  - agent-design
  - automation
  - workflow
  - ai/chatgpt
aliases:
  - AI活用の費用対効果
  - 実務ROIファースト
  - AI業務適用の習得工程
created: 2026-10-02
updated: 2026-10-02
sources:
  - ChatGPT conversation "AI活用の業務負荷削減と習得工程設計" (2026-10-02)
---

# AI活用の業務負荷削減と習得工程

## Purpose

AI活用（Prompt / Context / Workflow / Agent / Loop Engineering）を業務に適用して業務負荷を下げる。適性の低い領域に過剰投資せず、適性の高い領域を中心に山型で習得する。最終的な費用対効果の評価関数を作るため、まず概念と工程を整理する。

## Principles

- 目的はAI知識の獲得ではなく、業務負荷削減と費用対効果の評価。学習そのものを目的化しない。
- 最終決定はユーザーが行う。AIは素案、評価材料、テンプレート、実装案を提示する。
- AI化の評価は、時間削減だけでなく、品質、修正・レビュー時間、構築・保守コスト、AI利用料、リスク、再利用性も見る。
- 高度なAgentやLoopを最初から入れない。小規模な業務で効果を確認してから段階的に進める。
- AIの自己評価だけで品質を保証しない。原資料との一致、必須項目、矛盾、未決事項の扱いなど、外部化された検証基準を置く（[[ai-harness-concepts]] の検証）。

## Decisions

### 進め方は案A「実務ROIファースト型」（2026-10-02）

- 根拠: 学習を目的化せず、実業務の負荷削減と効果測定から始められる。
- 検討した案: B「AI Workflow Engineer型」、C「メタAI活用型」。代替ではなく、Aの後に発展させる工程として位置づける。

### 発展は A → B → C の反復型

- A: 業務候補発見・ROI評価・小規模実証。
- B: 効果が確認できた業務をContext / Workflow / Tool / Agentとして体系化。
- C: EvaluationやLoopでAI活用自体を継続改善。
- ウォーターフォールではなく、実測結果に応じてAへ戻る。A/B/Cは標準分類ではなく、この会話での作業モデル。

### 習得の主戦場はLevel 2〜4（Context / Workflow / Agent）

- Prompt Engineeringは必要十分にし、テンプレート作成はAIに委任する。Loop Engineeringは必要性が生じた案件で深める。
- 根拠: 会話内の暫定評価では、Promptは既に一定水準、Context / Workflow / Agentが重点候補。これは実測に基づく評価ではなく仮説。

## A工程（暫定）

1. AI活用の基本思想を最小限把握
2. 業務をAI化候補に分解
3. AI適性・ROI評価
4. 優先案件を選択
5. Prompt / Context設計
6. 実業務で試行
7. 効果測定
8. 継続・改善・却下を判断し、次候補へ

## Facts

- 以前の業務改善の話題として、Power Automate + Office Script + SharePointによる勤怠Excel処理のPOC（約100件を約2時間で処理）が共有されている。候補選定に使える可能性がある（[[power-automate-office-automation]]）。

## Gotchas

- Promptのテンプレート作成や技法の学習自体が目的化しやすい。必要なテンプレートはAI側で作成し、ユーザーは業務選定・任せる範囲・実測評価に集中する。
- 高度なAgentやLoopを最初から入れると過剰設計になる。

## Open Questions

- 実際の業務棚卸し対象と優先順位。
- ROI評価関数の具体的な変数、重み、単位、最低採用基準。
- 時間削減の金額換算と、品質・認知負荷・判断速度などの非金銭価値の扱い。
- 実装環境（ChatGPT、Microsoft 365、Power Automate、Office Script、社内規程・データ制約）の適用範囲。
- A工程の期間・学習時間配分・実証案件数。

## Related

- [[ai-harness-concepts]]
- [[ai-handson-framework]]
- [[human-ai-decision-loop]]
- [[power-automate-office-automation]]
