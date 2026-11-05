# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認と置き場の実測、Vault 2 分割の両 PC 確認を済ませ、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用し、eg1（Web）の実験で構造を直した。同日、Marp・Slidev・Quarto の実機比較（`records/2026-11-04-slide-tools-live-compare.md`）と、`init` への Marp CLI の追加（段 `marp`、実機確認済み）も済んだ。11-05 に組み合わせ試験（A 少・B 中・C 全部。置き場・組み合わせ・聞き返しは良好）と eg2（国勢調査 CSV を社内 Excel に見立てた分析。部屋なし、マスクは不要と判断）を行い、結果（`records/2026-11-05-inv-eg2-population-csv.md`）を受けて `project-structure.md` に 4 点（`checks/` の取り込みの落とし穴、台帳の URL 無しの書き方、スクリプトの置き場と仮定の書き方）を反映した。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## 11-05 追記

「pptx で」を明示した追試を実施。`publish/` に pptx が出た（`records/2026-11-05-inv-pptx-explicit-result.md`）。quickref に反映済み。

## Next Actions

- 【期日 11-12、起票 11-05】eg2 の room 版（myenv・internal・`sample_inveg2`。同じ c01.csv）を人が部屋で行い、返答と `ai/docs/inv-log.md` を別セッションで見せる。手順と依頼文と比べる観点は `records/2026-11-05-inv-eg2-room-request.md`。結果は部屋なし（`records/2026-11-05-inv-eg2-population-csv.md`）と比べて `records/` に残す。
- 【人の確認】`room umount --area myenv` が `sample_inveg1` の古いマウントで失敗した。確認して外す。

## Open Questions

- （なし）
