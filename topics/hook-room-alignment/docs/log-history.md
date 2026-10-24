# 作業ログの経緯（log-history）

## Log

### 2026-10-24
- ユーザーの依頼で、`room` の導入によって名前や工程が重なった `init` `open` `start` のフックを見直した。事実の表（フック ↔ `room` コマンド）を作り、論点と案を出した（[[hook-room-alignment-notes]]）。
- ユーザーが、`init` は人がやる操作なので `room` に取り込む（`room mkworks`、`--update`。将来 `--list` など引数で足す）、他リポジトリへの導入と履歴復元は廃止（`kit` は作らない）、`open` と `close` は畳む、`start` は改名してよい、と決めた。`start` の名前は `brief` で承認。
- 実装して push した: `a015bda`（`mkworks` とテスト 12 件）、`c771c01`（`init` `open` の廃止と文書の直し）、`45ee732`（`start` → `brief`）。単体テスト 137 件と `check_hook_outline` は通った。`mkworks` の実機は未確認。
- ユーザーが、過去の記録の旧名は、現在の仕様が回りだしたら読み替えごと消すと決めた。フックと `room` の調整は継続する。
- 残りのフックと `room` の整合を調べた。名前の重なりは `stock` と `room stock` だけで、同じ1件のメモの前半（AI の下書き）と後半（人の運搬）なので意図どおり。`integrate` `review` は部屋で行わず、重なりなし。抜けは `hooks.md` の room 表だけ。
- ユーザーが、表はフックと対のものだけに絞る（案A）、`stock` の行に `room stock` を足す、`wrap` のコミットは AI が行う（部屋では指示なしで部屋の git に。push はしない。works へのコミットは人の `room start` の回収）、と決めた。決定は root の `docs/decisions.md` の同日の項。
