# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%。キャッシュ読みを含む数かは確認しない（ee の決定 10-27）。切る目安は「作業の区切り、または 100k」。
- PC1 room の日ごと: 10-26 23.7M → 10-27 以降 約 7M。【仮 〜11-29】仕組みの効果とみなす（ee の見立て 10-29。作業量の裏づけなし）。土台 17.9k（Windows 側 27.8k）。60k 超はトークンの 74%（`records/2026-10-29-pc1-room-effect-and-requests.md`）。
- 依頼別の応答数: 平均 6.3、中央値 5。room では wrap 4.6、continue 10.8（トークンの 13%）、other の 101 文字以上が 74 件・41.3M。トークンの 76% は会話の途中の依頼（最初の依頼は応答 2 倍だが 24%）。Windows 側は `records/2026-10-28-requests-by-kind.md`。
- 傾向分析の骨子は `records/2026-10-27-trend-skeleton.md`（伸びの要因: Read 45%、書き込み 23%、Grep 10%）。room の 107k は判定済み（`records/2026-10-29-room-107k-judgment.md`）。
- 用語（ee と合意 10-28）: セッション = 会話、依頼 = テキスト入力から出力まで、応答 = モデルへの 1 回の呼び出し（並列は 1）。
- 解説は `guides/explain/claude-code-cost-session-size.md`。

## Next Actions

1. 【最優先・10-29 決定】NA 5 の (d)（全文読みを止める）の残り。上位 3 本の全文読み（`commit-push-rules.md`、`docs/log.md`、`wrap-hook.md`）は、すべて縮小・分割した（10-29。大きさは `records/2026-10-29-repeat-reads-2.md`）。残り（再測定は 11-05、期日は `docs/due.md`。ee の決定 10-29）: (1) Windows 側で `repeat_reads.py --since 2026-10-30 --detail`（分割後だけ）を実行し、3 本の 1 回あたり（commit-push-rules 6.1k、log 2.5k、wrap-hook 2.7k）が下がったかを見る。(2) 基準値は PC2 の Windows と WSL で取得済み（`records/2026-10-29-repeat-reads-baseline-pc2.md`。room は 2 本で基準にならない）。PC1 では未実行。縮小の次の候補: `docs-rules.md`（NA 9）、`stock-hook.md`（8.5k/回）。(4) 次に多い全文読み（`token-cap-start-here.md` 22 回、各トピックの `docs/log.md`）は、小さいので優先度は低い。
1b. 【仮説・検証は後日（ee、10-29）】「依頼の末尾に完了条件を 1 行足す（例「○○が△△になったら止める。それ以外は読まない」）と応答数が減る」（NA 5 の (f)）。足す依頼と足さない依頼を数件ずつ比べる（ee が実施。印は先頭に `[完了条件あり]`）。根拠: `--detail`（`records/2026-10-29-pc1-room-other-detail.md`）で重いのは 101-300 文字の途中の依頼（37%）。ee の確認: 場所は伝えている、ゴールは無い、依頼は指示型（「完了条件が無いと終わりを AI が決める」は仮説）。
2. 【10-29 測定済み・判定保留】`integrate` の上限（仮 〜11-29）の個別の効果。Windows 側（`requests_by_kind.py --csv`、10-01 以降）の integrate は 16 件。10-27 より前 13 件は応答 9.4・1 件 809k・ピーク平均 92k。10-27 以降は 3 件で応答 11.0・708k・ピーク 85k。うち 10-29 の 1 件は 7 応答でピーク 134k と 100k 超。件数が少なく、効果の有無は言えない。room 側（PC1）の件数は未確認。再測定は 1 週間あけて 11-05（期日は `docs/due.md`、ee の決定 10-29）。
3. （低優先）マクロ側の常駐文書に、全文読みを避ける指示を入れる案。
4. 土台の整理（`AGENTS.md` など）は、100k 運用の結果を見てから再判断する（`records/2026-10-26-base-trim.md`。ee の決定 10-27。再判断の前に、動かせる土台の内訳を測る。room の土台は 17.9k で、優先度は低い）。
5. **応答数を減らす（第一の角度。`docs/decisions.md`）**。手段（効く順の案）: (b) 出力の型を応答数の多い依頼へ広げる（room は wrap が 4.6 と小さく、continue と other が先）。 (c) 独立した読み書きを 1 応答にまとめる。 (d) 全文読みの連発と重複読みを止める（大きいものは節、小さいものは全文）。 (e) 編集後の確認だけの再読みをしない。 (f) 場所・ゴール・完了条件を依頼に書く（`guides/quickref/ai-work-prompts.md`）。 (g) 機械的な処理はスクリプトで 1 回にする。 (h) 探索を別エージェントに任せる効果を実測する。 (i) 聞き返しを減らす。注意: 1 応答で大量に読むと逆効果。「応答数 × 文脈の大きさ」の積で見る。
6. 【10-28 試験中】出力の型（`exmem/lessons/*-output.md` の 8 本）を実際の依頼で試す。見るもの: 誤爆、型の品質、開始時の大きさ（`cap_meter --latest`）。`methods.md` と `brief-hook.md` の構成変更に合わせ、`review` を勧める。
7. Zed の ACP が何を表示しているかを確定する（ee の決定 10-28。別セッション）。仮説は「直近の応答 1 回の入力の大きさ」。1 依頼の前後で表示の値を控え、`cap_meter --latest` と突き合わせ、ガイドの「基礎知識」に反映する。

8. 【ee 10-29】`wrap-hook.md` の見直しの効果の確認（反映は済。`records/2026-10-29-wrap-decompose.md`）。再測定は 11-05（期日は `docs/due.md`）。測定は `requests_by_kind.py --since 2026-10-30`（Windows 側）で、wrap の応答平均（8.3）と 1 件平均のトークンが下がったかを見る。書き漏れ・誤りが出ていないかも、`review` で見る。

9. 【起票 10-29】`workflow-kit/docs-rules.md`（11.3k/回、27 回）の分割を実施する（別セッション。ee の決定 10-29）。案: 1〜33 行と末尾の共通ルールを `docs-rules.md` に残す（1〜27 行は動かさない。各 `AGENTS.md` が `offset` 24 で読むため）。35〜75 行を `docs-format.md`（log.md / decisions.md の書式）、77〜91 行を `docs-carry.md`（知識にしたとき）に分ける。元の場所に 1 行の案内を残す。参照元は `files_with_matches` で洗い出して張り替える。`workflow-kit` の変更なので、実施前に ee の承認を得る。分割後の効果は 11-05 の再測定に含める。

## Open Questions

- Zed の System tools が 9.0k → 9.9k に増えた原因（再起動でも戻らず）。
- continue を細かい会話の切り方に多用すると、応答数は増えるがトークンは減るのか（room では応答の 23%・トークンの 13%。切る効果との差引は未算出）。
