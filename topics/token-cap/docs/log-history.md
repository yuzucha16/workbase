# 経緯（log-history）

## Log

- 2026-10-29（NA 9: `docs-rules.md` の分割）: 「token-cap の続き」。ee が NA 9 の実施を承認。`docs-rules.md`（11.3k）から 35〜75 行を `docs-format.md`（5.4k）、77〜91 行を `docs-carry.md`（3.1k）へ移し、`docs-rules.md` は 5.7k に（1〜27 行は動かさず、「続き」の節は `offset` 24 のまま）。参照元 8 か所（`wrap-hook.md`、`stock-hook.md`、`templates/decisions.md`、`token-matrix.md`、`README.md`、`exmem/lessons` 2 件）を張り替えた。push 済み（`1de15d2`、`[workflow-kit]`）。効果は 11-05 の再測定（NA 1）に含める。`hook-matrix.md` の字数の記録と `hooks.md` の表は未更新。wrap。

- 2026-10-29（NA 2 の測定、再測定の期日化、PC2 の基準値、`docs-rules.md` の分割案）: 「token-cap の続き」。NA 2（`integrate` の上限の個別の効果）を Windows 側の `requests_by_kind.py --csv` で測った。integrate は 10-01 以降 16 件、10-27 より前 13 件は応答 9.4・809k・ピーク 92k、以降 3 件は応答 11.0・708k・ピーク 85k（10-29 の 1 件はピーク 134k）。件数が少なく判定不能。ee が「再測定は 1 週間あける」と決め、NA 2・NA 1・NA 8 の再測定を `docs/due.md` に 11-05 の単発として移した。ee が PC2 で `repeat_reads.py --since 2026-10-01 --detail 15` を実行（Windows: 会話 150 本、全文読み 56%・70% の文字数。log 3,831/回、docs-rules 11,289/回で 3 位。WSL は会話 2 本で基準にならない）。`records/2026-10-29-repeat-reads-baseline-pc2.md`。縮小の次の候補は `docs-rules.md` と `stock-hook.md`。`docs-rules.md` の 3 分割案を出し、ee が実施を別セッションにすると決めた（NA 9）。コミットは `[token-cap]`。wrap。

- 2026-10-29（NA 8: wrap の分解と `wrap-hook.md` の見直し）: 「token-cap の続き na8」。ee が wrap の会話（e1ea4789: 応答 4、最大 33.7k）の `decompose_session.py` を共有。軽い例だったので、重い例 d02fe8e6（作業 5 件のあとの wrap、13 応答・1.45M）も分解し、10-27 以降の wrap 45 件を会話の大きさ別に集計: 100k 以上の 5 件（1 件平均 1.3M）が wrap 計 26.3M の 25%、50〜100k の 35 件が 71%。wrap の費用は手順の読み（約 6k 字）でなく、膨らんだ文脈を 8〜13 回運ぶこと（`records/2026-10-29-wrap-decompose.md`）。ee が「100k 前に言う」と「応答のまとめ方」（読み・書き・コミットを各 1 応答、目標 4〜6）の両方を承認し、`wrap-hook.md` に反映（`cf6c606`）。ee の指摘: 応答数を半分にすればトークンもほぼ半分になる（AI が「手順の文章の短縮」と「応答数の削減」を混ぜて小さく見積もっていた。訂正済み）。NA 8 は、効果の確認だけ残して一部済に。コミットは `[workflow-kit]`。wrap（新しい手順で実施）。

- 2026-10-29（NA 1 (3) の参照直しと Windows 側の再測定）: 「token-cap の続き」。`commit-push-rules.md` などの分割で古い参照が残っていた 3 か所（`templates/workspace/AGENTS.md`、`exmem/lessons/workflow-kit-delegation.md`・`claude-code-permissions.md`）を直した（NA 1 の (3) は済）。ee が Windows 側で `repeat_reads.py --since 2026-10-27 --detail` を実行: 会話 58 本、全文読み 72%、1 回あたりは commit-push-rules 6,107、log 2,461、wrap-hook 2,703（分割前の会話が大半で、効果の判定はできない）。NA 5(a) の `requests_by_kind --detail --since 2026-10-27`（PC2。ee が確認して閉じた）: 182 依頼、平均 6.5 応答、wrap が応答の 29%・トークンの 37%（8.4 応答、入力 72k）で最大、会話の途中の依頼がトークンの 82%。ee が wrap-hook の見直しを次のセッションにすると決め、NA 8 に積んだ。コミットは `[workflow-kit]` `[exmem]` `[token-cap]`。wrap。

- 2026-10-29（`docs/log.md` と `wrap-hook.md` の縮小）: 「token-cap の続き」。`repeat_reads.py --detail` を再実行（全文読みは Read の 72%、その 96% が md。`records/2026-10-29-repeat-reads-2.md`）。ee の指摘で、直下の `docs/log.md` のトピック固有の NA（4・6・7・8）は、各トピックの `docs/log.md` が持つので二重管理と判明。トピック側にあるかを確認し、無かった 2 点を移して削除、直下 3,973 → 2,449 文字。規則を `topics/AGENTS.md`・`wrap-hook.md` に反映（決定は `docs/decisions.md`）。ee が `wrap-hook.md` の縮小を承認し、2,963 → 2,637 文字、まれな分岐を `wrap-targets.md` に分けた。NA 1 の「log.md と wrap-hook.md を絞る」は済として移した。コミットは `[docs]` と `[workflow-kit]`。wrap。

- 2026-10-29（(d) の測定と `commit-push-rules.md` の分割）: 「token-cap の続き」。ee が、完了条件の仮説（(f)）の検証を後日にして (d) に進むと決めた（NA 1b に積んだ）。`repeat_reads.py` を作り、Windows 側（10-27 以降、52 会話・Read 448 回）を測った: 重複読み 5%、md の全文読み 74%、上位 3 本が全文読みの md の 61%（`records/2026-10-29-repeat-reads.md`）。ee が `--detail`（md の名前の表示）を承認。`commit-push-rules.md`（6,387 文字）を、核・`push-rules.md`・`commit-special.md` の 3 本に分ける案を作り（`records/2026-10-29-commit-push-split-plan.md`）、ee が承認、このセッションで実装した（push は別ファイル、「しないこと」は核に残す。核 3,100 文字）。ee の気づき: 規則が長いのは、`lessons/` に置くべき個別の事情を同じファイルに足してきたため。参照 8 ファイルを直し、決定をルートの `docs/decisions.md` に記録。コミットは `[token-cap]` と `[workflow-kit]`。wrap。

- 2026-10-29（other の仕分け `--detail` と (f) の試験）: 「token-cap の続き」。ee が PC1 room の `requests_by_kind --detail` の画面を共有。other の 101 文字以上（74 件・41.3M）は、101-300 文字が 54 件・37%、1001 文字以上は 3%、コードブロックなしが 44%。仮説（マクロの仕様入力で長い）は当たらない。continue 26 件は全件が最初の依頼でトークンの 13%。全依頼ではトークンの 76% が会話の途中の依頼（最初は応答 2 倍だが 24%）。ee が数件を自分で見て、「場所は伝えている、ゴールは無い、指示型」と回答。AI の仮説は「完了条件が無いと終わりを AI が決めて読みが増える」（未検証）。ee が (f) を完了条件の足す・足さない比較で試すと決めた。`records/2026-10-29-pc1-room-other-detail.md`。NA1（仕分け）は済として移し、試験に置き換えた。wrap。

- 2026-10-29（PC1 room の効果と依頼別の応答数、`--detail`）: 「workbase の続き na7」。Windows 側の `cap_meter`（10 月 303.4M、土台 27.8k）は効果の判定に使えず、ee が PC1 room の `cap_meter`（85.8M、土台 17.9k、日ごと 10-26 23.7M → 10-27 以降 約 7M）を共有。ee の見立て（作業量は 10-26 以前と同等）で「仕組みの効果」を仮決め（〜11-29）。room の `requests_by_kind`（193 依頼、平均 6.3 応答、wrap は 4.6、other の 101 文字以上が 74 件・41.3M、continue は 10.8 応答）を記録（`records/2026-10-29-pc1-room-effect-and-requests.md`）。ee の仮説（マクロの仕様入力で長い）の仕分けは、依頼文を読まず機械的な特徴で行うと決め、`requests_by_kind.py` に `--detail` を追加（Windows 側で 1 回実行して動作を確認。この PC の other の 101 文字以上は 117 件、置き場は resources が 101 件、会話の途中が 107 件、101〜300 文字が 91 件で、マクロの仕様入力という仮説の材料は無い。PC1 room で確認する。動作確認は ee が別チャットで行う）。ee の質問「continue を多用して応答数が増えたか」: room では continue は平均 10.8 応答（全体 6.3）で応答の 23%・トークンの 13%（1 応答の入力 38k と小さい）。Windows 側は 5.7 応答で増えていない。コミットは `[token-cap]`。wrap。

- 2026-10-29（room の 107k の判定）: 「topics/* の続き pc1でやること」。ee が PC1 の room で `decompose_session.py --session e3edb1ce` を実行し、画面を共有。結果: 依頼 1 件、34 応答、土台 18,437、最大 106,979、1 回の増加は最大 11,653（8k 超は 2 回）、Bash 28 回で 85,951 文字、Read 10 回はすべて png（0 文字、重複 2 ファイル）。判定: 172k の型（全文読みの連発）ではなく、応答数の多さ（Bash の出力と画像読みの積み上げ）。ee は、PC2 の分析にも同じ傾向があったと確認（`records/2026-10-29-room-107k-judgment.md`）。NA 1 から該当部分を消した。画像のトークンは未測定。同じセッションで、ルートの NA 12（room の記録先）も調べた（ルートの `docs/log-history.md` の同日）。wrap。

- 2026-10-28（応答数を減らす手段の洗い出しと、依頼別の応答数の測定）: 「token-cap の続き」。ee が、分析の結果「消費量は 1 依頼の中の応答数が第一」とわかったと述べ、減らすために必要なことのリストアップを依頼。AI が調査結果（172k の 1 依頼は 27 応答、Read 58 回・Edit 44 回。「振り返って」の型で 4→3 応答）から 10 個を挙げた。ee が 1（依頼別の応答数の測定）を依頼し、残りは wrap で記録、8（別エージェントへの委譲）も実測すると決めた。`requests_by_kind.py` を作り、Windows 側（10-01 以降、543 依頼）を実行した。結果: 平均 6.3 応答（概算の約 10 より小さい）、wrap は 88 件・8.3 応答・トークンの 24%、11 応答以上の依頼が 16% でトークンの 44%（`records/2026-10-28-requests-by-kind.md`）。ee は wrap の伸びが高い感覚に合うと確認し、room も同じ分析をすると決めた。コミットは `[token-cap]` の 1 件。wrap。

- 2026-10-28（NA6 の拡大と入力側の畳み）: 「token-cap の続き np6,7」。ee が 3 回目の「振り返って」の結果を共有（応答 3、土台 26.1k、読みは型 1 本。応答 4 → 3 回で、`triggers` の修正が効いた）。NA7 の ①〜③ は説明して済み（`cap_meter` の表の見方、`--session` の実行例。② の Zed の ACP 表示は、ガイドの記述を根拠に「直近の応答の大きさ」と答えたが、ee が後で NA7 を「確定する」に書き直した＝根拠は未確認）。ee の決定で、(1) 調査1・2、計画、改善1〜3 の出力の型 6 本を作り、`brief` の引数と `brief-modes.md` を廃止、(2) 入力側を畳み、元の調査1・2、改善1〜3（のちに改善4・5 も）を `superseded`、依頼の文例を `guides/quickref/ai-work-prompts.md` に集約、(3) 型の名前から `-2` をやめた（`research-explain-output`、`research-procedure-output`、`retrospective-incident-output`）。`methods.md` は選ぶ基準だけに。コミットは `[exmem]` `[guides]` `[workflow-kit]` `[token-cap]`。wrap。

- 2026-10-28（用語の整理と Zed 表示の確認依頼）: 「token-cap の続き」。ee が、1 会話 = 1 応答という誤解を訂正した。整理: セッション（会話）> 依頼 > 応答（モデルへの 1 回の呼び出し。ツールの実行自体はトークンを使わず、結果を受け取る次の呼び出しが履歴の全部を入力にする）。1 応答の入力 = 土台 + 履歴で、合計は各応答の入力の足し算。「振り返って」の応答 4→3 は、並列呼び出しでまとめた分（ee の説明）。応答数は、ツール呼び出しの数（並列なら 1）と指示で決まり、推論レベルは間接的に効くだけ。「約 10」は実測（上位 1 会話、125 応答）からの概算で、規則ではない。ee の質問「Zed は最後の 1 依頼の消費量か」に対し、AI は「直近の応答の入力の大きさ」と答えたが、確認はしていない。ee は確定させたいと決め、作業は別セッション（Next Actions 7）。コード・記録の変更なし。wrap。

- 2026-10-28（「振り返って」試験の 2 回目と `--session`）: 「token-cap の続き na6」。ee が 2 回の `cap_meter --latest` と `decompose_session.py --at` の結果を共有。1 回目の分解は、開始時刻が 10 秒差の別の会話（`0111e2e1`、応答 32）を選んでおり、「振り返って」の評価に使えない。2 回目（`80c99fea`、応答 4、土台 26.4k、積算 130k）が正。積算の 8 割が土台。応答 4 回の内訳は、`-2-output` の Read、`-output` の Read、`git log`、回答。`-2-output` の `triggers: 振り返` が「振り返って」で当たって余分に読んだのが原因（`triggers` から外した）。`decompose_session.py` に `--session <id>` を追加（取り違え防止）。大きさのずれ（cap_meter の方が 0.3〜2k 大きい）は、cap_meter が出力トークンを含むため（ee は (a) 説明を足す案を選択、docstring に追記）。コミットは `[token-cap]` の 1 件。wrap。

- 2026-10-28（「振り返って」試験の 1 回目と原因の切り分け）: 「token-cap の続き na6」。ee の `cap_meter --latest`（土台 26,010、応答 7、最大 55,530）と `decompose_session.py --at` の結果から、切り出した `-output` が使われず、元の `retrospective-method.md`（11KB）と `hooks.md`（5KB）を全文読んだと判明（Grep 4 回は 2.3k 文字で全文検索ではない）。土台が小さいのは開始時の `brief` 読み込みが走らなかったためで、切り出しの効果ではない（最初の読みを取り消した）。原因は、元の手順書の `aliases:` と本文の「振り返って」が、フックの部分一致より先に当たったこと。`aliases:` と本文を `-output` 側へ移した（`retrospective-method` と `-2`）。「振り返って」を `hooks.md` に載せる案は見送り（ee の決定）。`records/2026-10-28-retrospective-trial-result.md`。wrap。

- 2026-10-28（`--at` の時刻の確認）: ee が 107k を調べる前に、decompose の `--at` に渡す時刻を質問。時刻は会話記録の timestamp と同じ UTC で、`heavy_sessions.py` の日時はそのまま使える（`cap_meter.py` と Zed の表示は現地時刻なので、日本時間は 9 時間引くか `+09:00` をつける）と回答。時差つきの指定を UTC に直す修正と先頭の説明の追記を push（`8c66f7b`）。ee は PC1 でログを取得済み、結果の判定は PC での続き。
- 2026-10-28（wrap の新しい規則で log.md を掃除）: 済んだ部分を移した。NA2: `integrate` の読む量の上限と lessons の分割（`1d545aa`、`29bb5e0`）は済み。`--check-triggers` の FAIL 1 件は、上限が 30 語になって解消した（`06b3583`。10-28 の実行で fail=0）。NA4: `room reap` の退避は済み（残りの方針は「状態」へ移した）。OQ: 差の約 16M の出どころは取らない（ee の決定 10-27）。
- 2026-10-27（107k の確認の道具）: 「workbase の続き」で PC1 でやることを列挙し、ee が room の 107k の確認方法を token-cap 配下から探させた（方法は `records/2026-10-27-pc2-one-request-172k.md`）。ee の依頼で分解を道具化。最初に `workflow-kit/tools/` へ置いたが、ee の指示で `topics/token-cap/decompose_session.py` に移した。読み取り専用で、道具名・ファイル名・文字数のみ。応答と tool_use を id で重複除去。ダミーの jsonl で確認、実機の room では未実行。wrap。
- 2026-10-27（傾向分析の骨子を埋める）: 「token-cap の続き 傾向分析の骨子」。room の 107k は、この PC の room-myenv に 10-25 22:27 までの記録しか無く確認できず、ee が後日に回した。伸びの要因別の分解を PC1 Windows（10-01 以降、115 会話、2,916 応答）で実行（`%TEMP%` の一時スクリプト、道具名と文字数のみ、増加分を文字数で按分）: Read 45%、書き込み本文 23%、Grep 10%、AI 本文 9%、PowerShell 9%、ユーザー発言 1.6%。効く順は区切る → 大きな読み込みを避ける → 土台。ee から土台の比率が区切りまでの余裕を食い、依頼数が減るとの指摘（「6万」は「10万」の誤り）。AI の意見: 上限への効きは中、作業性では効く。ee は前倒ししないが漏らさないと決定し、decisions と Next Actions 5 に記録。`log.md` は 5.7KB→4KB 内に圧縮。wrap。

- 2026-10-27（integrate の読む量の上限）: Next Actions 2 を実行。xmem/inbox/ は今は空で、172k の型（下書き 14 本の全文読み）は再発しない。次に効くのは大きい lessons（workflow-kit.md 60KB、i-isolated-work-room.md 58KB、obsidian-vault.md 56KB、shell-script-testing-wsl.md 41KB）。ee が承認（数値は「3、20KB」）し、integrate-hook.md に「読む量の上限【仮 〜11-29】」を追加（下書き 3 本、20KB 超は節読み、重複読みなし、100k で区切る）。大きい lessons の分割は Next Actions に積んだ。room の 107k の確認は room 側データ待ち。wrap。

- 2026-10-27（PC2 の 172k の分解）: 傾向分析の「1 依頼で大きく増える会話」を PC2 の 1 本（172k、依頼 1）で分解。最初に「98 回の自走」と報告したが、jsonl の行数（内容ブロックごとに重複）を数えた誤りで、実際は応答 27 回。主因は全文読み 47 回（Read 58 回）。28 ファイルの 66% は `exmem/inbox/` の下書き 14 本と `exmem/lessons/` 5 本で、`integrate` の型。`usage_report.py` と `cap_meter.py` は重複を除いており、合計は正しいと確認。ee の順番は、重複の確認 → 種類別の仕訳 → wrap、止める基準の案は別セッション。`records/2026-10-27-pc2-one-request-172k.md`。wrap。

- 2026-10-27（PC1 の room 側の実測）: ee の「10-20 以降は WSL 側」の推測を確かめた。この PC の room-myenv には 10-25 の試運転の 5 会話（7.25M）だけ。ee が PC1 の room 内で `cap_meter.py --root /home/ai/.claude/projects` を実行し、10-21〜27 は 78.80M（37 会話）。合算 約 170.7M（85%）で、勤務先の表示との差は 88M → 約 16M。room の土台は約 18k（Windows 側 31k）。残り約 29M で 1〜2 日で尽きる見込みを伝え、ee は重い作業を止める、退避の手順を作る、分析は別セッションと決めた。`records/2026-10-27-pc1-room-meter.md`。wrap。

- 2026-10-26（土台の下調べ）: Next Actions 6 の下調べ。最大は claude.ai 同期の skills（約 3.2k、月の約 3.3%）で、外し方は claude.ai 側（未確認）。`resources/AGENTS.md` の整理は約 1%。「記録先」2 節を手順書へ移す案は、`workflow-kit/AGENTS.md`（固有事情を書かない）に反すると分かって取り下げ、`docs/record-destinations.md` に寄せる代案も含め、ee が影響が少ないとして全案を見送った。`records/2026-10-26-base-trim.md`。`log.md` は 4KB に圧縮（6.6KB→）。wrap。

- 2026-10-26（log.md の予算超え）: ee が a を選択。`topics/logbook-design/docs/log.md` を 6.4→3.8KB（予算 4KB 内）に縮めた。状態の節を圧縮し、Next Actions・Open Questions・待ち行列 3 件は意味を変えずに残した。縮めた旨は `logbook-design/docs/log-history.md` にも追記。これで読む量の削減の一手は一巡。wrap。

- 2026-10-26（hook-common の 6 万）: ee が承認。`hook-common.md` 38〜39 行の「会話が約10万トークン未満／以上」を約6万に直した（5d6ca15。約2万未満の例外は変更なし）。残りは `log.md` の予算超え（`logbook-design` 6.4KB）。wrap。
- 2026-10-26（brief の読む量）: ee が案 1・2 を承認。`brief-hook.md` の `hook-common.md` 参照を節指定（報告の型、他のフックを勧める条件。約 4KB／13KB）にし、引数つきモード（解決・改善・変更・調査・計画）を `brief-modes.md`（4.8KB）に切り出した（`brief-hook.md` 12.0→8.0KB）。切り出しの途中で `check-hook-outline.ps1` が参照の書き方（手順名にフックのファイル名が要る）で FAIL し、直して全件 OK。見込みは 1 会話 3〜4k 減で、実測は 10-27 以降。`hook-common.md` の「約 10 万で切る」が 60k 運用と食い違うのを見つけ、Next Actions に起票。wrap。

- 2026-10-26（exmem-index.md の読み方）: ee が提案を承認し、`exmem/AGENTS.md` の読む順番 1 を「`find_knowledge.py --triggers` で出なかったときだけ、索引を Grep で引く」に変えた。索引は 7.2KB（約 3.4k）で、+16k は直前の Glob との重なり。見込みは 1 会話 3〜4k 減で、実測は 10-27 以降。この会話では `python` がブロックされ、`--triggers` は実行できなかった。wrap。

- 2026-10-26（切り出しと 100k の調査）: ee が `docs-rules.md` の切り出しを承認し、「コミットと push」を `workflow-kit/commit-push-rules.md` に切り出した（`ce52646`。参照元 5 ファイルを修正、`docs-rules.md` は 24.6KB→12.4KB）。切り出した節は 13KB で、「約 4k」は誤りだった（両方読む会話は減らない）。続けて、`review 消化`（会話「コミット残件と承認待ちの整理」）が 100k に届いた原因を、uv run python の一時スクリプトで調べた: 2 回目のユーザー発言の実行中（API 18 回目）に、旧名の横断の掃除で行内容つきの Grep（12〜19KB が 3 回）と全文読みが積み上がった。ee の承認で、読み込みを抑える規則を `AGENTS.md` に書いた。`records/2026-10-26-review-digest-100k.md`。wrap。

- 2026-10-26（支配的な側の判定）: ee の問い「ベースを減らすか、フックを減らすか」に、会話記録の実測で答えた。土台は固定の約 28k で、伸びの主因はファイルの全文読み（`docs-rules.md` +7〜12k など）。ee の観察: フックなしのこの会話も 1 応答目で 55k、`review 消化` は 2 応答目で 100k（会話「コミット残件と承認待ちの整理」）。ee の予想どおりフックと `AGENTS.md` の両方に余地がある。最初の一手（`docs-rules.md` の切り出し）は ee が別セッションで行う。`records/2026-10-26-growth-by-reads.md` に記録。wrap。

- 2026-10-26（PC2 の実測）: ee が PC2 で `cap_meter.py` を実行（合計 2.33 億、応答 2,412、60k 超の応答はトークンの 89%、土台の中央値 27.9k）。ee の申告: PC1 と PC2 は別々で、上限は PC1 のもの。Zed の表示を累計と読み違えていたため多めに出ている。AI が削減量を見積もり（60k で切ると約 54% 減、土台 6k 減は切った後に約 14%）、`records/2026-10-26-cap-meter-pc2.md` に記録。10-25 と 10-26 を運用前の比較の基準にする。数字の理解を `stock 理解` で `exmem/inbox/2026-10-26-token-cap-meter-reading.md` に残した。wrap。

- 2026-10-26（`/context` の実測）: ee が家の PC で `/context` を取った。土台は端末 36.4k、Zed 19.4k（`records/2026-10-26-context-measure.md`）。差の大半（約 14k）は、Zed がツール定義を遅延読み込みにしていること（端末は全載せとみられる。未確認）。自前で動かせるのは skills 約 6k（claude.ai 同期 13 件が約 3.2k）と memory。ee は端末を使う予定がないため、端末の遅延読み込みの調査は保留（必要になったら依頼）。wrap。

- 2026-10-26（実機なし）: 土台の workbase 分を字数から推定（約 4〜5k）、フックの読み込み（`brief` 約 1.2万）が 60k 運用で効くことを確認。`/context` が Zed の ACP で通る見込みを確かめ、削減量の式と勤務先への確認の文面を `records/2026-10-26-desk-prep.md` に用意した。

- 2026-10-26（夜）: ee が切る目安を 6万（会話の大きさ）にし、2026-10-27 から運用。積算とサイズの違いを例で説明（土台 2.4万、10万で切ると平均 6.2万）。`cap_meter.py`（`--latest` つき）を追加。ベーストークンの内訳取りは、ee が家の PC で行う。wrap。

- 2026-10-26: 職場の AI 使用に月次上限。26 日で 90%。ee が 2 角度（仕組み、線引き）を提示。AI が既存資料（`notes/token-saving/` など）から角度 A〜L を一覧にした。ee が上限を 2億トークンへ訂正、haiku 案を追加、PC1 のデータは翌日取る。トピックを作成。Zed の表示の意味を調べ、マクロの役割分割を整理した。

- 2026-10-27: skills の整理。claude.ai の Customize > Skills で個別にオフにできると判明（設定の「クラウドでコードを実行」は前提のスイッチ）。前半の 5 件、第 1 段階の 4 件をオフにし、obsidian プラグインを uninstall。Zed の Skills は 5.8k → 3.5k。第 2 段階（xlsx・docx・pptx・pdf）は ee の判断で残す。System tools が 7.6k → 9.9k に増え、合計は 19.7k のまま（原因不明、再起動でも戻らず）。wrap。

- 2026-10-27（PC1）: ee が PC1 で 3 スクリプトを実行。合計 91.85M（10-09〜10-20）、1 応答の平均 約 124k、上位 3 本が 55%、上位 1 本は 125 応答で最大 408k。60k では PC1 の作業が 1 依頼で尽きると分かり、ee が切る目安を「作業の区切り、または 100k」に変更。解説に実測・チェックリスト・考察・方針を追記（guides/explain/claude-code-cost-session-size.md）。wrap。


- 2026-10-27（分析）: PC1 room の重い会話（上位 10 件すべて 100k 超、最大 216k）と会話別（上位 10 本で 66%）、PC2 の最新値（251.1M）を記録。3 か所の比較表と傾向分析の骨子を作った（`records/2026-10-27-trend-skeleton.md`）。room の会話は複数の mount をまとめるので大きく見える（ee）。勤務先への確認は省く（ee）。wrap。

- 2026-10-27（続き）: PC2 の会話別の占有率を埋めた（合計 252.31M、89 会話、上位 10 本で 41%、最大 8%、キャッシュ読み 96%。偏りは 3 か所で最小）。ee がマクロの現況を回答（1 本 1000 行規模、微修正のみ、PC1 の Windows 11 で bas を取り込むだけ、失敗時はエラー文のみ）して閉じ、10-01〜08 と Desktop の分は取らないと決めた。room の会話記録の退避は進める。wrap。

- 2026-10-27（room の内訳）: ee が `usage_report.py` の出力（画面の写真）を渡し、PC1 room の会話別の合計ランキングを記録した（`records/2026-10-27-pc1-room-ranking.md`。上位 10 会話 52.20M、応答 543 件、1 応答の平均 約 96k。出力は 1.3%）。最大入力の順位との会話の対応は未確認。wrap。


- 2026-10-27（room の退避）: ee が「ここでやる」と決め、`room reap` が消す前に部屋の会話履歴を Windows 側 `~/.claude/room-history/<部屋>/` へ tar で写すようにした（`f6da784`。写せなければ消さずに止まる。room のテスト全 150 件 OK、実機の WSL は未確認）。集計は `cap_meter.py --root` で読める。`-home-ai` は対象外。`--check-triggers` の FAIL（16 語）は、上限を 30 語にした意図的な変更で解消済みと ee が訂正。wrap。

- 2026-10-27（lessons の分割の続き）: ee の依頼で、obsidian-vault-structure（25KB）を 3 本（本体 12KB、obsidian-vault-rename、obsidian-vault-home-works）、windows-bat-testing（23KB）を 3 本（本体 7KB、windows-bat-pitfalls、windows-bat-eol-and-log）に分けた。索引・triggers 点検（fail=0）・リンクは確認済み。これで大きい lessons 6 本の分割が済んだ。

- 2026-10-28（brief の引数を絞るか）: Next Actions 6 の机上の部分を進めた。引数つき `brief` の開始時の読み込みは 約 7k でなく 17〜24k（`methods.md` 全文とやり方のノートまで読むため）と測り、出力の型だけなら 1 型 0.5〜2k と分かった（`691c5a4`、`records/2026-10-28-brief-mode-load.md`）。ee は「振り返りだけで試す」を選び、`retrospective-method-output` と `-2-output` に切り出して、依頼の語を型のノートへ移した（`a9a6c5c`。`decisions.md` に記録）。索引の部分一致は「振り返って」に当たらないため、語は語幹（`振り返`）にした。
