# 作業ログの経緯（log-history）

## Log

### 2026-10-16
- 3リポジトリ（works、resources、dotfiles）の cwd の扱いを揃えた。resources に `README.md`（窓口）と `docs/`（`log.md` `decisions.md` `log-history.md`）を新設し、`AGENTS.md` の「読む順番」を追加した。kit の `docs-rules.md` に「上の階層で起動して『〜の続き』と言われたら」を足し、`hooks.md` の「起動する場所（cwd）」はそこへのポインタに畳んだ。判断は `decisions.md` の「cwd はリポジトリのトップだけ…」。
