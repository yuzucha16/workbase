# draw 複数パターン試験（NA2、2026-11-07）

room `room-myenv`（Project `myinv-draw-na2`、ダミー）で、`workflow-kit/draw-hook.md` の手順を 4 パターン通した。図は 3 段の流れ（日本語の箱 3 つ + 矢印 + 注記）。生成は Python の簡易ヘルパ（箱と文字を別要素で書く）。

| パターン | プロファイル | 結果 |
|---|---|---|
| 理解用・文のみ | `--font` なし、PNG | OK。目視で崩れなし（直し 0 回） |
| slide・文のみ | `Noto Sans JP`、SVG | OK。SVG の `font-family` が `Noto Sans JP, sans-serif` に変わる。`@font-face` は埋め込まれない（想定どおり） |
| pptx・文のみ | `BIZ UDPゴシック`、PNG | OK。部屋にフォントが無く、警告が出て代替字形（想定どおり）。字形は他 2 つとほぼ同じに見えた |
| キャプチャあり | `Noto Sans JP` | OK。`image` 要素 + `files` の dataURL で、SVG・PNG とも書き出せた（手順書に追記した） |

付随の確認: `-o` が相対パスでも出る。`-o x.png` はディレクトリ `x.png/` ができる（仕様どおり。手順書に既記）。無い入力は「見つかりません」で止まる。

## フィードバック（直す候補）

1. `room start --no-launch` は、標準入力が閉じている環境（エージェントの非対話シェル）では `input()` の EOF で落ちる（`room.py` 1863 行）。マウントは外れる。回避は、開いたままの標準入力を渡すこと（`Start-Sleep 3500 | uv run room.py start … --no-launch`）。ただし、その場合の後始末は `room umount --area <Area>` で足りるはずが、「マウントは残っていない」と出て、`start` プロセスの終わり方は確認できなかった。非対話で部屋を使う正式な入口（例: `--no-launch` を標準入力が TTY でないときは Enter 待ちせず sleep する）は未決。
2. Windows 側から `wsl -d <部屋> -- bash -c '… $? …'` を書くと、`$?` などが wsl 側で先に展開される（`false; echo $?` が 0 になる）。終了コードを見るときは、スクリプトファイルにして `bash <file>` で走らせる。
3. PowerShell のヒアストリングを `wsl … -- bash` の標準入力に渡すと CRLF で構文エラーになる（`-replace "`r"` でも直らない）。LF のスクリプトを、プロジェクトの `ai/work/` に Write で置いて、部屋の `/mnt/room/<名>/work/` から `bash` で実行するのが確実。
4. `wsl` の呼び出しごとに `wsl: Failed to translate '<Windows のパス>'` の警告が出る（雑音。無害）。
5. 部屋のスクリプトの置き場は `~/shared/workflow-kit/tools/excalidraw-viewer/` で正しく入っていた（`room start` のコピーに入る）。`python3 -I … --help` も通る。部屋は Python 3.14.4、Node 24。
6. Project の実体は `works/projects/<名>/`（`areas/<Area>/projects/` ではない）。手で `ai/work/parts/` を作るときに取り違えやすい。

## あふれ試験（必須分。実施済み）

箱の幅 150 に 12〜14 字（fontSize 20）を入れた図を書き出した。PNG で、文字が箱の外へはみ出し、隣の箱の文字と矢印に重なるのが一目で分かった（検出できる）。箱の幅を 330 に直して 1 回で解消（直し 1 回）。

- 気づき: 直し方が「箱を広げる」だけだと、3 箱で幅が約 1060 になり、半幅（700 前後）の用途に収まらない。手順書の直し方に「幅を広げられないときは、`\n` で行を折る・箱を縦に積む・fontSize を下げる（20 未満は半幅では避ける）」を足すとよい（案。未反映）。
- 幅の見積もり（全角 1 字 ≒ fontSize、左右 + 16 以上）は、今回の値（14 字 × 20 + 16 = 296 → 330）で足りた。

## 未実施

- T の `side.img` に入れて render するところまでは見ていない（3 段の図が約 680 幅で半幅に収まることだけ確認）。
- サブエージェントは不要（ユーザー判断 11-07）。
