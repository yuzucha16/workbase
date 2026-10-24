# 判断の記録（decisions）

## Decisions

### 【この件】フックと room の整合の決定（2026-10-24）

- 正本は workbase 直下の `docs/decisions.md` の同日の3項（`init` `open` の廃止と `room mkworks`、`start` の `brief` への改名）。ここには重ねて書かない。
- 論点と案、変更範囲は [[hook-room-alignment-notes]]。

### 【この件】過去の記録の旧名は、現在の仕様が回りだしたら読み替えごと消す（2026-10-24）

- 決めたこと（ユーザー、2026-10-24）: 旧名（`init` `open` `start` のフック、`start-hook.md` など）の履歴は、新しい仕様が運用で回りだしたら、読み替えの注記もなくして消す。今は `hooks.md` の旧名の項が読み替えを持つ。
- 見直しの条件: `mkworks` の実機確認が済み、`brief` で問題が出ていないこと。
