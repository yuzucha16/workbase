# 作業ログ（log）

`init` `open` フックを廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24。`a015bda` `c771c01` `45ee732`）。`brief 変更` の入口を足し、`brief-hook.md` と `review-hook.md` の字数超過を解消した（2026-10-24）。残りフック（`wrap` `stock` `integrate` `review`）と `room` の整合も見て反映した（2026-10-24。`hooks.md` の room 表を絞り、`wrap` のコミットは AI が行う）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- `stock` の `scope: area` の実機確認: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更（ユーザーの予告）があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。

- 旧名の読み替えと注記を消す（ユーザーの決定 2026-10-24。「現在の仕様が回りだしたら、読み替えもなくして消す」）。対象: `hooks.md` の旧名・旧ファイル名の項、各ノートの「旧 `init`」「旧 `start`」の注記、記録中の旧名。条件: `mkworks` の実機確認と、`brief` の運用で問題が出ないこと。
- `room mkworks` の実機確認（Windows）: 新しい PC の `mkworks`、既存の works の `mkworks --update`（基点が旧 `Template-Rev` のとき）。単体テストのみ。
- dotfiles の Claude 用スキルに、旧 `start` や「workflowを導入して」の入口があれば直す。

## Open Questions

- 【起票 10-24】場所: `script-guide.md` の束ねる役の型（Python・ps1）、`check_py.py` / `check-ps1.ps1`、`room-context.md` / 問題: 実行環境の違い（文字コードなど）のデバッグのラリー。既定ではログを出さないため、最初の失敗に情報が無く、再実行が1周余分に要る。原因の蓄積先も無い / 案: 毎回 `ai/work/diag.json`（環境、結果、失敗の型と場所。伏せ字つき）を出し、原因は `ai/out/knowledge/`（`scope: area`）の台帳に貯め、一般の原因は `scope: public` で上げて、3回で `check_py.py` に昇格する。works 共通の置き場は作らない。2026-10-21 の「既定ではログを出さない」を、診断に限って変える。仮決め済み（`decisions.md`）。進み（10-25）: 診断ログは `verify-result.json` / `run-result.json` として実装済み（Python と ps1。`diag.json` の名前は使わない。root の `decisions.md` の `run` / `verify` / `release` の項）。原因の台帳も 10-25 に実装した（ユーザーの承認。`script-guide.md` の「原因の台帳」、`room-context.md` に1項）。残りは実機: PC2 で verify を叩き、最初の失敗で台帳が使われるかを見る。
- `mkworks` は `Template-Rev` を新規に付けず `Room-Rev` に統一した。旧版の `room.py` で `--update` した works との行き来は考えていない。
