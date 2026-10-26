# 作業ログ（log）

`logbook-design`（期限のあるナレッジの置き場 `logbook/` の設計）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `logbook/` の型を 2026-10-26 に決め（7 点、`decisions.md`）、`logbook/README.md` と `find_knowledge.py --check-aging` を入れた。`exmem/lessons/` の 6 ファイルに版依存の印を付けた（78df71b）。
- 置き場: workbase 直下の `logbook/`（仮決め）。入る型は ①時系列の観測・測定、②版・時点に縛られる事実、③試行の途中。個人の好み・1 回きりの構成記録は含めない。
- ② は移さず、lessons の節に印（`<!-- 版依存: 一方向|並存 / 確認: 日付 -->`）を付けて残す。降格するのは ①③ だけ。判断は 3 段チェック（確認の単位はファイル、降格と印の単位は節）。
- 第1〜3陣の本文確認は済み（`records/2026-10-26-wave{1,2,3}-review.md`）。第1陣の待ち行列 8 件は `review 消化` で判断済み（`decisions.md`）。移すのは測定値が主。

## Next Actions

1. 畳む候補（`records/2026-10-26-fold-candidates.md`）の「聞」にユーザーが答え、削除する（AI は挙げるだけ）。「済」は根拠つきなので消してよい。Stop フックの実機記録、旧 `C:\vault` の削除、`obsidian-vault` のバックアップ未設定は、ユーザーの PC でしか確かめられない。
2. 第2陣の旧名の更新は書き換える対象がほぼ無かった。畳み（1）で消えるので、閉じてよいかをユーザーに聞く。残る 1 か所は `para-operations` の開始インタビュー（旧 `start`）。
3. 印の付け忘れの確認: `shell-script-testing-wsl` は節単位の版依存が無く付けていない。
4. 移す残り（2026-10-26 承認）: `user-thinking-habits`（ファイルごと。公開範囲は解消済み）、`user-manual` の Facts 9 項（先に各項と Principles の対応表を出し、未昇格を確かめてから明細へ合流）。済みは `ai-work-metrics` `shell-command-usecases` `para-operations` `session-handoff`。`--check-aging` は、この PC で Python がブロックされ未実行。
5. 別セッションで、`logbook/` が上位の md から辿れるかを確かめる(引当率、`topics/md-link-graph/` の道具)。実装の後。
6. 試行: 2026-11-29 の月次の振り返りで、週次の記録(`kit-growth/records/`)を 1 回手で畳む(置き場は変えない)。

## Open Questions

- `logbook/` を `find_knowledge.py --triggers` の対象にするか、上位の md から辿れるか。別セッションで引当率を測って決める(Next Actions 5)。
- 素材の節の扱い: lesson に残して印を付ける案(推奨)でよいか。

### 待ち行列(判断は、置いたセッションの次の `review 消化` 以降)

- 【保留 2026-10-26】lessons の追記の型: 追記のたびの Facts／OQ／NA がファイルを太らせる。案 (b) OQ・NA を本体に 1 つにまとめる。代替: NA に起票日だけ付ける。10-19 の R-02 の却下と同じ理由で覆りやすい。(a) は正式化済み(`docs/decisions.md` 直下)。
- 【保留 2026-10-26】`exmem/lessons/shell-command-usecases.md` の素材(約 15.5KB、dotfiles が正本として読む)。(a) lesson に残し `素材` の印、開始時に読まない。(b) `exmem/seeds/` を新設(dotfiles の読み先も変わる)。dotfiles へ移す案は依存の向きに反するので除く。
- 単価の記述が複数の lessons にある(`records/2026-10-26-wave3-review.md` の観察 3)。1 か所にまとめ、他は指す。まとめ先は実施の前に 3 行で示す。
