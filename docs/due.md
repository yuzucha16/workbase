# 期日（due）

日付で浮上する項目の置き場（2026-10-29 に `docs/log.md` の「期日」の節から移した）。開始時には読まない。`review 消化` が `python -I workflow-kit/tools/due.py` で期日が今日以前の行を出し、単発は Next Actions に `【起票 MM-DD、期日 MM-DD】` として上げて、この表から消す。定例は、上げたあと次回の期日に書き換え、消さない。書式は `workflow-kit/docs-rules.md`。

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-04 | 単発 | 保留 2 件（元は log の Open Questions。11-05 から前倒し）: ① `repos/` の受け渡し（`dev` の `env/` の実使用の後に決める）、② `restore_project` の `_noai/final/` の上書き（実機で保護を試してから決める） | ユーザー（実機） |
| 2026-11-05 | 単発 | room-type-consolidation の実機確認（起票 10-25。追加の作業が入ったため 11-05 に設定、11-01 ユーザー）: 1 Project で `env/` と `tests/` と `docs/` に加えて `src/`（コード開発）を通す実測（題材は同じ WSL の Python 環境。`repos:` を書いた `dev` の Project）。観察点: 構成要素の選び方、置き場の取り違えの再発、検証が自己向けになって弱くならないか（ユーザー、10-25）。案 A の実装（`a9d03cc` `721f3f9`。単体テストのみ）の実機確認: ① `room start` で `~/src/<repo>` が `--add-dir` で渡り、その `CLAUDE.md` が読まれる ② AI が `git -C ~/src/<repo>` で commit でき、`ai/` に化けない ③ 修正した `ROOM.md` が届いて置き場の取り違えが再発しない ④ `room close` が未 push の clone で止まる ⑤ 対話での `cd` 後の cwd の持続（未測）。あわせて置き場の実測（11-01、旧 11-07 の「聞き返すか」を統合）: ケース A `src/` のみ、B `src/` `tests/` `docs/`、C `env/` `src/` `tests/` `docs/` `report.md` を、置き場を依頼に書かずに通す。規則なしで `<成果物名>` の付け方を見てから、`dev-deliverable-guide.md` に「既定は Project 名と同じ」を書いて再測。詳細は `topics/room-type-consolidation/docs/log.md` | ユーザー（実機） |
| 2026-11-05 | 単発 | token-cap NA 6: 出力の型（8 本）の試用の結果を見る（誤爆、型の品質、開始時の大きさ） | ユーザー |
| 2026-11-06 | 単発 | token-cap NA 5: 応答数を減らす手段（(b)(f)〜(i)）の優先と残す・畳むを決める | ユーザー |
| 2026-11-08 | 単発 | token-cap NA 4: 土台の整理の再判断（NA 7 は 11-01 に閉じ、26k は注記が主因と確定）。100k 運用の効果を見てから決める | ユーザー |
| 2026-11-08 | 定例 | weekly の振り返り（7日周期、日曜。材料は `topics/kit-growth/records/`）。仮決めの期限切れを数える | ユーザー |
| 2026-11-08 | 単発 | 索引（triggers）の引き当て率の初回: `python -I workflow-kit/tools/triggers_stats.py --since 2026-10-25 --detail`。語の足し方か出し方を決める。あわせて部分一致の誤爆（例: 「ログイン」が札「ログ」に当たる）への備え（短い札の禁止、完全一致の書き方、現状維持）を決める。現状（誤爆する）は単体テスト `test_substring_match_false_positive_is_current_behavior` で固定してあり、方針を変えるときはこのテストも直す。あわせて、旧 `md-link-graph` の積み残し 2 件: ① 上限 30 語で誤爆が増えていないか、取りこぼしは `triggers:` に語を足す案にする、② S11（`AGENTS.md` や kit の規則にも `triggers` を付けるか）は付けない方針のまま届かなければ見直す。`logbook/` を `--triggers` の対象にするかの判断もこの結果の後（旧 `logbook-design` NA 3）。構造の点検（循環・階層・複雑度）は `review` の入力 9 | ユーザー（AI が実行） |
| 2026-11-09 | 単発 | log の Next Actions 2（11-03 から延期。room-type-consolidation などで成果物の周辺を整えてから。11-01 ユーザー）: PC2 で `verify.bat` と `verify.ps1` を 1 回ずつ（`docs/alignment-baseline.md`。未決は `release` の束ね先。起票 10-25）。旧 `hook-room-alignment` の同じ項目はここに統合。見るもの: uv の取得、文字コード、y/n と日本語のひとこと。最初の失敗が原因の台帳（`script-guide.md`）の初めての使用になる | ユーザー（実機） |
| 2026-11-09 | 単発 | room-type-consolidation: Vault 2 分割の実装（11-02 に正式化。dotfiles の実装は別コミット。進み具合を見て延期か判断） | ユーザー・AI |
| 2026-11-10 | 単発 | token-cap: 全文読みの縮小の効果（分割後だけ）。Windows 側・room・PC1 で `repeat_reads.py --since 2026-10-30 --detail`。(1) 3 本の 1 回あたり（commit-push-rules 6.1k、log 2.5k、wrap-hook 2.7k）が下がったか。(2) `docs-rules.md`（5.7k に分割。`docs-format.md` 5.4k、`docs-carry.md` 3.1k）が下がったか、wrap が `docs-format.md` を読んで増えていないか。(3) `stock-hook.md`（10-29 に 19.2KB → 17.8KB、例外を `stock-exceptions.md` へ）の 1 回あたりが下がったか。基準は `topics/token-cap/records/2026-10-29-repeat-reads-baseline-pc2.md`（PC1 は未実行）。次の縮小候補は、効果を見てから決める（11-05 から延期） | AI（ユーザーの依頼で） |
| 2026-11-10 | 単発 | token-cap: wrap-hook 見直しの効果（反映は済。`topics/token-cap/records/2026-10-29-wrap-decompose.md`）。`requests_by_kind.py --since 2026-10-30` で wrap の応答平均（8.3）と 1 件平均のトークンを見る。書き漏れ・誤りは `review` で（11-05 から延期） | AI（ユーザーの依頼で） |
| 2026-11-10 | 単発 | token-cap: `AGENTS.md` に足した 2 行（10-29。まとめて呼ぶ、編集後に読み直さない）の効果。`requests_by_kind.py --since 2026-10-30` で応答の平均が下がったかを見る（wrap-hook の測定と同時。11-05 から延期） | AI（ユーザーの依頼で） |
| 2026-11-11 | 単発 | 振り返り（改善4）に計画を入力として足す案の判断 | ユーザー |
| 2026-11-11 | 単発 | token-cap: `integrate` の上限（仮 〜11-29）の個別の効果を再測定（`requests_by_kind.py --csv` で integrate の 10-27 以降の件数を見る。Windows 側と room 側。11-05 から延期）。10-29 の値（Windows 側、10-01 以降 16 件）: 10-27 より前 13 件は応答 9.4・1 件 809k・ピーク平均 92k。10-27 以降 3 件は応答 11.0・708k・ピーク 85k（うち 1 件は 7 応答でピーク 134k）。件数が少なく判定保留。room 側（PC1）の件数は未確認 | AI（ユーザーの依頼で） |
| 2026-11-12 | 単発 | ooxml-clean NA 1: room の `mask` への組み込み（pptx の確認は済。報告の置き場の OQ もここで決める） | AI（ユーザーの依頼で） |
| 2026-11-12 | 単発 | ooxml-clean OQ: 本文の個人名は `mask.toml` の運用に任せるか、候補の検出を足すか（判断） | ユーザー |
| 2026-11-16 | 単発 | ooxml-clean NA 3: 外向け Area の共有（`room stock --dst area` と `ctx/area/` の写し）の PC1 での動作確認（別セッション。期日は仮） | ユーザー |
| 2026-11-16 | 単発 | ooxml-clean NA 4: internal の Area への適用を決める（ee が na に積んだ。期日は仮） | ユーザー |
| 2026-11-13 | 単発 | office-output-types NA 2: PC1 で入力 2〜3 種類の見出し・列名だけで定義表の行を書く（実機） | ユーザー（PC1） |
| 2026-11-14 | 単発 | office-output-types NA 3: 雛形を `exmem/lessons/` に昇格するか（11-13 の実機の後） | ユーザー |
| 2026-11-14 | 単発 | token-cap OQ: Zed の System tools が 9.0k → 9.9k に増えた原因（実機の Zed） | ユーザー（実機） |
| 2026-11-15 | 単発 | 旧 `logbook-design` NA 1: 実機でしか確かめられない畳み候補。room の OQ 4 項（マウントの可視性、プリンタ設定、マスクから復元までの通し、pptx）と、obsidian-vault-backup の NA 2 項（WSL の張り直し〔`GHQ_ROOT` は WSL の中で確認〕、`vault-backup.bat`）。実機の機会がなければ、項ごとに「畳む（OQ/NA を閉じる）」か「延期」かを決める | ユーザー |
| 2026-11-15 | 単発 | 旧 `logbook-design` NA 5: 追記の型 (b)（OQ・NA を本体に 1 つ）が、その後の lessons 追記で守られているか確かめる。既存ファイルの直しは `review 消化` で。守られていれば取り下げ | AI（`review 消化` で） |
| 2026-11-16 | 単発 | `mdrank.py` の値が下がった理由（元は直下 log の OQ。11-01 は 1 位 24/40、上位 5 件 35/40。10-30 は 25/40、35/40。場面の一覧か `triggers:` の変更の影響と見ているが未調査。引当率は母数が 42 件から 1383 件に変わり、単純には比べられない）。次の `review` の入力 9 で前回と比べる | AI（`review` で） |
| 2026-11-16 | 単発 | `stock` の `scope: area` の実機確認（旧 `hook-room-alignment` NA 1）: 部屋の AI が `ai/out/knowledge/` に `kind: lesson` で書く → `restore` で Area に実名で置く → 次の Project の `room pull --where kind=lesson` で受け取れるか。`room pull --where` の仕様変更の予告があれば、`room-context.md` の `stock` の節と合わせて見直す（単体テストのみ。2026-10-24）。実機の機会がなければ延期か取り下げを決める（11-08 から延期） | ユーザー（実機） |
| 2026-11-17 | 単発 | office-output-types OQ: 型を足す順とテキストを共通の受け渡しにする案の当否、取得層の切り出し | ユーザー |
| 2026-11-29 | 単発 | `brief 計画` は実務で3回使うまで試験運用（`decisions.md` の 2026-10-25）。使った回数: 0（10-29 時点）。3回に達していれば試験運用を閉じる判断、未達なら続ける（monthly で確認） | ユーザー |
| 2026-11-29 | 定例 | monthly の振り返り（28日周期、日曜）。R-2026-10-25-02 の検証もここで | ユーザー |
| 2026-11-29 | 単発 | 旧 `logbook-design` NA 2・4: (a) `--check-aging` の FAIL 1 件（`logbook/user-thinking-habits.md` が budget 32KB を 40 バイト超過）を圧縮か budget の付け直しで決める。(b) 週次の記録（`kit-growth/records/`）を 1 回手で畳む試行（置き場は変えない）。月次の振り返りと同時 | ユーザー |
