# inbox メモの見本

`knowledge-hook.md` の形式・項目の型・表記を、1つの完成例で示す。**内容は架空で、事実として扱わない。** 書き方（見出し、項目の型、確認・仮説の表記、統合先の1行）だけを真似る。

見本を直すのは、`knowledge-hook.md` を直したときだけ。出力が揺れた箇所があれば、このファイルに見本を足す（`improvements.md` に記録する）。

````markdown
---
type: inbox
title: Git の改行コードを .gitattributes で統一する
tags:
  - tool/git
  - line-endings
  - setup
created: 2026-01-15
kit: 2026-10-04.2
sources:
  - Claude Code conversation "改行コードの統一"
---

# Git の改行コードを .gitattributes で統一する

## Goal
Windows と WSL でリポジトリを共有するときに、改行コードの差分が出ないようにする方法を決めたかった。
統合先の候補: knowledge/git-config.md（キーワード: git, 改行, line-endings, gitattributes）

## Principles
- 改行コードの扱いは、各PCの設定（`core.autocrlf`）ではなく、リポジトリ内の `.gitattributes` で決める。理由: clone したPCごとに結果が変わらず、差分の原因を探さずに済む。
- 既存のファイルに一括変換をかけるときは、変換だけのコミットに分ける。理由: 差分の中身を読むときに、変換と変更が混ざらない。

## Decisions
- **`.gitattributes` に `* text=auto eol=lf` を書く**（2026-01-15）
  - 根拠: 全PCで作業ツリーも LF にそろい、エディタ設定も LF だけでよくなる。
  - 却下案: PCごとに `core.autocrlf=true`（PCの設定が漏れると差分が出る）。

## Facts
- `.gitattributes` を変更したあと、既存ファイルは `git add --renormalize .` で再正規化できる（確認: 2026-01-15、根拠: テスト用リポジトリで実行）。
- Windows 側のエディタが CRLF で保存する設定のままだと、保存のたびに警告が出る（仮説）。

## Gotchas
- 状況: `.gitattributes` を追加したあとも、`git status` に差分が出続けた
  - 原因: 追加前に作られたファイルが、再正規化されていなかった
  - 解決: `git add --renormalize .` を実行し、変換だけのコミットにした

## Open Questions
- 画像などのバイナリ拡張子は、`text=auto` の判定に任せてよいか。

## Next Actions
- 他のリポジトリにも同じ `.gitattributes` を入れるか判断する。
````
