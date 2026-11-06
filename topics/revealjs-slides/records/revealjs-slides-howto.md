# revealjs スライドの作り方（手順書）

見本から複製して、図解レイアウトの HTML スライドを 1 本作る手順。型の意味・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。部品は同じ `records/`。

## 手順

1. **作業ディレクトリを作る**: 空の一時ディレクトリ（コミットしない。成果物は `ai/out/` など）。
2. **型を選ぶ**: `python -I gen_layouts.py --list` で台帳（番号・名前・使いどころ）を見る。AI は番号と使いどころを理由に提案し、最終判断はユーザー。無い形は近い型で作り、slide に `"want": "欲しい形"` を書く。
3. **spec を書く**: JSON。先頭に `title`、任意で `subtitle` `author` `date`（表紙に出る）。`slides` に 1 枚ずつ `{"title", "type", ...}`。各型の形は `gen_layouts.py` の docstring と、組み込み見本 `SAMPLE`（同ファイル末尾）をコピーして直す。spec は JSON なので、`true`・`false` は小文字（Python 風の `True` は読み込みで止まる）。`split` の `cols` は、左の K を 1/4 にするなら `1fr 3fr`、1/3 なら `1fr 2fr`。
4. **qmd を出し、部品を複製する**:
   `python -I gen_layouts.py --spec spec.json -o <dir>/slides.qmd --copy-assets`
   （`--copy-assets` が scss とアイコン 3 種を `<dir>` へ複製する。完成版は `--no-id` を足してレイアウト番号を消す。）
5. **render**: `quarto render <dir>/slides.qmd`（`embed-resources` なので HTML 1 枚で完結）。
6. **目視**: Edge で全スライドを見る（折り返し、はみ出し、アイコン、左下の出典 1 行）。直すのは spec（qmd は手で直さず作り直す）。

## 図（SVG）を入れる

T の `side.img`（`alt`・`caption` つき）が標準。仕様から SVG を出す例は、Excalidraw 試験の方式 A（`lessons` と `decisions.md` に記録。試験用ディレクトリは削除済み）。実スライド用の汎用 SVG 雛形は無い。必要になったら、題材の図をその都度 SVG で作り、`alt` を必ず付ける。

## 注意

- アイコンの `icon` は接頭辞つき（`myself-pc` `dads-search` `lc-folder`）。`dads-` `lc-` を使うと出典が自動で左下に出る（`"credit": false` で消せる）。
- 日本語フォント（Noto Sans JP）が無い PC では見え方が変わる（Open Questions）。
