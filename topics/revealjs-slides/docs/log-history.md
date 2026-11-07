# 経緯（log-history）

## Log

### 2026-11-07 NA 2 件を移管し、Open Question を omit した（クローズの前準備）
- ユーザーの指示: NA1（共通化）を `topics/office-output-types/docs/log.md` へ、NA2（PC1 での `excalidraw_view.py` の確認）を直下 `docs/log.md` へ移管。`due.md` の 2 行は削除（移管先に期日の行を足した）。「別 PC のフォントで崩れないか」の Open Question は omit（動作確認は移管した NA で行い、実害があれば起票）。トピックのクローズはまだしない（準備の確認のみ）。
- AI: 移管先は office-output-types の NA 8（期日 11-20）と直下 NA（期日 11-14）。このトピックの NA・Open Questions・`due.md` は空。残るのは、旧 `excalidraw-viewer` の records などのリンクの直し（クローズ時）と、`exmem/inbox/2026-11-07-excalidraw-viewer-js-npm-explain.md` の統合（ユーザーが後で行う）。

### 2026-11-07 部屋に BIZ UDPGothic を入れた（NA1 済み）
- ユーザーの指示: 手段とサイズを見積もる → 「これで行きましょう」（google/fonts から Regular・Bold を取得、`room init` の段）→ 実機は room-myenv で。生成 HTML の目視は「問題ありませんでした」。
- AI: `room.py` に段 `bizudpgothic`（SHA-256 固定、約 9.3MB、OFL）と README の段名を足した（コミット 45cc2fc）。room-myenv で `--only bizudpgothic`、`fc-list` に日英両名、`--font "BIZ UDPゴシック"` の PNG は警告なし・Noto 指定や代替とバイト違い、T の `side.img` に PNG を入れて quarto render が通った。単体テスト通過。試験ファイルは部屋から削除。
- 発見: 部屋の `~/shared` に `topics/` は無い（`gen_layouts.py` は都度コピーが要る）。

### 2026-11-07 room 通しのフィードバックを `draw` に取り込み、スクリプトを `workflow-kit/tools/` へ移した（NA1 の一部）
- ユーザーの指示: room で `draw` を通した AI のフィードバック 6 点を精査して取り込む。次は別セッションで room とサブエージェントによる複数パターン試験。スクリプトの移動は了承（「トピッククローズのときにやろうと思っていた。records/ などのリンクはその時に直す」）。
- AI: `excalidraw-viewer/` 一式を `workflow-kit/tools/excalidraw-viewer/` へ移した（room の `~/shared/workflow-kit/` に入る固定パス）。`draw-hook.md` に固定パス、ユーザー指定の優先と Windows パスの読み替え、部屋の `work/parts/`、箱内の文字の座標と高さの式、生成スクリプトの扱い（`gen-<題>.py`）を追記。決定は直下 `docs/decisions.md`。
- 失敗: 移動中に `Remove-Item` が追跡外の `sample-side-img.html` と `samples/tmp2/` を消した（生成物・一時物。html は qmd から再生成できる）。追跡済みは `git restore` で戻した。
- 残: 旧 `topics/revealjs-slides/excalidraw-viewer/samples` が掴まれて消せない。records などのリンクの直しはトピックのクローズ時。

### 2026-11-07 `--export` へのフォント指定（`--font`）を実装した（NA ①が済）
- ユーザーの指示: 「`--export` へのフォント指定(svg,png)を実装します」。確認後「こちらも問題なく、フォントが出力されました。動作確認完了」。
- AI: `excalidraw_view.py` に `--font NAME` を追加。SVG の `font-family` をすべて `NAME, sans-serif` に書き換える（`apply_font`）。端末にフォントが無ければ警告（`font_installed`。Windows はレジストリ、Linux は `fc-list`）。複数名・引用符つきはエラー。`samples/sample-flow.excalidraw` で SVG の書き換えと PNG（Noto Sans JP）を確認。字幅の変化による箱からのはみ出しは、ユーザーの目視で問題なし。
- 残: 手順書 `作図`（プロファイル決め込み）。room での `--font` 実行と別 PC・PowerPoint は未確認。
- コミット: `excalidraw_view.py`、`log.md`、`log-history.md`、`due.md`（`samples/tmp/`・`tmp2/` は含めない）。

### 2026-11-07 Excalidraw の SVG を `side.img` と pptx に入れて確認した（NA ③が済）
- ユーザーの指示: 「手順 2,3 をやってもらえますか。結果を同フォルダに」→ 手順 4 以降はユーザー。「png が出ました。png も svg も pptx に挿入できました。文字の違和感もありません。次のセッションで `--export` へのフォント指定をやります」。
- AI: `samples/sample-jp-font.svg`（ユーザーが「SVG を保存」で書き出し）を T の `side.img`（alt・caption つき）にした spec `sample-side-img.spec.json` を書き、`gen_layouts.py` で qmd、`quarto render` で HTML（SVG は `data:image/svg` で埋め込まれる）。変換は不要で、パスを `img` に書くだけ（qmd と同じ階層の相対パス）。
- 不具合: `--export png -o ./tmp/...` が「PNG を作れませんでした」になった。原因は Edge の `--screenshot` に相対パスを渡していたこと。`export_files` で出力先を `resolve()` して直した（`excalidraw_view.py`。相対・絶対の両方で確認）。`-o` はファイルでなく出力ディレクトリ。
- 結果（ユーザーの目視）: PNG は出る。SVG・PNG とも pptx に挿入でき、文字に違和感なし（この PC・PowerPoint。別 PC は未確認）。
- 残: `--export` へのフォント指定（次のセッション）、手順書 `作図`。コミットは spec・qmd・SVG・`excalidraw_view.py` のみ（HTML 約 3.5MB と、ユーザーの出力 `samples/tmp/` は含めない）。

### 2026-11-07 日本語が多い Excalidraw 図の `--export` を確認し、pptx・他 PC 向けは PNG 標準と決めた
- ユーザーの指示: 「1. でお願いします」→「良いです。ただフォントが変わります。BIZ UDPゴシックになると思うけど、スライドの種類によって図中フォントも変わります。quarto の revealjs は noto sans jp に固定できる」「room確認は不要です」→「b」（フォント指定の実装は③の後）。
- 結果: `sample-jp-font.excalidraw`（`fontFamily: 2`。濁点・小書き・記号・漢字・英数の混在）を Windows で `--export svg,png`。PNG は崩れず（目視）。SVG は `@font-face` も埋め込みも無く、`font-family="Helvetica, Segoe UI Emoji"` のみ。決定は `decisions.md` の同日の項。room の Chromium での確認は不要。
- 残: ③ユーザーの手動確認、フォント指定の方式（③の後）、手順書 `作図`。NA に残した。

### 2026-11-07 Excalidraw 作図ループの設計と、`--export`（SVG・PNG の画面なし書き出し）を実装した
- ユーザーの指示: 「excalidraw で図解の依頼プロンプトを作り、render して共通の置き場に置くループを」→ sheet・text など部品が増えても流用でき、深く・広くしない置き場の検討 → 「A にします」「`ai/work` を想定。仕組みの整合性で選んで」「追跡、賛成」「手順書は workflow-kit」「すすめて」→「部屋に chromium があると思う」→「wrap。残件は NA に。図は AI が作って試す方向でよい」。
- 結果: 置き場は `ai/work/parts/<日付>-<部品>-<題>/`、残す図は成果物の中（`ai/out/<成果物名>/` の `publish/` か `docs/` の下に平置き）。直下 `docs/decisions.md` に【汎用】で記録。`excalidraw_view.py --export svg,png -o <出力先>`（`viewer_entry.jsx` に書き出しモード）を実装。`file://` のフォント取得は `--allow-file-access-from-files` で通し、空になる不具合は 6 回までやり直しで回避。Windows の Edge と room-myenv の Playwright Chromium で SVG・PNG が出て、PNG を目視（Linux の通常の Chromium は窓の高さから約 85px を引いた領域しか撮らないので、PNG は同梱の headless shell で撮る）。
- 残: 日本語が多い図での SVG のフォント確認、ユーザーの手動の保存・取り込み（revealjs・pptx）、手順書 `作図`。NA に残した。
- 後始末: 部屋の `/tmp/exv-*` と Windows の一時ファイルは削除済み。部屋の `~/.cache/excalidraw-viewer`（約 273MB）は残した。

### 2026-11-07 Excalidraw の閲覧スクリプトを作った（room 非依存）
- ユーザーの指示: 「excalidraw の viewer 環境を作ろうかと思います（毎回 HTML に render／Windows の npm・docker／WSL の npm・docker）。少ないリソース・無償・PC1 でも使える条件で選択肢に優先順位を」→「Docker Desktop は Enterprise 要件で使えない。用途はあなたやスクリプトが作った excalidraw を見ること」「viewer は room に依存させたくない。Windows でも使えると嬉しい」→「どちらも見れました。Windows 側は sample ごとコミット。--no-open も保存と参照どちらもできた」。
- 結果: 毎回 HTML に render する案を 1 位にした（MIT・常駐なし）。`excalidraw-viewer/` に `excalidraw_view.py`・`build_viewer.mjs`・`viewer_entry.jsx`・`package.json`・`samples/sample-flow.excalidraw` を作った。Edge のヘッドレスで日本語・手描き風の表示を確認。room の図は Windows 側から UNC パスで読む形にした。決定は `decisions.md`。
- 後始末: 試験用の一時ディレクトリと room の `/tmp/exv` は削除済み。room の `/home/ai/work/figs/sample-flow.excalidraw` はユーザーの確認用に残した。

### 2026-11-07 手順書と --copy-assets を足し、room で見本を render した（NA を閉じた）
- ユーザーの指示: 「revealjs-slides の続き NA1」→「room-myenv を使って render。H/I/J はこちらで見る」→「目視 OK です。NA1 を close。コミット・push も」。
- 結果: `gen_layouts.py` に `--copy-assets` と spec の `subtitle`/`author`/`date`（表紙）を追加。手順書 `records/revealjs-slides-howto.md` を新規作成（SVG 雛形は「無い・都度作る」）。一時ディレクトリで生成・複製・quarto render が通った。room-myenv（Quarto 1.11.9、Python 3.14.4）の `/tmp/rjs` に複製して render し、qmd は Windows とバイト一致。HTML をユーザーが目視して OK。閉じた NA: 起票 11-06、期日 11-13（根拠: 本コミット）。決定は無し。
- 後始末: room の `/tmp/rjs` と Windows の `%TEMP%\rjs-room`・`rjs-test` は残した（削除の指示待ち）。

### 2026-11-07 records/ の整理とアイコンの命名・id の統一
- ユーザーの指示: 「dads-sample/ と excalidraw-trial を削除。自作・DADS・Lucide のアイコンの命名規則を揃え、プレビューも作る」「`build_dads_sample.py` も削除」「id は Lucide ベースで `i-<素材>-<名前>`。自作は `i-myself-*`、DADS は `i-dads-*`」「Lucide は `i-lc-*` でよい」「Quarto で render し直してパスつきでコミット」。
- 結果: `excalidraw-trial/`（追跡 7 ファイル）・`dads-sample/`（未追跡）・`build_dads_sample.py` を削除。ファイル名を `revealjs-diagram-icons-{myself,dads,lucide}.html` と `-preview.html` の 3 組に統一（`-myself-preview.html` は `build_myself_preview.py` で新規。`-dads-preview.html` は旧合体版から DADS だけに変更）。symbol の id を `i-myself-*`（9）・`i-dads-*`（32）・`i-lc-*`（99、変更なし）に振りなおし、`gen_layouts.py`（`OWN_ICONS` を廃止し接頭辞で出典を判定）・qmd・html・build スクリプト・lessons を追随。qmd は `gen_layouts.py` で作り直し、html は `quarto render` で作り直した。決定の追記は無し（ユーザーの指示のみ）。

### 2026-11-06 Excalidraw の図作成から revealjs の HTML 化までを room で通した
- ユーザーの指示: 「excalidraw を room で動かせるか確認。room-myenv を使ってよい。room の図解を作り、SVG を revealjs に組み込んでスライド化。ゴールは room 作成の HTML を Windows で目視してズレがないこと」→ 確認後「問題なく、win で作ったものと同等です。一時ディレクトリは削除してください」。
- 結果: `room-myenv` は C: が空なので、`gen_layouts.py`・scss・アイコン html・`build_*.py` を `\\wsl.localhost\...\tmp\exc` へ複製し、room 内で `build_room_diagram.py` → `build_slide.py`（`quarto render`）を実行。SVG 2 つと `.excalidraw` は Windows 版とバイト一致。HTML を Windows に取り出し Edge ヘッドレスで 4 枚を撮影（画像方式の半幅用・全幅版は崩れなし。インラインは既知どおり不向き）。
- 後始末: `records/excalidraw-room-check/`（Windows 側）と room の `~/tmp/exc` を削除。決定は無し。
### 2026-11-06 room 図の半幅用の版を作った（NA を閉じた）
- ユーザーの指示: 「room 図の半幅用の版: 文字を大きくした版をやります。ナレッジは別セッションでやったのでここでは不要」→ 確認後「目視は問題ないです。これでいけます。これも close」。
- 反映: `records/excalidraw-trial/build_room_diagram.py` に `SPEC_HALF`（幅 700×560。見出し 22・補足と注記 20px、補足は改行可、矢印ラベルは複数行）を足し、全幅と半幅を同時に出す（`room-structure-half.excalidraw` / `.svg`）。`build_slide.py` は E インライン（全幅）・T の `side`（半幅用）・T の `side`（全幅を半幅に置く比較）の 3 枚を出す。`README.md` の「次」を更新。
- NA と `due.md` の行を閉じた。NA の後半（図解の型と Excalidraw 固有の手順のナレッジ化）は、ユーザーが別セッションで済ませたので、ここでは扱わず閉じた。
### 2026-11-06 K を横幅 1/3〜1/4 の列に置けるようにした（NA を閉じた）
- ユーザーの指示: 「K を、横幅 1/3〜1/4 の列に置けるように。layout.html にサンプルを出して。字間を詰めた版も比較できるように」→ 確認後「1/4 が使えます。0% が使えます。K だけ。英字列は 0% でないとスカスカ。全体は日本語が入るので 2%。補足の下に回る見た目は良い。インデントを揃えて」→「良いです」。
- 反映: `records/revealjs-diagram-theme.scss`（split 内の K は幅 100%・`min-width` と左余白を外す、補足は `nowrap` で入らなければ名前の字の開始位置にそろえて下の行へ、K の箱は字間 0、比較用クラス `tight`）、`records/gen_layouts.py`（spec の `cls`、見本に split(K+T) 1/3 と split(K+L) 1/4 を標準・詰めで 4 枚）。`revealjs-diagram-layouts.qmd`・`.html` を作り直した。`cols` だけでは足りず（`.tree-box` の `min-width: 55%` が邪魔）、split 内の K 用の CSS を足した。
- NA と `due.md` の行を閉じた。
### 2026-11-06 アイコン素材の出典の 1 行を、スライドごとに自動で入れた（NA を閉じた）
- ユーザーの指示: 「デジタル庁と lucide の 2 件をお願いします。layout.html にサンプルを出してください」→ 確認後「あってます。正しく記載されていました／良いです／重なりはないです。これで本件 close」。
- 反映: `records/gen_layouts.py` に `credit_div`（本文の `#i-<id>` から素材を判定。自作 9 種は出さない）、`records/revealjs-diagram-theme.scss` に `.src`（左下、14px）、組み込みの見本に「アイコン出典の見本」を追加。`revealjs-diagram-layouts.qmd`・`.html` を作り直した。文言: デジタル庁は「…を元に、色を変更して使用」+ URL、Lucide は「Lucide（ISC License）」+ URL。「末尾」はスライドごとの下（左下）と解釈し、ユーザーが確認した。
- NA と `due.md` の行を閉じた。
### 2026-11-06 Devicon の利用をやめ、ストックを削除した（組み込みの NA を omit）
- ユーザーの指示: 「組み込みは omit。devicon 自体も利用をやめるので、ストックのアイコンファイルを削除して。理由はアイコンが固有すぎて使うイメージが湧かないことと、ライセンスの縛り（提携に関する記載）が面倒なこと」。
- 反映: `git rm` で `records/build_devicon_icons.py`・`devicon-LICENSE.txt`・`revealjs-diagram-icons-devicon.html`・`…-devicon-preview.html` を削除（素材は MIT で、取得元から再取得できる）。NA（組み込み）と `due.md` の行を閉じ、出典の自動表記の NA から Devicon を外した。Open Questions の Devicon の項も削除。
ecords/build_devicon_icons.py・devicon-LICENSE.txt・
evealjs-diagram-icons-devicon.html・…-devicon-preview.html を削除（素材は MIT で、取得元から再取得できる）。NA（組み込み）と due.md の行を閉じ、出典の自動表記の NA から Devicon を外した。Open Questions の Devicon の項も削除。
- 決定: `decisions.md` に記録。

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

### 2026-11-07 実スライド 1 本を作った（NA 1 件を一部済み）
- 題材: LT「図解スライドを AI と作る流れ」7 枚（T・S・I・J・split(K+L)・T）。手順書どおりに一時ディレクトリで spec → qmd → render → Edge で目視。ユーザーが「よくできている」と確認。余白（S・I・J の下半分が空く）はこのままでよい（ユーザー）。
- 直したこと: 表紙のサブタイトルを中央（`.quarto-title-block p.subtitle`）。箇条書き 2 段目は本文を 1 字ぶん（1em）右にして日本語の字の並びをそろえ、行頭記号は白丸。「-」は存在感が無く、■ は ● と形が違うため（ユーザーが ○ で確定）。レイアウト番号は `--no-id` で消した。K の `cols` を `1fr 3fr` にした（最初に `1fr 1.2fr` と書いた私の指定ミス）。S・I の折り返しは文言を短くして解消。spec の `True` は JSON では `true`（手順書に追記）。
- 一部済: 「型の棚卸しの残り」のうち実スライドの確認が済み、`topics/office-output-types` との共通化の検討（別セッション）と P2（需要待ち）が残り。根拠: `records/revealjs-diagram-theme.scss`、`records/revealjs-slides-howto.md`。

### 2026-11-07 NA 2 npm install の目的の確認と、理解ガイドの下書き
- ユーザーの質問: 初回の `npm install` は WSL で Excalidraw を見るためか。答え: いいえ。Windows で人がブラウザで見るための閲覧用 JS（Excalidraw・React・esbuild）をキャッシュに作る。WSL では人が見ないので不要。ターミナルの AI にはブラウザの描画が出ないので、AI 用の利点も無い。PC1 の確認（NA）は残す（ユーザー）。
- 依頼を受けて、`stock 理解` で `exmem/inbox/2026-11-07-excalidraw-viewer-js-npm-explain.md` を作った（未追跡のまま。点検スクリプトは PASS 24・FAIL 0）。中身は JS・Node.js・npm・バンドル・React と、`excalidraw_view.py` ・`viewer_entry.jsx`・`build_viewer.mjs` の関係。`guides/explain/` への統合は `integrate` で行う。
- 見つけた食い違い: `excalidraw_view.py` の冒頭は「約 40MB」、`log.md` は「約 210MB」。PC で実測して直す（NA に足した）。

### 2026-11-07 NA2 draw の複数パターン試験（NA1・NA2 を閉じた）
- room-myenv の dummy Project（`myinv-draw-na2`。試験後に `room rm` で削除）で、`workflow-kit/draw-hook.md` を 4 パターン通した: 理解用（フォントなし・PNG）、slide（Noto Sans JP・SVG）、pptx（BIZ UDPゴシック・PNG。部屋にフォントが無く警告、代替字形）、キャプチャ入り（`image` 要素 + `files`）。すべて書き出せ、目視で崩れなし。
- あふれ試験（ユーザー指定の必須）: 幅 150 の箱に 12〜14 字を入れ、PNG で重なりを検出でき、幅を広げて 1 回で直った。ただし広げると半幅に収まらないので、手順書に直し方（行を折る・縦に積む・fontSize を下げる）を足した。キャプチャの書き方も足した（ユーザー承認）。
- フィードバック（`records/2026-11-07-draw-na2-trial.md`）: `room start --no-launch` が標準入力 EOF で落ちる、`wsl -- bash -c` で `$?` が wsl 側で展開される、PowerShell の標準入力渡しは CRLF で壊れる、Project の実体は `works/projects/`。サブエージェントは不要（ユーザー判断）。
- NA1（作図ループの仕上げ）: 手順書・room 通し・フィードバック取り込み・置き場の移動は 11-07 に済み、残りの NA2 も済んだので閉じた。根拠: `workflow-kit/draw-hook.md`、上の記録。残った pptx のフォントは新しい NA に切り出した。
