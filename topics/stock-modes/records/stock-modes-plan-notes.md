---
type: record
title: stock のモード追加の計画の作り方のメモ
tags:
  - workflow
  - knowledge-management
created: 2026-10-20
updated: 2026-10-20
---

# 作り方のメモ: stock のモード追加

6R は [[stock-modes-6r]]、憲章・WBS・マイルストーンは [[stock-modes-plan]]。手順は `workflow-kit/start-plan.md`。

## 迷った点・決めたこと

- 出力先は A（`exmem/inbox/` 維持、`kind` で区別）。ユーザーが選択（2026-10-20）。C（`guides/inbox/`）は「煩雑」、D（`workbase/inbox/`）は「影響の割に動作が同じ」で却下。
- モード名は `stock 理解` と `stock ナレッジ`。引数なしは1問で選ばせる（ユーザー、2026-10-20）。
- `integrate` はフックを分けず、`kind` で分岐する。理解ガイドの型は既存の型を使う（ユーザーの方針）。
- 全員がユーザーの題材なので、メンバー・リーダー・オーナーの欄と、必要なマイルストーンの欄は省いた。承認が要る変更先と機微の欄を足した（前回の所見）。
- 置き場は `topics/planning-method/`（ユーザーが指定、2026-10-20）。

## 推測・未確認

- 日付、予算（判断の回数・セッション数）は推測。
- 通し試験の「理解ガイド1本分」は、既存の `guides/explain/` のうち1本を元に使う（どれかは M3 で決める）。
- `room` の中の `stock 理解`: 下書きは `ai/out/stock/` に置き、`room stock` が `exmem/inbox/` に運ぶ。`kind` がそのまま運ばれるかは 1.2.3 で `room.py` を読んで確かめる（未確認。コード変更が要るかも未確認）。

## 本との違い

- 本は未読。欄名は図表からの読み取り（`start-plan.md` のとおり）。
