# init: works の生成（項目 5）

`init-hook.md` の導入項目 5 の作り方。項目 5 のときだけ読む。入力と報告の型は `init-hook.md` に従う（既定値と、項目 5 の自己点検は、このファイルの末尾）。項目 5 は任意（トップを作るときだけ。1〜3 も合わせて導入する）。

works のトップを、この PC だけのローカルなリポジトリとして作る。共有ナレッジ（`resources/` = `workbase`）は、トップが参照するだけで、トップの管理に入れない。骨組みはこのフックで作り、PC ごとの違いは中身（PARA、`docs/`、固有ルール）に限る。決まった配置（リンクと clone）は、dotfiles（`30_link`、`50_repos`）が行う。

1. **確認する**（変更しない）: 対象の中身（空か、既存のファイルがあるか）、`.git` の有無、`resources/.git` の有無と、その `origin` が `workbase` か、`.obsidian` が実ディレクトリかジャンクションか。`resources/` が無いときは、clone を案内して止まる（このフックは clone しない）。`.obsidian` が実ディレクトリのときは、dotfiles の `30_link` が `[ERR]` で止まるので、手で退避する旨を報告に書く。
2. **生成する**（既存は上書きしない）:
   - `.gitignore`: `templates/workspace/gitignore.template` を、そのまま置く（`/resources_p/` を含む）。
   - `.ignore`: `templates/workspace/ignore.template` を、そのまま置く。ripgrep（Claude Code の Grep / Glob を含む）は `.gitignore` を尊重するので、`.gitignore` が除外する `resources/` と `resources_p/` が、検索から黙って外れる。`.ignore` の `!/resources/` と `!/resources_p/` で打ち消す（実測: 2026-10-05）。
   - `.gitattributes`: `templates/workspace/gitattributes.template` を、そのまま置く（改行コードを LF に統一する。Obsidian・AI・WSL/Linux の出力が LF のため）。
   - `.claude/settings.json`: `templates/workspace/claude-settings.template.json` を、そのまま置く（`projects/` `areas/` `archives/` の `Read` と `Edit` を deny。AI 作業部屋の works 側の安全網。既に `.claude/settings.json` があれば上書きせず、`permissions.deny` に足す案を報告する。実機での効き方: 2026-10-16 に works のトップで起動して確認した。`areas/` のファイルの `Read` は拒否された。PowerShell（`Get-Content`）は止まらない。つまり `Read` と `Edit` の道具だけを止める安全網で、シェル経由は防げない）。追跡する（`.claude/settings.local.json` は追跡しない）。
   - `README.md`: `templates/workspace/README.md` を埋める（名前、役割。構成の表は、この PC の実態に合わせて足す・消す）。
   - `AGENTS.md`: `templates/workspace/AGENTS.md` を埋める（役割、remote、固有ルール）。「共通ルール」の節は、雛形のまま変えない。`CLAUDE.md`、`docs/` は、項目 1 と 2 のとおり。
   - `areas/` `projects/` `archives/`: `.gitkeep` を置く（既存の中身があっても。中身は追跡しない）。
   - `resources_p/`: 空のディレクトリを作る（既存なら何もしない）。PC ローカルの resources（共有の `resources/` に置けない、この PC だけの情報の置き場）。`.gitignore` が除外するので、`.gitkeep` は置かない。works 側の AI は読み書きしてよい（`claude-settings.template.json` で deny しない）。
   - `git init`。remote は、方針が「なし」なら足さず、`templates/workspace/pre-push.template` を `.git/hooks/pre-push` として置く（誤って remote を足しても push を止める。改行は LF）。URL があれば `origin` を足す（push はしない）。
3. **初回コミットをする**（`init-hook.md` の入力 7 が「する」のとき。`docs-rules.md` の「コミットと push」に従う）。コミットが1つもないときだけ行う（`git rev-parse --verify HEAD` が失敗する）。既にコミットがあれば、何もコミットせず、報告に書く。
   - 追加するのは、このフックが生成した次のファイルだけ（パス指定）: `.gitignore`、`.ignore`、`.gitattributes`、`.claude/settings.json`、`README.md`、`AGENTS.md`、`CLAUDE.md`、`docs/`、`areas/.gitkeep`、`projects/.gitkeep`、`archives/.gitkeep`。PARA の既存の中身は、追跡しない（未追跡のまま、報告に一覧する）。
   - コミットの前の確認（`docs-rules.md` の ① 〜 ③）に加えて、`resources/`、`resources_p/`、`.obsidian` がステージされていないこと。外れたら、ステージを戻して（`git reset -q -- <パス>`）、コミットせずに報告する。
   - 身元とトレーラーは、`docs-rules.md` の「コミットの身元とトレーラー」に従う（agent の身元を `-c` で渡す。`git config` は変えない）。
   - メッセージ: `[works] initial commit: PC-local vault top (PARA, docs, AGENTS.md, ignore rules)`。
   - push はしない。remote があるときは、報告に push のコマンド（`git push -u origin main`）を書き、リモートに既存のコミットがあると拒否されるので、その場合は先に `git pull --rebase origin main` が要る旨を添える。

## 既定値

`init-hook.md` の入力で、項目 5 とみなしたときの既定値（質問せずに使う。ユーザーが言葉で指定した項目は、それを優先する）。

| 入力 | 既定値 |
|---|---|
| 対象ディレクトリ | `$HOME\works`（Windows と WSL の標準の場所。ネイティブ Linux では、対象を言葉で指定する。例: `~/works`） |
| 目的 | 業務用 PC の作業場。この PC のローカルの作業を PARA で管理し、共有ナレッジ（`resources/`）を参照する。 |
| 読む順番の固有項目 | なし |
| 固有ルール | なし |
| PC の役割 | 業務用 |
| remote の方針 | なし |
| 初回コミット | する |

## 自己点検（項目 5）

- [ ] works を生成した場合（項目 5）: `.gitattributes` がある。`.gitignore` に `/resources/` と `/.obsidian` があり、`.ignore` に `!/resources/` がある（トップで `resources/` の中の語を Grep して、ヒットすることを確認する）。`resources/` と `.obsidian/` に何も書いていない。remote が方針どおり（「なし」なら `git remote -v` が空で、`pre-push` がある）。`AGENTS.md` が works 用の雛形で、共通規約を複製していない。PARA の3フォルダと `README.md` がある。初回コミットは、生成物だけ（`git show --stat HEAD` で確認）で、PARA の既存の中身と `resources/` `.obsidian` を含まない。初回コミットが agent の身元（`agent <agent@agent.local>`）で、トレーラー2行（`Agent` `Kit-Rev`。`Workflow-Kit` は 2026-10-08 に廃止）が付いている（`git log -1 --format=fuller` で確認）。`git config` を書き換えていない。push していない。既定値を使った項目は、報告の「条件」に「既定値」と明記した
