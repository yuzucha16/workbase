# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 実装はまだ無い（`logbook/` ディレクトリも、`exmem` の変更も無い）。決定は `decisions.md` の 2026-10-26。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は 3 つ: ①時系列の観測・測定、②版・時点に縛られる事実（版が上がるだけのものを含む）、③試行の途中。個人の好み・1 回きりの構成記録は含めない（ユーザーが直接削除する）。素材（履歴の種など）は別扱い。
- ② は `logbook/` に移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。並存型（Python のように下げうる）は版つきの表、一方向型は上書きして古いものを捨てる。降格するのは ①③ だけ。
- 降格は承認プロセスの 3 段チェックで決める。確認の単位はファイル、降格と印の単位は節。
- 第1陣（5 ファイル）の本文確認は済み（`records/2026-10-26-wave1-review.md`）。第1陣の 5 項目は、下の Open Questions の待ち行列に置いた（2026-10-26。判断は次の `review 消化` 以降）。`ai-work-metrics` の ③（`bare`/`briefed` の試行、雛形）は、ユーザーの判断で畳み済み（`exmem/lessons/ai-work-metrics.md`）。
- 第2陣（6 ファイル）の本文確認は済み（`records/2026-10-26-wave2-review.md`）。logbook へ移すものはほぼ無く、主な作業は ② の印と、1 回きりの移行の記録・古い ③ の畳み。第3陣（`para-operations` `session-handoff`）の本文確認も済み（`records/2026-10-26-wave3-review.md`。logbook へ移すのは測定値だけ）。

## Next Actions

1. 次の `review 消化`（「logbook-design の続き」）で、待ち行列の 7 件をスクリーニングし、ユーザーが 1 件ずつ判断する。
2. 第2陣の現況確認は済み。旧 `C:\vault` は消してよい（ユーザー、2026-10-26。消す作業自体は PC 上で、ユーザーが行う）。回答済み（2026-10-26）: MX Linux は導入済み（`linux-distro-selection` の Next Actions は畳める）、`claude-code-auth-providers` の Next Actions は完了（畳める）、vault のバックアップ（robocopy）は未設定（`obsidian-vault` の Next Actions に残す）。畳みは待ち行列の第2陣の項で行う。
3. 第3陣の現況をユーザーに確認する: `para-operations` の Next Actions（Area の雛形、open の雛形、2 回目の Project）が今も現役か、`session-handoff` の Next Actions（2026-10-17〜18 時点）が現役か。
4. 最小の `logbook/` の型を決める: 節（いま／明細）、frontmatter（`review_by` `budget`）、スクリーニング（`find_knowledge.py` に `--check-aging` 相当を足すか。日数は暫定 60）、`triggers` 索引の対象にするか。実装は承認の後。
5. 別セッションで、`logbook/` に上位の md（`AGENTS.md` `README.md` `exmem/` の索引など）から辿れるかを確かめる（引当率、`topics/md-link-graph/` の道具。`find_knowledge.py --triggers` の対象にするかも同時に決める）。実装の後。
6. 試行: 2026-11-29 の月次の振り返りで、週次の記録（`kit-growth/records/`）を 1 回手で畳んでみる（置き場は変えない）。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか、上位の md から辿れるか（短命の内容が引き当てを汚す一方、取扱説明書の観測は引きたい）。別セッションで引当率を測って決める（Next Actions 5）。
- 公開範囲: `user-thinking-habits` の追補は「癖の評価は公開側に置かない」と書きつつ癖の表を載せている。降格のときに合わせて確認する。
- 素材の節の扱い: lesson に残して印を付ける案（推奨）でよいか。

### 待ち行列（3 段チェックの 1 段目。2026-10-26 に置いた。判断は次の `review 消化` 以降）

- 場所: `exmem/lessons/user-thinking-habits.md` / 問題: 31KB 全体が「分析の実行ごとに足される観測」（①）。公開リポジトリで、追補は「癖の評価は公開側に置かない」と書きつつ癖の表を載せている / 案: `logbook/user-thinking-habits.md` へ移す（ファイル名は変えず `[[user-thinking-habits]]` を保つ）。移す前に公開範囲をユーザーが確認する。補正策は `user-manual` の Principles にあるので、明細は圧縮してよい。
- 場所: `exmem/lessons/user-manual.md` の Facts（確認: 日付つきの観察 9 項） / 問題: ① の性質で、繰り返し確認されたものは Principles に昇格済み / 案: 上の `logbook/user-thinking-habits.md` の「明細」に合流する。Principles・Decisions・Gotchas は残す。
- 場所: `exmem/lessons/ai-work-metrics.md` の実測値（Facts のうち 52 本・中央値・最大 5 日など） / 問題: 2026-10-06 の測定値（①）。形式の事実（②一）は `claude-code-storage` と重複 / 案: 実測値を `logbook/ai-work-metrics.md` の「明細」へ。形式の事実は 1 か所にまとめて印を付ける。③ の畳みは済み。
- 場所: `exmem/lessons/shell-command-usecases.md` の「傾向（2026-10-04 時点）」 / 問題: 件数つきの 1 回の測定（①）。素材（履歴の種、約 15.5KB）は lesson 内で読み込みが重い / 案: 傾向を `logbook/` の「明細」へ移し、lesson には結論 1 行を残す。素材は (a) lesson に残して節に `素材` の印を付け、サイズの予算の対象外にする。
- 場所: `exmem/lessons/claude-code-storage.md` / 問題: 3 回の追記が別々の Principles／Decisions／Facts を持つ。Stop フックの Open Questions と Next Actions（2026-10-17 時点）は 10-21 に実装済みで古い。1 回きりの移行の Decisions が残る / 案: Facts に ②一の印を付け、古い ③ と 1 回きりの移行の記録を畳む。
- 場所: 第2陣 6 ファイル（`records/2026-10-26-wave2-review.md` の 3） / 問題: 降格より整理が主。② の節への印の付与と、X・古い ③ の畳みの 2 件にまとまる。現況の確認が先に要る項目がある / 案: 2 件に分けて載せる。
- 場所: 仕組み（lessons の整理の経路） / 問題: 「1 回きりの構成記録はユーザーが直接削除する」と決めてあるが、AI が古い ③ と X を見つけて畳む案を出す経路が無い。追記のたびに Facts／OQ／NA を持つ形が、ファイルを太らせる / 案: (a) `review 消化` の 1 段目（すでに close していそうなもの）を lessons に広げる。(b) 追記の型を変え、OQ・NA は本体の 1 つにまとめる。
- 場所: 第3陣 2 ファイル（`records/2026-10-26-wave3-review.md` の 3） / 問題: 降格は測定値（`para-operations` の Facts、`session-handoff` の実験の費用）だけ。残りは古い ③ の畳みと、単価・TTL への印 / 案: 2 件に分けて載せる。現況の確認が先。
