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
- **試験運用（`start` `open` `close`）**: 実測が少ないので、叩き台として扱う。作業の種類ごとの差分の項目（`start-hook.md`）は、実測がたまってから設計する。改善は、呼び出し元の `docs/metrics/events.csv` に記録し、ユーザーの承認後に直す。
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

ユーザーが「workflowを導入して」と言ったら、エージェントは `setup-hook.md` に従う。入力は4項目（対象ディレクトリ、目的、読む順番の固有項目、固有ルール）。生成物は `AGENTS.md`、`CLAUDE.md`（`@AGENTS.md`）、`docs/log.md`、`docs/decisions.md`。既存のファイルは上書きせず、差分案を示して承認を得る。導入項目は `setup-hook.md` の一覧で管理し、新しい機能はその一覧に足す。

### ワークスペース（Vault のトップ）を作る

新しい PC では、共有リポジトリ `workbase` を `resources/` に clone してから、その中でエージェントに「workflowを導入して」と言い、`setup-hook.md` の項目 5 に従う。`workbase` の中で、対象を指定せずに言うと、項目 5 とみなして、既定値（対象 `$HOME\works`、業務用、remote なし、初回コミットする）で作る。作成後の報告に、使った条件（既定値か指定か）を示す。生成物は、`.gitignore`、`.ignore`、`.gitattributes`、ワークスペース用の `AGENTS.md`、PARA の3フォルダ、`git init`（業務用は remote なし）、初回コミット（生成物だけ）。`resources/` の clone と `.obsidian` のリンクは、dotfiles（`50_repos`、`30_link`）が行う。

呼べるのは、`setup-hook.md` を参照している `AGENTS.md` の配下（`workbase` の中と、ワークスペースの中）と、ユーザーがパスを指示したとき。他の場所からの入口は、Claude 用スキル（TODO）。

### 「ナレッジ化して」を使う

ユーザーが「ナレッジ化して」と言ったら、エージェントは `knowledge-hook.md` に従う。単独で言われたときは、知識の抽出だけを行い、`docs/` の更新・棚卸し・コミットは「終了処理して」に任せる（誤入力でも害が小さい）。

### 「終了処理して」と「inboxを整理して」を使う

作業の終わりに、「終了処理して」と言うと、`closing-hook.md` に従って、`docs/` 更新 → 棚卸し → ナレッジ化 → コミット → 統合待ちの報告、を順に行う。統合待ち（メモが5件以上、または `転記待ち` が15件以上）と報告されたら、exmem 側で「inboxを整理して」と言うと、`integrate-hook.md` に従って統合し、`転記待ち` を `転記済` に進める案が出る（承認制）。ソース側が統合待ちを知らせ（push）、exmem 側が統合する、という分担。

## 構成

| ファイル | 役割 |
|---|---|
| `docs-rules.md` | `docs/` の運用規則と、コミットと push の規則 |
| `knowledge-hook.md` | 「ナレッジ化して」の手順・書き方・形式、改善フック |
| `closing-hook.md` | 「終了処理して」の手順（対象の特定、`docs/` 更新、棚卸し、ナレッジ化、コミット、統合待ちの報告）・報告の型 |
| `integrate-hook.md` | 「inboxを整理して」の手順（統合、行き先の検索、`転記済` への案、承認、コミット）・報告の型 |
| `review-hook.md` | `review`（別名「見直して」。試験運用）の手順: 自動採用の規則の見直し、台帳による転記の一括確定、`reviews.csv` の指標 |
| `setup-hook.md` | 「workflowを導入して」の導入項目・入力・手順・自己点検・報告の型 |
| `improvements.md` | 改善提案の記録 |
| `tools/check-inbox.ps1` | inbox のメモの機械的な点検（`knowledge-hook.md` の自己点検のうち、機械で確認できる項目。PowerShell 7）。点検の改善は、フックの改善と同じ手順で回す（`knowledge-hook.md` の「点検スクリプトの改善」） |
| `tools/check-docs.ps1` | `docs/decisions.md` の項目の、ラベルと行き先の点検（`docs-rules.md` の「decisions.md の項目の行き先」。行き先の欠落、不正な状態、転記待ちの上限20件。PowerShell 7） |
| `tools/item-hash.ps1` | `decisions.md` の項目の本文ハッシュ（`転記待ち` の行に記録し、`review` が、項目が転記待ちの後に変わっていないかを見る。読み取り専用。PowerShell 7） |
| `tools/find-knowledge.ps1` | `knowledge-hook.md` 手順 5 の既存知識の検索（ファイル名・見出し・tags・aliases をキーワード検索。`-Body` で本文の行も検索。読み取り専用。PowerShell 7） |
| `templates/` | 導入用の雛形（`AGENTS.md`、`log.md`、`decisions.md`）。`workspace/` はワークスペース（Vault のトップ）用（`AGENTS.md`、`gitignore.template`、`ignore.template`、`gitattributes.template`、`pre-push.template`） |
| `examples/` | 出力の見本（`inbox-example.md`、`setup-example.md`）。出力のブレを抑える基準 |
| `AGENTS.md` | このディレクトリ自体を編集するときのルール |

## TODO（次回以降）

- `review` に、チェック機能を集約していく（いまは、自動採用の規則の見直しと、転記の一括確定だけ。`wrap` の棚卸し `check-docs.ps1` などは、実測してから1つずつ移す）。

- Claude 用スキル（`dotfiles` の `home/.claude/skills/`）。「workflowを導入して」と「ナレッジ化して」の入口にする。スキルは kit のファイルを読むだけにして、手順を重複させない。

## 変更履歴

版番号と README の変更履歴は、2026-10-08 に廃止した。変更の理由は、コミットメッセージに書く（`git log -- workflow-kit/`）。廃止前の README（版 `2026-10-08.5` までの変更履歴 58 件を含む）は、タグ `kit-history-20261008` で読める（`git show kit-history-20261008:workflow-kit/README.md`）。コミットのトレーラー `Kit-Rev` が、規則の時点を示す。
