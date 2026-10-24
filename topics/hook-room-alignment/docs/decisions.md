# 判断の記録（decisions）

## Decisions

### 【この件】【仮】Windows 実行のデバッグのラリーを減らす仕組み: 診断ログを毎回出し、原因を台帳に貯める。works 共通の置き場は作らない（2026-10-24）

- 決めたこと（ユーザー、2026-10-24。「方向性はOK」「この2つなら許容できる。仮決めで3段に乗せましょう」）: ① 境界（`interop`、マウント、sudo 不可）は変えない。`interop` の有効化は却下のまま。別ユーザー・Sandbox は PC1 で使えない。② 束ねる役の型に、毎回 `ai/work/diag.json`（環境、工程の結果、失敗の型と場所。伏せ字つき。環境由来の例外型に限りメッセージも載せる）を出す機能を足す。全文ログは今まで通り `--log` のときだけ。③ 原因の台帳は `ai/out/knowledge/`（`scope: area`、`kind: lesson`）。一般の原因は `scope: public` の下書きにも書き、`room stock` → `exmem/lessons/` に上げ、同じ原因が3回出たら `check_py.py` の規則に昇格する。④ works 共通の置き場は作らない。許容する弱点: PC1 の知見が他の Area に届くのが遅い（PC1 → PC2 は手で運ぶ）、業務固有の原因が Area ごとに重複する。⑤ ダミー入力での先行運用は保留（ユーザー「行きすぎな気もする」）。
- 根拠: ユーザーの回答（ラリーの主因は pwsh・bat の文字コードなど環境の違い。COM は未使用。対象は Excel、今後 pptx）。`script-guide.md` の型は既定ではログを出さず、最初の失敗では何も残らない（再実行がもう1周要る）。`baf6b64` で `stock` の行き先が `scope: public | area` になり、works 直下の層は却下済み。部屋には `exmem/lessons` と `workflow-kit` が全 Area に同じ写しで渡る（`room.py` の `SHARE_PATHS`）。
- 却下案: `interop` の有効化、`room debug`（実行中は人の目を通らない）、別ユーザー・Sandbox（PC1 で不可）、works 直下の置き場（写し・権限・`mkworks` の変更が要る。`stock` の相談でも却下済み）、現状維持で「`--log` で再実行」と表示するだけ（1周余分が残る）。
- 変更範囲（案）: `script-guide.md`（束ねる役の型 Python・ps1 に診断ログ、台帳の節）、`tools/check_py.py` と `check-ps1.ps1`（診断ログの有無を WARN）、`room-context.md`（失敗報告を受けたときの数行）、`docs/decisions.md`（2026-10-21「再訂正」の「既定ではログを出さない」を、診断に限って変える旨）。変えない: `room.py` の動作、境界、全文ログの既定。部屋用 `CLAUDE.md` の文面（`room.py` 内）に1行足す場合は文面だけ。
- 確認済み（2026-10-24）: `check_py.py` は `--log` と `'work'` と `argparse` の有無を見る（92 行）。型は `script-guide.md` にあり、既定ではログを出さない。`SHARE_PATHS` に `exmem/lessons` と `workflow-kit` が含まれる。WSL の `interop` は実行ファイルを限定できない（公式文書に該当の設定が無い）。
- 未確認: 診断ログの型を Windows の Python と pwsh で動かすこと（実装後に PC2 で1回）。伏せ字がユーザー名・ホスト名・パスを漏らさないこと。台帳が実際に参照されるか。
- 見直しの条件: 診断ログを入れても環境の違いのラリーが減らないとき。PC1 → PC2 の遅れで同じ原因が複数の Area で再発したとき（works 層を再検討）。

### 【この件】フックと room の整合の決定（2026-10-24）

- 正本は workbase 直下の `docs/decisions.md` の同日の3項（`init` `open` の廃止と `room mkworks`、`start` の `brief` への改名）。ここには重ねて書かない。
- 論点と案、変更範囲は [[hook-room-alignment-notes]]。

### 【この件】過去の記録の旧名は、現在の仕様が回りだしたら読み替えごと消す（2026-10-24）

- 決めたこと（ユーザー、2026-10-24）: 旧名（`init` `open` `start` のフック、`start-hook.md` など）の履歴は、新しい仕様が運用で回りだしたら、読み替えの注記もなくして消す。今は `hooks.md` の旧名の項が読み替えを持つ。
- 見直しの条件: `mkworks` の実機確認が済み、`brief` で問題が出ていないこと。
