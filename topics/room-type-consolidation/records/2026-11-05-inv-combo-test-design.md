# inv の工程の組み合わせ試験: 設計と依頼文（2026-11-05）

`dev` の a) `src` のみ、b) `env`+`src`、c) 全部、と同じ形を `inv` で行う。eg1（Web）と eg2（CSV）は「全工程で構造が使えるか」を見た。ここでは「軽い依頼で、AI が必要な分だけ作るか」を見る。決定は `docs/decisions.md`、状態は `docs/log.md`。

## 方針

- 部屋は external（Web。マスク不要）。Project は 3 つ（`sample_invA` `sample_invB` `sample_invC`）。type は `inv`。
- 依頼文では構成要素の名前を言わない。**重さの言葉**（軽く／根拠つきで／資料にして）だけで頼み、AI が `project-structure.md` の `inv` の節（部屋では `~/shared/workflow-kit/`）を見て組み合わせを選ぶかを見る。
- 題材は、答えが 1 次情報で確かめやすい小さな問いにする（結果の正否ではなく、構造を見るため）。

## ケース

| ケース | 期待する組み合わせ | 依頼の重さ | 題材（案） |
|---|---|---|---|
| A 少 | `report.md` だけ | 「軽く。口頭で足りる」 | Python 3.13 で `pathlib.Path.walk` が使えるか、いつ入ったか |
| B 中 | `question.md` + `findings/` + `report.md`（`checks/` は短く、`publish/` なし） | 「根拠つきで、後で見返せるように」 | uv と pip-tools の違い（個人の開発用途、3 点） |
| C 全部 | 全部（`publish/` に pptx） | 「報告資料にして、確認できない点も明記」 | Marp・Slidev・Quarto の選び方（既存の比較結果は見せない） |

## 見る点（判定 3 点）

1. 置き場: 成果物を `ai/out/<成果物名>/` の下に置いたか。`ai/work/` や `ai/docs/` との混同。
2. 組み合わせ: 重さに合う分だけ作ったか（A で `question.md` `sources/` を作る＝過剰。C で `checks/` が無い＝不足）。
3. 聞き返し: 用途・範囲を聞いたか。聞いたなら、重さの言葉で足りなかったか。

あわせて、`dev` との差（`inv` は最小が `report.md` 1 本でよいと読めたか）、`ai/docs/inv-log.md` の迷った点を見る。

## 人の手順（ケースごと）

1. `uv run room.py open sample_invX --area <external の Area>`、type は `inv`、`start`。
2. 部屋の AI に、下の依頼文を渡す（A→B→C の順。1 つ終わるごとに `close` まで行う）。
3. 終わったら、`ai/out/` の木（`find ai/out -type f`）と `ai/docs/inv-log.md` を、別のセッションで見せる。

## 依頼文（共通の枠。{ } を差し替える）

````
これは inv(調査)の構造の実験です。調査の中身より、成果物をどう組み立てるかを見ます。
【お題】{題材}
【重さ】{重さの言葉}
【進め方】ROOM.md を読んでから始めてください。成果物名は sample_invX(Project 名と同じ)。構成の正本は ~/shared/workflow-kit/project-structure.md の inv の節です。必要なものだけ作ってください。
【記録】終わったら、ai/docs/ の inv-log.md に、作ったものと作らなかったものの理由、迷った点を 5 行以内で書いてください。
【確認なしで進めてよい範囲】切り口と細部。聞き返すのは、読者や範囲が変わるときだけ。
````
