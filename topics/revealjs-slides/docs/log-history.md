# 経緯（log-history）

## Log

### 2026-11-06 Excalidraw の方式 B（公式リモート MCP）を試して外した（NA1 を閉じた）
- 根拠: `records/excalidraw-trial/README.md` の「方式 B の結果」。同じ room 図を `read_me` 1 回 + `create_view` 1 回で描けたが、戻り値は `checkpointId` のみで、画像・`.excalidraw`・SVG は手元に出ない。revealjs には使えない。
- 数字: `/context` で `create_view` 221、`read_me` 100 の計 321 トークン（ユーザーの計測）。`read_me` の返答は約 9KB（呼んだときだけ）。
- 決定: ユーザーが外すと決め、`claude mcp remove excalidraw` を実行した（`claude mcp list` で消えたことを確認）。`decisions.md` に記録。
- 残り: 応答数・トークンの `requests_by_kind.py` での比較は取らなかった（外すと決めたため不要）。

### 2026-11-06 Excalidraw を Claude 経由で使う試験を始めた（方式 A: MCP なし）
- ユーザーの指示: 「excalidraw を claude 経由で操作したい。最終的にはスライドに挿入したり図解の道具にする。MCP 周りの追加トークンが分からないのでお試しで。revealjs とは別々に使いこなし、draw.io のような別の道具にもナレッジを使えるようにしたい」。選択は A（MCP なし）から、次に B（公式リモート MCP）、出力は SVG。お題は room の構造図（Windows と WSL の関係、マウント）。
- 調べたこと: 公式 `excalidraw/excalidraw-mcp` はリモート `https://mcp.excalidraw.com` を勧め、チャット内の描画（MCP Apps）向け。ツール名・数、ファイル保存・書き出しの記載は README に無かった。コミュニティの作成系は 26〜42 ツールで `.excalidraw` 保存と SVG・PNG 書き出しがある（数は一覧ごとに違い、未確認）。
- 反映: `records/excalidraw-trial/`（`build_room_diagram.py`、`room-structure.excalidraw`・`.svg`、`build_slide.py`、`README.md`）。
- 確認: `.excalidraw` は Excalidraw で開いて崩れない（ユーザー）。SVG は Edge で描画して、はみ出しを直した（箱の幅 360 → 300、注記の分割）。revealjs では、T の `side.img` が良好（ユーザー確認）、E の `fig`（インライン）は縮んで読めない。
- 未確認: Excalidraw 本体からの書き出し（手描き風 SVG とフォント埋め込み）、方式 B のトークン。

### 2026-11-06 Devicon の開発系アイコン 49 種をストックした（未組み込み）
- ユーザーの指示: 「Lucide と同じく、Devicon（言語寄りのアイコン）もストックしたい。ソフトウェア開発系を選択・抽出して」。見本を見て「使わなそうなものがあるので半分くらい落としてよい。判断は任せる。Web・クラウド・ビルドは上位 2〜3 割を残す」「使ったものだけ（埋め込み）でよい」「line 版は外して」。
- 素材: devicons/devicon（MIT。Copyright (c) 2015 konpa）、コミット 32fe1d3 の `icons/<名前>/<名前>-plain.svg`（空の一時ディレクトリへ取得。`git` の外）。塗りの色を捨てて `currentColor` に統一（形は変えていない）。`original` は多色で単色にすると崩れ、`line` は線が細く薄いので使わない。
- 反映: `records/build_devicon_icons.py`（図形以外の要素・属性があれば止まる。`GROUPS` に名前を足して作り直す）、`revealjs-diagram-icons-devicon.html`（49 種、72KB、id は `i-dv-<名前>`、viewBox 128 角）、`…-devicon-preview.html`、`devicon-LICENSE.txt`。93 種で作って Edge で目視し、薄い `line` の 7 種を外して絞った。
- 確認: Edge（headless）で一覧を目視（93 種の版）。絞った後の 49 種の一覧は目視していない（同じスクリプトの出力）。`gen_layouts.py` には未組み込み。
- 新規: 組み込みの NA と、出典の自動表記への Devicon の追加（期日 11-13）。

### 2026-11-06 ディレクトリ構造の型 K を追加し、Lucide のアイコン 99 種をストックした
- ユーザーの指示: 「スライド作成ではディレクトリ構造を頻繁に使う（フォルダ・ファイルのアイコンとテキストの図）。出力の型に入れてほしい。Lucide はライセンス次第で活用したい。ディレクトリ構造に限らず、ソフトウェア開発系のアイコンをストックしたい」。見本を見て「ばっちり。行間は広く感じたが一旦これでやってみる」「フォルダは青でよい」「出典は入れる」「ディレクトリ構造は 1/3〜1/4 の幅で使う予定」。
- ライセンス: Lucide は ISC（改変・再配布・商用可。条件は著作権表示と許諾文の同梱）。Feather 由来の一部は MIT（同じ LICENSE に記載）。`lucide-LICENSE.txt` に素材の LICENSE を置いた。
- 反映: `records/build_lucide_icons.py`（SVG の外枠を除き、線の属性を `<g>` に移して symbol 化。図形以外の要素・属性があれば止まる）、`revealjs-diagram-icons-lucide.html`（99 種、id は `i-lc-<名前>`）、`…-lucide-preview.html`（区分つきの一覧）、`gen_layouts.py`（型 K・`tree_rows`・`tree_slide`、`include-before-body` に 3 つ目、台帳と見本）、`revealjs-diagram-theme.scss`（`.tree-box`・`.tr`）。
- 確認: Lucide の LICENSE と 1.70.0 の SVG を GitHub から取得（空のディレクトリ。`git` の外）。Windows の Quarto で render し、Edge で K と見本全体（26 枚目）を目視。
- 一部済ではなく新規: 出典の自動表記（Lucide を含める）と K の 1/3〜1/4 幅を NA に起票した（期日 11-13）。
### 2026-11-06 デジタル庁のアイコン素材（line 版）から 32 種を足した
- ユーザーの指示: 「アイコンの種類を増やしたい。デジタル庁のアイコン素材（商用可の zip）から今のレイアウトに合うものを抽出して使えるように。サイズは 1 つでよい」「見えないとわからないのでプレビューがほしい」「このアイコンで始めてみます」。
- 素材: zip は SVG 120（塗り・線の 60 種）と PNG 360（3 サイズ）。24px の SVG の線版を採用（札の絵柄が線中心のため）。色 `#1A1A1C` を `currentColor` に置換し、clip-path を除いた。出典は html の先頭コメント（利用規約 1-2。加工して公開するときは出典と加工内容を明示）。
- 反映: `records/build_dads_icons.py`（素材から作り直す・プレビューだけ作り直す）、`revealjs-diagram-icons-dads.html`、`revealjs-diagram-icons-preview.html`（ブラウザで開く一覧。自作 9 + 素材 32）、`gen_layouts.py`（`include-before-body` を 2 ファイルの列に）、lessons のアイコンの項。Edge で一覧を目視済み。
- 注意: 単体の icons html は `width=0` の隠し SVG なので、開いても真っ白で正常（仕様）。

### 2026-11-06 DADS の table/usage・card/usage を取得し、表のセルを上揃えにした（NA 1 を閉じた）
- ユーザーの指示: 「table/usage, card/usage を取得するところがゴール」。取得後、表のセルの縦位置の変更を「変えます」と採用。Edge で H・J を目視し「ばっちり。上揃えの方がみやすいかもしれない」「これで NA1 も close」。
- 取得: 両ページとも数値（罫線の太さ・余白）は無く、規則だけ。表: 見出し下は黒のボーダー・太字、セルは上揃え・左揃え（数値は右も可）、結合は最小限、縞・ホバーは 3:1 以上。カード: 最大 4 パーツ、コンテナは外周と背景必須で外周 3:1 以上（影だけは不可）、クリッカブルなエリアにリンク・ボタンを置かない。ノートの「テーブル」「カード」の節に反映した。
- 反映: `revealjs-diagram-theme.scss`（`.tb th/td` を `vertical-align: top`、`.mx .h/.rl` を `align-items: flex-start`、`.mx .c` を `justify-content: flex-start`。`.mx.chev .h` だけ `align-items: center`）、`revealjs-diagram-layouts.html`（再生成）、lessons の状態。探索は subagent に任せず自分で取得した。
- 済: NA 1（DADS 準拠の残り）。完了条件の「未取得ページの取得」が満たされ、`due.md` の 11-13 の行も消した。
### 2026-11-06 DADS コンポーネント 3 件を型にした（S ステップナビゲーション・L 説明リスト・N 注釈ブロック。スイッチは不採用）
- ユーザーの指示: 「ステップナビゲーション・説明リスト・スイッチ・注釈ブロックも dads 準拠で使えるように」。見本を見て「スイッチは使えないか。omit してください。他の 3 つは採用」「既存レイアウトに組み込む形で、拡充の幅を広げる位置づけ」。
- 反映: `gen_layouts.py`（型 S・L・N、`body()` に登録。`split` の部品にも使える。台帳 `LAYOUTS` と見本スライドを追加）、`revealjs-diagram-theme.scss`、`revealjs-diagram-layouts.qmd`・`.html`（再生成）、lessons の DADS 節（ステップナビ・説明リスト・注釈ブロックの状態、スイッチは不採用）。
- 確認: DADS の 4 ページ（概要）を取得。数値・マークアップの記載は無く、サイズは自前（丸 32px、線 2px、3:1 以上）。Edge で見本を目視（横・縦の手順、説明リスト 2 種、注釈 3 パターン、split(S+N)）。スイッチ（型 W）は試作後に撤去した。
- 一部済: NA 1 は未取得ページ（`table/usage`・`card/usage` など）の取得だけに縮めた。
### 2026-11-06 DADS 準拠の残り 3 件を反映（`ol` 止め・SVG の aria-label・画像キャプション。NA 1 件を一部済み）
- ユーザーの指示: 「3 つのアイテムやります。推奨とともに情報ください。特に害がなければ dads に寄せます」。見本を見て「キャプションばっちりです」。
- 反映: `gen_layouts.py`（`no_ol`: T の `items`・`p` の行頭 `1.` で生成を止める。図の SVG に `role="img"` と `aria-label`〔箱の `alt`、無ければ `tab`、無ければ `aria-hidden`〕。`side` の `caption` で `figure` + `figcaption`）、`revealjs-diagram-theme.scss`（`.tright figcaption` 0.6em・行高 1.5）、`revealjs-diagram-layouts.qmd`（再生成）、lessons の状態の記述。
- 確認: `1.` で停止、`caption` で `figure` が出ることを確認。Edge で `caption-sample` を目視し、ユーザーが確定。`caption` なしの見た目は未目視。
- 一部済: NA は未取得ページ（`table/usage`・`card/usage` など）の取得だけに縮めた。
### 2026-11-06 DADS 準拠の差を解消（罫線・余白・行高・字間・alt。NA 1 件を一部済み）
- ユーザーの指示: 罫線 2.1:1 と 3:1 の違いを聞き、見本（`#b3b3b3` / `#949494` / `#767676` を表・目次で並べた）を見て案 2（`#949494`）を採用。続けて余白・行高・字間の見本を見て「全部採用。字間は広げた方が見やすい」。
- 反映: `revealjs-diagram-theme.scss`（罫線 5 か所、`.cell` の余白 px、`.txt` の行高 1.5、字間 2%・h2/h3 1%・コード 0）、`gen_layouts.py`（`side` 画像の `alt` 必須。組み込みの見本の生成は通る）、lessons の状態の記述。格子・表の角丸 4px は SCSS に無く、記述が誤りだった。
- 確認: gap-sample を render できた。画面の目視はユーザー（見本）。実スライドでの再 render は未。
- 一部済: NA は残り（`ol` 化の扱い、SVG の代替テキスト、キャプション）に縮めた。
- 落とし穴: 縦の余白 12px は 4 の倍数で 8 の倍数ではない（8px にすると詰まる）。
### 2026-11-06 型の棚卸し NA から完了済みの 2 点を外す
- ユーザーの指示: 「行高 1.5・字間は実スライドで試す」以降（C の見た目の見直しを含む）は完了しているので削除。NA の文から外した（根拠: ユーザーの発言）。

### 2026-11-06 型の棚卸し P3 の実装（NA 1 件を一部済み）
- 経緯: `LAYOUTS` の値を「名前, 使いどころ」の組にし、12 型すべてに使いどころの 1 行を書いた（ユーザーが文言を確認、OK）。`--list` で番号・名前・使いどころを出せる。AI は提案のとき番号と理由を一緒に言う。確認: `--list` の出力と、組み込みの見本の生成が通ること。render は未実施（出力の qmd は変わらない）。根拠: `records/gen_layouts.py`（`LAYOUTS`、`--list`）。
- 一部済: 「型の棚卸しの実装」は P3 が済み、P2（需要待ち）と共通化の検討が残り。

### 2026-11-06 型の棚卸し P1 の実装（NA 1 件を一部済み）
- 経緯: A〜G の箱の型を 1 つの `box_slide` にし、並びを `PRESETS`（grid-template-areas）にした。新しい並びは `PRESETS` に 1 行足すだけで作れる。scss の型ごとの grid 規則を外した。つまずき: areas 名を二重引用符で囲むと、Pandoc の div 属性の解析が壊れて B が崩れた（単一引用符で解決）。確認: 変更前後の見本 A・B・D・E・F・G を Edge の headless で並べて目視し、同一（違いは進捗バーのみ）。`height` 指定の描画は未確認。根拠: `records/gen_layouts.py`（`PRESETS`、`box_slide`）、`records/revealjs-diagram-theme.scss`。
- 一部済: 「型の棚卸しの実装」は P1 が済み、P3（次のセッション）と P2（需要待ち）が残り。

### 2026-11-06 型の棚卸しの整理とレイアウト番号の表示（NA 1 件を omit、1 件を一部済み）
- 経緯: pptx の残り（階段・3 要素）は、ユーザーが「H・I で足りる」として omit。型の棚卸しは、重なり・管理・拡充の観点で 12 個を整理し、案 P1〜P3 を出した（実装は別セッション）。ユーザーの決定で、型は AI が提案・ユーザーが最終判断とし、スライドの右上にレイアウト番号（`H+notes` など）を出す。無い形は `want` に書いて逐次作る。`gen_layouts.py` の docstring の誤った `\n` も直した。確認: Edge の headless で G と split の 2 枚。根拠: `records/gen_layouts.py`（`LAYOUTS`、`layout_id`）、`records/2026-11-06-layout-inventory.md`、`decisions.md`。
- close した NA: 「pptx レイアウトの残り（階段・3 要素の判断、ほかの pptx の棚卸し）」（omit）。一部済: 「型の棚卸し」は整理と番号表示が済み、P1〜P3 の実装が残り。

### 2026-11-06 目次の型 C を作る（NA 1 件を close）
- 経緯: DADS に「目次」コンポーネントがあることをサイトで確認した（web ページ内ナビ。点線の箱 + 入れ子の箇条書き。見出し「このページの目次」を消さない、見出し文言をそのまま使う）。スライド向けに、罫線だけの番号付き一覧（番号・章名・ひとこと・小項目、`current` で表示中の章を薄青の地）として型 C にした。Edge の headless で 2 枚を目視。根拠: `records/gen_layouts.py`（`toc_slide`）、`records/revealjs-diagram-theme.scss`（`.toc`）、`decisions.md`。
- close した NA: 「目次の型（DADS の見本確認 → 型化）」。見た目はユーザーが確定（11-06）。

### 2026-11-06 土台更新（見出し・T の軽量化、T の右側、split）と NA 2 件の close

- 経緯: 見出し・T の軽量化（h2 1.5em、h3 1.1em、本文 0.9em・行高 1.5）、h3 のインデント修正（軽量化の margin 指定が左余白を消していた）、T と箇条書きの開始位置を揃える、箇条書き 2 段まで、h2 の先頭に濃青の縦棒（6px）。T の `side`（右にコード・画像）、全型の `lead`/`notes`（実装は既存）、`split`（2 型を左右に）を追加した。
- 原因と対処: 見出しで始まる `:::` の div を Pandoc が `<section>` にし、reveal の縦スライドになって後続が見えなくなった。先頭に空の印（`NOSEC`）を置いて防いだ。Quarto のコードブロックは行番号の位置ずれで左が欠けたため、素の `<pre>` にした。確認: Edge の headless のスクリーンショットで、T 右コードと split の 2 枚。根拠: `records/gen_layouts.py`、`records/revealjs-diagram-theme.scss`、`decisions.md`。
- close した NA: 「新しい部屋で room init を 1 回通し Noto Sans JP が入ることを確かめる」（実機で通した。ユーザーが完了と確認、11-06）。「土台の更新の残り」のうち見出し・T の軽量化（済）。
### 2026-11-06 NA 3 件を close
- ユーザー報告: 新しい部屋で `room init`（または `--only notosansjp`）を通し、問題なし。PC1 の生成スクリプトは workbase のものを取り込み済み。H・I・J は Windows の Edge 以外でも問題なし。3 件とも close（`log.md` の Next Actions と `due.md` から外した）。

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

### 2026-11-06 NA2 実スライドを 1 本作る（PC2。題材: room 導入の LT）
- 済（根拠: `records/ai-room-lt/` に spec.json・qmd・html。13 枚を Edge の headless 撮影で全枚目視、はみ出しなし。ユーザー「本件は完了」）。題材は `guides/explain/ai-room-why.md` と `guides/howto/ai-room-setup.md`。部署 30 名・20 分の想定。PC1 でなく PC2 で作った。
- 使った型: A・B・E・F・H・I・J・T（D・G は未使用）。E の図は手書き SVG。
- 出た不足と対処（コミット `29da2df`）: ①A〜G の下が空く → spec の `"height"`（`--lh`）を追加。②図が無い箱の文字が小さい → 0.9em。③型 T を型に登録（10 型）。④I 型のセルにリストを渡すと改行が箇条書きになる（改行は文字列の `\n`）。
- 未対応の不足: 実スライド用の SVG 雛形、表紙のサブタイトル・日付、render 用に scss・icons を複製する手間（`--copy-assets` 案）、使い方の手順書、アイコンが 9 種のみ。kit へのフィードバックはユーザーが行う。
- 成果物（html 3.5MB を含む）はユーザーの指示で一時扱い（コミットしない）。

### 2026-11-06 DADS 取り込みの相談（論点と進め方の立案）
- ユーザーの依頼: 素案 v1 に、デジタル庁デザインシステム（DADS。`https://design.digital.go.jp/dads/`）を言語化・取捨選択して取り込み、10 型を作り直したい。型の問題は「目線が迷う・文字が少ない・使い分けが分かりにくい」（`records/ai-room-lt` は情報量が少ない）。
- 相談の型で論点 8 つ（取り込みの範囲と単位、型と土台の順序、既存の確定との衝突、文章・視線の規則、アイコン、ライセンスと公開、置き場）を一覧にし、進め方を 5 段（一次情報の取得 → 取捨選択表 → 土台の更新 → 型の再設計 → 昇格）に決めた。着手はこのセッションではせず、立案まで。
- 用途はカジュアルな簡易スライドのまま。フォーマルは pptx の別の型。markdown → {revealjs, pptx} の経路は共通なので、共通にできる構成は revealjs 専用の CSS と分けて持つ。
- 仮決めを `decisions.md` に、Next Actions 3 件を `log.md` と `due.md` に起票した。DADS の一次情報は未取得（リポジトリ内に DADS の記述は 0 件だった）。

### 2026-11-06 DADS の一次情報の取得、取捨選択表、見本、5 点の採用
- 手順 1（一次情報）: 利用条件を先に確認（本体はコピーライトポリシーと出典表示、Figma は CC BY 4.0、コードは MIT。加工して自サイトに使う分は帰属不要）。基本デザインの文字・余白・レイアウト・色・アイコンを要約した。公式の色ページは画像のみで 16 進が読めず、配布元のデザイントークン（MIT。`tokens-simple.css`）から Blue 13 段・solid-gray 14 段の値を取った。要約は `records/2026-11-06-dads-summary.md`。「文章」の節は DADS に見当たらない。探索は subagent に任せず自分で取得した。
- 取捨選択表: `records/2026-11-06-dads-selection-table.md`。v1 の色のコントラスト比を計算し、灰色の枠 `#9aa5b1` が 2.33:1（非文字の 3:1 未満）、箱のクラス名 `red` が実際は濃灰、と分かった。
- 見本: `records/build_dads_sample.py` が v1 の SCSS を色（`PALETTE`）と余白（`SPACING`）で置換し、v1.html と dads.html を並べて render する（微修正は値を直して再実行）。Edge で H の 1 枚を目視、崩れなし。出力 `records/dads-sample/` は未コミット。
- ユーザーが 5 点とも採用（`decisions.md`）。「色だけでも雰囲気が変わり、よくなっている」。表の背景・罫線は気になる点で、次回の別セッションで直す。
- 落とし穴: PowerShell の二重引用符の文字列で、バッククォート + r が復帰文字になり、`log.md` の `records/` の語が壊れた（単一引用符の here-string か Write を使う）。

### 2026-11-06 NA 土台の更新: DADS の反映、表・工程・箱を「罫線だけ」に、lead と notes
- DADS 5 点を `revealjs-diagram-theme.scss`・`gen_layouts.py`・見本 qmd に反映した（色、余白 8px、箱のクラス名 `red`→`dark`・`green`→`blue`、リンク色・選択色を濃青）。`ai-room-lt` は途中まで揃えたが、以後は追わない（ユーザー: v1・`ai-room-lt` にこだわらない）。
- 表の見た目: 参考画像（DADS 流の表）を受け、H・I・J を背景なし・罫線だけにした（見出しの下は黒の太線、行は灰の細線、強調列は薄青の地と太字、行ラベルは太字）。J の spec に `emphasize` `rowhead` を追加。I の列見出しはシェブロンのまま薄青の帯（強調だけ濃青）。
- 行の高さは内容なりを既定にした。`height` を指定したときだけ `--h` で下まで等分する（実際の資料は表の上か下にまとめ・総評が入るため。ユーザー）。いったん `--h` 未指定でも 1fr のままで、最も高い行に揃って間延びした。行トラックを `auto` にして解決。
- `lead`（上のひとこと・箇条書き）と `notes`（下のまとめ・総評）を全型に足した。p10 の下に 2 点、p12 の上に 2 点の例。位置は固定でなく、AI が内容で選ぶ位置づけ（ユーザー）。
- 箱 A〜G: 白地・2px の細枠、見出しの札は塗りをやめて色文字（青の箱だけ薄青の地）。
- 落とし穴: 「p10」は画面の表示ページ（`#/9`、1 始まり）。`#/n` は 0 始まりなので、スクリーンショットの番号が 1 ずれる。
- 描画の確認は Edge ヘッドレスで H・I・J・B の数枚。T と見出しの軽量化は未。

### 2026-11-06 DADS v2.18.2 の章立てで lessons の設定ルールを整理
- ユーザーの依頼: `-output`（`exmem/lessons/revealjs-diagram-layout-output.md`）に DADS v2.18.2 を反映し、以後の版・項目追加に追従できる章立て（基本デザイン: カラー・タイポグラフィ・余白、コンポーネント: 箇条書きリスト・画像・見出し）に合わせる。合わないものは DADS の表現で章を足す。
- 版はサイトで確認（v2.18.2、デザインデータ公開 2026-10-21）。ノートに節「DADS 準拠の設定ルール」を新設し、各項を「DADS／現行／状態（〇△×─）」で記述。追加章: レイアウト、アイコン、テーブル、ステップナビゲーション、目次、カード、角の形状・エレベーション。ユーザーが章立てを確認（「イメージと一致」）。関係するページ（table、step-navigation、toc、card、corner-shapes、elevation）を取得して反映した。箇条書き・画像・見出しの `usage` は見出しのみ取得、画像の usage は 404。探索は subagent に任せず自分で取得した。
- 見つかった差（NA に起票、別セッション）: 罫線 `#b3b3b3` が白に 約 2.1:1、箱の em 余白、格子の角丸 4px、箱の行高 1.4、字間 0、Markdown `1.` が `ol` になる、alt・キャプション未実装。SCSS の先頭に版のコメントを追加。
- 古い「下部と右側に余白を作らない」のルールに「置き換わった」と注記。
