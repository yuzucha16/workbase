# 窓口: ooxml-clean

- 型: Project 型。完了条件: xlsx・pptx を AI に渡す前の点検・掃除（`workflow-kit/room/cleankit.py`）が、実ファイルを Excel・PowerPoint で警告なしに開ける形で通り、room の `mask` への組み込みの要否をユーザーが決める。
- 何の取り組みか: 消したつもりのシートが xlsx の XML に残り、AI に見えた（2026-10-26）。残り方の整理（`records/2026-10-26-mechanism-and-plan.md`、理解ガイド `guides/explain/ooxml-residue.md`）と、AI に渡す前のクリーン化スクリプトの実装。

## いま

PC1 の実ファイルで掃除の残りが 0 件になった（2026-10-27）。xlsx は Excel で警告なしに確認済み（2026-10-28）。room の `mask` への組み込みは決定済み（2026-10-30）。pptx は PC1 で確認済み（2026-11-02、問題なし）。読ませる用途は掃除でなく取り出し（`workflow-kit/room/pptxtext.py` v0、5b84cf7）に割り切った。

## あなた待ち

- PC1 の実 pptx で `pptxtext.py` を回し、出力の足りないところを知らせる（動作確認と要件の拡充は別セッション、`docs/log.md` の NA 0）。

## 次の一手

「ooxml-clean の続き」で、pptxtext の確認と要件の拡充（NA 0）、room の `mask` への組み込みの実装（`docs/log.md` の NA 1）。

## 読む順

1. `docs/log.md`（現在状態。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（出力）

## リポジトリに無いローカルの状態

PC1 の実ファイルとその報告は `projects/` の `_noai/` にある（実データを含む。AI に見せない）。
