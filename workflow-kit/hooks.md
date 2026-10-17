# フックの呼び出し表（正本）

合言葉を受けたら、この表の「読むファイル」を読んで実行する。**この表の写しを、ほかの場所に作らない**（各 `AGENTS.md` には、この表への1行のポインタだけを置く）。合言葉は、ユーザーが言ったときだけ実行する（自発的には実行しない）。

| 合言葉 | 別名（日本語） | 読むファイル | 寿命・時機 | 要点 |
|---|---|---|---|---|
| `init` | 「workflowを導入して」 | `init-hook.md` | ワークスペース | 作業ディレクトリへの導入の入口（Vault のトップの生成を含む）。`init 更新`（「雛形を反映して」）で、雛形の変更をワークスペースに反映する |
| `open` | | `open-hook.md` | Project の開始 | 目的と完了条件を聞いて README 本文を下書きし、`start` を呼ぶ。Project の構造の表は `project-structure.md`（ひな形は `room open`） |
| `start` | 「作業を始めて」 | `start-hook.md` | セッションの開始 | 開始インタビュー。`start 解決` / `start 改善` / `start 調査` で、進め方を選んで始める |
| `wrap` | 「終了処理して」 | `wrap-hook.md` | セッションの終了 | 現在状態の更新・昇格の案・コミットと push を、順序を固定して行う |
| `stock` | 「ナレッジ化して」 | `stock-hook.md` | 随時 | 書き込みは `exmem/inbox/` の新規ファイルだけ（例外は `stock-hook.md`） |
| `integrate` | 「inboxを整理して」 | `integrate-hook.md` | 随時（exmem 側の作業） | `inbox/` のメモを `lessons/` に統合し、照合を報告する |
| `review` | 「見直して」 | `review-hook.md` | 週1回を目途 | 遠回りの事例を見て、1つ直すか1つ畳む。`review 消化` で Next Actions / Open Questions の消化 |
| （常時） | | `docs-rules.md` | `docs/` を更新するとき、コミット・push の前 | `docs/` の運用規則 |

- 連鎖: `init`、`open → [start → 作業 → wrap]×N`。`stock` と `integrate` は随時。Project の終了は合言葉を持たず、人が `room close` で行う（部屋の AI が書く `ai/out/close.md` の書き方は `room-context.md`）。トピックの終了は `topics/AGENTS.md`。
- 全フックの共通規則（冒頭の定型、改善、承認、フックを足す・消すとき）は `hook-common.md`。
- 上のファイルが読めない場合（`workbase` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。
- ディレクトリ名: `exmem/knowledge/` は `exmem/lessons/` に、`cheatsheets/` は `guides/`（`howto/` `explain/` `quickref/`）に、2026-10-10 に改名した。履歴の中の旧名は、これで読み替える。
- 旧ファイル名 `closing-hook.md` `knowledge-hook.md` `setup-hook.md` は、2026-10-08 に削除した（新名は `wrap` `stock` `init`）。履歴の中の旧名は、この表で読み替える。
- `close-hook.md` は、2026-10-16 に削除した（Project の終了は `room close`、判断の部分は `room-context.md`。トピックの終了は `topics/AGENTS.md`）。履歴の中の `close` は、これで読み替える。

## 運用コマンド（`room`）

合言葉のフックとは別の層。人が端末で打つスクリプトで、AI は実行しない。呼び出し表と正本は `room/README.md`。合言葉の `open` `start` と名前が重なるので、必ず `room` を前置して区別する。部屋の中でフックを使うときの読み替えと分担は `room-context.md`。

| コマンド | すること |
|---|---|
| `room open` / `start` / `close` | Project のひな形、起動の準備（マスク、写しの送付、マウント）と回収（復元）、Area への引き渡しと `archives/` への移動 |
| `room mask` / `restore` / `readme` / `umount` | マスクと復元の単独実行、AI の下書きの README への反映、残ったマウントの解除 |

## 領域とフックの権限（r/w 表）

2026-10-17 ユーザーの決定（r/w 属性での管理）。フックを実行できる場所は、**この表だけが正本**（各フックと `hook-matrix.md` に、実行できる場所を写さない）。

- **領域** は4つ: works（ワークスペース。Vault 側の AI が扱うのは自分の `docs/` などの管理だけで、`projects/` `areas/` `archives/` の中身は room の作業）、workbase、dotfiles、room（AI 作業部屋。WSL のユーザーランド）。領域 = cwd（リポジトリのトップ。room は `/mnt/room/<名>`）。works・workbase・dotfiles は、トップに `AGENTS.md` `CLAUDE.md` `README.md` と `docs/` を持つ（下の契約）。room の `AGENTS.md` に当たるのは、`~/shared` の写し。
- **表の見方**: そのフックを、その領域で起動したときの、その領域への権限。r 読める、w 書ける、－ 行わない（実行を弾く。理由を伝えて止まる）。

| フック | works | workbase | dotfiles | room |
|---|---|---|---|---|
| `init` | w | r | w | － |
| `open` | － | － | － | rw |
| `start` | rw | rw | rw | rw |
| `wrap` | rw | rw | rw | rw（コミット・push は人） |
| `stock` | w | rw | w | w |
| `integrate` | － | rw | － | － |
| `review` | rw | rw | rw | － |

- `init` の works は、works が無い初回だけ、workbase の clone の中から書く（例外。ユーザーの決定）。以後は works の中で起動する。
- `stock` の w は、窓口への書き込み（下の型3）。room は `ai/out/stock/` に置くだけで、運ぶのは人（`room stock`）。
- **跨ぎ**（起動した領域の外）の型は3つだけ。これ以外の跨ぎ書き込みは行わない。
  1. 読み: どの領域でも、r は自由（lessons、methods、他のリポジトリの点検）。
  2. 作業対象の `docs/`: このセッションで作業した領域の `docs/` に、作業したセッション自身が書く（`wrap`）。報告に、触った領域と更新した `docs/` を挙げる。各フックの改善案の1行（Open Questions。`hook-common.md` の「改善」）も、この型で書く。
  3. 集約の窓口: workbase の `exmem/inbox/`（知識。`stock`）と `topics/kit-growth/inbox.md`（kit の改善と、使った印象）にだけ、他の領域から書いてよい。
- room は物理的に跨げない（`ai/` だけがマウントされる）。窓口への下書きは `ai/out/stock/` と `ai/docs/log.md` に残し、人が運ぶ（PC1 は記憶かキャプチャ）。

## 作業ディレクトリへの契約（手順書が前提にするもの）

手順書は、次だけを前提にする。これ以外の作業側のファイル名・列・スクリプトを、手順書に書かない（共有側は公開されているので、作業側の構造を載せない）。

- **必須**: `AGENTS.md`（共通ルールのポインタ、読む順番、固有ルール）と `CLAUDE.md`（`@AGENTS.md` の1行）。`docs/log.md`（現在状態と次にやること）。複数セッションにまたがる判断があるときは `docs/decisions.md`。
- **呼び出し元の `AGENTS.md` が定めるもの**: コミットの規則と push の許可リスト（無ければ push しない）。追加の手順（指標の記録など。`docs/` の更新に続けて行う）。
- **任意の記録**: 記録名は `events`（質問・承認・改善案）、`sessions`、`reviews`、`rule-hits`。保存先と列は、呼び出し元の `AGENTS.md` が定める。定められていなければ記録しない（手順書は、存在を確かめてから記録する）。
- 共有側から作業側へ `[[リンク]]` を張らない。作業側固有の情報を、共有側に書かない。

### 起動する場所（cwd）

- Claude は、リポジトリのトップ（`AGENTS.md` を置いた単位）で起動する。Claude Code は cwd から上の `CLAUDE.md` を自動で読むので、起動した単位の規則が前提になる。
- 開始時に読む順番と、上の階層で起動して「<名前> の続き」と言われたときの扱いは、`docs-rules.md` の「読む順番」に1か所で定める（ここに写さない）。
- 例外は AI 作業部屋。`room start` が cwd を `/mnt/room/<名>` に固定する。読む順番は `room-context.md`。どのフックをどの領域で起動できるかは、上の「領域とフックの権限」。
