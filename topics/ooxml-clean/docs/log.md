# 作業ログ（log）

`ooxml-clean`（xlsx・pptx の残存情報の点検・掃除）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `workflow-kit/room/cleankit.py`（標準ライブラリだけ、人が実行）と単体テスト 19 件（`tests/test_cleankit.py`）、使い方は `workflow-kit/room/README.md` の「クリーン化」、仕組みは `guides/explain/ooxml-residue.md`。最新は 2026-10-28 の `check` の文字の検査（`unseen-text`。見えている文字と固定語に当たらない文字を、部品ごとに報告。消さない）。
- 掃除の既定: 非表示シート、ノート、コメント、プロパティ、保存場所のパス、プリンター、縮小画像、calcChain、変更履歴、`#REF!` の定義名、非表示の定義名、外部リンク（数式は値に）、使っていない共有文字列、孤立した部品。`--also hidden-rows,hidden-cols` で非表示の行・列の値を空にする。
- 確認済み: ダミーで LibreOffice が出力を開き値が保たれる。PC1 の実 xlsx で、点検 20 件 → 掃除後 0 件（2026-10-27）。
- 確認済み（2026-10-28）: 修正後の出力が Excel で警告なしに開き、残り 0（警告の原因は共有文字列の番号の範囲外。修正済み）。
- 実装済み（2026-10-29）: プロファイル `standard` / `strict`（グラフ・画像・埋め込み・ピボット・接続を参照ごと外す。`--allow` で残す）。PC1 の実 xlsx・pptx で確認済み（2026-10-30、11-02、ユーザー）。pptx は strict が必須に近く unseen の区分が多いため、読ませる用途は取り出しに割り切った（`decisions.md` の同日の項）。cleankit の確認はこれで閉じた。
- 実装済み（2026-11-02）: `workflow-kit/room/pptxtext.py`（v0）と単体テスト 3 件。見えているスライドの文章・表・SmartArt・つながった矢印を md に出す。画像・グラフは印だけ。PC1 の実 pptx で動作確認済み（2026-11-02、ユーザー、問題なし）。要件の拡充は、足りないところが見えたときに積む。直させる用途の掃除（cleankit の pptx 手直し）は、需要が見えるまでしない。

- 実装済み（2026-11-03）: `room clean`（strict の掃除 → `ai/in`、`pending`）。語のマスクは必須でなくなった(任意の補助)。
- 実装済み（2026-11-02）: 知識の出口を `room stock --dst kit|area` の一本にし、internal にも `--dst area` と `ctx/area/` の写しを許した（`mask.toml` の語が空なら止まる）。単体テストは関係する 14 件を通した。

## Next Actions

1. 【期日 11-12】`room clean` の実機確認(PC1 の internal の Area で、実 xlsx・pptx を `pull` → `clean` → 読む → `start --adopt`)。報告 `_noai/reports/` の置き場と、`mask.toml` が無くても `stock --dst area` と Area の写しが通ることも見る。
2. 【期日 11-30】`room mask` / `restore` の削除は、使ってみてから決める(2026-11-03、ユーザー)。単体スクリプト化はしない。
3. 完了(2026-11-03): 語のマスクの必須を外した(`area_gate_terms` は語が空でも通る)。`room clean` を追加(internal だけ、strict、単体テスト 2 件)。決定は `decisions.md` の同日の項。

## Open Questions

- 報告（実データの抜粋入り）の置き場は決定済み（2026-10-30）: 組み込み後は `_noai/` 内の専用ディレクトリにまとめる。単体で叩くときの今の置き場（出力の隣）をどうするかは、組み込みの実装で決める。
- 書いていない語（本文の個人名）は掃除では消えない。11-02 に `cleankit check` へ検出（金額・メール・電話・割合の形と `--terms` の語）を足した。NA1 の確認（11-02）で、ダミーの金額・メール・電話・割合は検出された。本文の個人名の取りこぼしは `--terms` の語を使う運用で残る。
