# 作業ログ（log）

`init` `open` フックを廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24。`a015bda` `c771c01` `45ee732`）。`brief 変更` の入口を足し、`brief-hook.md` と `review-hook.md` の字数超過を解消した（2026-10-24）。残りフック（`wrap` `stock` `integrate` `review`）と `room` の整合も見て反映した（2026-10-24。`hooks.md` の room 表を絞り、`wrap` のコミットは AI が行う）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- `stock` の `scope: area` の実機確認: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更（ユーザーの予告）があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。

- 旧名の読み替えと注記は 2026-10-26 に消した（`hooks.md` の旧名の項 4 つ、`workflow-kit/README.md` の旧ファイル名、`project-structure.md` `room-context.md` `session-goal-modes.md` `ai-development-workflow.md` の注記）。残したもの: `hooks.md` のディレクトリ名の改名（`knowledge/` `cheatsheets/`）、`docs-rules.md` の `Template-Rev`（`mkworks --update` が読む）、`guides/explain/` の経緯の説明、各 `records/` と `log-history.md` の履歴。`mkworks` の実機確認は同日にユーザーが済ませた（問題なし）。
- 【起票 10-25】PC2 の Windows で `verify.bat` と `verify.ps1` を 1 回ずつ叩く（uv の取得、文字コード、y/n と日本語のひとこと）。最初の失敗が、原因の台帳（`script-guide.md`）の初めての使用になる。`run.py` の型と ps1 版は Linux でのみ確認（2026-10-25）。
- dotfiles の旧入口（10-26 に調べた）: Claude 用スキル（`SKILL.md`、commands）は dotfiles に無い。旧入口は `docs/setup/win11.md` の「workflowを導入して」1か所だけで、`room mkworks` に直してコミットした（dotfiles の `e53f684`、2026-10-26 に push 済み）。

## Open Questions

- 【起票 10-24】場所: `script-guide.md` の束ねる役の型（Python・ps1）、`check_py.py` / `check-ps1.ps1`、`room-context.md` / 問題: 実行環境の違い（文字コードなど）のデバッグのラリー。既定ではログを出さないため、最初の失敗に情報が無く、再実行が1周余分に要る。原因の蓄積先も無い / 案: 毎回 `ai/work/diag.json`（環境、結果、失敗の型と場所。伏せ字つき）を出し、原因は `ai/out/knowledge/`（`scope: area`）の台帳に貯め、一般の原因は `scope: public` で上げて、3回で `check_py.py` に昇格する。works 共通の置き場は作らない。2026-10-21 の「既定ではログを出さない」を、診断に限って変える。仮決め済み（`decisions.md`）。進み（10-25）: 診断ログは `verify-result.json` / `run-result.json` として実装済み（Python と ps1。`diag.json` の名前は使わない。root の `decisions.md` の `run` / `verify` / `release` の項）。原因の台帳も 10-25 に実装した（ユーザーの承認。`script-guide.md` の「原因の台帳」、`room-context.md` に1項）。残りは実機: PC2 で verify を叩き、最初の失敗で台帳が使われるかを見る。
- `mkworks` は `Template-Rev` を新規に付けず `Room-Rev` に統一した。旧版の `room.py` で `--update` した works との行き来は考えていない。
