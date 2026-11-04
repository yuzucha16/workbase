# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認（① 〜 ⑤）と置き場の実測（ケース A・B・C）を済ませた。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【起票 11-04、期日 11-11】`ROOM.md` の雛形（`room.py`）を変えた（`git -C` の緩和）ので、既存の部屋・Project の `ROOM.md` への反映方法を確かめる（`room mkworks --update` で足りるか。足りなければ手で直す範囲を決める）。あわせて `workflow-kit/room/README.md` に `git -C` を必須とする記述が残っていないか見る（11-04 の grep では「必須」の文は見つからなかったが、長い行の全文は未確認）。

## Open Questions

- `inv` の基準文書は仮決め。
