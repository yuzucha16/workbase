# 作業ログ（log）

`ooxml-clean`（xlsx・pptx の残存情報の点検・掃除）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `workflow-kit/room/cleankit.py`（標準ライブラリだけ、人が実行）と単体テスト 13 件（`tests/test_cleankit.py`）、使い方は `workflow-kit/room/README.md` の「クリーン化」、仕組みは `guides/explain/ooxml-residue.md`。最新は 2026-10-28 の `check` の文字の検査（`unseen-text`。見えている文字と固定語に当たらない文字を、部品ごとに報告。消さない）。
- 掃除の既定: 非表示シート、ノート、コメント、プロパティ、保存場所のパス、プリンター、縮小画像、calcChain、変更履歴、`#REF!` の定義名、非表示の定義名、外部リンク（数式は値に）、使っていない共有文字列、孤立した部品。`--also hidden-rows,hidden-cols` で非表示の行・列の値を空にする。
- 確認済み: ダミーで LibreOffice が出力を開き値が保たれる。PC1 の実 xlsx で、点検 20 件 → 掃除後 0 件（2026-10-27）。
- 確認済み（2026-10-28）: 修正後の出力が Excel で警告なしに開き、残り 0。10-28 までの警告は、共有文字列の番号が範囲の外になる不具合（空のセル `<c .../>` の次を読み落とし）で説明がつく（合成 xlsx で再現・修正。`check` で古い出力を点検すると「整合の問題」に出る）。PowerPoint 本体、pptx の実ファイル。
- 実装済み（2026-10-29）: プロファイル `standard` / `strict`（グラフ・画像・埋め込み・ピボット・接続を参照ごと外す。`--allow` で残す）。ダミーの単体テストまで。実ファイルを Excel・PowerPoint で開く確認は未。

## Next Actions

1. プロファイル方式の掃除（`--profile standard|strict`、`--allow`、`profiles`。10-29 に実装、単体テスト追加、手順書 `guides/howto/ooxml-clean.md`）を、PC1 の実ファイルで通す（動作確認は別セッション、ユーザー）。Excel・PowerPoint で警告なしに開くか、`strict` で見た目が許容か、`unseen-text` の量（固定語の足りなさ）と取りこぼしを見る。
2. 見た目・数式が崩れていないか、非表示の行・列を空にして困らないかをユーザーが確認。
3. room の `mask` への組み込み（掃除 → マスク）の要否を決める（2026-10-26 の方針案では前段に挟む）。
4. pptx を実ファイルで 1 回通す。

## Open Questions

- 報告（実データの抜粋入り）の既定の置き場。今は出力の隣（リポジトリ外を指定させる守りは入れた）。`_noai/` 固定にするか。
- 書いていない語（本文の個人名）は掃除では消えない。`mask.toml` の運用に任せるか、候補の検出を足すか。
