# 作業ログ（log）

`init` `open` フックを廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24。`a015bda` `c771c01` `45ee732`）。`brief 変更` の入口を足し、`brief-hook.md` と `review-hook.md` の字数超過を解消した（2026-10-24）。残りフック（`wrap` `stock` `integrate` `review`）と `room` の整合も見て反映した（2026-10-24。`hooks.md` の room 表を絞り、`wrap` のコミットは AI が行う）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- `stock` の `scope: area` の実機確認: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更（ユーザーの予告）があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。
- 【起票 10-25】PC2 の Windows で `verify.bat` と `verify.ps1` を 1 回ずつ叩く（uv の取得、文字コード、y/n と日本語のひとこと）。最初の失敗が、原因の台帳（`script-guide.md`）の初めての使用になる。`run.py` の型と ps1 版は Linux でのみ確認（2026-10-25）。

## Open Questions

- `mkworks` は `Template-Rev` を新規に付けず `Room-Rev` に統一した。旧版の `room.py` で `--update` した works との行き来は考えていない。
