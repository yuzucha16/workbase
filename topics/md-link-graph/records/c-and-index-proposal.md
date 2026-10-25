# 論点 C と索引の自動生成の案（2026-10-25。Next Actions 3・4）

実機の要らない分を進めた結果。決めるのはユーザー。

## 論点 C: 未到達と入次数 0

`python -I topics/md-link-graph/tools/mdgraph.py` の再計測（2026-10-25、このセッション）: 178 ファイル、辺 1,516、到達 172、最大の循環 92%（163/178）、未到達 6、入次数 0 が 6。前回（193 ファイル、未到達 14、入次数 0 が 9）からの減りは、ファイルの整理による（トピックの削除など。内訳は追っていない）。

未到達の 6 件は、入次数 0 の 6 件と同じ。

この記録では 6 件のパスをバッククォートで書かない（書くと `mdgraph.py` がこの記録からの辺として数え、未到達が 0 に見える。2026-10-25 に一度そうなった）。

| ファイル | 何か | 読まれ方 | 案 |
|---|---|---|---|
| exmem/CLAUDE.md | 中身は `@AGENTS.md` の 1 行 | Claude Code が、そのディレクトリのファイルを読むときに自動で取り込む。リンクで辿るものではない | 数えない |
| topics/CLAUDE.md | 同上 | 同上 | 数えない |
| workflow-kit/templates/log.md | 雛形 | `room mkworks` のコードと、人が手本に見る。`workflow-kit/README.md` は `templates/AGENTS.md` `log.md` `decisions.md` と書くので、`log.md` が別のファイルに解決される | 数えない（雛形は読まれる知識ではない） |
| workflow-kit/templates/decisions.md | 同上 | 同上 | 同上 |
| topics/README.md | `topics/` の窓口 | root `README.md` は `topics/topics-index.md` と `topics/AGENTS.md` を指し、topics/README.md を指さない | root `README.md` の表の行に topics/README.md を足す |
| guides/README.md | `guides/` の窓口 | root `README.md` は入口を `guides/guides-index.md` と書き、guides/README.md を指さない | 同上（guides/README.md） |

推奨: `mdgraph.py` で `CLAUDE.md`（`@` の 1 行だけのもの）と `templates/` を数えない（測る道具の定義を変えるだけ。ノートは変えない）。窓口の 2 件は、root `README.md` の表にパスを書く（2 行の変更）。これで未到達と入次数 0 は 0 になる見込み（未試行）。

## 索引（`exmem-index.md`）の自動生成

現状を数えた（このセッション）: `exmem-index.md` の行 67、`exmem/lessons/` 67。抜けも、存在しないノートを指す行も無い。説明文が frontmatter の `title` と違う行が 9（`planning-method` `shell-script-testing-wsl` `change-method` `research-method` `research-method-2` `retrospective-method` `retrospective-method-2` `user-thinking-habits` `ai-isolated-work-room`）。違いは、索引の側が補足（`（Must / Want）`、`（改善4。定期）`、`.bat` の文字化け など）を足したもの。

| 案 | 良い点 | 悪い点 |
|---|---|---|
| A. `title` から生成し、手で書かない | ずれが出ない | 9 行の補足が消える。補足を残すには frontmatter に別の欄が要る |
| B. 生成せず、ずれだけ点検する（`find_knowledge.py --check-index` のような点検。`review` の入力 9 で回す） | 今の手書きの補足が残る。足すのは点検だけ | 直すのは人か AI の手 |
| C. 何もしない | 手間が無い | 今は揃っているが、`integrate` の手順（1 行足す）を忘れたときに気づけない |

推奨: B。今は 67/67 で揃っていて、生成の利点（ずれが出ない）が実際には効いていない。`triggers:` が依頼の引き当てを担うようになったので、索引は人が眺める用に寄り、手書きの補足に価値がある。
