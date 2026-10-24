# room open の type 集約（叩き台。段1: 論点の解消・仮決め）

> 状態（2026-10-24）: 実装済み。冒頭の「推奨」は、末尾の「改訂」と「段2」で置き換わった（決定は `docs/decisions.md`）。

2026-10-24。ee の依頼「`dev` `dev-env` `dev-test` `doc` は1つにまとめられる。env をサブディレクトリに足すだけに見える。その後 `research` も含めて一般化」。

## 1. 事実: type は今どこで効いているか（main `06133d0` で確認）

**コード（`room.py`）では、type はラベルだけ。** `--type` の選択肢（`room.py:2127`、既定 `doc`）を README の frontmatter に書き込むだけで（`room.py:488` `584`）、分岐は1つも無い。`room open` が作るディレクトリ（`ai/` 直下の5つと `_noai/`）は全 type で同じ。`ai/out/` の下は作らない方針（`project-structure.md`）。以前あった `data:` と type の組み合わせの警告（`decisions.md` 211 行）は、`data:` の廃止（同 88 行）で消えている。

**違いは、すべて手順書の中にある。** 5か所:

| 何が違うか | 置き場 | `dev` | `dev-env` | `dev-test` | `doc` | `research` |
|---|---|---|---|---|---|---|
| A. `ai/out/<成果物名>/` の中身 | `project-structure.md`、`dev-deliverable-guide.md` | `src/` `tests/` `tools/` `docs/` README | `src/`（セットアップ・コンテナ定義・版の固定）`tools/`（確認）`docs/` README `report.md` | `tests/` `tools/` `docs/` `report.md` | 最終版の文書 | `report.md` |
| B. 基準文書と正の向き | `dev-deliverable-guide.md`、`project-structure.md` | `docs/` の3文書。正はソース | 環境の要求仕様＋運用（機能仕様は省略可） | テスト仕様。**正はテスト対象の要求仕様（`ai/in/`）** | 未決 | 未決 |
| C. 立ち上げで聞くこと | `start-work-types.md`、`dev-deliverable-guide.md` | 開発の表（優先順位、コーディングルール、対象環境、最適化の軸） | 開発の表＋対象環境・環境の置き場・再現方式・版の固定 | 開発の表＋対象と仕様の版・層・合否の基準 | 文書作成の表（ゲートの基準、骨子、図） | `start 調査`（調査1/2、読者と範囲） |
| D. 固有の制約 | `dev-deliverable-guide.md` | — | 実環境は人が作る・確認する | 対象を直さない。不具合は対象の Project に返す | — | AI が集めた資料は `ai/work/` |
| E. `ai/work/` の使い方 | `project-structure.md` | 中間物・使い捨て | 試行ログ・メモ | 試しのテスト・切り分け | 版ごとの下書き | 集めた資料と抜粋 |

**見立ての確認**: 構造（A）だけを見れば、ee の見立てどおり、違いは `ai/out/<成果物名>/` のサブディレクトリの組み合わせだけ。`dev-env` は「`src/` の代わりに環境定義」、`dev-test` は「`src/` が無く `tests/` だけ」、`doc` は「`docs/` だけ」と読める。

ただし B〜D はサブディレクトリだけでは表れない。とはいえ、どれも「どのサブディレクトリがあるか」から導ける:

- B: `src/` があれば3文書、`env/` があれば環境の要求仕様、`src/` が無く `tests/` があれば、正の向きは `ai/in/` の対象。
- C: サブディレクトリごとに聞く項目を持てば、組み合わせで聞く項目が決まる（今の「開発の表＋差分」と同じ形）。
- D: `env/` の「人が実行」、`tests/` だけのときの「対象を直さない」は、サブディレクトリの規則として書ける。

導けないのは `research` だけ（成果物が `report.md` 1つで、違いは成果物でなく、調べ方（`start 調査`）にある）。

## 2. 論点と仮決め案

| # | 論点 | 選択肢 | 仮決め案（推奨） | 理由 |
|---|---|---|---|---|
| 1 | 4つをどうまとめるか | a 1つの type にまとめる／b `dev` 系3つだけまとめ、`doc` は残す／c 現状 | **a** | `doc` も「`docs/` だけの成果物」と読める。分ける根拠はコードに無く、手順書の分岐が増えるだけ |
| 2 | 違いの持ち方 | a 成果物の構成要素（`src/` `env/` `tests/` `tools/` `docs/` `report.md`）で持つ／b 型の中に「副種別」を残す | **a** | ee の見立て（env を足すだけ）そのもの。組み合わせ（例: アプリと環境を両方）も書ける |
| 3 | `dev-env` の置き場 | a `env/` を新設（今の `src/` から移す）／b `src/` のまま | **a** | `src/` があるかで「3文書が要るか」を判定できる。`dev` と同居したときに混ざらない |
| 4 | まとめた type の名前（frontmatter） | a `type` を廃止／b `type: make`（仮）＋`research`／c `type` は残し値は自由記述のヒント | **段階: まず b、`research` を一般化できたら a** | 段階を踏むと、今の手順書（`start 調査` への分岐）を壊さずに済む |
| 5 | 1 Project = 1 成果物との関係 | a 構成要素が複数でも成果物は1つ／b 構成要素ごとに Project | **a**（入れ子なし、受け渡しは `ai/in/`＋`--adopt` のまま） | 2026-10-16 の決定（`dev-env` は独立の Project）は、「別の成果物なら別 Project」の部分だけ残る |
| 6 | `research` の一般化 | a 構成要素 `report.md` として同じ type に入れ、調べ方は `start 調査` が持つ／b `research` を残す | **a（段2）** | 成果物から見れば `report.md` 1つ。違いは「進め方」で、それは `start` のモードの責務 |
| 7 | `remote` の type（期日 11-02） | 構成要素か立ち上げの質問で吸収／type を足す | **吸収**（「環境の置き場」の質問のまま） | 2026-10-16 も「置き場は type を分けない」。集約の方向と同じ |
| 8 | 既存の Project の README | a 古い値はそのまま（`room.py` は読まない）／b 書き換える | **a** | コードが type を読まないので動作は変わらない |

## 3. 変更範囲（段2で事実と突き合わせる予定。今は候補）

- `workflow-kit/room/room.py`（`--type` の選択肢と既定値）、`room/README.md`（使い方の1行）
- `project-structure.md`（種類別の表 → 構成要素の表）
- `dev-deliverable-guide.md`（「`dev-env` と `dev-test`」の節 → `env/` と `tests/` だけのときの規則。題名の `type: dev`）
- `open-hook.md`（手順3「聞く」、未決）、`start-hook.md` `start-work-types.md`（種類の列挙）
- `templates/project/README.template.md`（frontmatter と注記）、`workflow-kit/README.md`（`dev-deliverable-guide.md` の行）、`methods.md`（`research` type の言及2か所）
- `docs/decisions.md`（10-16 の決定を置き換える記録）、`docs/log.md`（`remote` の期日の扱い）

## 4. 決めてほしいこと

1. 論点 1〜3（4つを構成要素で1つにまとめ、`env/` を足す）の方向でよいか。
2. 論点 4 の段階（まず `make`（仮）＋`research`、後で廃止）か、いきなり `type` を廃止か。名前の案があれば。

---

# 改訂（2026-10-24 ee の追加: 2 type 案を取り込む）

ee の考え（別セッションの議論 `2026-10-24-problem-solving-activity-taxonomy.md` による）: problem solving ＝ Project ＝ 部屋。活動は investigation（調べて理解する）と development（作る）に分かれる。今の `dev` を development に割り当て、`research` を investigation に格上げすれば type は2つ。type の違いは作業の構造と特性の違いで、それがサブディレクトリの構造に現れる。

**この改訂は、上の論点 4（段階案）と論点 6 を置き換える。** 論点 1〜3、5、7、8 は変わらない。

## 1. 新しい対応

| 新 type | 旧 type | 作業の特性 | `ai/out/<成果物名>/` の構成 |
|---|---|---|---|
| `development` | `dev` `dev-env` `dev-test` `doc` | 作って保守する成果物。基準文書があり、検証できる | 必要な要素を選ぶ: `src/` `env/` `tests/` `tools/` `docs/`（`doc` は `docs/` だけ） |
| `investigation` | `research` | 調べて結論を出す。結論と出典が成果物。保守しない | `report.md`（結論、出典、確認できなかった点） |

事実との整合（確認済み）: `room.py` は type を読まないので、既存 Project の旧値は動作に影響しない。`--type` の選択肢と既定値（今は `doc`）を `development` / `investigation` に替えるだけ。旧値は受け付けて新値に読み替える（互換）か、受け付けない（`room open` は新規 Project だけ）かは、実装時の選択。

## 2. 手順書側に起こること

- `start 調査` ↔ `investigation`、開発・文書作成の表 ↔ `development`。いまは「type から自動で決まる」記述が弱いので、type が入口の振り分けとして初めて意味を持つ（`start-hook.md` の「作業の種類の差分」）。
- `development` の中の聞く項目は、サブディレクトリで切り替える。`docs/` だけなら文書作成の表（ゲート、骨子、図）、`src/` なら開発の表、`env/` なら環境の置き場の質問、`tests/` だけなら対象と仕様の版。
- 基準文書の正の向きも同じ。`src/` があればソースが正、`env/` なら環境の要求仕様、`src/` が無く `tests/` だけなら `ai/in/` の対象の要求仕様が正。
- `investigation` の基準文書は、問い（章立て）と品質条件（出典・未確認の明記）で、`methods.md` の調査の Must が当たる。`open-hook.md` の未決「`doc` と `research` の基準文書の形」は、`doc` が development に入ることで、`research` だけが残る。

## 3. 分類の線（ここは ee の確認が要る）

添付の分類は、活動（Research / Analysis / Planning / Execution）の概念整理で、排他的な工程分類ではないと明記されている（暫定、ChatGPT 由来）。type は Project の分類なので、**活動ではなく成果物で線を引く**必要がある。仮の基準:

- 成果物が「結論と出典」で、一度出したら保守しない → `investigation`
- 成果物が「作って保守するもの」で、基準文書と検証がある → `development`

この基準で曖昧になる例:
1. 調査して、その結果を設計書にまとめる Project。設計書が成果物なら `development`、結論の報告なら `investigation`。→ 成果物の名前で決める。
2. 調査してから作る流れ。1 Project = 1 成果物の決定（10-16）のとおり、Project を分け、調査の `report.md` を次の `ai/in/` に渡す（`--adopt`）。1 Project の中で type を変えない。
3. `doc` のうち手順書・仕様は development だが、調査1（説明する文書）は investigation。`methods.md` の調査1・2 の置き場（`guides/explain/`）とのつなぎは変えない。

## 4. 変更範囲の差分（上の 3 に追加）

`start-hook.md` の「作業の種類の差分」（type と `start` モードの対応を明記）、`start-work-types.md`（見出しを development の中の要素別にする）、`methods.md` の `research` type の言及2か所（`investigation` へ）、`room-context.md`（type の言及が無いことは確認済み。変更なし）。`remote` の type は、`env/` の置き場の質問で吸収（変わらず）。

## 5. 決めてほしいこと（更新）

1. type を `investigation` / `development` の2つにする方向でよいか（この改訂の推奨は賛成。成果物の線引き 3 の基準つき）。
2. 旧値の扱い: `room open` は新値だけ受け付け、既存 Project の旧値はそのまま（推奨）か、旧値も受け付けて読み替えるか。
3. 線引き 3 の例 1〜3 の扱い（成果物の名前で決める、で足りるか）。

---

# 段2: 決定の反映と変更範囲の確定（2026-10-24）

## ee の決定（10-24）

1. type は2つにする。線は成果物で引く（結論と出典で保守しない → 調査、作って保守する → 開発）。
2. 旧値の扱い: `room open` は新値だけ受け付ける。既存 Project の旧値はそのまま。新値は **`inv` と `dev`**。「env」と書かれたのは打ち間違いと解釈した（`dev` は今の値と同じなので、`dev` の Project は書き換え不要）。違えば直す。
3. 曖昧な例（設計書にまとめる調査、調査してから作る流れ）は、成果物の名前で決める。

## 事実との突き合わせ（main `06133d0` 以降を確認）

| 変更先 | 内容 |
|---|---|
| `workflow-kit/room/room.py:2127` | `--type` の `choices` を `["dev", "inv"]` に。既定値は `doc` → **要決定**（下の確認 A） |
| `workflow-kit/room/README.md:12` | 使い方の1行 |
| `workflow-kit/room/tests/test_room.py` | `type="doc"` が 133・392・402・682・688・1230 行にあり、1243 行は `type=t` を回し、1259・1266 行も type を使う。`doc` → `dev` に直し、1243 行の回す値を確認する（旧値の拒否のテストも足す） |
| `project-structure.md`（7・25〜29・33・38 行） | 種類別の表 → `dev`（構成要素 `src/` `env/` `tests/` `tools/` `docs/` を選ぶ）と `inv`（`report.md`）の2行。基準文書の節は構成要素ごとの正の向きに |
| `dev-deliverable-guide.md` | 題名と冒頭の「`dev` `dev-env` `dev-test` のとき」、末尾の節「`dev-env` と `dev-test`」を、`env/` `tests/` だけのときの規則に書き換え。「`env/` 新設」はここ |
| `open-hook.md`（24・49・52 行） | 聞く項目の type 列挙、未決（`doc` の基準文書は `dev` の `docs/` で決まる。`inv` の分だけ残す）、「type は5種」の実測の項 |
| `start-hook.md`（56・89 行）、`start-work-types.md`（5・9 行） | 種類の列挙。`dev` の中は構成要素で聞く項目を切り替える。`start 調査` ↔ `inv` |
| `templates/project/README.template.md`（4・41・42 行） | frontmatter の値と注記 |
| `workflow-kit/README.md`（74・77 行）、`methods.md`（60 行）、`exmem/lessons/research-method.md`（29・40・90 行） | `research` type → `inv` type の言及 |
| `guides/howto/ai-room-setup-script.md`（116・136・151 行）、`ai-room-mask-summary.md`（31 行）、`guides/explain/ai-room-why.md`（168・324 行） | コマンド例の `--type doc` → `--type dev`。ただし `--data` 付きの例は `room.py` に `--data` が無く、もともと古い（今回は触れず、別件として報告） |
| `docs/decisions.md` | 10-16「`dev-env` と `dev-test` を足した」を置き換える決定。`docs/log.md` の `remote` の期日 11-02 は「`env/` の置き場の質問で吸収。type は足さない」で閉じられる |
| 変更しない | 既存 Project の README の旧値、`room-context.md` |

## 確認 A（実装前に1つだけ）

`--type` の既定値を何にするか。今は `doc`。**`dev` を既定に**（`doc` を含む）するのを推奨。`inv` は調べるときに明示する。省略時に失敗させる案もあるが、誤って `dev` で始めても `inv` へ直せない理由が無いので、省略時は `dev` で足りる。

## 次

review 消化の承認（上の範囲でよいか、確認 A）を待って実装する。実装は1コミット（`[workflow-kit] room の type を dev / inv の2つに集約`）、テストを先に直して通す。
