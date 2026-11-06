---
type: logbook
title: inv の工程の組み合わせ試験（重さの言葉で必要な分だけ作るか）
created: 2026-11-06
updated: 2026-11-06
review_by: 2027-01-05
budget: 8KB
---

# inv の工程の組み合わせ試験（2026-11-05）

反映先: `workflow-kit/project-structure.md` の `inv` の補足、`guides/quickref/ai-work-prompts.md`（重さの言葉）、`exmem/lessons/ai-isolated-work-room.md`（`claude -p` の起動の注意）。再実行の型は [[room-split-test-procedure]] の起動の節と同じ。

## いま

- 構成要素の名前を依頼に書かず、**重さの言葉**（軽く／根拠つきで／資料にして）だけで頼むと、AI は `project-structure.md` の `inv` の節を見て、重さに合った分だけ作った。聞き返しは 3 件とも 0。
- 置き場は 3 件とも `ai/out/<Project 名と同じ>/`。`question.md` は作らず、問い・仮定・完了条件を `report.md` の冒頭に書いた（基準文書は「問い＋完了条件の 1 行」の仮決めと一致）。
- 指摘 3 点は採用して `project-structure.md` に反映済み: ①清書は「pptx で」と明示する、②部屋の cwd は `ai/` そのもの（`ai/out/` を `out/` と読み替える）、③未確認が数項目なら `checks/` を作らず `report.md` に書いてよい。

## 明細（2026-11-05）

### 設計

部屋は external（Web 可）。Project は `sample_invA` `sample_invB` `sample_invC`（`--type inv`）。題材は答えが一次情報で確かめやすい小さな問い。見た点: ①置き場（`ai/work/` `ai/docs/` との混同）、②組み合わせ（A で `question.md` `sources/` は過剰、C で `checks/` が無いのは不足）、③聞き返し。

| | 期待 | 依頼の重さ | 題材 |
|---|---|---|---|
| A 少 | `report.md` だけ | 軽く。口頭で足りる | Python 3.13 で `pathlib.Path.walk` が使えるか、いつ入ったか |
| B 中 | `question.md` + `findings/` + `report.md` | 根拠つきで、後で見返せるように | uv と pip-tools の違い（個人の開発用途、3 点） |
| C 全部 | 全部（`publish/` に pptx） | 報告資料にして、確認できない点も明記 | Marp・Slidev・Quarto の選び方 |

依頼文の枠: 「これは inv(調査)の構造の実験です。…【お題】{題材}【重さ】{重さの言葉}【進め方】ROOM.md を読んでから始めてください。成果物名は Project 名と同じ。構成の正本は `~/shared/workflow-kit/project-structure.md` の inv の節。必要なものだけ作ってください。【記録】終わったら `ai/docs/inv-log.md` に、作ったものと作らなかったものの理由、迷った点を 5 行以内で。【確認なしで進めてよい範囲】切り口と細部。聞き返すのは、読者や範囲が変わるときだけ。」

### 結果

起動の注意: `claude -p` は書き込みの許可で止まる（初回の A は何も作れず）。`--permission-mode acceptEdits --allowedTools 'Bash WebFetch WebSearch Read Write Edit Glob Grep'` を付け、プロンプトは引数でなく stdin（`< prompt.txt`）で渡す（`--allowedTools` が可変長引数でプロンプトを吸う）。

| | 作ったもの | 作らなかったもの | 聞き返し |
|---|---|---|---|
| A | `report.md` のみ | `question.md` `sources/` `findings/` `checks/` `publish/` | 0 |
| B | `report.md` `sources/sources.md` `findings/findings.md` | `question.md` `checks/` `publish/` | 0 |
| C | `report.md` `sources/` `findings/` `checks/checks.md` | `question.md` `publish/` | 0 |

- 組み合わせは段階的に増えた（A 1 本 → B 3 本 → C 4 本）。過剰作成なし。
- A は実測（部屋の Python 3.13）と公式文書の 2 本立てで未確認を明記。C は Slidev が部屋に無く未実測と明記し、結論に「推測を含む」と付けた。

### 指摘

1. `publish/` が C で作られなかったのは依頼文の誤り。「報告資料にして」を pptx と読まず md の報告にした（規則どおり）。→ 明示した追試は [[room-inv-publish-explicit-log]]。
2. 部屋の cwd が `ai/` そのもので `ai/` が無く、3 件とも `ai/out/` を `out/` と読み替えた（C は `ai/` を作りかけて直した）。
3. B は `checks/` を作らず、未確認 4 項目を `report.md` に入れた。
4. 費用は未集計。
