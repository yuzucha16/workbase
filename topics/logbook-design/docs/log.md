# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `logbook/` の型を 2026-10-26 に決め（7 点、すべて推奨どおり。`decisions.md`）、`logbook/README.md` と `find_knowledge.py --check-aging` を入れた。中身のファイルはまだ無い。`exmem/lessons/` の 6 ファイルに版依存の印を付けた（2026-10-26、78df71b）。決定は `decisions.md` の 2026-10-26。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は 3 つ: ①時系列の観測・測定、②版・時点に縛られる事実（版が上がるだけのものを含む）、③試行の途中。個人の好み・1 回きりの構成記録は含めない（ユーザーが直接削除する）。素材（履歴の種など）は別扱い。
- ② は `logbook/` に移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。並存型（Python のように下げうる）は版つきの表、一方向型は上書きして古いものを捨てる。降格するのは ①③ だけ。
- 降格は承認プロセスの 3 段チェックで決める。確認の単位はファイル、降格と印の単位は節。
- 第1陣（5 ファイル）の本文確認は済み（`records/2026-10-26-wave1-review.md`）。第1陣の 5 項目を含む待ち行列 8 件は、2026-10-26 の `review 消化` で判断した（スクリーニングは `records/2026-10-26-queue-screening.md`、結果は `decisions.md`）。`ai-work-metrics` の ③（`bare`/`briefed` の試行、雛形）は、ユーザーの判断で畳み済み（`exmem/lessons/ai-work-metrics.md`）。
- 第2陣（6 ファイル）の本文確認は済み（`records/2026-10-26-wave2-review.md`）。logbook へ移すものはほぼ無く、主な作業は ② の印と、1 回きりの移行の記録・古い ③ の畳み。第3陣（`para-operations` `session-handoff`）の本文確認も済み（`records/2026-10-26-wave3-review.md`。logbook へ移すのは測定値だけ）。

## Next Actions

1. 畳む候補（`records/2026-10-26-fold-candidates.md`）の「聞」にユーザーが答え、削除する（AI は挙げるだけ。2026-10-26 承認）。「済」は根拠つきなので、そのまま消してよい。Stop フックの実機での記録、旧 `C:\vault` の削除、`obsidian-vault` のバックアップ（robocopy）の未設定は、ユーザーの PC でしか確かめられない。
2. 第2陣の旧名の更新は、調べた結果、書き換える対象がほぼ無かった（`room` のコマンドの `init` `open` `start` `close` は今もある）。畳み（1）で消えるので、閉じてよいかをユーザーに聞く。残る 1 か所は `para-operations` の開始インタビュー（旧 `start`）。
3. 印の付け忘れの確認: `shell-script-testing-wsl` は節単位の版依存が無く付けていない。単価・TTL の 1 か所化は別件で待ち行列にある。
4. 移す（2026-10-26 承認。型は同日に決定・実装済み）。済み（2026-10-26）: `ai-work-metrics`（実測は `logbook/ai-work-metrics-log.md`、形式の事実は `claude-code-storage` の「jsonl の形式」）、`shell-command-usecases` の傾向、`para-operations` の開始時の実測、`session-handoff` の実験の費用（それぞれ `logbook/*-log.md`、lesson に結論 1 行と `→` を残した）。残り: `user-thinking-habits`（ファイルごと。公開範囲の食い違いは、ユーザーが「癖の評価は公開側に置かない」の一文を削除して解消した。2026-10-26。癖の表を公開側に置いてよいかは、ユーザーが一文を削除したことで決着とみなした）、`user-manual` の Facts 9 項（先に各項と Principles の対応表を出し、未昇格の項を確かめてから明細へ合流）。`--check-aging` は、この PC で Python がブロックされ未実行。
5. 別セッションで、`logbook/` に上位の md（`AGENTS.md` `README.md` `exmem/` の索引など）から辿れるかを確かめる（引当率、`topics/md-link-graph/` の道具。`find_knowledge.py --triggers` の対象にするかも同時に決める）。実装の後。
6. 試行: 2026-11-29 の月次の振り返りで、週次の記録（`kit-growth/records/`）を 1 回手で畳んでみる（置き場は変えない）。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか、上位の md から辿れるか（短命の内容が引き当てを汚す一方、取扱説明書の観測は引きたい）。別セッションで引当率を測って決める（Next Actions 5）。
- 素材の節の扱い: lesson に残して印を付ける案（推奨）でよいか。

### 待ち行列（3 段チェックの 1 段目。判断は、置いたセッションの次の `review 消化` 以降）

- 【保留 2026-10-26】場所: 仕組み（lessons の追記の型） / 問題: 追記のたびに Facts／OQ／NA を持つ形が、ファイルを太らせる / 案: (b) 追記の型を変え、OQ・NA は本体の 1 つにまとめる。代替: lessons の NA に起票日を付けるだけにする。10-19 の R-02（NA の追記は 3 回まで）の却下と同じ理由で覆りやすい。(a)（`review 消化` で列挙だけ）は 2026-10-26 に正式化済み（`docs/decisions.md` 直下）。
- 【保留 2026-10-26】場所: `exmem/lessons/shell-command-usecases.md` の素材（履歴の種、約 15.5KB。dotfiles が正本として読む元） / 問題: lesson 内で読み込みが重い / 案: 推奨なしで選ぶ。(a) lesson に残して節に `素材` の印を付け、開始時に読まない。(b) `exmem/seeds/` を新設して切り出す（dotfiles 側の読み先も変わる）。dotfiles 側へ移す案は依存の向きに反するので除く。「サイズの予算」は 10-15 に lessons の字数の目安を見送っているので前提にしない。
- 場所: 単価の記述（`session-handoff` ほか複数の lessons。`records/2026-10-26-wave3-review.md` の観察 3） / 問題: 同じ単価が複数のファイルにあり、版が上がると直し漏れる / 案: 1 か所にまとめ、他は指す。まとめ先は実施の前に 3 行で示す（2026-10-26 に置いた）。
