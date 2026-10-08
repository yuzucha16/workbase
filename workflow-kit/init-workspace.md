# init: ワークスペースの生成（項目 5）

`init-hook.md` の導入項目 5 の作り方。項目 5 のときだけ読む。入力、自己点検、報告の型は `init-hook.md` に従う。項目 5 は任意（トップを作るときだけ。1〜3 も合わせて導入する）。

Vault のトップを、この PC だけのローカルなリポジトリとして作る。共有ナレッジ（`resources/` = `workbase`）は、トップが参照するだけで、トップの管理に入れない。骨組みはこのフックで作り、PC ごとの違いは中身（PARA、`docs/`、固有ルール）に限る。決まった配置（リンクと clone）は、dotfiles（`30_link`、`50_repos`）が行う。

1. **確認する**（変更しない）: 対象の中身（空か、既存のファイルがあるか）、`.git` の有無、`resources/.git` の有無と、その `origin` が `workbase` か、`.obsidian` が実ディレクトリかジャンクションか。`resources/` が無いときは、clone を案内して止まる（このフックは clone しない）。`.obsidian` が実ディレクトリのときは、dotfiles の `30_link` が `[ERR]` で止まるので、手で退避する旨を報告に書く。
2. **生成する**（既存は上書きしない）:
   - `.gitignore`: `templates/workspace/gitignore.template` を、そのまま置く。
   - `.ignore`: `templates/workspace/ignore.template` を、そのまま置く。ripgrep（Claude Code の Grep / Glob を含む）は `.gitignore` を尊重するので、`.gitignore` が除外する `resources/` が、検索から黙って外れる。`.ignore` の `!/resources/` で打ち消す（実測: 2026-10-05）。
   - `.gitattributes`: `templates/workspace/gitattributes.template` を、そのまま置く（改行コードを LF に統一する。Obsidian・AI・WSL/Linux の出力が LF のため）。
   - `AGENTS.md`: `templates/workspace/AGENTS.md` を埋める（役割、remote、固有ルール）。「共通ルール」の節は、雛形のまま変えない。`CLAUDE.md`、`docs/` は、項目 1 と 2 のとおり。
   - `areas/` `projects/` `archives/`: `.gitkeep` を置く（既存の中身があっても。中身は追跡しない）。
   - `git init`。remote は、方針が「なし」なら足さず、`templates/workspace/pre-push.template` を `.git/hooks/pre-push` として置く（誤って remote を足しても push を止める。改行は LF）。URL があれば `origin` を足す（push はしない）。
3. **初回コミットをする**（`init-hook.md` の入力 7 が「する」のとき。`docs-rules.md` の「コミットと push」に従う）。コミットが1つもないときだけ行う（`git rev-parse --verify HEAD` が失敗する）。既にコミットがあれば、何もコミットせず、報告に書く。
   - 追加するのは、このフックが生成した次のファイルだけ（パス指定）: `.gitignore`、`.ignore`、`.gitattributes`、`AGENTS.md`、`CLAUDE.md`、`docs/`、`areas/.gitkeep`、`projects/.gitkeep`、`archives/.gitkeep`。PARA の既存の中身は、追跡しない（未追跡のまま、報告に一覧する）。
   - コミットの前の確認（`docs-rules.md` の ① 〜 ③）に加えて、`resources/` と `.obsidian` がステージされていないこと。外れたら、ステージを戻して（`git reset -q -- <パス>`）、コミットせずに報告する。
   - 身元とトレーラーは、`docs-rules.md` の「コミットの身元とトレーラー」に従う（agent の身元を `-c` で渡す。`git config` は変えない）。
   - メッセージ: `[works] initial commit: PC-local vault top (PARA, docs, AGENTS.md, ignore rules)`。
   - push はしない。remote があるときは、報告に push のコマンド（`git push -u origin main`）を書き、リモートに既存のコミットがあると拒否されるので、その場合は先に `git pull --rebase origin main` が要る旨を添える。
