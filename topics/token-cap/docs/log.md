# 作業ログ（log）

`token-cap`（職場の月次上限に向けたトークン削減の見直し）の現在状態と次にやること。経緯は `docs/log-history.md`、判断の根拠は `docs/decisions.md`、出力は `records/`。

## 状態

- 上限は月 2億トークン。勤務先の表示は 26 日で 90%。キャッシュ読みを含む数かは確認しない（ee 10-27）。切る目安は「作業の区切り、または 100k」（100k 維持。ee 11-01）。
- 用語（ee 10-28）: セッション = 会話、依頼 = テキスト入力から出力まで、応答 = モデルへの 1 回の呼び出し（並列は 1）。
- 効果確認（`records/2026-11-05-pc2-windows-effect.md`、`records/2026-11-06-pc1-room-effect.md`）: PC2 は 1 件 574k → 323〜384k、ピーク 89k → 55〜65k。PC1 room はピーク 86k → 51〜58k、1 件 436k → 371〜420k（−4〜15%。応答が 5.8 → 6.8〜7.8 に増えた）。応答の中央値は 5 で不変、21 以上の 6 件（7.5%）がトークンの 42%。測定の期日項目は閉じた。測るのは主戦場のみ（PC1 = room、PC2 = Windows。ee 11-05）。
- 応答 21 以上の尾（NA 8）: Bash の直列が原因で、`AGENTS.md` に「読みの Bash は連結する」を足した（11-06）。効果は次回の `requests_by_kind.py`（PC1 に期日は足さない）。
- continue の増加は重い作業が原因（`records/2026-11-05-continue-growth-cause.md`）。全文読みの縮小は 10-29 に済み（`records/2026-10-29-repeat-reads-2.md`）。
- 費用の内訳（`records/2026-10-29-zed-cost-check.md`）: キャッシュ書き込み 64%、読み 23%、出力 14%。大きなファイル・スキルを 1 回読む書き込みで 1 応答が会話の費用の約 4 割。解説は `guides/explain/claude-code-cost-session-size.md`。
- そのほかの記録: 傾向 `records/2026-10-27-trend-skeleton.md`、room の 107k `records/2026-10-29-room-107k-judgment.md`、相談の型の費用（+16.9%）`exmem/lessons/consultation-pattern.md`。
- 測定スクリプトは `workflow-kit/tools/`（`requests_by_kind.py`、`repeat_reads.py`、`decompose_session.py`、`subagent_cost.py`）。今後のスクリプトもここに作る。
- ツールの理解ガイド（NA 10 close）: `exmem/inbox/2026-11-06-claude-code-tools-explain.md`（未追跡。別セッションで integrate する。ee の指示）。

## Next Actions

期日つきの測定（11-10: 全文読みの縮小、wrap-hook の見直し、AGENTS.md の 2 行。11-11: integrate の上限の効果）は `docs/due.md` に移した（ee 10-30）。優先度（ee 承認 10-30）: 高 = 5 の (c)(d)(e)（反映済み）の効果・wrap-hook の効果（いずれも期日か次の会話待ち）。中 = 6・integrate の効果。低 = 4。5 は手段ごとに分解済み（g > h > b > i。下の 5 に優先を書いた）。
5. **応答数を減らす（第一の角度。`docs/decisions.md`）**。元の長文は `records/2026-11-06-na5-original-text.md`。11-06 に手段ごとに分解し、5f を close、5i を omit した（`docs/log-history.md`）。残りの優先は g > h。注意: 1 応答で大量に読むと逆効果。「応答数 × 文脈の大きさ」の積で見る。
   - 5g 【優先: 高。仕込み済み・効果測定待ち。期日 11-13】機械的な処理（承認・close・omit のまとめ返答）を `workflow-kit/tools/na_apply.py` で 1 回にする（11-02 導入。`docs-write-rules.md`）。測定の仕込みは 11-06 に `requests_by_kind.py` へ足した（出力の末尾に「まとめ返答」の群別表: na_apply あり / なし。CSV に `bulk` `na` 列）。見る数字: 応答数（基準 15.1）、ツール数、トークン。11-06 時点: あり 13 件・応答 13.1・ツール 17.8、なし 47 件・応答 7.6・ツール 10.2（11-02 以降）。ただし「あり」は close を行う会話に偏るので単純比較できない。11-13 に `--since 2026-11-07` で再実行し、あり・なしの差でなく「あり」の応答数が 15.1 から下がったかで判断する。
   - 5h 【優先: 中。方針決定済み・試用待ち。期日 11-13】探索を別エージェントに任せる効果。方針（ee 11-06）: 既存の subagent は screening 用の 10 会話だけで探索の例がない（`subagent_cost.py`: 本体 32.4M に対し subagent 1.9M = 6%）。通常運用の規則は変えない。ee が探索の重い依頼（調査・決定の検索など）の依頼文に「探索は subagent に任せてよい」と書いた日を試用とし、`subagent_cost.py` で本体と subagent の合計、`requests_by_kind.py` で本体の応答数・トークンを見る。比べる相手は同じ種類の subagent なしの依頼。試用の機会が来るまで待つ（足すものはない）。

## Open Questions

- 【期日なし、NA・OQ が全件クローズした後】切る目安を 100k から 60k に下げるか: 100k 維持を採用（ee の決定 11-01）。全件クローズの後に全体を見て再判断する。10-29 の算出: ピーク 60〜100k の依頼は 1 件 537k で、〜60k の 169k の 3 倍（`records/2026-10-29-continue-split-effect.md`。切る回数が増える費用との差引は、同じ作業の比較ではないので確定しない）。
