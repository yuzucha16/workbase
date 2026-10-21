# 作業ログ（log）

会議録のナレッジ化（`private-knowledge`）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## 状態

Area を跨ぐ共有知の仕組みは、2026-10-21 に実装し、実機の通し試験で問題なし（ダミーの Area。決定 ⑧〜㉕）。流れ: Area の `knowledge/`（実名）→ `room pull` → `mask` → 部屋の AI が統合 → `restore` が実名に戻して Area へ。人の変更は `restore` が止める（`--force` で上書き）。型は `records/meeting-note-example.md`、手順は `guides/howto/ai-room-setup-script.md` の 4.1・6.1、理解は `guides/explain/cross-area-shared-knowledge.md`。

## Next Actions

1. 実例1件で通す（works の実際の会議録。マスクして `pull`、統合、`restore`）。指標を測る: 冒頭の数行に収まった決定・ToDo の数、人が直した箇所の数、冒頭の行数の上限（仮 10 行）。works 側の `areas/<Area>/knowledge/` を人が作る（このリポジトリの外）。
2. 統合の手順書の整備: 部屋の AI に統合させる指示（`ai/out/knowledge/` に `kind: integrated` で書く）を、`room-context.md` か手順書に固める。いまは `ai-room-setup-script.md` の 6.1 の例だけ。
3. 進行中の `stock` のモード追加（`topics/stock-modes/`）との重なりを整理する（裏づけ #5）。型の用語（冒頭の数行 = 人向け）が、理解ガイドの6見出しと食い違わないか。
4. 型・理解ガイドの型の整理と改善は、別セッションで行う（ユーザーの指示、2026-10-21）。

## Open Questions

- 【案件】の行き先（`ai/docs/inbox.md` か Area の `docs/decisions.md` か）。root の Open Questions にある。
- Area 側の保管場所と同期（Git か、PC ごとのローカルか）。
- 選び方（絞って人が確認）は仮案。使って負担が出たら見直す。
