# 作業ログ（log）

計画と部屋の紐付け（`start 計画` の出力と、`room init` / `room open` が作る README の関連付け）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. 論点 1〜3 は仮に決まった（本体は `ai/in/plan/`、案 A、日付は本文。`decisions.md`）。印の範囲は新しい節「計画」だけ（案1）。論点 4（Area は触らない）と 6（雛形に空の節、既存は手で貼る）も仮に決まった。論点 5 と `readme-block.md` の形（3.7）も、ユーザーが了承した。論点 1〜6 は仮に出そろった。
2. 決まったら、`start 計画` で、この題材の 6R を作るか決める（作るなら出力は `records/`。`topics/AGENTS.md` の仕訳）。
3. （済 2026-10-21）実装の範囲をユーザーが確認し、root の `docs/log.md` の Open Questions に1件置いた。次は `review 消化`（待ち行列 → スクリーニング → 最終判断）。通ったら実装する（`room.py`、雛形、案内、テスト）。
4. 仕組みの変更（`open` は触らないという 2026-10-19 の取り決めの見直しを含む）は、`review 消化` の3段で承認してから、kit と `room.py` に反映する。

## Open Questions

- 相談の型（事実→論点→叩き台→確認）の仮決めは5回まで。使った回: 3（論点 1〜3、4〜6。同じ相談の続きは数え直さない）。5回目で判断する（`decisions.md` の同日の項）。
- `start-plan.md` の「参照用の計画は Area 配下」は、置き場が無く食い違う（issues の 3 章）。直し方は、論点 4（Area の README）と一緒に決める。
