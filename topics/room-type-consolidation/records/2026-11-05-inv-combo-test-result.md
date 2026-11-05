# inv の工程の組み合わせ試験: 結果（2026-11-05）

設計は `2026-11-05-inv-combo-test-design.md`。方法は `dev` の追試（11-04）と同じ。部屋 `room-myenv`（internal。Web は使えた）で、Project `sample_invA` `sample_invB` `sample_invC`（`--type inv`）を `room start --cmd` で、`claude -p` を AI が起動して通した。cwd は `/mnt/room/<名>`。規則（`ROOM.md` と `project-structure.md`）だけで、依頼に置き場も構成も書かない。

起動の注意: `claude -p` は書き込みの許可で止まる（初回の A は何も作れず）。`--permission-mode acceptEdits --allowedTools 'Bash WebFetch WebSearch Read Write Edit Glob Grep'` を付け、プロンプトは引数でなく stdin（`< prompt.txt`）で渡す（`--allowedTools` が可変長引数でプロンプトを吸う）。

## 結果

| | 依頼の重さ | 作ったもの | 作らなかったもの | 聞き返し |
|---|---|---|---|---|
| A | 軽く。口頭で足りる | `report.md` のみ | `question.md` `sources/` `findings/` `checks/` `publish/` | 0 |
| B | 根拠つきで、後で見返せるように | `report.md` `sources/sources.md` `findings/findings.md` | `question.md` `checks/` `publish/` | 0 |
| C | 報告資料にして。確認できない点も明記 | `report.md` `sources/` `findings/` `checks/checks.md` | `question.md` `publish/` | 0 |

- 置き場: 3 件とも `ai/out/<Project 名と同じ>/`（規則どおり。`ai/` 直下への誤配置なし）。
- 組み合わせ: 重さに合って段階的に増えた（A 1 本 → B 3 本 → C 4 本）。過剰作成なし。A の理由づけ（「1 問・事実 1 つ」「清書の依頼なし」）も合う。
- 出力の質: A は実測（部屋の Python 3.13）と公式文書の 2 本立てで、未確認を明記。C は Slidev が部屋に無く未実測と明記し、結論に「推測を含む」と付けた。
- `question.md` は 3 件とも作らず、問い・仮定・完了条件を `report.md` の冒頭に書いた（仮決め「問い＋完了条件の 1 行」と一致）。

## 指摘（直す候補）

1. `publish/` が C で作られなかったのは、依頼文の誤り。「報告資料にして」を pptx と読まず md の報告にした（`publish/` は「頼まれたときだけ」の規則どおり）。pptx と明示したときの動きは未測。
2. 部屋の cwd が `ai/` そのもので、`ai/` が無い。3 件とも「`ai/out/` を `out/` と読み替えた」と迷いに書いた（C は `ai/` を作りかけて直した）。`dev` の追試でも出た既知の件（`room-context.md` に読み替えの記述あり）。ただ `project-structure.md` の `inv` の節は `ai/` 前提のままで、迷いが出る。
3. B は `checks/` を作らず、未確認を `report.md` に入れた（4 項目だけのため）。`checks/` は 1 ファイルとあるので、軽い依頼では `report.md` に含めてよい、と一言あってよい。
4. 費用は未集計。
