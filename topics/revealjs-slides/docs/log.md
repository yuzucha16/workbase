# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、部品は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 部品（`records/`）: `gen_layouts.py`（生成スクリプト。型と文言から qmd を出す）、`revealjs-diagram-layouts.qmd`（スクリプトの出力。手で直さず作り直す）、`revealjs-diagram-theme.scss`（DADS 反映済み）、`revealjs-diagram-icons.html`、`2026-11-06-pptx-layout-inventory.md`、`2026-11-06-layout-inventory.md`（型の棚卸しと提案 P1〜P3）、`2026-11-06-dads-summary.md`、`2026-11-06-dads-selection-table.md`、`build_dads_sample.py`（DADS 反映前後の見本を並べる。役目はほぼ終わり）、`build_lucide_icons.py`・`revealjs-diagram-icons-lucide.html`・`…-lucide-preview.html`・`lucide-LICENSE.txt`（Lucide 1.70.0 の 99 種。id は `lc-<名前>`。ISC）。Devicon は使わないと決めて削除した（11-06）。`dads-sample/` と `ai-room-lt/` は一時扱いで未コミット（`ai-room-lt` は旧スタイルのまま。追わない）。
- 型は 15 つ（A・B・C 目次・D・E・F・G・H・I・J・T、K ディレクトリ構造（`tree` の文字列 + Lucide のアイコン。フォルダは青・ファイルは灰。11-06 に Edge で目視、ユーザー確定）、DADS 部品の S 手順・L 説明リスト・N 注釈ブロック）に、組み合わせ `split`（2 つの型を左右に。表 + 箇条書き、図 + コードなど）。T は `side` で右にコード・画像を置ける。全型が `lead`/`notes` を持てる。仕様の正は `gen_layouts.py` の docstring。見た目は DADS 流の「背景なし・罫線だけ」（表・工程・箱。11-06 に図表の見た目は確定。`decisions.md`）。強調は薄青の地・太字・濃青の帯だけ。罫線は `#949494`（3:1）、箱の余白は px、箱の行高 1.5、字間は本文 2%・見出し 1%（11-06 反映。見本は目視済み）。
- 行の高さは内容なりが既定（`height` 指定のときだけ下まで等分）。図表の上下に `lead`（上）と `notes`（下）でまとめ・総評を置ける。型と位置は AI が提案し、最終判断はユーザー。スライドの右上に**レイアウト番号**（例 `H+notes`）を出す（`--no-id` で消す）。無い形は近い型で代用して spec に `want` を書き、逐次作る（11-06 ユーザーの決定。`decisions.md`、台帳は `gen_layouts.py` の `LAYOUTS`）。
- 基準の版: DADS v2.18.2（11-06）。`lessons/revealjs-diagram-layout-output.md` に DADS の章立て（基本デザイン・コンポーネント）で現行ルールと状態を記録済み。章立てはユーザー確認済み。版が上がったら突き合わせる。
- 検証: Edge（Windows）で H・I・J・B を目視済み。H・I・J は Windows の Edge 以外（PC1 のブラウザ）でも問題なし（11-06）。room init の Noto Sans JP 段は実機で通した（11-06）。PC1 の生成スクリプトは `gen_layouts.py` に取り込み済み。room での新スタイルの描画も確認済み（11-06 ユーザー）。見出し・T の軽量化、h3 の 1 段インデント、箇条書き 2 段まで、タイトルの濃青の縦棒は反映・目視済み（11-06）。C は Edge で目視し、ユーザーが確定（11-06）。`side` の画像はキャプションつきを目視済み（11-06 ユーザー。`1.` 止め・SVG の `aria-label` も反映済み）。`split` に A〜G を半幅で置く場合、コードの色分けは未検証。表（H・J）のセルは上揃え（DADS の table/usage に合わせた。11-06 ユーザーが目視して確定。工程の帯 I の見出しだけ中央）。`table/usage`・`card/usage` は取得・反映済み（DADS の未取得は `accessibility` など）。

- Excalidraw 試験（`records/excalidraw-trial/`。11-06 開始。方式 A = MCP なし）: `build_room_diagram.py` が仕様から `.excalidraw` と SVG を出す（SVG は自前の描画）。`.excalidraw` は Excalidraw で開いて崩れないことをユーザーが確認。SVG は T の `side.img`（alt・caption つき）で入れるのを標準にし、Edge で目視済み（ユーザー確認）。E の `fig`（インライン）は横長の図に不向き。方式 B（公式リモート MCP）は試して外した（11-06。ターミナルでは画像・ファイルが出ず成果物に使えない。MCP の常時分は 321 トークン。`decisions.md`）。経緯と次は同ディレクトリの `README.md`。

## Next Actions

- 【起票 11-06、期日 11-13】room 図の半幅用の版: 文字を大きくした版（幅 680 ほど）を `build_room_diagram.py` の仕様から作れるようにし、実スライドに入れる。あわせて、道具に依存しない図解の型と Excalidraw 固有の手順を分けてナレッジ化する案（draw.io へ差し替えられる形。`stock` はユーザーが言ったとき）。担当: AI、ユーザー（目視）。

- 【起票 11-06、期日 11-20】型の棚卸し（`records/2026-11-06-layout-inventory.md`。重なり・管理・拡充の整理は済み）の残りの実装。P2（split を 3 部品まで）は需要が出てから（`want` に溜める）。`topics/office-output-types` と共通にできる構成を分ける。担当: AI、ユーザー（選択・目視）。

- 【起票 11-06、期日 11-13】アイコン素材の出典の 1 行を、スライドの末尾に自動で入れる（11-06 ユーザーが「入れます」と決定）。デジタル庁の素材（利用規約 1-2: 加工して公表・利用するときは出典と加工内容を明示し、国が作ったかのように見せない）と Lucide（ISC。著作権表示と許諾文の同梱は済み）が対象（Devicon は使わない）。`gen_layouts.py` が、使ったアイコンの素材（`lc-` は Lucide、デジタル庁の素材名、自作は出さない）ごとに、末尾へ 1 行（例: 「アイコン: 『イラストレーション・アイコン素材』（デジタル庁）を元に色を変更して使用」「アイコン: Lucide（ISC License）」と URL）。担当: AI（実装）、ユーザー（文言と位置の目視）。

- 【起票 11-06、期日 11-13】K を、横幅 1/3〜1/4 の列に置けるようにする（ユーザーの予定: ディレクトリ構造は左右二分割だと余白が広くなる）。`split` の `cols`（例 `1fr 3fr`）で足りるか、`.tree-box` の `min-width: 55%` が邪魔しないか、右に説明（T・L・N）を置いた見え方を Edge で確かめ、必要なら K 用の `cols` の既定を足す。担当: AI、ユーザー（目視）。

## Open Questions

- Lucide（開発系 99 種。`lc-<名前>`、札の `icon` と K の `[..]` で使う）を足した（11-06）。1.70.0 には `github`・`triangle-alert`・`trash-2`・`history` が無い（警告の三角形は無し。別名 `trash`・`undo-2`・`octagon-x`）。K の行間は広めだが、一旦このまま使う（ユーザー）。
- アイコンは自作 9 種に、デジタル庁の素材（line 版・24px）から 32 種を足した（11-06。`records/revealjs-diagram-icons-dads.html`、作り直しは `build_dads_icons.py`。一覧を Edge で目視済み。意味の割り当てはスクリプトの `PICK`）。札の `icon` に素材名（例 `search`）を書けば使える。実スライドで足りるかは次の題材で見る。出典の明示は利用規約 1-2（加工した場合）。
- 保留（ユーザーが細部を見始めたら）: ①閲覧側の PC でフォントが違っても崩れないか、②使い方の手順書（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）。
