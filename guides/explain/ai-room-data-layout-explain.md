---
type: explain
title: AI 作業部屋のデータの置き場と流れ（原本・成果物・知識）
tags:
  - ai-room
  - security
  - harness
  - para
  - knowledge-management
triggers: [原本, 成果物, データの置き場, _noai, ai/out, 掃除, 部屋のデータ, 知識の流れ]
---

# AI 作業部屋のデータの置き場と流れ（原本・成果物・知識）

## 冒頭
実名を含むデータが Area と Project のどこに置かれ、どの順に流れるか、なぜ分けたかを、自分で説明できるようにする。前提: 実名を AI に見せない作業部屋（`room`）を使い、works は PARA 構成。確認状況: 単体テストで確認。実機の通しは未確認。語のマスク・復元（`mask` `restore`）は 2026-11-06 に、`room clean`・成果物の Area への引き渡し・Area の `_noai/source/` `_noai/deliverable/` は 2026-11-07 に廃止した。この文書は廃止後の現行の姿だけを書く（旧い設計は git の履歴と `docs/decisions.md`）。

## ダイジェスト
- 状況: 実名の原本、掃除した写し、成果物、知識の置き場が複数あり、窓口も複数あるように見えた。
- 原因: 掃除と成果物の引き渡しを room に持たせたため、目視が要る作業まで自動の流れに入れていた。
- 解決: 原本を AI に渡す窓口は、人が `cleankit`（`check` → `clean` → 目視）で掃除して `ai/in/` に置き、`start --adopt` で通す1本にした。成果物は Area へ渡さず、`archives/<Project>/ai/out/` に残す。Area からは `room trace` で Project の決定・経緯を引く。知識は `stock --dst area` で `areas/<Area>/ai/` に運ぶ。

## 基礎知識
流れ（実名は `_noai/` の側だけ。部屋に渡るのは `ai/in/` だけ）:

```
原本（人が _noai/ の下に置く）─ cleankit（人が実行・目視）─▶ ai/in/ ─ start --adopt ─▶ 部屋の AI
                                                                                    │
archives/Project名/ai/out/ ◀─ close（archives へ移動するだけ）─ ai/out/Project名/ ◀─┘
Area の ai/{knowledge,docs}/ ◀─ stock --dst area（点検を通す）─ ai/out/stock/
Area ◀─ room trace（archives の ai/docs を引く）
```

| 場所 | 役割 | 書く人 | 実名 |
|---|---|---|---|
| Area `ai/{knowledge,docs}/` | 知識・決定・経緯。実名なし | `stock --dst area` | なし |
| Project `_noai/` | 人だけの置き場（手で掃除する前の原本、仮置き、全文ログ）。予約名は `mask.toml` だけ。`room` は触らない | 人 | 任意 |
| Project `ai/in/` | 人が掃除・確認した写し。部屋に渡る | 人（`--adopt` で記録） | 掃除後（語は人が確かめる） |
| Project `ai/out/` | 部屋の AI の出力。close 後は archives に残る | 部屋の AI | なし |

- 3つの関係は昇格: 原本 → 成果物 → 知識。知識は成果物の一部が一般化・蒸留されたもので、別系統ではない。
- 実名を含むデータは、同じ親 `_noai/` に寄せる。works の `.gitignore`（`**/_noai/`）と AI の閲覧拒否が親の名前に結びついているので、新しい置き場も親の下に作れば同じ守りが効く。
- 語の置換はしない。掃除は構造（非表示シート、コメント、プロパティなど）を減らし、本文の語は人が `check` の報告で確かめる（`_noai/mask.toml` の語は点検の任意の入力）。
- 掃除に目視が要るので、自動の流れ（`room clean`）にしない。人が置いたものを `start --adopt` で通す関門が、external の Area では止まる（`boundary:`）。
- 成果物は Area へ渡さない。実体は archives に残り、決定記録は `room trace` で拾う。
- 自分で説明するときの一言: 「原本は人が cleankit で掃除して目視し、`ai/in/` に置いて `--adopt` で通す。成果物は archives に残り、Area からは trace で引く」

## チェックリスト
| 症状・疑問 | 原因 | 対処 |
|---|---|---|
| Area の実名のファイルが追跡されている、AI から読める | `_noai` の外に置いた | `_noai/` の下へ移す。追跡に入っていたら履歴に実名が残るので、履歴の扱いは別に判断する（`git ls-files` と `git log` で確認） |
| `start` が「由来の記録が無い」と止まる | `ai/in/` に人が置いたファイルを `--adopt` で通していない | 内容を確認して `start --adopt` |
| `--adopt` が止まる | Area が external（`boundary: internal` でない） | 業務データは AI に入れない。社内向けなら Area の README に `boundary: internal` |
| 共通の資料が部屋の AI に見えない | md を `ai/docs/` に置いていない | md は Area の `ai/docs/` に置く（`start` で `ctx/area/` に写る） |
| 過去の Project の成果物を見たい | Area には渡していない | `archives/<Project>/ai/out/`。決定・経緯は `room trace --area <Area> <語>` |

## 補足
- 知識の書き出しは、運ぶ前に `cleankit` の点検（金額・メール・電話などの形、`mask.toml` の語）を全ファイルに掛け、1つでも当たれば何も運ばず止まる。
- 既存の Project の `_noai/raw/` `_noai/map/` と、Area の `_noai/source/` `_noai/deliverable/` は、消していない。`room` が読まなくなっただけで、人が手で移す。

## 要確認事項
- 人が置いた `ai/in/` → `start --adopt` の流れを、実機で通していない（単体テストのみ）。
- 部屋の AI に、成果物を `ai/out/<Project 名>/` に置かせる案内が、部屋に渡す文書（`ROOM_GUIDE`）に入っていることは確認済み（`room.py`）。実機での読まれ方は未確認。
- [[cross-area-shared-knowledge]] の設計の軸の表（「戻り」「統合」）は、この置き場の分け方より古い。
