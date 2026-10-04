---
type: knowledge
title: アプリの設定ディレクトリを置くリポジトリの判断基準
status: active
tags:
  - dotfiles
  - tool/obsidian
  - workflow
aliases:
  - 設定の置き場の判断基準
  - .obsidianの置き場
  - 設定ディレクトリの置き場
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation ".obsidian の置き場の判断基準" (2026-10-04)
  - "notes の .obsidian/、dotfiles の manifests/links.map（2026-10-04 に確認）"
---

# アプリの設定ディレクトリを置くリポジトリの判断基準

## Purpose

アプリの設定ディレクトリを、データのリポジトリ（例: Vault の `notes`）に置くか、設定ファイル用のリポジトリ（dotfiles）に置くかを決める基準。最初の適用例は Obsidian の `.obsidian/`。Zed や Notepad++ など他のアプリの設定にも使える形にする。

## Principles

- **設定の置き場は、その設定が何と連動して変わるかで決める。** 連動先が Vault の中身（ノート規約、プロパティ型、検索除外）なら Vault 側、環境全体（テーマ・フォントを複数アプリでそろえるなど）なら dotfiles 側。連動するものと同じリポジトリにあれば、変更が1つのコミットで済む。
- **アプリが固定の場所を読む設定は、実体をその場所に置く。** リンクで別のリポジトリに逃がさない。リンクは、clone 順、リンク前の起動による衝突、コミット先の分離といった運用の負担を足す。
- **設定ファイルの管理を2つのリポジトリで相互に参照させない。** セットアップの順序が循環し、片方だけの環境で動かなくなる。
- **`AGENTS.md` と `docs/` は、リポジトリのルートか、独立して判断を積む単位にだけ置く。** 小さなサブディレクトリごとには置かない。AI が読む前提資料が作業単位ごとに増え、管理コストだけが膨らむ（[[workflow-kit]]）。
- **AI に置き場の影響を説明させるときは、作業場（Claude を開くディレクトリ）がどこになるかを前提に整理させる。** 置き場を変えると作業場も変わるので、粒度への影響は作業場を基準にしないと誤る（Gotchas）。

## 判断基準の6項目

① アプリが読む場所の制約、② 設定の連動先、③ リポジトリ間の依存の向き、④ 全環境への到達性、⑤ 履歴の軽さ、⑥ `AGENTS.md` と `docs/` を置く粒度。⑥は、どちらのリポジトリでもルートで作業すれば差が出ない（ユーザーの指摘）。④は、全PCに dotfiles も clone するので、今は決め手にならない（ユーザーの発言）。

## Decisions

### `.obsidian` は `notes` に置き続け、dotfiles には戻さない（2026-10-04）

- 根拠: Obsidian は Vault 直下の `.obsidian` を読む（dotfiles に置くとジャンクションが必須）。設定の中身は Vault と連動する。dotfiles → `notes` の片方向の依存を保てる。プラグインで dotfiles の履歴が重くなるのを避けられる。Zed とテーマ・フォントをそろえる意図は無い（ユーザーの発言）。
- 却下案: dotfiles に戻して `notes/.obsidian` へリンクする（上の負担が増え、得られるのは Zed との統一だけで、その意図が無い）。

### Obsidian の設定を変える作業は、`notes` のルートで Claude を開いて行う（2026-10-04）

- 根拠: `.obsidian/` 専用の `AGENTS.md` と `docs/` を作らずに済む。
- 却下案: `.obsidian/` 単体を作業単位にする（専用の `AGENTS.md` と `docs/` が要る。`.obsidian/docs/log.md` は `git log -- .obsidian` の再掲で、履歴から復元して作れた。その後、`notes/docs/` に置く形に変わった）。

## Facts

`.obsidian` を dotfiles に置いて `notes/.obsidian` へリンクした場合の、確認できている影響（既存のリンクスクリプトの仕様と `links.map` から。2026-10-04）:

- `notes` と dotfiles の clone 順が循環する（dotfiles の `links.map` が `..\notes` を参照するため）。
- リンクの前に Obsidian が実ディレクトリの `.obsidian` を作ると、リンクスクリプトが「実体がある」として止まる。手で退避して再実行する。
- 設定の変更が dotfiles のコミットに入り、`notes` 側の `[obsidian]` コミットが使えなくなる。
- `workspace.json` の除外が、両リポジトリで要る。

同じ構成の、確認していない影響（仮説）:

- 改行コードの規則が、`notes` の `.gitattributes`（LF 統一）ではなく dotfiles 側になる。
- `notes` のルートで Claude を開くと、実体は作業ディレクトリの外になり、編集の確認が増える。
- ripgrep などはシンボリックリンクを既定でたどらないので、中身が検索に出ない。
- シンボリックリンクの作成には開発者モードか管理者権限が要る（ジャンクションは不要）。
- ファイル単位のリンクは、Obsidian の保存で実ファイルに置き換わる。
- Obsidian のコアプラグイン `sync` や、WSL（`/mnt/c`）からのリンクの見え方は不明。
- Obsidian の「設定フォルダを上書き」機能で `.obsidian` を別の場所に置けるか（端末ごとの設定のはずで、採用しても脆い）。

実物（2026-10-04）: `.obsidian/` は `notes` で追跡されている。

## Gotchas

- **AI が「置き場を変えても解決しない」と答えた**: `.obsidian` を dotfiles に置いた場合の `AGENTS.md` と `docs/` の粒度への影響を整理させたとき。置き場を変えると作業場が dotfiles のルートに変わり、既存の `AGENTS.md` で足りることを見落とした（作業場を前提にしないまま一般化した）。ユーザーの指摘で「置き場では差が出ない。コストが生じるのは `.obsidian/` 単体で Claude を開く運用のときだけ」に直した。

## Open Questions

- Obsidian の「設定フォルダを上書き」機能は、端末をまたいで使えるか。
- 将来、dotfiles を clone しない環境（スマホなど）が出たとき、到達性の基準は `notes` 側に有利に働くか。
- 他のアプリの設定（Zed、Notepad++ など）を、この6項目で見直すか。

## Related

- [[obsidian-vault]]
- [[zed-dotfiles]]
- [[notepad-plus-plus]]
- [[workflow-kit]]
