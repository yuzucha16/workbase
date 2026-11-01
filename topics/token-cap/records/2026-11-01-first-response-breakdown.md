# 最初の応答の入力の分解（2026-11-01、NA 7）

対象: この日の token-cap の続きの会話（resources 起動、Windows 側）。会話記録の `attachment` 行を種類ごとに数えた（文字数。JSON の行の長さなので、エスケープを含み、トークンではない）。

最初の応答の入力: 26,519 トークン（キャッシュ読み 16,027 + 書き込み 10,490 + 新規 2）。`/context` の合計 20.2k との差は約 6.3k。

| 添付の種類 | 文字数 | 内容 |
|---|---|---|
| skill_listing | 23,141 | スキルの一覧（名前＋説明文。`/context` の Skills 3.6k に相当） |
| instructions | 9,225 | CLAUDE.md / AGENTS.md / メモリ（`/context` の Memory 2.8k に相当） |
| prompt_snapshot | 7,907 | 内容は未確認 |
| deferred_tools_delta | 5,244 | 遅延ツールの名前一覧 |
| mcp_instructions_delta | 4,605 | MCP の指示（`/context` の MCP 0.72k に相当） |
| agent_listing_delta | 3,731 | エージェントの種類の一覧 |
| session_context | 2,714 | git 状態など |
| environment / model / hook_success / date / credential_org | 計 約 4,300 | 環境、フックの出力など |

## わかったこと

- `/context` に出ない添付は、遅延ツールの名前一覧（5.2k 文字）、エージェントの一覧（3.7k 文字）、session_context（2.7k 文字）、環境・フック（約 4.3k 文字）。合計 約 16k 文字で、日本語混じりの換算（約 0.4〜0.5 トークン/文字相当）にすると 5〜7k トークン。差 6.3k とほぼ合う。仮説 (c) が主因。
- 差の中身は、ほぼハーネスが付ける注記で、workbase の仕組みでは動かせない。動かせるのは、フックの出力（約 1.1k 文字）と、`instructions`（AGENTS.md の連鎖）だけ。
- 結論: 動かせる土台の上限は `2026-11-01-base-breakdown.md` の約 2.4〜3.0k のまま。差の 6.3k は新しい動かせる量にならない。

## 限界

- トークンの内訳は直接取れない（文字数からの見積もり）。`prompt_snapshot` の中身は読んでいない。
- 1 会話だけ。会話ごとにスキル・エージェントの一覧は変わりうる。
