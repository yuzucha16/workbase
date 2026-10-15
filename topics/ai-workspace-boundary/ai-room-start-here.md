# 窓口: AI 作業部屋（ai-workspace-boundary）

- 型: Project 型。完了条件 = 優先順位 1〜7 が PC で確認済み。
- 何か: 顧客データを AI に見せないため、Project の作業を専用 WSL（部屋）の中で行い、`ai/` だけを渡す。マスク・復元は人が実行する `room` が行う。理由と経緯は `guides/explain/ai-room-why.md`、導入は `guides/howto/ai-room-setup.md`。

## いま

実装は 1〜7 が済み、PC での実機の確認が残っている。詳細は `docs/log.md`。

## あなた待ち

なし（`docs/log.md` の「あなた待ち」は実施の確認だけ）。

## 次の一手（PC）

`docs/log.md` の「次の一手」。1項目ずつ、未決はユーザーに1つずつ聞く。

## 読む順

1. `docs/log.md`（状態の正本）
2. `docs/decisions.md`（決定）
3. 必要なとき: `notes/`（`ai-room-*-handover.md` に各項目の「PC で確認すること」、`ai-room-local-state.md` にローカルの状態と作業の約束、`ai-room-design.md` に詳細）、`docs/log-history.md`（実測の経緯）

## 約束（要点）

`workflow-kit/` の変更はユーザーの承認を得てから。コミットは main に直接。公開されうる前提で、勤務先名・顧客名・実在の Project 名を書かない。`room` は人が実行し、AI には実行させない。
