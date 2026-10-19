---
type: howto
title: マスクだけで資料の要約を出す（data: mask）
tags:
  - security
  - tool/wsl
  - ai/claude
  - windows
---

# マスクだけで資料の要約を出す（`data: mask`）

顧客情報を含む資料（議事録、事業戦略の資料など）を、AI に原本を見せずに要約・アクション抽出させる手順書。マスクした写しだけを AI に渡し、**実名には戻さない**（読むのは本人だけ）。部屋（`room-<Area>`）は作成済みとする（[[ai-room-setup-script]] の 2 章）。なぜこの型か、3つの型の違いは [[ai-room-why]]。

- **ゴール（完了の目安）**: `ai/work/` か `ai/out/` に、プレースホルダー（`⟦CUST_001⟧` など）入りの要約ができ、原本と対応表を AI が読んでいないこと
- 範囲: Project の作成から、要約の受け取りまで。`close` は [[ai-room-setup-script]] の 7 章
- 実機の確認: `data:` の3つの型の通しは確認済み（2026-10-19、ユーザー）。pptx・txt の実データでの確認は未了

## 全体の流れ

| 章 | 内容 | 区分 | 完了の目安 |
|---|---|---|---|
| 1 | Project を `data: mask` で作る | 手動（`room open`） | `_noai/` に `raw` `map` `user` がある |
| 2 | 原本を置き、語の表を書く | 手動 | `_noai/raw/` に原本、`_noai/mask.toml` がある |
| 3 | マスクして、部屋で要約させる | 手動（`room start`） | 要約ができる |
| 4 | 要約を読む | 手動 | プレースホルダー入りの要約を、人が読む |

## 1. Project を作る

```powershell
uv run room.py open <Project> --area <Area> --type doc --data mask
```

- `_noai/` には `raw/` `map/` `user/` ができる（`final/` は無い。復元しないため）
- README の本文（目的、完了条件）を書く。ひな形のままだと `close` が通ってしまう

## 2. 原本を置き、語の表を書く

1. 原本（csv・md・txt・xlsx・pptx）を `_noai/raw/` に置く。docx は対象外
2. `_noai/mask.toml` に語の表を書く（`[terms.<種類>] キー = ["正式名", "表記ゆれ"]`、列単位は `[columns]`。書き方は [[ai-room-setup-script]] の 4 章）
3. 人だけで使う仮置きは `_noai/user/` に置く（予約名。`room` も AI も触らない）

- **よく忘れる点**: **辞書にない名前は置き換わらない**。人名は特に漏れる。`mask` の警告（法人格、敬称、メールアドレス、電話番号、URL の形）を見て、必要な語を足す
- 数値は、既定ではマスクしない

## 3. マスクして、部屋で要約させる

```powershell
uv run room.py mask <Project>      # 先に確かめたいとき（start の最初でも自動で行う）
uv run room.py start <Project>
```

1. `mask` が `_noai/raw/` を `ai/in/` にマスクして写す。語が残っていれば止まる
2. 部屋の AI に、`ai/in/` を読んで要約・アクション抽出を頼む。成果物は `ai/work/` でも `ai/out/` でもよい
3. 終わったら、`start` が自動でアンマウントする。`data: mask` なので**復元は行わない**

- 目安: 「回収: 変更 N 件」に、要約のファイルが出る

## 4. 要約を読む

- 要約はプレースホルダー入り。実名で読みたいときは、`_noai/map/` の対応表（実名入り）を人が見る。AI には見せない
- 実名入りの版が欲しいなら、`data: restore` の Project にする（[[ai-room-setup-script]] の 6 章）
- 実名に戻した文書は、works のコミットの対象外（`_noai/` は追跡しない）

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| `start` が `_noai/raw/` があると止まる | `data: none` の Project に原本を置いていないか。README の `data:` を確認する |
| マスクが止まる | 語が残っている。`mask.toml` に足して、`mask` を再実行する |
| `dev` で `mask` にして警告が出る | `type: dev` は `data: none` だけが仕様 |
