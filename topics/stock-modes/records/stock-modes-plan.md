---
type: record
title: stock のモード追加の憲章・WBS・マイルストーン
tags:
  - workflow
  - knowledge-management
created: 2026-10-20
updated: 2026-10-20
---

# 憲章・WBS・マイルストーン: stock のモード追加

元は [[stock-modes-6r]]。作り方のメモは [[stock-modes-plan-notes]]。

## 憲章

| 欄 | 内容 |
|---|---|
| 名前 | stock のモード追加（`stock 理解` / `stock ナレッジ`） |
| 更新日 | 2026-10-20 |
| 使命（What） | `stock` を、AI 用（`exmem/lessons`）と私用（`guides/explain`）の両方に使えるようにする。窓口は `exmem/inbox/` のまま、frontmatter の `kind` で区別し、`integrate` と `check-inbox` が `kind` で分岐する |
| ビジネスの目的（Why） | 知識の整理の入口を1つにし、理解ガイドも同じ品質管理（重複確認・点検）に乗せる |
| 完了時期 | 2026-10-27（バッファは 10-28 以降に別に置く。日付は推測） |
| 予算 | ユーザーの判断 4〜5 回、2〜3 セッション |
| 品質 | `stock ナレッジ` と引数なしの動作が変わらない。理解ガイドの下書きが点検に FAIL なしで通り、`integrate` で `guides/explain/` に入る。`check-hook-outline` が通る |
| 指標 | 既存の理解ガイド1本分の内容を通し試験にかけ、FAIL が 0 |
| 承認が要る変更先 | `workflow-kit/` のすべて（ユーザーの承認なしに書き換えない）。承認後に `guides/AGENTS.md`、`exmem/inbox/README.md` も直す |
| 出力の機微 | なし（公開してよい中身） |

## 成果物 WBS

```
1 stock のモード追加
 1.1 設計
  1.1.1 設計の決定（kind の値、引数なしの1問、integrate の分岐）   置き場: topics/stock-modes/docs/decisions.md
  1.1.2 理解ガイドの下書きの見本（型は reference-doc-types の理解ガイドの型） 置き場: 承認までは topics/stock-modes/records/explain-inbox-example.md。M2 の承認後に workflow-kit/examples/ へ移す
 1.2 手順書の変更（要承認）
  1.2.1 stock-hook.md（モード、引数なしの1問、kind 別の書き方と自己点検） 置き場: workflow-kit/stock-hook.md
  1.2.2 integrate-hook.md（kind 分岐、guides 側の規則） 置き場: workflow-kit/integrate-hook.md
  1.2.3 整合（hooks.md の表、hook-common.md、hook-matrix.md、room-context.md、README、exmem/inbox/README.md、guides/AGENTS.md） 置き場: 各ファイル
 1.3 点検
  1.3.1 check-inbox の kind 分岐（ps1 と py） 置き場: workflow-kit/tools/
 1.4 動作確認
  1.4.1 通し試験（理解ガイド1本 → stock 理解 → 点検 → integrate。引数なしの1問も） 置き場: 結果の数字は topics/stock-modes/records/ に足す。やり方の品質チェックにあたる場合だけ topics/kit-growth/records/ に足す
  1.4.2 check-hook-outline の実行結果（1.4.1 の親にまとめる）
2 プロジェクトマネジメント
 2.1 憲章
 2.2 WBS（変更の記録は下）
 2.3 マイルストーン
 2.4 課題ログ（条件付き）
 2.5 使い心地の記録
```

変更の記録（日付・追加した葉・理由）:

| 日付 | 変更 | 理由 |
|---|---|---|
| 2026-10-20 | 1.3.2 を追加（条件付き） | 6R の前提の表に「`find-knowledge` を `guides/` に拡張するか未決」とあったが、WBS に葉が無かった。理解ガイドの重複確認（`stock` の手順「既存の知識と重なるか確認する」）に関わる |
| 2026-10-20 | 1.3.2 を削除 | ユーザーが「`find-knowledge` の `guides/` 対応は不要」と決めた（`decisions.md`） |
| 2026-10-20 | 1.1.2 の置き場を `records/` に変更 | 設計までは `workflow-kit/` を書き換えない（承認前）。移すのは M2 の承認後 |
| 2026-10-20 | 憲章の完了時期の「バッファ込み」を削除 | マイルストーンの「バッファは 10-28 以降」と矛盾していた |

## マイルストーン（1週間、上限3つ）

| # | 日付 | 内容 | 置く基準 |
|---|---|---|---|
| M1 | 10-21（水） | 1.1 完了。設計の決定をユーザーが確認する | オーナーのレビュー |
| M2 | 10-23（金） | 1.2・1.3 完了。kit の変更をユーザーが承認する | オーナーのレビュー |
| M3 | 10-27（火） | 1.4 完了。通し試験が通る | 成果物の作成完了 |

日付は開始日 10-20 から出した推測。AI だけで進む区間は日付より順序とゲートで見る。バッファは 10-28 以降。
