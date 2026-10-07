---
status: active
area: <Area 名>
type: <doc | dev | research>
review: <見直し日。ユーザーが承認するまでは「仮置き」と書く>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Project 名>

<目的を1〜2文。所属 Area: [[areas/<Area 名>/README|<Area 名>]]>

## 完了条件

<1文。ユーザーが承認してから書く（承認の前に「ユーザー承認: 日付」を書かない）>

## 成果物

- `<最終成果物>`: <直下に置く>

## 範囲外

- <やらないこと>

## Open Questions

- <未決の事項>

<!--
構造（open-hook.md「Project の構造」）:
- 固定: README.md、docs/（log.md と decisions.md。複数セッションにまたがるときだけ）、最終成果物（直下）
- doc: drafts/（版ごとの下書き、レビュー版）、refs/（渡された資料、チェックリスト）
- dev: src/、tests/、tools/、ビルド設定
- research: sources/（収集した資料と抜粋）、report.md（結論。直下）
- 空のディレクトリは先に作らない。最初のファイルが来たときに作る。深さは Project 直下から2階層まで。
この注記は、Project の README では削除する。
-->
