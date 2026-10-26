# skills の整理の実測（2026-10-27）

Zed の `/context` と `/skill-doctor` の値。Claude Code 端末の値は参考（ee は端末を使わない）。

## 手順

1. claude.ai の Customize > Skills で、同期の skills を個別にオフにする（設定の「クラウドでコードを実行」は前提のスイッチで、個別ではない）。
2. Claude Code の obsidian プラグイン（`obsidian@obsidian-skills`）を `/plugin` で uninstall する（claude.ai 側に別の登録が残って表示されることがある）。
3. 新しいスレッドで `/context` を見る（既存のスレッドは古い一覧のまま）。`/skill-doctor` が skill ごとの文字数（context）と使用回数を出す。Zed に `/skills` は無い。

## 実測

| 時点 | Skills | System tools | 合計（Zed） |
|---|---|---|---|
| 10-26 | 5.8k | 7.6k | 19.4k |
| 前半 5 件を切った後 | 4.5k | 9.0k | 19.7k |
| 第 1 段階（4 件）の後 | 3.5k | 9.9k | 19.7k |

- 1 件あたり 約 0.15〜0.34k（`/skill-doctor`）。切った 9 件で 約 2.3k。
- 切った 9 件は、いずれも使用 0 回。
- 残した 4 件: `xlsx` 320、`docx` 320、`pptx` 330、`pdf` 150（トークン）。
- System tools の +2.3k は、ハーネス側の変動とみる。`/reload-skill` の後に 9.9k になり、Zed の再起動でも戻らなかった。

## 結論

skills の整理は 2.3k 減（土台の約 12%）。ただし合計は System tools の増加で打ち消され、土台は 19.7k のまま。月の使用量への効きは小さい。効果の本命は、60k で切る運用。
