# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。最初の実利用（`sample_dev` と `sample_inv`）の観察を受け、手順書を直した（2026-10-25）。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【済 10-25】`report.md` の置き場: コードは `ai/out/deliverable/` だけ Area に、それ以外は `_noai/final/` に戻す。食い違いは `methods.md` の書き方だけだったので、`ai/out/<成果物名>/report.md` に直した。決定は要らなかった。
- 【済 10-25】単一の問いの章立て（`brief-hook.md`、`research-method.md`）。
- 【起票 10-25】`dev` の「テスト」の節に、文書と実装の食い違いを機械で検査する型（`sample_dev` の `tests/test_docs.py`）を足すか決める。
- 【起票 10-25】`dev-deliverable-guide.md:78` の旧名（`dev-env` `dev-test`）の説明を、削るか残すか。
- 【起票 10-25】`brief-work-types.md` の「文書作成」の項（`docs/` だけの `dev`）を、使わない見込みなので残すか見直す。

## Open Questions

- `env/` だけ、`tests/` だけの成果物の実測が無い。最初に使うときに測る。
- 成果物の形を AI が決める場面（依頼で指定が無いとき）は、まだ起きていない。
- `inv` の基準文書は仮決め（問い＋完了条件の 1 行）。複数の問いの調査で見直す。
- 既存の Project の README の旧 type 値（`doc` `dev-env` など）は、そのまま。読むコードが無いので影響なし。
