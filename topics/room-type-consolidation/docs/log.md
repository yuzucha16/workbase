# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認と置き場の実測、Vault 2 分割の両 PC 確認を済ませ、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用し、eg1（Web）の実験で構造を直した。同日、Marp・Slidev・Quarto の実機比較（`records/2026-11-04-slide-tools-live-compare.md`）と、`init` への Marp CLI の追加（段 `marp`、実機確認済み）も済んだ。11-05 に組み合わせ試験（A 少・B 中・C 全部。置き場・組み合わせ・聞き返しは良好）と eg2（国勢調査 CSV を社内 Excel に見立てた分析。部屋なし、マスクは不要と判断）を行い、結果（`records/2026-11-05-inv-eg2-population-csv.md`）を受けて `project-structure.md` に 4 点（`checks/` の取り込みの落とし穴、台帳の URL 無しの書き方、スクリプトの置き場と仮定の書き方）を反映した。同日、依頼に「pptx で」と明示すると `publish/` に pptx が出ることを確認し（`records/2026-11-05-inv-pptx-explicit-result.md`）、quickref に反映した。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【起票 11-05】`dev`・`inv` とも、1 つの Project で複数の工程を行いたく、かつ 1 回のプロンプトで終わらせず分割して進めたいとき、初手のプロンプトをどう書くかを試験する(工程の区切りの伝え方、2 回目以降の続け方、`ai/docs/` の記録で引き継げるか、`close` までの扱い。方法は `records/` に設計を置いてから)。
- 【起票 11-05】eg2 room 版の指摘 5 点(落とし穴の置き場、`sources.md` 1 本、findings の自動生成、計算出力の置き場、仮定)を `project-structure.md` に反映するか、ユーザーが決める。結果は `records/2026-11-05-inv-eg2-room-result.md`。
- 【起票 11-05】「pptx で」と同じように「quarto/revealjs で」と明示したとき、簡易スライド(`publish/` の html)を作るかを見る。方法は `records/2026-11-05-inv-pptx-explicit-result.md`(重さの言葉だけ「報告資料にして、quarto/revealjs で」に変える。`quarto` が部屋にあるかも見る)。うまくいけば quickref の清書の行に足す。
- 【人の確認】`room umount --area myenv` が `sample_inveg1` の古いマウントで失敗した。確認して外す。

## Open Questions

- （なし）
