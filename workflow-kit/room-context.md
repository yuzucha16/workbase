# 部屋の中でフックを使うとき

AI 作業部屋（`workflow-kit/room/`）の中で、合言葉のフックを使うときの読み替えと分担。`hooks.md` の表が正本（どのフックを部屋で行うかは、同じ `hooks.md` の「領域とフックの権限」）で、ここは部屋の中での差分だけを書く。部屋でないときは読まない。

## 2つの層

| | 運用コマンド（`room …`） | 合言葉のフック |
|---|---|---|
| 呼ぶ人・場所 | 人が Windows の端末で打つ | 人が言い、AI が手順書を読んで実行 |
| 性質 | 決まった手順の副作用（マウント、写しの送付、マスク、移動、コミット） | 判断（聞き取り、確認、振り分け、下書き） |
| 実行者 | スクリプト。**AI は実行しない** | AI |

運用コマンドには必ず `room` を前置し、合言葉は日本語の別名で呼ぶ。2つをつなぐのは**ファイルの受け渡しだけ**。

## 部屋の中の読み替え

- 起動する場所は `/mnt/room/<名>`（Project の `ai/`）に固定される。Zed などで開くときも `/mnt/room/<名>` を開く（`/mnt/room` を開かない。記録・git・会話履歴が壊れる）。開始時に読むのは `~/shared/ROOM.md` → `ai/ctx/README.md`（Project の窓口の写し）→ `ai/ctx/area-README.md`（所属する Area の README の写し。Area の共通ルール）→ `ai/docs/log.md`。
- 手順書の `ai/X`（`ai/docs/` `ai/out/` など）は、部屋では `/mnt/room/<名>/X`（`ai/` そのものがマウント点で、`ai/` という名前のディレクトリは無い。cwd が `/mnt/room/<名>` のときは cwd 直下の `X`）。手順書の `docs/` は、部屋では `/mnt/room/<名>/docs/`（Project の記録。`log.md` `decisions.md` `log-history.md` の 3 つを `room open` が置く）。Project と Area の `README.md` は書き込めない。写し（`ai/ctx/README.md`、`ai/ctx/area-README.md`）を読む。
- 手順書は `~/shared/workflow-kit/` にある（読み取り専用の写し。基準コミットは `~/shared/ROOM.md`）。
- 副作用を伴う手順（Project の作成、状態の更新、`archives/` への移動、works へのコミット）は AI が行わない。判断をファイルに書いて、人が `room` で反映する（部屋の git へのコミットは別で、AI が行う。下）。
- スクリプトや変換を作るときは、言語をユーザーに聞かず、優先順位 Python → ps1 → bat で決める（`script-guide.md` の「言語の選び方」）。あわせて同じ文書の「実行の方針」に従う（部屋で完結できるなら、すべて部屋で実行する。Excel・COM などの Windows 依存部は、できるだけ小さな層にして、人の手数を 1 コマンドに減らす。2026-10-21）。人が Windows で実行する薄い層は、Python が既定（2026-10-21）。同じ文書の「Windows で実行するスクリプト」に従う（束ねる役も同じ言語、bat は起動用の 3 行だけ。作った直後に、Python なら `python3 ~/shared/workflow-kit/tools/check_py.py`、ps1 なら部屋の pwsh 7 で `~/shared/workflow-kit/tools/check-ps1.ps1` を実行する）。ps1 は、実行先に Python が無いときなどの例外。
- 人が Windows で叩いた `verify` / `run` の失敗を伝えたら、ログを頼む前に `ai/work/<名前>-result.json` を読み、Area の台帳（`ctx/area/knowledge/windows-run-causes.md`）を引く。原因が分かったら `ai/out/stock/windows-run-causes.md`（`scope: area`）に書く（`script-guide.md` の「原因の台帳」。2026-10-25）。
- 部屋の git（`/mnt/room/<名>` の下で使える、部屋のローカルの git）は例外で、AI が使う（許可は要らない。リポジトリは `room start` が用意済みなので、AI は `git init` `git config` をしない。この案内は、部屋の `~/.claude/CLAUDE.md` と `~/shared/ROOM.md` の両方に入る。`git diff` で回収される変更を見る。コミットは、人に言われなくても、作業の区切りと `wrap` のたびに行う。push は、リモートが無いので行わない）。セッションの終わりに捨てるので、works には届かない。works へのコミットは人の `room start` の回収が既定で行い、人が最終コミット分を回収する。
- `wrap-hook.md` の手順「コミットする」は、部屋では部屋の git へのコミットまで行う（指示は要らない。push はしない。works へのコミットは回収の側）。`wrap-hook.md` の手順「昇格の案を出す」の知識化は、部屋では `ai/out/stock/` の下書きに一本化する（下の `stock`）。部屋の `wrap` は、業務の知識を `ai/docs/` に残し、共有知は `stock` の窓口だけから出す（公開は `ai/out/stock/`、Area の業務は `ai/out/knowledge/`）。

## `ai/out/close.md` の書き方（部屋の中）

Project を終えるときの、部屋の AI の判断。人が頼んだとき、または AI が完了条件の達成を確認したときに提案して、書く（提案だけで、勝手に書かない）。完了条件を達成したら、見直し日を待たずに閉じる。`room close` は、このファイルが無いと止まる。

1. **完了条件**: `ai/ctx/README.md` の完了条件を、実測（コマンドと結果）で確かめ、結果を書く。未達なら、`close.md` は書かず、残りを `ai/docs/log.md` の Next Actions に書いて止まる。
2. **暫定の見直し**: `ai/docs/decisions.md` で暫定にしていた決定を、実測で見直す。変えるものは、人の承認を得てから `decisions.md` に書く。
3. **未解決の振り分け**: Next Actions と Open Questions の残りを、Area へ渡す、次の Project、破棄に分ける。Area へ渡すものは、`- 【案件】<内容>` の行にする（`room close` がこの行を Area の `ai/docs/inbox.md` に追記する）。Project の決定を Area へ上げるときは、`- 【決定】<要旨>（根拠: <ai/docs/{decisions,log-history,log}.md の見出しの一部>）` の行にする（根拠が見出しに無い、または機密らしい語があると close が止まる。`room trace <Project>#n` で根拠の節を引ける）。
4. **【汎用】候補**: `ai/docs/decisions.md` の未仕分けの【汎用】を一覧にして示す。`stock` は、人が言ったときだけ行う（`ai/out/stock/` に下書き）。

## README 本文の下書きの書き方（部屋の中）

Project の README の本文が雛形のまま（`ai/ctx/README.md` に未記入の `<…>` がある）なら、`brief` の最初に、人に断ってから下書きする。名前・Area・type は `room open` の引数で決まっているので、聞かない（判断基準は `project-structure.md` の「Project を立てる前の判断基準」）。

1. **聞く**（選択式。答えが1つに定まるものは宣言する）: 主題（言語や方式など）、完了条件の種類、見直し日。`dev` の Project は、`brief-work-types.md` の「開発」の項目を、**実装の前に**ここで聞く。
2. **下書きを書く**: `ai/work/plan/6r.md`（先頭に `status: 仮`）に、目的・完了条件・範囲外・未決を 6R として書く。README の目的・成果物は人が埋める（部屋の AI は README に書けない）ので、報告に 1〜2 文の案を添える。完了条件は、AI が具体案（成果物）を出し、ユーザーが承認してから書く（ユーザーが完了条件を自分で書いて渡したときは、その文を案として扱い、承認の言葉を得てから「ユーザー承認」を書く）。承認の前に「ユーザー承認: 日付」を書かない。既に `ai/work/plan/` に下書きがあれば、読んでから更新する。
3. **記録する**: `ai/docs/log-history.md` に1項目（現在状態に影響するなら `ai/docs/log.md` も更新）。判断（完了条件など）は、ユーザーが承認したものだけを `ai/docs/decisions.md` に決定として書く。
4. **報告する**: 下書きのパス、type、完了条件、見直し日と、人が README に書く目的・成果物の案（Project と Area の `README.md` は書き込めない）。コミットはしない。

## `stock` の下書きの書き方（部屋の中）

まず行き先を決める（2026-10-24 ユーザーの決定）。問いは「実名や社内の事情を剥がしても、社外の人が使えるか」。使えれば `scope: public`、剥がすと意味が無くなれば `scope: area`。迷うときは `area`（公開は取り返しがつかない。後で一般化して `public` に出せる）。形は `stock-hook.md` の7見出しで、どちらも同じ。

**`public`**: `ai/out/stock/YYYY-MM-DD-<topic>.md` に書く。frontmatter に次の2つを足す（点検スクリプトは、知らない項目があっても FAIL にしない）。

- `base_commit: <~/shared/ROOM.md の基準コミット>`
- `observed: YYYY-MM-DD`（観測した日。並べる順は到着順でなく、この日付）

**`area`（external・internal 共通。internal も 2026-11-02 に同じ道にした）**: `ai/out/stock/YYYY-MM-DD-<topic>.md` に、frontmatter `scope: area` を付けて書く（`base_commit` と `observed` は付けない）。行き先の区分は `dest: knowledge`（知識。既定）か `dest: docs`（決定・経緯）。実名を含めずに書く。人が `room stock <名> --dst area` で、`cleankit` の点検（金額・メール・電話などの形、`mask.toml` の語）を通して `areas/<Area>/ai/<dest>/` に運ぶ（internal は `mask.toml` の語が空だと止まる。人が通した業務データが部屋にあるため）。点検に当たると何も運ばれないので、当たった形を書き換える。次の Project 以降は、`start` が `areas/<Area>/ai/{knowledge,docs}/` の写しを `ctx/area/` に読み取り専用で置く。**過去の決定や経緯から今の判断をするときは、先に `ctx/area/` を読む**。

`area` は internal も上の道（`ai/out/stock/` → `--dst area` → `ctx/area/`）を使う（2026-11-03 に `restore` / `pull` の知識用の経路を外した）。公開側に出せる一般則が育ったら、別ファイルで `public` の下書きを書く。

`stock 理解` の下書き（`kind: explain`）も同じ場所に書く。形は `stock-explain.md`（部屋の中では、マスク後の語だけで書く。対応表の語を含む下書きは、`room stock` が運ばない）。

`public` は、人が `room stock <名> --dst kit` で確認して `exmem/inbox/` に運ぶ。運ばれた下書きは `ai/out/stock/` から消える（move。2026-11-04）。消えた下書きを書き直さない。残っている下書きは、まだ運ばれていないもの（`area` も同じ）。`kind` はそのまま運ばれる。`scope: area` の下書きが `ai/out/stock/` にあっても、`room stock` は運ばない。基準以降に統合先の `lessons/` が変わっていると、`base_stale` が付く。`integrate` は、印が付いたメモを、基準の版・下書き・最新の版の3点で照らして統合する（食い違いは Open Questions）。

## 計画（部屋の中）

Project の目的・完了時期・マイルストーンは、README に写さず、計画（`ai/work/plan/`。6R・憲章・WBS・マイルストーン）を読む。README の「計画:」の行は、その場所を指す固定のポインタ。各ファイルの先頭に `status: 仮 | 正式` と `approved: 日付` を書き、承認はユーザーが行う（部屋の AI は `正式` にしない）。`room start` は、正式なファイルのハッシュを manifest に記録し、承認のあとで内容が変わっていれば警告して `仮` に戻す（検知だけで、書き換えは止めない。2026-11-03）。

## 知識の統合と成果物の置き場（部屋の中）

2026-10-21 ユーザーの決定（`topics/private-knowledge/` の決定の移し先は `docs/decisions.md` の同日の項）。部屋の AI は実名を見ない。マスクのまま書く。知識は人が `room stock --dst area` で、最終版は `room restore` か `room close` で Area に置く（`start` は自動で行わない）。

- **統合した知識**: `ctx/area/`（`start` が置く Area の `ai/{knowledge,docs}/` の読み取り専用の写し）を読み、統合したノートを `ai/out/stock/<英数字の名前>.md` に書く（`scope: area`、`dest: knowledge`）。実名を含めない。人が `room stock <名> --dst area` で運ぶ。同じ名前のファイルが Area にあり、前回運んだ後に人が変えていると、`stock` は運ばずに止まる（人が確認して消すか、名前を変える）。
- **Area に実名で戻したい最終版**: `ai/out/deliverable/` の下に置く。人が `room restore` を実行するか、`room close` すると、Area の成果物置き場（Project 名の下）に書く（マスクした Project は実名に戻して、マスクしていない Project はそのまま）。Project の成果物は `ai/out/<成果物名>/` に置き（置き場と構成は `project-structure.md`）、`deliverable/` に置かない。`deliverable/` の外の `ai/out/<成果物名>/` は、従来どおり Project の `_noai/final/` に戻る。
- **残したい知見**（`stock`）は、行き先を `scope:` で決める（下の `stock` の節）。Area の業務に固有なら `scope: area`、公開できる一般則なら `scope: public`（どちらも `ai/out/stock/`）。

## 分担と受け渡し

| 場面 | AI（部屋の中）が行う | 人（`room`）が行う | 受け渡しのファイル |
|---|---|---|---|
| `open`（合言葉なし） | 目的・完了条件の聞き取りと 6R の下書き（下の節） | `room open <名>`（ひな形）。README の目的・成果物は人が埋める | `ai/work/plan/6r.md`（`status: 仮`） |
| `brief` | 開始インタビュー | `room start <名>`（チェック、写しの送付、マウント、起動。マスクは人が先に `room mask`） | `ai/ctx/`、`ai/in/` |
| `wrap` | `ai/docs/` の更新、昇格の案、部屋の git へのコミット | 回収（works へのコミット。復元は人が `room restore`） | `ai/docs/log.md`、`ai/docs/decisions.md`（Area へ渡す項目に【案件】ラベル） |
| `close`（合言葉なし） | `ai/out/close.md` を書く（下の節） | `room close <名>`（`ai/out/deliverable/` を Area の成果物置き場へ、Area へ転記、状態の更新、`archives/` へ移動） | `ai/out/close.md` |
| `stock`（`public`） | 下書きまで | `room stock <名> --dst kit`（確認なしで `exmem/inbox/` へ運び、運んだ後に表を出す） | `ai/out/stock/`（先頭に基準コミットと観測日） |
| `stock`（`area`。external・internal 共通） | `ai/out/stock/` に `scope: area` で書く（実名なし） | `room stock <名> --dst area`（cleankit の点検を通して `areas/<Area>/ai/` へ。internal は `mask.toml` の語が要る）。次の Project の `ctx/area/` に写る | `ai/out/stock/` |

`integrate` `review` は、部屋では行わない（`hooks.md` の r/w 表で －。works 側の workbase の作業）。works の作成と雛形の反映は `room mkworks`、部屋の作成は `room init`（どちらも人が打つ）。
