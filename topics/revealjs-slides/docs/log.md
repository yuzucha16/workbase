# 作業ログ（log）

`revealjs-slides`（Quarto → revealjs の図解レイアウト）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、見本・CSS は `records/`、型・原則は `exmem/lessons/revealjs-diagram-layout-output.md`。

## 状態

- 2026-11-06 に作成。PC1 の room で作ったノートと見本（`layouts.qmd`）を、写真から書き起こし、ノートは 11-06 に `exmem/lessons/revealjs-diagram-layout-output.md` へ統合した（置き場の決定は `decisions.md`）。
- 見本 `records/revealjs-diagram-layouts.qmd` と CSS `records/revealjs-diagram-theme.scss`: 6 型（A・B・D・E・F・G）を、見本のダミー図で置いてある。繰り返しの SVG は生成スクリプトで作り直した（スクリプトは一時ディレクトリで、リポジトリには無い）。
- 検証（11-06、Windows、Quarto 1.11.9、Edge ヘッドレス）: 7 枚（表紙 + 6 型）。空スライドの増えなし、札・アイコン・矢印・枠とも表示された。
- 未検証: room の Quarto での描画、枠の削れ（ノートの Gotchas）、D・E・F・G の実スライド。

## Next Actions

- 【期日 11-13】room（Quarto 入り）で見本を render し、Windows と見え方が同じか確かめる。担当: ユーザー（room）。
- 【期日 11-13】inv 型の成果物で、実スライドを 1 本作る（型 D・E・F・G の適用、文字量、枠の削れの対処）。ここまで通れば完了条件。

## Open Questions

- アイコンの語彙は、題材が変わっても流用できるか。
