---
type: knowledge
title: Power Automate / Office Scriptsによる業務自動化
status: active
tags:
  - tool/power-automate
  - tool/excel
  - automation
  - office
  - ai/chatgpt
  - ai/claude
aliases:
  - Power Automate学習計画
  - 週次・月次作業レポート自動化
  - 入力層設計
created: 2026-10-02
updated: 2026-10-02
sources:
  - Claude conversation "Power Automate/Office Scriptsによる週次・月次作業レポート自動化(入力層設計)" (2026-10-02)
  - ChatGPT conversation "Power Automate学習計画" (2026-10-02)
---

# Power Automate / Office Scriptsによる業務自動化

## Purpose

会社のMicrosoftアカウントでPower AutomateとOffice Scriptsを使い、月次データ集計などの定常業務を自動化する。その一環として、部下・パートナーの作業可視化を目的とした週次・月次作業レポートの集約・配信をPoCとして作る。この文書では特に「入力層」（データの受け口とマスタの持ち方）の設計と、学習の進め方をまとめる。

## Principles

- Office ScriptsはExcelブックしか直接読み書きできない。Excel中心の構成なら、データもExcelに寄せる。
- データはlong/tidy形式（1行1レコード）で持つ。列が人や週で増減する構造は、ピボットやPower BIと相性が悪い。
- 生データ（Raw）と集計（Aggregate）を物理的に分ける。生データはAppend-onlyにして汚さない。
- 自由入力をやめ、マスタ参照のドロップダウンにして表記揺れを防ぐ。
- 小さく作る・壊す・調べて直す実践型で学ぶ。
- 実務フロー化する段階で、エラー処理、再実行、重複登録防止（冪等性）、ログを設計する。

## Decisions

### Formsの送信先はSharePoint上のExcelテーブルに直接送る（2026-10-02）

- 根拠: SharePointリストを経由するとPower Automateでの転記処理が増える。リスト化の利点はUIくらいで、Excel連携の相性を優先した。
- 却下案: Forms → SharePointリスト → Power Automateで転記 → Excel集計。過去にFormsからリストへの登録フローを作った経験はあるが、Office Scripts中心の構成には回り道。

### データはlong/tidy形式で持つ

- 根拠: 人×週のマトリクス（wide）は、列が増減して後工程で破綻しやすい。
- スキーマ例: Date, WeekOf, EmployeeID, Name, ProjectCode, TaskName, Hours, Status, Comment

### Raw / Aggregate を分離する

- 根拠: 集計ロジックを変えても生データに影響しない。異常値の「入力ミスか集計バグか」を切り分けやすい。

### マスタ（社員・案件）を別テーブルにし、Formsはドロップダウン化する

- 根拠: 氏名・プロジェクト名の自由入力は表記揺れを生む。
- 却下案: 自由入力のまま文字列正規化で吸収する。規模が増えると事故率が上がる。

### 名寄せはPoC段階ではFormsの選択肢を手動メンテする（案①）

- 根拠: Power AutomateでFormsの選択肢をマスタと自動同期する案（案②）はForms REST APIが必要で複雑。Excel入力 + データ入力規則に全面移行する案（案③）は現時点ではオーバースペック。PoC規模（数人〜十数人、変更頻度低）に労力が見合わない。
- 将来: チーム規模が拡大し変動が頻繁になったら案③へ移行を検討する。

## Facts

- Office ScriptsはSharePointリストを直接操作できず、SharePoint/OneDrive上のExcelブックにのみアクセスできる（確認済み）。
- FormsのドロップダウンはForms設定画面で手入力する静的な選択肢で、Excelのマスタテーブルと自動連携しない（確認済み）。
- 着手済み: Office ScriptsとPower Automateを組み合わせた月次データ集計の自動化。Forms → SharePointリストへのtodo自動登録フローの構築経験もある（ユーザー発言）。
- Power Automateのスケジュール実行からCopilot Studio経由でエージェントを呼ぶ構成は [[ai-handson-framework]] で検討している。

## 学習計画（提案。採用は未確認）

- 方針: 基礎から始め、SharePoint・データ加工・式・エラー処理へ進む。順序は クラウドフロー基本 → データ操作 → 式 → エラー処理・再実行設計 → Microsoft 365連携。
- 学習項目: トリガー、アクション、動的コンテンツ、条件分岐、Apply to each、変数、SharePoint、Excel、CSV、JSON、Select、Filter array、Compose、式（`if` / `equals` / `empty` / `coalesce` / `formatDateTime` など）、Scope、ログ。
- 練習題材の案: Forms回答からTeams通知 / SharePoint登録を起点に承認依頼 / 定時実行で前日データを集計してTeams通知 / CSVを読み込みSharePoint Listを更新 / 月次データからPL・稼働率などを集計してレポート化。
- 4週間（基本、SharePoint、CSV/JSON、管理向け集計）の学習案は提案であり、確定ではない。
- 注意: ユーザーは既にPower Automate / Office Scriptsの実務経験があるため、この学習計画の位置づけ（入門か補強か）は要確認。

## Gotchas

### FormsとマスタのIDを一致させる標準の仕組みがない

- 回避策（未実装・方針のみ）: 選択肢表示に「氏名 (ID)」のようにIDを埋め込み、Office Scripts側で正規表現抽出する。または、Name文字列のままマスタとVLOOKUP相当で突合する。

### 環境・ライセンスで使える機能が変わる

- Microsoft 365 Business Standardの利用有無や、利用可能なPower Automateライセンス・コネクタは未確認。テナントのDLPで使えない場合もある。

### Excelをデータベース代わりにする制約

- 同時編集やテーブル構造の制約がある。詳細は未検討。

## Open Questions

- Formsの項目設計（工数入力の粒度: タスク / プロジェクト、日次 / 週次）。
- Excelテーブルの列定義とシート構成（Raw / Aggregate / Master を同一ブックにするか分けるか）。
- マスタに存在しない値（未解決データ）の検出・通知の運用。
- 学習用の題材を作るか、実際の業務課題を題材にするか。デスクトップフロー（Power Automate for desktop）も対象にするか。目標期間と週あたりの学習時間。

## Next Actions

- Power Automateの利用環境・ライセンス・コネクタを確認する。
- Formsの入力項目（粒度）を設計する。
- SharePoint上のExcelブックのシート構成（Raw / Aggregate / Master）と列定義を決める。
- マスタテーブルの初期データを作り、Formsのドロップダウンに反映する。
- Office Scriptsで「生データ → マスタ突合 → 集計テーブル生成」を実装する（未解決値の出力を含む）。

## Related

- [[ai-handson-framework]]
- [[ai-business-adoption]]
- [[office-ai-workspace]]
- [[ai-business-adoption/context]]
