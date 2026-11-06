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
実名を含むデータが Area と Project のどこに置かれ、どの順に流れるか、なぜ分けたかを、自分で説明できるようにする。前提: 実名を AI に見せない作業部屋（`room`）を使い、works は PARA 構成。確認状況: 単体テストで確認。実機の通しは未確認。語のマスク・復元（`mask` `restore`）は 2026-11-06 に廃止した。この文書は廃止後の現行の姿だけを書く（旧い設計は git の履歴と `docs/decisions.md`）。

## ダイジェスト
- 状況: 実名の原本は Area の置き場と Project の `_noai/raw/` の両方に置かれ、`ai/in/` にも似たファイルが写る。置き場が複数あり、窓口が複数あるように見えた。
- 原因: 「入力元」（原本）と「処理の窓口」を同じものとして数えていた。
- 解決: 実名を含むデータは `_noai/` にまとめ、原本を AI に渡す窓口は `clean`（`cleankit` の掃除）の1本にした。成果物の Area への引き渡しは `close` の1本。知識は `stock --dst area` で `areas/<Area>/ai/` に運ぶ。

## 基礎知識
流れ（実名は `_noai/` の側だけ。部屋に渡るのは `ai/in/` だけ）:

```
Area の _noai/source/（共通の xlsx・pptx）─ clean --path ─▶ ai/in/area/ ─┐
Project の _noai/raw/（固有の原本）─ clean ─▶ ai/in/ ──────────────────────┴▶ 部屋の AI
                                                                              │
Area の _noai/deliverable/Project名/ ◀─ close（そのまま渡す）─ ai/out/Project名/ ◀─┘
Area の ai/{knowledge,docs}/ ◀─ stock --dst area（点検を通す）─ ai/out/stock/
```

| 場所 | 役割 | 書く人 | 実名 |
|---|---|---|---|
| Area `_noai/source/` | Project 共通の xlsx・pptx（入力）。変えない | 人 | なし（置かない運用） |
| Area `_noai/deliverable/<Project>/` | 成果物（出力）。Project 名の下に置く | `close` | 部屋の AI が書いたまま |
| Area `ai/{knowledge,docs}/` | 知識・決定・経緯。実名なし | `stock --dst area` | なし |
| Project `_noai/raw/` | Project 固有の原本（入力） | 人（直接置く） | 実名を含みうる |
| Project `_noai/map/` | `room` の記録（成果物の書き出しの記録）。名前は旧マスクの対応表の名残 | `close` | なし |
| Project `_noai/user/` | 人だけの仮置き（予約名） | 人 | 任意 |
| Project `ai/in/` | 掃除した写し。部屋に渡る | `clean` | 掃除後（語は人が確かめる） |
| Project `ai/out/` | 部屋の AI の出力 | 部屋の AI | なし |

- 3つの関係は昇格: 原本 → 成果物 → 知識。知識は成果物の一部が一般化・蒸留されたもので、別系統ではない。
- 実名を含むデータは、同じ親 `_noai/` に寄せる。works の `.gitignore`（`**/_noai/`）と AI の閲覧拒否が親の名前に結びついているので、新しい置き場も親の下に作れば同じ守りが効く。
- 語の置換はしない。`clean` は構造（非表示シート、コメント、プロパティなど）を減らし、本文の語は人が `check` の報告で確かめる（`_noai/mask.toml` の語は点検の任意の入力）。
- 成果物は `close` が `ai/out/<Project 名>/` をそのまま Area へ渡す。人が変えた既存ファイルがあれば、何も変えずに止まる。上書きの経路は無い。
- 名前: `ai/in/` `ai/out/` は部屋の側の語。Area 側は `source` `deliverable` と呼び、混ざらないようにした。
- 自分で説明するときの一言: 「Project 共通の xlsx・pptx は Area の `_noai/source/`、Project 固有の原本は Project の `_noai/raw/` に置く。どちらも `clean` で掃除して `ai/in/` に渡し、結果は `close` が Area に返す」

## チェックリスト
| 症状・疑問 | 原因 | 対処 |
|---|---|---|
| 置き場が複数に見える | 置き場は共通性で分かれている | 共通は Area の `source/`（xlsx・pptx）か `ai/docs/`（md。`ctx/area/` に自動で写る）、固有は Project の `raw/`。実行は `clean` の1本 |
| Area の実名のファイルが追跡されている、AI から読める | `_noai` の外に置いた | `_noai/` の下へ移す。追跡に入っていたら履歴に実名が残るので、履歴の扱いは別に判断する（`git ls-files` と `git log` で確認） |
| `close` が止まり、Area 側が変わっていると出る | Area の既存の成果物を人が編集した | 内容を確認し、人が手で統合する（上書きの経路は無い） |
| `clean --path` が「ファイル名に実名や機密らしい語がある」と止まる | `source/` の名前に検出または `mask.toml` の語が当たった | `source/` は実名を置かない運用。名前を直す |
| 共通の資料が部屋の AI に見えない | md を `source/` に置いた | md は Area の `ai/docs/` に置く（`start` で `ctx/area/` に写る）。`source/` は xlsx・pptx 用 |

## 補足
- `clean --path` は一覧を人が確認する（`--yes` で省略）。`source/` の外を指すパスは拒否する。名前は相対パスのまま `ai/in/area/` に出る。
- 知識の書き出しは、運ぶ前に `cleankit` の点検（金額・メール・電話などの形、`mask.toml` の語）を全ファイルに掛け、1つでも当たれば何も運ばず止まる。

## 要確認事項
- 原本の置き場 → `clean --path` → `close` → 成果物の返却を、実機で通していない（単体テストのみ）。
- 部屋の AI に、成果物を `ai/out/<Project 名>/` に置かせる案内が、部屋に渡す文書（`ROOM_GUIDE`）に入っていることは確認済み（`room.py`）。実機での読まれ方は未確認。
- [[cross-area-shared-knowledge]] の設計の軸の表（「戻り」「統合」）は、この置き場の分け方より古い。
- Project の `raw/` に人が置いた原本を、注意だけでなく拒否にするかは未決。
