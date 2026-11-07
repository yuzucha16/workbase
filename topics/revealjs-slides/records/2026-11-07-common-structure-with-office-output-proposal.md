# revealjs と pptx の共通構成の案（2026-11-07。案のみ。コードは変えていない）

対象: `topics/revealjs-slides`（Quarto → revealjs。`gen_layouts.py`）と `topics/office-output-types`（Quarto → pptx。`reference-doc` の 7 段手順）。決定 `decisions.md`（DADS 取り込み ②）の「pptx 側と共通にできる構成は revealjs 専用の CSS と分けて持つ」を具体にする。

## 見立て: 共通にできるもの / できないもの

| 層 | 内容 | revealjs | pptx | 共通化 |
|---|---|---|---|---|
| 1 内容の spec | 表紙（title/subtitle/author/date）、スライド（title、本文の段落・箇条書き（2 段まで）、表、画像（alt・caption）、コード、`lead`/`notes`、発表者ノート） | `gen_layouts.py` の JSON | Quarto の markdown | **する**（最小の共通部分） |
| 2 型の台帳 | 番号・名前・使いどころ（`LAYOUTS`） | 15 型 | Pandoc の 7 レイアウト名 + `layout=` | **対応表だけ**共通（下） |
| 3 トークン | 色（濃青 `#0017c1`、罫線 `#949494`、本文 `#1a1a1a`）、見出しの規則、日本語フォント | scss | 雛形のテーマ（BIZ UDPGothic） | **値を 1 か所**に置き、両方へ写す |
| 4 文章の規則 | 箇条書き 2 段まで、1 スライド 1 主張、lead は結論、notes は補足、出典の書き方 | docstring・lessons | 同じ | **する**（文書にするだけ） |
| 5 進め方 | spec → 生成 → render → 目視 → spec を直す。作り直し前提（成果物は手で直さない） | 手順書 | 7 段手順 | **する**（骨格が同じ） |
| 6 見た目の実装 | 格子・シェブロン・アイコン・K ツリー | CSS + HTML | 不可（Pandoc は HTML を出せない） | しない |

要点: pptx は Pandoc の制約で、図解型（A〜K のうち格子・シェブロン・アイコン）を直接は出せない。共通の経路は **図は SVG（alt・caption つき）にして画像として入れる**（T の `side.img` と同じ。Excalidraw 試験の方式 A）。

## 型の対応（案。pptx の Pandoc レイアウト名）

| revealjs | pptx | 備考 |
|---|---|---|
| 表紙 | Title Slide | 共通 |
| C 目次 | Section Header（章扉） | 目次の一覧は Title and Content |
| T | Title and Content | `side` が画像なら Content with Caption |
| A | Comparison / Two Content | 左右が対等ならこちら |
| J 表 | Title and Content（markdown の表） | 強調列・罫線は雛形のテーブルスタイル次第（差の一覧 (c)） |
| H・I・B・D・E・F・G・K・S | 画像（SVG）を Title and Content に | 図を別に作る。pptx で編集できない |
| L・N | Title and Content（定義リスト・引用） | 近似 |
| split | Two Content | 3 部品は不可 |

## 案（段階。A から順に。B 以降は需要が出てから）

- **A（推奨・今すぐ）: 文書だけ分ける。** 新しい 1 ファイル（`records/` か `guides/`）に、層 3・4 の「値と規則」だけを書く（トークン表、文章の規則、型の対応表）。コードは変えない。revealjs は scss、pptx は雛形の作り方がこの表を参照する。
- **B: トークンを JSON 1 つにし、scss の変数と pptx テーマの色を生成する。** 値の二重管理が実際に食い違ってから。
- **C: spec を renderer 非依存にし、`gen_layouts.py` を「spec → revealjs」と「spec → pptx 用 markdown」に分ける。** pptx 用 markdown の生成は、office-output-types の 7 段手順の 4（全要素の試験）が通った後。P2（split 3 部品）と同様、需要待ち。

置き場の候補: (1) revealjs-slides の `records/` のまま（今は唯一の実装。移動が要らない）、(2) 新トピック（共通が 2 実装を超えて育ったとき）、(3) `guides/`（規則だけなら）。推奨は (1) で、C に進む時点で (2) を再検討。

## 確認が要る点

- 層 4 の文章の規則は、pptx（正式な資料）でも同じでよいか。DADS はカジュアルな簡易スライド前提で取り込んだ（decisions 30〜31）。フォーマルは別の型にする、が元の方針。
- pptx 側の図は SVG 画像でよいか（編集不可）。編集が必要な図は、別の経路（PowerPoint で描く）か。
