# inv: 「quarto/revealjs で」と明示した試験の結果（2026-11-06）

pptx 追試（`2026-11-05-inv-pptx-explicit-result.md`）の続き。部屋 `room-myenv`（internal）、Project `sample_invQ`（`--type inv`）、`room start --cmd` で `claude -p`（方法は `2026-11-05-inv-combo-test-result.md` の「起動の注意」と同じ）。

依頼: 「Marp・Slidev・Quarto のどれでスライドを作るのがよいか、選び方を調べて。報告資料にして、quarto/revealjs で。確認できない点も明記して。」（pptx 追試と同じ題材。重さの言葉だけ変えた）

## 結果

- 終了コード 0。聞き返し 0。`quarto` は部屋にあり、html まで描画できた。
- 作った: `slide-tool-selection.qmd`（5.9KB）と `slide-tool-selection.html`（3.9MB、`embed-resources: true`、10 枚）。置き場は `ai/out/sample_invQ/` の直下。
- 作らなかった: `report.md` `question.md` `sources/` `findings/` `checks/` `publish/`。
- 質: スライド内に「未確認」の項目と根拠 URL の一覧がある（`.qmd` 冒頭の結論と末尾の一覧）。

## 指摘

1. 清書物が `publish/` でなく工程の親（`ai/out/<Project>/`）の直下に出た。pptx 追試（`publish/` に出た）と違う。成果物がスライドだけなので、報告本体（`report.md`）が無く、問い・仮定も残らない。`project-structure.md` の `inv` の規則が「清書は `publish/`」と読めるか、見直す余地がある。
2. 根拠・未確認はスライドの中に入り、`sources/` `findings/` に分かれなかった。軽い依頼なら許容だが、後で見返す用途には足りない。
3. 3.9MB の html は一枚で共有しやすい（pptx の `deck.js` のような再実行の手間が無い）。

## 反映（案。ユーザーの承認待ち）

`guides/quickref/ai-work-prompts.md` の清書の行に「quarto/revealjs で」を足す。足すなら「`publish/` に置いて、`report.md` も付けて」と添える（添えないと直下に出る）。
