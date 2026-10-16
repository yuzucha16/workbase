# 作業ログ（log）

`workbase`（共有ナレッジと共通機能）全体の現在状態と次にやること。トピックの中身は各トピックの `docs/`。作業の終わりに Next Actions と Open Questions を更新し、経緯は `docs/log-history.md` の `## Log` の先頭に足す。判断の根拠は `docs/decisions.md`。

## Next Actions

- push はユーザーが行う（許可リストなし）。未 push のコミットは `git log origin/main..HEAD` で確認する。
- `guides/` の `CLAUDE.md` は本文をそのまま持つ。cwd を増やさない方針なので、いまは触らない（`AGENTS.md` へ移して `CLAUDE.md` を1行にするのは後回し）。
- `handson/` は削除予定。そのままにする。

## Open Questions

なし
