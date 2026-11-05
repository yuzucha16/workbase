# inv: 「pptx で」と明示した試験の結果（2026-11-05）

C の追試（`2026-11-05-inv-combo-test-result.md` の指摘 1）。部屋 `room-myenv`（internal）、Project `sample_invP`（`--type inv`）、`room start --cmd` で `claude -p`（方法は同結果の「起動の注意」と同じ）。

依頼の【重さ】だけを「報告資料にして、pptx で。確認できない点も明記して」に変えた（題材は Marp・Slidev・Quarto の選び方。既存の比較結果は見せない）。

## 結果

- 作った: `report.md` `sources/sources.md` `findings/findings.md` `publish/sample_invP.pptx`（5 枚）と生成スクリプト `publish/deck.js`。すべて `ai/out/sample_invP/` の下（`out/` と読み替え）。
- 作らなかった: `question.md`（問いと仮定は `report.md` 冒頭）、`checks/`（未確認が 5 項目ほどで `report.md` に記載）。
- 聞き返し 0。`publish/` は「pptx で」の明示で作られた（前回 C は明示なしで作られなかった）。
- 質: Slidev は未実測と明記、Marp の編集版は部屋で 150 秒打ち切りで未確認と明記。

## 指摘

1. `deck.js` は pptxgenjs を `/tmp` に入れて動かしたため、再実行には入れ直しが要る（部屋に無い）。`init` の段に入れるかは未決。
2. `ai/` が無い読み替えは今回も（既知）。
3. 後始末: `room umount --area myenv` が、別 Project `sample_inveg1` の古いマウントで失敗した（今回の分ではない）。人が確認する。

## 反映

`guides/quickref/ai-work-prompts.md` の清書の行に「pptx で」を追記した。
