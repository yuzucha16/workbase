# 作業ログ（log）

計画と部屋の紐付け（`start 計画` の出力と、`room init` / `room open` が作る README の関連付け）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`。リポジトリ全体の状態は workbase 直下の `docs/log.md`。

## Next Actions

1. 論点 1〜3 は仮に決まった（本体は `ai/in/plan/`、案 A、日付は frontmatter。`decisions.md`）。次は、frontmatter の項目名とマイルストーンの入れ方、`readme-block.md` の形（印つきの範囲、6R の分解の書き方）。
2. 決まったら、`start 計画` で、この題材の 6R を作るか決める（作るなら出力は `records/`。`topics/AGENTS.md` の仕訳）。
3. 論点 4〜6（Area の README、`open` の前に作った計画、雛形の変更）を決める。
4. 仕組みの変更（`open` は触らないという 2026-10-19 の取り決めの見直しを含む）は、`review 消化` の3段で承認してから、kit と `room.py` に反映する。

## Open Questions

- 相談の型（事実→論点→叩き台→確認）の仮決めは5回まで。使った回: 2（論点 1〜3 の相談。同じ相談の続きは数え直さない）。5回目で判断する（`decisions.md` の同日の項）。
- `start-plan.md` の「参照用の計画は Area 配下」は、置き場が無く食い違う（issues の 3 章）。直し方は、論点 4（Area の README）と一緒に決める。
