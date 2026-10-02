---
type: project
title: AI活用の業務適用 Project Context
status: active
tags:
  - agent-design
  - automation
  - office
  - harness
aliases:
  - AI活用の業務適用 Project Context
created: 2026-10-02
updated: 2026-10-02
---

# AI活用の業務適用 Project Context

## Current State

- 進め方は「実務ROIファースト型（A → B → C の反復）」と決めた（[[ai-business-adoption]]）。業務の棚卸しとROI評価シートは未着手。
- ハーネスの座学は一通り整理した（[[ai-harness-concepts]]）。実装は別スレッドのハンズオンで行う。
- 最初のハンズオン題材は、メール・Teams・業務連絡の情報ダイジェスト（[[ai-handson-framework]]）。設計は決まっているが、**未実装**。`ai-handson/` はvaultにまだ無い（2026-10-02 確認）。
- 週次・月次作業レポートの入力層は、Forms → SharePoint上のExcelテーブル、long形式、Raw / Aggregate分離、マスタはドロップダウンと決めた。列定義と項目の粒度は未決（[[power-automate-office-automation]]）。
- Office成果物（xlsx / pptx）の作業環境は、Master / view分離と案件フォルダ構成を設計した（[[office-ai-workspace]]）。Claude CodeはWindowsネイティブで始め、Coworkは後回し（[[claude-code-vs-cowork]]）。`excel-aggregation` スキルは未配置（2026-10-02 確認）。
- 意思決定ループ（Decision Loop）は、キーボード購入を題材に最小版を試作する予定（[[human-ai-decision-loop]]）。

## Next Actions

優先度の目安（上から着手）:

1. 環境の確認: Microsoft 365のCopilotライセンス、Power Automateのライセンス・コネクタ、テナントのDLP。ここで決まることが多い。
2. `ai-handson.zip` を展開してAreas直下に置き、`ai-handson/` でClaude Codeを起動して、CLAUDE.mdが読まれるか確認する（[[ai-handson-framework]]）。
3. 情報ダイジェスト: Agent Builderのエージェントの指示欄を5項目（目的と読み手、対象範囲、判断基準、出力形式、禁止事項）で書き直し、権限（読むだけ、書き込み先1か所）を明記する。Power Automateのスケジュール実行 → Copilot Studio経由で呼び、OneDriveに日付付きMarkdownを保存する。前日ファイルを参照させて「新規」と「継続」を分ける。最初の1〜2週間は未対応メールと出力を突き合わせ、結果を `tasks/comms-digest.md` の失敗ログに記録する。
4. 業務棚卸しフォーマット（最初は10〜20件）とROI評価シート v0.1 を作る（[[ai-business-adoption]]）。
5. 既存の集計ブック1つを `src/` に原本として置き、Master / view分離を試す。`excel-aggregation` スキルを配置して小さな依頼で試す（[[claude-code-vs-cowork]]）。
6. 失敗パターンが見えてから制御フックを足す。タスクが2〜3個溜まったら、抽象化タスクでテンプレートを見直す。
7. 週次・月次レポート: Formsの入力項目、Excelのシート構成、マスタの初期データ、Office Scriptsの集計ロジックを順に作る。
8. 並行して、Decision Loopの最小版をキーボード購入で試す。

## Goal

AI活用で業務負荷を下げる。適性の高い領域（Context / Workflow / Agent）を中心に山型で習得し、費用対効果を評価できるようにする。

## Open Questions

- 業務棚卸しの対象と優先順位。ROI評価関数の変数・重み・最低採用基準。
- どのタスクを「AIが実装 / 人間が実装 / AIが下書き、人間が実行」に振り分けるか（[[ai-handson-framework]] の判別基準）。
- ClaudeのCode / Cowork / チャットの使い分け。このPCはWindows Homeで、Coworkの要件を満たさない（業務PCは別かもしれない）。
- 会社の端末・テナントでできることの範囲（Copilotライセンス、DLP、Excel COM）。

## Related

- [[ai-business-adoption]]
- [[ai-harness-concepts]]
- [[ai-handson-framework]]
- [[power-automate-office-automation]]
- [[office-ai-workspace]]
- [[claude-code-vs-cowork]]
- [[human-ai-decision-loop]]
