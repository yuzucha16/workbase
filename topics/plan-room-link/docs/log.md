# 作業ログ（log）

計画と部屋の紐付け（`start 計画` の出力と、`room init` / `room open` が作る README の関連付け）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. （済 2026-10-21）`review 消化` の最終判断: 案 D（雛形に固定のポインタ1行だけ。案 A の印つきの節と差し替えは取り下げ）。`decisions.md` の先頭の項。論点 4（Area は触らない）と 5（`open` が先）は有効。
2. 【起票 10-21】実装（小さくなった）: `README.template.md` と `room.py` の `README_TEMPLATE` に固定の1行、`room-context.md` に部屋の AI が計画を `ai/in/plan/` から読むこと、`start-plan.md` の B-5 に置き場。`room.py` のロジックは変えない。承認済みの範囲を、着手前にユーザーに確認する。
3. 決まったら、`start 計画` で、この題材の 6R を作るか決める（作るなら出力は `records/`）。案が小さくなったので、作らない選択もある。

## Open Questions

- 相談の型（事実→論点→叩き台→確認）の仮決めは5回まで。使った回: 4（論点 1〜3、4〜6、`review 消化` での代替案の比較）。5回目で判断する（`decisions.md` の同日の項。締めとケア9項目を足した）。
