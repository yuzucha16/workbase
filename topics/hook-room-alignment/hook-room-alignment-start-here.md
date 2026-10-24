# 窓口: hook-room-alignment

- 型: Project 型。完了条件: `mkworks` の実機確認が済み、旧名（`init` `open` `start`）の読み替えと注記が消えて、フックと `room` の名前・工程の重なりが無い（残りのフックの調整は続ける）
- 何の取り組みか: `room` の導入で、合言葉のフックと `room` のコマンドの名前・工程が重なった。線は「決まった手順の副作用は人が打つ `room`、判断はフック」。`init` `open` を廃止して `room mkworks` などに移し、`start` を `brief` に改名した（2026-10-24）。議論の記録は [[hook-room-alignment-notes]]。

## いま

`init` `open` の廃止、`room mkworks`、`brief` の改名は反映済み（2026-10-24）。残りのフックと `room` の整合も反映済み。残りは `mkworks` の実機確認と、旧名の読み替えの削除。詳細は `docs/log.md`。

## あなた待ち

`review 消化` で、Windows 実行のデバッグのラリーを減らす仕組み（診断ログと原因の台帳。`docs/decisions.md` の仮決め）の承認。承認後に実装する。

## 次の一手

PC: `room mkworks --update` を既存の works で試す。

## 読む順

1. `docs/log.md`（現在状態と次にやること。開始時に読むのはここまで）
2. `docs/decisions.md`（何かを決める・変える前に検索する）
3. 必要なとき: [[hook-room-alignment-notes]]（事実の表、論点、変更範囲）、`docs/log-history.md`（経緯）

## リポジトリに無いローカルの状態

なし。dotfiles の Claude 用スキルに旧 `start` や「workflowを導入して」の入口が残っていないかは、dotfiles 側で確認する。
