---
type: inbox
title: アプリの設定ディレクトリを、どのリポジトリに置くか決める判断基準
tags:
  - tool/obsidian
  - dotfiles
  - repo-layout
  - decision-criteria
  - symlink
created: 2026-10-04
sources:
  - Claude Code conversation ".obsidian の置き場の判断基準"
---

# アプリの設定ディレクトリを、どのリポジトリに置くか決める判断基準

## Goal
Obsidian の設定ディレクトリ（`.obsidian/`）を、Vault のリポジトリ（`notes`）に置くか、設定ファイル用のリポジトリ（dotfiles）に置くかを決める基準を作り、実際に決めたかった。他のアプリの設定にも使える形にする。
統合先の候補: knowledge/obsidian-vault.md（キーワード: obsidian, .obsidian, dotfiles, vault, 設定）、または新規トピック（キーワード: 置き場, 判断基準, symlink, junction, リポジトリ分割）

## Principles
- 設定の置き場は、「その設定が何と連動して変わるか」で決める。連動先が Vault の中身（ノート規約、プロパティ型、検索除外）なら Vault 側、環境全体（テーマ・フォントを複数アプリでそろえるなど）なら dotfiles 側。理由: 連動するものと同じリポジトリにあれば、変更が1つのコミットで済む。
- アプリが固定の場所を読む設定は、実体をその場所に置く。リンクで別のリポジトリに逃がさない。理由: リンクは、clone 順、リンク前の起動による衝突、コミット先の分離といった運用の負担を足す。
- 設定ファイルの管理を2つのリポジトリで相互に参照させない。理由: セットアップの順序が循環し、片方だけの環境で動かなくなる。
- `AGENTS.md` と `docs/` は、リポジトリのルートか、独立して判断を積む単位にだけ置く。小さなサブディレクトリごとには置かない。理由: AI が読む前提資料が作業単位ごとに増え、管理コストだけが膨らむ。
- AI に置き場の影響を説明させるときは、「作業場（Claude を開くディレクトリ）がどこになるか」を前提に整理させる。理由: 置き場を変えると作業場も変わるため、粒度（`AGENTS.md` と `docs/` を置く単位）への影響は、作業場を基準にしないと誤る（Gotchas を参照）。

## Decisions
- **`.obsidian` は `notes`（Vault のリポジトリ）に置き続け、dotfiles には戻さない**（2026-10-04）
  - 根拠: Obsidian は Vault 直下の `.obsidian` を読む（dotfiles に置くとジャンクションが必須）。設定の中身は Vault と連動する。dotfiles → `notes` の片方向の依存を保てる。dotfiles の履歴が、プラグインで重くなる問題を避けられる。Zed とテーマ・フォントをそろえる意図は無い（ユーザーの発言）。全PCに dotfiles も clone するので、到達性は決め手にならない（ユーザーの発言）。
  - 却下案: dotfiles に戻して `notes/.obsidian` へリンクする（上の「根拠」に挙げた負担が増え、得られるのは Zed との統一だけで、その意図が無い）。
- **Obsidian の設定を変える作業は、`notes` のルートで Claude を開いて行う**（2026-10-04）
  - 根拠: `.obsidian/` 専用の `AGENTS.md` と `docs/` を作らずに済む。
  - 却下案: `.obsidian/` 単体を作業単位にする（専用の `AGENTS.md` と `docs/` が要る。`.obsidian/docs/log.md` は、`git log -- .obsidian` の再掲で、実際に履歴から復元して作れた）。

## Facts
- 判断基準の6項目: ① アプリが読む場所の制約、② 設定の連動先、③ リポジトリ間の依存の向き、④ 全環境への到達性、⑤ 履歴の軽さ、⑥ `AGENTS.md` と `docs/` を置く粒度。⑥は、どちらのリポジトリでもルートで作業すれば差が出ない（確認: 2026-10-04、根拠: ユーザーの指摘）。
- `.obsidian` を dotfiles に置いて `notes/.obsidian` へリンクした場合の、確認できている影響（確認: 2026-10-04、根拠: 既存のリンクスクリプトの仕様と `links.map`）:
  - `notes` と dotfiles の clone 順が循環する（dotfiles の `links.map` が `..\notes` を参照するため）。
  - リンクの前に Obsidian が実ディレクトリの `.obsidian` を作ると、リンクスクリプトが「実体がある」として止まる。手で退避して再実行する。
  - 設定の変更が dotfiles のコミットに入り、`notes` 側の `[obsidian]` コミットが使えなくなる。
  - `workspace.json` の除外が、両リポジトリで要る。
- 同じ構成の、確認していない影響（仮説）:
  - 改行コードの規則が、`notes` の `.gitattributes`（LF 統一）ではなく、dotfiles 側になる。
  - `notes` のルートで Claude を開くと、実体は作業ディレクトリの外になり、編集の確認が増える。
  - ripgrep などはシンボリックリンクを既定でたどらないので、中身が検索に出ない。
  - シンボリックリンクの作成には開発者モードか管理者権限が要る（ジャンクションは不要）。
  - ファイル単位のリンクは、Obsidian の保存で実ファイルに置き換わる。
  - Obsidian のコアプラグイン `sync` や、WSL（`/mnt/c`）からのリンクの見え方は不明。
- Obsidian の「設定フォルダを上書き」機能で `.obsidian` を別の場所に置けるかは、未確認（仮説。端末ごとの設定のはずで、採用しても脆い）。

## Gotchas
- 状況: AI に、`.obsidian` を dotfiles に置いた場合の `AGENTS.md` と `docs/` の粒度への影響を整理させたら、「置き場を変えても解決しない」と答えた
  - 原因: 置き場を変えると作業場（Claude を開くディレクトリ）が dotfiles のルートに変わり、既存の `AGENTS.md` で足りることを見落とした。作業場を前提にしないまま一般化した
  - 解決: ユーザーの指摘で、「置き場では差が出ない。コストが生じるのは `.obsidian/` 単体で Claude を開く運用のときだけ」に直した

## Open Questions
- `notes` に残す決定のあと、`.obsidian/` に暫定で作った `AGENTS.md`・`CLAUDE.md`・`docs/` を撤去するか（ユーザーの確認待ち。ただし `notes/docs/` へ移す別の整理が、別のメモに記録されている）。
- Obsidian の「設定フォルダを上書き」機能は、端末をまたいで使えるか。
- 将来、dotfiles を clone しない環境（スマホなど）が出たとき、到達性の基準は `notes` 側に有利に働くか（今は決め手にならない）。

## Next Actions
- `knowledge/obsidian-vault.md` の「dotfiles との関係」に、`.obsidian` を `notes` に置く判断と基準を足す（統合のときに行う）。
- 他のアプリの設定（Zed、Notepad++ など）を、この6項目で見直すかを検討する。
