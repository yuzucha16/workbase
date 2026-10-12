# 次のステップ: workbase と dotfiles の切り分け

方針は [[dotfiles-boundary-handover]]。ファイルごとの仕分けは [[dotfiles-boundary-inventory]]。ここは PC のセッションで行う順序。dotfiles と workbase の両方を開けるところ（Vault のトップか `$HOME\works\repos`）で作業する。

## TODO（済んだら `[x]`）

- [ ] 要判断の4つをユーザーに確認する（下の「1」）
- [ ] dotfiles の中で workbase を参照している箇所を洗い出す（下の「2」）
- [ ] 手順書3本を dotfiles へ移す（下の「3」）
- [ ] workbase の規則・索引を直す（下の「4」）
- [ ] 「割る」「削る」を行う（下の「5」）
- [ ] 線と一方向の規則を exmem に残す（下の「6」）
- [ ] 反映が終わったら、`mobile-session/dotfiles-boundary/` を削除し、`mobile-session-index.md` の行を消す

## 1. 要判断（ユーザーに1つずつ確認）

1. 手順書の移動先。案: dotfiles の `docs/setup/`。dotfiles に既にある手順書（`windows/claude/README.md`）の置き方と合わせるか。
2. `guides/CLAUDE.md` の手順書の書式・文体の規則を、workbase に残すか、dotfiles へ一緒に移すか。案: 移す（workbase に手順書が無くなるため）。将来 workbase に手順書が戻るなら、[[reference-doc-types]] に型があるので足りる。
3. 「割る」の4ノートを、割るか、そのまま残して実物の写しだけ削るか。案: `pc-setup-manuals` と `zed-dotfiles` は割る、`shell-command-usecases` の種の正本は dotfiles へ、`obsidian-vault` は削るだけ。
4. `docs-rules.md` の push の対象外の理由。案: 「公開範囲が決まるまで」を「public 前提で扱うため、push の前に人が確認する」に書き換え、対象外は維持。

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

- [[app-config-placement]] に、リポジトリ全体の線（置かれる・実行される／読まれる）と、依存の一方向（dotfiles → workbase）を Principles として足す。理由は handover の「取り込まない理由」。
- ルートの `AGENTS.md` の「共有の範囲」に、1行で「dotfiles の挙動（スクリプトの中身・配置）をこのリポジトリに書かない。名前とリンクで指す」を足すか、ユーザーに確認する。
