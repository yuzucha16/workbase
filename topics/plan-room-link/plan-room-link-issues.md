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
| 1 | 計画の本体をどこに置くか | A: Project の `ai/in/plan/` / B: Area の `_noai/` / C: README に転記のみ | **A（仮。2026-10-21 ユーザーの前提つき）**: 計画は実名なしで用意する。実名入りが要るときは派生品として別に作る（計画の対象外）。置くのは承認版。作業用の下書きは `ai/work/plan/`（AI）。Area 側の参照用の置き場は未定（事実 3 章） |
| 2 | README に何を載せるか | A: リンクだけ / B: 5節に分解 / C: 全文 / D: 新しい節「計画」だけ | **D に決定（仮。ユーザー、2026-10-21 の案1）**: 完了時期、主要マイルストーン（最大3つ）、6R の要約、本体へのポインタ。既存の5節は触らない |
| 3 | いつ・誰が README に書くか | A: 人が `room readme`（AI が下書き）/ B: 承認で自動反映 / C: 手で | **案 A に決定（仮。ユーザー、2026-10-21）**。承認前後とも改良で何度も作り直すので、手の反映は漏れる。日付は本文に置く（frontmatter は変えない）。仕組みは 3.6 |
| 4 | Area の README に何を載せるか | A: 何も足さない / B: Project の行に完了予定を添える / C: Area 自身の計画の欄 | **A に決定（仮。ユーザー、2026-10-21）**: 完了予定だけならコストのほうが高い。Area は触らない |
| 5 | `open` の前に計画を作った場合 | 6R だけを works で作り、`open` の後に運ぶ / 計画は必ず `open` の後に部屋で作る | 未定。`start 計画` は works でも部屋でも起動できる（`hooks.md` の表）。順序の決まりは無い |
| 6 | 雛形を変えるか | 印つきの空の節「計画」を足す / 足さない | **足す（仮。ユーザー、2026-10-21）**。印の無い既存の Project は反映時に止まって案内し、人が手で貼るのを許容する（パイロット版ばかり）。`close` の雛形チェックは対象にしない |

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
  - **事実の食い違い（2026-10-21、ユーザーの指摘を受けて確認）**: この「Area 配下」は、同日に `knowledge/` を `_noai/knowledge/` に移す前の決定に基づく。いまの `scaffold_area` が作る Area の置き場は `_noai/{knowledge,source,deliverable}` と `ai/docs/inbox.md` だけで、実名なしの参照用の計画を置く場所が無い。`start-plan.md` の表は、ここを直す必要がある（直すのは `review 消化` の後）。
- 出力は憲章・WBS・マイルストーンの Markdown、作り方のメモは別ファイル（`start-plan.md` の B-5）。
- `open`、`start` のインタビュー、改善4は触らない、という取り込みの論点 B1〜B4（2026-10-19）。このトピックは、その「`open` は触らない」を見直すことになる（〔推測〕。変えるなら `review 消化` の3段に乗る）。
- 振り返り（改善4）に計画を入力として足す案は、やらないことにした（2026-10-21）。

### 3.5 6R と README の対応（案。AI の読み。未確認）

README の雛形の節（`README_TEMPLATE`）は、6R の欄にほぼ対応する。新しい節をたくさん足さなくても、分解して置ける。

| README の節 | 6R・憲章のどこから |
|---|---|
| 目的 | 要求（1文）と、問題意識の見出し1文 |
| 完了条件 | 期待する成果（指標1つ）。ユーザー承認の印は計画の承認 |
| 成果物 | 成果物 WBS の第2層（成果物の種類） |
| 範囲外 | 今回のスコープの対象外 |
| Open Questions | 6R の未決 |
| 本文（決定済み。置く節は未決） | 憲章の完了時期と主要マイルストーン（日付）。frontmatter は変えない |

### 3.5 の訂正（2026-10-21 の決定後）

上の対応表は、6R を既存の5節に分解して置く案だった。決定は案1（印の範囲は新しい節「計画」だけ。既存の5節は触らない）。表は、人が `room readme` で5節を書くときの参照として残す。

### 3.6 承認で自動反映する仕組みの事実と案

- 承認の印になりうるもの: 人が `ai/in/` にファイルを置き、`room start --adopt` で来歴（ハッシュ）を記録する流れ。`ai/in/` に記録の無いファイルがあると `start` は止まり、記録後に内容が変わっても止まる（`check_provenance`）。計画の改良のたびに「置き直し → `--adopt`」が要る。
- README を書く既存の経路は `room readme`（下書きの本文を反映）だけ。`start` は README を `ai/ctx/` に写すだけで、書かない（`snapshot_readme`）。
- 案 A: AI が計画4点と一緒に、README 用のブロック（`readme-block.md`。6R からの分解は AI が下書きの時点で行う）を `ai/work/plan/` に書く。人が `ai/in/plan/` に置いて `--adopt` する（承認）と、`room` が README の印つきブロックを機械的に差し替える。`room` は判断せず、写すだけ。
- 案 B: 本物の README は触らず、`start` が `ai/ctx/README.md`（写し）にだけ計画のブロックを合成する。README に計画が見えない（人が Obsidian で読むとき）のが弱点。
- どちらも `room.py` の変更と単体テストが要る。`open` は触らない（2026-10-19）という取り決めの見直しになるので、`review 消化` を通す。

### 3.7 `readme-block.md` の形（叩き台。未確認）

README の印の範囲に入るもの。AI が下書きし、`room` は印の間を置き換えるだけ（承認の日付の行は `room` が書く）。10 行・1KB 以内を目安にし、超えたら `room` が知らせる。

```
## 計画
<!-- plan:start -->
- 完了時期: 2026-11-04（バッファ込み）
- マイルストーン: M1 2026-10-28 …／M2 …／M3 …（最大3つ）
- 6R の要約: 要求 1文。スコープの要点。期待する成果（指標1つ）
- 本体: `ai/in/plan/`（6R・憲章・WBS・マイルストーン）
- 承認: 2026-10-21（room が書く）
<!-- plan:end -->
```

## 4. 変更先（論点 1〜6 の仮決めを実装するとき。承認前）

`review 消化` の3段を通してから行う（`open` は触らないという 2026-10-19 の取り決めの見直しを含むが、`open` 自体は変えない）。

| # | 変更先 | 内容 |
|---|---|---|
| 1 | `workflow-kit/room/room.py` | `README_TEMPLATE` に印つきの空の節「計画」。`cmd_start` で来歴チェックの通過後、`ai/in/plan/readme-block.md` があれば、README の印の間を置き換える（承認日の行は room が書く。内容が同じなら何もしない）。印が無ければ止まって節を貼るよう案内する。10 行・1KB を超えたら知らせる |
| 2 | `workflow-kit/room/tests/` | 置き換え、同じ内容で変更なし、印なしで停止、frontmatter を変えないこと、超過の警告 |
| 3 | `workflow-kit/templates/project/README.template.md` | 同じ印つきの節。注記を足す |
| 4 | `workflow-kit/start-plan.md` | B-5 の出力に `readme-block.md` を足す。置き場の表の works の行から「Area 配下」を直し（事実の食い違い）、`ai/work/plan/` → `ai/in/plan/` に統一する |
| 5 | `workflow-kit/room-context.md`、`room/README.md`、`ROOM.md`（`room.py` の案内） | 部屋の AI が `ai/work/plan/readme-block.md` を書くこと、承認は人の `--adopt` であること |
| 6 | `exmem/lessons/planning-method.md` | 事実と決定を足す |
| 変えない | `open-hook.md`、Area の README、`close` の雛形チェック | 論点 4・5 の決定による |

確認済み（`room.py` の `cmd_start` 末尾、1274 行付近）: `start` の自動コミットは `projects/<P>` 全体を対象にするので、README の反映も同じコミットに入る。反映の位置は、来歴チェックの通過後、`snapshot_readme` の前（部屋の写しに新しい節が入る）。実機での確認は PC1（実装直後は単体テストのみ）。

