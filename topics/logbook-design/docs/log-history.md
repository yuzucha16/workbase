# 作業ログの経緯（log-history）

## Log

### 2026-10-29（「残」の整理と、辿れるかの確認）
- 畳み候補の「残」を実物で確かめた。旧 `C--vault*` のキーは `~/.claude/projects` に無く、`10_env.bat` の結果（`CERTS_DIR`、`WSLENV`、`~\.certs`）もこの PC で正しい。claude-code-storage の OQ/NA 3 項と obsidian-vault-backup の NA 1 項を閉じた（`exmem/lessons/`。根拠: ユーザーの承認）。`vault-backup.bat` は無く、`schtasks` の登録も無い（未了のまま）。
- 辿れるか（旧 NA 3）: `README.md:12` と、5 本すべてで親の lessons からの wikilink を確認した。`triggers:` は無い。実際にエージェントに辿らせる測定はしていない。`--triggers` の対象にするかは 11-08 の測定の後に判断する（Next Actions 3）。

### 2026-10-28（wrap の新しい規則で log.md を掃除）
- `wrap` の新しい規則で、済んだ項目を移した。NA3: `shell-script-testing-wsl` の Gotchas に一方向の印を付けた（`01ae113`。Facts の Ubuntu 24.04 は作業時の環境の記録なので付けない）。OQ「素材の節の扱い」と待ち行列の決定 2 件（追記の型は案 (b)、素材は案 (a)。`decisions.md`、`a1f70b4`）は決まったので外した。印の付与は Next Actions 6 に残る。

### 2026-10-27（単価の集約と素材の印）
- 単価を `session-handoff` の Facts に集約（auth-providers・storage・Decisions の根拠は指す）。`shell-command-usecases` の 2 節に素材の印、README の表を更新。

### 2026-10-27（保留 3 件への回答）
- 追記の型は (b)、素材は (a) と決まった（`decisions.md`）。単価の 1 か所化は進めてよいとの指示で、まとめ先を調べて案を出した（`session-handoff` の Facts に集約）。

### 2026-10-27（印の確認と `--check-aging` の初回）
- `shell-script-testing-wsl` を見直し、Gotchas の節に一方向の印を付けた（ツールの安全チェックの挙動は版で変わる）。Facts の Ubuntu 24.04 は環境の記録として印なし。
- `--check-aging` をクラウドの環境で初めて実行した。5 本中 1 本が FAIL（`user-thinking-habits.md` 32808 バイト > 32KB）。判断は月次に回す。

### 2026-10-27（畳み候補の「前」の圧縮）
- 「前」の 8 行を圧縮した（auth-providers、obsidian-vault-backup、obsidian-vault-structure、shell-script-testing-wsl、workflow-kit 2 件、para-operations 2 件）。一覧の行番号が現状とずれていたため、grep で現在の節を探して直した。6 ファイルの `updated:` を更新。`decisions.md` に 1 項。
- 旧名の更新（旧 Next Actions 3）は畳みで吸収として閉じ済み。

### 2026-10-27（畳み候補の「聞」への回答）
- ユーザーが「聞」に回答し、AI が 9 ファイルを編集した（auth-providers、linux-distro-selection、shell-script-testing-wsl、ai-isolated-work-room、session-handoff、claude-code-storage、obsidian-vault-backup、obsidian-vault、obsidian-vault-home-works）。room は決定 2 件を足した。session-handoff の TTL は Next Actions へ。範囲の判断は `decisions.md`。
- 旧名の更新（Next Actions 3）は「畳みで吸収」として閉じた。

### 2026-10-27
- 畳み候補の「済」をユーザーが承認し、8 ファイル 39 行を削除した（claude-code-storage、claude-code-auth-providers、linux-distro-selection、obsidian-vault-backup、obsidian-vault、workflow-kit、workflow-kit-closing、para-operations）。「たぶん」「一部」「大半」の付いた行と「聞」「前」「残」は残した。
- 旧名の更新（Next Actions 2）は、畳みで吸収したとして閉じた。
- `user-thinking-habits` を `exmem/lessons/` から `logbook/` へ移した（`exmem-index.md` の行を削除。名前は同じで `[[ ]]` は有効）。
- `user-manual` の Facts と Principles の対応表を作り（`records/2026-10-27-user-manual-facts-map.md`）、昇格済みの 6 項を `logbook/user-thinking-habits.md` の明細へ移した。未昇格の 3 項（やらないことを先に決める、引き継ぐ前提で終える、理解してから決める）は、ユーザーが捨てると決め、削除した。
### 2026-10-26（log.md の予算超えの整理、token-cap）
- `log.md` を 6.4KB から約 4KB に縮めた。経緯の細部（第1陣 5 ファイルの確認、`ai-work-metrics` の ③ の畳み、移した先の `logbook/*-log.md` の名前、`user-thinking-habits` の公開範囲の解消の経過）は `decisions.md` と `records/` にある。Next Actions の意味は変えていない。

### 2026-10-26（型の判断と実装）
- 叩き台の 7 点を、ユーザーがカードで 1 点ずつ判断した（すべて推奨どおり。`decisions.md`）。待ち行列の「`logbook/` の最小の型」の項を消した。
- 実装: `logbook/README.md`、`find_knowledge.py --check-aging`（`--today` で基準日を変えられる。一時ディレクトリの 4 ファイルで、欠け・type 違い・日付でない・budget が読めない・期限切れ・budget 超過の 7 件の FAIL と、正常なファイルの通過を確かめた）、ルートの `README.md` の構成の表、`exmem/AGENTS.md` のディレクトリの役割、`review-hook.md` の入力 3 に 1 行ずつ。消した Next Actions: 「最小の `logbook/` の型を決める」（完了）。

### 2026-10-26（review 消化）
- 待ち行列 8 件をサブエージェントでスクリーニングし（`records/2026-10-26-queue-screening.md`）、ユーザーが 1 件ずつ判断した（`decisions.md`）。消した Next Actions: 「次の `review 消化` で待ち行列 8 件を判断する」（完了）。`obsidian-vault` の未設定を残す項は、畳みの列挙（Next Actions 4）に合流した。
- 7(a) を kit に反映した（`review-hook.md` の消化モード、04ac4c7）。
- 版依存の印を lessons 6 ファイルの 14 か所に付けた（78df71b）。旧名の更新は対象がほぼ無いと分かった。畳む候補の一覧（d8a52c8）と `logbook/` の最小の型の叩き台（64bcc85）を出した。消した Next Actions: 「版依存の印を付ける」（完了）。

### 2026-10-26（続き）
- ユーザー: `para-operations` と `session-handoff` の Next Actions は置き換わり。畳んだ。
- ユーザー: 旧 `C:\vault` は消してよい。第3陣（`para-operations` `session-handoff`）の本文確認を `records/2026-10-26-wave3-review.md` に記録。降格は測定値だけで、残りは古い ③ の畳みと印。
- 第2陣の現況をユーザーが回答: MX Linux 導入済み、auth の Next Actions 完了、vault のバックアップは未了。
- 第1陣の 5 項目を、ユーザーの選択でこのトピックの Open Questions の待ち行列に置いた。`review 消化` の 3 段チェックの 1 段目。
- `ai-work-metrics` の ③ は、ユーザーが「続けていない、置き換わっている」と答え、畳んだ（`decisions.md`）。
- 第2陣 6 ファイルの本文確認（`records/2026-10-26-wave2-review.md`）。logbook に移すものはほぼ無く、1 回きりの移行の記録と古い ③ の畳みが主と分かった。仕組みの候補 2 つ（AI が古い ③ を見つける経路、追記の型）を待ち行列に置いた。

### 2026-10-26
- ユーザーの相談: exmem は半永久のナレッジ。これとは別に、期限のあるナレッジ（review の記録、取扱説明書、時系列で変わる知識、改善の規準、週報・月報）の置き場と、捨てる・圧縮・昇格・降格の仕組みが欲しい。流用できる既存の仕組みで、データフローを複雑にしない。must ではない。
- AI が現状を調べ、置き場の案 A/B/C と運用の叩き台を出した（`records/2026-10-26-logbook-proposal.md`）。期限のある記録は、取扱説明書（lessons）、週報・月報（`kit-growth/records/`）、review の記録（`docs/metrics/`）に散り、畳む経路が無い。
- ユーザーが案 A を `logbook/` で仮決めし、ほかにも漏れがあるはずと依頼。AI が `exmem/lessons/` 69 件を仕分けた（`records/2026-10-26-exmem-leaks.md`。title・節の構成・「時点」の数からの推測で、全文は読んでいない）。
- ユーザーが 3 型を定義（個人の好み・1 回きりを除く）。AI は ② を logbook に移さず lessons に残す案へ練り直し（`records/2026-10-26-recommendation-v2.md`）、承認された。
- 第1陣 5 ファイルの本文確認（`records/2026-10-26-wave1-review.md`）。節が単位であること、古い ③ が残っていること、`ai-work-metrics` と `claude-code-storage` の重複、公開範囲の確認事項を見つけた。
- 第1陣の仕分けを 3 段チェックに載せる前に、ユーザーが `wrap` を指示。辿れるかの確認（引当率）は別セッションに分けると決めた。記録は `topics/logbook-design/` に残し、`9f7a22b` で push 済み。
