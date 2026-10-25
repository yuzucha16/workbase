# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 実装はまだ無い（`logbook/` ディレクトリも、`exmem` の変更も無い）。決定は `decisions.md` の 2026-10-26。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は 3 つ: ①時系列の観測・測定、②版・時点に縛られる事実（版が上がるだけのものを含む）、③試行の途中。個人の好み・1 回きりの構成記録は含めない（ユーザーが直接削除する）。素材（履歴の種など）は別扱い。
- ② は `logbook/` に移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。並存型（Python のように下げうる）は版つきの表、一方向型は上書きして古いものを捨てる。降格するのは ①③ だけ。
- 降格は承認プロセスの 3 段チェックで決める。確認の単位はファイル、降格と印の単位は節。
- 第1陣（5 ファイル）の本文確認は済み（`records/2026-10-26-wave1-review.md`）。第2陣（版依存「中」: `claude-code-auth-providers` `linux-distro-selection` `obsidian-vault` `ai-isolated-work-room` `shell-script-testing-wsl` `workflow-kit`）と、第3陣（`para-operations` `session-handoff`）は未確認。

## Next Actions

1. 第1陣の仕分け（wave1-review の 4）を 3 段チェックに載せる。`review 消化` で行うか、このトピックで行うかはユーザーが決める。
2. `ai-work-metrics` の Next Actions（10-06〜07 時点）が現役か、ユーザーに確認する。
3. 第2陣の本文確認。節ごとに型（②並／②一／③）を付け、wave2 の記録を `records/` に足す。
4. 最小の `logbook/` の型を決める: 節（いま／明細）、frontmatter（`review_by` `budget`）、スクリーニング（`find_knowledge.py` に `--check-aging` 相当を足すか。日数は暫定 60）、`triggers` 索引の対象にするか。実装は承認の後。
5. 試行: 2026-11-29 の月次の振り返りで、週次の記録（`kit-growth/records/`）を 1 回手で畳んでみる（置き場は変えない）。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか（短命の内容が引き当てを汚す一方、取扱説明書の観測は引きたい）。
- 公開範囲: `user-thinking-habits` の追補は「癖の評価は公開側に置かない」と書きつつ癖の表を載せている。降格のときに合わせて確認する。
- 素材の節の扱い: lesson に残して印を付ける案（推奨）でよいか。
