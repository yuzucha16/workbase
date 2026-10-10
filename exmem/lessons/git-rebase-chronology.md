---
type: knowledge
title: rebase の前にコミットの時系列を確認する
status: active
tags:
  - tool/git
  - workflow
  - ai/claude
aliases:
  - rebase の順序確認
  - 分岐した main の rebase
created: 2026-10-06
updated: 2026-10-06
sources:
  - Claude Code conversation "分岐した main の rebase とコンフリクト解消" (2026-10-06)
  - "dotfiles の AGENTS.md の rebase の規則（2026-10-06 に確認）"
---

# rebase の前にコミットの時系列を確認する

## Purpose

複数のPCで同じブランチを更新して分岐したとき、エージェントに rebase を任せる場合の手順と注意点。特に「どちらが時間的に先か」を、実行前に確認する習慣。人とAIの役割分担の考え方は [[human-ai-decision-loop]]。

## Principles

- rebase / merge の前に、双方のコミット日時を比べ、どちらが新しいかを人に伝えて、順序でよいか確認する。rebase はコミットの日時と並びを書き換えるので、実際の作業順とずれた履歴が黙って出来上がる。
- 人が「rebase してよい」と言っても、順序の確認は省かない。許可は手段への許可で、「古い側を新しい側の上に載せる」という結果の確認ではない。
- 履歴を書き換える操作の前に、戻り先のコミットを控える。reflog から戻せるが、戻り先の ID を報告に書いておくと、人が判断しやすい。

## Decisions

### rebase 前に、双方のコミット日時を比べて順序を確認する、をリポジトリの `AGENTS.md` に規則として足した（2026-10-06）

- 根拠: 確認せずに rebase したあとで、人から順序の確認を求められた。結果は時系列に沿っていて問題なかったが、確認のタイミングが事後だった。
- 却下案: 規則を残さず口頭の注意だけで済ませる（次のセッションのエージェントに引き継がれないため）。
- 実物（2026-10-06 確認）: dotfiles の `AGENTS.md` の33行目に、同じ内容の規則がある。

## Facts

- 日時の比べ方は `git log --format='%h %ad %s' --date=iso <ブランチ>` を双方で実行する。作成日時（author date）とコミット日時（committer date）は別の値で、`--format='%ad / %cd'` で両方見られる（確認: 2026-10-06、根拠: `git log --format='%h %ad (author) %cd (commit)' --date=iso`）。
- rebase でコミットし直されたコミットは、author date が元のまま、committer date が rebase の実行時刻になる（確認: 2026-10-06、根拠: rebase 後の `git log`。author 2026-10-05 23:27、commit 2026-10-06 09:13）。
- rebase の直前の位置は `git reflog` に残り、`git reset --hard <ID>` で戻せる（確認: 2026-10-06、根拠: `git reflog` に rebase 前の先頭が記録されていた。戻す操作は実行していない）。
- 分岐の確認は `git log --oneline main..origin/main` と `git log --oneline origin/main..main`、衝突しそうなファイルは `git diff --stat main...origin/main` と `git diff --stat origin/main...main` で見る。双方が変えたファイルの交わりが衝突の候補になる（確認: 2026-10-06、根拠: 今回この手順で、交わりが1ファイルだけと分かり、実際の衝突もそのファイルだけだった）。
- 変更を `git rebase` したあと、ローカルのコミットだけが先行し、リモートの先頭が祖先になっているので、通常の `git push` で足りる（force push は不要）（確認: 2026-10-06、根拠: `git status -sb` が `ahead 4`、のちに push 後 `main...origin/main` が差分なし）。

## Gotchas

- **日付ごとの節を新しい順に積む追記型のログ（`docs/log.md` など）を、2つのPCがそれぞれ更新して rebase した**: 双方が「先頭に新しい日付の節を足す」同じ位置を変えたため、内容が重ならなくても同じ箇所で衝突する。双方の節を両方残し、日付の降順に並べる。マーカー（`<<<<<<<` `=======` `>>>>>>>`）が残っていないことを `Select-String` で確認してから `git add` し、`GIT_EDITOR=true git rebase --continue` で進める。
- **対話できないシェルで `git rebase --continue` を実行した**: エディタが開いてコミットメッセージの確認で止まる場合がある。`GIT_EDITOR=true` を付けると、メッセージをそのまま使って進む。

## Open Questions

- 履歴を書き換える操作（rebase、amend、reset --hard）の前に確認する規則を、リポジトリごとではなく、共通ルール（workflow-kit の `docs-rules.md`）に入れるか（AI の提案。未承認）。
- コミット日時（committer date）が書き換わることを避けたいときは、rebase ではなく merge を選ぶかの基準は未整理。

## Related

- [[human-ai-decision-loop]]
- [[workflow-kit]]
- [[git-line-endings]]
