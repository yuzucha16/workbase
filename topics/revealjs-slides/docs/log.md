# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、見本・CSS は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 2026-11-06 に作成。PC1 の room で作ったノートと見本（`layouts.qmd`）を、写真から書き起こし、ノートは 11-06 に `exmem/lessons/revealjs-diagram-layout-output.md` へ統合した（置き場の決定は `decisions.md`）。
- 見本 `records/revealjs-diagram-layouts.qmd` と CSS `records/revealjs-diagram-theme.scss`: 6 型（A・B・D・E・F・G）を、見本のダミー図で置いてある。繰り返しの SVG は生成スクリプトで作り直した（スクリプトは一時ディレクトリで、リポジトリには無い）。
- 検証（11-06、Windows、Quarto 1.11.9、Edge ヘッドレス）: 7 枚（表紙 + 6 型）。空スライドの増えなし、札・アイコン・矢印・枠とも表示された。
- room（`room-myenv`、Quarto 1.11.9）でも 7 枚で同じ見え方（11-06、B・D・F を目視。PC1 実機は未確認）。見え方の確認用に、room と Windows の html を `Downloads\revealjs-diagram-check\` に置いた（リポジトリ外）。
- 未検証: 枠の削れ（見本のダミー図では再現せず。実スライドで確かめる）、D・E・F・G の実スライド、PC1 の room 実機。

## Next Actions

- 【起票 11-06、期日 11-13】改善案の採否（試験は 11-06 に実施）: ①アイコン定義を include-before-body の別ファイルへ（試験で通った。先頭スライドに依存しなくなる）、②見本の SVG は約 20KB の手書きなので、生成スクリプトをリポジトリに入れるか Lua フィルタ化して、型と文言だけ書けば済む形にする、③閲覧側の PC でフォントが違っても崩れないか（フォント指定と埋め込み）、④多くの型で下 4 割が空く（図とフォントを大きくするか）、⑤使い方の手順（複製 → 型を選ぶ → 文言と図を置換 → render → 目視）を手順書にする。担当: ユーザー（採否）。
- 【期日 11-13】inv 型の成果物で、実スライドを 1 本作る（型 D・E・F・G の適用、文字量、枠の削れの対処）。ここまで通れば完了条件。

## Open Questions

- アイコンの語彙は、題材が変わっても流用できるか。
