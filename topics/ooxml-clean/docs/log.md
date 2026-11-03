# 作業ログ（log）

`ooxml-clean`（xlsx・pptx の残存情報の点検・掃除）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `workflow-kit/room/cleankit.py`（標準ライブラリだけ、人が実行）と単体テスト 19 件（`tests/test_cleankit.py`）、使い方は `workflow-kit/room/README.md` の「クリーン化」、仕組みは `guides/explain/ooxml-residue.md`。最新は 2026-10-28 の `check` の文字の検査（`unseen-text`。見えている文字と固定語に当たらない文字を、部品ごとに報告。消さない）。
- 掃除の既定: 非表示シート、ノート、コメント、プロパティ、保存場所のパス、プリンター、縮小画像、calcChain、変更履歴、`#REF!` の定義名、非表示の定義名、外部リンク（数式は値に）、使っていない共有文字列、孤立した部品。`--also hidden-rows,hidden-cols` で非表示の行・列の値を空にする。
- 確認済み: ダミーで LibreOffice が出力を開き値が保たれる。PC1 の実 xlsx で、点検 20 件 → 掃除後 0 件（2026-10-27）。
- 確認済み（2026-10-28）: 修正後の出力が Excel で警告なしに開き、残り 0（警告の原因は共有文字列の番号の範囲外。修正済み）。
- 実装済み（2026-10-29）: プロファイル `standard` / `strict`（グラフ・画像・埋め込み・ピボット・接続を参照ごと外す。`--allow` で残す）。PC1 の実 xlsx・pptx で確認済み（2026-10-30、11-02、ユーザー）。pptx は strict が必須に近く unseen の区分が多いため、読ませる用途は取り出しに割り切った（`decisions.md` の同日の項）。cleankit の確認はこれで閉じた。
- 実装済み（2026-11-02）: `workflow-kit/room/pptxtext.py`（v0）と単体テスト 3 件。見えているスライドの文章・表・SmartArt・矢印を md に出す。PC1 で確認済み。拡充は足りないところが見えたときに積む。pptx の手直しは需要が見えるまでしない。

- 実装済み（2026-11-03）: `room clean`（strict の掃除 → `ai/in`、`pending`。報告は `_noai/raw/tmp/`、章の順は「掃除の後も残っているもの」が先）。語のマスクは必須でなくなった(任意の補助)。
- 実装済み（2026-11-03）: `pull` を廃止。原本は共通性で分ける(固有は `raw/`、共通の xlsx・pptx は `source/` を `room clean --path`、共通の md は Area の `ai/docs/`)。決定は root の `docs/decisions.md`。
- 実装済み（2026-11-02）: 知識の出口を `room stock --dst kit|area` の一本にし、internal にも `--dst area` と `ctx/area/` の写しを許した（`mask.toml` の語が空なら止まる）。単体テストは関係する 14 件を通した。
- 実機確認済み(2026-11-03、PC1): `clean --path` → `ai/in/area/`、`start --adopt` で通る。報告は `_noai/source/tmp/`(`461160d`)。

## Next Actions

1. 【期日 11-10】Project の `docs/`(log・decisions への追記)を Area の共有知に統合する経路を設計する。今の `stock --dst area` は `ai/out/stock/*.md` を新規ファイルとして運ぶ形で、追記・マージの意図(各 Area で共有知として育てる)とずれる(2026-11-03 実機確認、ユーザー)。

## Open Questions

- 報告（実データの抜粋入り）の置き場は決定済み: `raw` 経由の `room clean` は `_noai/raw/tmp/`、`--path` は Area の `_noai/source/tmp/`(2026-11-03、ユーザー。どちらも原本には数えない)。単体で叩くときの置き場(出力の隣)は変えない。
- 書いていない語（本文の個人名）は掃除では消えない。11-02 に `cleankit check` へ検出（金額・メール・電話・割合の形と `--terms` の語）を足した。NA1 の確認（11-02）で、ダミーの金額・メール・電話・割合は検出された。本文の個人名の取りこぼしは `--terms` の語を使う運用で残る。
