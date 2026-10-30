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
triggers: [filter-repo, 切り出し, 分離, サブディレクトリ, 別リポジトリ, 履歴を保つ, subtree, bundle, mailmap, author, 作者, 匿名, noreply, force push, push --mirror, reset --hard, reset-author, 履歴の書き換え, git log --all, stash, contribution, 草, user.email, replace-message]
created: 2026-10-05
updated: 2026-10-30
sources:
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05)
  - "scoop の shim `git-filter-repo.cmd` の存在（2026-10-05 に確認）"
  - Claude Code conversation "作者を agent にそろえる書き換え" (2026-10-29)
---

# 履歴を保ってサブディレクトリを別リポジトリに切り出す（git filter-repo）

## Purpose

1つのリポジトリの `resources/` 配下を、履歴を保ったまま、新しいリポジトリのルートに切り出した（`notes` → `workbase`。経緯は [[obsidian-vault]]）。同時に、使っていない大きなバイナリ（LFS）を履歴ごと除いた。手順と、確認の観点を残す。

## Principles

- 切り出しは、元のリポジトリを壊さないよう、新しい clone に対して行う。元はアーカイブとして残す。履歴を書き換えるので、元には戻せない。
- 履歴から不要なパス（使っていない大きなバイナリ、LFS の対象）を消すなら、切り出しと一緒に、2回に分けて行う。① 除外（`--invert-paths`）、② ルート化（`--subdirectory-filter`）。後から消すと、履歴をもう一度書き換えることになる。
- 切り出した後は、除外したパスの履歴の漏れ、LFS の参照、remote、単独 clone でのリンク切れを確認する。書き換えの成功は、コマンドの終了だけでは分からない。
- 切り出し元は、完全な履歴の保管場所として扱う（切り出し先は、除外したパスの履歴を持たない）。元の GitHub リポジトリを削除する前に、削除に依存しない形（`git bundle create <名前>.bundle --all`、`git bundle verify`）で、別の媒体にも複製して検証する。アーカイブは戻せるが、削除は戻せない（または期間に限りがある）ので、削除は急がず、前提の確認が済んでから、期限を決めて行う（2026-10-06）。
- ルート化すると、元のルート直下のファイル（`.gitattributes`、`.gitignore`、`AGENTS.md` など）は、新しいリポジトリに含まれない。新しいルート用に作り直す。

### 履歴の作者を書き換えて匿名にする（2026-10-29）

- 作者の匿名化は、名前だけでなくメールも変える。理由: GitHub の noreply メール（`<数字>+<ユーザー名>@users.noreply.github.com`）にユーザー名が入っており、名前だけ変えても読み取れる。
- 履歴の確認は、`git log --all --format='%aN <%aE>' | sort -u` で履歴全体の作者の種類を見る。直近の数件だけで「全部そろった」と判断しない。理由: 古いコミットに別の作者が残る。
- 書き換えは、使い捨ての mirror clone で行い、結果を確認してから push する。理由: 元の clone を壊さず、やり直せる。
- `agent@agent.local` のような、アカウントに紐づかないメールにすると、GitHub の contribution graph（草）には載らない。理由: GitHub はコミットのメールをアカウントのメールと照合して集計する。

## Decisions

### 履歴の作者は `agent <agent@agent.local>` にそろえる（2026-10-29）

- **作者は `agent`、メールは `agent@agent.local` にそろえる。** 根拠: ユーザーが、匿名にするなら `agent@agent.local`（草に載らないだけ）と確認し、各 clone の local の git config をその値に直した。却下案: noreply メールのまま名前だけ `agent`（メールからユーザー名が読める）。
- **force push は、ユーザーが deny を切った後に、`push --force --mirror` で全ブランチを入れ替える。** 根拠: ユーザーが「force push してよい」と明示した。却下案: `main` だけを push する（他ブランチの旧履歴が GitHub に残る）。
- **git config は global でなく local（clone ごと）で `agent` にする。** 根拠: ユーザーが local で運用している。却下案: global を変える（他の用途のコミットまで匿名になる）。

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

### 作者の書き換え（確認: 2026-10-29。特記以外の根拠は下の各項）

- 手順は、`git clone --mirror` → mailmap（`agent <agent@agent.local> <古いメール>` を古い身元ごとに 1 行）→ `git filter-repo --mailmap <mailmap> --replace-message <regex ファイル> --force` → 確認 → `git remote add origin` → `git push --force --mirror origin`（根拠: works 208・dotfiles 240・workbase 1351 コミットで実行し、作者が `agent` と別の意図した作者だけになった）。
- `--mailmap` は author と committer の両方を書き換える（根拠: 書き換え後の `%aN`・`%cN` の出力）。
- マージコミットの本文に入る `Merge branch 'main' of https://github.com/<ユーザー名>/<リポジトリ>` は mailmap では直らず、`--replace-message` の `regex:github\.com/<ユーザー名>/==>github.com/owner/` で直る（根拠: 書き換え後に `git log --all --format=%B` の該当が 0 件）。
- `git filter-repo` は `origin` を外すので、push の前に `git remote add origin <url>` が要る（根拠: 書き換え後の mirror に remote が無く、追加して push できた）。
- システムの Python は PEP 668 で `pip install --user` が拒否される。`uv tool install git-filter-repo` で入る（根拠: 実行結果）。
- 書き換え後の他の clone は、`git fetch --prune && git reset --hard origin/main` で合わせる。未コミットの変更は消えるので、先に退避する（根拠: 手元と他の Windows PC の clone で実行し、作者の種類が揃った。ユーザーの報告）。
- 直近のコミットだけを直す場合は `git rebase <基点> --exec "git commit --amend --no-edit --reset-author"` で足りる。ただし、この環境のエージェントは `rebase`・`--amend`・`reset --hard` が権限で拒否され、ユーザーが実行した（根拠: 拒否された実行結果）。

## Gotchas

- **書き換えと push の後に `git log --all --format='%aN <%aE>' | sort -u` を実行すると、ユーザー名の作者が大量に出た**: 原因は、`--all` が `refs/stash` と、更新前の `origin/*` も数えること。stash は古い履歴を土台にしている。解決: `git fetch --prune` の後、`git for-each-ref --contains <ハッシュ>` で、どの ref が持つかを見る。stash のみなら、不要か確かめて `git stash drop` する。
- **「全コミットが `agent`」と記録したが、実際は古いコミットに別の作者が 189 件残っていた**: 原因は、直近 15 件の `git log` だけを見て判断したこと。解決: 履歴全体の作者の種類を数える（`--all` と `sort -u`）。

## Open Questions

- 提案: マージコミット本文の置換先は `owner` とした（AI の提案。未承認。別の語がよければやり直しになる）。
- `--force` が要る条件（clone の状態）。
- 切り出し元（旧 `notes`）の GitHub リポジトリを削除する時期と、`git bundle` の保存先・世代管理（[[obsidian-vault-backup]] の「旧 GitHub リポジトリ（`notes`）の削除」）。

## Next Actions

- 他の端末の clone は合わせ済み。WSL の room は対象外（workbase の clone を持たず、部屋の `.git` は回収後に捨てる使い捨て。確認: 2026-10-29、根拠: `room.py` を読んだ。WSL の中は未確認）。

## Related

- [[obsidian-vault]]
- [[scoop-app-management]]
