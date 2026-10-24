# フックと room コマンドの整合: init / open / start（議論の記録。第1〜3版）

> 2026-10-24 に実装済み（決定は workbase 直下の `docs/decisions.md` の同日3項）。本文の `start` は、実装でフック `brief` に改名した。状態は `docs/log.md`。

2026-10-24。対象は `init` `open` `start` の3フック。一次情報は workbase の main（`ad9d52a`）の `workflow-kit/hooks.md`、`init-hook.md`（＋`init-workspace.md` `init-update.md` `init-restore.md`）、`open-hook.md`、`start-hook.md`、`room-context.md`、`room/README.md`、`room/room.py`、`README.md` の「フックの体系」。段階は「① 論点を解消・仮決め」。変更範囲の確定と実装は、仮決めの後。

## 1. 事実の表

| | フック（合言葉。判断） | `room` コマンド（人が打つ。副作用） | 重なり方 |
|---|---|---|---|
| **init** | `init-hook.md`。寿命は works（PC）。中身は3つ: (a) 任意の作業ディレクトリに `AGENTS.md` `CLAUDE.md` `docs/` を入れる（項目 1〜3、6。dotfiles など）、(b) works のトップを作る（項目 5。`.gitignore`、PARA の3フォルダ、`git init` など。workbase の clone の中で言うと既定でこれ）、(c) `init 更新` ＝雛形の変更を works に3者マージで反映（項目 7、`init-update.md`）。r/w: works w、workbase r、dotfiles w、**room －** | `room init <Area>`。寿命は Area。WSL のディストロ `room-<Area>` を作り、道具を入れ、`areas/<Area>/README.md` と Area の置き場（`_noai/knowledge/` など）を作ってコミット | **名前だけ**。対象（works/作業ディレクトリ ↔ Area と部屋）も寿命も違う。`room-context.md` は「部屋の作成は `room init`」と書き分けている |
| **open** | `open-hook.md`。寿命は Project。**部屋の中だけ**で実行（r/w: room rw だけ）。手順: 1 対象と Area を決める → 2 判断基準の検査（完了条件1文、成果物1つ、進行中の上限3件）→ 3 type・主題・完了条件・見直し日を聞く → 4 `ai/out/readme-draft.md` に README 本文、Project 名の案 → 5 記録 → 6 `start` を呼ぶ | `room open <Project> --area <Area> [--type dev\|inv]`（ひな形、Area の一覧、コミット）→ 部屋に入るには `room start` → 部屋を出たあと `room readme <Project>`（下書きを本文に反映。**frontmatter は変えない**） | **工程が重なり、順序が食い違う**（下の 2.2） |
| **start** | `start-hook.md`。寿命はセッション。どの領域でも rw。開始インタビュー（ゴール・前提・触ってよい範囲…）。モード `解決` `改善` `調査` `計画`。進行中の Project が無ければ `open` を案内する | `room start <Project>`。寿命はセッション。チェック、マスク、写しの送付（`~/shared`）、マウント、AI の起動（既定 `claude`、プロンプトなし）、回収（復元、コミット） | **名前が同じで、寿命も同じ**（セッション）。役割は分かれている（準備と起動 ↔ ゴールの聞き取り）。`room start` の後に、部屋の中で人が「作業を始めて」と言う順 |

補足の事実:

- 名前の規則はすでにある: `hooks.md` と `room-context.md` に「運用コマンドには必ず `room` を前置し、合言葉は日本語の別名で呼ぶ」。ただし `open` には日本語の別名が無い。
- 2026-10-08 の体系（`README.md`）は「寿命の階層ごとに、開始と終了の対」: works `init`、Project `open`・`close`、セッション `start`・`wrap`。2026-10-16 に `close` の合言葉を廃止し、Project の終了は `room close`、部屋の AI の判断（`ai/out/close.md` の書き方）は `room-context.md` に移した。**Project の寿命のうち、開始だけが合言葉に残っている**。

## 2. 論点と叩き台

### 2.1 init: 名前だけの衝突

- 事実: 対象と寿命が `room init` と違う。いちばん使うのは (c) `init 更新`（雛形が変わるたび）で、(b) works の生成は PC ごとに1回、(a) は dotfiles など新しいリポジトリのとき。
- 判断の線（提案）: **同じ名前は、同じ寿命の階層のときだけ許す**。init は階層が違う（works ↔ Area）ので、名前を分ける。
- 案:
  - **A（推奨）合言葉を改名する**: 中身（kit の導入と雛形の反映）に合わせて `kit`（`kit 導入`、`kit 更新`）。日本語の別名「workflowを導入して」「雛形を反映して」はそのまま。room 側は変えない。
  - B 合言葉を `setup` に戻す（2026-10-08 に `setup-hook.md` → `init-hook.md` にした経緯があり、戻す理由を記録に足す要がある）。
  - C 名前は変えず、`room` 前置の規則で足りるとする（今のまま）。
- A の弱点: `kit` は `kit-growth`（トピック名）や「kit の改善」と語が重なる。気になるなら B。
- ついでの論点（任意）: (a)(b)(c) を1つのフックに置くままでよいか。分ける案は今回は出さない（字数は分離済み、`hook-matrix.md` の例外の記載あり）。

### 2.2 open: 工程の重なりと順序の食い違い

事実として、次の3点が合っていない。

1. **決める順が逆**: Project の名前・Area・type は、`room open` の引数で先に決まる。フックは後から「どの Area か」（手順 1）、「type」（手順 3）、「Project 名の案」（手順 4）を出す。`room readme` は frontmatter を変えないので、フックで決め直した type や名前には反映の経路が無い。
2. **判断基準の検査が遅い**: 「完了条件を1文で書けるか（書けなければ Area）」「成果物は1つか（複数なら分ける）」「上限3件」は、`room open` を打つ前に要る判断。だがフックは部屋の中（`room open` → `room start` の後）でしか動かない。
3. **`room start` と隣り合う**: フックを動かすには `room start` で部屋に入る必要がある。実際の流れは `room open` → `room start` → 部屋で `open` → そのまま `start` → … → 回収 → `room readme`。部屋の中から見ると、`open` は「初回の `start` の最初の項目（README の本文が空のとき）」と同じ位置にある。

- 案:
  - **A（推奨）`close` と同じ形に畳む**: 合言葉 `open` と `open-hook.md` を廃止する。部屋の AI の判断（README 本文の下書き `ai/out/readme-draft.md` の書き方: 目的・完了条件・成果物・範囲外、承認の前に「ユーザー承認」を書かない）は、`room-context.md` に `close.md` と並べて置く。`start` の事前確認に「`ai/ctx/README.md` の本文が雛形のままなら、下書きを先に行う」を1行足す。判断基準の検査（1文・1成果物・上限）と名前の付け方は `room open` の前の人のチェックとして、`project-structure.md`（または `room/README.md` の `open` の行）に移す。連鎖は `[start → 作業 → wrap]×N` になり、Project の寿命は `room open` / `room close` の対だけになる。
  - B 残して縮める: 手順から Area・type・名前を外し、README 本文の下書きだけにする。合言葉は残る（`room open` と同名のまま。日本語の別名を足す）。
  - C works 側に移す: `room open` の前に works で実行し、名前・Area・type・判断基準を決めて `room open` のコマンドを出す。r/w 表の変更（works の open を w に）が要り、本文の下書きは部屋で別に要るので、2か所に分かれる。
- A の弱点: `room open` の前の判断基準の検査を、AI が手伝う場所が無くなる（人のチェックリストになる）。必要なら、works の `start` の中で扱える（Project を立てるかの相談）。
- 10-16 の方針（open は構造に限定、`_noai` は残す）とは矛盾しない。構造の表は `project-structure.md` にあり、今回は触らない。

### 2.3 start: 名前は同じ、寿命も同じ

- 事実: `room start` は準備と起動と回収、フックはゴールの聞き取り。同じセッションの寿命で、順に続く（`room start` → 部屋で「作業を始めて」）。
- 判断の線（2.1 と同じ）: 寿命が同じなので、**同名を許す**。`room` 前置の規則で区別する。
- 案:
  - **A（推奨）名前は今のまま**。直すのは食い違いだけ: 契機の「`open-hook.md` で Project を始める」（2.2 で A なら消す）、`hooks.md` の連鎖と「要点」の列。
  - B `room start` を改名（例 `room enter`）。`room.py`、テスト、guides、利用の慣れに波及するので推さない。
- 付随の論点（任意、今回は出すだけ）: `room start` が部屋の AI を起動するとき、最初のプロンプトを渡さない。「作業を始めて」を毎回言うのは人。自動で渡すと「言われたときだけ実行する」（`hook-common.md`）と反するので、今のままを推奨。

## 3. 仮決めが要ること（ee）

1. 判断の線「同じ名前は、同じ寿命の階層のときだけ許す」でよいか。
2. init: A（`kit` に改名）/ B（`setup`）/ C（そのまま）。
3. open: A（`close` と同じ形に畳む）/ B（縮めて残す）/ C（works へ移す）。
4. start: A（名前はそのまま、食い違いだけ直す）/ B（`room start` を改名）。

## 4. 変更範囲の見込み（仮決めの後に確定する）

- init を改名するとき: `hooks.md`（表、連鎖、r/w 表）、`init-hook.md` `init-workspace.md` `init-update.md` `init-restore.md`（ファイル名を変えるかも論点）、`README.md`（フックの体系）、`hook-common.md`（記録の表、コミットの節）、`hook-matrix.md`、`docs-rules.md`、`examples/setup-example.md`、`templates/` の `AGENTS.md`、`room-context.md` の最終行、`exmem/lessons/` の数件（`para-operations.md` など。room init との読み分けが要る）。既存の works の `AGENTS.md` の合言葉の行（PC ごと、`kit 更新` で反映）。
- open を畳むとき: `open-hook.md` の削除、`hooks.md`（表、連鎖、旧名の注記）、`room-context.md`（readme-draft の書き方、分担の表）、`start-hook.md`（契機、事前確認）、`README.md`（フックの体系）、`hook-common.md`（例外の文、記録の表）、`hook-matrix.md`（列）、`project-structure.md`、`dev-deliverable-guide.md`、`room/README.md`（`readme` の行の「`open` の判断部分」）、guides の `ai-room-setup*.md` と `ai-room-why.md`、`exmem/lessons/` の数件。`room.py` は変えない見込み（`readme` は下書きのファイル名だけを見る）。
- start: 上の2つに付随する文の直しだけ。

---

# 第2版（2026-10-24 ee のコメントを受けて）

ee: ① init は AI がやらず人がやる操作なので room に取り込めないか（`room mkkit` のイメージ。works を作る操作なので寿命が合わないかも）。② open も close も畳む。③ start は引数があるので、そこの整合。room start と寿命は同じでも目的が違うので改名してもよい。

## 判断の線の取り直し

第1版の「同じ名前は同じ寿命のときだけ」より、`room-context.md` の「2つの層」が根拠として強い: **決まった手順の副作用は `room`（人が打つ。AI は実行しない）、判断は合言葉のフック（AI）**。init の大半は前者なので、取り込むのが筋。寿命のずれは障害にならない。`room` はすでに寿命に縛られないコマンド（`shell` `aws-key` `reap` `rename-area`）を持ち、`room.py` は `resources/` の clone の中にあるので、works が無い新しい PC でも動く（`uv run room.py …`、works は `$ROOM_VAULT` か `~/works`）。

## ① init を room に取り込む

init の3つの中身を、実行者で分ける。

| 中身 | 実行者 | 理由 |
|---|---|---|
| (b) works のトップを作る（項目 5） | **room** | 雛形を置く、`.gitkeep`、`git init`、`pre-push`、初回コミットは決まった手順。入力は PC の役割・remote の方針・初回コミットの3つだけ（既定値あり）で、聞くのも引数で足りる |
| (c) 雛形の反映（`init 更新`） | **room**（衝突時だけ人が判断） | 3者マージ（`git merge-file`）、`deny` の集合合わせ、`Template-Rev` はすべて機械的。承認は `room readme` と同じ「差分を見せて確認、`--yes` で省略」の形にできる。衝突・消えた `deny` は、書かずに止めて一覧を出す（`restore` と同じ「止まる型」） |
| (a) 他のディレクトリへの導入（項目 1〜3、6）＋(4) 履歴からの復元 | **フックのまま**（改名） | `AGENTS.md` の目的・固有ルール・読む順番を、会話や既存の内容から埋める判断が要る。`room` の領域外（dotfiles、他のリポジトリ） |

- コマンド名（案）: `room mkworks`（b）と `room upworks`（c）。ee の `mkkit` は「kit を導入する」の意味でも読めるが、(a) も指しうるので、works を作る/更新するとはっきり書ける名前を勧める。`mkkit` でよければ、(b)(c) を1つのコマンドにして `mkkit --update` でもよい。
- 残るフック(a)(4): `init` の名前は `room init` と衝突したままなので、合言葉を改名する（候補 `kit`、別名「workflowを導入して」）。`init 更新` の別名「雛形を反映して」は `room upworks` の説明に移す。
- 寿命について: works は PC に1つで Area の上位。`room mkworks` は「`room init <Area>` の前に1回」という位置づけで `room/README.md` の先頭に流れを書く（`mkworks` → `init <Area>` → `open` → `start` → `close`）。
- 効くところ: ① 例外が消える（`hooks.md` の r/w 表の「`init` の works は初回だけ workbase から書く」）。② トレーラーが `Room-Op` / `Room-Rev` に統一できる（今は `Agent` `Kit-Rev` `Template-Rev` が別系統）。ただし `Template-Rev` は次回の基点なので、残すか `Room-Rev` で代えるか決める。③ 単体テストを書ける（一時ディレクトリの git。今はテストなしの AI 実行）。
- 論点（要決定）: 
  1. コミットの身元: 今は agent 名義（`docs-rules.md`）。`room` の他のコミットがどの身元かは未確認（`room.py` の `commit_paths` を読んで合わせる）。人が打つので、既定は git の身元の設定にする案。
  2. 既存の works（すでに `init` で作ったもの）の基点: `Template-Rev` を読み、無ければ初回の `Kit-Rev` を候補にする、は引き継ぐ。
  3. `.claude/settings.json` の安全網（`projects/` などの Read/Edit の deny）を `mkworks` が置く。AI が実行しないので、むしろ設定を勝手に緩める経路が減る。

## ② open と close を畳む

- close は 2026-10-16 に合言葉・手順書とも削除済み（`room close` と `room-context.md` の `close.md` の書き方）。**残るのは open だけ。**
- 第1版の A 案で進める: `open-hook.md` を廃止し、`hooks.md` の `open` の行・連鎖・旧名の注記を直す。README 本文の下書きの書き方（目的、完了条件、成果物、範囲外、承認の前に「ユーザー承認」を書かない）は `room-context.md` に `close.md` の節と並べて置く。`start` の事前確認に「`ai/ctx/README.md` の本文が雛形のままなら、下書きを先に行う」を足す。`room open` の前の判断基準の検査（完了条件1文、成果物1つ、上限3件）は `project-structure.md` に移す。
- ついでに: 連鎖は `[start → 作業 → wrap]×N`。Project の寿命は `room open` / `room close` の対だけ。

## ③ start の整合と改名

事実: `start` は2種類の引数を混ぜている。

| 引数 | 実体 | `methods.md` の区分 |
|---|---|---|
| なし | インタビュー。モード（確定型/探索型）を1問で選ぶ | — |
| `解決` `改善` | 区分の表から「やり方」を選ぶ | 解決、改善 |
| `調査` `計画` | 区分のやり方を選び、`start-plan.md` などの A 仕込みへ | 調査、計画 |

- 引数は、`methods.md` の区分（解決・改善・変更・計画・調査）の名前そのもの。ただし `変更` には対応する `start 変更` が無い（`methods.md` の「変更」は別の入口）。ここが整合の穴。
- `room start` との違い: `room start` は準備・起動・回収。フックは「今日のゴールと前提を揃える」。目的が違うので改名する案に賛成。名前は「作業の前提を揃える」意味の語がよい。
  - 候補 A（推奨）`brief`（別名「作業を始めて」は残す）。`brief 解決` `brief 調査` のように、引数はそのまま区分の名前。
  - 候補 B `goal`。ゴールだけに聞こえるが、前提・範囲も扱う。
  - 候補 C そのまま（`room` 前置の規則で区別）。
- `wrap` との対（開始/終了）は、名前としては崩れるが、体系の説明は「セッションの寿命で `brief` → 作業 → `wrap`」で足りる。
- 引数の整合（要決定）: ① 区分の名前を `methods.md` の見出しと揃えて、`変更` の入口を足すか（`brief 変更`）、② 引数なしのインタビューを `methods.md` の区分としては扱わないと明記するか。

## 要決定の一覧（第2版）

1. 取り込む範囲: (b)(c) を room へ、(a)(4) はフックに残す。でよいか。
2. コマンド名: `mkworks`/`upworks`（推奨）か `mkkit`（1つにして `--update`）か。
3. 残る init フックの名前: `kit` か、他か。
4. open を畳む: 第1版 A のとおり。でよいか。
5. start の名前: `brief`（推奨）/ `goal` / そのまま。
6. start の引数に `変更` を足すか。
7. 取り込み後の commit の身元と、`Template-Rev` の扱い。

---

# 第3版: 決定事項と変更範囲（2026-10-24）

## ee の決定（確定）

1. `init` フックは廃止し、`room mkworks` に一本化する。雛形の反映は `--update`。今後の機能は引数で足す（`--list` など）。コマンドは `mkworks` のまま増やさない。
2. 他リポジトリへの導入と履歴からの復元は消す。`kit` フックは作らない。環境移行で必要になったら相談する。
3. `open` を畳む（`close` は 10-16 に廃止済み）。
4. r/w 表: `init` の行を消す。「初回だけの例外」の記述も消える。

未回答（仮決めで進め、実装の前に確認する）: start の改名（仮: `brief`）、`brief` の引数に「変更」を足すか。ここだけは、mkworks と open の実装とは別のコミットにする（影響範囲が広いため）。

## `room mkworks` の設計（叩き台）

```
uv run room.py mkworks [--role 業務用|個人用] [--remote <URL>|none] [--no-commit]   # 作る（既定）
uv run room.py mkworks --update [--yes] [--no-commit]                             # 雛形の反映
```

- 作る: `init-workspace.md` の項目 5 の手順をそのままコードにする。確認（空か、`.git`、`resources/.git` の `origin` が workbase か、`.obsidian` の種類）→ `.gitignore` `.ignore` `.gitattributes` `.claude/settings.json` `README.md` `AGENTS.md` `CLAUDE.md` `docs/log.md` `docs/decisions.md`（`templates/` から）→ `areas/` `projects/` `archives/` の `.gitkeep`、`resources_p/` → `git init`（remote なしなら `pre-push`）→ 初回コミット。既存のファイルは上書きしない。`resources/` が無ければ clone を案内して止まる。`AGENTS.md` の役割・remote の欄（`<…>`）は `--role` `--remote` で埋め、`README.md` の構成の表は雛形のまま（この PC の実態に合わせて人が直す）。
- 更新: `init-update.md` の手順 1〜8 をコードにする。基点は、最新の `Room-Rev`（`Room-Op: mkworks`）、無ければ `Template-Rev`、無ければ初回の `Kit-Rev`。3者マージ（`git merge-file`）、`settings.json` の `deny` は集合で合わせる。差分を見せて確認（`--yes` で省略）。**衝突、雛形から消えた `deny`、未コミットの変更があるファイルは、書かずに止まって一覧を出す**。
- コミット: 人が打つので、git の身元は git config（`room` の他のコミットと同じ。`agent` 名義と `Agent` `Kit-Rev` トレーラーは付けない）。トレーラーは `Room-Op: mkworks` または `mkworks-update`、`Room-Rev: <resources の短縮ハッシュ>`。`Template-Rev` は新規には付けず、読むだけ（既存の works のコミットのため）。
- 残らない: events の記録（質問ごとの行）、導入する単位の確認（サブディレクトリでないか）、自己点検のチェックリスト。コードの検査とテストに置き換える。
- テスト: `tests/test_room.py` に、一時ディレクトリの git で足す（新規、既存あり、`--update`、衝突で止まる、`deny` が消えない、remote なしで `pre-push` が置かれる）。

## 変更範囲

**A. 新規・コード（`workflow-kit/room/`）**
- `room.py`: `mkworks` のサブコマンドと関数、トレーラー。`tests/test_room.py`: 上のテスト。
- `README.md`（room）: 使い方に `mkworks` を足し、トレーラーの対象に加える。流れを `mkworks → init <Area> → open → start → close` と先頭に書く。

**B. 削除（workflow-kit）**
- `init-hook.md` `init-workspace.md` `init-update.md` `init-restore.md` `open-hook.md` `examples/setup-example.md`（見本は init-hook 用）。手順の中身は `room.py` のコードと、`room/README.md` の `mkworks` の行（要点だけ）に移る。履歴は git。
- 注意: `improvements.md`（凍結）と、`docs/decisions.md` `docs/log-history.md` `topics/*/records` の過去の記述は書き換えない（履歴は旧名のまま。読み替えは `hooks.md` の注記に足す）。

**C. 直す（生きている文書）**
- `workflow-kit/hooks.md`: 表から `init` `open` の行を消す。連鎖（`[start → 作業 → wrap]×N`、works の作成は `room mkworks`）。r/w 表の `init` `open` の行と、「`init` の works は…初回だけ」の例外を消す。旧名の注記に `init` `open` を足す。「運用コマンド」の表に `mkworks` を足す。
- `workflow-kit/README.md`: 「フックの体系」「使い方」（作業ディレクトリに導入する／works を作る）、ファイル一覧（5行）、スキルの TODO の行。「新しい PC では… `room mkworks`」に書き換える。
- `workflow-kit/hook-common.md`: 記録の表（`init` `open` の行）、「コミットするフック」の `init`、フックを足す・消すときの例、`open` を `start` が案内する例外の文。
- `workflow-kit/hook-matrix.md`: 列 `init` `open`、字数の行、基準値。`tools/check_hook_outline.py` の「init の表は目次を兼ねる」の例外の記述（`.ps1` 側は同じ）。
- `workflow-kit/docs-rules.md`: `init 更新` のトレーラーの段落（`Template-Rev`）。
- `workflow-kit/room-context.md`: `open` の行（分担表）、`readme-draft.md` の書き方の節を `close.md` の節と並べて足す（旧 `open-hook.md` の手順 3〜5、実測から分かっていること）。最終行の `init`。
- `workflow-kit/start-hook.md`: 契機の「`open-hook.md` で Project を始める」、事前確認に「README の本文が雛形のままなら下書きを先に行う」を1行。
- `workflow-kit/project-structure.md`（冒頭の「open-hook.md から移した」、`room open` の前の判断基準の検査をここへ）、`dev-deliverable-guide.md`（`open-hook.md` の未決への参照 2か所）、`start-work-types.md`。
- `workflow-kit/templates/workspace/` と `templates/project/README.template.md`: 合言葉の記述を確認（今は `room open` への言及のみで変更なしの見込み）。
- exmem と guides（生きている手順）: `exmem/lessons/obsidian-vault.md:302` と `ai-development-workflow.md:338`（新しい PC の再現手順の「workflowを導入して」「`init`」→ `room mkworks`）、`exmem/lessons/workflow-kit.md`（導入フックの経緯。履歴として残し、冒頭に「廃止、`room mkworks` へ」の1行）、`guides/explain/ai-room-why.md:146`（名前の衝突の説明）、`guides/howto/ai-room-setup.md:20,358`、`ai-room-setup-script.md`（手順 3 の「`open`」は `room open` で変更なし）。`exmem/lessons/para-operations.md` は 2026-10-08 の注があり、履歴として残す。
- 外（workbase の外）: dotfiles の Claude 用スキル（「workflowを導入して」の入口。`workflow-kit/README.md:96` が TODO として言及）、各 PC の works の `AGENTS.md`（合言葉の行は `hooks.md` を指すだけなので変更不要の見込み）。
- `docs/log.md` `docs/decisions.md`: 今日の決定を `decisions.md` に追記、`log.md` の room の節に1行。

**D. 別コミット（start の改名。ee の確認の後）**
- ファイル名 `start-hook.md` → `brief-hook.md`（など）と、`hooks.md` `README.md` `hook-common.md` `methods.md` `start-plan.md` `start-work-types.md` `review-hook.md` `token-matrix.md` `room-context.md` `room/room.py`（`ROOM_GUIDE` と部屋に置く案内文の「`start` `wrap`」）、`templates/project/README.template.md` の `start 計画`、`guides/AGENTS.md`、exmem の lessons 数件（`session-goal-modes.md` `planning-method.md` `research-method*.md` `retrospective-method*.md` ほか）。過去の記録（topics の records、decisions、log-history）は旧名のまま。

## 事実の照合（確かめたこと）

- `room.py` の `commit_paths` は人の git の身元で動く（`room-ai` は部屋の中の git だけ）。トレーラーは `Room-Op` `Room-Rev` `Room-Area` で、`kit_rev()` が `Template-Rev` と同じ意味（resources の短縮ハッシュ、dirty 判定つき）。統一できる。
- `room.py` は `templates/` を読んでいない（インラインの雛形のみ）。`mkworks` は `<resources>/workflow-kit/templates/workspace/` を読む。`room.py` は resources の中にあるので、`Path(__file__)` から辿れる。
- `tools/check_hook_outline.py` と `.ps1` の点検は、フック名を決め打ちしていない（「init の表」の例外の文だけ）。廃止後も通る見込み（実装時に実行して確かめる）。
- `init-hook.md` の自己点検は、コードに置き換えるとテストになる。「導入する単位」の確認（サブディレクトリでないか）は、`mkworks` が works のトップ以外では動かないので不要になる。
- 新しい PC の手順: 今は「clone → エージェントに言う」。変更後は「clone → `uv run room.py mkworks`」。`uv` は Windows に導入済み（`decisions.md` の記録）。dotfiles の `50_repos` が `resources/` を clone するので、その直後の1コマンドになる。

## 次の段（review 消化）

この範囲で実装してよいかの承認を求める。実装順（案）: ① `mkworks` のコードとテスト → ② フックの削除と文書の直し（B・C）→ ③ start の改名（D。確認の後）。各段で `check_hook_outline` とテスト（`uv run python -m unittest discover -s tests`）を通し、`main` に直接 push（プロジェクトの指示どおり）。
