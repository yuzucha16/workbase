---
type: inbox
title: Claude Code のセッションの費用と ID を、Stop フックで記録する
tags:
  - ai/claude
  - tool/claude-code
  - hooks
  - cost
  - transcript
  - zed
created: 2026-10-17
sources:
  - Claude Code conversation "Zed 経由で session_id と費用を取る"
---

# Claude Code のセッションの費用と ID を、Stop フックで記録する

## Goal
各フックの最終処理で、セッションの ID と費用を見たかった。Zed の AI agents（ACP 経由）から Claude Code を使う環境で、`/status` と `--output-format json` が使えるか、使えなければ何で代えるかを調べ、Stop フックで記録する手順にした。
統合先の候補: lessons/claude-code-storage.md（キーワード: claude-code, transcript, jsonl, hook）。広い候補: 新規トピック（キーワード: stop hook, session_id, cost, usage, acp）

## Principles
- 会話の中でスラッシュコマンドや `claude -p` の出力に頼らず、フックが受け取る入力と transcript で代える。理由: スラッシュコマンドはユーザーが打つもので AI が実行できず、`claude -p` は別セッションの値を返す。
- 毎回の記録は、モデルを通さないフック（Stop）で行い、標準出力に何も出さない。理由: AI の手順の最後に足すと往復が1回増え、会話全体のキャッシュ読みの分だけ費用が増える（1回あたり約1.6円、キャッシュ切れで約40円）。
- 費用は「推定」と明記して記録し、正は `/usage` にする。理由: transcript にない内部の呼び出しがあり、実測で数%低く出る。

## Decisions
- **セッションの費用と ID は、Stop フックのスクリプトで記録する**（2026-10-17）
  - 根拠: ユーザーの依頼（「stop フックの方向で手順作成を」）。
  - 却下案: 手順書の最後に AI が集計を実行（往復が増える）、statusline（Zed に表示されない）、`claude -p` の JSON（別セッションの値）。

## Facts
- Stop フックの入力には `session_id`、`transcript_path`、`cwd`、`last_assistant_message` があり、費用や使用量の項目は無い（確認: 2026-10-17、根拠: `claude -p` で Stop フックを動かして入力 JSON を保存して見た）。
- Stop フックの標準出力は、会話に入らない（`UserPromptSubmit` `SessionStart` などの例外にない）。公式の文面からの読み取りで、実測では出力した目印が応答に現れなかった（仮説）。
- transcript の `assistant` 行は同じ `message.id` が複数あるため、id で重複を除いて合計する。単価は、入力・出力・キャッシュ読み・キャッシュ書き込み（1時間と5分で別）に分けて掛ける。Haiku 5.5 は、1リクエストの入力が10万トークンを超えると高い単価になる（確認: 2026-10-17、根拠: 公式の価格表。`claude -p` の `modelUsage` の値で Haiku の1リクエストを手計算し、$0.0027926 と一致）。
- transcript の集計は、`claude -p` の費用より約3%低かった（0.0027 対 0.00279）。transcript にない内部の呼び出しがあるため（確認: 2026-10-17、根拠: 同じ実行の `modelUsage` の入力トークン 1172 に対し、transcript は 2）。
- ACP アダプタ（`@agentclientprotocol/claude-agent-acp` 0.93.0）は、`/usage` を対応コマンドとして返し（セッションの費用、トークンの内訳、プランの利用枠）、`/cost` を非対応にしている。毎ターン `usage_update`（コンテキスト使用量と費用 USD）をクライアントに送る。設定は user・project・local を読む（確認: 2026-10-17、根拠: 配布物の `dist/acp-agent.js` を読んだ）。
- 環境変数 `CLAUDE_CODE_SESSION_ID` は、クラウド環境では設定されていたが、公式の環境変数のページには載っていない（確認: 2026-10-17、根拠: `env` の出力と公式ページの前半）。

## Gotchas
- 状況: transcript を集計して費用を出そうとした
  - 原因: 公式は「transcript の形式は内部用で版ごとに変わる」「Stop の時点で最後の発言が入っていないことがある」と書いている
  - 解決: 集計は `message.id` と `usage` の2項目だけに依存させ、失敗しても作業を止めない（exit 0）作りにした。最新のターンの遅れは次のターンで追いつく

## Open Questions
- Zed 経由で Stop フックが動くか。アダプタが設定を読むのでコード上は動くはずだが、実機では未確認。
- WSL2 の対話モードで入力が同じ形か。
- サブエージェントの分が、メインの transcript に入るか。
- 提案: 応答本文の保存（`2026-10-17-claude-reply-text-capture.md`）と費用の記録を、同じ1つの Stop フックのスクリプトにまとめる（AI の提案。未承認）。

## Next Actions
- Zed の1往復で、記録のファイルが更新されるか確かめる（2026-10-17 時点）。
- 実機の `/usage` の費用と、推定の費用を比べる。
