# repeat_reads の基準値（PC2。2026-10-29）

`repeat_reads.py --since 2026-10-01 --detail 15` の出力（ee が PC2 で実行して貼った）。10-29 の縮小・分割の前後が混ざる。11-05 の再測定（`--since 2026-10-30`）の比較元にする。PC1 ではない（PC1 の room の会話記録は別。下の room は PC2 の WSL）。

## Windows（PC2）

- 会話 150 本、Read 1662 回、結果 5.29M 文字。全文読み 938 回（56%）・3.71M 文字（70%）。重複読み 213 回（12%）・0.52M 文字（10%）。
- 全文読みの拡張子: .md 3.49M、.py 130k、.ps1 66k。
- 全文読み md の上位（文字数 / 回 / 1 回あたり）:

| ファイル | 文字数 | 回 | 1回あたり |
|---|---|---|---|
| docs/log.md | 662,805 | 173 | 3,831 |
| workflow-kit/docs-rules.md | 304,816 | 27 | 11,289 |
| workflow-kit/commit-push-rules.md | 300,687 | 51 | 5,895 |
| workflow-kit/wrap-hook.md | 263,012 | 100 | 2,630 |
| workflow-kit/stock-hook.md | 144,564 | 17 | 8,503 |
| workflow-kit/hooks.md | 136,620 | 26 | 5,254 |
| workflow-kit/hook-common.md | 132,388 | 21 | 6,304 |

## room（PC2 の WSL）

会話 2 本、Read 7 回、28k 文字。件数が少なく基準にならない（hooks.md、brief-hook.md、ROOM.md、brief-work-types.md）。

## 読み取り

- 「1 回あたり」は縮小前後の混在。10-29 の縮小後の値（commit-push-rules 6.1k、log 2.5k、wrap-hook 2.7k）は、ここでは混ざって見える。wrap-hook の 2,630 は縮小後の値に近い（10-29 に縮小した読みが多い）。
- 縮小済みの 3 本の外に、`docs-rules.md`（11.3k/回、27 回）、`stock-hook.md`（8.5k/回）、`hook-common.md`（6.3k/回）、`hooks.md`（5.3k/回）が残る。回数 × 大きさで見ると、docs-rules が 3 位。次の縮小候補（節だけ読む運用か分割）。
- 総量では .md の全文読みが結果の 66%（3.49M / 5.29M）。
