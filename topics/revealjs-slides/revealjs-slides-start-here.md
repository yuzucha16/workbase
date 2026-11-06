# 窓口: revealjs-slides

- 型: Project 型。完了条件: inv 型の成果物（`ai/out/`）に、図解レイアウトの revealjs HTML スライドを、見本から複製して作れる土台ができる（雛形、型の選び方、PC1 の room で 1 回通る）。
- 何の取り組みか: 社内の勉強会・LT 向けの簡易スライド（Quarto → revealjs の自己完結 HTML）の「図解レイアウト」を出力の型にして育てる。正式な pptx（`topics/office-output-types`）とは別。確定ではなく拡張の土台。型・原則・落とし穴は `exmem/lessons/revealjs-diagram-layout-output.md`（2026-11-06 に統合）。

## いま

PC1 のノートと見本を書き起こし、Windows の Quarto 1.11.9 で全スライドの描画を確認し、ノートを lessons に統合した（11-06）。11-06 に生成スクリプトとアイコン分離を入れ、pptx の例から型 H・I・J（行・列が自由な格子と表）を足した。11-06 に型 K（ディレクトリ構造）と Lucide 99 種を足した。次は room での確認、K の 1/3〜1/4 幅、出典の自動表記、実スライド。

## あなた待ち

なし

## 次の一手

room（Quarto 入り）で見本を render し、H・I・J が Windows と同じ見え方か確かめる。そのあと実スライドを 1 本作る。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（見本・CSS）

## リポジトリに無いローカルの状態

なし。見本の render 結果（html、png）は一時ディレクトリで作り、コミットしない。
