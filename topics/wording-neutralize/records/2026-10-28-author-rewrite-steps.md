# works・dotfiles の author を agent にそろえる手順

起票: 2026-10-28（NA 11）。workbase は済み（全コミットが `agent <agent@agent.local>`）。noreply メールにも `yuzucha16` が入っているので、これでは名前が隠れない。force push はユーザーが実行する（deny を切る）。

対象: works（`worksample`）と dotfiles。

1. 古い身元を調べる: `git log --all --format='%aN <%aE>%n%cN <%cE>' | sort -u`（`agent` 以外が対象。dotfiles には `user <user@example.com>` もある）。
2. 作業用に mirror clone する: `git clone --mirror <url> x.git`。
3. `mailmap.txt` に、1 の古い身元ごとに `agent <agent@agent.local> <古いメール>` を 1 行ずつ書く。
4. `replace-message.txt` に `regex:github\.com/yuzucha16/==>github.com/<owner>/` を書く（マージコミットの本文の URL。各リポジトリ 1 件）。
5. `cd x.git && git filter-repo --mailmap ../mailmap.txt --replace-message ../replace-message.txt --force`
6. 確認: 手順 1 のコマンドが `agent <agent@agent.local>` だけになり、`git log --all --format=%B | grep -ci yuzucha16` が 0。
7. `git remote add origin <url>` の後、`git push --force --mirror origin`（ユーザー）。
8. 他の PC・WSL の clone は `git fetch && git reset --hard origin/main`。

試験（2026-10-28、クラウドの複製）: works 208、dotfiles 240 コミットが全部 agent、本文の該当は 0 件。
