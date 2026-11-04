# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認と置き場の実測、Vault 2 分割の両 PC 確認を済ませ、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用し、eg1（Web）の実験で構造を直した。同日、Marp・Slidev・Quarto の実機比較（`records/2026-11-04-slide-tools-live-compare.md`）と、`init` への Marp CLI の追加（段 `marp`、実機確認済み）も済んだ。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【期日 11-11、起票 11-04】`inv` の工程別構造の実験 eg2（社内の Excel・テキスト。マスクの差分）を、別セッションで行う。結果は `records/` に残し、構造を直す。
- 【期日 11-11、起票 11-04】`inv` の工程の組み合わせ試験(`dev` の a) `src` のみ、b) `env`+`src`、c) `src`+`env`+`tests` と同じ形)。工程(`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`)を、a) 少ない組み合わせ、b) 中間、c) 全部、のように変えて部屋に渡し、置き場などの観点(`ai/out/<成果物名>/` の下の置き場、聞き返し、`dev` との差)でフィードバックを見る。設計(組み合わせの決め方と観点)は着手時に決める。eg2 とは別に、eg2 の結果(社内 Excel・テキスト)を受けて行ってよい。

## Open Questions

- （なし）
