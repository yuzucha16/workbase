---
type: knowledge
title: Excel VBA マクロを AI で作るときの規約と落とし穴
status: active
tags:
  - tool/excel
  - office
  - automation
  - testing
  - windows
  - tool/powershell
aliases:
  - VBAマクロのAI開発
  - Excel VBA の落とし穴
created: 2026-10-14
updated: 2026-10-14
sources:
  - Claude Code conversation "他環境の AI 開発環境プレイブックの取り込み" (2026-10-14)
---

# Excel VBA マクロを AI で作るときの規約と落とし穴

## Purpose

他環境で、Excel VBA マクロを AI に作らせて保守させたときに実際にハマった点と、そこから決めた規約を、題材としての知識として残す。成果物の構成・文書・テストの共通部は [[ai-tool-deliverable-structure]] に分け、この環境の部屋の設計（[[ai-isolated-work-room]]）とは合流させない。以下の事実は他環境の文書を読んだもので、この環境では再現していない。

## Principles

- VBA のソースは UTF-8 / LF を正本にし、実行環境が読める形式（Shift-JIS / CRLF の `.bas`）は変換スクリプトで作る。検査に失敗したら何も書き出さない。理由: VBE は cp932・CRLF の `.bas` しか正しく読めず、壊れた派生物を残さないため。
- 実行中に変える Excel の設定（再計算、画面更新、イベント）は先に保存し、正常・中止・エラーのすべてで戻す。理由: 途中で止まると、利用者の Excel が設定を変えたままになる。
- 出力先のブックを開いたときは、マクロが開いたものだけを閉じ、中止・エラー時は保存せずに閉じる。利用者が先に開いていたものは閉じない。理由: 利用者の作業中のデータを失わないため。
- 外部ライブラリは使わない（Windows 標準の `Scripting.Dictionary`、`ADODB.Stream`、`FileSystemObject` は可）。Mac 版・Web 版の Excel は対象外と明記する。理由: 配布先の環境に依存せず動かすため。
- 操作画面は UserForm でなく、セルとボタンの「操作シート」にする。理由: UserForm の部品定義はバイナリ（`.frx`）で、テキストの `.bas` では渡せない。

## Decisions

- **VBA 固有の知識は、成果物の構成・文書・テストの共通の型と分け、別ノートにする**（2026-10-14）
  - 根拠: ユーザーの方針は「共通部の考えが特に重要。VBA は題材としての知識として残したい」。VBA 固有の部分は、部屋の設計（`ai/` と `_noai/`）との合流が要らない。
  - 却下案: 共通のノートに混ぜる（言語依存の規約が、他言語への一般化を邪魔する）。

## Facts

すべて他環境の文書をユーザーが画像で提示したもの（確認: 2026-10-14）。この環境では未再現。

- ブックは `.xlsm` で保存し、ログと出力ファイルの文字コードは UTF-8（BOM あり）を既定にした（`ADODB.Stream`）。cp932 で表せない文字は使わず、変換スクリプトで検査した。
- 処理の工程名を変数（`mStep`）に入れ、エラー表示に「処理中: 」に続けて工程名を付けた。危険な操作の前に更新する習慣にした。実行中に変える Excel の設定は、`SaveState` で保存し `RestoreState` で戻した。
- 範囲の取り方は、`UsedRange` を使わず、最終行を `Cells(Rows.Count, 列).End(xlUp).Row`、範囲を `Cells(行, 列)` の絶対位置にした。`Option Explicit` を保ち、ブロック（Sub / If / For / Do / Select / With）の対応を検査した。
- ピボットは、`PivotField.Position` や `DataRange` に頼らず、見出しの文字から列を探した。元データは列全体でなく名前付き範囲にし、条件付き書式は先頭セルを選択してから `Add` した。旧「共有ブック」がオンのブックは、ピボットの作成と書き込みが制限される。
- 結果のダイアログは、`MsgBox` の上限（約1000文字）があるので、収まらないときは件数と「ログを参照」で示した。「要チェックだけを短く出す」ダイアログと「全員分のログ」の二層にした（Office 16.0 時点の他環境の報告）。
- Excel COM のテストは PowerShell 7 で書いた（`#Requires -Version 7`、`$ErrorActionPreference = 'Stop'`）。`finally` で `Close($false)`、`Quit()`、`ReleaseComObject` の順に後始末した。起動した Excel のプロセス ID を記録して終了時に確実に止め、利用者の Excel とは別のプロセスで起動した。
- テストでは、「VBA プロジェクト オブジェクト モデルへのアクセスを信頼する」（`HKCU\Software\Microsoft\Office\16.0\Excel\Security\AccessVBOM`）を実行中だけ 1 にし、終了時（失敗時も `finally`）に元へ戻した。作業フォルダは `%TEMP%` の下に作り、終了時に削除した（オプションで残せる）。
- Excel を開く前に、必ず TEMP にバックアップを取った。`DisplayAlerts = $false`、`EnableEvents = $false`、`AutomationSecurity = 3`（マクロを動かさない）で開いた。
- AI が実行できない VBA（利用者の実機でしか動かない処理）は、出力の前に型、`ByVal` / `ByRef`、配列の添字、エラー処理の範囲を読み直した。差し替えの手順は、モジュールの解放 → インポート → 初期化 → コンパイルを毎回明記し、エラーはメッセージ全文と処理中の工程名を貼ってもらった。

## Gotchas

- 状況: モジュールを差し替えたら、`modX1` のように二重に入った
  - 原因: 古いモジュールを解放せずにインポートした
  - 解決: 古いものを右クリックして「解放」し（エクスポートは「いいえ」）、そのあとでインポートする
- 状況: モジュールレベルの宣言（`Private mX As`、`Private Const`）を、最初の `Sub` / `Function` の後ろに書いて、コンパイルエラーになった
  - 原因: VBA は、モジュールレベルの宣言を最初のプロシージャより前に要求する
  - 解決: 先頭に書く。変換スクリプトの検査で検出する
- 状況: 変数名に `dir`、`name`、`date`、`format`、`left` を使ったら、「配列がありません」などのエラーになった
  - 原因: 組み込み関数の名前と衝突した（`Dir` が配列として扱われた）
  - 解決: 組み込み関数名を変数名に使わない。変換スクリプトで検査する
- 状況: `On Error Resume Next` の下の `If <式> Then` で、式の評価がエラーになったのに `Then` の中に入った
  - 原因: エラーを無視して続行する設定のため、評価エラーのまま分岐に入る
  - 解決: リスクのある判定は、エラー処理の外で行う
- 状況: `Round` の結果が JavaScript の `Math.round` と合わず、`Trim` で全角空白が残った
  - 原因: VBA の `Round` は銀行丸め。`Trim` は全角空白を除かない
  - 解決: `Int(x + 0.5)` を使う。全角空白は自前の `JTrim` で除く。文字列の比較は `StrComp(…, vbBinaryCompare)` にする
- 状況: `Range.Value2` に文字列を入れたら、「2026年04月」が日付に変わった
  - 原因: 書き込み時の自動変換
  - 解決: 書き込む前に、表示形式を `@`（文字列）にする
- 状況: `ThisWorkbook.Path` が URL（クラウド上のブック）になり、ログの出力先に使えなかった
  - 原因: クラウドで同期されたブックは、パスが URL になることがある
  - 解決: ログの出力先は `%TEMP%` にフォールバックする。URL のブックを `Workbooks.Open` するときは、警告を有効にして複数の開き方を順に試す

## Open Questions

- テストで `MsgBox` を差し替える方法（ダイアログで止まらず、文言も検証できる）の詳細。元の文書の該当部分が、まだ手元にない。
- 元の文書で判読できなかった箇所（cp932 で表せない文字の具体例、工程名の表示の書式）。
- 他環境の値（Office 16.0 のレジストリのパス、`MsgBox` の上限、Mac・Web 版が対象外）が、この環境の Excel でも同じか。

## Next Actions

- ユーザーが後日用意する元の文書の詳細で、判読できなかった箇所と `MsgBox` の差し替えを確認し、このノートを直す（2026-10-14 時点）。

## Related

- [[ai-tool-deliverable-structure]]
- [[office-ai-workspace]]
- [[power-automate-office-automation]]
