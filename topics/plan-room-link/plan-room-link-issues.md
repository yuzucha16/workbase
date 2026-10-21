---
type: topic-note
title: 計画と部屋の紐付けの論点と現状
created: 2026-10-21
updated: 2026-10-21
---

# 計画と部屋の紐付けの論点と現状

トピック `plan-room-link` の議論の材料。状態は `docs/log.md`、決定は `docs/decisions.md`。

## 1. 目的

- `room init`（Area）と `room open`（Project）が作る README に、`start 計画` の出力（6R・憲章・成果物 WBS・マイルストーン）を、リンクか転記で関連させる。どちらでもよい（ユーザー、2026-10-21）。
- 紐づくのは `init` / `open` の時点でなくてよい。後からでもよい（ユーザー、2026-10-21）。
- ねらい（〔推測〕。計画のやり方の目的から）: 部屋の AI とユーザーが、Project の目的とゴールを同じ文書で見る。計画が作られたまま読まれない状態を避ける。

## 2. 論点

決めることを、順に並べた。AI の叩き台は「案」に書いた（決定ではない）。

| # | 論点 | 読み | 案（叩き台） |
|---|---|---|---|
| 1 | 計画の本体をどこに置くか | A: Project の `ai/in/`（部屋の AI が読める）/ B: Area の `_noai/` の下（AI に見えない。`pull` で渡す）/ C: README に転記（本体を持たない） | A。`start-plan.md` と lesson の「`ai/work/` で下書き → 人が `ai/in/` に置く」に合う。マスク後の語で書くので、実名の問題が出にくい（〔推測〕） |
| 2 | README に何を載せるか | A: リンクだけ / B: 要約の転記（使命・完了時期・主要マイルストーン）/ C: 6R の全文 | B ＋ 本体へのリンク。Project の README は部屋に写される（`ai/ctx/README.md`）ので、要約は確実に読まれる。全文は 2KB の予算を超えやすい |
| 3 | いつ・誰が README に書くか | A: `open` フック（部屋の AI）が `readme-draft.md` に書き、人が `room readme` で反映 / B: `room` の新しい操作（例: 計画の取り込み）/ C: 人が手で | A。既存の経路だけで済む。新しい操作は、A で手間が見えてから |
| 4 | Area の README に何を載せるか | A: 何も足さない（Project の行だけ）/ B: Project の行に、計画へのリンクか完了時期を添える / C: Area 自身の計画（6R）の欄 | B。Area は期限の無い責任領域で、計画の単位は Project（lesson）。C は Area に期限が無いので合わない（〔推測〕） |
| 5 | `open` の前に計画を作った場合 | 6R だけを works で作り、`open` の後に運ぶ / 計画は必ず `open` の後に部屋で作る | 未定。`start 計画` は works でも部屋でも起動できる（`hooks.md` の表）。順序の決まりは無い |
| 6 | 雛形を変えるか | `README_TEMPLATE`（`room.py`）と `templates/project/README.template.md` に「計画」の節を足す / 足さない | 2 と 3 が決まってから。足すなら、ひな形の `<...>` を `close` の検査（`README_PLACEHOLDERS`）に含めるかも決める |

## 3. 現状の事実

確かめたのは workbase の main（`b22c381`、2026-10-21）。

### room が作るもの

- `room init <Area>`: Area の README を、無ければ frontmatter（`status` `boundary` `updated`）と見出し `# <Area>` だけで作る（`room.py` の `AREA_README_TEMPLATE`）。置き場（`_noai/knowledge/` `_noai/deliverable/` `_noai/source/`、`ai/docs/inbox.md`）も無ければ作る（`scaffold_area`）。
- `room open <Area> <名>`: Project の README を雛形（目的・完了条件・成果物・範囲外・Open Questions の `<...>`、`review: 仮置き（未承認）`）で作り、Area の README の「## 進行中の Project」に1行足し、コミットする（`cmd_open`、`README_TEMPLATE`）。計画の欄は無い。
- 方針（2026-10-21、root `docs/decisions.md`）: 準備は `init` で行い、後続のコマンドは置き場が無ければ何も変えずに止まる。紐付けで新しい置き場を作るなら、この方針に合わせる（〔推測〕）。

### 部屋の AI から見えるもの

- Project と Area の README は、部屋の AI が書き込めない。写し（`ai/ctx/README.md`、`ai/ctx/area-README.md`）を開始時に読む（`room-context.md`）。Area の README が 16 KiB を超えると `start` が警告する（`AREA_README_WARN_BYTES`）。
- README の本文を変える経路は、部屋の AI が `ai/out/readme-draft.md` に書き、人が `room readme <名>` で反映する（`open-hook.md`、`cmd_readme`）。
- `close` は、README に雛形の `<...>` が残っていると止まる（`readme_placeholders`）。
- Area の `_noai/` の下は AI に見えない。部屋に渡すには `room pull`（`_noai/raw/area/` へ）。

### 計画のやり方の決まり

- `start 計画` は `start` のモード（`start-hook.md`）。`start` は works・workbase・dotfiles・room のどこでも起動できる（`hooks.md` の r/w 表）。
- 単位は PARA の Project 1つ。期限付き、上限4週（`exmem/lessons/planning-method.md`）。
- works の置き場（`start-plan.md` の「置き場」）: 参照用の計画と知識は Area 配下。Project の作業用の下書きは、AI が `ai/work/` に書き、承認したものを人が `ai/in/` に置く。Area の README には最新の Project を1行書く。
  - 〔推測〕「Area 配下」が `_noai/` の中か外かは書かれていない。論点 1 の B と関係する。
- 出力は憲章・WBS・マイルストーンの Markdown、作り方のメモは別ファイル（`start-plan.md` の B-5）。
- `open`、`start` のインタビュー、改善4は触らない、という取り込みの論点 B1〜B4（2026-10-19）。このトピックは、その「`open` は触らない」を見直すことになる（〔推測〕。変えるなら `review 消化` の3段に乗る）。
- 振り返り（改善4）に計画を入力として足す案は、やらないことにした（2026-10-21）。

## 4. 変更先の候補（論点が決まった後）

`workflow-kit/room/room.py`（`README_TEMPLATE`、`AREA_README_TEMPLATE`、`README_PLACEHOLDERS`）と tests、`workflow-kit/templates/project/README.template.md`、`workflow-kit/open-hook.md`、`workflow-kit/start-plan.md`（置き場）、`workflow-kit/room-context.md`、`workflow-kit/room/README.md`、`exmem/lessons/planning-method.md`。
