# 作業ログ（log）

`init` `open` フックを廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24。`a015bda` `c771c01` `45ee732`）。残りフック（`wrap` `stock` `integrate` `review`）と `room` の整合は未着手。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 旧名の読み替えと注記を消す（ユーザーの決定 2026-10-24。「現在の仕様が回りだしたら、読み替えもなくして消す」）。対象: `hooks.md` の旧名・旧ファイル名の項、各ノートの「旧 `init`」「旧 `start`」の注記、記録中の旧名。条件: `mkworks` の実機確認と、`brief` の運用で問題が出ないこと。
- `room mkworks` の実機確認（Windows）: 新しい PC の `mkworks`、既存の works の `mkworks --update`（基点が旧 `Template-Rev` のとき）。単体テストのみ。
- dotfiles の Claude 用スキルに、旧 `start` や「workflowを導入して」の入口があれば直す。
- 残りのフックと `room` の整合を見る（`wrap` と回収、`stock` と `room stock`、`review` `integrate` は対象外か）。ユーザーが「継続したい」と言った範囲で、気づいたときに。

## Open Questions

- `brief 変更`（`methods.md` の「変更」の入口）を足すか。引数が `methods.md` の区分（解決・改善・変更・調査・計画）と1対1でない。足すなら設計が要る。
- `brief-hook.md` が 5,042 字で目安（5,000）を超える（`check_hook_outline` の NOTE）。基準 4,490 の +12%。
- `mkworks` は `Template-Rev` を新規に付けず `Room-Rev` に統一した。旧版の `room.py` で `--update` した works との行き来は考えていない。
