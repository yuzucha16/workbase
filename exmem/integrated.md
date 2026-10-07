# 統合台帳

`inbox/` のメモを `knowledge/` に統合したときに、`integrate`（`workflow-kit/integrate-hook.md`）が、メモと統合先の照合をユーザーが承認した後で、1行足す台帳。作業ディレクトリ側の `review`（`workflow-kit/review-hook.md`）が、`転記待ち` を `転記済` に進める根拠として読む。

- 共有側のファイル。作業ディレクトリの固有の情報（項目名、パス）は書かない。書くのはメモ名と統合先だけ。
- 追記のみ。行を消さない・直さない。**同じメモ名の行が複数あるときは、日付が最も新しい行を有効とする（同じ日付なら、ファイルの下の方の行）。** 誤記は、種別 `訂正` の行を足して直す。統合を取り消すときは、種別 `取消` の行を足す。
- 種別: `統合`（通常）、`取消`、`訂正`。照合: `承認済（YYYY-MM-DD）`（メモと統合先の照合を、ユーザーが承認した日）。統合先は複数書いてよい（`、`区切り）。
- 並行する追記の競合は、`.gitattributes` の `merge=union` で防ぐ。マージで行の順序が入れ替わりうるので、有効な行は、順序でなく日付で決める。
- 2026-10-08 より前に統合したメモは、記録が無い（そのメモを指す `転記待ち` は、従来の方式で確定する）。

| 日付 | 種別 | メモ名 | 統合先 | 照合 |
|---|---|---|---|---|
| 2026-10-08 | 統合 | 2026-10-07-deciding-what-to-decide | knowledge/human-ai-decision-loop.md、knowledge/para-operations.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-07-claude-code-resume-sdk-sessions | knowledge/claude-code-storage.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-07-zed-thread-db-folder-paths | knowledge/zed-acp.md、knowledge/claude-code-storage.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-07-office-deliverable-ai-workflow | knowledge/office-ai-workspace.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-07-gitattributes-leftover-crlf-index | knowledge/git-line-endings.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-08-workflow-hook-naming-lifecycle | knowledge/workflow-kit.md、knowledge/para-operations.md | 承認済（2026-10-08） |
| 2026-10-08 | 統合 | 2026-10-08-hook-authority-delegation-ledger | knowledge/workflow-kit.md、knowledge/windows-cli-pitfalls.md | 承認済（2026-10-08） |
