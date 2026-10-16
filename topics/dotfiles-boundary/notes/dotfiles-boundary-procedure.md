# 手順: workbase と dotfiles の切り分け（PC）

状態と要判断は `docs/log.md`、方針は `docs/decisions.md`、ファイルごとの仕分けは [[dotfiles-boundary-inventory]]。ここは PC のセッションで行う手順だけ（番号は `log.md` の項目と同じ）。dotfiles と workbase の両方を開けるところ（ワークスペースのルートか `$HOME\works\repos`）で作業する。

## 2. dotfiles 側の確認（読むだけ）

- `rg -n "workbase|resources/|guides/|exmem|workflow-kit" <dotfiles>` で、dotfiles から workbase への参照を一覧する。一方向の規則で許すのは、`50_repos` の clone の URL と置き場所、スキルが読む kit のパスだけ。それ以外（例: README から `guides/howto/` へのリンク）は、移動後に dotfiles 内のリンクへ直す対象。
- dotfiles の `docs/` の構成（`decisions.md`、`log.md` など）と `AGENTS.md` を読み、移す先と書式を決める。

## 3. 手順書を移す

- dotfiles と workbase のコミットは分ける（`guides/CLAUDE.md` の既存の規則。dotfiles を先にコミットして、移した先が存在してから workbase 側を消す）。
- 移す前に `grep -n '\[\[' guides/howto/*.md` で wikilink を確認し、dotfiles 側では URL か名前に直す。
- 付録「dotfiles 側の課題」は、残っているものを dotfiles の課題の置き場へ移し、付録自体は消す。
- 移したあと、workbase の中に `[[win11]]` `[[debian-family]]` `[[fonts-setup]]` への wikilink が残っていないか確かめる（`rg -n "\[\[(win11|debian-family|fonts-setup)"`）。
- dotfiles の push は、`docs-rules.md` の規則どおり、エージェントは行わずコマンドを報告する。

## 4. workbase の規則・索引を直す

[[dotfiles-boundary-inventory]] の「直す」の表のとおり。

## 5. 割る・削る

- 「削る」は、実物の写しを「dotfiles の `<ファイル>` が正」のような1行に置き換える。判断・理由・Gotchas は残す。
- ノートの形式と更新日は `exmem/AGENTS.md` に従う。

## 6. exmem に残す

- [[app-config-placement]] に、リポジトリ全体の線（置かれる・実行される／読まれる）と、依存の一方向（dotfiles → workbase）を Principles として足す。理由は `docs/decisions.md` の「取り込まない理由」。
- ルートの `AGENTS.md` の「共有の範囲」に、1行で「dotfiles の挙動（スクリプトの中身・配置）をこのリポジトリに書かない。名前とリンクで指す」を足すか、ユーザーに確認する。
