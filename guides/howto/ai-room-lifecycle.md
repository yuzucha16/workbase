---
type: howto
title: Area の中の Project の一生（room とフックの全体像）
tags:
  - workflow
  - tool/wsl
  - ai/claude
---

# Area の中の Project の一生（room とフックの全体像）

Area を作ってから、Project を立て、作業し、閉じ、片付けるまでを、**人が打つ `room` コマンド**と、**部屋の AI に言う合言葉（フック）**を組み合わせて 1 枚で見る手順書。コマンドを 1 手ずつ打つ実例は [[ai-room-setup-script]]、理由は [[ai-room-why]]。ここは「いま何の段で、誰が何を言うか」を見るための地図。

- **ゴール（完了の目安）**: Project の成果物が Area に渡り、`archives/` に移り、`reap` で会話履歴が消える。
- **範囲**: 1 つの Area の中の Project。Area そのものの運営（Area の inbox の取り込み、Area の終わり方）は範囲外（`docs/log.md` の NA に積んである。いまは入口が無い）。
- 基準は 2026-11-04 時点のコード（`room.py`）。確認していない箇所は「未確認」と書く。

## 1. 登場するもの

| 層 | 誰が | 例 | 性質 |
|---|---|---|---|
| `room` コマンド | 人（Windows の端末） | `room open`、`room start` | 決まった手順の副作用（作る、マウント、運ぶ、移す）。AI は実行しない |
| 合言葉のフック | 部屋の AI（人が言う） | `brief`、`wrap`、`stock`、論点出し | 判断（聞き取り、下書き、振り分け）。書くのは部屋の中だけ |
| ファイル | 両者の受け渡し | `ai/out/readme-draft.md`、`ai/out/close.md`、`ai/out/stock/` | 2 つの層をつなぐのは**ファイルだけ** |

## 2. 全体の流れ

```
[Area を作る] → [Project を立てる] → [前半: 目的と計画をそろえる] → [作業] → [回収・運ぶ] → [閉じる] → [片付ける]
   人 init        人 open               部屋の AI ＋ 人                 部屋の AI    人 stock/restore   AI close.md→人 close   人 reap
```

`start` から `wrap` までは**セッション**の単位で、作業は何度でも `start` し直す。下の 3〜6 は 1 回きりでなく、行き来する。

## 3. 各段（誰が・何で・何が動くか）

| # | 段 | 人 | 部屋の AI | 止まる主な条件 | 結果 |
|---|---|---|---|---|---|
| 0 | works を用意（PC に 1 回） | `room mkworks` | － | `resources/` が無い | works の雛形 |
| 1 | Area と部屋 | `room init <Area> [--boundary]`、ログイン | － | 部屋がすでにある（`--resume`） | `areas/<Area>/`、部屋 `room-<Area>`、成果物置き場 |
| 2 | 立てる前の判断 | 完了条件 1 文、成果物 1 つ、type（`dev`／`inv`）を決める（下の「判断基準」） | － | － | 名前と type |
| 3 | Project を立てる | `room open <P> --area <A> --type …` | － | `.gitignore`、`boundary:` | `projects/<P>/`（README はひな形） |
| 4 | 入力（任意。internal の Area だけ） | 原本を `_noai/raw/` へ → `room clean`（または `mask`）→ `ai/in/` を読む | － | external では止まる | `ai/in/`（未確認の印） |
| 5 | 起動 | `room start <P> [--adopt]` | （起動される） | マウント残り、未確認の `ai/in/`、来歴の不一致 | `ai/ctx/`（README の写し）、`~/shared`（kit の写し） |
| 6 | 前半のお作法（4 節） | 合言葉を言う、承認する | 下書きを作る | － | README 本文、論点、計画 |
| 7 | 作業 | 指示、承認 | 成果物を `ai/out/<成果物名>/` に作る。`wrap` で `ai/docs/` を更新 | － | 成果物、記録 |
| 8 | 終わり（セッションごと） | 部屋を閉じる（Enter） | `wrap` | － | 回収（`ai/docs/` が works にコミットされる） |
| 9 | 運ぶ（随時） | `room readme`、`room stock --dst kit\|area`、`room restore` | `stock` で下書き（`ai/out/stock/`） | 点検（cleankit）に当たる、人が Area 側を変えている | README 本文、共有知、Area の成果物 |
| 10 | 閉じる判断 | 「閉じよう」と言う | `ai/out/close.md`（完了条件の実測、決定の見直し、【案件】【決定】の振り分け） | 完了条件が未達なら書かず Next Actions に残す | `close.md` |
| 11 | 閉じる | `room close <P>` | － | `close.md` 無し、README に `<…>`、マウント残り、決定の根拠が不明 | `archives/<P>/`、成果物と【案件】【決定】が Area へ |
| 12 | 片付ける | `room reap`（close の 14 日後。早めるなら `--force`） | － | － | 会話履歴が消える（写しは Windows 側に残る） |
| 13 | 後から引く | `room trace <P>#n` | － | － | 閉じた Project の根拠の節 |

### 判断基準

`room open` の前に人が確かめる（正本は `workflow-kit/project-structure.md`）。完了条件を 1 文で書けるか（書けなければ Project でなく Area）、見直し日を置けるか、成果物が 1 つに特定できるか、進行中の上限（暫定 3 件）。type は成果物で決める: 結論と出典なら `inv`、作って保守するなら `dev`。

## 4. 前半のお作法（`room start` の直後）

`start` したあとの最初の数十分は、次の順で進めることが多い。**room はこの順を強制しない**（運用の型）。どれも部屋の AI への合言葉か依頼文で、出力の型は依頼の言葉で自動的に引かれる。

| 順 | 言うこと | 目的 | できるもの | 置き場 |
|---|---|---|---|---|
| ① | 「作業を始めて」（`brief`） | ゴールと前提をそろえる。確定型か探索型かを決める | 今日のゴールの要約 | 会話（`events` があれば記録） |
| ② | （README がひな形なら ① の中で）README の下書き | 目的と完了条件を文にする | `ai/out/readme-draft.md` | 人が `room readme <P>` で反映 |
| ③ | 「論点出し」「課題設定」 | 作業の前に、決める点だけを洗い出す。各 ID に 決／任／後／確／聞 を付ける | 決定メモ | 会話。残すものは `ai/docs/decisions.md` |
| ④ | 「brief 計画」（6R） | 取り組みの目的とゴールを共有する。6R → 憲章 → WBS → マイルストーン | 計画のファイル | `ai/work/plan/`（先頭 `status: 仮`） |
| ⑤ | 承認 | 計画を正式にする | `status: 正式`、`approved: 日付` | 人が先頭を書く。AI は正式にしない |

- 小さな Project は ③④ を飛ばしてよい（6R だけで止まってもよい）。
- `start` は正式な計画のハッシュを記録し、**承認のあとで内容が変わっていれば、次の `start` で警告して `仮` に戻す**（検知だけで、書き換えは止めない）。
- 順 ③④ の前後（先に論点出しか、先に 6R か）は、運用の例で、決まりではない（NA に積んである）。

## 5. 文書・成果物・計画が通る道

| もの | 生まれる | 育てる | Area へ | close 後 |
|---|---|---|---|---|
| README | `room open`（ひな形） | AI の `readme-draft.md` → `room readme` | Area の一覧に 1 行（open で進行中、close で完了） | `archives/<P>/README.md`（`status: done`） |
| 計画（6R ほか） | `brief 計画` → `ai/work/plan/` | 人が正式にする | 運ばない | `archives/` に残る |
| 作業の記録（`ai/docs/`） | `room open` | AI が `wrap` で更新 | close の【案件】【決定】行だけ | `archives/` に残る。`room trace` の引き先 |
| 成果物 | AI が `ai/out/<成果物名>/` | － | `ai/out/deliverable/` の下だけ、`restore` か `close` で渡る | `archives/` に残る（許可リスト方式では git 追跡外） |
| 知見 | AI の `stock` → `ai/out/stock/` | － | `room stock --dst area`（Area の `ai/`）、`--dst kit`（workbase の `exmem/inbox/`） | － |

README の置き換え方、`stock` の点検、`restore` の止まり方の詳細は [[ai-room-setup-script]] の 6 章と `workflow-kit/room/README.md`。

## 6. うまくいかないとき

- `start` が止まる: マウントが残っている（`room umount --area <A>`）、`ai/in/` が未確認（internal なら読んで `start --adopt`。external では入力を置けない）。
- `close` が止まる: メッセージの条件を直してやり直す（何も変えずに止まる）。
- 計画に警告が出た: 内容を確認して、正式に戻すなら `approved:` の日付を書き換える。

## 未決

- Area 側の運営（inbox の取り込み、Area の終わり方）は範囲外。入口が決まったら 4 の後に足す。
- 4 節の順（論点出し、6R、README の前後）と、README の完了条件を 6R に畳むかは未決（`docs/log.md`）。
- 実機で未確認: deliverable の Area への書き出し（`restore`・`close`）。
