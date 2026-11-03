---
type: explain
title: AI 作業部屋のデータの置き場と流れ（原本・成果物・知識）
tags:
  - ai-room
  - security
  - harness
  - para
  - knowledge-management
triggers: [原本, 成果物, データの置き場, _noai, ai/out, マスク, 復元, 部屋のデータ, 知識の流れ]
---

# AI 作業部屋のデータの置き場と流れ（原本・成果物・知識）

## 冒頭
実名を含むデータが Area と Project のどこに置かれ、どの順に流れるか、なぜ3つに分けたかを、自分で説明できるようにする。前提: 実名を AI に見せない作業部屋（`room`）を使い、works は PARA 構成。確認状況: 単体テスト（115件）で確認。実機の通しは未確認。

## ダイジェスト
- 状況: 実名の原本は Area の置き場と Project の `_noai/raw/` の両方に置かれ、マスク済みの `ai/in/` にも似たファイルが写る。置き場が複数あり、窓口が複数あるように見えた。
- 原因: 「入力元」（原本、知識）と「処理の窓口」を同じものとして数えていた。さらに、Area の知識置き場が `_noai` の外にあり、追跡の除外と AI の閲覧拒否が効いていなかった。
- 解決: 実名を含む Area のデータを `areas/<Area>/_noai/` にまとめた。窓口を1本に絞った（当時は `pull`。2026-11-03 に `pull` を廃止し、`clean` に替えた。下の「2026-11-03 の改訂」）。

## 2026-11-03 の改訂
- 置き場は共通性で分ける（ユーザーの決定）。Project 共通で md にできるもの（憲章など）は Area の `ai/docs/`（実名を書かない）に置く。Project 共通の xlsx・pptx は Area の `_noai/source/`（実名・機密なし、internal のみ）。Project 固有の原本は Project の `_noai/raw/` に人が直接置く。
- 窓口は `clean` の1本。`pull` は廃止した。下の本文に、改訂前の記述（`pull`、knowledge 経路）が残る箇所がある場合は、この節を正とする。

## 基礎知識
流れ（実名は左側だけ。部屋に渡るのは `ai/in/` だけ）:

```
Area の _noai/source/（共通の xlsx・pptx）─ clean --path ─▶ ai/in/area/ ─┐
Project の _noai/raw/（固有の原本）─ clean / mask ─▶ ai/in/ ───────────────┴▶ 部屋の AI
                                                                              │
Area の _noai/knowledge/    ◀─┐                                    ai/out/ ◀──┘
Area の _noai/deliverable/Project名/ ◀─ restore（実名に戻す）← 対応表 _noai/map/
                                         └→ Project の _noai/final/（写しも残る）
```

| 場所 | 役割 | 書く人 | 実名 |
|---|---|---|---|
| Area `_noai/source/` | 原本（入力）。変えない | 人 | あり |
| Area `_noai/deliverable/<Project>/` | 成果物（出力）。Project 名の下に置く | `restore` | あり |
| Area `_noai/knowledge/` | 知識。成果物の一般化、または工程で蒸留したもの | `restore`（部屋の AI が統合した結果） | あり |
| Project `_noai/raw/` | Project 固有の原本（入力） | 人（直接置く） | 実名を含みうる |
| Project `_noai/map/` | 対応表（実名とプレースホルダー）。部屋に渡らない | `mask` | あり |
| Project `ai/in/` | マスク済みの写し。部屋に渡る | `mask` | なし |
| Project `ai/out/` | 部屋の AI の出力（プレースホルダー入り） | 部屋の AI | なし |
| Project `_noai/final/` | 復元後の成果物 | `restore` | あり |

- 3つの関係は昇格: 原本 → 成果物 → 知識。知識は成果物の一部が一般化・蒸留されたもので、別系統ではない。
- 実名を含むデータは、同じ親 `_noai/` に寄せる。works の `.gitignore`（`**/_noai/`）と AI の閲覧拒否が親の名前に結びついているので、新しい置き場も親の下に作れば同じ守りが効く。
- マスクと復元は、設定でなく状態で決まる。`_noai/raw/` に原本があればマスクし、`_noai/map/mapping.json` があれば（マスクしたことがあれば）復元する。Project ごとの「データの型」の設定は無い。
- 名前: `ai/in/` `ai/out/` は部屋の側（実名なし）の語。Area 側（実名あり）は `source` `deliverable` と呼び、混ざらないようにした。
- 自分で説明するときの一言: 「Project 共通の xlsx・pptx は Area の `_noai/source/`、Project 固有の原本は Project の `_noai/raw/` に置く。どちらも `clean` で掃除して `ai/in/` に渡し、結果は `restore` が実名に戻して Area に返す」

## チェックリスト
| 症状・疑問 | 原因 | 対処 |
|---|---|---|
| 置き場が複数に見える | 置き場は共通性で分かれている | 共通は Area の `source/`（xlsx・pptx）か `ai/docs/`（md。`ctx/area/` に自動で写る）、固有は Project の `raw/`。実行は `clean` の1本 |
| Area の実名のファイルが追跡されている、AI から読める | `_noai` の外に置いた | `_noai/` の下へ移す。追跡に入っていたら履歴に実名が残るので、履歴の扱いは別に判断する（`git ls-files` と `git log` で確認） |
| `init` が「旧 `knowledge/` がある」と警告する | 旧い置き場が残っている | 人が `_noai/knowledge/` へ移す（自動では動かさない） |
| `restore` が止まり「前回の書き出しから変わっている」と出る | Area の既存ファイルを人が編集した | 内容を確認し、上書きしてよければ `--force`。直前の版は `_noai/final/_prev/` に退避される |
| マスクしていない Project で `restore` が「復元できない形式」で止まる | `ai/out/` にコードなどがあるのに復元が走った | 復元は対応表（`mapping.json`）があるときだけ走る。無いのに止まるなら対応表の有無を確認する |
| `clean --path` が「ファイル名に実名や機密らしい語がある」と止まる | `source/` の名前に検出または `mask.toml` の語が当たった | `source/` は実名を置かない運用。名前を直す |
| 共通の資料が部屋の AI に見えない | md を `source/` に置いた | md は Area の `ai/docs/` に置く（`start` で `ctx/area/` に写る）。`source/` は xlsx・pptx 用 |

## 補足
| 項目 | 以前 | 今 |
|---|---|---|
| マスク・復元の切替 | 設定で選ぶ | 状態（原本の有無、対応表の有無）。設定なし |
| 知識置き場 | `areas/<Area>/knowledge/`（`_noai` の外） | `areas/<Area>/_noai/knowledge/` |
| 原本の入口 | Project の `_noai/raw/` に直接置く、または `pull`（Area の `source/` → `raw/`） | 固有は `raw/` に直接置く。共通の xlsx・pptx は `source/` に置き `clean <Project> --path <パス or glob>`（`pull` は廃止） |
| 成果物の戻り先 | Project の `_noai/final/` だけ | `final/` に加えて、Area の `deliverable/<Project>/` |

- `clean --path` は一覧を人が確認する（`--yes` で省略）。`source/` の外を指すパスは拒否する。名前は相対パスのまま `ai/in/area/` に出る。
- 書き出しの規則は知識と成果物で共通: プレースホルダーが残る名前と置き場の外を指す名前は止める。人が変えた既存ファイルがあれば止める（`--force` で上書き）。

## 要確認事項
- 原本の置き場 → `clean --path` → `restore` → 成果物の返却を、実機で通していない（単体テストのみ）。
- 部屋の AI に、成果物を `ai/out/deliverable/` に置かせる案内が、部屋に渡す文書に入っているか未確認。
- [[cross-area-shared-knowledge]] の設計の軸の表（「戻り」「統合」）は、この置き場の分け方より古い。
- Project の `raw/` に人が置いた原本を、注意だけでなく拒否にするかは未決。
