# 作業ログ（log）

type 集約（`dev` と `inv`）は済み（2026-10-24）。10-31 に room の GitHub 認証と cwd（案 A）を確認し、11-01〜02 に Obsidian の Vault の 2 分割を実装した。11-04 に案 A の実機確認と置き場の実測、Vault 2 分割の両 PC 確認を済ませ、`inv` を工程別（`question.md` `sources/` `findings/` `checks/` `report.md` `publish/`）にする素案を採用し、eg1（Web）の実験で構造を直した。同日、Marp・Slidev・Quarto の実機比較（`records/2026-11-04-slide-tools-live-compare.md`）と、`init` への Marp CLI の追加（段 `marp`、実機確認済み）も済んだ。11-05 に組み合わせ試験（A 少・B 中・C 全部。置き場・組み合わせ・聞き返しは良好）と eg2（国勢調査 CSV を社内 Excel に見立てた分析。部屋なし、マスクは不要と判断）を行い、結果（`records/2026-11-05-inv-eg2-population-csv.md`）を受けて `project-structure.md` に 4 点（`checks/` の取り込みの落とし穴、台帳の URL 無しの書き方、スクリプトの置き場と仮定の書き方）を反映した。11-06 に分割して進める試験(dev・inv とも 6 回)を行った。同日、依頼に「pptx で」と明示すると `publish/` に pptx が出ることを確認し（`records/2026-11-05-inv-pptx-explicit-result.md`）、quickref に反映した。経緯は `docs/log-history.md`、根拠は `docs/decisions.md`。

## Next Actions

- 【起票 11-06、期日 11-13】`room start` の後にマウントが残り、次の `room start` が「マウントが残っている」で止まる。ユーザーの所見: Zed の remote server がプロセスをつかんでいる可能性があり、`room start` を解除したあと Zed を再起動すると直る。確かめる(Zed を閉じた状態で `start` を繰り返し、残るかを見る)。原因が Zed なら、`room/README.md` か `ai-room-lifecycle.md` に「止まったら Zed を再起動」と書く。`umount` の案内文に足すかも決める。
- 【起票 11-05、試験済み 11-06】「quarto/revealjs で」の追試は済み(`records/2026-11-06-inv-quarto-explicit-result.md`。`.qmd` と html が出たが `publish/` でなく `out/` 直下で、`report.md` なし)。quickref の清書の行に足すか(「`publish/` に置いて `report.md` も付けて」と添える案)を、ユーザーが決める。

## Open Questions

- （なし）
