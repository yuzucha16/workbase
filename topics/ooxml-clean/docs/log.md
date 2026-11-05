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
- 実装済み（2026-11-03）: `workflow-kit/room/exceltext.py`（v0。pptxtext の xlsx 版）と単体テスト 4 件。単体のスクリプトとして使う（room には組み込まない。11-03 に一度 `room clean --text` を足したが、ユーザーの指示で外した）。実ファイル（PC1）は未確認。
- 実装済み(2026-11-03): `room close` の `【決定】` 行(根拠の実在検査と sensitive_hits で、移動前に止める)→ Area の inbox、`INBOX_NEW` の規約、`room trace <Project>#n`。`test_room` 全 167 件を通した。実機確認済み（2026-11-04、PC1、ユーザー）。
- 実装済み（2026-11-04）: clean 後に残るテナント ID・ラベル ID の掃除。`labels`・`custom-xml` を既定に、`hyperlinks`・`tags`・`addins` を strict に足し、`props`・`revisions` を広げ、check に `tenant-id` ほかを足した（単体テスト 5 件。ダミー値の合成ファイルで standard・strict の出力を実測し、LibreOffice で開けた）。PC1 の実ファイルで、ラベル・テナント ID が残らないことと Excel・PowerPoint で開けることは確認済み（2026-11-05、ユーザー、問題なし）。
- 確認済み（2026-11-05、PC1、ユーザー）: `exceltext.py` を実 xlsx に通して問題なし。
- 見送り（2026-11-05）: `room clean` と `cleankit` の一本化（`cleankit check` を `room clean --check` に寄せる案、`cleankit clean` を `room clean` に寄せる案とも）。影響範囲が広く、確認の手間に見合わない（`decisions.md`）。cleankit と room clean は今のまま並べて使う。

## Next Actions

なし。残りは `docs/due.md` の 11-30（`mask` / `restore` の削除。使ってみてから決める）。

## Open Questions

- なし（2026-11-04 に 2 件を閉じた。経緯は `log-history.md`、制約は `decisions.md`）。
