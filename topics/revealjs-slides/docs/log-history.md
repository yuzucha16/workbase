# 経緯（log-history）

## Log

### 2026-11-06 トピックを作成し、PC1 の写真から書き起こす
- PC1 の room stock の内容（ノート 3 枚、`layouts.qmd` 8 枚）が写真で `exmem/inbox/` に来た（フォルダ 2 つ、約 5MB × 11）。
- 写真を読んで、ノートは `records/2026-11-05-revealjs-diagram-layout-note.md`、CSS は `records/revealjs-diagram-theme.scss`、見本は `records/revealjs-diagram-layouts.qmd` に書き起こした（見本の繰り返しは生成スクリプトで作った）。
- Windows の Quarto 1.11.9 で render し、Edge ヘッドレスで撮った 6 枚を目視。崩れなし。
- 命名の意見: 型は `*-output`（`exmem/lessons/` の流儀）。部品（見本・CSS）は lessons に入れず、トピックの `records/` に置く案。
- 写真フォルダの削除は、自動判定で拒否された。ユーザーに依頼。
- 統合（11-06）: ノートを `exmem/lessons/revealjs-diagram-layout-output.md` に統合（新規）。タグ 4 つ（tool/quarto、tool/revealjs、slides、diagram）を `tags.md` に追加。書き起こしノートは削除。写真フォルダはユーザーが削除。
- room での確認（11-06）: `room-myenv` に見本を `/tmp` で render（Quarto 1.11.9、Chromium 1248、マウントなし）。7 枚、同じ見え方。部屋の Chromium は `--no-sandbox` `--disable-dev-shm-usage` が要る。シェル変数は `wsl -- bash -c '...'` の中で展開されず、スクリプトを base64 で渡して実行した。アイコン定義を `include-before-body` に出す案を Windows で試験し、通った。push は `fcd1e93` まで（別セッションの `fc51744` は除く）。

### 2026-11-06 wrap（push、room での確認、優先順位）
- `fcd1e93` を push。`e893d5c` は下に別セッションの大きなコミット（`fc51744`、37 ファイル）が乗っていたので、一時 worktree で `origin/main` に cherry-pick して push した（`fc51744` は push していない）。
- 優先は改善案 1・2。PC1 では Python の生成スクリプトを内部で叩いていた（取り込みは未）。pptx のレイアウト例の使い回しを Next Actions に足した（ユーザーが pptx を渡す）。
- 作業を 11-06 にここで切った。次は `revealjs-slides の続き`。

### 2026-11-06 NA3 pptx の棚卸しと、生成スクリプト、アイコン分離、型 H・I・J
- ユーザーが `slide_layout.pptx`（33 枚、16:9、ダミー文言）を渡した。展開し、PowerPoint の COM で PNG にして全枚を目視、`records/2026-11-06-pptx-layout-inventory.md` に分類を書いた。全枚が同じレイアウトで、図形はスライド上に直接ある。濃紺中心、フォントは BIZ UDPゴシック。
- ユーザーの承認: H・I・J の 3 型を足す。順は生成スクリプトが先。ポイントは「行・列を増やせる」と「余白をそろえる」（`decisions.md` の同日の項）。
- NA（アイコン定義の別ファイル）済: `records/revealjs-diagram-icons.html`。15 枚でも空スライドなし。
- NA（生成スクリプト）済（PC1 との見比べは残り）: `records/gen_layouts.py`（A〜G、H・I・J）。見本 `revealjs-diagram-layouts.qmd` はスクリプトの出力に置換。
- CSS は `revealjs-diagram-theme.scss` に H・I・J を追加。直した点: 高さと文字を大きくして下を埋める、表の既定の線を消して行間を白にする、見本のタイトルを短くする。
- lessons（`revealjs-diagram-layout-output.md`）の Decisions、Facts、Gotchas、Open Questions を更新（9 型、部品の置き場、アイコン分離を採用済みに）。
- 環境の注意: PowerShell の二重引用符の中のバッククォートは、`` `t `` がタブになるなど文字を壊す。Markdown の編集は Edit を使う。`Remove-Item` のワイルドカード（`$dir\*`）はブロックされるので、ディレクトリごと消して作り直す。
- ユーザーの発言: 実スライドの題材はあるが、PC1 で作りたい。room で H・I・J を見たい。

### 2026-11-06 NA5 Noto Sans JP・インデント・行間の目視と、基本形の確定
- ユーザーが Windows で目視: Noto Sans JP で表示された。直した点: ①見出しより箇条書きの行頭記号が左に出ていた（`--ind` が em で、見出しの大きい文字に引きずられた）→ px の固定値 40px、箇条書きは 2.5 段。②タイトルの下の空きを 0.5em → 0.8em。③文字サイズを下げる依頼に、`$presentation-font-size-main` を 32px にしたが効かず（実際は 40px のまま）、H の 5 行がはみ出した。Edge の headless 撮影で確かめ、`$presentation-font-size-root: 28px` に直して効いた。
- H・I・J の高さ `--h` を em から 560px にした。H と J は 3 行までにした（ユーザー: 構造化は 3 要素以上で再分割するので、実用は 3 程度が上限）。
- 型 T に段落（`"p"`）を足し、文章・文字列・箇条書きのサンプルを足した。画像の粗さはユーザーの拡大画面のためで、SVG は粗くならない（未修正）。
- ユーザー: 「読めます。これで fix」「一旦これで OK」。見本を基本形にして `records/` をコミット（`44799e1`）。

### 2026-11-06 NA1 room init の Noto Sans JP 段の準備
- `notosansjp` 段が `room.py` の `INIT_STEPS` にあることを確認し、`init` 関連の単体テスト 17 件（2 件スキップ）が通ることを確かめた。実機の確認（`room init <Area> --resume` か `--only notosansjp`、`fc-list` で確認）は、ユーザーが別セッション・別 PC で行う。NA1 は未完了のまま `log.md` に残した。
