# 作業ログ（log）

`init` `open` フックを廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24。`a015bda` `c771c01` `45ee732`）。`brief 変更` の入口を足し、`brief-hook.md` と `review-hook.md` の字数超過を解消した（2026-10-24）。残りフック（`wrap` `stock` `integrate` `review`）と `room` の整合も見て反映した（2026-10-24。`hooks.md` の room 表を絞り、`wrap` のコミットは AI が行う）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- `stock` の `scope: area` の実機確認: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更（ユーザーの予告）があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。

- 旧名の読み替えと注記を消す（ユーザーの決定 2026-10-24。「現在の仕様が回りだしたら、読み替えもなくして消す」）。対象: `hooks.md` の旧名・旧ファイル名の項、各ノートの「旧 `init`」「旧 `start`」の注記、記録中の旧名。条件: `mkworks` の実機確認と、`brief` の運用で問題が出ないこと。
- `room mkworks` の実機確認（Windows）: 新しい PC の `mkworks`、既存の works の `mkworks --update`（基点が旧 `Template-Rev` のとき）。単体テストのみ。
- dotfiles の Claude 用スキルに、旧 `start` や「workflowを導入して」の入口があれば直す。

## Open Questions

- `mkworks` は `Template-Rev` を新規に付けず `Room-Rev` に統一した。旧版の `room.py` で `--update` した works との行き来は考えていない。
