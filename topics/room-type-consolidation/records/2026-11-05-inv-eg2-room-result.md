# inv eg2(room 版)の結果(2026-11-05)

依頼文と観点は `2026-11-05-inv-eg2-room-request.md`。部屋 `room-myenv`(internal)、Project `sample_inveg2`。人の手順の代わりにエージェントが `mask` → `start --adopt --cmd`(`claude -p`。方法は `2026-11-05-inv-combo-test-result.md` の「起動の注意」と同じ)→ `restore` を実行した。所要は部屋の AI が約 25 分(自己申告)。

## 観点ごと

1. 聞き返し: 0。仮定を `question.md` と `report.md` の冒頭に書いた(部屋なしと同じ)。
2. 置き場: 迷いなし。`ai/out/sample_inveg2/`、スクリプトは `ai/work/scripts/analyze.py`、計算出力は `ai/work/analysis_out.txt`。報告の根拠が `work/` を指す形になった(AI の指摘 4)。
3. 落とし穴: P1〜P10 で、0A・0B、沖縄 1945 の「-」、末尾の注 2 行、先頭 0 を発見し、1960 年の差 73 人まで注 2 と突合した。**cp932 は消えた**: `mask` が UTF-8(BOM つき)に変換し(55,038 → 60,225 バイト)、AI は BOM だけを落とし穴にした。
4. 道具: 標準の Python で足りた。表計算ライブラリは使わず。
5. internal の流れ: `mask` は cp932 を通した(語が空なので置換 0)。`start --adopt` は一度で通った。止まった点: `close` が非対話(エージェント実行)では警告を承知できず止まる。警告は、README がひな形のまま、`ai/out/close.md` が無い、の 2 点。`close` は未実行、人が端末から `y` で行う。`restore` は成功(Area の `deliverable/sample_inveg2` に 8 ファイル)。
6. 数字: 一致(2010 年が最大 128,057,352 人、2010→2015 に 39 県減・8 都県増、東京圏 28.43%)。

## 構成の使い方

作った: `question.md` `sources/sources.md` `findings/`(4 ファイル) `checks/checks.md` `report.md`。作らなかった: `publish/`(頼んでいない)。部屋なしと同じ構成で、過不足なし。

## 指摘(AI の提案 5 点 + こちらの所見)

- AI: 落とし穴を集める工程の入口に置く / 情報源が少ないとき `sources.md` 1 本でよい / findings を出力から自動生成 / 根拠の計算出力の置き場 / 仮定は現行で足りる。うち 1 と 4 は部屋なし版の指摘(置き場の未決)と重なる。
- `close` の警告のうち README のひな形は、試験では毎回出る(Project を実際に使うなら README を書く)。`close.md` は部屋の AI が書かなかった(依頼文に無い)。
- 反映は未決。人の判断を待つ。
