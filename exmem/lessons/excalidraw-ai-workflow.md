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
triggers: [excalidraw, .excalidraw, Excalidraw MCP, mcp.excalidraw.com, excalidraw-mcp, create_view, read_me, 手描き風, SVG書き出し, 図解, draw.io, 作図, PNG, フォント, 日本語, font-family, 埋め込み, pptx, --font, --screenshot, headless, 相対パス, 絶対パス, excalidraw_view, --export, side.img, Edge, 書き出し失敗]
created: 2026-11-06
updated: 2026-11-07
sources:
  - Claude Code conversation "Excalidraw を Claude 経由で使う試験"
---

# Excalidraw の図を AI に作らせる手順と MCP の試験結果

## Goal
Claude Code から Excalidraw の図を作り、SVG にしてスライドに入れる方式を決める。MCP を使う方式と、AI が `.excalidraw`（JSON）を直接書く方式を比べた結果と、手順を残す。道具に依存しない原則は [[ai-diagram-generation]]。

## Principles
- Excalidraw の図は、AI が `.excalidraw`（JSON）を直接書く方式を標準にする。理由: 追加の読み込みがなく、座標が確定し、編集用ファイルと SVG が手元に残る。
- 手描き風の見た目が要るときだけ、Excalidraw 本体の書き出しを使う。理由: 自前で描く SVG は手描き風にならない。本体の書き出しの SVG はフォント参照が入るので、埋め込み先で表示を確認する。
- 他の PC や pptx に渡す日本語の図は、SVG でなく PNG にする。理由: SVG は日本語の字を埋め込まず、見る端末のフォントで字形と幅が変わる。
- 図の中のフォントは、使う先の本文フォントに合わせる。理由: HTML スライドは Noto Sans JP に固定できるが、pptx は別のフォントになりうる、図だけ違うと浮く。
- 子プロセス（ブラウザなど）に渡すファイルパスは、呼ぶ側で絶対パスにしてから渡す。理由: 解釈の基準になる場所が呼ばれる側で違うことがあり、保存だけが無言で失敗する。
- 無言で失敗する外部コマンドは、出力の存在確認で失敗を検出し、原因は同じ入力で条件（相対と絶対など）を 1 つずつ変えて切り分ける。出力先の引数がファイルかディレクトリかは、ヘルプとエラー文に明記する。

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
- **pptx・他 PC 向けの図は PNG を標準にする**（2026-11-07）
  - 根拠: ユーザーが「良いです」と承認。書き出した SVG にフォントが埋め込まれていなかった。
  - 却下案: SVG のまま渡す（見る端末のフォントで崩れる）。
- **書き出し時のフォント指定は、SVG の `font-family` 全置換で実装する**（2026-11-07）
  - 根拠: ユーザーが「--export へのフォント指定(svg,png)を実装します」と依頼し、動作確認後に「フォントが出力されました。動作確認完了」と承認した。
  - 却下案: SVG にフォントを埋め込む（日本語フォントは巨大で、Excalidraw の書き出しは日本語の字を埋め込まない）。

## Facts
- `.excalidraw` は JSON で、要素に `id`・`type`・`x`・`y`・`width`・`height`・`strokeColor`・`backgroundColor`・`roundness` などを持たせれば、Excalidraw で開いて崩れない。矢印は `points`（始点からの相対）、文字は `text`・`originalText`・`fontSize`・`fontFamily`・`textAlign` が要る（確認: 2026-11-06、根拠: 27 要素のファイルを生成し、ユーザーが Excalidraw で開いて目視）。
- `fontFamily: 2`（標準の書体）にすると、日本語の文字も崩れず読めた（確認: 2026-11-06、根拠: 同上のユーザーの目視）。
- 公式リモート MCP（`https://mcp.excalidraw.com`）は、Claude Code に HTTP で接続でき、道具は `read_me` と `create_view` の 2 つ。`read_me` の返答は約 9KB で、1 会話に 1 回読む。`create_view` の戻り値は `checkpointId` だけで、画像・`.excalidraw`・SVG は手元に出ない。描画は MCP 対応の画面（claude.ai、デスクトップ）側のビューで、ターミナルでは見えない（確認: 2026-11-06、根拠: 実際に接続して同じ図を描かせた結果）。
- `/context` で見た MCP の常時分は、`create_view` 221、`read_me` 100、計 321 トークン（確認: 2026-11-06、根拠: ユーザーの計測）。道具は遅延読み込みで、名前だけが常時載る。
- MCP は `claude mcp add --scope local` で入れ、`claude mcp remove <名前>` で外せる（確認: 2026-11-06、根拠: ユーザーが外した）。
- 公式の README には、ツール名・数、ファイル保存・書き出しの記載が見当たらなかった。コミュニティの作成系 MCP は 26〜42 ツールで保存と書き出しを持つと一覧に書かれているが、数は一覧ごとに違い、実際には試していない（仮説）。補足: 道具が多いほど常時のツール定義は大きくなると考えられる。

- `fontFamily: 2` の日本語図を書き出した SVG には `@font-face` も埋め込みフォントも無く、`style-fonts` は空で、`font-family="Helvetica, Segoe UI Emoji"` の指定だけだった（確認: 2026-11-07、根拠: 書き出した SVG の中身）。
- 同じ図の PNG は、濁点・小書き・記号・漢字・英数が混在しても崩れなかった（確認: 2026-11-07、根拠: PNG を目視）。日本語の字形は、SVG では見る端末、PNG では書き出す端末のフォントで決まる。
- `excalidraw_view.py` の `--font NAME` は、書き出した SVG の `font-family="…"` をすべて `NAME, sans-serif` に置き換える。PNG は置き換え後の SVG を撮るので、書き出す端末にそのフォントが無いと代替フォントになり、無いときは警告を出す（確認: 2026-11-07、根拠: Windows で Noto Sans JP を指定した SVG の属性値と PNG の目視、存在しない名前での警告。実物: `apply_font` と `font_installed` を確認）。フォント替え後も日本語の図は箱からはみ出さなかった（ユーザーの目視）が、字幅は変わるので替えたときは目視する。
- Windows の Edge の `--screenshot=<相対パス>` は、PNG が保存されなかった。絶対パスでは保存された（確認: 2026-11-07、根拠: 同じ `--export png` を `-o` の相対と絶対で実行して比べた）。`excalidraw_view.py` の `-o` は出力ディレクトリで、`-o ./tmp/a.png` と書くと `a.png` というディレクトリの中に PNG ができる。出力先を `resolve()` する修正で相対パスでも出る（実物: `export_files` の `outdir.resolve()` を確認）。
- 書き出した SVG は、revealjs の `side.img` にパスを書くだけで入る（変換不要）。Quarto の `embed-resources` で `data:image/svg` として HTML に埋め込まれ、HTML 1 枚で完結する（確認: 2026-11-07、根拠: render した HTML を検索）。保存した SVG も PNG も、この PC の PowerPoint に挿入でき、文字に違和感はなかった（ユーザーの発言）。

## Gotchas
- 状況: `excalidraw_view.py x.excalidraw --export png -o ./tmp/x.png` を実行した（修正前）
  - 原因: 出力先が相対パスのまま Edge の `--screenshot` に渡され、保存に失敗した（「PNG を作れませんでした」と出るだけ）
  - 解決: 出力先を絶対パスにしてから渡す（現在は自動）。`-o` にはディレクトリを渡す
- 状況: 欧文のサンプル図の SVG（埋め込みサブセットあり）を Linux 側の Chromium で書き出した
  - 原因: 埋め込まれたフォントのサブセットが「glyf: zero-length table」で読めないと出た。日本語の字はそもそも埋め込まれていない
  - 解決: 日本語の図は、埋め込みに頼らず、書き出す端末に使うフォントを入れる
- 状況: 自前の SVG（`role` と `aria-label` を持つ）を、生成スクリプトのインライン埋め込み（`fig`）に渡す
  - 原因: 生成側が `role="img" aria-label` を自動で足すため、属性が二重になる
  - 解決: 埋め込む前に、SVG の `role` と `aria-label` を正規表現で外し、alt は札（tab）の文言で渡す

## Open Questions
- Excalidraw 本体の書き出しで、手描き風の SVG のフォント埋め込みが、スライド（自己完結の HTML）で崩れずに表示されるか。→ 一部回答: 日本語の字は埋め込まれない（Facts）。HTML スライドで `--font` 指定の SVG が崩れないかは未確認。
- 別の PC の PowerPoint で、pptx に入れた SVG・PNG の字形が崩れないか（未確認）。

## Next Actions
- room（WSL）の Linux 側で `--font` を使い、フォントが当たるか確かめる（2026-11-07 時点。エージェント経由の確認ではなく、ユーザーの通常の環境で）。
- 別の PC と PowerPoint で、SVG と PNG を入れた図のフォントが崩れないか確かめる（2026-11-07 時点）。
- 半幅用の大きい文字の版を作り、実スライドに入れて確かめる（2026-11-06 時点。のち、半幅用の版を作り確認した記録が `topics/revealjs-slides` にある）。

## Related
- [[ai-diagram-generation]]: 道具に依存しない原則。
- [[revealjs-diagram-layout-output]]: スライド側の図解レイアウトの型。
