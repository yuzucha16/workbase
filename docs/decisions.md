# 判断の記録（decisions）

## Principles

## Decisions

### 【汎用】cwd はリポジトリのトップだけにし、下位は「<名前> の続き」で扱う（2026-10-16）
- 決めたこと: 起動する単位は works、resources、dotfiles のトップの3つだけ。下位の単位は cwd を増やさない。3つの `AGENTS.md` の「読む順番」を同じ文面にし、「続き」の規則は kit の `docs-rules.md` に1か所で定める。resources 直下にも `README.md`（窓口）と `docs/` を置く。
- 根拠: ユーザーが方針を承認した（シンプルでわかりやすい。cwd を増やすと忘れる）。
- `topics/kit-growth/docs/` は kit 改善の受け皿として維持する。resources 直下の `docs/` は、resources 全体の状態と、トピックに属さない変更に限る（ユーザーが推奨案を承認）。
- `guides/` は触らない。`handson/` は削除予定でそのまま（ユーザー）。
- `.claude/` の扱い（ユーザーの決定。実害が出たら個別に直す）: `settings.local.json` は全リポジトリで追跡しない。`settings.json` は、固有の規則が要るリポジトリだけ置く（works のみ。`projects/` `areas/` `archives/` の Read/Edit の deny）。dotfiles の `.gitignore` は `.claude/` 全体から `settings.local.json` だけに変えた。プロジェクト設定は親から子へ継承されない（公式ドキュメントと issue の報告。works の設定は works のトップで起動したときだけ効く）。
- → kit/docs-rules.md

## Gotchas
