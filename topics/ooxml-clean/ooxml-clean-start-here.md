# 窓口: ooxml-clean

- 型: Project 型。完了条件: xlsx・pptx を AI に渡す前の点検・掃除（`workflow-kit/room/cleankit.py`）が、実ファイルを Excel・PowerPoint で警告なしに開ける形で通り、room の `mask` への組み込みの要否をユーザーが決める。
- 何の取り組みか: 消したつもりのシートが xlsx の XML に残り、AI に見えた（2026-10-26）。残り方の整理（`records/2026-10-26-mechanism-and-plan.md`、理解ガイド `guides/explain/ooxml-residue.md`）と、AI に渡す前のクリーン化スクリプトの実装。

## いま

PC1 の実ファイルで掃除の残りが 0 件になった（2026-10-27）。Excel で開くと「パーツがない」警告が出ていた件の原因が未特定。

## あなた待ち

- 最新版の出力を Excel で開き、警告の文面（`/xl/…` のパーツ名）を知らせる。

## 次の一手

「ooxml-clean の続き」で、`docs/log.md` の Next Actions を見る。PC（Excel で開く確認）。

## 読む順

1. `docs/log.md`（現在状態。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: `docs/log-history.md`（経緯）、`records/`（出力）

## リポジトリに無いローカルの状態

PC1 の実ファイルとその報告は `projects/` の `_noai/` にある（実データを含む。AI に見せない）。
