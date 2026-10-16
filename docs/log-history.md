# 作業ログの経緯（log-history）

## Log

### 2026-10-16
- `docs/log.md` の Next Actions 3件を、ユーザーが完了と確認して消した。① 「push はユーザーが行う（許可リストなし）」: 同日に公開リポジトリのまま、エージェントが `main` に push してよいと決定済み（`decisions.md` の「cwd はリポジトリのトップだけ…」）。`git fetch` 後に `origin/main..HEAD` が空であることも確認した。② 「`guides/` の `CLAUDE.md` は本文を持つ」: `bda9216` で `AGENTS.md` へ改名し、`CLAUDE.md` は `@AGENTS.md` の1行になった。③ 「`handson/` は削除予定」: `8b9222f` で削除済み（`ad3e966` で README の行も除去）。Open Questions は元から「なし」。`decisions.md` の該当行に、変更後の状態を補足した。
- 3リポジトリ（works、resources、dotfiles）の cwd の扱いを揃えた。resources に `README.md`（窓口）と `docs/`（`log.md` `decisions.md` `log-history.md`）を新設し、`AGENTS.md` の「読む順番」を追加した。kit の `docs-rules.md` に「上の階層で起動して『〜の続き』と言われたら」を足し、`hooks.md` の「起動する場所（cwd）」はそこへのポインタに畳んだ。判断は `decisions.md` の「cwd はリポジトリのトップだけ…」。
