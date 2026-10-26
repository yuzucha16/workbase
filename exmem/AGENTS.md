# AGENTS.md

exmem（external memory、外部メモリ）は、AIと人間が共有するナレッジ置き場。AIとの壁打ちや作業から得た知識を、AI・端末をまたいで引き継ぐ。Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。人間はObsidianで閲覧・編集する。

場所は `$HOME\works\resources\exmem`（共有リポジトリ `workbase` の一部）。起動する単位はリポジトリのトップ（`resources/`）で、exmem での作業は「exmem の続き」で扱う（`workflow-kit/docs-rules.md` の「上の階層で起動して…」。2026-10-16 の決定）。

## 共有の範囲

- `workbase` の内容は、すべて共有（Git管理）する。公開されうる前提で書く。機密、勤務先固有の情報、PC ごとのデータを入れない。ローカルのデータ（勤務先・個人の作業）は、`workbase` の外に置く。
- 共有側のノートから、ローカル側（`areas/` など）へ `[[リンク]]` を張らない。他のPCでリンク切れになる。
- **exmem に業務の文脈（勤務先固有・案件固有の内容、勤務先環境の制約や設定）を書かない**（2026-10-08 ユーザーの決定。公開の予定はあるが未決定。2026-10-10 に `contexts/` を廃止したので、対象を exmem 全体の表現にした）。業務の引継ぎが必要なときは、作業側の `docs/`（非公開の remote か、ローカルの git）に書く。書いてしまったら、公開前に削除する。

## 読む順番

0. 作業の前に、依頼の言葉で `python -I workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"` を実行し、出たノートを読む（各ノートの `triggers:` と部分一致で照合する。`lessons/`、`guides/explain/`、未統合の `inbox/` が対象）。
1. `exmem-index.md`（知識の索引）で、該当する知識を探し、その `lessons/*.md` を読む（全件は読まない）。大きいノート（目安 10KB 超）は、見出しの一覧か `find-knowledge.ps1` が示す行の範囲を見て、必要な節だけを読む。
2. 作業の途中の状態は、その `lessons/` のノートの `Open Questions` と `Next Actions`。
3. タグの一覧は `tags.md`。

## ディレクトリの役割

- `inbox/`: 未整理の会話メモの一時置き場。知識へ統合したら削除する（`inbox/README.md` は除く）。
- `lessons/`: AI が今後の参考にする、判断・原則・落とし穴の記録。1ファイル1トピック。旧名は `knowledge/`（2026-10-10 に改名。履歴の中の旧名は読み替える。frontmatter の `type: knowledge` は、ノートの種類名としてそのまま）。
- `lessons/` の節のうち、時系列の観測・測定と試行の途中は、`../logbook/` へ降格できる（承認の 3 段チェックで決める。版・時点依存の節は降格せず印を付ける。型は `logbook/README.md`。2026-10-26）。
- 人が手順や仕組みを思い出すための文書は、exmem でなく `../guides/` に置く（`reference-doc-types.md`）。

## Frontmatter

```yaml
---
type: knowledge          # knowledge / index / inbox
title: Zed Vim環境
status: active           # active / superseded
tags:
  - tool/zed
  - keymap
aliases:
  - ZedへのVim環境移行
created: 2026-09-26
updated: 2026-09-26
sources:
  - ChatGPT conversation "ZedへのVim環境移行" (2026-09-26)
---
```

- `type` / `title` / `status` / `tags` / `created` / `updated` は必須。
- `triggers: [語, 語]`（`lessons/` の必須項目。2026-10-25）: 後で同じ作業をするとき、依頼文に出そうな言葉（コマンド名、拡張子、症状、作業名）を、同義語・言い換えを含めて15語まで、1行で書く。上の「読む順番」0 の検索が使う。`integrate` が統合のときに合わせ、`find_knowledge.py --check-triggers` が点検する。
- `aliases` には日本語名や別名を入れる。Obsidianのリンク補完・検索で使われる。
- 日付は `YYYY-MM-DD`。知識ファイルを変更したら `updated` を今日の日付にする。

## タグ

タグは「何についての知識か」を表す横断的な分類。ルールと語彙は `tags.md` にある。

- frontmatter の `tags` にリストで書く。`#` は付けない。本文中にタグを書かない。
- 英小文字の kebab-case。スペース不可。
- `tags.md` の語彙から選ぶ。新しいタグが必要なら `tags.md` に追記してから使う。
- `type` や `status` の値（`knowledge`、`inbox` など）をタグにしない。プロパティと重複するため。
- 特定のノートとの関係はタグではなく `[[リンク]]` で表す。

## 本文の書き方

- Markdown + 通常の見出しで書く。AI固有の形式は使わない。
- 確認済みの事実と仮説を区別する。バージョンなど変わりやすい値には「YYYY-MM-DD 時点」を付ける。
- 古くなった記述は削除せず、`status: superseded` にして新しいファイルへリンクする。

知識ファイルは、該当する内容があれば次の見出しを使う。

| 見出し | 書くこと |
|---|---|
| `## Principles` | 判断の拠り所になる方針・原則。「〜しない」「〜を優先する」など |
| `## Decisions` | 個別の決定。決めたこと、根拠、却下案、日付をそろえる |
| `## Gotchas` | 実際に遭遇したエラーや詰まった点。状況、原因（わかれば）、解決の順 |

注意点や方針のうち、実際に遭遇したエラーでないものは `Gotchas` ではなく `Principles` に書く。

## リンク

- ノート間のリンクは `[[ファイル名]]` で書く（例: `[[zed-vim]]`）。
- 知識ファイルには、関係する知識・プロジェクトへのリンクを `## Related` にまとめる。

## 統合と書き込み

- 新しい知識ファイルを作ったら、`exmem-index.md` に1行足す。
- `inbox/` の統合は、ユーザーが「inboxを整理して」と言ったときに、kit の `integrate-hook.md`（統合の手順の正本）に従う。
- 作業ディレクトリは exmem を基本は読み取り専用で参照する。書き込みの例外は、ユーザーが「ナレッジ化して」（人用の理解ガイドは「理解ガイドにして」。frontmatter の `kind: explain`）と指示したときの `inbox/` への新規メモ1つだけ（正本は kit の `stock-hook.md`。`inbox/README.md` のプロンプトはその写し）。
- exmem に、作業ディレクトリの作業ログを置かない（経緯・決定・次にやることは、各ディレクトリの `docs/` が持つ）。`contexts/`（作業の引継ぎ用）は 2026-10-10 に廃止した（[[ai-development-workflow]] D10）。未完の項目は、該当する `lessons/` のノートの `Open Questions` / `Next Actions` に書く。
