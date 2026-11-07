---
type: explain
title: Area を跨ぐ共有知: workbase の共有知との違いと、設計の軸（理解ガイド）
tags:
  - knowledge-management
  - para
  - security
  - harness
triggers: [Area, 共有知, 会議録, room stock, knowledge, Area跨ぎ, 横断, 業務知識]
---

# Area を跨ぐ共有知: workbase の共有知との違いと、設計の軸（理解ガイド）

works の Area（非公開）に溜める知識を、別の Project の AI 作業部屋でも使えるようにするとき、何が難しいのか、公開の共有知（workbase の `exmem` と `guides`）と何が違うのか、どこで設計を選ぶのかを、自分で説明できるところまで理解するための文書。会議録は最初の題材だが、この文書は題材を限らない一般の話として書く。

> **現行の設計（2026-11-06 時点）**: 実名の会議録を部屋に渡さない。部屋の AI が**実名なしで**書いた知識・決定・経緯を、人が `room stock --dst area` で Area の `ai/{knowledge,docs}/` に運ぶ（`cleankit` の点検が関門）。次の Project では `start` が `ctx/area/` に読み取り専用の写しを置き、AI が先に読む。手順は `guides/howto/ai-room-setup-script.md` の 4.1、決定は `docs/decisions.md` の 2026-11-02・11-03。以前の案（実名の知識を取り出してマスクして渡す `room pull`、`restore` で実名に戻して Area に書く）は、2026-11-03 に `pull` を、2026-11-06 に語のマスク・復元を廃止した（経緯は git の履歴）。

- 前提: works は PARA 構成（`areas/` `projects/` `archives/`）で、リポジトリの外にある。AI 作業部屋（[[ai-room-why]]）は、作業中の Project の `ai/` だけを見せる WSL の部屋。共有知の正本は workbase の `exmem/`（AI 向け）と `guides/`（人向け）
- 確認状況: 規則と手順書を読んだ範囲での整理。`stock --dst area` と `ctx/area/` は単体テストで確認し、実機の通しは未確認。Obsidian の Bases での一覧は未確認
- 勤務先名、顧客名、実際の Project 名などの固有情報は、この文書に書かない

## 1. 状況と解決（ダイジェスト）

**状況**

- 打合せの決定・ToDo・背景のような知識は、特定の Project に閉じず、Area 全体に効く。しかし置き場が Project 内（`ai/work` と `ai/in`）だと、Project が閉じて `archives/` に移るときに、他の Project から引けなくなる
- workbase の共有知は、公開リポジトリにあり、固有名を持たない。顧客名や案件の内容を含む知識は、そこに置けない

**原因**

1. 部屋の AI は、Area を直接読めない。部屋に渡るのは、Project の `ai/` と、Area の README の写し（`ai/ctx/area-README.md`）、`ctx/area/` の写しだけ
2. Area の実名の知識は、部屋の AI に渡さない決まり
3. workbase の共有知には、書き込みから育てる流れ（`stock` → `inbox` → `integrate`）がある。Area の側には、同じ流れが要る

**解決**

- 部屋の AI は、実名を含めずに知識の下書きを書く（`ai/out/stock/`、`scope: area`）
- 人が `room stock --dst area` で運ぶ。運ぶ前に `cleankit` の点検（金額・メール・電話などの形、`_noai/mask.toml` の語）を全ファイルに掛け、1つでも当たれば止める
- 次の Project 以降は、`start` が Area の `ai/{knowledge,docs}/` の写しを `ctx/area/` に読み取り専用で置く

```
部屋の AI（実名なしで書く）
  ai/out/stock/（scope: area） ── room stock --dst area（点検が関門）──▶ Area の ai/{knowledge,docs}/
                                                                              │ start が写す（読み取り専用）
  次の Project の ctx/area/ ◀─────────────────────────────────────────────────┘
```

## 2. 理解のための基礎知識

### 2.1 workbase の共有知との違い（マトリックス）

| 軸 | workbase の共有知（exmem / guides） | Area を跨ぐ共有知 |
|---|---|---|
| 共有の単位 | 全作業ディレクトリ | 1つの Area |
| 公開範囲 | 公開リポジトリ | 非公開（works 側） |
| 実名を消す時期 | 書くとき（一般化して固有名を剥がす） | 書くとき（部屋の AI が実名なしで書く） |
| AI の読み方 | 直接読む（読み取り専用の参照、`find-knowledge`） | `ctx/area/` の写しを読む |
| 知識の性質 | 一般化した原則・落とし穴。1ファイル1トピック。長持ち | 固有の事実・決定・経緯（実名なし）。寿命は Area に紐づく |
| 書き込みの流れ | `stock` → `inbox` → `integrate` でトピックに統合する | `stock --dst area` で Area に運ぶ |
| 置き場と同期 | 公開 Git。複数 PC に配る | works 側（リポジトリの外）。PC ごとの扱いは要確認 |
| 索引・タグ | `exmem-index.md` と `tags.md` が正本 | 同じ型・タグ・索引にそろえると決めたが、索引の置き場は未設計 |
| リンクの向き | 共有側から works へは張れない | works 側から workbase へは張れる（一方向） |
| 退役 | `status: superseded` で残す | Project や Area が閉じると `archives/` に移る |

最大の違いは、「公開されるか」と「固有の事実を持つか」の2つ。ほかの違いの多くは、ここから出る。

### 2.2 設計の軸

| 軸 | 選択肢 | 現行 |
|---|---|---|
| 渡し方 | (a) Area の実名の知識を取り出し、加工して `ai/in/` に置く / (b) 知識を常に実名なしで持つ / (c) AI が Area を直接読む | **(b)**。Area の知識を実名なしで書き、`ctx/area/` に写す。(a)（`pull`、マスクして渡す）は廃止。(c) は `areas/` を AI が扱わない決まりに反する |
| 実名を消す時期 | 書くとき / 渡すとき | **書くとき**。実名を含む会議録などは部屋に渡さない（語の置換は構造の穴を塞がず、書いていない語も残るため） |
| 戻り | AI の出力を Area に戻す / 戻さない | **知識・決定・経緯は `stock --dst area`**。人が読む成果物は `ai/out/<Project 名>/` に置く（2026-11-07 から `close` は Area へ渡さず、archives に残る）。2026-11-05 から、`close` は Area の inbox へ【案件】を運ばない（置き場の分け方は [[ai-room-data-layout-explain]]） |
| 統合 | 件ごとに溜める / 統合して育てる | **Area に置く**。部屋の AI が下書きを書き、人が運ぶ。works の AI は実名を読まない。`integrate` の権限は変えない |
| 知識の層 | ① 事実（実名、Area）/ ② 実名なしの知識（Area の `ai/`）/ ③ 一般化した教訓（workbase） | 固有の事実は、仮名にしても workbase に切り出さない。③ は一般化したものだけを、`room stock` で出す。下書きの `scope:` で振り分ける: 剥がしても社外で使える → `public`（`exmem/inbox/`）、剥がすと意味が無い → `area`（Area の `ai/`） |

### 2.3 一般の型

1. 部屋の AI が書く知識は、種類を問わず同じ約束事を持つ: frontmatter に `scope:` とタグ、`stock-hook.md` の見出し
2. 運ぶときは、`cleankit` の点検（形と、任意の `mask.toml` の語）を通す。当たれば、人が下書きを直して、やり直す
3. 運んだ一覧（どのファイルを、どこへ）は、運んだ後に表で出る

自分で説明するときの一言: 「Area の知識は、部屋の AI が実名なしで書き、人が点検を通して Area に運ぶ。次の部屋は、その写しを読み取り専用で先に読む」

## 3. チェックリスト（症状・疑問 → 原因 → 対処）

| 症状・疑問 | 原因 | 対処 |
|---|---|---|
| 別の Project の部屋で、Area の過去の決定が引けない | 部屋に渡るのは Project の `ai/` と `ctx/` の写しだけ | 前の Project で `room stock --dst area` を運んだか確認する。運んでいれば、次の `start` で `ctx/area/` に写る |
| `stock --dst area` が止まる | 点検が、金額・メール・電話などの形か、`mask.toml` の語を見つけた | 報告を見て、下書きの該当箇所を実名なしに直す。語の表を足すなら `_noai/mask.toml` に書く（任意） |
| 実名が下書きに混ざった | 部屋の AI が原本の語を知っている | 運ぶ前に人が読む。点検は形と表の語だけで、人名などは見つけられない |
| 冒頭の数行と frontmatter の ToDo がずれる | 同じ内容を二重に持った | frontmatter を正にして、冒頭の数行をそこから書く |

## 4. 補足

### 4.1 経緯

- 最初の題材は、顧客を含む打合せの記録（会議録）。「AI 向けと私向けの2系統にしたい」は手段で、論点は「読者の違う1つの情報をどう管理するか」だった
- 分ける基準は「読む問いが違い、かつ中身も違うか」。同じ事実の表示違いは分けない（分けると同期がずれる）。手順書のように問い（順序・実行）が違うものは分ける
- 2026-10-21 は、実名の知識を取り出してマスクして渡し、`restore` で戻す案で通し試験をした。2026-11-03 に知識用の経路を `stock --dst area` と `ctx/area/` に置き換え（`pull` を廃止）、2026-11-06 に語のマスク・復元を廃止した

## 5. 要確認事項

- `stock --dst area` と `ctx/area/` の実機の通し
- Area 側の保管場所と同期（Git か、PC ごとのローカルか）
- 型の用語が、理解ガイドの型（6 つの見出し）と食い違わないか
