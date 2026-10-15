# AGENTS.md（topics）

大きな取り組み（トピック）の置き場。入口は `topics-index.md`。

## 「<トピック名> の続き」と言われたら

1. `<トピック>/` の窓口（`*-start-here.md`、無ければ `*-handover.md`）を読む。
2. `<トピック>/docs/log.md`（現在状態と次の一手）を読む。開始時に読むのはここまで。
3. `docs/decisions.md` は、何かを決める・変える前に検索する。`docs/log-history.md` と `notes/` は、必要なときだけ読む。

## 書くとき

- 状態は `docs/log.md` だけに置く（窓口には「いま」の1行だけ。ほかに写さない）。予算: 窓口 2KB、`log.md` 4KB。
- 決定は `docs/decisions.md`（ユーザーの発言を根拠に）。経緯は `docs/log-history.md`。
- 反映が済んだトピックは close して削除する（履歴は git）。
