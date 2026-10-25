---
type: inbox
kind: explain
title: Git の改行コードが PC ごとに変わる仕組み
tags:
  - tool/git
  - line-endings
  - git-config
triggers: [改行コード, CRLF, LF, autocrlf, eol, 改行, PCごとの違い]
created: 2026-01-15
sources:
  - Claude Code conversation "改行コードの統一"
---

# Git の改行コードが PC ごとに変わる仕組み

## 冒頭
同じリポジトリでも PC によって差分が出る理由を、自分で説明できるようにする。前提: Windows と WSL でリポジトリを共有している。確認状況: 一部のみ確認（確認した箇所には日付と根拠を付けた）。
統合先の候補: guides/explain/新規（キーワード: git, 改行, line-endings, autocrlf）

## ダイジェスト
- 状況: 同じコミットなのに、Windows 側で `git status` に差分が出た。
- 原因: `core.autocrlf` が PC ごとの設定で、チェックアウト時と保存時の変換が PC によって違った。
- 解決: リポジトリ内の `.gitattributes` で変換を決めた。

## 基礎知識
- 改行コードは、Windows が CRLF、Linux と macOS が LF。Git は、保存時とチェックアウト時に変換できる。
- 変換の指定は2層ある。PC の設定（`core.autocrlf`）と、リポジトリの `.gitattributes`。後者はリポジトリごとに共有され、前者より優先される（確認: 2026-01-15、根拠: テスト用リポジトリで両方を変えて実行）。
- 自分で説明するときの一言: 「改行の扱いは、PC の設定でなくリポジトリで決めると、誰が clone しても同じ結果になる」

## チェックリスト
| 症状 | 原因 | 対処 |
|---|---|---|
| `git status` に改行だけの差分が出る | 追加前のファイルが再正規化されていない | `git add --renormalize .` を実行し、変換だけのコミットにする |
| 保存のたびに警告が出る | エディタが CRLF で保存する設定（仮説） | エディタの設定を LF にする |

## 補足
| 設定 | 効く範囲 | 備考 |
|---|---|---|
| `core.autocrlf` | PC（ユーザー） | 設定漏れで結果が変わる |
| `.gitattributes` | リポジトリ | 全員に同じ結果 |

## 要確認事項
- 画像などのバイナリ拡張子は、`text=auto` の判定に任せてよいか。
