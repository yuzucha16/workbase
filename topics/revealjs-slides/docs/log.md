# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、部品は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 部品（`records/`）: `gen_layouts.py`（生成スクリプト。型と文言から qmd を出す）、`revealjs-diagram-layouts.qmd`（9 型。スクリプトの出力。手で直さず作り直す）、`revealjs-diagram-theme.scss`、`revealjs-diagram-icons.html`（アイコン定義。`include-before-body` で読む）、`2026-11-06-pptx-layout-inventory.md`（pptx 33 枚の棚卸し）。
- 型は 10 つ: A・B・D・E・F・G に、pptx の例から H（行ラベル × 列）、I（工程 × 行。シェブロン）、J（表）を足し、図解なしの T（見出し + 段落 + 箇条書き。11-06 ユーザーの決定）を型に含めた。A〜G は spec の `"height"` で下の空きを埋められる。表現の方針は「行・列の数が自由」と「余白の統一」（`--gap` `--pad`、高さ `--h`。11-06 ユーザーの決定）。
- 検証（11-06）: 15 枚（表紙 + 14）を Windows（Quarto 1.11.9、Edge）で確認。room（`room-myenv`、Quarto 1.11.9、headless Chromium）でも 15 枚が render でき、I・J（3 枚）は Windows と同じ見え方（余白・右寄せ・ヘッダ色）。H は未目視、PC1 は未確認。
- 基本形を確定（11-06 ユーザーの決定）: 見本（`records/` の 3 ファイル。コミット `44799e1`）をそのまま基本形にする。フォントは Noto Sans JP、基準の文字サイズは 28px（`$presentation-font-size-root`。Quarto の `-main` は効かない）、インデントは `--ind: 40px` の固定値（見出し 1 段、箇条書き 2.5 段、入れ子は 1 段ずつ）、タイトルの下は 0.8em の空き。H・I・J の高さ `--h` は 560px（px。em は文字サイズに引きずられる）。H・J の行は 3 行までを見本にした（J の p17 は 4 行のまま。構造化は 3 要素以上で再分割するので、実用の上限は 3 程度）。見本に型 T の「文章・文字列・箇条書き」を足した（`gen_layouts.py` の `"p"`）。Windows（Edge、1280×720）で目視済み。
- 保留: 型 A〜G は下 4 割が空く（H・I・J は `--h` で埋めた。ユーザーは「一旦これでよい」）。- 実スライドは PC1 で作る（題材は PC1 側にある。11-06 ユーザーの発言）。PC1 は、このリポジトリを pull して `records/` の部品を使う。
- 細部は、ユーザーが見始めたら直す（11-06 決定）。フォントと文字サイズは 11-06 に確定した。

## Next Actions

- 【起票 11-06、期日 11-13】新しい部屋で `room init`（または `--only notosansjp`）を 1 回通し、Noto Sans JP が入ることを確かめる（11-06 は既存の room-myenv に root で手入れして確認済み）。担当: ユーザー（部屋の作り直し時）、AI。11-06 AI 側は済み（`notosansjp` 段は `room.py` の `INIT_STEPS` にあり、`init` 関連の単体テスト 17 件が通る）。実機の確認は、ユーザーが別 PC で `room init <Area> --resume`（または `--only notosansjp`）を実行し、`fc-list | grep 'Noto Sans JP,'` で確かめる。
- 【起票 11-06、期日 11-13】PC1 で実スライドを 1 本作る（題材は PC1 側。`gen_layouts.py` に JSON の仕様を渡す。型 D・E・F・G・H・I・J の適用、文字量、枠の削れの対処）。ここまで通れば完了条件。担当: ユーザー（PC1 で実行）、AI（PC1 のセッション）。作る中で出た型の不足は、このトピックに戻す。
- 【起票 11-06、期日 11-13】PC1 の生成スクリプトがあれば、`gen_layouts.py` と見比べて足りない点を取り込む。担当: ユーザー（`room stock` で運ぶかを決める）、AI（見比べ）。
- 【起票 11-06、期日 11-13】pptx レイアウトの残り: 階段（pptx の 9）と 3 要素（28）が H・I で足りるかを判断する。ほかの pptx が渡されたら、同じ手順で棚卸しする。担当: AI、ユーザー（pptx）。
- 【起票 11-06、期日 11-13】H・I・J が Windows の Edge 以外（PC1 のブラウザ、PowerPoint への貼り付けでない閲覧）でも同じ見え方か確かめる。担当: ユーザー（PC1 で開く）。

## Open Questions

- アイコンの語彙は、題材が変わっても流用できるか（PC1 の題材で分かる）。
- 保留（ユーザーが細部を見始めたら）: ①閲覧側の PC でフォントが違っても崩れないか（指定と埋め込み）、②型 A〜G は下 4 割が空く（H・I・J は `--h` で埋めた。A〜G にも同じ手を入れるか）、③使い方の手順書（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）。
