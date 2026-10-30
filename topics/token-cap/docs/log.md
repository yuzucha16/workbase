# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%。キャッシュ読みを含む数かは確認しない（ee の決定 10-27）。切る目安は「作業の区切り、または 100k」。
- PC1 room の日ごと: 10-26 23.7M → 10-27 以降 約 7M。【仮 〜11-29】仕組みの効果とみなす（ee の見立て 10-29。作業量の裏づけなし）。土台 17.9k（Windows 側 27.8k）。60k 超はトークンの 74%（`records/2026-10-29-pc1-room-effect-and-requests.md`）。
- 依頼別の応答数: 平均 6.3、中央値 5。room では wrap 4.6、continue 10.8（トークンの 13%）、other の 101 文字以上が 74 件・41.3M。トークンの 76% は会話の途中の依頼（最初の依頼は応答 2 倍だが 24%）。Windows 側は `records/2026-10-28-requests-by-kind.md`。
- 傾向分析の骨子は `records/2026-10-27-trend-skeleton.md`（伸びの要因: Read 45%、書き込み 23%、Grep 10%）。room の 107k は判定済み（`records/2026-10-29-room-107k-judgment.md`）。
- 用語（ee と合意 10-28）: セッション = 会話、依頼 = テキスト入力から出力まで、応答 = モデルへの 1 回の呼び出し（並列は 1）。
- Zed の Context 表示は直近の応答 1 回の入力の大きさ（10-29 確定）。費用の内訳（Sonnet 5.5 の定価で計算、この会話 13 応答）は、キャッシュ書き込みが 64%、読みが 23%、出力が 14%。大きなファイル・スキルを 1 回読む書き込みが 1 応答で会話の費用の約 4 割になった。Zed の Cost とは 20% 以内で合う（`records/2026-10-29-zed-cost-check.md`）。勤務先の上限がキャッシュ読みを数えるかは未確認のまま（ee の決定 10-27）。
- 全文読みの縮小（NA 5 の (d)）: 上位 3 本、`docs-rules.md`、`stock-hook.md` は縮小・分割済み（10-29。大きさは `records/2026-10-29-repeat-reads-2.md`）。効果の再測定は 11-05 で、`docs/due.md` に移した（ee の決定 10-29）。次に多い全文読み（`token-cap-start-here.md` 22 回、各トピックの `docs/log.md`）は小さく、優先度は低い。
- 相談の型の費用（10-29 測定）: 型の有無で事実集めの量は同じ。同じ 12 応答で型ありが +16.9%（差の大半は `decisions.md` を探す読みと、記録・push の規則書。`records/2026-10-29-consultation-pattern-cost.md`）。本文は `exmem/lessons/consultation-pattern.md` に移した。応答ごとの表は `decompose_session.py --steps --upto N`。
- 測定スクリプト 3 本（`requests_by_kind.py`、`repeat_reads.py`、`decompose_session.py`）は `workflow-kit/tools/` に移した（ee の決定 10-29。`topics/` は room にコピーされないため）。今後の token-cap のスクリプトも `workflow-kit/tools/` に作る。
- 解説は `guides/explain/claude-code-cost-session-size.md`。

## Next Actions

2. 【優先度低・10-29 測定済み・判定保留】`integrate` の上限（仮 〜11-29）の個別の効果。Windows 側（`requests_by_kind.py --csv`、10-01 以降）の integrate は 16 件。10-27 より前 13 件は応答 9.4・1 件 809k・ピーク平均 92k。10-27 以降は 3 件で応答 11.0・708k・ピーク 85k。うち 10-29 の 1 件は 7 応答でピーク 134k と 100k 超。件数が少なく、効果の有無は言えない。room 側（PC1）の件数は未確認。再測定は 1 週間あけて 11-05（期日は `docs/due.md`、ee の決定 10-29）。
4. 【優先度低】土台の整理（`AGENTS.md` など）は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`。ee の決定 10-27。再判断の前に、動かせる土台の内訳を測る。room の土台は 17.9k で、優先度は低い）。
5. **応答数を減らす（第一の角度。`docs/decisions.md`）**。手段（効く順の案）: (b)【優先度低】出力の型を応答数の多い依頼へ広げる（room は wrap が 4.6 と小さく、continue と other が先）。既存の 8 本は、文書を作る依頼（調査・計画・改善・振り返り）の章立て。重い other は、マクロ作業の途中の 101-300 文字・コードブロックなしの依頼で、型の対象が違う。continue は最初の依頼でトークン 13% と小さい。ee の回答（10-29）: (1) 依頼は細かく書いている（入力・出力ファイルの場所・構成・使い方、目的、チェックしたい項目）ので、(f) の余地は小さい。(2) 探索の読みは効いている（入力ミスの補正、追加提案）。いつかはマクロ作成作業を型にしたい。文字コード・スクリプトのナレッジは `exmem/lessons/excel-vba-ai-development.md` に揃っており、今後も使える。【10-30 方向決定】マクロ作業の型は `topics/office-output-types/` に引き継いだ（Excel 集約の基準文書の雛形と、人・AI・コードの分担。弱い点は同トピックの Open Questions に積んだ）。効果は PC1 で 1 回回した後に、応答数と 1 件のトークンで測る。この (b) には continue と other の一般の型だけを残す。 (c)【済 10-29】独立した読み書きを 1 応答にまとめる（`AGENTS.md` の「読み込みの量を抑える」に 1 行。ee の決定 10-29。効果は 11-05）。 (d) 全文読みの連発と重複読みを止める（大きいものは節、小さいものは全文）。 (e)【済 10-29】編集後の確認だけの再読みをしない（同じ節に 1 行）。 (f) 場所・ゴール・完了条件を依頼に書く（`guides/quickref/ai-work-prompts.md`）。 (g)【優先度低】機械的な処理はスクリプトで 1 回にする（型の設計と重なる）。 (h)【優先度低】探索を別エージェントに任せる効果を実測する（(c)(e) の結果を見てから）。 (i) 聞き返しを減らす。注意: 1 応答で大量に読むと逆効果。「応答数 × 文脈の大きさ」の積で見る。
6. 【優先度低・10-28 試験中】出力の型（`exmem/lessons/*-output.md` の 8 本）を実際の依頼で試す。見るもの: 誤爆、型の品質、開始時の大きさ（`cap_meter --latest`）。`methods.md` と `brief-hook.md` の構成変更に合わせ、`review` を勧める。
9. 【採用済み 10-30・効果の確認待ち】規則書（`commit-push-rules.md`、`push-rules.md`）をコミット・push の直前に読む。`exmem/lessons/consultation-pattern.md` に反映した（`AGENTS.md`・`wrap` は元から直前に読む書き方で、変更なし）。見込みは約 19k 文字分の読み直しの減（概算。キャッシュ読みを上限が数えるかは未確認）。次: 次の相談の型の会話で `decompose_session.py --steps --upto N` を使い、規則書を読んだ応答の番号がコミット・push の直前かを確かめる。
8. 【優先度低・ee 10-29】`wrap-hook.md` の見直しの効果の確認（反映は済。`records/2026-10-29-wrap-decompose.md`）。再測定は 11-05（期日は `docs/due.md`）。測定は `requests_by_kind.py --since 2026-10-30`（Windows 側）で、wrap の応答平均（8.3）と 1 件平均のトークンが下がったかを見る。書き漏れ・誤りが出ていないかも、`review` で見る。


## Open Questions

- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
- 切る目安を 100k から 60k に下げるか: 100k のまま（ee の決定 10-30）。いま具体化しても効果は薄いので、データがそろってから全体を見て決める。10-29 の算出: ピーク 60〜100k の依頼は 1 件 537k で、〜60k の 169k の 3 倍（`records/2026-10-29-continue-split-effect.md`。切る回数が増える費用との差引は、同じ作業の比較ではないので確定しない）。
