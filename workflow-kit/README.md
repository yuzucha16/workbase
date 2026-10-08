# workflow-kit

作業ディレクトリごとに必要になる、共通機能の正本。

共通機能の一覧と呼び出し表は **`hooks.md`（正本）**。`docs/` の仕組み（作業ログと判断ログ）の運用規則は `docs-rules.md`。

## フックの体系（2026-10-08 に決定）

フックは、寿命の階層ごとに、開始と終了の対にする。呼び出し名は英語の短い名前を主にし、日本語の言葉は別名として当面残す（別名は、いま決まっているものだけ。増減は後で揃える）。

呼び出し表は `hooks.md` に移した（2026-10-08。写しを作らない）。寿命の階層: ワークスペース `init`、Project `open`・`close`、セッション `start`・`wrap`、随時 `stock`・`integrate`、週1回の目途 `review`。

連鎖は `init`、`open → [start → 作業 → wrap]×N → close`。`stock` と `integrate` は随時。

- **用語**: スレッド = Claude Code の1会話（フックの対象にしない）。セッション = `start` から `wrap` までの作業手順の単位（1スレッドに複数セッション、複数スレッドで1セッションがありうる）。`open` と `close` は、スレッドでなく Project の寿命。
- **`open` と `start`**: `open` は Project のひな形（`README.md`、`AGENTS.md`）を作ったあとに `start` を呼ぶ。`start` は単独でも呼べる（進行中の Project があるとき）。
- **`end` にしない理由**: 「会話を終える」と取られやすいので、`wrap` にした（ユーザー）。
- **旧ファイル名**: `closing-hook.md`、`knowledge-hook.md`、`setup-hook.md` は、2026-10-08 に削除した（新名は `wrap-hook.md`、`stock-hook.md`、`init-hook.md`）。以下の履歴の旧名は、読み替える。
- **フックの章立て**: 共通部は H2 の `目的と契機` → `場所と書き込みの制約` → `手順` → `報告の型`（この順。新しいフックにも置く）。共通部の中身（冒頭の定型、目的と契機、章の並び、手順の参照、改善、承認、記録、フックを足す・消すとき）は `hook-common.md`。それ以外の章は、フック固有の部分で、共通部の後ろに置く（例外: `入力`、init の `導入項目の一覧`）。`このフックの改善` は、固有の確認項目があるフックだけが持つ任意の章。`tools/check-hook-outline.ps1` で点検する。
- **実測が少ないフック（`start` `open` `close`）**: 叩き台として扱い、実測で直して育てる。作業の種類ごとの差分の項目（`start-hook.md`）は、実測がたまってから設計する。改善の流れは `hook-common.md`。
## 目的

ナレッジと作業ログを分ける。

- ナレッジ: 育てて、次の作業で使う共有知。置き場は `resources/exmem`。
- 作業ログ: 各作業ディレクトリの `docs/`。現在状態、判断の根拠、次にやること。日報・週報・仕様書などの文書の入力にもなる。

この仕組みは、dotfiles、その他のリポジトリ、ワークスペース（Vault のトップ）、`projects/` `areas/` 配下など、どの作業ディレクトリでも同じ。各ディレクトリはコピーを持たず、このディレクトリを参照する。直せば全体に効く。

## 場所

- Windows: `$HOME\works\resources\workflow-kit`
- WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources/workflow-kit`

## 使い方

### 作業ディレクトリに導入する

ユーザーが「workflowを導入して」と言ったら、エージェントは `init-hook.md` に従う。入力は4項目（対象ディレクトリ、目的、読む順番の固有項目、固有ルール）。生成物は `AGENTS.md`、`CLAUDE.md`（`@AGENTS.md`）、`docs/log.md`、`docs/decisions.md`。既存のファイルは上書きせず、差分案を示して承認を得る。導入項目は `init-hook.md` の一覧で管理し、新しい機能はその一覧に足す。

### ワークスペース（Vault のトップ）を作る

新しい PC では、共有リポジトリ `workbase` を `resources/` に clone してから、その中でエージェントに「workflowを導入して」と言い、`init-hook.md` の項目 5 に従う。`workbase` の中で、対象を指定せずに言うと、項目 5 とみなして、既定値（対象 `$HOME\works`、業務用、remote なし、初回コミットする）で作る。作成後の報告に、使った条件（既定値か指定か）を示す。生成物は、`.gitignore`、`.ignore`、`.gitattributes`、ワークスペース用の `AGENTS.md`、PARA の3フォルダ、`git init`（業務用は remote なし）、初回コミット（生成物だけ）。`resources/` の clone と `.obsidian` のリンクは、dotfiles（`50_repos`、`30_link`）が行う。

呼べるのは、`init-hook.md` を参照している `AGENTS.md` の配下（`workbase` の中と、ワークスペースの中）と、ユーザーがパスを指示したとき。他の場所からの入口は、Claude 用スキル（TODO）。

### 「ナレッジ化して」を使う

ユーザーが「ナレッジ化して」と言ったら、エージェントは `stock-hook.md` に従う。単独で言われたときは、知識の抽出だけを行い、`docs/` の更新・棚卸し・コミットは「終了処理して」に任せる（誤入力でも害が小さい）。

### 「終了処理して」と「inboxを整理して」を使う

作業の終わりに、「終了処理して」と言うと、`wrap-hook.md` に従って、現在状態の更新 → 昇格の案 → コミットと push → 報告（終了時の1問）、を順に行う。まとまった知識化は「ナレッジ化して」（`stock-hook.md`）で `exmem/inbox/` に置く。exmem 側で「inboxを整理して」と言うと、`integrate-hook.md` に従って統合する。未統合のメモが5件以上たまったら、`review` が勧める。

## 構成

| ファイル | 役割 |
|---|---|
| `docs-rules.md` | `docs/` の運用規則と、コミットと push の規則 |
| `hook-matrix.md` | フックの網羅度の一覧（各フックが何を書いていて、何を書いていないか。字数の行つき）。足す・消す・章を変えるときの横展開の確認用 |
| `hook-common.md` | 全フックの共通規則: 冒頭の定型、改善の流れ、承認、フックを足す・消すとき |
| `stock-hook.md` | 「ナレッジ化して」の手順・書き方・形式 |
| `wrap-hook.md` | 「終了処理して」の手順（対象の特定、現在状態の更新、昇格の案、コミットと push）・報告の型 |
| `integrate-hook.md` | 「inboxを整理して」の手順（統合、照合の報告、コミット）・報告の型 |
| `review-hook.md` | `review`（別名「見直して」）の手順: `again` と遠回りの事例を見て、1つ直すか1つ畳む。`reviews` の指標 |
| `init-hook.md` | 「workflowを導入して」の導入項目・入力・手順・自己点検・報告の型 |
| `init-workspace.md` | init の導入項目 5（ワークスペースの生成）の作り方。項目 5 のときだけ読む |
| `init-restore.md` | init の導入項目 4（履歴からの復元）の作り方。項目 4 のときだけ読む |
| `open-hook.md` | `open`（Project の開始）の手順: 対象の決定、判断基準での検査、ひな形の作成、Area の一覧の更新。Project の構造 |
| `start-hook.md` | `start`（別名「作業を始めて」。セッションの開始）の手順: 共通の項目と作業の種類の差分でゴールと前提をそろえる |
| `close-hook.md` | `close`（Project の終了）の手順: 完了条件の確認、暫定の見直し、`archives/` への移動 |
| `improvements.md` | 改善提案の記録 |
| `tools/check-inbox.ps1` | inbox のメモの機械的な点検（`stock-hook.md` の「書き方」「形式」のうち、機械で確認できる項目。PowerShell 7）。点検の改善は、フックの改善と同じ手順で回す（`hook-common.md` の「改善」） |
| `tools/find-knowledge.ps1` | `stock-hook.md` の手順「既存の知識と重なるか確認する」の検索（ファイル名・見出し・tags・aliases をキーワード検索。`-Body` で本文の行も検索。読み取り専用。PowerShell 7） |
| `tools/check-hook-outline.ps1` | `*-hook.md` の章立ての共通部（制約、手順、報告の型、改善）の存在と順序の点検、`hooks.md` と README の表にフックが過不足なく載っているかの点検（フックの追加・削除の漏れ止め。PowerShell 7） |
| `templates/` | 導入用の雛形（`AGENTS.md`、`log.md`、`decisions.md`）。`workspace/` はワークスペース（Vault のトップ）用（`AGENTS.md`、`gitignore.template`、`ignore.template`、`gitattributes.template`、`pre-push.template`） |
| `examples/` | 出力の見本（`inbox-example.md`、`setup-example.md`）。出力のブレを抑える基準 |
| `AGENTS.md` | このディレクトリ自体を編集するときのルール |

## TODO（次回以降）

- 手順書本体をさらに薄くする（`stock-hook.md` の手順「知識かどうかを判定する」の例外の細則、`docs-rules.md`）。2026-10-15 の点検と 2026-11-08 の判定の結果を見てから。

- Claude 用スキル（`dotfiles` の `home/.claude/skills/`）。「workflowを導入して」と「ナレッジ化して」の入口にする。スキルは kit のファイルを読むだけにして、手順を重複させない。

## 変更履歴

版番号と README の変更履歴は、2026-10-08 に廃止した。変更の理由は、コミットメッセージに書く（`git log -- workflow-kit/`）。廃止前の README（版 `2026-10-08.5` までの変更履歴 58 件を含む）は、タグ `kit-history-20261008` で読める（`git show kit-history-20261008:workflow-kit/README.md`）。コミットのトレーラー `Kit-Rev` が、規則の時点を示す。
