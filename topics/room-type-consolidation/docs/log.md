# 作業ログ（log）

type 集約（`dev` と `inv`）は実装済み。続きは `dev-deliverable-guide.md` の見直し。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【起票 10-24】`dev-deliverable-guide.md` の見直し: 構成要素の選び方（`src/` `env/` `tests/` `tools/` `docs/`）で組み直す。`env/` と `tests/` だけの成果物の節は、差分でなく選び方にする。文書だけの `dev`（`docs/` だけ）と、`inv` の基準文書の形（`open-hook.md` の未決）も合わせて見る。ユーザーが、区分が明文化された後にやると希望（10-24）。

## Open Questions

- `inv` と、`dev` の構成要素（`env/`、`tests/` だけ）の実測が無い。最初の利用の後に見直す。
- 既存の Project の README の旧 type 値（`doc` `dev-env` など）は、そのまま。読むコードが無いので影響なし。
