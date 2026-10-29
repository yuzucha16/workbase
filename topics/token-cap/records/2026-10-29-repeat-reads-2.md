# 全文読みの再測定と、log.md・wrap-hook.md の縮小（2026-10-29）

`python -I topics/token-cap/repeat_reads.py --since 2026-10-27 --detail 15`（Windows 側。大きさは Read の結果の文字数）。縮小の前の値。

- Read 472 回・1,180,449 文字。全文読み 264 回（55%）・849,177 文字（72%）、その 96% が md。重複読み 42 回（8%）・86,606 文字（7%）。
- 全文読みの md 上位: `commit-push-rules.md` 249,995（39 回、1 回 6,410。分割前の読みを含む）、`docs/log.md` 147,111（57 回、2,580）、`wrap-hook.md` 102,313（37 回、2,765）、`token-cap-start-here.md` 22,670（22 回）。

## 縮小（同日）

| ファイル | 前 | 後 | 方法 |
|---|---|---|---|
| 直下 `docs/log.md` | 3,973 | 2,449 | トピック固有の Next Actions を外し（トピックの `docs/log.md` だけが持つ）、NA 9・10・13 を短くした |
| `wrap-hook.md` | 2,963 | 2,637 | 重複の説明を削り、手順 1 のまれな分岐を `wrap-targets.md` に分けた |

`wrap-hook.md` は元が小さく、効果は 1 回あたり 約 330 文字。直下 `docs/log.md` が効く。決定は `docs/decisions.md`（2026-10-29 の 2 項）。

## 確かめ方

翌週に同じコマンドを実行し、`commit-push-rules.md`（核 3,100）、`docs/log.md`（2,449）、`wrap-hook.md`（2,637）の 1 回あたりが下がったかを見る。
