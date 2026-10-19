---
status: active
area: <Area 名>
type: <doc | dev | dev-env | dev-test | research>
data: <none | mask | restore。dev は none だけ。room/README.md の「データの扱い」>
review: <見直し日。ユーザーが承認するまでは「仮置き」と書く>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Project 名>

<目的を1〜2文。所属 Area: [[areas/<Area 名>/README|<Area 名>]]>

## いま / あなた待ち / 次の一手

<各1行。詳細は `docs/log.md`。`docs/` が無い小さな Project では省く。README が窓口の役を兼ねる（予算 2KB）>

## 完了条件

<1文。ユーザーが承認してから書く（承認の前に「ユーザー承認: 日付」を書かない）>

## 成果物

- `ai/out/<成果物名>/`: <最終成果物>

## 範囲外

- <やらないこと>

## Open Questions

- <未決の事項>

<!--
構造（project-structure.md）:
- 固定: README.md、ai/{docs,in,work,out,records}（`room open` が作る）、_noai/（原本・対応表・復元済みの成果物・人だけの仮置き `user/`。`data:` に応じて作る。追跡しない）
- doc: ai/in/ に渡された資料、ai/work/ に版ごとの下書き、ai/out/<成果物名>/ に最終版
- dev: ai/out/<成果物名>/ に src/、tests/、tools/、ビルド設定（dev-deliverable-guide.md）
- dev-env: ai/in/ に対象環境の情報、ai/out/<成果物名>/ に環境定義と確認スクリプト（dev-deliverable-guide.md「dev-env と dev-test」）
- dev-test: ai/in/ にテスト対象と、その要求仕様、ai/out/<成果物名>/ に tests/ とテスト仕様、report.md
- research: ai/in/ に渡された資料、ai/work/ に集めた資料と抜粋、ai/out/<成果物名>/report.md に結論
- ai/ の下は、空のディレクトリを先に作らない。最初のファイルが来たときに作る。
この注記は、Project の README では削除する。
-->
