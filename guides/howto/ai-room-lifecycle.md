---
type: howto
title: Area の中の Project の一生（room とフックの全体像）
triggers: [room, ライフサイクル, Project の一生, 6R, 論点出し, frame, plan, brief, wrap, room open, room close, 合言葉, フック, 全体像]
tags:
  - workflow
  - tool/wsl
  - ai/claude
---

# Area の中の Project の一生（room とフックの全体像）

Area を作ってから、Project を立て、作業し、閉じ、片付けるまでを、**人が打つ `room` コマンド**と、**部屋の AI に言う合言葉（フック）**を組み合わせて 1 枚で見る手順書。コマンドを 1 手ずつ打つ実例は [[ai-room-setup-script]]、理由は [[ai-room-why]]。ここは「いま何の段で、誰が何を言うか」を見るための地図。

- **ゴール（完了の目安）**: Project の成果物が Area に渡り、`archives/` に移り、`reap` で会話履歴が消える。
- **範囲**: 1 つの Area の中の Project。Area そのものの運営は範囲外。Area の log・decisions は持たず（2026-11-05）、記録は `archives/` から `room trace --area` で引く。Area を終えるのは `room close --area <Area>`（条件は Project 0 件・`stock` の scope: area の未処理 0 件・y/N の宣言。`areas/<Area>` を `archives/areas/<Area>` へ移す。部屋は消さない。2026-11-05）。
- 基準は 2026-11-04 時点のコード（`room.py`）。確認していない箇所は「未確認」と書く。

## 1. 登場するもの

| 層 | 誰が | 例 | 性質 |
|---|---|---|---|
| `room` コマンド | 人（Windows の端末） | `room open`、`room start` | 決まった手順の副作用（作る、マウント、運ぶ、移す）。AI は実行しない |
| 合言葉のフック | 部屋の AI（人が言う） | `brief`、`wrap`、`stock`、論点出し | 判断（聞き取り、下書き、振り分け）。書くのは部屋の中だけ |
| ファイル | 両者の受け渡し | `ai/out/close.md`、`ai/out/stock/` | 2 つの層をつなぐのは**ファイルだけ** |

## 2. 全体の流れ

```
[Area を作る] → [Project を立てる] → [前半: 目的と計画をそろえる] → [作業] → [回収・運ぶ] → [閉じる] → [片付ける]
   人 init        人 open               部屋の AI ＋ 人                 部屋の AI    人 stock           AI close.md→人 close   人 reap
```

`start` から `wrap` までは**セッション**の単位で、作業は何度でも `start` し直す。下の 3〜6 は 1 回きりでなく、行き来する。

## 3. 各段（誰が・何で・何が動くか）

| # | 段 | 人 | 部屋の AI | 止まる主な条件 | 結果 |
|---|---|---|---|---|---|
| 0 | works を用意（PC に 1 回） | `room mkworks` | － | `resources/` が無い | works の雛形 |
| 1 | Area と部屋 | `room init <Area> [--boundary]`、ログイン | － | 部屋がすでにある（`--resume`） | `areas/<Area>/`、部屋 `room-<Area>`、成果物置き場 |
| 2 | 立てる前の判断 | 完了条件 1 文、成果物 1 つ、type（`dev`／`inv`）を決める（下の「判断基準」） | － | － | 名前と type |
| 3 | Project を立てる | `room open <P> --area <A> --type …`（閉じた Project の再作業は `--from <前>`。13 節） | － | `.gitignore`、`boundary:` | `projects/<P>/`（README はひな形。目的と成果物だけ） |
| 4 | 入力（任意。internal の Area だけ） | 原本を `_noai/raw/` へ → `room clean` → `ai/in/` を読む | － | external では止まる | `ai/in/`（未確認の印） |
| 5 | 起動 | `room start <P> [--adopt]` | （起動される） | マウント残り、未確認の `ai/in/`、来歴の不一致 | `ai/ctx/`（README の写し）、`~/shared`（kit の写し） |
| 6 | 前半のお作法（4 節） | 合言葉を言う、承認する | 計画・論点の下書きを作る | － | 6R、論点、計画 |
| 7 | 作業 | 指示、承認 | 成果物を `ai/out/<成果物名>/` に作る。`wrap` で `ai/docs/` を更新 | － | 成果物、記録 |
| 8 | 終わり（セッションごと） | 部屋を閉じる（Enter） | `wrap` | － | 回収（`ai/docs/` が works にコミットされる） |
| 9 | 運ぶ（随時） | `room stock [--dst kit\|area]`（省くと各下書きの `scope:` に従う。確認なし。運んだ元は消え、結果は表で出る） | `stock` で下書き（`ai/out/stock/`） | 点検（cleankit）に当たる、`scope:` が無い、人が Area 側を変えている | 共有知、Area の成果物 |
| 10 | 閉じる判断 | 「閉じよう」と言う | `ai/out/close.md`（完了条件の実測、決定の見直し、【案件】の振り分け） | 完了条件が未達なら書かず Next Actions に残す | `close.md` |
| 11 | 閉じる | `room close <P>` | － | マウント残り、未 push の clone、決定の根拠が不明。**README がひな形のまま・`close.md` 無しは警告（y/N。非対話では止まる）** | `archives/<P>/`、成果物が Area へ |
| 12 | 片付ける | `room reap`（close の 14 日後。早めるなら `--force`） | － | － | 会話履歴が消える（写しは Windows 側に残る） |
| 13 | 後から引く | `room trace --area <A> <語>` | － | － | 閉じた Project の記録の節（閉じた順） |
| 14 | 再作業（機能追加など） | `room open <新> --area <A> --from <前>` | `plan` が引き継いだ `close.md` と前の計画を読む | 前が `archives/` に無い／`done` でない／別の Area（写すものが無いときは止めず来歴だけ。成果物は git 追跡外なので、閉じた PC で） | `ai/in/from-<前>/`。archives は開き直さない |

### 判断基準

`room open` の前に人が確かめる（正本は `workflow-kit/project-structure.md`）。完了条件を 1 文で書けるか（書けなければ Project でなく Area）、見直し日を置けるか、成果物が 1 つに特定できるか、進行中の上限（暫定 3 件）。type は成果物で決める: 結論と出典なら `inv`、作って保守するなら `dev`。

## 4. 前半のお作法（`plan` と `brief`）

`room open` のあと、`start` の前後で、状態は 2 つある（2026-11-04 ee の決定）。**状態 1（`room open` 直後）は Project の方向性が未決**で、`plan` が 6R → 論点出し → 憲章以降（任意）で決める。**状態 2（`room start` 直後）は作業の方向性が未決**で、`brief` が計画に向けて各タスクを進める。room はこの順を強制しないし、行き来してよい（6R は更新する前提で書き、論点出しの結果は 6R に戻す）。どれも部屋の AI への合言葉か依頼文で、出力の型は依頼の言葉で自動的に引かれる。小さな Project では、計画を人の頭の中で進めてよい（`plan` は必須でない）。

| 順 | 言うこと | 目的 | できるもの | 置き場 |
|---|---|---|---|---|
| ① | 「計画を立てて」（`plan`。**6R** が必須の入口） | 状況・問題意識・要求・スコープ・期待する成果をそろえる。README がひな形なら、ここで目的と完了条件を文にする | `ai/work/plan/6r.md`（`status: 仮`） | 人が README の目的・成果物を埋める |
| ② | 「論点出し」「課題設定」（`frame`。`plan` の中でも使う。単独でも言える） | 6R の未決・裏づけを、決／任／後／確／聞に振り分け、実作業の前に決める点だけを固める | 決定メモ | 会話。残すものは `ai/docs/decisions.md`。結果は 6R に書き戻す |
| ③ | 憲章 → 成果物 WBS → マイルストーン（`plan` の中。**任意**） | 日付や複数の成果物が要る大きめの Project だけ。6R で止まってよい | 計画のファイル | `ai/work/plan/` |
| ④ | 承認 | 計画を正式にする | `status: 正式`、`approved: 日付` | 人が先頭を書く。AI は正式にしない |
| ⑤ | 「作業を始めて」（`brief`） | ゴールと前提をそろえる。計画が `正式` なら、次のマイルストーンと未完了の葉をゴール候補にする。計画が無い・`仮` なら `plan` を一度だけ勧める（止めない） | 今日のゴールの要約 | 会話（`events` があれば記録） |

- 小さな Project は 6R だけで始めてよい。完了条件・範囲外・Open Questions は README に書かず、6R が持つ（2026-11-04）。`room readme` は廃止した。
- `start` は正式な計画のハッシュを記録し、**承認のあとで内容が変わっていれば、次の `start` で警告して `仮` に戻す**（検知だけで、書き換えは止めない）。

## 5. 文書・成果物・計画が通る道

| もの | 生まれる | 育てる | Area へ | close 後 |
|---|---|---|---|---|
| README | `room open`（ひな形） | 人が埋める（AI の 6R の下書きを参照） | Area の一覧に 1 行（open で進行中、close で完了） | `archives/<P>/README.md`（`status: done`） |
| 計画（6R ほか） | `plan` → `ai/work/plan/` | 人が正式にする | 運ばない | `archives/` に残る。再作業では `--from` が正式の計画を引き継ぐ |
| 作業の記録（`ai/docs/`） | `room open` | AI が `wrap` で更新 | 運ばない（記録ごと `archives/` へ） | `archives/` に残る。`room trace` の引き先 |
| 成果物 | AI が `ai/out/<成果物名>/` | － | `ai/out/<Project 名>/` の下だけ、`close` で渡る | `archives/` に残る（許可リスト方式では git 追跡外） |
| 知見 | AI の `stock` → `ai/out/stock/` | － | `room stock --dst area`（Area の `ai/`）、`--dst kit`（workbase の `exmem/inbox/`） | － |

README の置き換え方、`stock` の点検、`close` の止まり方の詳細は [[ai-room-setup-script]] の 6 章と `workflow-kit/room/README.md`。

## 6. うまくいかないとき

- `start` が止まる: マウントが残っている（`room umount --area <A>`。外れないときは、Zed のエージェント〔claude-agent-acp〕が部屋の中でマウント点を cwd にして残っている。Zed を終了〔再起動〕してから再実行する。11-06 に実機で確認）、`ai/in/` が未確認（internal なら読んで `start --adopt`。external では入力を置けない）。
- `close` が止まる: メッセージの条件を直してやり直す（何も変えずに止まる）。
- 計画に警告が出た: 内容を確認して、正式に戻すなら `approved:` の日付を書き換える。

## 7. 試験用のダミー Project（`myinv*` / `mydev*`）

コマンドの動作確認や試験は、名前が `myinv` または `mydev` で始まる Project（`myinv`、`myinv1`、`mydev_aaa` など）で行う（2026-11-07 ユーザーの決定）。

- 作り方は普通の `room open <名前> --area <Area>`。本番の Area に置く。部屋（WSL）も本物と同じ動き（特別扱いしない）。
- **git 追跡の対象外**: works の `.gitignore` に `/projects/myinv*/` などを入れてある（雛形は `workflow-kit/templates/workspace/gitignore.template`）。
- `open` / `close` / `start` / `rm` は、コミットしない。Area の README の一覧にも載せず、触らない。`--no-commit` は要らない。
- `close` は、追跡外のファイルとして `archives/` へ移す。`reap` は本物と同じ（`--force` で期限を飛ばせる）。
- 注意: `close` は `ai/out/<名前>/` の成果物を Area に渡す。ダミーに成果物を置くと、本番の Area にファイルが入る。

## 未決

- Area 側の運営（inbox の取り込み）は範囲外。Area の終わり方は `room close --area`（上の「範囲」）。
- 実機で未確認: `room open --from`、`room close` の y/N 警告、`room stock` の move（`docs/log.md`）。
