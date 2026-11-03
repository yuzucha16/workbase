# 窓口: ooxml-clean

- 型: Project 型。完了条件: xlsx・pptx を AI に渡す前の点検・掃除（`workflow-kit/room/cleankit.py`）が、実ファイルを Excel・PowerPoint で警告なしに開ける形で通り、room の `mask` への組み込みの要否をユーザーが決める。
- 何の取り組みか: 消したつもりのシートが xlsx の XML に残り、AI に見えた（2026-10-26）。残り方の整理（`records/2026-10-26-mechanism-and-plan.md`、理解ガイド `guides/explain/ooxml-residue.md`）と、AI に渡す前のクリーン化スクリプトの実装。

## いま

PC1 の実ファイルで掃除の残りが 0 件になった（2026-10-27）。xlsx は Excel で警告なしに確認済み（2026-10-28）。語のマスクは必須でなくなり、入口は `room clean`（strict、2026-11-03）。`pull` は廃止し、原本は共通性で分けた(2026-11-03)。pptx は PC1 で確認済み（2026-11-02、問題なし）。読ませる用途は掃除でなく取り出し（`workflow-kit/room/pptxtext.py` v0、5b84cf7）に割り切り、実 pptx で動作確認済み（2026-11-02、問題なし）。

## あなた待ち

- なし(境界の見直し・internal の確認は 2026-11-03 に済)。

## 次の一手

「ooxml-clean の続き」で、NA 1(Project の `docs/` を Area の共有知へ統合する経路の設計)。古い文書の書き直し(NA 2)と `clean --path` の実機確認(NA 3)も期日 11-10。`mask` / `restore` の削除は `docs/due.md`(11-30)。

## 読む順

1. `docs/log.md`（現在状態。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（出力）

## リポジトリに無いローカルの状態

PC1 の実ファイルとその報告は `projects/` の `_noai/` にある（実データを含む。AI に見せない）。
