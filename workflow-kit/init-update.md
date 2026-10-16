# init: 雛形の反映（`init 更新`）

`init-hook.md` のモード。`init 更新`（別名「雛形を反映して」）と言われたときだけ読む。項目 5 で作ったワークスペースのトップに、その後の雛形（`templates/workspace/`）の変更を反映する。入力、自己点検、報告の型は、下に書いたもの以外は `init-hook.md` に従う。

前に反映した版の雛形（**基点**）から、新しい雛形（`resources/` の HEAD）への変更だけを、ローカルのファイルに当てる（3者マージ）。ローカルで埋めた行や足した行は、そのまま残る。まず案を出し、承認を得てから書く（`init-hook.md` の「既存のファイルは、上書きしない」の具体化）。

## 場所と対象

- 起動する場所は、ワークスペースのトップ（`AGENTS.md` と `resources/` がある単位）。`resources/` の中で言われたときは、対象をワークスペースのトップ（`resources/` の親）とする。
- 対象は、次の表のファイルだけ。`docs/` の中身、`areas/` `projects/` `archives/`、`_noai/`、`resources/`、`resources_p/` の中身、`.obsidian` は、読まない・書かない。
- `resources/` の pull はしない（人が行う）。push もしない。

| ローカル | 雛形（`workflow-kit/templates/workspace/`） | 扱い |
|---|---|---|
| `README.md` | `README.md` | 3者マージ（埋めた行と、足した行が残る）。ローカルに無ければ、手順 4 で作る |
| `AGENTS.md` | `AGENTS.md` | 3者マージ（埋めた行が残る） |
| `.gitignore` | `gitignore.template` | 3者マージ |
| `.ignore` | `ignore.template` | 3者マージ |
| `.gitattributes` | `gitattributes.template` | 3者マージ |
| `.claude/settings.json` | `claude-settings.template.json` | `permissions.deny` の集合で合わせる（下の手順 3） |
| `.git/hooks/pre-push` | `pre-push.template` | ローカルにあるときだけ3者マージ（remote の方針が「なし」の PC）。追跡されない |

雛形を足す・消す・改名したら、この表を同じコミットで直す。

## 手順

1. **確認する**（変更しない）。
   - `resources/` に未コミットの変更が無い（`git -C resources status --porcelain` が空）。あれば止まる（その状態の雛形は、後から再現できない）。
   - 新しい版: `git -C resources rev-parse --short HEAD`。
   - 基点: ワークスペースのコミットの、最新の `Template-Rev` トレーラー（`git log --format='%(trailers:key=Template-Rev,valueonly)' | grep -m1 .`）。無ければ、最初のコミットの `Kit-Rev`（`git log --reverse --format='%(trailers:key=Kit-Rev,valueonly)' | grep -m1 .`）を候補にする。末尾が `-dirty` の候補や、`resources/` に無いハッシュ（`git -C resources cat-file -e <基点>^{commit}` が失敗）は使わない。
   - 基点 = 新しい版なら、「反映するものなし」と報告して終わる。
   - 雛形の変更の一覧: `git -C resources diff --stat <基点> HEAD -- workflow-kit/templates/workspace/ workflow-kit/init-workspace.md`。上の表に無い雛形が増えていたら、止まって報告する（表を先に直す）。`init-workspace.md` の変更は、ファイル以外の手順（ディレクトリの作成など）の変更なので、手順 4 で拾う。
   - 対象のローカルのファイルに、未コミットの変更が無い（`git status --porcelain -- <ファイル>`）。あれば、そのファイルは案だけ出して書かない。
2. **案を作る**（変更しない）。作業用のファイルは、ワークスペースの外（OS の一時ディレクトリ）に置き、終わったら消す。
   - 基点の雛形と新しい雛形を取り出す（`git -C resources show <版>:workflow-kit/templates/workspace/<雛形>`）。
   - 3者マージ: `git merge-file -p <ローカル> <基点の雛形> <新しい雛形>`（ローカルを書き換えない）。終了コードが衝突の数。結果とローカルの差分（`diff -u`）が、そのファイルの案。
   - 衝突した箇所は、自動で決めない。両方を示して、ユーザーに選んでもらう。
   - 基点が無いとき（候補が使えないとき）は、その回だけ、新しい雛形とローカルの2者の差分を案にする。埋めた行（プレースホルダ `<` `>` に当たる行）は残す前提で、雛形の変更に当たる行だけを、案として示す。
3. **`.claude/settings.json` は集合で合わせる。** `deny` を、ローカル ∪（新しい雛形 − 基点の雛形）にする。基点の雛形にあって新しい雛形から消えた項目は、自動で消さない（安全網を黙って緩めない）。報告に並べ、消すかはユーザーが決める。`deny` 以外の項目は触らない。
4. **足りない生成物を確かめる。** 新しい `init-workspace.md` の「生成する」のうち、ファイル以外（`areas/` などの `.gitkeep`、`resources_p/` など）で、無いものを案に足す。既存は上書きしない。
5. **案を報告して、承認を待つ。** ファイルごとに、差分、衝突、消さなかった `deny` を示す。承認の前に書かない。
6. **承認されたものを書く。** 承認されなかったファイルは、そのままにする。
7. **自己点検を通す**（下の節と、`init-hook.md` の自己点検の「ワークスペースを生成した場合」のうち、ファイルの有無と ignore の確認）。
8. **コミットする**（`docs-rules.md` の「コミットと push」に従う）。追加するのは、手順 6 で書いた追跡対象のファイルだけ（パス指定）。メッセージは `[works] init 更新: 雛形を <基点>..<新しい版> に合わせる`。トレーラーは、通常の2行に加えて `Template-Rev: <新しい版>`（次回の基点になる）。承認されたファイルが1つも無いときはコミットしない（`Template-Rev` も残らないので、次回も同じ基点から案が出る）。一部だけ承認されたときも、`Template-Rev` は新しい版にし、承認されなかった変更を報告に残す（次回の案には出ないため）。

## 報告の型

1. **版**: 基点（出どころ: `Template-Rev` / 初回コミットの `Kit-Rev` / なし）と新しい版。雛形の変更の一覧（ファイルと行数）。
2. **ファイルごとの結果**: 置き換えた / 3者マージした / 衝突あり（選んだ側）/ 案のまま残した（理由: 未承認、ローカルに未コミットの変更）。
3. **消さなかったもの**: 雛形から消えた `deny` や行。
4. **作った生成物**（手順 4）。
5. **コミット**: ハッシュ、`Template-Rev`、含めなかったファイル。
6. **改善案**（あったときだけ）: `hook-common.md` の「改善」に従う。

## 自己点検

- [ ] `resources/` が未コミットの変更なしで、新しい版はその HEAD
- [ ] 書き込んだのは、上の表のファイルと手順 4 の生成物だけ。`docs/`、PARA、`_noai/`、`resources/`、`resources_p/` の中身、`.obsidian` に触れていない
- [ ] 承認の前に書いていない。衝突を自動で決めていない
- [ ] `settings.json` の `deny` を、ユーザーの決定なしに減らしていない
- [ ] 書いたファイルに、マージの印（`<<<<<<<` `=======` `>>>>>>>`）が残っていない。ローカルで埋めた行（役割、remote、固有ルール）が、雛形のプレースホルダに戻っていない
- [ ] コミットに `Template-Rev` が付き、生成物だけを含む（`git show --stat HEAD`）。push していない
- [ ] 一時ファイルを消した
