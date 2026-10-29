---
type: knowledge
title: 公開リポジトリの履歴を git filter-repo で書き換える（語の置換と作者の匿名化）
status: active
tags:
  - tool/git
  - workflow
aliases:
  - 履歴の書き換え
  - 作者の匿名化
triggers: [履歴の書き換え, filter-repo, force push, mailmap, replace-text, replace-message, 作者, author, noreply, 匿名化, lookbehind]
created: 2026-10-29
updated: 2026-10-29
sources:
  - "topics/wording-neutralize（2026-10-27〜10-29。閉じたトピック。決定は root の docs/decisions.md の 2026-10-29 の項）"
---

# 公開リポジトリの履歴を git filter-repo で書き換える（語の置換と作者の匿名化）

## Purpose

公開リポジトリの履歴から、語（環境を特定する語、ユーザー名を含むパス）や作者の身元を消すときの手順と落とし穴。何に置き換えるかは [[public-repo-wording]]。サブディレクトリの切り出しは [[git-subdirectory-split]]。

## Principles

- 書き換えは、現在の文言を片付けてから最後に 1 回にまとめる。書き換えるたびに他の clone の履歴が分岐し、作り直しが要る。
- 使い捨ての mirror clone で試し、結果を数えて確かめてから `git push --force --mirror` する。force の deny はユーザーが切る（`workflow-kit/commit-push-rules.md` の「しないこと」）。
- 確かめるときは `--all` で全件を数える。直近の数件で判断しない。

## 手順（作者を `agent <agent@agent.local>` にそろえる）

1. 古い身元を調べる: `git log --all --format='%aN <%aE>%n%cN <%cE>' | sort -u`（`agent` 以外が対象）。
2. `git clone --mirror <url> x.git`
3. `mailmap.txt` に、古い身元ごとに `agent <agent@agent.local> <古いメール>` を 1 行ずつ書く。
4. 本文の URL にユーザー名がある場合は、`replace-message.txt` に `regex:github\.com/<ログイン名>/==>github.com/<owner>/` を書く（マージコミットの本文）。
5. `cd x.git && git filter-repo --mailmap ../mailmap.txt --replace-message ../replace-message.txt --force`
6. 手順 1 のコマンドが `agent` だけになり、`git log --all --format=%B | grep -ci <ログイン名>` が 0 なのを確かめる。
7. `git remote add origin <url>` の後、`git push --force --mirror origin`（ユーザー）。
8. 他の clone は `git fetch && git reset --hard origin/main`。各 clone の local の `user.name` / `user.email` も `agent` にする（global は変えない）。

語の置換は、同じ流れで `--replace-text`（ファイルの中身）と `--replace-message`（コミットの本文）を使う。

## Facts

- 2026-10-29 に、workbase（1351 コミット、43 ブランチ）、works（208）、dotfiles（240）で作者をそろえ、workbase では語の置換もした（確認: 2026-10-29、根拠: 書き換え後の `git log --all --format='%aN <%aE>' | sort -u` が `agent` と `Claude <noreply@anthropic.com>` だけ。Claude は意図して残した）。
- WSL の room の clone は reset が要らない。`room start` は Windows 側の Project をマウントするだけで、部屋の `.git` は回収後に捨てる（確認: 2026-10-29、根拠: `room.py` の `setup_room_git` `discard_room_git`）。

## Gotchas

- **GitHub の noreply メールで作者を隠したつもりだった**: noreply のアドレスにもログイン名が入るので、名前は隠れない。作者は `agent` にそろえる。
- **直近 15 件のコミットだけを見て「全部 agent」と判断した**: 実際には 189 件が残っていた（2026-10-28 の誤り、10-29 に判明）。`--all` で全件を数える。
- **stash や古い remote ref が残った clone で確かめた**: 書き換え前の身元が出て、偽陽性になる。新しい clone で確かめる。
- **語の regex 置換で、対象語を部分文字列に含む語（法人格の語）や Office のプロパティ名まで変わった**: 除外を先に決める。
- **置換で、検索規則（`push-rules.md` の条件 4）や決定メモの引用まで書き換わった**: 対象語そのものを引用した箇所は、lookbehind で除外する。最初の試験で気づき、直してから push した。

## Related

- [[git-subdirectory-split]]
- [[git-rebase-chronology]]
- [[public-repo-wording]]
