# draw フック（別名「作図」）

呼び出し名は draw。別名は「作図」。呼び出し表の正本は `hooks.md`。ユーザーが言ったときだけ実行する（自発的には実行しない）。

## 目的と契機

- **目的**: 説明・キャプチャ・用途から、Excalidraw の図（`.excalidraw`）を AI が書き、SVG・PNG に書き出して目視で直し、置き場に置く。作図の手順（書く → 書き出す → 見る → 直す）を固定する。
- **契機**: ユーザーが「作図」または `draw` と言ったとき。合言葉の後ろの文を「説明」に当てる。
- **前提**: 部屋で動く。書き出しスクリプトが使える（次の「手順」の「道具を確かめる」）。使えないときは、記憶で代用せず、ユーザーに伝えて止まる。

## 場所と書き込みの制約

- 起動できる領域は `hooks.md` の「領域とフックの権限」に従う。
- 書くのは、Project の `ai/work/parts/<日付>-diagram-<題>/` の中だけ（部屋では `/mnt/room/<名>/work/parts/…`。`room-context.md` の「ai/X は /mnt/room/<名>/X」）（置き場の決定は直下 `docs/decisions.md` の 2026-11-07）。`<日付>` は `YYYY-MM-DD`、`<題>` は英小文字・数字・`-`。
- 残す図は、成果物の中（`ai/out/<成果物名>/`）へ人が移す。AI は `ai/out/` に書かない。

## 入力

次の 3 つ。足りない欄は、1 回の質問にまとめて聞く（図の中身を聞き返さず、用途だけは必ず決める）。

1. **説明**: 何を図にするか（文、箇条書き、構成。キャプチャや既存の図があれば、そのパス）。
2. **用途**: 理解用 / slide / pptx のどれか。
3. **題**: 置き場の名前に使う短い語（無ければ AI が決める）。

## 手順

1. **プロファイルを決める**: 用途で、フォントと残す形式を決める。

   | 用途 | `--font` | 渡す形式 | 理由 |
   |---|---|---|---|
   | 理解用 | 指定しない | PNG | 自分が読むだけ。フォントは問わない |
   | slide（revealjs） | `Noto Sans JP` | SVG（T の `side.img`） | 本文が Noto Sans JP に固定でき、HTML で SVG が崩れない |
   | pptx | `BIZ UDPゴシック` | PNG | SVG は日本語の字を埋め込まず、見る端末で崩れる。PNG は書き出す端末のフォントで決まる |

   値は想定（2026-11-07）。pptx の本文フォントが違うときは、そのフォントに合わせる。

2. **道具を確かめる**: 書き出しスクリプトは固定の場所にある。workbase では `workflow-kit/tools/excalidraw-viewer/excalidraw_view.py`、部屋では `~/shared/workflow-kit/tools/excalidraw-viewer/excalidraw_view.py`（`~/shared/workflow-kit/` の写しに入る。2026-11-07 に `topics/revealjs-slides/` から移した）。探し回らない。無ければ記憶で代用せず止まる。ユーザーが別の場所（`tmp\excalidraw-viewer` など）を指定したときは、その指定を優先する。Windows 形式の相対パスは部屋では読み替える（`tmp\X` → `/tmp/X`。`C:\...` は部屋から見えないので、見つからなければユーザーに聞く）。スクリプトは同じディレクトリの `build_viewer.mjs` などに依存するので、複製するときはディレクトリごと。`python3 -I <スクリプト> --help` が通ること。`--font` のフォント（Noto Sans JP など）が部屋に入っているか `fc-list` で見る。無ければ警告が出るだけで書き出しは通るが、PNG の字形は代替になる。
3. **`.excalidraw` を書く**: `parts/<日付>-diagram-<題>/diagram-<題>.excalidraw` に JSON を書く（箱と文字が多いときは Python の生成スクリプトで出してよい。再編集に要るなら同じディレクトリに `gen-<題>.py` で残し、要らなければ `/tmp` に置いて残さない。残したかどうかは用途のメモに書く）。
   - 先頭は `{"type":"excalidraw","version":2,"elements":[...],"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}`。
   - 要素は `rectangle` `ellipse` `arrow` `text`。共通の欄（`id` `x` `y` `width` `height` `angle` `strokeColor` `backgroundColor` `fillStyle` `strokeWidth` `roughness` `opacity` `seed` `version` `versionNonce` `isDeleted` `groupIds` `boundElements` `updated` `link` `locked`）を省かない。見本は `topics/revealjs-slides/excalidraw-viewer/samples/sample-jp-font.excalidraw`。
   - 文字は `text` と `originalText` を同じにし、`fontSize` `fontFamily: 2` `textAlign` `verticalAlign` `containerId: null` `lineHeight: 1.25` を付ける。箱の中の文字は、箱とは別の `text` 要素として箱の上に置く: 中央揃えは `textAlign: center` で、文字の `x` = 箱の `x`、`width` = 箱の `width`。複数行の高さは 行数 × `fontSize` × 1.25、`y` = 箱の `y` + (箱の高さ − その高さ) / 2。矢印は `points`（始点からの相対）を持つ。
   - 幅の見積もり: 全角 1 字 ≒ `fontSize`、半角 1 字 ≒ `fontSize` の 0.55 倍。箱の幅は文字の幅 + 左右 16 以上。日本語の図は `roughness: 0` を既定にする（手描き風は、ユーザーが求めたときだけ）。
   - 半幅（slide の `side`）に入れる図は、横幅 700 前後、文字 20px 以上にする。
4. **書き出す**: `python3 -I <スクリプト> <.excalidraw> --export svg,png -o <同じディレクトリの絶対パス> [--font "<名前>"]`。`-o` はディレクトリ（ファイルを渡すと、その名前のディレクトリができる）。結果が空になることがあるが、スクリプトが 6 回までやり直す。それでも PNG が出なければ、出力を添えて止まる。
5. **目視して直す**: PNG を Read で開いて見る。見る点は、文字が箱からはみ出していない、文字が重なっていない、矢印が箱に繋がっている、読む順が左から右・上から下、用途の幅に収まっている。直す点があれば、手順「`.excalidraw` を書く」に戻って直し、書き出す。**直すのは最大 2 回**。2 回で直らなければ、残った点を報告に挙げて止める（無限に直さない）。フォントを替えたときは字幅が変わるので、替えた後の PNG で見る。
6. **用途のメモを書く**: 同じディレクトリに `diagram-<題>.md` を置く。1 行目に用途、次にプロファイル（`--font`）、使う先（例: T の `side.img`）、元の説明、直した回数、生成スクリプトを残したか。
7. **報告する**: 次の「報告の型」。

## 報告の型

共通の項目（`hook-common.md` の「報告の型」の節だけ読む。コミット、次にやること、固有の項目、ユーザーに求めることの順）を報告する。このフックでの追記:

- **コミット**: 部屋の git へのコミットは `wrap` で行う。このフックはコミットしないので「なし」と書く。
- **次にやること**: 図を使う先（slide の `side.img`、pptx）。直らない点があれば、その修正。
- **ユーザーに求めること**: 図の確認（PNG のパス）。残す図を `ai/out/<成果物名>/` へ移す判断。

固有の項目（「次にやること」の後、「ユーザーに求めること」の前）:

1. **置いた物**: ディレクトリと、できたファイル（`.excalidraw` `.svg` `.png` `.md`）。
2. **プロファイル**: 用途、`--font`、渡す形式とその理由。
3. **目視の結果**: 見た点と、直した回数（0〜2）。直らなかった点があれば、それ。フォントが部屋に無かったときも、ここに書く。
