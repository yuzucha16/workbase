# 作業ログ（log）

公開リポジトリから環境を特定する表現を、性質で書く表現にする取り組みの現在状態。影響分析と方針の決定まで済み（2026-10-27）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`、分析の全文は `records/2026-10-27-impact-analysis.md`。

## Next Actions

- 【起票 10-27】段階 1: コマンド例など約 12 か所（8 ファイル）と、`room.py` のヘルプ文、`guides/howto/*` を性質で書き直す。先に行単位の差分案を出し、ユーザーが確認してから適用する。未コミットの 5 件（`exmem/lessons/obsidian-vault-*.md` など）には触れない。
- 【起票 10-27】段階 2: `AGENTS.md` ほかの規則の文言を、禁止範囲を変えずに書き直す。公開前の検索（`commit-push-rules.md` の push の条件 4）に、対象語を足すかを決める。

## Open Questions

- 段階 4（履歴の書き換え）で、対象語を何に置換するか。中立な 1 語にする案。急がない。
- 段階 4 の前に、他の clone（PC2、WSL の部屋、`works_sub*`）をどう作り直すか。force の deny は、実行時に人が切る。
- `lessons/` の `triggers:` に対象語を含むノートがあるか（置換前に `find_knowledge.py --check-triggers` で確かめる）。
