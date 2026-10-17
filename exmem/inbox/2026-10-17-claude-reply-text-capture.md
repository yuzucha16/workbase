---
type: inbox
title: Claude Code の応答本文だけをファイルに残し、画面のファイル操作表示を減らす
tags:
  - ai/claude
  - tool/claude-code
  - hooks
  - transcript
  - output
created: 2026-10-17
sources:
  - Claude Code conversation "Claude の応答本文のローカル保存"
---

# Claude Code の応答本文だけをファイルに残し、画面のファイル操作表示を減らす

## Goal
チャット画面は過去ログが長くなると、ファイル操作の差分に埋もれて報告の本文が読みにくい。応答本文（報告など）だけをテキストで残す方法と、画面側でファイル操作の表示を減らす方法を、公式ドキュメントと実測で確かめたかった。
統合先の候補: lessons/claude-code-storage.md（キーワード: claude-code, transcript, jsonl, hook）。広い候補: 新規トピック（キーワード: stop hook, last_assistant_message, focus, 出力）

## Principles
- 会話の記録を後から取り出す用途には、非公開の内部形式（`.jsonl`）を解析するより、公式が値を渡すフックの入力を使う。理由: 公式が「形式は内部用で版ごとに変わる」と明記しており、解析スクリプトは版が上がると壊れうる。
- 「保存する量」と「画面に出す量」は別の問題として分けて扱う。理由: 保存は Stop フックなど出力に触れない仕組みで足りるが、画面の見づらさは表示設定（`/focus` など）でしか変えられない。

## Decisions
なし

## Facts
- Stop フックの入力に `last_assistant_message`（Claude の最後の応答のテキスト）がある。ツール呼び出しやその結果は入らない（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの Stop の節と、`claude -p` で Stop と MessageDisplay の両フックを動かした実測。途中の一言は Stop に入らず、最後の報告だけが入った）。
- 公式は、`transcript_path` の JSONL は非同期に書かれ、Stop の時点で最後の発言が入っていないことがあるので、直近の応答は `last_assistant_message` から取るよう勧めている（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの共通入力フィールドの節）。
- Stop フックは、ユーザーが中断（Esc）したターンでは動かず、API エラーのときは代わりに StopFailure が動く（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの Stop の節）。
- MessageDisplay フックは、表示される本文を受け取る。対話モードでは行のまとまりごとに何度も呼ばれ、フックが返るまで表示が止まる。実測（`claude -p`）では途中の一言も最後の報告も、どちらも渡された（確認: 2026-10-17、根拠: 公式ドキュメントと上の実測）。
- `/export <ファイル名>` は会話全体を、ツール出力も含めてテキストで書き出す。`/copy` は最後の応答をクリップボードへ送り、ピッカーで `w` を押すとファイルに書ける（確認: 2026-10-17、根拠: 公式 commands と sessions ドキュメント）。
- 画面側: `/focus` は、直前の発言、ツール呼び出しの1行の要約（編集は追加・削除の行数だけ）、最後の応答だけを出す。fullscreen の描画（`/tui fullscreen`、試験提供中）が必要で、`viewMode: "focus"` で固定できる。`Ctrl+O` で全体を見られる（確認: 2026-10-17、根拠: 公式 commands、fullscreen、settings-reference ドキュメント。実機の表示は未確認）。
- `bashEditDiffEnabled: false`（ユーザー設定）または環境変数 `CLAUDE_CODE_BASH_EDIT_DIFF=0` で、Bash の実行後に出る変更ファイルの差分を止められる。止めると PostToolUse の Bash フックにも変更ファイルの一覧が渡らない（確認: 2026-10-17、根拠: 公式 settings-reference と env-vars ドキュメント）。
- Edit ツールの差分を、通常の表示のまま隠す設定は、公式ドキュメントに見つからなかった（確認: 2026-10-17、根拠: settings-reference と interactive-mode ドキュメントを検索）。
- output styles は応答の役割・口調・形式を変えるだけで、ファイルへ書き出す機能は無い（確認: 2026-10-17、根拠: 公式 output-styles ドキュメント）。
- WSL2 の対話モードで、Stop フックの `last_assistant_message` が `claude -p` と同じ内容になる（仮説）。補足: 公式の説明からの推測で、対話モードは試していない。

## Gotchas
- 状況: 最後の応答だけを残すつもりで Stop フックを使う
  - 原因: 長い説明を書いた後にツールを呼び、短い一言で終わると、その一言しか `last_assistant_message` に入らない。途中で書いた本文は残らない
  - 解決: 途中の本文も残したいなら MessageDisplay フックを使う（ただし途中の一言も全部入り、表示が止まる分の遅延が出る）。または、長い報告は最後の応答にまとめるよう指示する

## Open Questions
- 提案: 応答本文の保存は Stop フックで日付ごとの Markdown に追記する（AI の提案。未承認）。
- 提案: 画面の見づらさは、まず `/focus` を試す（AI の提案。未承認）。
- `/focus` で、直前のターンより前の過去ログがどう見えるか。
- 保存先を、AI 作業部屋の中では `ai/records/` の下、部屋の外ではリポジトリの外にする案で足りるか。

## Next Actions
- 提案した Stop フックを、実際の環境で動かして確かめる（2026-10-17 時点）。
- `/focus` を試して、見え方を確かめる（2026-10-17 時点）。
