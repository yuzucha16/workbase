# 境界の見直し（external / internal）で積んだ残りと動作確認（2026-11-02）

決定は `docs/decisions.md`（直下）の 2026-11-02 の 2 項。実装は 9d35958（boundary の 2 値化と external のガード）と 54b2a8b（`start` から自動のマスク・復元を外す、マスクの出力は `pending`、`cleankit check` の検出）。

## 動作確認（PC1。internal の Area で、ダミーのデータから）

1. `boundary:` が無い Area、`boundary: external` の Area で、`room pull` / `room mask`（原本あり）/ `start --adopt` が理由つきで止まる。`init` / `open` は止まらない。
2. `boundary: internal` の Area で `room mask` → `ai/in/` を読む → `start` が「確認していない」で止まる → `start --adopt` で通る → `restore` で `_noai/final/` に戻る。手順が 1 つ増えて重くないか。
3. `start` が、`_noai/raw` の原本と `ai/out` を見つけたときに案内だけ出し、マスクも復元もしない。
4. `cleankit check <ファイル> --terms <mask.toml>` が、金額・メール・電話・割合の形と語を警告する。雑音（日付や型番の数）と取りこぼしを、実ファイルで見る。
5. 既存の Area の `boundary:` が自由な印のままなら、すべて external 扱いになる。internal にしたい Area にだけ手で付ける。

## 積んだ残り

- 外向け（external）の Area で、共有用の `areas/<Area>/ai/` を部屋に見せる案: 2026-11-02 に決着。マウントでなく「写し」（`start` が `ai/ctx/area/` に読み取り専用で置く）。書き込みは `room stock --dst area`（cleankit の点検つき）。internal への適用は未決（`docs/log.md` の NA4）。動作確認は別セッション（NA3）。
- mask / restore / pull の単体スクリプト化（第 2 段）。使わないと分かってから。分けるときの注意: マスクの状態（原本と `mask.toml` のハッシュ）は manifest に入っている、restore は Area の置き場への公開（`routes` と `plan_publish`）も持つ、`start` の自動の歯止めが無くなる。
- `cleankit` の `internal` での既定を `strict` にするか（今は `standard` が既定。room から呼ぶ組み込みは未実装）。
- 検出（`check_sensitive`）の拡張: 出力側の点検（AI の出力に実名や金額の形が無いか）。
- `docs/decisions.md` の理由は書かない運用。理由は ee が na に移す（`notes/ai-guideline-realign/2026-11-02-reason-for-na.md`）。
