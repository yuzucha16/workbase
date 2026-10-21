# 作業ログ（log）

計画と部屋の紐付け（`start 計画` の出力と、`room init` / `room open` が作る README の関連付け）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. （済 2026-10-21）`review 消化` の最終判断: 案 D（雛形に固定のポインタ1行だけ。案 A の印つきの節と差し替えは取り下げ）。`decisions.md` の先頭の項。論点 4（Area は触らない）と 5（`open` が先）は有効。
2. （済 2026-10-21。範囲はユーザーが承認）実装: `README.template.md` と `room.py` の `README_TEMPLATE` に固定の1行、`room-context.md` に節「計画（部屋の中）」、テスト1件。単体テスト 109 件パス（スキップ 3）。実機は未確認（`room open` で作った README に1行あるかを、次の `open` で見る）。
3. 【起票 10-21】`start 計画` で、この題材の 6R を作る（ユーザーが決めた。出力は `records/`）。続けて憲章・WBS・マイルストーンへ進むかは、6R の後に決める。

## Open Questions

- 相談の型（事実→論点→叩き台→確認）の仮決めは5回まで。使った回: 4（論点 1〜3、4〜6、`review 消化` での代替案の比較）。5回目で判断する（`decisions.md` の同日の項。締めとケア9項目を足した）。
