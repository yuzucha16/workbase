---
type: logbook
title: Marp・Slidev・Quarto の実機比較（部屋で pptx を出す）
created: 2026-11-06
updated: 2026-11-06
review_by: 2027-01-05
budget: 8KB
---

# Marp・Slidev・Quarto の実機比較（2026-11-04）

使う側の決定は `office-output-types` の決定（Quarto を主、Marp 既定を副。Slidev は入れない）。版が変わると古くなる実測なので、`logbook/` に置く。

## いま

- 編集できる pptx を出せるのは Quarto だけ（文字・表・ノートが本物）。Marp 既定と Slidev の pptx はスライドが画像（見た目のみ、ノートは入る）。Marp の `--pptx-editable` は実験的で、表・ノート・日本語の字形に問題がある。
- pptx が成果物なら、Slidev の強み（段階表示・Vue の部品・ライブ）は pptx で消える。Slidev を選ぶのは、HTML で発表するのが主のときだけ。
- 「お手軽に画像の pptx」なら Marp 既定（導入が軽く、組み込みテーマで見た目が整う）。「初版を AI が作り、人が微修正」なら Quarto（見た目は `reference-doc` 次第）。
- 未確認: Marp・Slidev のテーマを替えたときの差。Quarto の `reference-doc` を替えたときの差。

## 明細（2026-11-04）

部屋（WSL。Quarto・Chromium・LibreOffice 入り）で、同じ内容（日本語の箇条書き・表・発表者ノート）から pptx を出した。Marp CLI 4.5.1、Slidev CLI 53.0.0、Quarto は部屋の版。導入は root（`/usr/local` は `ai` が書けないため。`npm i -g` を root で）。

| 項目 | Quarto | Marp（既定） | Marp（`--pptx-editable`） | Slidev |
|---|---|---|---|---|
| 出力 | 約 1.7 秒。4 枚 | 約 2 秒。3 枚 | 約 2.5 秒。3 枚 | 約 5.4 秒。3 枚（初回の依存の事前ビルド込み） |
| 編集 | 可 | 不可（画像） | 文字は可 | 不可（画像） |
| 日本語 | 正常 | 画像なので見た目のみ | 「⽐」「⽇」など康熙部首の互換文字に化ける | 画像なので見た目のみ |
| 表 | 本物の表（`a:tbl`） | 画像 | 壊れる（空白区切りの文字に） | 画像 |
| ノート | 入る | 入る | 失われる | 入る |
| Mermaid | 画像で入る（部屋の mmdc） | 未確認 | 未確認 | 未確認 |

### 動かすための注意

- Marp が部屋で動くには `--browser-path /usr/local/bin/room-chrome`（`--no-sandbox` を付ける薄い包み）。Marp は標準入力を読むので、スクリプトからは `</dev/null` を付ける。
- Slidev に要った準備（root）: ①`@slidev/theme-default@0.25.0` と `playwright-chromium`（1.64.1。ブラウザのリビジョン 1248 が部屋と一致）を作業フォルダに入れる、②Vite のキャッシュ用に `@slidev/cli/node_modules/.vite` を `ai` が書ける形で作る（無いと `EACCES` で 33 秒で時間切れ）。実行時は `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright`。導入の手間は Marp より大きい。

### 見た目・表現幅（PNG で見比べた。Marp は `gaia`、Slidev は既定テーマ）

| 観点 | Marp | Slidev |
|---|---|---|
| 既定の見た目 | 組み込みテーマ（3 種）で最初から整う | 白地に黒でほぼ装飾なし |
| 表 | 内容の幅に縮み、左に寄る | 全幅で罫線が細く読みやすい |
| コード | 背景色つきで見やすい | 薄い灰色の枠。構文の色つき |
| 段組み | CSS・HTML を書けば可 | `layout: two-cols` が標準（上寄せで余白が大きい） |
| Mermaid | 単体では描けない（画像を貼る） | 標準で描ける（日本語も正常） |
| pptx に残るもの | 見た目のみ | 見た目のみ。段階表示・動く部品は消える |

注意: 入力は小さい見本で、Slidev は既定テーマだけ。実際の資料量・他のテーマでは差が変わりうる。

### Quarto の pptx の見た目（LibreOffice で PDF にして見た）

- 部屋の `soffice --headless --convert-to pdf` は動いた（最初に出力が出なかったのは、初回のプロファイル作成か時間切れとみられる。原因は未特定）。部屋に `pdftoppm` が無いので、PDF はホストへ取り出し、`uv run --with pymupdf` で PNG にした。
- 既定テンプレートは素の Office 風（白地・黒字、タイトル中央、表は青の見出し行と縞）。日本語は正常。弱い点: インライン `コード` の装飾が消える。図のスライドはタイトルと図の位置が揃わない（LibreOffice での表示）。
- 初版としては読める。整えるなら `reference-doc` で社内テンプレートを当てる。
