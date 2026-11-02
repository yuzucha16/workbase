# 作業ログ（log）

`ooxml-clean`（xlsx・pptx の残存情報の点検・掃除）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- `workflow-kit/room/cleankit.py`（標準ライブラリだけ、人が実行）と単体テスト 19 件（`tests/test_cleankit.py`）、使い方は `workflow-kit/room/README.md` の「クリーン化」、仕組みは `guides/explain/ooxml-residue.md`。最新は 2026-10-28 の `check` の文字の検査（`unseen-text`。見えている文字と固定語に当たらない文字を、部品ごとに報告。消さない）。
- 掃除の既定: 非表示シート、ノート、コメント、プロパティ、保存場所のパス、プリンター、縮小画像、calcChain、変更履歴、`#REF!` の定義名、非表示の定義名、外部リンク（数式は値に）、使っていない共有文字列、孤立した部品。`--also hidden-rows,hidden-cols` で非表示の行・列の値を空にする。
- 確認済み: ダミーで LibreOffice が出力を開き値が保たれる。PC1 の実 xlsx で、点検 20 件 → 掃除後 0 件（2026-10-27）。
- 確認済み（2026-10-28）: 修正後の出力が Excel で警告なしに開き、残り 0（警告の原因は共有文字列の番号の範囲外。修正済み）。
- 実装済み（2026-10-29）: プロファイル `standard` / `strict`（グラフ・画像・埋め込み・ピボット・接続を参照ごと外す。`--allow` で残す）。PC1 の実 xlsx・pptx で確認済み（2026-10-30、11-02、ユーザー）。pptx は strict が必須に近く unseen の区分が多いため、読ませる用途は取り出しに割り切った（`decisions.md` の同日の項）。cleankit の確認はこれで閉じた。
- 実装済み（2026-11-02）: `workflow-kit/room/pptxtext.py`（v0）と単体テスト 3 件。見えているスライドの文章・表・SmartArt・つながった矢印を md に出す。画像・グラフは印だけ。PC1 の実 pptx で動作確認済み（2026-11-02、ユーザー、問題なし）。要件の拡充は、足りないところが見えたときに積む。直させる用途の掃除（cleankit の pptx 手直し）は、需要が見えるまでしない。

- 実装済み（2026-11-02）: 知識の出口を `room stock --dst kit|area` の一本にし、internal にも `--dst area` と `ctx/area/` の写しを許した（`mask.toml` の語が空なら止まる）。単体テストは関係する 14 件を通した。

## Next Actions

1. 【期日 11-09】境界の見直し（external / internal）の動作確認と残り: `records/2026-11-02-boundary-pending.md`（PC1 の確認 5 点と、単体スクリプト化、cleankit の internal 既定）。
2. 【期日 11-12】room の `mask` への cleankit の組み込み（決定 2026-10-30）。11-02 の見直しで `start` が自動でマスクしなくなったので、組み込み先と要否を、1 の確認の後に決め直す。

3. 【期日 11-16】外向け Area の共有（NA1）の動作確認（別セッション、PC1）: external のダミーの Area で、部屋の AI が `ai/out/stock/` に `scope: area`（`dest: knowledge|docs`）で書く → `room stock <名> --dst area`（cleankit の点検に当たると止まる）→ `areas/<Area>/ai/` → 次の `start` で `ai/ctx/area/` に写る → AI が読める。確認点: 点検の雑音と取りこぼし、`docs/inbox.md` 除外、1 MiB 上限、人が直した先を上書きしない。
4. 【期日 11-16】internal の Area への適用: 決定・実装済み（2026-11-02）。出口は `room stock --dst kit|area` の一本で、internal にも `--dst area` と `ctx/area/` の写しを許した（`mask.toml` の語が空なら止まる・写さない）。残り: internal のダミーでの動作確認（NA3 と同じ確認点に、語が空で止まることを足す）。確認の後に、`restore`・`pull` の知識用の経路をコードから外す（ユーザーの決定。成果物の戻し `ai/out/deliverable/` は残す）。

## Open Questions

- 報告（実データの抜粋入り）の置き場は決定済み（2026-10-30）: 組み込み後は `_noai/` 内の専用ディレクトリにまとめる。単体で叩くときの今の置き場（出力の隣）をどうするかは、組み込みの実装で決める。
- 書いていない語（本文の個人名）は掃除では消えない。11-02 に `cleankit check` へ検出（金額・メール・電話・割合の形と `--terms` の語）を足した。実ファイルでの雑音と取りこぼしは NA1 の確認で見る。
