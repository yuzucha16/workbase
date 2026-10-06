---
type: knowledge
title: 履歴を保ってサブディレクトリを別リポジトリに切り出す（git filter-repo）
status: active
tags:
  - tool/git
  - tool/scoop
  - repository-design
aliases:
  - git filter-repo
  - リポジトリの切り出し
  - サブディレクトリの分離
created: 2026-10-05
updated: 2026-10-05
sources:
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05)
  - "scoop の shim `git-filter-repo.cmd` の存在（2026-10-05 に確認）"
---

# 履歴を保ってサブディレクトリを別リポジトリに切り出す（git filter-repo）

## Purpose

1つのリポジトリの `resources/` 配下を、履歴を保ったまま、新しいリポジトリのルートに切り出した（`notes` → `workbase`。経緯は [[obsidian-vault]]）。同時に、使っていない大きなバイナリ（LFS）を履歴ごと除いた。手順と、確認の観点を残す。

## Principles

- 切り出しは、元のリポジトリを壊さないよう、新しい clone に対して行う。元はアーカイブとして残す。履歴を書き換えるので、元には戻せない。
- 履歴から不要なパス（使っていない大きなバイナリ、LFS の対象）を消すなら、切り出しと一緒に、2回に分けて行う。① 除外（`--invert-paths`）、② ルート化（`--subdirectory-filter`）。後から消すと、履歴をもう一度書き換えることになる。
- 切り出した後は、除外したパスの履歴の漏れ、LFS の参照、remote、単独 clone でのリンク切れを確認する。書き換えの成功は、コマンドの終了だけでは分からない。
- ルート化すると、元のルート直下のファイル（`.gitattributes`、`.gitignore`、`AGENTS.md` など）は、新しいリポジトリに含まれない。新しいルート用に作り直す。

## Decisions

### 切り出しに `git filter-repo` を使う（2026-10-05。`scoop install git-filter-repo` の導入は、ユーザーの承認）

- 根拠: 履歴から特定のパス（`fonts/` など）を除きながら、`resources/` をルートにできる。
- 却下案: `git subtree split`（標準で入っているが、パスを除外できない）、履歴なしの新規リポジトリ（exmem の履歴を失う）。

## Facts

- 手順: `GIT_LFS_SKIP_SMUDGE=1` を設定して `git clone --no-local <元>` → `git filter-repo --invert-paths --path <除くパス>... --force` → `git filter-repo --subdirectory-filter <dir> --force` → ルート用のファイルを足して1コミット → 単独 clone して検査する（確認: 2026-10-05、根拠: 実行した。filter-repo 2.47.0、Windows 11、scoop で導入）。`--force` が要ったかは未確認（仮説: 要らない場合がある）。
- `git filter-repo` は `origin` を削除する。切り出した後に、新しい remote を足す（確認: 2026-10-05、根拠: 切り出し後の `git remote -v` が空だった）。
- 空になったコミットは落ちる。58コミット、139ファイルが、30コミット、68ファイルになった（確認: 2026-10-05、根拠: 切り出しの前後の `git rev-list --count` と `git ls-files`）。
- 履歴の漏れは、`git log --all --oneline -- <パス>` が0件、LFS は `git lfs ls-files` が0件で確認できる（確認: 2026-10-05、根拠: 除外した6つのパスで実行した）。
- 単独 clone して wikilink を全件検索すると、規約の説明文にある書式の例（`[[リンク]]` など）が、未解決として出る。実際の切れではない（確認: 2026-10-05、根拠: 340件中8件で、すべて書式の例だった）。
- `git-filter-repo` は scoop の shim として、現在も入っている（確認: 2026-10-05、根拠: `Get-Command` が `scoop\shims\git-filter-repo.cmd` を返した）。

## Gotchas

なし

## Open Questions

- `--force` が要る条件（clone の状態）。

## Related

- [[obsidian-vault]]
- [[scoop-app-management]]
