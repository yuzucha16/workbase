# 期日（due）: room-type-consolidation

このトピックの日付で浮上する項目。開始時には読まない。`review 消化` が `python -I workflow-kit/tools/due.py` で期日が今日以前の行を出し、このトピックの `docs/log.md` の Next Actions に上げる。書式は `workflow-kit/docs-format.md`。

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-13 | 単発 | `room start` の後にマウントが残る件の様子見(1 週間。起票 11-06、ユーザー)。期日までに再発したら、`room-log.md` に記録されたつかむプロセスで原因を決める(Zed が原因なら `room/README.md` か `ai-room-lifecycle.md` に「止まったら Zed を再起動」と書く。`umount` の案内文に足すかも決める)。再発しなければ、`unmount()` の再試行(1 秒おき 10 回)と記録の追加で close。残っている `sample_inv` `sample_inveg1` のマウントは `room umount --area myenv` で外す | ユーザー |
