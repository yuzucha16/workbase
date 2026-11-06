# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、部品は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 部品（`records/`）: `gen_layouts.py`（生成スクリプト。型と文言から qmd を出す）、`revealjs-diagram-layouts.qmd`（スクリプトの出力。手で直さず作り直す）、`revealjs-diagram-theme.scss`（v1。まだ DADS 案を反映していない）、`revealjs-diagram-icons.html`、`2026-11-06-pptx-layout-inventory.md`、`2026-11-06-dads-summary.md`（DADS の要約。色の 16 進値を含む）、`2026-11-06-dads-selection-table.md`（取捨選択表）、`build_dads_sample.py`（v1 と DADS 案の見本 HTML を並べて作る。`dads-sample/` は一時扱いで未コミット）。
- 型は 10 つ（A・B・D・E・F・G・H・I・J・T）。表現の方針は「行・列の数が自由」と「余白の統一」。基本形は 11-06 に確定済み（Noto Sans JP、28px、`--ind: 40px` など。経緯は `log-history.md`）。ただし色と余白は、下の DADS の採用で置き換わる。
- DADS（デジタル庁デザインシステム）の取り込み（11-06）: 一次情報を要約し、取捨選択表の 5 点（強調色 Blue-900 `#0017c1`、純グレー、箱の色を青 1・濃灰 1・灰 1 に整理してクラス名を改める、余白は px の 8 の倍数、行高 1.5 と字間は実スライドで試す）をユーザーが採用した。見本（`dads-sample/dads/dads.html`）を Edge で確認し、「色だけでも雰囲気が変わり、よくなっている」。表の背景・罫線は気になる点で、次回に直す。決定は `decisions.md`。
- 実スライド（room 導入の LT、13 枚）は作成済み。`records/ai-room-lt/` は一時扱いで未コミット。
- 検証: Windows（Edge）と room（headless Chromium）で見本を確認済み。H は room で未目視、PC1 は未確認。保留: 型 A〜G は下 4 割が空く（H・I・J は `--h` で埋めた）。

## Next Actions

- 【起票 11-06、期日 11-20】土台の更新: 採用した 5 点（`decisions.md` の DADS の項。色は `build_dads_sample.py` の `PALETTE`）を `revealjs-diagram-theme.scss` と `gen_layouts.py`（箱のクラス名 `red` `green` `gray` の改称。見本 qmd と `ai-room-lt` も）に反映する。表の背景・罫線も直す（H・I・J の `.mx` `.tb`。気になる点はユーザーが指摘する）。そのあと 10 型を棚卸して統合・廃止・新設を決める（`topics/office-output-types` と共通にできる構成を分ける）。DADS の保留（角の形状・エレベーション）も要るなら取る。担当: AI、ユーザー（罫線の指摘）。
- 【起票 11-06、期日 11-13】新しい部屋で `room init`（または `--only notosansjp`）を 1 回通し、Noto Sans JP が入ることを確かめる。担当: ユーザー（部屋の作り直し時）、AI。AI 側は済み（`INIT_STEPS` に段あり、単体テスト 17 件）。実機は、別 PC で `room init <Area> --resume`（または `--only notosansjp`）のあと `fc-list | grep 'Noto Sans JP,'`。
- 【起票 11-06、期日 11-13】PC1 の生成スクリプトがあれば、`gen_layouts.py` と見比べて足りない点を取り込む。担当: ユーザー（`room stock` で運ぶかを決める）、AI（見比べ）。
- 【起票 11-06、期日 11-13】pptx レイアウトの残り: 階段（pptx の 9）と 3 要素（28）が H・I で足りるかを判断する。ほかの pptx が渡されたら、同じ手順で棚卸しする。担当: AI、ユーザー（pptx）。
- 【起票 11-06、期日 11-13】H・I・J が Windows の Edge 以外（PC1 のブラウザ）でも同じ見え方か確かめる。担当: ユーザー（PC1 で開く）。

## Open Questions

- アイコンの語彙（9 種）は、別の題材で足りるかを次の実スライドで見る。
- 保留（ユーザーが細部を見始めたら）: ①閲覧側の PC でフォントが違っても崩れないか、②型 A〜G の下 4 割の空き（`--h` の手を入れるか）、③使い方の手順書（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）。
- DADS 案で、Quarto 既定の青（左下のメニュー、下の進捗バー）が残る。土台の更新で、`$link-color` などを濃青に揃えるか決める。
