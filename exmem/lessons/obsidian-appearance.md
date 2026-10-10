---
type: knowledge
title: Obsidian のファイル一覧の色分けと、CSS で変えられない範囲
status: active
tags:
  - tool/obsidian
  - accessibility
  - theming
aliases:
  - Obsidianの見た目
  - ファイルエクスプローラーの配色
  - file-explorer-compact
created: 2026-10-05
updated: 2026-10-05
sources:
  - Claude Code conversation "Obsidian のファイルエクスプローラーの配色調整" (2026-10-04〜2026-10-05)
  - "dotfiles の windows/obsidian/.obsidian/snippets/file-explorer-compact.css（2026-10-05 に確認）"
---

# Obsidian のファイル一覧の色分けと、CSS で変えられない範囲

## Purpose

Obsidian のファイルエクスプローラー（と、周辺のタブ・ウィンドウボタン）を見やすくする。単一色だったアイコンを種類ごとに色分けし、起動や処理が重くならないことを確かめる。CSS で変えられた範囲と、変えられなかった範囲（入れ子のインデント）を残す。設定全体は [[obsidian-vault]]。

## Principles

- ファイルの種類を色で見分けられるようにする。探す作業が速くなり、目への負担も減る（ユーザーの発言。作業効率に加えて目への負担も考慮している）。
- 見た目の調整は、プラグインを入れず CSS スニペットだけで行う。JS を読み込まないので、起動や処理が重くならない。
- 色は、テーマのパレット（`--color-*`）を使う。テーマやライト・ダークの切り替えに追従する。見出しの色など、パレットに無い値だけを直接書き、どこと同じ値かをコメントに残す。
- 見た目の調整のように試行錯誤が多い作業は、`docs/log.md` に途中経過を書かず、確定したときにまとめて記録する（ユーザーの指示。理由の説明は無かった）。

## Decisions

### ファイルの種類ごとにアイコンを色分けする（2026-10-04）

- 根拠: 単一色（`--text-faint`）では見分けにくい。形状（`mask`）は流用でき、色の変更だけで済む。
- 却下案: 単一色のまま。

### アイコンは CSS だけで付ける（2026-10-04）

- 根拠: ユーザーが目標を「アイコンの適用と、起動や処理が重くならないことの確認まで」と定めた。静的な属性セレクタだけで、スクリプトは増えない。
- 却下案: アイコン用のプラグイン（Iconize、`obsidian-icon-folder`。JS を読み込むので起動が重くなる可能性がある。仮説）。

### 階層ごとのインデントを狭めることは、見送る（2026-10-04）

- 根拠: Obsidian が行ごとにインラインの `!important` で位置を決めていて、スニペットから変えられない（Facts を参照）。ユーザーが試して、見送りを決めた。
- 却下案: `--nav-item-children-margin-left` と `--nav-item-children-padding-left` の変更（変わらなかった）、`.nav-folder-children` の `margin-left` の直接指定（余白だけ変わり、行の位置と食い違って、一部の行がずれた）。

### `.md` の拡張子を、エクスプローラーに足さない（2026-10-04）

- 根拠: Obsidian は `.md` だけを隠す標準の挙動で、ユーザーはそれを知って、足す必要は無いと判断した。
- 却下案: `::after` で薄い色の `.md` を足す（一度適用したが、取りやめた）。

## Facts

- 使った Obsidian のバージョンは 1.13.7（2026-10-05 時点。根拠: ユーザーが貼った DOM のタイトルバー）。
- 色分け（ユーザーが選んだ配色。理由の説明は無かった）: ノート=blue、`.base`=green、コード・設定（`.json` `.css` `.js` `.yml` `.yaml` `.toml` `.sh` `.ps1`）=orange、画像=purple、`.pdf`=red。フォルダは、開いているとき `--color-yellow`、閉じているとき `#A7B85A`（スニペットの見出し色と同じ）。途中で「開=緑、閉=本文色」を試し、変更した（確認: 2026-10-05、根拠: `file-explorer-compact.css` の色指定がこの配色と一致した）。
- Material Gruvbox テーマでは、`--color-yellow` が `--neutral-yellow`、`--color-orange` が `--faded-yellow`（確認: 2026-10-04、根拠: テーマの `theme.css`）。ユーザーは、最初の `--color-yellow` のフォルダを「orange」と呼んだ。
- エクスプローラーとアウトラインの各行には、階層に応じたインライン指定が付く。例: 深さ0のフォルダは `margin-inline-start: 0px; padding-inline-start: 8px`、深さ2は `-34px` と `42px`、深さ3のファイルは `-50px` と `63px`（すべて `!important`）。1階層ごとに約17px（確認: 2026-10-05、根拠: ユーザーが貼った DOM）。
- 行の基準位置は、`--nav-item-padding` の値が反映される（トップレベルのファイルの `padding-inline-start` が、指定した 13px になっていた。確認: 2026-10-05、根拠: DOM）。階層ごとの増分には、`--nav-item-children-*` の変更が反映されなかった。
- アウトラインにも同じインライン指定が付く（確認: 2026-10-05、根拠: DOM。`padding-inline-start: 30px !important`）。
- エクスプローラーでは、`.md` の行に拡張子バッジが無く、`.base` の行には `nav-file-tag` で `base` が出る（確認: 2026-10-05、根拠: DOM）。
- テーマは、アクティブなタブの文字色 `--tab-text-color-focused-active-current` を赤、`--tab-text-color-focused-active` を黄、タイトルバー（最小化・最大化・閉じるのボタン）の `--titlebar-text-color-focused` を赤にしていた（確認: 2026-10-04、根拠: `theme.css`。ダークは `neutral-red`、ライトは `bright-red`）。スニペットは3つとも `var(--text-normal)` で上書きしている（確認: 2026-10-05、根拠: `file-explorer-compact.css` の42〜45行目）。変数はテーマが `.theme-dark` / `.theme-light` に定義するため、スニペット側は `body.theme-dark, body.theme-light` で上書きする（セレクタの優先度のため。仮説）。上書きの効果は、ユーザーから追加の指摘が無かったが、明示的な確認は取っていない。
- 起動・処理の軽さは、計測していない（CSS のルールの追加だけで、スクリプトは無い）。

## Gotchas

- **入れ子の余白の変数と、`.nav-folder-children` の `margin-left` を変えて、インデントを狭めようとした**: Obsidian が各行に、階層に応じた `margin-inline-start` と `padding-inline-start` を、`!important` のインラインで付けている。コンテナの余白だけを変えると、行の位置との前提が崩れ、アクティブ行などがずれる（仮説）。元に戻して、見送った（アウトラインも同じ仕組みで、変数を変えても変わらなかった）。
- **「タグのファイル名を緑に」の指示を、ノート名に適用してしまった**: 対象の呼び方が曖昧で、確認の選択肢でも取り違えが起きた（本来の対象は、タグペインのタグ名）。戻して、対象を画面上の名称（タグペイン）で指定し直した。

## Open Questions

- `file-explorer-compact.css` に、エクスプローラー以外（タブ、タイトルバー）の指定が入った。スニペットを分けるか、名前を変えるか。
- ウィンドウがフォーカスされていないときの色（`--titlebar-text-color`、`--tab-text-color` 系）が赤や黄のままか。未確認。
- 提案: 見出しの緑 `#A7B85A` を、1つの変数にまとめ、`material-gruvbox-bold.css` と `file-explorer-compact.css` で共有する（AI の提案。未承認。現状は値を2か所に書いている）。

## Next Actions

- タブとウィンドウボタンの色を、フォーカスの有無で確認する。

## Related

- [[obsidian-vault]]
- [[app-config-placement]]
