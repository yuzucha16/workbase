---
type: record
title: 会議録のナレッジ化の裏づけの確認
tags:
  - workflow
  - knowledge-management
created: 2026-10-21
updated: 2026-10-21
---

# 裏づけの確認: 会議録のナレッジ化

6R（[[private-knowledge-6r]]）の「裏づけ（未確認。最初に確かめる）」5件の結果と落とし穴。WBS 1.2。読んだ資料の範囲での確認で、実機（部屋・Obsidian）では動かしていない。works の `areas/` の中身は、works 側の AI は読まない決まりなので、読んでいない。

| # | 確かめること | 結果 |
|---|---|---|
| 1 | works 側（Area）で `inbox` → 統合の流れを使い回せるか | 現状のままでは不可。拡張か並行する手順が要る |
| 2 | 3ラベルで会議録の出力が仕分けられるか | 一部は可。決定は載るが、会議録そのものを入口にする経路が無い |
| 3 | `org:` と Bases で横断の ToDo 一覧が作れるか | 絞り込みは可。ToDo を1件ずつ並べるには、形を選ぶ必要がある |
| 4 | マスク後の `ai/in` に、2層のファイルを渡せるか | 渡せる見込み。ただし結果の置き場と、Area の知識を部屋の AI に見せる経路が論点 |
| 5 | `stock` のモード追加との重なり | 重なりは「型」の部分だけ。置き場と公開範囲が違う |

## 1. works 側での inbox → 統合

- `hooks.md` の権限表で、works の `stock` は `w`（窓口への書き込みだけ）、`integrate` は `－`（行わない）。`stock` が書けるのは workbase の `exmem/inbox/` と `kit-growth/inbox.md` だけで、works の Area の中には書かない（確認: 2026-10-21、根拠: `workflow-kit/hooks.md` の「領域とフックの権限」、`stock-hook.md` の「場所と書き込みの制約」）。
- `integrate` の書き込み先は `exmem/lessons/`、`exmem-index.md`、`tags.md` に固定されている（確認: 2026-10-21、根拠: `integrate-hook.md`）。場所の引数で使い回すには、フックの権限表と書き込み先を変える必要がある。works には「AI が `areas/` の中身を扱わない」決まりがあり（`init-workspace.md` の deny 設定）、Area の中の統合は room の作業になる。
- すでにある Area 側の入口: `room close` が【案件】の行を Area の `ai/docs/inbox.md` に追記する（確認: 2026-10-21、根拠: `room/README.md` の `close`、`room-context.md` の手順）。Area 向けの inbox は、この形で既にある。
- **案（AI の提案。未承認）**: `stock` / `integrate` を works に広げず、会議録は room の Project（`data: mask`）から Area の `ai/docs/inbox.md`（【案件】）に流す既存の経路に載せる。足りないのは、会議録の下書きの型と、Area 側の知識の置き場（`ai/docs/` の下）の決め。

## 2. 3ラベルでの仕分け

- 【案件】は room の Project だけで使い、回収のときに Area の `ai/docs/inbox.md` へ転記する（確認: 2026-10-21、根拠: `docs-rules.md` の項目のラベル、`room-context.md`）。部屋を使わない作業ディレクトリでは【汎用】か【この件】だけ。
- `para-operations`（2026-10-07）は【案件】を「Area の `docs/decisions.md` に直接書く」としたが、後の実装（2026-10-14）は `ai/docs/inbox.md` への転記になっている（確認: 2026-10-21、根拠: `para-operations.md` と `room/README.md`）。**どちらが現行かは未確認**。
- 決定事項は【案件】に載る。アクションアイテムは、Next Actions / Open Questions の残りの振り分け（Area へ渡す / 次の Project / 破棄）と、Area の README の「タスク候補」に当たる（確認: 2026-10-21、根拠: `room-context.md`、`para-operations.md`）。
- 落とし穴: 3ラベルは Project の終了処理で出るものを仕分ける。会議録（Project に属さない打合せ）を入口にする経路は無い。
- 会議録の内容のうち、顧客に依存しないもの（打合せの進め方など）は【汎用】で、`room stock` → `exmem/inbox/` の既存の経路に乗る。

## 3. `org:` と Bases

- vault には Bases の使用例があり、frontmatter の `type` で絞り込んでいる（`exmem/knowledge.base`。確認: 2026-10-21、根拠: そのファイル）。`org:` で絞り込む点は同じ形で書ける。
- Bases の1行は1ファイル（仮説）。本文中の ToDo の箇条書きを1件ずつ並べる一覧は、Bases では作れない。ToDo を一覧にするには、(a) frontmatter に ToDo のリストを持たせる、(b) 会議録1件を1ファイルのまま、冒頭の ToDo の件数や期日を frontmatter に持たせて、会議録の一覧で見る、(c) タスクのプラグインを使う、のどれかになる。実機（Obsidian）での確認は未了。
- 落とし穴: 冒頭の数行（人向け）と frontmatter の ToDo で、同じ内容を二重に持つと、同期がずれる。持つなら frontmatter を正にし、冒頭の数行は、そこから書く。

## 4. マスクと 2 層のファイル

- 既存の手順書がある: `data: mask` は「顧客情報を含む資料（議事録など）を、AI に原本を見せずに要約・アクション抽出させる」型で、マスクした写しだけを AI に渡し、実名には戻さない（読むのは本人だけ）（確認: 2026-10-21、根拠: `guides/howto/ai-room-mask-summary.md`）。会議録の入口は、この型で足りる可能性が高い。
- マスクの対象は csv・md・txt・xlsx・pptx。md と txt は、csv と同じ読み方で文字列を置換する（確認: 2026-10-21、根拠: `room/mask-spec.md`）。frontmatter を特別扱いする記述は見つからなかった。つまり frontmatter の `org:` の値も、`mask.toml` の語に当たれば置換される（仮説。実機で未確認）。
- 辞書にない名前は置換されない（人名が特に漏れる）。マスクの警告（法人格、敬称、メール、電話、URL）を見て語を足す（確認: 2026-10-21、根拠: 同手順書の「よく忘れる点」）。
- 論点: 部屋の AI が Area の知識（過去の決定・ToDo）を見るには、マスクした写しを `ai/in/` に置く必要がある。いまの `room start` が Area から渡すのは、Area の README の写し（`ai/ctx/area-README.md`）だけ（確認: 2026-10-21、根拠: `room/README.md` の `start`）。**Project を跨いで参照する、という要求の核心がここで詰まる**。Area の知識を、毎回マスクして渡す経路が要る。
- `data: mask` は復元しない。実名入りの会議録を Area に残すなら、`data: restore` の `_noai/final/` に出す経路になる（`restore` は AI が見ない場所）。

## 5. `stock` のモード追加との重なり

- あちら（[[stock-modes-plan]]）は、公開してよい知識を `exmem/inbox/` の `kind: lesson | explain` で区別し、`exmem/lessons/` と `guides/explain/` に統合する。こちらは works 側の非公開の知識。窓口も、統合先も、公開範囲も違う。
- 重なるのは、理解ガイド（人向け）の型と、AI 向けの型を別の見出しで持つ、という設計の部分。こちらは1ファイル2層にする決定（`docs/decisions.md`）で、あちらの `kind` 分岐とは別の答えになる。型の用語（冒頭の数行 = 人向け、本文 = AI 向け）が、あちらの6見出しの理解ガイドと食い違わないかは未確認。

## 結論（AI の提案。未承認）

1. 入口は既存の `data: mask` の型（議事録の要約・アクション抽出）に載せる。新しいフックは作らない。
2. 結果の置き場は、Area の `ai/docs/` の下（【案件】の inbox の隣）を候補にする。Area の `decisions.md` との関係は、`para-operations` の未了の書き換えと合わせて決める。
3. Area の知識を部屋の AI に見せる経路（マスクして `ai/in/` に置く）が、いちばん大きな未決。設計が必要。
4. 横断の ToDo 一覧は、frontmatter に件数と期日を持たせ、会議録の一覧を Bases で見る形から始める。
