---
type: knowledge
title: Claude Codeのチャット履歴とメモリの保存場所
status: active
tags:
  - ai/claude
  - tool/zed
  - dotfiles
  - setup
  - harness
  - windows
  - metrics
aliases:
  - Claude Codeの履歴の保存場所
  - Claudeチャット履歴の移行
triggers: [チャット履歴, 会話履歴, メモリ, 保存場所, .claude, jsonl, 履歴の移行, プロジェクトの移動]
created: 2026-10-01
updated: 2026-10-18
sources:
  - Claude Code conversation "Zed 経由で session_id と費用を取る" (2026-10-17。Stop フックによる記録)
  - Claude Code conversation "Claude の応答本文のローカル保存" (2026-10-17。Stop フックによる記録)
  - Claude Code conversation "Claude Code のセッション履歴の復元" (2026-10-07。「履歴の移行と再開」)
  - Claude (Claude Code via Zed ACP) conversation "Claudeチャット履歴の保存場所" (2026-10-01)
  - "$HOME\\.claude\\projects（2026-10-01 に確認）"
  - Claude Code conversation "Vault のトップの rename と certs の移動" (2026-10-06。履歴コピーと `--resume` の結果)
---

# Claude Codeのチャット履歴とメモリの保存場所

## Purpose

Claude Code（ZedのACP経由を含む）のチャット履歴とメモリがどこに保存され、プロジェクトを移動したときにどう引き継ぐかをまとめる。

## 保存場所
<!-- 版依存: 一方向 / 確認: 2026-10-01 -->

2026-10-01 時点で確認済み。

| 中身 | 場所 |
|---|---|
| チャット履歴 | `%USERPROFILE%\.claude\projects\<プロジェクト名>\<session-id>.jsonl` |
| メモリ | `%USERPROFILE%\.claude\projects\<プロジェクト名>\memory\` |
| プロジェクトごとの許可設定 | `<プロジェクト>\.claude\settings.local.json` |

- `<プロジェクト名>` は、プロジェクトの絶対パスの英数字以外（`:` `\` `.` など）を `-` に置き換えたもの。
  - `C:\Users\<ユーザー名>\vault\github.com\yuzucha16\notes` → `C--Users-<ユーザー名>-vault-github-com-yuzucha16-notes`（確認済み）
  - `C:\vault\repos\github.com\yuzucha16\areas_shared` → `C--vault-repos-github-com-yuzucha16-areas-shared`（`_` も `-` になる。確認済み）
- ジャンクション経由のパスは、実体のパスに解決されてから名前になる可能性がある（仮説）。exmemの場合、`C--vault-notes-areas-shared-exmem` と `C--vault-repos-github-com-yuzucha16-areas-shared-exmem` のどちらになるかは未確認のため、2026-10-01 に両方へ履歴とメモリをコピーした。
- 1チャット = 1ファイル。隠しファイルではない。
- プロジェクト直下の `.claude\` にあるのは `settings.local.json` だけで、履歴は入っていない。
- ZedのACP経由のチャットも、Zedの `threads.db` ではなくここに保存される（[[zed-dotfiles]]）。会話の中身はここだが、Zed 側にも `db.sqlite` の `sidebar_threads` があり、スレッドの一覧と作業フォルダはそこにある（2026-10-07 の補足。[[zed-acp]]）。
- Claude Desktop の Projects はクラウド（アカウント側）に保存され、`~/.claude` のローカル履歴とは独立している。
- 履歴から作業の指標を取る方法は [[ai-work-metrics]]。実測の数字は [[ai-work-metrics-log]]。

## jsonl の形式
<!-- 版依存: 一方向 / 確認: 2026-10-06 -->

[[ai-work-metrics]] の Facts から、形式の事実だけを移した（2026-10-26。数字つきの実測は [[ai-work-metrics-log]]）。確認は 2026-10-06、根拠は会話履歴の集計。内部形式なので版で変わりうる（Stop フックの節にも同じ注意がある）。

- 1応答は複数の行に分かれ、同じ `message.id` と同じ `usage` が各行に繰り返される。`message.id` で一意化しないと、トークンを過大計上する。
- ユーザーの実プロンプトと、ツール結果は、どちらも `type` が `user`。ツール結果には `toolUseResult` がある。ほとんどはツール結果。
- 各行に時刻（`timestamp`）、ツール呼び出し、トークン数（`usage`）がある。
- コンテキストの圧縮（compact）の記録は見当たらなかった（`isCompactSummary` と `compact_boundary` の検索）。
- Vault のディレクトリ名を変えて履歴をコピーすると、同じ会話 ID が旧キーと新キーの両方に残る。会話 ID で重複を除く。

## プロジェクトを移動したとき

履歴とメモリはプロジェクトの絶対パスごとに分かれるため、プロジェクトを移動すると前のチャットやメモリが見えなくなる。

引き継ぐ方法の候補は、`projects\<旧プロジェクト名>\` の `.jsonl` と `memory\` を `projects\<新プロジェクト名>\` にコピーすること。ただし、**コピーした履歴は `claude --resume <ID>` で再開できなかった**（確認: 2026-10-06、根拠: Vault のトップを `C:\vault\notes` から `C:\vault\works` へ移したときのユーザーの発言。エラーの内容は未取得）。再開の条件は未特定。移動後は、新規のセッションを始める運用を基本にする。（2026-10-07 に解決: 原因は、picker が SDK 経由のセッションを除外していたことと、`cwd` が旧パスだったことの2つ。手順は下の「履歴の移行と再開」。）
- 旧キーは消さず、コピーで行う。旧キーが唯一の確実な履歴になる。
- コピーした `.jsonl` には、旧パスの `"cwd"`（`C:\\vault\\notes\\...` と `/c/vault/notes/...` の2形式）が入っている。`"cwd"` を新パスに書き換えて再コピーしても、再開できなかった。「`cwd` の不一致が原因」は、`cwd` だけでは足りないことが分かった。（2026-10-07 の注: 当時は一覧から開いていて、`claude --resume <ID>` で直接開けば通っていた可能性がある。仮説。未確認。）
- `cwd` を書き換えた後も、旧パスが約 1180 件残っていた。内訳は、user メッセージ 941（ほぼツールの出力）、assistant 188、`attachment` 14（`edited_text_file` 8、`instructions` 4、`environment` 2）、`last-prompt` 7。構造的な情報にあたるのは `attachment` の `environment` と `instructions` の約6件で、残りは会話の中身。再開の可否にどれが関わるかは未検証。
- 履歴全体の置換はしない。会話の内容が「`works` を `works` に」のように壊れ、記録として不適切になる。試すなら、コピーした一時キーで、構造的な部分だけを書き換える。
- 旧パスが本文に残ったまま再開できた場合の実害は、モデルが旧パスを現在のパスと取り違えて、旧ディレクトリを作り直すこと（仮説）。
- 旧パスのディレクトリを残して（または作り直して）、そこを cwd にすれば旧キーの履歴は再開できる（仮説。未試験）。旧 clone のディレクトリを削除すると、その cwd での再開ができなくなる。

2026-10-01 に、作業拠点を `C:\Users\<ユーザー名>\vault\notes` から `C:\vault\notes\areas_shared\exmem` へ移すときにこの方法を使った（`C--Users-<ユーザー名>-vault-notes` → `C--vault-notes-areas-shared-exmem`）。コピーした履歴が新しい場所で表示されるかは、未確認のまま（上の 2026-10-06 の結果から、再開は通らない可能性が高い。仮説）。

Claude Codeを起動して `projects\` に別の名前のフォルダができた場合は、プロジェクト名の仮説が外れている。そのフォルダへ `.jsonl` と `memory\` をコピーし直す。

## 履歴の移行と再開（2026-10-07 追記）

作業フォルダを別のパスへ移したあと、旧パスで作った約56本のセッション（jsonl）を、新しい構成で `claude --resume` から再開できるようにした。上の「プロジェクトを移動したとき」で未解決だった原因と、安全な手順。

### Principles（履歴の移行）

- 移動後に再開できないときは、「一覧（picker）に出ない」と「ID 指定でも読めない」を分けて調べる。理由: 今回の「再開できない」は、picker が一部のセッションを除外していたことと、`cwd` が旧パスだったことの2つが重なっていた。
- 内部形式の書き換えは、先に履歴フォルダ全体をバックアップし、書き換えるのは `cwd` や `entrypoint` などのメタ項目だけにする。理由: jsonl の形式は公式の手順ではなく、会話本文のパスを置換すると記録が壊れる。
- 履歴の復元は、非対話の `claude -p --resume <ID> --fork-session` で、読み込めるかを先に確かめる。理由: 元のセッションを変えずに、一覧に出ない原因と、読み込めない原因を切り分けられる。

### Decisions（履歴の移行。すべて 2026-10-07）

- **旧パスのセッションの `cwd` を、現在の構成に対応するパスへ書き換え、対応する保存先ディレクトリに置く**。根拠: 保存先ディレクトリ名は `cwd` から計算され、再開はそのディレクトリだけを探す。ユーザーが「できるだけ、現構造に `cwd` を一致させたい」と指示した。却下案: 旧パスのディレクトリを作り直して、そこを `cwd` にする（旧構成が残り、現在の構成と一致しない）。
- **対応先が現在の構成に無いセッションは、共有の知識置き場（exmem）の `cwd` に寄せる**。根拠: ユーザーが「寄せてください。だめならあきらめます」と指示した。一覧に出す場所が必要だった。却下案: 対応先が無いものは諦める（会話が読めなくなる）。
- **`entrypoint` を `sdk-ts` から `cli` に書き換える（1本で試してから全件）**。根拠: CLI の picker は SDK 経由のセッションを出さないため。ユーザーが1本で picker に出ることを確認してから、全件の書き換えを指示した。却下案: 毎回 `claude --resume <ID>` で指定する（一覧から選べず、ID の控えが要る）。

### Facts（履歴の移行）
<!-- 版依存: 一方向 / 確認: 2026-10-07 -->

- CLI の picker と `--continue` は、`claude -p` と Agent SDK で作ったセッションを除外する。ID を直接指定すれば再開できる（確認: 2026-10-07、根拠: 公式ドキュメント `code.claude.com/docs/en/sessions`）。
- Zed の ACP 経由のセッションは SDK 経由で、jsonl の `entrypoint` は `sdk-ts` だった。調べた54本すべてが `sdk-ts`（確認: 2026-10-07、根拠: jsonl の `entrypoint` を集計）。統合時（2026-10-08）の集計では、先頭付近の `entrypoint` が `sdk-ts` のファイルが62、`cli` が55（`projects` 全体のファイル数で、旧キーのコピーを含む。新しい Zed のセッションは `sdk-ts` で作られるとみられるが、再現は未実施）。
- 一覧に何も出なくても、`claude -p --resume <ID> --fork-session` は応答した（確認: 2026-10-07、根拠: 実行して `OK` が返った）。テストで増えたフォーク用の jsonl は削除した。
- `entrypoint` を `cli` に1本書き換えたら picker に出た。全件を `cli` にしたあとも、Zed のスレッド履歴から開けた（確認: 2026-10-07、根拠: ユーザーの報告）。
- 保存先ディレクトリ名は、`cwd` の英数字以外（`:` `\` `.` `_`）を `-` に置換したもの。`.obsidian` は `--obsidian` になる（確認: 2026-10-07、根拠: 移行後に picker と Zed で開けた。2026-10-08 に `projects` の一覧で `…-windows-obsidian--obsidian` を確認）。
- `claude --resume <ID>` は、現在のプロジェクト、他のプロジェクトの順に ID を探す。他のプロジェクトに同じ ID の transcript が複数あると、どれも選ばず not found になる（確認: 2026-10-07、根拠: 公式ドキュメント。実機では、重複がある状態の検証は未実施）。
- `cwd` が `.jsonl` の JSON 行ごとに入っていて、`"cwd":"C:\\..."` の形（バックスラッシュ2重）と `/c/...` の形の2通りがある（確認: 2026-10-07、根拠: jsonl の集計）。
- `projects` の保存先に、コピー前後の同じセッション ID が複数ディレクトリにあると、ディスク上のセッション数が水増しされる。ユニークな ID は56本だった（確認: 2026-10-07、根拠: ファイル名の集計）。

### Gotchas（履歴の移行）

- **作業フォルダを移したあと、`claude --resume` の画面に何も出ない（`No conversations found in this project`、または検索欄だけ）**: セッションが SDK 経由（`entrypoint: sdk-ts`）で、picker の対象外。`cwd` の不一致とは別の原因。`claude --resume <ID>` で開く。一覧から選びたいときは、`entrypoint` を `cli` に書き換える。
- **コピーしたセッションが、新しい場所で再開できない**: jsonl の `cwd` が旧パスのまま。旧パスが存在しないと、作業ディレクトリを決められない（仮説）。`cwd` の値だけを、新パスに書き換える。会話本文のパスは触らない。

### Open Questions（履歴の移行）

- 旧ディレクトリに同じセッションが残っている状態で、別のディレクトリから ID 再開すると not found になるか（公式の記述だけ。未検証）。

### Next Actions（履歴の移行）

- 数日使って問題が無ければ、履歴のバックアップと、旧ディレクトリの重複を削除する（2026-10-07 時点。旧 `C--vault-works*` のキーが残っていることを 2026-10-08 に確認）。

## Stop フックによる記録（2026-10-18 追記）

Claude Code（Zed の ACP 経由を含む）で、セッションの費用・ID と応答本文を、フックの入力と transcript から取る方法。2026-10-17 の2つの会話（費用の記録、応答本文の保存）の統合。

### Principles（Stop フックによる記録）

- 会話の中でスラッシュコマンドや `claude -p` の出力に頼らず、フックが受け取る入力と transcript で代える。理由: スラッシュコマンドはユーザーが打つもので AI が実行できず、`claude -p` は別セッションの値を返す。
- 毎回の記録は、モデルを通さないフック（Stop）で行い、標準出力に何も出さない。理由: AI の手順の最後に足すと往復が1回増え、会話全体のキャッシュ読みの分だけ費用が増える（1回あたり約1.6円、キャッシュ切れで約40円）。
- 費用は「推定」と明記して記録し、正は `/usage` にする。理由: transcript にない内部の呼び出しがあり、実測で数%低く出る。
- 会話の記録を後から取り出す用途には、非公開の内部形式（`.jsonl`）を解析するより、公式が値を渡すフックの入力を使う。理由: 公式が「形式は内部用で版ごとに変わる」と明記しており、解析スクリプトは版が上がると壊れうる。
- 「保存する量」と「画面に出す量」は別の問題として分けて扱う。理由: 保存は Stop フックなど出力に触れない仕組みで足りるが、画面の見づらさは表示設定（`/focus` など）でしか変えられない。

### Decisions（Stop フックによる記録）

- **セッションの費用と ID は、Stop フックのスクリプトで記録する**（2026-10-17）
  - 根拠: ユーザーの依頼（「stop フックの方向で手順作成を」）。
  - 却下案: 手順書の最後に AI が集計を実行（往復が増える）、statusline（Zed に表示されない）、`claude -p` の JSON（別セッションの値）。

### Facts（Stop フックによる記録）
<!-- 版依存: 一方向 / 確認: 2026-10-17 -->

費用と ID:

- Stop フックの入力には `session_id`、`transcript_path`、`cwd`、`last_assistant_message` があり、費用や使用量の項目は無い（確認: 2026-10-17、根拠: `claude -p` で Stop フックを動かして入力 JSON を保存して見た）。
- Stop フックの標準出力は、会話に入らない。公式の文面からの読み取りで、実測では出力した目印が応答に現れなかった（仮説）。
- transcript の `assistant` 行は同じ `message.id` が複数あるため、id で重複を除いて合計する。単価は、入力・出力・キャッシュ読み・キャッシュ書き込み（1時間と5分で別）に分けて掛ける。Haiku 5.5 は、1リクエストの入力が10万トークンを超えると高い単価になる（確認: 2026-10-17、根拠: 公式の価格表。`claude -p` の `modelUsage` の値で Haiku の1リクエストを手計算し、$0.0027926 と一致）。
- transcript の集計は、`claude -p` の費用より約3%低かった（0.0027 対 0.00279）。transcript にない内部の呼び出しがあるため（確認: 2026-10-17、根拠: 同じ実行の `modelUsage` の入力トークン 1172 に対し、transcript は 2）。
- ACP アダプタ（`@agentclientprotocol/claude-agent-acp` 0.93.0）は、`/usage` を対応コマンドとして返し（セッションの費用、トークンの内訳、プランの利用枠）、`/cost` を非対応にしている。毎ターン `usage_update`（コンテキスト使用量と費用 USD）をクライアントに送る。設定は user・project・local を読む（確認: 2026-10-17、根拠: 配布物の `dist/acp-agent.js` を読んだ）。
- 環境変数 `CLAUDE_CODE_SESSION_ID` は、クラウド環境では設定されていたが、公式の環境変数のページには載っていない（確認: 2026-10-17、根拠: `env` の出力と公式ページの前半）。

応答本文:

- Stop フックの入力に `last_assistant_message`（Claude の最後の応答のテキスト）がある。ツール呼び出しやその結果は入らない（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの Stop の節と、`claude -p` で Stop と MessageDisplay の両フックを動かした実測。途中の一言は Stop に入らず、最後の報告だけが入った）。
- 公式は、`transcript_path` の JSONL は非同期に書かれ、Stop の時点で最後の発言が入っていないことがあるので、直近の応答は `last_assistant_message` から取るよう勧めている（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの共通入力フィールドの節）。
- Stop フックは、ユーザーが中断（Esc）したターンでは動かず、API エラーのときは代わりに StopFailure が動く（確認: 2026-10-17、根拠: 公式 hooks ドキュメントの Stop の節）。
- MessageDisplay フックは、表示される本文を受け取る。対話モードでは行のまとまりごとに何度も呼ばれ、フックが返るまで表示が止まる。実測（`claude -p`）では途中の一言も最後の報告も、どちらも渡された（確認: 2026-10-17、根拠: 公式ドキュメントと上の実測）。
- `/export <ファイル名>` は会話全体を、ツール出力も含めてテキストで書き出す。`/copy` は最後の応答をクリップボードへ送り、ピッカーで `w` を押すとファイルに書ける（確認: 2026-10-17、根拠: 公式 commands と sessions ドキュメント）。
- output styles は応答の役割・口調・形式を変えるだけで、ファイルへ書き出す機能は無い（確認: 2026-10-17、根拠: 公式 output-styles ドキュメント）。
- WSL2 の対話モードで、Stop フックの `last_assistant_message` が `claude -p` と同じ内容になる（仮説）。補足: 公式の説明からの推測で、対話モードは試していない。

画面の表示:

- `/focus` は、直前の発言、ツール呼び出しの1行の要約（編集は追加・削除の行数だけ）、最後の応答だけを出す。fullscreen の描画（`/tui fullscreen`、試験提供中）が必要で、`viewMode: "focus"` で固定できる。`Ctrl+O` で全体を見られる（確認: 2026-10-17、根拠: 公式 commands、fullscreen、settings-reference ドキュメント。実機の表示は未確認）。
- `bashEditDiffEnabled: false`（ユーザー設定）または環境変数 `CLAUDE_CODE_BASH_EDIT_DIFF=0` で、Bash の実行後に出る変更ファイルの差分を止められる。止めると PostToolUse の Bash フックにも変更ファイルの一覧が渡らない（確認: 2026-10-17、根拠: 公式 settings-reference と env-vars ドキュメント）。
- Edit ツールの差分を、通常の表示のまま隠す設定は、公式ドキュメントに見つからなかった（確認: 2026-10-17、根拠: settings-reference と interactive-mode ドキュメントを検索）。

### Gotchas（Stop フックによる記録）

- **transcript を集計して費用を出そうとした**: 公式は「transcript の形式は内部用で版ごとに変わる」「Stop の時点で最後の発言が入っていないことがある」と書いている。集計は `message.id` と `usage` の2項目だけに依存させ、失敗しても作業を止めない（exit 0）作りにした。最新のターンの遅れは次のターンで追いつく。
- **最後の応答だけを残すつもりで Stop フックを使う**: 長い説明を書いた後にツールを呼び、短い一言で終わると、その一言しか `last_assistant_message` に入らない。途中で書いた本文は残らない。途中の本文も残したいなら MessageDisplay フックを使う（ただし途中の一言も全部入り、表示が止まる分の遅延が出る）。または、長い報告は最後の応答にまとめるよう指示する。

### Open Questions（Stop フックによる記録）

- Zed 経由で Stop フックが動くか。アダプタが設定を読むのでコード上は動くはずだが、実機では未確認。
- WSL2 の対話モードで入力が同じ形か。
- サブエージェントの分が、メインの transcript に入るか。
- 提案: 画面の見づらさは、まず `/focus` を試す（AI の提案。未承認）。
- `/focus` で、直前のターンより前の過去ログがどう見えるか。

### Next Actions（Stop フックによる記録）

- Zed の1往復で、記録のファイルが更新されるか確かめる（2026-10-17 時点）。
- 実機の `/usage` の費用と、推定の費用を比べる（2026-10-17 時点）。
- 提案した Stop フックを、実際の環境で動かして確かめる（2026-10-17 時点）。
- `/focus` を試して、見え方を確かめる（2026-10-17 時点）。

## Decisions

### チャット履歴（`.jsonl`）はdotfilesに含めない（2026-10-01）

- 根拠: サイズが大きくなりやすく、会話の中身がそのまま入っている。
- 却下案: `~/.claude` 全体をdotfilesに入れる。

## Gotchas

### `.claude` をコピーしたのに、移動先でチャットが見えない

- 原因: コピーしたのはプロジェクト直下の `.claude`（設定のみ）だった。履歴はユーザーフォルダ直下の `%USERPROFILE%\.claude\projects\` にある。名前が同じ別のフォルダ。
- 解決: ユーザーフォルダ側の `projects\<旧プロジェクト名>\*.jsonl` を `projects\<新プロジェクト名>\` にコピーする。

### `.jsonl` が見つからない

- 原因: プロジェクト内の `.claude` を見ていた。隠し属性ではない。
- 解決: エクスプローラーのアドレスバーに `%USERPROFILE%\.claude\projects` を入力して開く。

### Zedで exmem のセッションを立てても、exmem として動かない

- 状況: Zedのワークスペースが `C:\vault` のまま、Claude Agentのチャットに exmem のパスや `cd notes/areas_shared/exmem` と書いた。セッションは `C:\vault` を作業フォルダとして動き、履歴は `C--vault` に保存された。exmemの `CLAUDE.md` も読まれなかった。
- 原因: ZedのClaude Agentは、Zedで開いているプロジェクトのルートを作業フォルダにして起動する。チャットでの `cd` では変わらない。
- 解決: exmemをZedのプロジェクトとして開き直す（`zed C:\vault\notes\areas_shared\exmem`、または File > Open で exmem フォルダを選ぶ）。その上で新しいThreadを作る。

### Zedで `/resume` が使えない

- 原因: `/resume` はターミナル版Claude Codeのコマンドで、ZedのACP経由では使えない。
- 解決: 過去のチャットを再開するときは、ターミナルで作業フォルダに移動してから `claude --resume` を実行する。

### コピーした履歴が、新しいパスで `claude --resume` できない

- 状況: Vault のトップを `C:\vault\notes` から `C:\vault\works` に rename したとき、履歴を新キー（`C--vault-works-*`）へコピーして `claude --resume <ID>` したが、再開できなかった。`"cwd"` を書き換えて再コピーしても同じだった（2026-10-06）。
- 原因: 不明（2026-10-06 時点）。`cwd` の不一致だけではない。`cwd` 以外のフィールドの旧パス（上の「プロジェクトを移動したとき」）、キーの付け方、セッションの索引が候補（未調査）。
- 解決: 2026-10-06 時点はなし。新しいパスでは、新規のセッションを始める。旧キーの履歴は残してある。2026-10-07 に解決した（原因は picker が SDK 経由のセッションを除外していたこと。上の「履歴の移行と再開」）。

### Claude Desktop の Projects に履歴が出ない

- 原因: 不具合ではない。Desktop の Projects はクラウド、Claude Code の履歴はローカルで、保存先が別。

## Open Questions

- `~/.claude` の手書き設定のうち、`settings.json` は管理済み（dotfiles が管理。WSL・Windowsとも適用済み、2026-10-04 に確認。[[claude-code-permissions]]）。`CLAUDE.md` と `projects\<プロジェクト名>\memory\` をdotfilesで管理するかは未決。
- Claude Desktop の Code 機能から、ローカルの履歴が見えるか。

## Next Actions

- ターミナルで `$HOME\works\resources\exmem`（2026-10-06 以前は `C:\vault\works\resources\exmem`）に移動して `claude --resume` を実行し、コピーした履歴が表示されるか確認する。あわせて、`projects\` のどちらのフォルダに書き込まれるかを確認し、使われなかった方を削除する。

## Related

- [[zed-dotfiles]]
- [[zed-acp]]
- [[obsidian-vault]]
- [[claude-code-project-settings]]
- [[ai-work-metrics]]
