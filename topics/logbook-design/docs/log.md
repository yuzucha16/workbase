# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `logbook/` の型を 2026-10-26 に決め（7 点、`decisions.md`）、`logbook/README.md` と `find_knowledge.py --check-aging` を入れた。`exmem/lessons/` の 6 ファイルに版依存の印を付けた（78df71b）。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は ①時系列の観測・測定、②版・時点に縛られる事実、③試行の途中。個人の好み・1 回きりの構成記録は含めない。
- ② は移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。降格するのは ①③ だけ。判断は 3 段チェック（確認の単位はファイル、降格と印の単位は節）。
- 第1〜3陣の本文確認は済み（`records/2026-10-26-wave{1,2,3}-review.md`）。第1陣の待ち行列 8 件は判断済み。2026-10-27 に畳み候補の「済」を削除し、`user-thinking-habits` と `user-manual` の Facts を移し、「聞」にユーザーが回答して 9 ファイルを畳んだ。「前」の 8 行も圧縮した（`decisions.md`）。

## Next Actions

1. 畳み候補（`records/2026-10-26-fold-candidates.md`）の残り: 「残」（残す）だけ。「前」は 2026-10-27 に圧縮した。「聞」は回答済みで畳んだが、判断が付かず残した項目がある（room の OQ 4 項、obsidian-vault-backup の NA 3 項、claude-code-storage の旧キーの OQ/NA、para-operations の OQ。範囲の判断は `decisions.md`）。
2. `--check-aging` の FAIL 1 件: `logbook/user-thinking-habits.md` が budget 32KB を 40 バイト超えた（2026-10-27 にクラウドで実行。他の 4 本は合格）。畳み方（圧縮か budget の付け直し）は 2026-11-29 の月次で決める。
3. （済 2026-10-27）印の付け忘れの確認: `shell-script-testing-wsl` の Gotchas（Claude Code の安全チェックの挙動）に一方向の印を付けた。Facts の Ubuntu 24.04 は作業時の環境の記録で、節単位の版依存ではないため付けない。
4. 別セッションで、`logbook/` が上位の md から辿れるかを確かめる(引当率、`topics/md-link-graph/` の道具)。
5. 試行: 2026-11-29 の月次の振り返りで、週次の記録(`kit-growth/records/`)を 1 回手で畳む(置き場は変えない)。
6. `shell-command-usecases` の素材の節に `素材` の印を付け、`logbook/README.md` の表の「素材」行を更新する。
7. 単価の 1 か所化: 案は `session-handoff` の Facts（版依存: 並存の節）に集約し、`claude-code-auth-providers` ほかは指す。承認後に実施。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか、上位の md から辿れるか。別セッションで引当率を測って決める(Next Actions 4)。
- 素材の節の扱い: lesson に残して印を付ける案(推奨)でよいか。

### 待ち行列(判断は、置いたセッションの次の `review 消化` 以降)

- 【決定 2026-10-27】追記の型は案 (b)、OQ・NA を本体に 1 つにまとめる。実施は次の追記から（既存ファイルの直しは `review 消化` で）。
- 【決定 2026-10-27】`shell-command-usecases` の素材は案 (a)、lesson に残して `素材` の印を付け、開始時に読まない。印の付与は未実施（Next Actions 6）。
- 【案を提示 2026-10-27】単価の 1 か所化。まとめ先の案は、ユーザーの承認待ち（下の Next Actions 7）。
