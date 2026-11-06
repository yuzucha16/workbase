# Excalidraw 試験(方式 A: MCP なし)

2026-11-06 開始。目的: Claude 経由で Excalidraw の図を作り、revealjs に入れる型を作る。MCP の追加トークンは別に測る(方式 B)。将来は draw.io など別の道具にも同じ型を使う。

## 方式と決定(ユーザー 11-06)

- A(MCP なし)から始め、次に B(公式リモート `https://mcp.excalidraw.com`)を試す。出力は SVG。
- お題は room の構造図(Windows と WSL の関係、マウント)。

## 中身

- `build_room_diagram.py`: 仕様(`SPEC`)から `.excalidraw` と SVG を出す。SVG は自前の描画(Excalidraw の書き出しではない。手描き風にならない)。
- `build_slide.py`: SVG を revealjs に入れて render する(`gen_layouts.py` を使う。出力は一時ディレクトリ)。
- `room-structure.excalidraw`: Excalidraw で開いて崩れないことを確認済み(ユーザー 11-06)。
- `room-structure.svg`: 出力。

## 確認結果(Edge、11-06)

- 画像として入れる(T の `side.img` + alt + caption): 問題なし。これを標準にする。
- インライン SVG(E の `fig`): 不向き。E の箱が右下に小さく寄り、図が縮んで文字が読めない(980x520 の横長のため)。E の `fig` は 760x330 ほどの小さい図向き。
- 半幅に置くと図の文字(18〜24px)が小さい。スライド用には文字を大きくした版(幅 680 ほど)が要る。

## 次

1. 半幅用に文字を大きくした版を `SPEC` から作れるようにする(`W`・文字サイズの倍率)。
2. 方式 B の MCP を `claude mcp add --scope local` で入れ、`/context` の差と、同じ図を描かせたときの応答数・トークンを A と比べる。
3. 道具に依存しない図解の型と、Excalidraw 固有の手順を分けてナレッジ化する(draw.io 用に差し替えられる形)。
