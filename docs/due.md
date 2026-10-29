# 期日（due）

日付で浮上する項目の置き場（2026-10-29 に `docs/log.md` の「期日」の節から移した）。開始時には読まない。`review 消化` が `python -I workflow-kit/tools/due.py` で期日が今日以前の行を出し、単発は Next Actions に `【起票 MM-DD、期日 MM-DD】` として上げて、この表から消す。定例は、上げたあと次回の期日に書き換え、消さない。書式は `workflow-kit/docs-rules.md`。

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-01 | 定例 | weekly の振り返り（7日周期、日曜。材料は `topics/kit-growth/records/`）。仮決めの期限切れを数える | ユーザー |
| 2026-11-29 | 単発 | `brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0（10-29 時点）。3回に達していれば試験運用を閉じる判断、未達なら続ける（monthly で確認） | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-04 | 単発 | 返答の並び（求めること・確認を最下段、結論をその直前。`AGENTS.md`）の 1 週間の試行を続けるか判断 | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |
| 2026-11-05 | 単発 | token-cap の NA 2: `integrate` の上限の効果を再測定（`requests_by_kind.py --csv` で integrate の 10-27 以降の件数を見る。Windows 側と room 側）。手順と 10-29 の値は `topics/token-cap/docs/log.md` | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap の NA 1: 全文読みの縮小の効果（分割後だけ）。Windows 側・room・PC1 で `repeat_reads.py --since 2026-10-30 --detail`。(1) 3 本の 1 回あたり（commit-push-rules 6.1k、log 2.5k、wrap-hook 2.7k）が下がったか。(2) `docs-rules.md`（5.7k に分割。`docs-format.md` 5.4k、`docs-carry.md` 3.1k）が下がったか、wrap が `docs-format.md` を読んで増えていないか。(3) `stock-hook.md`（10-29 に 19.2KB → 17.8KB、例外を `stock-exceptions.md` へ）の 1 回あたりが下がったか。基準は `topics/token-cap/records/2026-10-29-repeat-reads-baseline-pc2.md`（PC1 は未実行）。次の縮小候補は、効果を見てから決める | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap の NA 8: wrap-hook 見直しの効果。`requests_by_kind.py --since 2026-10-30` で wrap の応答平均（8.3）と 1 件平均のトークンを見る。書き漏れ・誤りは `review` で | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap の NA 5 の (c)(e): `AGENTS.md` に足した 2 行（10-29。まとめて呼ぶ、編集後に読み直さない）の効果。`requests_by_kind.py --since 2026-10-30` で応答の平均が下がったかを見る（NA 8 の測定と同時） | AI（ユーザーの依頼で） |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める | ユーザー（AI が実行） |
| 2026-11-09 | 単発 | 振り返りの仮決め2件（字数の数え方、v6）をまとめて判断。規模をもっと縮められるかも決める | ユーザー |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断 | ユーザー |
