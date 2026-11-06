# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、部品は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 部品（`records/`）: `gen_layouts.py`（生成スクリプト。型と文言から qmd を出す）、`revealjs-diagram-layouts.qmd`（スクリプトの出力。手で直さず作り直す）、`revealjs-diagram-theme.scss`（DADS 反映済み）、`revealjs-diagram-icons.html`、`2026-11-06-pptx-layout-inventory.md`、`2026-11-06-layout-inventory.md`（型の棚卸しと提案 P1〜P3）、`2026-11-06-dads-summary.md`、`2026-11-06-dads-selection-table.md`、`build_dads_sample.py`（DADS 反映前後の見本を並べる。役目はほぼ終わり）。`dads-sample/` と `ai-room-lt/` は一時扱いで未コミット（`ai-room-lt` は旧スタイルのまま。追わない）。
- 型は 11 つ（A・B・C 目次・D・E・F・G・H・I・J・T）に、組み合わせ `split`（2 つの型を左右に。表 + 箇条書き、図 + コードなど）。T は `side` で右にコード・画像を置ける。全型が `lead`/`notes` を持てる。仕様の正は `gen_layouts.py` の docstring。見た目は DADS 流の「背景なし・罫線だけ」（表・工程・箱。11-06 に図表の見た目は確定。`decisions.md`）。強調は薄青の地・太字・濃青の帯だけ。
- 行の高さは内容なりが既定（`height` 指定のときだけ下まで等分）。図表の上下に `lead`（上）と `notes`（下）でまとめ・総評を置ける。型と位置は AI が提案し、最終判断はユーザー。スライドの右上に**レイアウト番号**（例 `H+notes`）を出す（`--no-id` で消す）。無い形は近い型で代用して spec に `want` を書き、逐次作る（11-06 ユーザーの決定。`decisions.md`、台帳は `gen_layouts.py` の `LAYOUTS`）。
- 検証: Edge（Windows）で H・I・J・B を目視済み。H・I・J は Windows の Edge 以外（PC1 のブラウザ）でも問題なし（11-06）。room init の Noto Sans JP 段は実機で通した（11-06）。PC1 の生成スクリプトは `gen_layouts.py` に取り込み済み。room での新スタイルの描画も確認済み（11-06 ユーザー）。見出し・T の軽量化、h3 の 1 段インデント、箇条書き 2 段まで、タイトルの濃青の縦棒は反映・目視済み（11-06）。C は Edge で目視し、ユーザーが確定（11-06）。`side` の画像、`split` に A〜G を半幅で置く場合、コードの色分けは未検証。

## Next Actions

- 【起票 11-06、期日 11-20】型の棚卸し（`records/2026-11-06-layout-inventory.md`。重なり・管理・拡充の整理は済み）の残りの実装。P2（split を 3 部品まで）は需要が出てから（`want` に溜める）。`topics/office-output-types` と共通にできる構成を分ける。行高 1.5・字間は実スライドで試す。C の見た目（章の再掲での強調、ひとこと列）も見直す。担当: AI、ユーザー（選択・目視）。

## Open Questions

- アイコンの語彙（9 種）は、別の題材で足りるかを次の実スライドで見る。
- 保留（ユーザーが細部を見始めたら）: ①閲覧側の PC でフォントが違っても崩れないか、②使い方の手順書（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）。
