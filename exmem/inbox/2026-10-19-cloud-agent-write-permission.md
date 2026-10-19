---
type: inbox
title: クラウドの AI セッションの書き込み権限の設計
tags:
  - workflow
  - permissions
  - cloud-session
  - git-push
sources:
  - Claude Code conversation "AI 作業部屋の取り組みの振り返りとナレッジ化"
created: 2026-10-19
---

# クラウドの AI セッションの書き込み権限の設計

## Goal
クラウドの AI セッションに、リポジトリの運用（ブランチを使わず main に直接）と合う書き込み権限を与える方法を残したかった。セッションの既定の制限とリポジトリの規約が食い違うと、作業が止まる。
統合先の候補: lessons/claude-code-permissions.md（キーワード: 権限, push, クラウド, 指定ブランチ）

## Principles
- セッションの既定の制限とリポジトリの規約が食い違うときは、リポジトリ側の恒常許可を Project の指示に明記する。理由: 毎回確認すると作業が止まり、指示に無ければ AI は既定の制限に従う。
- 恒常許可の手順は、許可リストの規則（`docs-rules.md` の push の節）に従って書く。理由: 条件（公開範囲の確認、先頭が祖先か、機密の検索）を毎回満たせる。
- 公開リポジトリへの push では、機密の検索を広げる。理由: 世界に読まれる前提で、メールアドレスや環境固有の値も対象にする。
- 使い捨ての環境では、未 push のコミットは消える。理由: 環境が片付けられると、未 push の作業とメモが失われる。

## Decisions
- **workbase は main に直接コミットして push する（ブランチ運用なし）。Project の指示に、承認済みの変更の恒常許可として書く**（2026-10-17）
  - 根拠: ユーザーが「基本は main に直接」と再確認し、Project の指示に追記した。
  - 却下案: 作業ブランチに push して PR を作る（使われないブランチが増え、PR は頼まれたときだけでよい）。

## Facts
- `git push origin HEAD:main` で main に push できた（確認: 2026-10-18、根拠: 本セッションでの push と `git log`）。
- 指定ブランチにも同じコミットを push しないと、終了時のフックが「未 push のコミットがある」と指摘する（確認: 2026-10-18、根拠: フックの指摘の後に指定ブランチを push して解消した）。
- 使い捨ての環境では、`exmem/inbox/` のメモもコミットして push する（確認: 2026-10-19、根拠: `stock-hook.md` の記述）。
- 指定ブランチの先頭が `origin/main` を含めば、指定ブランチのまま `git push origin HEAD:main` で fast-forward で main に入る。コンテナのローカル `main` は古い履歴のことがあり、checkout しない（確認: 2026-10-18、根拠: 本セッションで `merge-base --is-ancestor` の確認後に push した）。

## Gotchas
- 状況: 承認済みの変更を main に入れようとして、指定ブランチ以外への push を許可していないことで止まりかけた
  - 原因: セッションの指示が「指定ブランチ以外に push しない」で、リポジトリの規約（main に直接）と食い違っていた
  - 解決: Project の指示に恒常許可を書き、`docs-rules.md` の push の節を `HEAD:main` に対応させた

## Open Questions
- 提案: 恒常許可の書き方の雛形（承認範囲、禁止するコマンド）を、`docs-rules.md` に残す（AI の提案。未承認）。

## Next Actions
- 統合のときに、`claude-code-permissions.md` の権限移譲の項目と、重複しないように置く。
