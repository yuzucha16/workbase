---
type: procedure
title: Area の知識の通し試験の手順（room pull → 統合 → restore）
tags:
  - workflow
  - knowledge-management
  - harness
created: 2026-10-21
updated: 2026-10-28
---

# 通し試験の手順: `room pull` → マスク → 部屋で統合 → `restore` → Area の知識置き場

`pull` と `restore` の知識置き場への書き戻しを含む流れを、実機（WSL の部屋）で確かめる手順。**内容はすべて架空のダミー**で、実データは使わない。`room` の操作は人が Windows で実行する（AI には実行させない）。結果は、報告に数字と合否だけ書く（実名は書かない）。2026-10-21 に旧オプションで全項目を実施し、問題なしだった（ユーザーの報告。個別の数字は記録していない）。その後に `room` の `type` が `dev` と `inv` になり、知識置き場が `_noai/knowledge/` に移ったため、手順を今の形に直した（2026-10-28。**この直した形では未実施**）。

## 準備

- ダミーの Area `pk-test` で行う（実在の Area を汚さない）。部屋が無ければ `uv run room.py init pk-test --boundary internal`（時間がかかる。既にあれば流用）。
- Project を作る: `uv run room.py open pk-e2e --area pk-test --type inv`
- `projects/pk-e2e/_noai/mask.toml` に、次を書く:

```toml
[terms.CUST]
acme = ["アクメ商事株式会社", "アクメ商事"]

[terms.PERSON]
tanaka = ["田中太郎"]
```

- `areas/pk-test/_noai/knowledge/`（知識置き場。README の `knowledge_dest:` で変わる）を作り、次の3ファイルを置く（本文は短くてよい）。

`2026-10-14-アクメ商事-定例.md`（取り出す対象）:

```markdown
---
type: area-note
kind: meeting
title: 在庫システム更新の定例
status: active
date: 2026-10-14
org:
  - アクメ商事
tags:
  - knowledge-management
created: 2026-10-14
updated: 2026-10-14
todo_open: 1
todo_due: 2026-10-21
---

# 在庫システム更新の定例

## 冒頭
- 決定: 切替は11月第2週。ToDo: 項目一覧をアクメ商事が10-21 までに出す。

## 決定
- 切替日を11月第2週にする。理由: アクメ商事の締め処理と重ならない。【案件】

## ToDo
| 内容 | 担当 | 期日 | 状態 |
|---|---|---|---|
| 移行データの項目一覧を出す | 田中太郎（アクメ商事） | 2026-10-21 | 未了 |
```

`2026-10-15-自社内の打合せ.md`（`org: 自社`。取り出されない）、`2026-10-01-古い定例.md`（`org: アクメ商事`、`status: superseded`。取り出されない）。形は上と同じで、中身は短くてよい。

## 手順と確かめること

| # | 操作 | 確かめること（合否を報告に書く） |
|---|---|---|
| 1 | `uv run room.py pull pk-e2e --where org=アクメ商事` | 一覧は1件だけ（`org` 一致かつ active）。`y` で `_noai/raw/area/` に写り、ファイル名は `2026-10-14-<ハッシュ>.md`（実名を含まない）。`_noai/map/pull-sources.json` に元の名前がある |
| 2 | `uv run room.py mask pk-e2e` | `ai/in/area/` に写しができる。本文・frontmatter の `org:` の値に `アクメ` が残らない（`⟦CUST_001⟧` になる）。`田中太郎` も残らない。警告が出れば内容を記録する。`ai/records/manifest.json` に実名が無い |
| 3 | `uv run room.py start pk-e2e` で部屋の AI に依頼する: 「`ai/in/area/` を読み、`ai/out/knowledge/topic-cutover.md` に統合ノートを書く。frontmatter は `kind: integrated`、`status: active`、`org` はそのまま。ファイル名は英数字」 | AI が `ai/in/area/` を読める。プレースホルダー（`⟦…⟧`）を壊さずに書く。AI が実名を知らない |
| 4 | 部屋を終了（自動で `restore`） | `areas/pk-test/_noai/knowledge/topic-cutover.md` ができ、`⟦…⟧` が実名（`アクメ商事株式会社` など）に戻っている。`_noai/final/knowledge/` にも同じものがある。`org:` の値が実名に戻っている |
| 5 | Area の知識置き場の `topic-cutover.md` を人が1行書き換え、`room restore` を実行する。続けて `--force` 付きで実行する | 最初の `restore` は止まり、何も書かない。`--force` で上書きされ、直前の版が `_noai/final/_prev/knowledge/topic-cutover.md` にある（2026-10-21 に警告から停止へ変更。決定 ㉕） |
| 6 | 部屋の AI に、ファイル名に `⟦CUST_001⟧` を含む出力を書かせる（または手で `ai/out/knowledge/` に置く） | `restore` が何も書かずに止まる（プレースホルダーが残る） |

見るべき指標（6R の指標）: 統合ノートの冒頭に収まった決定・ToDo の数と、人が直した箇所の数（ダミーの試験では測らない。実例1件で測る）。

## 試験のあとに分かったら足す

- 2で `org:` の値が置換されない場合: 語の辞書に載っていない、または frontmatter が対象外。対処は、`org:` の値を辞書に足す（設計の再検討が要るなら decisions に書く）。
- 3で AI が `ai/in/area/` を読めない場合: `ai/in/` は読み取り専用でマウントされる（`start` の仕様）。パスと権限を確かめる。
