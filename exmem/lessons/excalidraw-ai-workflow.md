---
type: knowledge
title: Excalidraw の図を AI に作らせる手順と MCP の試験結果
status: active
tags:
  - tool/excalidraw
  - diagram
  - mcp
  - slides
  - ai/claude
aliases:
  - Excalidraw MCP の試験
triggers: [excalidraw, .excalidraw, Excalidraw MCP, mcp.excalidraw.com, excalidraw-mcp, create_view, read_me, 手描き風, SVG書き出し, 図解, draw.io, 作図]
created: 2026-11-06
updated: 2026-11-06
sources:
  - Claude Code conversation "Excalidraw を Claude 経由で使う試験"
---

# Excalidraw の図を AI に作らせる手順と MCP の試験結果

## Goal
Claude Code から Excalidraw の図を作り、SVG にしてスライドに入れる方式を決める。MCP を使う方式と、AI が `.excalidraw`（JSON）を直接書く方式を比べた結果と、手順を残す。道具に依存しない原則は [[ai-diagram-generation]]。

## Principles
- Excalidraw の図は、AI が `.excalidraw`（JSON）を直接書く方式を標準にする。理由: 追加の読み込みがなく、座標が確定し、編集用ファイルと SVG が手元に残る。
- 手描き風の見た目が要るときだけ、Excalidraw 本体の書き出しを使う。理由: 自前で描く SVG は手描き風にならない。本体の書き出しの SVG はフォント参照が入るので、埋め込み先で表示を確認する。

## Decisions
- **MCP なしの方式 A から始め、出力は SVG にする**（2026-11-06）
  - 根拠: MCP の追加トークンが不明なので、追加の常時費用がない方式で型を作り、後から比べる（ユーザーの発言: 「A がいいです」「svg がいいです」）。
  - 却下案: 最初から MCP を入れる（比べる基準が無いまま費用が載る）。
- **公式リモート MCP（方式 B）を試して外す**（2026-11-06）
  - 根拠: 画像・`.excalidraw`・SVG が手元に出ず、成果物に使えない（ユーザーの発言: 「方式 B は画像出力がなく、成果物に使えないので omit しました」）。
  - 却下案: 入れたままにする（成果物が出ず、常時 321 トークンだけが載る）。需要が出たら入れ直す。
- **SVG は画像ファイルとして入れる**（2026-11-06）
  - 根拠: 横長の図でも崩れず読める。インラインは小さい図向き（ユーザーが目視して「ばっちり見えてます」）。
  - 却下案: インライン SVG で埋め込む（横長の図が箱の中で縮み、文字が読めなかった）。

## Facts
- `.excalidraw` は JSON で、要素に `id`・`type`・`x`・`y`・`width`・`height`・`strokeColor`・`backgroundColor`・`roundness` などを持たせれば、Excalidraw で開いて崩れない。矢印は `points`（始点からの相対）、文字は `text`・`originalText`・`fontSize`・`fontFamily`・`textAlign` が要る（確認: 2026-11-06、根拠: 27 要素のファイルを生成し、ユーザーが Excalidraw で開いて目視）。
- `fontFamily: 2`（標準の書体）にすると、日本語の文字も崩れず読めた（確認: 2026-11-06、根拠: 同上のユーザーの目視）。
- 公式リモート MCP（`https://mcp.excalidraw.com`）は、Claude Code に HTTP で接続でき、道具は `read_me` と `create_view` の 2 つ。`read_me` の返答は約 9KB で、1 会話に 1 回読む。`create_view` の戻り値は `checkpointId` だけで、画像・`.excalidraw`・SVG は手元に出ない。描画は MCP 対応の画面（claude.ai、デスクトップ）側のビューで、ターミナルでは見えない（確認: 2026-11-06、根拠: 実際に接続して同じ図を描かせた結果）。
- `/context` で見た MCP の常時分は、`create_view` 221、`read_me` 100、計 321 トークン（確認: 2026-11-06、根拠: ユーザーの計測）。道具は遅延読み込みで、名前だけが常時載る。
- MCP は `claude mcp add --scope local` で入れ、`claude mcp remove <名前>` で外せる（確認: 2026-11-06、根拠: ユーザーが外した）。
- 公式の README には、ツール名・数、ファイル保存・書き出しの記載が見当たらなかった。コミュニティの作成系 MCP は 26〜42 ツールで保存と書き出しを持つと一覧に書かれているが、数は一覧ごとに違い、実際には試していない（仮説）。補足: 道具が多いほど常時のツール定義は大きくなると考えられる。

## Gotchas
- 状況: 自前の SVG（`role` と `aria-label` を持つ）を、生成スクリプトのインライン埋め込み（`fig`）に渡す
  - 原因: 生成側が `role="img" aria-label` を自動で足すため、属性が二重になる
  - 解決: 埋め込む前に、SVG の `role` と `aria-label` を正規表現で外し、alt は札（tab）の文言で渡す

## Open Questions
- Excalidraw 本体の書き出しで、手描き風の SVG のフォント埋め込みが、スライド（自己完結の HTML）で崩れずに表示されるか。

## Next Actions
- 半幅用の大きい文字の版を作り、実スライドに入れて確かめる（2026-11-06 時点。のち、半幅用の版を作り確認した記録が `topics/revealjs-slides` にある）。

## Related
- [[ai-diagram-generation]]: 道具に依存しない原則。
- [[revealjs-diagram-layout-output]]: スライド側の図解レイアウトの型。
