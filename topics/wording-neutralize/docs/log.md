# 作業ログ（log）

公開リポジトリから環境を特定する表現を、性質で書く表現にする取り組みの現在状態。影響分析と方針の決定まで済み（2026-10-27）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`、分析の全文は `records/2026-10-27-impact-analysis.md`。

## Next Actions

- 【起票 10-27】段階 1: コマンド例など約 12 か所（8 ファイル）と、`room.py` のヘルプ文、`guides/howto/*` を性質で書き直す。先に行単位の差分案を出し、ユーザーが確認してから適用する。未コミットの 5 件（`exmem/lessons/obsidian-vault-*.md` など）には触れない。
  - 【10-28】差分案を出した（群 A: 段階 1 の本体、群 B: `guides/explain/` の 2 本と索引ほか。18 ファイル・75 行。公開を避けて project files の `notes/wording-neutralize/` に置いた）。適用した状態で room のテスト 150 件と `--check-triggers` が通った。**ユーザーの確認待ち**（A だけか、A と B か）。確認後は、パッチを `git apply` で当て、テストを再実行してから push する。PC1 側の未コミットの 5 件と同じファイル（`obsidian-vault-backup.md`）に触れるので、PC1 で pull するときに衝突しうる。
- 【起票 10-27】段階 2: `AGENTS.md` ほかの規則の文言を、禁止範囲を変えずに書き直す。公開前の検索（`commit-push-rules.md` の push の条件 4）に、対象語を足すかを決める。
  - 【10-28】書き直しの案と、決めること 2 点（PC1 の定義の 1 行を `README.md` に足す、公開前の検索に対象語を足す。どちらも推奨は「足す」）を、段階 1 の差分案と同じファイルに出した。ユーザーの判断待ち。

## Open Questions

- 段階 4（履歴の書き換え）で、対象語を何に置換するか。中立な 1 語にする案。急がない。
- 段階 4 の前に、他の clone（PC2、WSL の部屋、`works_sub*`）をどう作り直すか。force の deny は、実行時に人が切る。
