---
type: knowledge
title: 外部の Claude Code スキル（プラグイン）の取り込み方
status: active
tags:
  - ai/claude
  - plugins
  - skills
  - setup
  - testing
aliases:
  - Claude Codeプラグインの導入
  - 外部スキルの取り込み
  - obsidian-skills の導入
triggers: [プラグイン, スキル, 外部スキル, 取り込み, marketplace, obsidian-skills, 導入, skill, 拡張]
created: 2026-10-14
updated: 2026-10-14
sources:
  - Claude Code conversation "obsidian-skills と defuddle の自動導入" (2026-10-14)
---

# 外部の Claude Code スキル（プラグイン）の取り込み方

## Purpose

外部が配布する Claude Code のスキル（プラグイン）を、複数PCで同じ状態に自動導入し、使う側にその存在をどう伝えるかの判断。

## Principles

- 外部スキルの本体（`SKILL.md`）は、自分のリポジトリや知識ベースに写さず、導入の宣言だけを持つ。理由: 更新はプラグインが持つので、写すと古くなり、正本が二重になる。
- 「どの作業でどのスキルを使うか」は、使う側の作業ディレクトリの `AGENTS.md` に1〜2行で書く。共有側には固有名を外した一般形だけを置く。理由: スキルは `description` で自動検出されるので存在を教える手間は小さく、共有側に作業固有の名前を出さずに済む。
- スキルを読むのは Claude Code 系だけで、他のエージェントには届かない前提で書く。理由: 他のエージェントにも効かせたい手順は、スキルでなく `AGENTS.md` に書く必要がある。
- `.bat` などの試験で偽のコマンドを `PATH` の先頭に置くときは、先にスクリプト自身が `PATH` を書き換えないかを確認する。理由: スクリプトが本物の場所を先頭に足すと、偽物より先に本物が呼ばれ、実環境に副作用が出る。

## Decisions

- **導入は CLI（`claude plugin marketplace add` / `install`）と、設定ファイルの宣言（`enabledPlugins` / `extraKnownMarketplaces`）の併用にする**（2026-10-14）
  - 根拠: ユーザー設定ファイルをリポジトリへのリンクで管理していると、CLI の導入が宣言をそのファイルへ書く。差分を戻すと、その PC でもプラグインが無効になりうる。併用なら、他の PC は `git pull` だけで宣言が入る。
  - 却下案: 差分を戻して CLI だけに一本化する（その PC で無効になる）、`git update-index --skip-worktree` で追跡から外す（設定の編集のたびに注意が要る）、設定の宣言だけで導入する（当初の CLI 方式の選択を、上の理由で変えた）。

## Facts

- `claude plugin marketplace add <ソース>` と `claude plugin install <plugin>@<marketplace>` が、`.bat` から呼べる。導入先は user スコープ（確認: 2026-10-14、根拠: 実行して `Successfully installed plugin ... (scope: user)` と表示）。
- ユーザー設定に `enabledPlugins`（`obsidian@obsidian-skills`）と `extraKnownMarketplaces`（GitHub の `kepano/obsidian-skills`）が入り、`claude plugin list` で user スコープ・enabled（v1.0.1）と出る（確認: 2026-10-14、根拠: 設定ファイルと `claude plugin list` を実際に見た）。
- `/skills` の画面で、プラグイン由来のスキルは `locked by plugin` と表示され、スキル単位では切り替えられない（仮説）。プラグイン単位では `claude plugin disable|enable <plugin>@<marketplace>` で切り替える。
- `/skills` の `~NN tok` は、名前と `description` の常時コストの見積もり。6スキルの合計は約 597 tok で、本文は呼ばれたときだけ約0.3k〜5k tok かかる（確認: 2026-10-14、根拠: `claude plugin details` の出力）。
- Obsidian 上の Claude Code プラグイン（Claudian）は、ユーザースコープのプラグインのスキルを読み、使えた（確認: 2026-10-14、根拠: ユーザーの報告）。

## Gotchas

- 状況: 偽の `claude` を `PATH` の先頭に置いて、`claude plugin install` を呼ぶ `.bat` を試験した
  - 原因: スクリプトが `~\.local\bin` を `PATH` の先頭に足していて、本物の `claude` が先に呼ばれ、実環境にプラグインが導入された
  - 解決: `where` で先に探し、`PATH` に無いときだけ末尾に足す形に直し、偽の `claude` / `volta` を使う試験を足した
- 状況: ユーザー設定ファイルをリンクで管理している PC で `claude plugin install` を実行した
  - 原因: CLI がリンク先のファイルに `enabledPlugins` と `extraKnownMarketplaces` を書き、リポジトリに未コミットの差分が出た
  - 解決: 上の決定のとおり、2キーをコミットして併用にした

## Open Questions

- 提案: 外部スキルを取り込む前に、配布元と `SKILL.md` の中身を確認する運用にするか（AI の提案。未承認）

## Next Actions

- 他の PC で、導入スクリプトを実行し、`/skills` に6つが見えることを確認する（2026-10-14 時点）

## Related

- [[claude-code-project-settings]]
- [[claude-code-permissions]]
- [[obsidian-vault]]
