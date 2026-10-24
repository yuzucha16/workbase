# 部屋の中でフックを使うとき

AI 作業部屋（`workflow-kit/room/`）の中で、合言葉のフックを使うときの読み替えと分担。`hooks.md` の表が正本（どのフックを部屋で行うかは、同じ `hooks.md` の「領域とフックの権限」）で、ここは部屋の中での差分だけを書く。部屋でないときは読まない。

## 2つの層

| | 運用コマンド（`room …`） | 合言葉のフック |
|---|---|---|
| 呼ぶ人・場所 | 人が Windows の端末で打つ | 人が言い、AI が手順書を読んで実行 |
| 性質 | 決まった手順の副作用（マウント、写しの送付、マスク、移動、コミット） | 判断（聞き取り、確認、振り分け、下書き） |
| 実行者 | スクリプト。**AI は実行しない** | AI |

運用コマンドには必ず `room` を前置し、合言葉は日本語の別名で呼ぶ（`start` は 2026-10-24 に合言葉を `brief` へ改名して、重なりは無くなった。前置は習慣として残す）。2つをつなぐのは**ファイルの受け渡しだけ**。

## 部屋の中の読み替え

- 起動する場所は `/mnt/room/<名>`（Project の `ai/`）に固定される。開始時に読むのは `~/shared/ROOM.md` → `ai/ctx/README.md`（Project の窓口の写し）→ `ai/ctx/area-README.md`（所属する Area の README の写し。Area の共通ルール）→ `ai/docs/log.md`。
- 手順書の `docs/` は、部屋では `ai/docs/`（Project の記録）。Project と Area の `README.md` は書き込めない。写し（`ai/ctx/README.md`、`ai/ctx/area-README.md`）を読む。
- 手順書は `~/shared/workflow-kit/` にある（読み取り専用の写し。基準コミットは `~/shared/ROOM.md`）。
- 副作用を伴う手順（Project の作成、状態の更新、`archives/` への移動、works へのコミット）は AI が行わない。判断をファイルに書いて、人が `room` で反映する（部屋の git へのコミットは別で、AI が行う。下）。
- スクリプトや変換を作るときは、言語をユーザーに聞かず、優先順位 Python → ps1 → bat で決める（`script-guide.md` の「言語の選び方」）。あわせて同じ文書の「実行の方針」に従う（部屋で完結できるなら、すべて部屋で実行する。Excel・COM などの Windows 依存部は、できるだけ小さな層にして、人の手数を 1 コマンドに減らす。2026-10-21）。人が Windows で実行する薄い層は、Python が既定（2026-10-21）。同じ文書の「Windows で実行するスクリプト」に従う（束ねる役も同じ言語、bat は起動用の 3 行だけ。作った直後に、Python なら `python3 ~/shared/workflow-kit/tools/check_py.py`、ps1 なら部屋の pwsh 7 で `~/shared/workflow-kit/tools/check-ps1.ps1` を実行する）。ps1 は、実行先に Python が無いときなどの例外。
- 部屋の git（`/mnt/room/<名>` の下で使える、部屋のローカルの git）は例外で、AI が使う（許可は要らない。リポジトリは `room start` が用意済みなので、AI は `git init` `git config` をしない。この案内は、部屋の `~/.claude/CLAUDE.md` と `~/shared/ROOM.md` の両方に入る。`git diff` で回収される変更を見る。コミットは、人に言われなくても、作業の区切りと `wrap` のたびに行う。push は、リモートが無いので行わない）。セッションの終わりに捨てるので、works には届かない。works へのコミットは人の `room start` の回収が既定で行い、人が最終コミット分を回収する。
- `wrap-hook.md` の手順「コミットする」は、部屋では部屋の git へのコミットまで行う（指示は要らない。push はしない。works へのコミットは回収の側）。`wrap-hook.md` の手順「昇格の案を出す」の知識化は、部屋では `ai/out/stock/` の下書きに一本化する（下の `stock`）。部屋の `wrap` は、業務の知識を `ai/docs/` に残し、共有知は `stock` の窓口だけから出す。

## `ai/out/close.md` の書き方（部屋の中）

Project を終えるときの、部屋の AI の判断。人が頼んだとき、または AI が完了条件の達成を確認したときに提案して、書く（提案だけで、勝手に書かない）。完了条件を達成したら、見直し日を待たずに閉じる。`room close` は、このファイルが無いと止まる。

1. **完了条件**: `ai/ctx/README.md` の完了条件を、実測（コマンドと結果）で確かめ、結果を書く。未達なら、`close.md` は書かず、残りを `ai/docs/log.md` の Next Actions に書いて止まる。
2. **暫定の見直し**: `ai/docs/decisions.md` で暫定にしていた決定を、実測で見直す。変えるものは、人の承認を得てから `decisions.md` に書く。
3. **未解決の振り分け**: Next Actions と Open Questions の残りを、Area へ渡す、次の Project、破棄に分ける。Area へ渡すものは、`- 【案件】<内容>` の行にする（`room close` がこの行を Area の `ai/docs/inbox.md` に追記する）。
4. **【汎用】候補**: `ai/docs/decisions.md` の未仕分けの【汎用】を一覧にして示す。`stock` は、人が言ったときだけ行う（`ai/out/stock/` に下書き）。

## README 本文の下書きの書き方（部屋の中）

Project の README の本文が雛形のまま（`ai/ctx/README.md` に未記入の `<…>` がある）なら、`brief` の最初に、人に断ってから下書きする。旧 `open` フックの手順 4〜5 を移した（2026-10-24）。名前・Area・type は `room open` の引数で決まっているので、聞かない（判断基準は `project-structure.md` の「Project を立てる前の判断基準」）。

1. **聞く**（選択式。答えが1つに定まるものは宣言する）: 主題（言語や方式など）、完了条件の種類、見直し日。`dev` の Project は、`brief-work-types.md` の「開発」の項目を、**実装の前に**ここで聞く。
2. **下書きを書く**: `ai/out/readme-draft.md` に、README の本文だけ（目的、完了条件、成果物、範囲外、Open Questions。雛形は `templates/project/README.template.md`。frontmatter を含めない）。完了条件は、AI が具体案（成果物）を出し、ユーザーが承認してから書く。承認の前に「ユーザー承認: 日付」を書かない。既に `readme-draft.md` があれば、読んでから更新する。
3. **記録する**: `ai/docs/log-history.md` に1項目（現在状態に影響するなら `ai/docs/log.md` も更新）。判断（完了条件など）は、ユーザーが承認したものだけを `ai/docs/decisions.md` に決定として書く。
4. **報告する**: 下書きのパス、type、完了条件、見直し日と、人が `room readme <名>` で反映すること（Project と Area の `README.md` は書き込めない）。コミットはしない。

## `stock` の下書きの書き方（部屋の中）

`ai/out/stock/YYYY-MM-DD-<topic>.md` に、`stock-hook.md` の形式で書く。frontmatter に次の2つを足す（点検スクリプトは、知らない項目があっても FAIL にしない）。

- `base_commit: <~/shared/ROOM.md の基準コミット>`
- `observed: YYYY-MM-DD`（観測した日。並べる順は到着順でなく、この日付）

`stock 理解` の下書き（`kind: explain`）も同じ場所に書く。形は `stock-explain.md`（部屋の中では、マスク後の語だけで書く。対応表の語を含む下書きは、`room stock` が運ばない）。

人が `room stock <名>` で確認して `exmem/inbox/` に運ぶ。`kind` はそのまま運ばれる。基準以降に統合先の `lessons/` が変わっていると、`base_stale` が付く。`integrate` は、印が付いたメモを、基準の版・下書き・最新の版の3点で照らして統合する（食い違いは Open Questions）。

## 計画（部屋の中）

Project の目的・完了時期・マイルストーンは、README に写さず、承認版の計画（`ai/in/plan/`。6R・憲章・WBS・マイルストーン。2026-10-21 `plan-room-link` の決定）を読む。README の「計画:」の行は、その場所を指す固定のポインタ。下書きは `ai/work/plan/` に書き、人が承認して `ai/in/plan/` に置いて `room start --adopt` する（部屋の AI は `ai/in/` に書かない）。

## 知識の統合と成果物の置き場（部屋の中）

2026-10-21 ユーザーの決定（`topics/private-knowledge/` の決定の移し先は `docs/decisions.md` の同日の項）。部屋の AI は実名を見ない。マスクのまま書き、人が `room restore`（`room start` の終わりでも自動）で実名に戻して Area に置く。

- **統合した知識**: `ai/in/area/`（Area から `room pull` で渡された、マスク済みの写し）を読み、統合したノートを `ai/out/knowledge/<英数字の名前>.md` に書く。frontmatter は `kind: integrated`、`status: active`、`org` は元のまま。`⟦…⟧` の記号は変えない。Area の知識置き場の既存ファイルを、人が前回から変えていると、`restore` は止まる（人が `--force` で判断する）。
- **成果物**（人が読む最終版）: `ai/out/deliverable/` の下に置く。`restore` が、Area の成果物置き場（Project 名の下）にも実名に戻して書く。それ以外の `ai/out/<最終成果物>` は、従来どおり Project の `_noai/final/` に戻る。
- **共有知へ出す知見**は、上のどちらでもなく、下の `stock` の窓口（`ai/out/stock/`）。

## 分担と受け渡し

| 場面 | AI（部屋の中）が行う | 人（`room`）が行う | 受け渡しのファイル |
|---|---|---|---|
| `open`（合言葉なし） | 目的・完了条件の聞き取りと README 本文の下書き（下の節） | `room open <名>`（ひな形）→ `room readme <名>`（下書きの反映） | `ai/out/readme-draft.md`（本文だけ。frontmatter を含めない） |
| `brief` | 開始インタビュー | `room start <名>`（チェック、マスク、写しの送付、マウント、起動） | `ai/ctx/`、`ai/in/` |
| `wrap` | `ai/docs/` の更新、昇格の案、部屋の git へのコミット | 回収（復元、works へのコミット） | `ai/docs/log.md`、`ai/docs/decisions.md`（Area へ渡す項目に【案件】ラベル） |
| `close`（合言葉なし） | `ai/out/close.md` を書く（下の節） | `room close <名>`（Area へ転記、状態の更新、`archives/` へ移動） | `ai/out/close.md` |
| `stock` | 下書きまで | `room stock <名>`（人が1件ずつ確認して `exmem/inbox/` へ運ぶ） | `ai/out/stock/`（先頭に基準コミットと観測日） |

`integrate` `review` は、部屋では行わない（`hooks.md` の r/w 表で －。works 側の workbase の作業）。works の作成と雛形の反映は `room mkworks`、部屋の作成は `room init`（どちらも人が打つ）。
