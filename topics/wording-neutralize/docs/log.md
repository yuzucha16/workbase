# 作業ログ（log）

公開リポジトリから環境を特定する表現を、性質で書く表現にする取り組みの現在状態。段階 1〜3 は適用済み（2026-10-28）。PC1 側の未コミットの 5 件と同じファイル（`obsidian-vault-backup.md`）に触れたので、PC1 で pull するときに衝突しうる。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`、分析の全文は `records/2026-10-27-impact-analysis.md`。

## Next Actions

- 【起票 10-27】段階 4（履歴の書き換え）: ユーザーが後日行う。急がない。置換語と他の clone の扱いは Open Questions。

## Open Questions

- 段階 4（履歴の書き換え）の置換語は「勤務先」を既定にした（10-28）。法人格の語と Office の「会社」プロパティを巻き込まない置換の方法を、段階 4 の前に決める。急がない。
- 段階 4 の前に、他の clone（PC2、WSL の部屋、`works_sub*`）をどう作り直すか。force の deny は、実行時に人が切る。
