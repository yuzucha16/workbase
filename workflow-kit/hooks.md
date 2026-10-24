# フックの呼び出し表（正本）

合言葉を受けたら、この表の「読むファイル」を読んで実行する。**この表の写しを、ほかの場所に作らない**（各 `AGENTS.md` には、この表への1行のポインタだけを置く）。合言葉は、ユーザーが言ったときだけ実行する（自発的には実行しない）。

| 合言葉 | 別名（日本語） | 読むファイル | 寿命・時機 | 要点 |
|---|---|---|---|---|
| `brief` | 「作業を始めて」<br>`brief 解決`＝「解決で始めて」<br>`brief 改善`＝「改善で始めて」<br>`brief 調査`＝「調査で始めて」<br>`brief 計画`＝「計画で始めて」 | `brief-hook.md` | セッションの開始 | 開始インタビュー。`brief 解決` / `brief 改善` / `brief 調査` / `brief 計画` で、進め方を選んで始める |
| `wrap` | 「終了処理して」 | `wrap-hook.md` | セッションの終了 | 現在状態の更新・昇格の案・コミットと push（許可リストにあれば）を、AI が順序を固定して行う。部屋では、部屋の git へのコミットまで（push はしない） |
| `stock` | 「ナレッジ化して」＝`stock ナレッジ`<br>`stock 理解`＝「理解ガイドにして」 | `stock-hook.md`（`stock 理解` は `stock-explain.md` も） | 随時 | 書き込みは `exmem/inbox/` の新規ファイルだけ（例外は `stock-hook.md`）。部屋では下書きまで（`ai/out/stock/`）で、人が `room stock` で運ぶ。`kind` で AI 用（`lessons/`）と人用（`guides/explain/`）に分かれる。合言葉だけなら1問でモードを選ぶ |
| `integrate` | 「inboxを整理して」 | `integrate-hook.md` | 随時（exmem 側の作業） | `inbox/` のメモを `lessons/` に統合し、照合を報告する |
| `review` | 「見直して」<br>`review 消化`＝「next action を消化して」 | `review-hook.md` | 随時（週1回・15分を目途） | 遠回りの事例を見て、1つ直すか1つ畳む。`review 消化` で Next Actions / Open Questions の消化 |
| （常時） | | `docs-rules.md` | `docs/` を更新するとき、コミット・push の前 | `docs/` の運用規則 |

- 連鎖: `[brief → 作業 → wrap]×N`。`stock` と `integrate` は随時。works の作成と雛形の反映（旧 `init`）、Project の開始（旧 `open`）と終了は合言葉を持たず、人が `room mkworks` `room open` `room close` で行う（部屋の AI が書く `ai/out/close.md` の書き方は `room-context.md`）。トピックの終了は `topics/AGENTS.md`。
- 全フックの共通規則（冒頭の定型、改善、承認、フックを足す・消すとき）は `hook-common.md`。
- 上のファイルが読めない場合（`workbase` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。
- ディレクトリ名: `exmem/knowledge/` は `exmem/lessons/` に、`cheatsheets/` は `guides/`（`howto/` `explain/` `quickref/`）に、2026-10-10 に改名した。履歴の中の旧名は、これで読み替える。
- 旧ファイル名 `closing-hook.md` `knowledge-hook.md` `setup-hook.md` は、2026-10-08 に削除した（新名は `wrap` `stock` `init`）。履歴の中の旧名は、この表で読み替える。
- `init` `open` の合言葉と `init-hook.md`（`init-workspace.md` `init-update.md` `init-restore.md` を含む）`open-hook.md` は、2026-10-24 に削除した（works の作成と雛形の反映は `room mkworks`、Project のひな形は `room open`、README 本文の下書きの書き方は `room-context.md`。他のリポジトリへの導入と履歴からの復元は廃止）。履歴の中の `init` `open` は、これで読み替える。
- `start` の合言葉は、2026-10-24 に `brief` に改名した（`room start` との名前の重なりをなくすため。別名「作業を始めて」と引数 `解決` `改善` `調査` `計画` は同じ。`start-hook.md` `start-plan.md` `start-work-types.md` は `brief-hook.md` `brief-plan.md` `brief-work-types.md` に改名）。履歴の中の `start` は、これで読み替える（`room start` は変わらない）。
- `close-hook.md` は、2026-10-16 に削除した（Project の終了は `room close`、判断の部分は `room-context.md`。トピックの終了は `topics/AGENTS.md`）。履歴の中の `close` は、これで読み替える。

## 運用コマンド（`room`）

合言葉のフックとは別の層。人が端末で打つスクリプトで、AI は実行しない。呼び出し表と正本は `room/README.md`。合言葉（`brief` など）と区別するため、会話と文書では必ず `room` を前置する（2026-10-24 までは、`start` が両方にあった）。部屋の中でフックを使うときの読み替えと分担は `room-context.md`。

| コマンド | すること |
|---|---|
| `room mkworks` | works のトップの作成（PC に1回）と、雛形の変更の反映（`--update`）。旧 `init` フックの項目 5 と `init 更新` |
| `room open` / `start` / `close` | Project のひな形、起動の準備（マスク、写しの送付、マウント）と回収（復元、works へのコミット）、Area への引き渡しと `archives/` への移動 |
| `room stock` | 部屋の AI の `stock` の下書き（`ai/out/stock/`）を、人が確認して `exmem/inbox/` に運ぶ |
| `room readme` | AI の下書き（`ai/out/readme-draft.md`）を README に反映する |

上のほかのコマンド（`init` `pull` `mask` `restore` `umount` `aws-key` `shell` `reap` `rename-area`）は、フックと対にならない。`room/README.md` を見る（この表に写さない）。

## 領域とフックの権限（r/w 表）

2026-10-17 ユーザーの決定（r/w 属性での管理）。フックを実行できる場所は、**この表だけが正本**（各フックと `hook-matrix.md` に、実行できる場所を写さない）。

- **領域** は4つ: works（この領域の AI が扱うのは自分の `docs/` などの管理だけで、`projects/` `areas/` `archives/` の中身は room の作業）、workbase、dotfiles、room（AI 作業部屋。WSL のユーザーランド）。領域 = cwd（リポジトリのトップ。room は `/mnt/room/<名>`）。works・workbase・dotfiles は、トップに `AGENTS.md` `CLAUDE.md` `README.md` と `docs/` を持つ（下の契約）。room の `AGENTS.md` に当たるのは、`~/shared` の写し。
- **表の見方**: そのフックを、その領域で起動したときの、その領域への権限。r 読める、w 書ける、－ 行わない（実行を弾く。理由を伝えて止まる）。

| フック | works | workbase | dotfiles | room |
|---|---|---|---|---|
| `brief` | rw | rw | rw | rw |
| `wrap` | rw | rw | rw | rw（部屋の git にコミット。works へのコミットは人の `room start` の回収） |
| `stock` | w | rw | w | w |
| `integrate` | － | rw | － | － |
| `review` | rw | rw | rw | － |

- `stock` の w は、窓口への書き込み（下の型3）。room は `ai/out/stock/` に置くだけで、運ぶのは人（`room stock`）。
- **跨ぎ**（起動した領域の外）の型は3つだけ。これ以外の跨ぎ書き込みは行わない。
  1. 読み: どの領域でも、r は自由（lessons、methods、他のリポジトリの点検）。
  2. 作業対象の `docs/`: このセッションで作業した領域の `docs/` に、作業したセッション自身が書く（`wrap`）。報告に、触った領域と更新した `docs/` を挙げる。各フックの改善案の1行（Open Questions。`hook-common.md` の「改善」）も、この型で書く。
  3. 集約の窓口: workbase の `exmem/inbox/`（知識。`stock`）と `topics/kit-growth/inbox.md`（kit の改善と、使った印象）にだけ、他の領域から書いてよい。
- room は物理的に跨げない（`ai/` だけがマウントされる）。窓口への下書きは `ai/out/stock/` と `ai/docs/log.md` に残し、人が運ぶ（PC1 は記憶かキャプチャ）。

## exmem の場所

`stock` `integrate` が書く exmem の場所（2026-10-18。各フックに同じ文を置かず、ここだけに書く）: `$HOME\works\resources\exmem`（WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources/exmem`）。

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
