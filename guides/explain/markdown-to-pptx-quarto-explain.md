---
type: explain
title: Markdown から pptx を作る道具（Quarto 主・Marp 副）の比較と、AI 活用への組み込み方（理解ガイド）
tags:
  - tool/chromium
  - tool/libreoffice
  - workflow
checked: 2026-11-04
triggers: [Marp, Quarto, Pandoc, Slidev, markdown to pptx, スライド, パワポ, pptx 生成, 資料化, プレゼン資料, reference-doc, Markdown スライド]
---

# Markdown から pptx を作る道具（Quarto 主・Marp 副）の比較と、AI 活用への組み込み方

Markdown を pptx にする道具を比べ、なぜ Quarto を主、Marp を副にしたかを、自分で説明できるところまで理解するための文書。調査日は 2026-11-04。

> **状態: 調査のみ。どの道具も実機では未試験。** 公式ページで確認したことは [公式]、ブログなどの二次情報は [二次]、筆者の見立ては【推測】と書く。

## 1. 3行で表すと

- Marp と Slidev の通常の pptx は、スライドを画像にしたもの。PowerPoint では編集できない。
- Quarto（Pandoc）は、最初から編集できる pptx を作る。既存の `.pptx` / `.potx` を雛形（`reference-doc`）にでき、後で組織の雛形に合わせる道筋がある。
- 画像の pptx は直すたびに AI を通すことになる。編集できる pptx なら、人が PowerPoint で直して終われる（手離れがよい）。

## 2. 決めたこと（2026-11-04、ユーザー）

| 項目 | 決定 | 理由 |
|---|---|---|
| 主 | Quarto（Pandoc） | 編集できる pptx。後で組織の雛形に合わせたい。画像だと毎回 AI を通すことになるので、手離れをよくしたい |
| 副 | Marp | 最も簡単。比較のために試す |
| 雛形への合わせ込み | 最初はしない。後で合わせる | 先に流れを通す |

## 3. 比較

| ツール | pptx の出力 | 長所 | 短所 |
|---|---|---|---|
| Quarto / Pandoc | 最初から編集できる | `reference-doc` で雛形を使える。レイアウトは内容から自動で選ばれる。発表者ノート対応 [公式] | 初期の雛形は地味。背景画像は stretch のみ。共通の背景は雛形のレイアウトに置く [公式] |
| Marp CLI | 通常は画像のみ。`--pptx-editable` は実験的 [公式] | 書式が単純で AI が書きやすい [二次] | 編集版は LibreOffice が必要。複雑なテーマはエラーや不完全な出力。発表者ノート非対応。見た目を保ちたいなら非推奨と公式が書いている [公式] |
| Slidev | 通常は画像。`pptx-editable` は図形に再構築 [公式] | コードの強調表示、Vue コンポーネント | `playwright-chromium` が必要。SVG・数式・動画・グラデーションは画像のまま。フォントは埋め込まれず、折り返しが変わる [公式] |
| reveal.js | 標準の pptx 出力なし [二次] | 自由度が高い HTML | pptx が最終形の用途に合わない |
| python-pptx / PptxGenJS | 編集できる pptx を直接作る | 雛形を使え、制御が細かい | コードを書く。python-pptx にはアニメーションと画面切替の API がない [二次] |

「Slidev は pptx を出せない」というブログの記述は、公式の `pptx-editable` の説明と食い違う。古い情報と見る。

## 4. Quarto で何が起きるか

1. 見出し `##` が1枚のスライド、`#` がセクションの表紙になる（`slide-level` で変更できる）[公式]。
2. 内容から雛形のレイアウトが自動で選ばれる。2列は Two Content、本文のあとに画像や表が続くと Comparison か Content with Caption、それ以外は Title and Content [公式]。
3. 雛形に要るレイアウトは Title Slide、Title and Content、Section Header、Two Content、Comparison、Content with Caption、Blank の7つ。足りないと警告が出て、既定の雛形のものが使われる [公式]。
4. 雛形の作り方: `quarto pandoc` で既定の pptx を出し、PowerPoint で編集する [公式]。

## 5. 図（mermaid）の扱い

- pptx では mermaid は PNG になる。作るときに Chrome か Edge を使う [公式]。
- Chrome が無いときは `quarto install chrome-headless-shell` で入れられる [公式]。
- 部屋には Playwright の Chromium が入っている（`ai-room-convert-tools-explain`）。Quarto がそれを見つけるかは **要確認**（見つからないときは、Quarto 側で入れる）。
- 図は PNG なので、pptx の中では画像のまま。図の直しは Markdown に戻る。

## 6. AI 活用への組み込み（案）【推測】

| 段 | 担当 | 内容 |
|---|---|---|
| 1 | AI | 元の資料から Markdown の下書きを作る（`##` 区切り、1枚1メッセージ、文章を載せない） |
| 2 | 人 | Markdown を直す。観点と意味の判断 |
| 3 | スクリプト | `quarto render x.md --to pptx` で pptx にする（決定的。AI を通さない） |
| 4 | 人 | 細かい見た目は PowerPoint で直して終わり（以後は pptx が正） |

- 手離れの要点は 3 と 4。AI が関わるのは 1 だけにする。
- 4 で直した後は pptx が正になる。Markdown に戻さない（二重管理を避ける。`office-ai-workspace` の却下案と同じ）。

## 7. 副（Marp）で確かめること

- 通常の pptx（画像）が、組織の用途で足りるか。足りるなら最も手間が少ない。
- `--pptx-editable` が、日本語と mermaid で使えるか。
- 同じ Markdown を Quarto と Marp に通し、直す手間を比べる。

## 8. 要確認事項

- Quarto の部屋への入れ方（deb か tarball か）と版。公式の取得ページから版を読み取れなかった。
- Quarto が、部屋の Chromium を見つけるか。
- 日本語フォントと mermaid の日本語が、pptx で崩れないか。
- 雛形に合わせるとき、どこまでを雛形側のレイアウトにできるか（共通背景、ロゴ、フォント）。
- Marp CLI の最新版と、`--pptx-editable` の現在の安定度。
- 第三者による、編集できる pptx の品質比較は見つからなかった。

## 9. 出典

一次（公式）:
1. [marp-team/marp-cli](https://github.com/marp-team/marp-cli)（2026-11-04 取得）
2. [Slidev: Exporting](https://sli.dev/guide/exporting)（2026-11-04 取得）
3. [Quarto: PowerPoint](https://quarto.org/docs/presentations/powerpoint.html)（2026-11-04 取得）
4. [Quarto: Diagrams](https://quarto.org/docs/authoring/diagrams.html)（2026-11-04 取得）

二次:
5. [Deckary: Marp Alternatives](https://deckary.com/blog/marp-alternatives)
6. [Dasroot: Marp, Slidev, reveal.js](https://dasroot.net/posts/2026/04/markdown-presentation-tools-marp-slidev-reveal-js/)
7. [Open Design: Marp](https://opendesigner.io/blog/marp)
8. [marp2pptx（PyPI）](https://pypi.org/project/marp2pptx/0.1.5/)
9. [freeCodeCamp: Claude Code + Marp](https://www.freecodecamp.org/news/how-to-use-claude-code-and-marp-to-think-through-presentations/)
10. [Termdock: terminal presentations](https://www.termdock.com/en/blog/terminal-presentations-markdown-to-slides)
11. [Smithery: document-pptx skill](https://smithery.ai/skills/vasilyu1983/document-pptx)

関連: [[ai-room-convert-tools-explain]]、[[office-ai-workspace]]。
