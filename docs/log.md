# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに Next Actions と Open Questions を更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## 期日（今日以前、または3日以内の項目は、最初の返答で知らせて判断を求める。定例は実行したら次回の期日に書き換える。書式は `workflow-kit/docs-rules.md`）

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| なし | | | |

## Next Actions

- Stop フックで、セッションの費用と ID を記録する手順（`notes/stop-hook-record/2026-10-17-procedure.md`、プロジェクトの共有フォルダ）を、Zed を使う PC で実機確認する（端末の `claude -p` と、Zed の1往復。2026-10-17 時点）。
- 別セッションの「Stop による標準出力量の抑制」の検討と、この手順を1つの Stop フックにまとめるか決める（ユーザーの希望。2026-10-17 時点）。

## Open Questions

- 費用と応答本文の記録を、同じ1つのスクリプトにまとめてよいか（AI の提案。スクリプトは `notes/stop-hook-record/stop-record.py`）。記録の置き場は `~/claude-records/`（部屋の中は `$CLAUDE_PROJECT_DIR/records` の案もある）。
