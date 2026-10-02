---
type: index
title: inbox
status: active
tags:
  - workflow
created: 2026-09-26
updated: 2026-09-26
---

# inbox

未整理の会話メモの一時置き場。
知識へ統合したらメモは削除する（手順は `../AGENTS.md`）。

ファイル名: `YYYY-MM-DD-<topic>.md`

## モバイル用の引き継ぎプロンプト

壁打ちの最後に、以下をAIに送って出力をそのまま保存する。
Obsidianのモバイルアプリで inbox に新規ノートを作って貼り付ければ、Obsidian SyncでPCに届く。

````text
この会話を、別のAIに引き継ぐためのMarkdownにまとめてください。
会話の再現ではなく、次の形式で要点だけを書き、全体を1つのコードブロックで出力してください。

ルール:
- tags は英小文字の kebab-case で3〜6個。ソフトウェアは tool/<名前>、AIサービスは ai/<名前> の形にする（例: tool/zed, ai/claude, keymap, setup）。
- 該当する内容がない見出しは省略する。
- 確認していないことは「仮説」と明記する。

---
type: inbox
title: <テーマ（日本語）>
tags:
  - <タグ>
created: <今日の日付 YYYY-MM-DD>
sources:
  - <このAIサービス名> conversation "<テーマ>"
---

# <テーマ>

## Goal
この会話で何を考えたかったか。

## Principles
判断の拠り所になる方針・原則（「〜しない」「〜を優先する」など）。

## Decisions
決めたこと。それぞれに根拠と、検討して捨てた案を書く。

## Facts
確認できた事実。未確認のものは「仮説」と明記する。

## Gotchas
実際に遭遇したエラーや詰まった点と、その解決方法。方針や一般的な注意点は Principles に書く。

## Open Questions
まだ決まっていないこと。

## Next Actions
次にやること。
````
