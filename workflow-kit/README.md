# workflow-kit

作業ディレクトリごとに必要になる、共通機能の正本。

共通機能の一覧と呼び出し表は **`hooks.md`（正本）**。`docs/` の仕組み（作業ログと判断ログ）の運用規則は `docs-rules.md`。

## フックの体系（2026-10-08 に決定）

フックは、寿命の階層ごとに、開始と終了の対にする。呼び出し名は英語の短い名前を主にし、日本語の言葉は別名として当面残す（別名は、いま決まっているものだけ。増減は後で揃える）。

呼び出し表は `hooks.md` に移した（2026-10-08。写しを作らない）。寿命の階層: セッション `brief`・`wrap`、随時 `stock`・`integrate`、週1回の目途 `review`。works の作成（`room mkworks`）と Project の開始・終了（`room open` `room close`）は、決まった手順の副作用なので、合言葉でなく人が打つ `room` のコマンドにした（2026-10-24。`init` `open` フックを廃止）。

連鎖は `[brief → 作業 → wrap]×N`。`stock` と `integrate` は随時。

- **用語**: スレッド = Claude Code の1会話（フックの対象にしない）。セッション = `brief` から `wrap` までの作業手順の単位（1スレッドに複数セッション、複数スレッドで1セッションがありうる）。Project の寿命は `room open` から `room close` まで（スレッドとは別）。
- **`end` にしない理由**: 「会話を終える」と取られやすいので、`wrap` にした（ユーザー）。
- **フックの章立て**: 共通部は H2 の `目的と契機` → `場所と書き込みの制約` → `手順` → `報告の型`（この順。新しいフックにも置く）。共通部の中身（冒頭の定型、目的と契機、章の並び、手順の参照、改善、承認、記録、フックを足す・消すとき）は `hook-common.md`。それ以外の章は、フック固有の部分で、共通部の後ろに置く（例外: `入力`）。`このフックの改善` は、固有の確認項目があるフックだけが持つ任意の章。`tools/check-hook-outline.ps1` で点検する。
- **実測が少ないフック（`brief`）**: 叩き台として扱い、実測で直して育てる。作業の種類ごとの差分の項目（`brief-hook.md`）は、実測がたまってから設計する。`brief 解決` / `brief 改善` / `brief 調査` は試験運用（実測してから、インタビューとの関係を決める）。フックの成熟度は、ここだけに書く。改善の流れは `hook-common.md`。
## 目的

ナレッジと作業ログを分ける。

- ナレッジ: 育てて、次の作業で使う共有知。置き場は `resources/exmem`。
- 作業ログ: 各作業ディレクトリの `docs/`。現在状態、判断の根拠、次にやること。日報・週報・仕様書などの文書の入力にもなる。

この仕組みは、dotfiles、その他のリポジトリ、works、`projects/` `areas/` 配下など、どの作業ディレクトリでも同じ。各ディレクトリはコピーを持たず、このディレクトリを参照する。直せば全体に効く。

## 場所

- Windows: `$HOME\works\resources\workflow-kit`
- WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources/workflow-kit`

## 使い方

### works を作る

新しい PC では、共有リポジトリ `workbase` を `resources/` に clone してから（dotfiles の `50_repos`）、人が端末で `uv run room.py mkworks` を打つ（`resources/workflow-kit/room/` の中で。AI は実行しない）。既定は、対象 `$HOME\works`（`--vault` か `$ROOM_VAULT` で変える）、業務用、remote なし、初回コミットする。生成物は、`.gitignore`、`.ignore`、`.gitattributes`、`.claude/settings.json`、works 用の `README.md` と `AGENTS.md`、`CLAUDE.md`、`docs/`、PARA の3フォルダ、`resources_p/`（PC ローカルの resources。追跡しない）、`git init`（業務用は remote なしで、`pre-push` で push を止める）、初回コミット（生成物だけ）。`.obsidian` のリンクは dotfiles（`30_link`）が行う。雛形が変わったら `mkworks --update` で既存の works に反映する。詳しくは `room/README.md`。

他のリポジトリ（dotfiles など）に `AGENTS.md` `CLAUDE.md` `docs/` を入れる操作は、フックにしない（2026-10-24 に廃止）。`templates/AGENTS.md` `log.md` `decisions.md` を手本に、手で、または AI に頼んで作る。環境移行などで繰り返し必要になったら、改めて決める。

### 「ナレッジ化して」を使う

ユーザーが「ナレッジ化して」と言ったら、エージェントは `stock-hook.md` に従う（AI 用。人用の理解ガイドは「理解ガイドにして」＝`stock 理解`で、`stock-explain.md` も読む。`stock` だけなら1問で選ばせる）。単独で言われたときは、知識の抽出だけを行い、`docs/` の更新・棚卸し・コミットは「終了処理して」に任せる（誤入力でも害が小さい）。

### 「終了処理して」と「inboxを整理して」を使う

作業の終わりに、「終了処理して」と言うと、`wrap-hook.md` に従って、現在状態の更新 → 昇格の案 → コミットと push → 報告、を順に行う。まとまった知識化は「ナレッジ化して」（`stock-hook.md`）で `exmem/inbox/` に置く。exmem 側で「inboxを整理して」と言うと、`integrate-hook.md` に従って統合する。未統合のメモが5件以上たまったら、`review` が勧める。

## 構成

| ファイル | 役割 |
|---|---|
| `docs-rules.md` | `docs/` の運用規則 |
| `commit-push-rules.md` | コミットと push の規則（身元・トレーラー、push の条件、しないこと） |
| `hook-matrix.md` | フックの網羅度の一覧（各フックが何を書いていて、何を書いていないか。字数の行つき。Must/Want の区分つき）。足す・消す・章を変えるときの横展開の確認用。`review` が週1回確認する |
| `token-matrix.md` | トークン消費の星取り表（切る・絞る・予算・外部化）と点の履歴。`review` が自己採点し、前回より点が下がったら見直す |
| `methods.md` | 解決・改善・変更・調査のやり方の要点の表(選ぶ基準・骨子・詳細ノートへの参照)。`brief 解決` / `brief 改善` / `brief 調査` が読む。詳細は `exmem/lessons/` |
| `hook-common.md` | 全フックの共通規則: 冒頭の定型、改善の流れ、承認、フックを足す・消すとき |
| `approval-screening.md` | 仕組みの決定を `review 消化` で承認する手順: 待ち行列・サブエージェントのスクリーニング・最終判断の3段、覆しの型 A〜E、仮決めの期限 |
| `stock-hook.md` | 「ナレッジ化して」（`stock ナレッジ`）の手順・書き方・形式。モードの選び方（合言葉だけなら1問） |
| `stock-explain.md` | `stock 理解`（別名「理解ガイドにして」）の違う点: 判定の問い、`kind: explain` の6見出し、統合先。見本は `examples/inbox-example-explain.md` |
| `wrap-hook.md` | 「終了処理して」の手順（対象の特定、現在状態の更新、昇格の案、コミットと push）・報告の型 |
| `integrate-hook.md` | 「inboxを整理して」の手順（統合、照合の報告、コミット）・報告の型 |
| `review-hook.md` | `review`（別名「見直して」）の手順: 遠回りの事例を見て、1つ直すか1つ畳む。`reviews` の指標 |
| `project-structure.md` | Project の構造: type（`dev` `inv`）の考え方、固定の核（`ai/` と `_noai/`）、type ごとの置き場、基準文書の置き場。`room open` の type の決定と、置き場に迷ったときに読む |
| `brief-work-types.md` | 作業の種類の差分（開発、文書作成）: `brief-hook.md` の手順「項目を埋める」で、インタビューの項目に加えて聞く項目 |
| `brief-plan.md` | 計画のやり方（`brief 計画`。試験運用）の手順と欄の定義: 6R → 憲章 → 成果物 WBS → マイルストーン |
| `dev-deliverable-guide.md` | `type: dev` の成果物（`ai/out/<成果物名>/`）の作り方: 成果物の形ごとの構成要素の選び方、守ること、文書、テスト、変更の依頼、立ち上げ・完了のチェック。環境構築（`env/` が主）とテストだけ（`tests/` だけ）の成果物の差分も持つ。`type: dev` の Project の立ち上げ（`room open` と最初の `brief`）のときに読む |
| `script-guide.md` | スクリプトや変換を作る・動かすときの規約（全 type 共通）: 言語の選び方（Python → ps1 → bat。AI は聞かずに決める）、実行の方針（部屋で完結できるなら部屋で実行する。Windows 依存部は小さな層にして人の手数を減らす）、Windows で実行するスクリプト（束ねる役も同じ言語、bat は起動用の 3 行だけ）。スクリプトを書く・動かすときに読む |
| `brief-hook.md` | `brief`（別名「作業を始めて」。セッションの開始）の手順: インタビューの項目と作業の種類の差分でゴールと前提をそろえる |
| `improvements.md` | 改善提案の記録（2026-10-15 に凍結。以後は `docs/decisions.md`） |
| `tools/check-inbox.ps1` | inbox のメモの機械的な点検（`stock-hook.md` の「書き方」「形式」と `stock-explain.md` のうち、機械で確認できる項目。frontmatter の `kind` で項目が切り替わる。PowerShell 7）。点検の改善は、フックの改善と同じ手順で回す（`hook-common.md` の「改善」） |
| `tools/check_inbox.py`、`tools/find_knowledge.py` | 上の2つの Python 版（標準ライブラリだけ。`pwsh` が無い環境、例: AI 作業部屋用）。出力は同じ（確認: 2026-10-17、現在のメモと検索で一致。違いは、`check_inbox.py` が英小文字の検査で大文字を通さないこと）。点検の項目を変えるときは、両方を直す |
| `tools/usage_report.py`、`tools/usage_report_html.py`、`tools/usage_prices.json` | Claude Code のセッションログから、トークン使用量と概算費用($)を週次・月次で集計する（ターミナル表示と HTML）。単価表は公式の料金ページの値（出典・取得日つき）。読み取り専用、標準ライブラリだけ。使い方は `guides/howto/claude-usage-report.md` |
| `tools/find-knowledge.ps1` | `stock-hook.md` の手順「既存の知識と重なるか確認する」の検索（ファイル名・見出し・tags・aliases をキーワード検索。`-Body` で本文の行も検索。ファイルの大きさと、ヒットした見出しの節の行の範囲を返す。読み取り専用。PowerShell 7） |
| `tools/check_py.py` | Windows で実行する Python スクリプト（`.py` と、`uv run --script` で呼ぶ起動用 `.bat`）を、実行せずに点検する（2026-10-21。標準ライブラリだけ。UTF-8、改行、構文、ruff〔あれば〕、起動用 bat の 3 行の型、束ねる役の `--log` 機能、bat の名前が `run` / `verify` / `release`、`verify.py` と `run.py` の結果ファイル（`<名前>-result.json`）。`--run-tests` で `test*.py` を unittest で実行）。規約は `script-guide.md` の「Python の薄い層」。終了コードは FAIL の数。pwsh を呼ぶ bat は対象外（下の `check-ps1.ps1` の担当）。確認: 良い例が通り、悪い例（構文エラー、cp932、ロジックのある bat、呼び先なし、pause なし）を検出した（Windows の Python 3.13） |
| `tools/check-ps1.ps1` | Windows で実行するスクリプト（`.ps1` と、それを呼ぶ起動用 `.bat`。Python が使えないときの例外の層）を、実行せずに点検する（2026-10-21。PowerShell 7。文字コード、改行、構文、`#Requires -Version 7`、`$ErrorActionPreference`、`Set-StrictMode`、PSScriptAnalyzer、起動用 bat の 3 行の型、束ねる ps1 が、`-Log` のときだけ `ai/work/<名前>.log` に出すログ機能（既定は出さない）を持つこと、bat の名前が `run` / `verify` / `release`、`verify.ps1` と `run.ps1` の結果ファイル（`<名前>-result.json`）。`-RunTests` で `*.Tests.ps1` を Pester 5 で実行）。部屋の pwsh 7 で動く（`room init` が入れる）。規約は `script-guide.md` の「Windows で実行するスクリプト」。終了コードは FAIL の数 |
| `tools/check-hook-outline.ps1` | `*-hook.md` の章立ての共通部（制約、手順、報告の型、改善）の存在と順序の点検、`hooks.md` と README の表にフックが過不足なく載っているかの点検（フックの追加・削除の漏れ止め。PowerShell 7）。Python 版は `tools/check_hook_outline.py`（`pwsh` が無い環境用。点検は同じ。どちらかを直したら合わせる） |
| `templates/` | 導入用の雛形（`AGENTS.md`、`log.md`、`decisions.md`）。`workspace/` は works 用（`AGENTS.md`、`gitignore.template`、`claude-settings.template.json`、`ignore.template`、`gitattributes.template`、`pre-push.template`）。`topic/` はトピックの窓口の雛形（`start-here.template.md`） |
| `examples/` | 出力の見本（`inbox-example.md` など）。出力のブレを抑える基準 |
| `AGENTS.md` | このディレクトリ自体を編集するときのルール |

## TODO（次回以降）

- 手順書本体をさらに薄くする（`stock-hook.md` の手順「知識かどうかを判定する」の例外の細則、`docs-rules.md`）。2026-10-15 の点検と 2026-11-08 の判定の結果を見てから。

- Claude 用スキル（`dotfiles` の `home/.claude/skills/`）。「ナレッジ化して」の入口にする（「workflowを導入して」の入口は、2026-10-24 の `init` 廃止で不要）。スキルは kit のファイルを読むだけにして、手順を重複させない。

## 変更履歴

版番号と README の変更履歴は、2026-10-08 に廃止した。変更の理由は、コミットメッセージに書く（`git log -- workflow-kit/`）。廃止前の README（版 `2026-10-08.5` までの変更履歴 58 件を含む）は、タグ `kit-history-20261008` で読める（`git show kit-history-20261008:workflow-kit/README.md`）。コミットのトレーラー `Kit-Rev` が、規則の時点を示す。
