# 期日（due）

日付で浮上する項目の置き場（2026-10-29 に `docs/log.md` の「期日」の節から移した）。開始時には読まない。`review 消化` が `python -I workflow-kit/tools/due.py` で期日が今日以前の行を出し、単発は Next Actions に `【起票 MM-DD、期日 MM-DD】` として上げて、この表から消す。定例は、上げたあと次回の期日に書き換え、消さない。書式は `workflow-kit/docs-rules.md`。

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-01 | 定例 | weekly の振り返り（7日周期、日曜。材料は `topics/kit-growth/records/`）。仮決めの期限切れを数える | ユーザー |
| 2026-11-29 | 単発 | `brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0（10-29 時点）。3回に達していれば試験運用を閉じる判断、未達なら続ける（monthly で確認） | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-03 | 単発 | log の Next Actions 2: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`）。旧 `hook-room-alignment` の同じ項目はここに統合。見るもの: uv の取得、文字コード、y/n と日本語のひとこと。最初の失敗が原因の台帳（`script-guide.md`）の初めての使用になる | ユーザー |
| 2026-11-03 | 単発 | ooxml-clean の NA 2: PC1 の実 pptx を `cleankit.py` で `check` → `clean`（standard）し、PowerPoint で警告なしに開くか確かめる。結果で NA 1（room の `mask` への組み込み）に進む。手順は `guides/howto/ooxml-clean.md` | ユーザー（PC1） |
| 2026-11-04 | 単発 | 返答の並び（求めること・確認を最下段、結論をその直前。`AGENTS.md`）の 1 週間の試行を続けるか判断 | ユーザー |
| 2026-11-05 | 単発 | Open Questions の保留 2 件（`repos/` の受け渡し、`restore` の上書き保護） | ユーザー |
| 2026-11-05 | 単発 | token-cap: `integrate` の上限（仮 〜11-29）の個別の効果を再測定（`requests_by_kind.py --csv` で integrate の 10-27 以降の件数を見る。Windows 側と room 側）。10-29 の値（Windows 側、10-01 以降 16 件）: 10-27 より前 13 件は応答 9.4・1 件 809k・ピーク平均 92k。10-27 以降 3 件は応答 11.0・708k・ピーク 85k（うち 1 件は 7 応答でピーク 134k）。件数が少なく判定保留。room 側（PC1）の件数は未確認 | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap: 全文読みの縮小の効果（分割後だけ）。Windows 側・room・PC1 で `repeat_reads.py --since 2026-10-30 --detail`。(1) 3 本の 1 回あたり（commit-push-rules 6.1k、log 2.5k、wrap-hook 2.7k）が下がったか。(2) `docs-rules.md`（5.7k に分割。`docs-format.md` 5.4k、`docs-carry.md` 3.1k）が下がったか、wrap が `docs-format.md` を読んで増えていないか。(3) `stock-hook.md`（10-29 に 19.2KB → 17.8KB、例外を `stock-exceptions.md` へ）の 1 回あたりが下がったか。基準は `topics/token-cap/records/2026-10-29-repeat-reads-baseline-pc2.md`（PC1 は未実行）。次の縮小候補は、効果を見てから決める | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap: wrap-hook 見直しの効果（反映は済。`topics/token-cap/records/2026-10-29-wrap-decompose.md`）。`requests_by_kind.py --since 2026-10-30` で wrap の応答平均（8.3）と 1 件平均のトークンを見る。書き漏れ・誤りは `review` で | AI（ユーザーの依頼で） |
| 2026-11-05 | 単発 | token-cap: `AGENTS.md` に足した 2 行（10-29。まとめて呼ぶ、編集後に読み直さない）の効果。`requests_by_kind.py --since 2026-10-30` で応答の平均が下がったかを見る（wrap-hook の測定と同時） | AI（ユーザーの依頼で） |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める。あわせて部分一致の誤爆（例: 「ログイン」が札「ログ」に当たる）への備え（短い札の禁止、完全一致の書き方、現状維持）を決める。現状（誤爆する）は単体テスト `test_substring_match_false_positive_is_current_behavior` で固定してあり、方針を変えるときはこのテストも直す。あわせて、旧 `md-link-graph` の積み残し 2 件: ① 上限 30 語で誤爆が増えていないか、取りこぼしは `triggers:` に語を足す案にする、② S11（`AGENTS.md` や kit の規則にも `triggers` を付けるか）は付けない方針のまま届かなければ見直す。`logbook/` を `--triggers` の対象にするかの判断もこの結果の後（旧 `logbook-design` NA 3）。構造の点検（循環・階層・複雑度）は `review` の入力 9 | ユーザー（AI が実行） |
| 2026-11-08 | 単発 | `stock` の `scope: area` の実機確認（旧 `hook-room-alignment` NA 1）: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更の予告があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。実機の機会がなければ延期か取り下げを決める | ユーザー |
| 2026-11-09 | 単発 | 振り返りの仮決め2件（字数の数え方、v6）をまとめて判断。規模をもっと縮められるかも決める | ユーザー |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断 | ユーザー |
| 2026-11-15 | 単発 | 旧 `logbook-design` NA 1: 実機でしか確かめられない畳み候補。room の OQ 4 項（マウントの可視性、プリンタ設定、マスクから復元までの通し、pptx）と、obsidian-vault-backup の NA 2 項（WSL の張り直し〔`GHQ_ROOT` は WSL の中で確認〕、`vault-backup.bat`）。実機の機会がなければ、項ごとに「畳む（OQ/NA を閉じる）」か「延期」かを決める | ユーザー |
| 2026-11-15 | 単発 | 旧 `logbook-design` NA 5: 追記の型 (b)（OQ・NA を本体に 1 つ）が、その後の lessons 追記で守られているか確かめる。既存ファイルの直しは `review 消化` で。守られていれば取り下げ | AI（`review 消化` で） |
| 2026-11-29 | 単発 | 旧 `logbook-design` NA 2・4: (a) `--check-aging` の FAIL 1 件（`logbook/user-thinking-habits.md` が budget 32KB を 40 バイト超過）を圧縮か budget の付け直しで決める。(b) 週次の記録（`kit-growth/records/`）を 1 回手で畳む試行（置き場は変えない）。月次の振り返りと同時 | ユーザー |
