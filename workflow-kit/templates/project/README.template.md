---
status: active
area: <Area 名>
type: <dev | inv>
review: <見直し日。ユーザーが承認するまでは「仮置き」と書く>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Project 名>

<目的を1〜2文。所属 Area: [[areas/<Area 名>/README|<Area 名>]]>

計画: [[projects/<Project 名>/ai/work/plan/6r|6R]]（`ai/work/plan/`。`plan` の出力。先頭の `status: 仮 | 正式` と `approved:` で承認を示す。6R が未作成の間は、リンクは未解決（Obsidian で薄く表示される。`plan` で作られると繋がる）。リンクは vault（works）の根からのパスで書く。`6r.md` は Project ごとにあり、短い名前だと別の Project に解決されるため）。完了条件・範囲外・未決は、ここ（6R）に書く。README には写さない

開発リポジトリ（`dev` で git のコードを扱うとき）: 上の frontmatter に `repos:`（url、where、branch。書式は `workflow-kit/project-structure.md`）を足す。無ければこの行を消す。

## 成果物

- `ai/out/<成果物名>/`: <最終成果物>

<!--
構造（project-structure.md）:
- 固定: README.md、ai/{docs,in,work,out,records}（`room open` が作る）、_noai/（原本・対応表・復元済みの成果物・人だけの仮置き `user/`。追跡しない）
- dev（作って保守する成果物）: ai/out/<成果物名>/ に src/、env/、tests/、tools/、docs/ から必要なもの（文書だけなら docs/ だけ。dev-deliverable-guide.md）
- inv（調べて結論を出す成果物）: ai/in/ に渡された資料、ai/work/ に集めた資料と抜粋、ai/out/<成果物名>/report.md に結論
- ai/ の下は、空のディレクトリを先に作らない。最初のファイルが来たときに作る。
この注記は、Project の README では削除する。
-->
