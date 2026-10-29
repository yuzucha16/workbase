# `logbook/` の最小の型（叩き台、2026-10-26）

`docs/log.md` の Next Actions 1 の叩き台。**実装はしていない**。仕組みの決定なので、`approval-screening.md` に従って待ち行列に置き、次の `review 消化` で 1 点ずつ判断する。前の案は `2026-10-26-logbook-proposal.md` の 3 と `2026-10-26-recommendation-v2.md` の 2。そこから変えた点は、1（名前の衝突）と 3 の frontmatter の追加。

前提（決定済み）: 置き場は workbase 直下の `logbook/`【仮 〜2026-11-29】。入るのは ① 時系列の観測・測定、③ 試行の途中（② は lessons に残して印）。降格は 3 段チェック。`logbook/` から上位の md へ辿れるか、`--triggers` の対象にするかは、別セッション（Next Actions 6）。

## 決める点（7 つ。それぞれ推奨つき）

### 1 ファイル名（新しく分かった問題）

- 問題: 一部だけ移すもの（`ai-work-metrics` の実測値など）を `logbook/ai-work-metrics.md` にすると、`exmem/lessons/ai-work-metrics.md` と名前が重なる。ルートの `AGENTS.md` の「ファイル名は Vault 内で一意」に反し、`[[ai-work-metrics]]` がどちらを指すか決まらない。
- 推奨: ファイルごと移すもの（`user-thinking-habits`）は名前を保つ（2026-10-26 の決定どおり）。一部を移すものは `<lesson の名前>-log.md`（例: `ai-work-metrics-log.md`）。
- 代替: すべて `logbook-<名前>.md` の接頭辞にする（ファイルごと移すものも名前が変わり、既存の `[[user-thinking-habits]]` を張り直す）。

### 2 節

- 推奨: 2 つだけ。`## いま`（要約。これだけ読めば使える。降格元の lesson への `[[リンク]]` を 1 行）と `## 明細`（日付つき、新しい順。開始時に読まない）。前の案のまま。

### 3 frontmatter

- 推奨: `type: logbook`、`title`、`source`（降格元の `[[lesson]]`。新規なら無し）、`created`、`updated`、`review_by`、`budget`。`tags` `aliases` `triggers` は付けない（`triggers` は Next Actions 6 で決める）。
- 前の案から足したもの: `type` と `source`。`type` は点検の道具が logbook のファイルを見分けるため、`source` は降格の行き先を逆に辿るため。

### 4 既定の値

- 推奨: `review_by` は作った日・判断した日から 60 日（暫定）。`budget` は 8KB（暫定）。どちらも根拠の無い目安なので、11-29 の月次の試行の後に実測で直す。

### 5 スクリーニングの道具

- 推奨: `find_knowledge.py` に `--check-aging` を足す。`logbook/` の各ファイルについて、`review_by` を過ぎたもの、`budget` を超えたもの、frontmatter が欠けたものを 1 行ずつ出し、件数を返す。呼ぶのは `review` の入力 3（警告の目安）に 1 行。判断は月次の振り返りで行う。
- 代替: 道具を作らず、月次で `logbook/` を手で見る（ファイルが 5 個くらいまでは足りる）。

### 6 窓口

- 推奨: `logbook/README.md` に、入る 3 型の定義（① ③ と、② は入らない理由）、型（上の 1〜4）、畳み方（捨てる・圧縮・昇格・降格）、公開リポジトリであることの注意を書く。ルートの `README.md` の構成の表に 1 行足す。`exmem/AGENTS.md` に「lessons の ① ③ の節は logbook へ降格できる（3 段チェック）」の 1 行を足す。

### 7 降格の書き方

- 推奨: lesson の側は、移した節の位置に結論 1 行と `→ [[<名前>-log]]` を残す。logbook の側は、`## いま` の先頭に `元: [[lesson]]`。明細は原文のまま移し、圧縮は降格とは別の判断にする（降格と圧縮を 1 つの承認にまとめない）。

## 入れるときに直すもの（実装の範囲）

- 新規: `logbook/README.md`、`find_knowledge.py --check-aging`（5 を採るなら）とその単体の確認。
- 1 行の追記: ルートの `README.md`、`exmem/AGENTS.md`、`workflow-kit/review-hook.md` の入力 3。
- 直さないもの: `topics/AGENTS.md` の「`records/` は 2 か所だけ」と、`kit-records-index.md` の「古い記録は消さない」。どちらも `topics/` の中の規則で、`logbook/` は外にあるので当たらない。11-29 の試行は置き場を変えないので、これも当たらない。

## 入れた後の順番

1. `logbook/` と README、道具を作る（上の範囲）。
2. 移す 6 件（`docs/log.md` の Next Actions 5）を、1 件ずつ移す。`user-thinking-habits` は、移す前に公開範囲をユーザーが確かめる。`user-manual` の Facts は、Principles との対応表を先に出す。
3. 別セッションで、上位の md から辿れるかを確かめる（Next Actions 6）。
