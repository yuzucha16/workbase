# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、部品は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 部品（`records/`）: `gen_layouts.py`（生成スクリプト。型と文言から qmd を出す）、`revealjs-diagram-layouts.qmd`（スクリプトの出力。手で直さず作り直す）、`revealjs-diagram-theme.scss`（DADS 反映済み）、`revealjs-diagram-icons.html`、`2026-11-06-pptx-layout-inventory.md`、`2026-11-06-dads-summary.md`、`2026-11-06-dads-selection-table.md`、`build_dads_sample.py`（DADS 反映前後の見本を並べる。役目はほぼ終わり）。`dads-sample/` と `ai-room-lt/` は一時扱いで未コミット（`ai-room-lt` は旧スタイルのまま。追わない）。
- 型は 10 つ（A・B・D・E・F・G・H・I・J・T）。見た目は DADS 流の「背景なし・罫線だけ」（表・工程・箱。11-06 に図表の見た目は確定。`decisions.md`）。強調は薄青の地・太字・濃青の帯だけ。
- 行の高さは内容なりが既定（`height` 指定のときだけ下まで等分）。図表の上下に `lead`（上）と `notes`（下）でまとめ・総評を置ける。型・位置は固定でなく、AI が内容で選ぶ位置づけ（`gen_layouts.py` の SAMPLE の p10・p12 が例）。
- 検証: Edge（Windows）で H・I・J・B を目視済み。room は旧スタイルでの確認（新スタイルは未）、PC1 は未確認。T と見出しは未軽量化。

## Next Actions

- 【起票 11-06、期日 11-20】土台の更新の残り（図表は 11-06 に確定）: 見出し・T の軽量化。10 型の棚卸し（統合・廃止・新設。「AI が内容で型と上下の総評の位置を選ぶ」前提で、選び方の指針を `exmem/lessons/revealjs-diagram-layout-output.md` に反映する。`topics/office-output-types` と共通にできる構成を分ける）。行高 1.5・字間は実スライドで試す。DADS の保留（角の形状・エレベーション）は要るなら取る。担当: AI、ユーザー（目視）。- 【起票 11-06、期日 11-13】新しい部屋で `room init`（または `--only notosansjp`）を 1 回通し、Noto Sans JP が入ることを確かめる。担当: ユーザー（部屋の作り直し時）、AI。AI 側は済み（`INIT_STEPS` に段あり、単体テスト 17 件）。実機は、別 PC で `room init <Area> --resume`（または `--only notosansjp`）のあと `fc-list | grep 'Noto Sans JP,'`。
- 【起票 11-06、期日 11-13】PC1 の生成スクリプトがあれば、`gen_layouts.py` と見比べて足りない点を取り込む。担当: ユーザー（`room stock` で運ぶかを決める）、AI（見比べ）。
- 【起票 11-06、期日 11-13】pptx レイアウトの残り: 階段（pptx の 9）と 3 要素（28）が H・I で足りるかを判断する。ほかの pptx が渡されたら、同じ手順で棚卸しする。担当: AI、ユーザー（pptx）。
- 【起票 11-06、期日 11-13】H・I・J が Windows の Edge 以外（PC1 のブラウザ）でも同じ見え方か確かめる。担当: ユーザー（PC1 で開く）。

## Open Questions

- アイコンの語彙（9 種）は、別の題材で足りるかを次の実スライドで見る。
- 保留（ユーザーが細部を見始めたら）: ①閲覧側の PC でフォントが違っても崩れないか、②使い方の手順書（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）。
