# 洗い出し: workbase の中の dotfiles への依存

- 作成: 2026-10-12。workbase の main（`61da8fc`）で `dotfiles`、`30_link`、`50_repos`、`scripts/` を全文検索した結果を、[[dotfiles-boundary-handover]] の線で仕分けた。
- 該当は 44 ファイル（`topics/` を除く）。1つのファイルが2つの区分に出る場合（`app-config-placement.md`、`docs-rules.md`）は、件数では主な区分で1回だけ数えた。仕分けは AI の案。**要判断**の行は、ユーザーに確認してから動かす。
- dotfiles 側は読めていない。dotfiles の中で workbase を参照している箇所は、PC で洗い出す（[[dotfiles-boundary-next-steps]] の 2）。

## 区分

| 区分 | 意味 | 件数 |
|---|---|---|
| 移す | dotfiles の使い方・挙動を書いた文書。dotfiles 側へ移す | 3 |
| 割る | 汎用の知識と、dotfiles 固有の記録が混ざる。固有の部分を dotfiles の `docs/` へ移す | 4（要判断） |
| 削る | 汎用の知識。dotfiles の「実物」「現状」の写し（ファイル配置、行番号、確認した中身）だけを、dotfiles へのリンクか名前に置き換える | 18 |
| 直す | 規則・索引。移動に合わせて書き換える | 5 |
| 残す | 名前・例・出典として触れるだけ。一方向の規則に反しない | 14 |

frontmatter の出典（`sources:` の「dotfiles の〜を確認」）は、履歴なので**どの区分でも残す**。

## 移す（guides/howto → dotfiles）

| ファイル | 行数 | 内容 | 移動先の案 |
|---|---|---|---|
| `guides/howto/win11.md` | 181 | Win11 の導入から dotfiles のスクリプト（`10`〜`40`）まで。付録に「dotfiles 側の課題」 | dotfiles の `docs/setup/win11.md` |
| `guides/howto/debian-family.md` | 319 | Debian 系の導入から dotfiles のスクリプトまで。付録あり | dotfiles の `docs/setup/debian-family.md` |
| `guides/howto/fonts-setup.md` | 49 | `scripts/*/24_fonts.*` の前後の手動作業 | dotfiles の `docs/setup/fonts-setup.md` |

- 移すと、`guides/howto/` は空になる。`guides/quickref/` と `guides/explain/` は dotfiles に依存しないので残る。
- 付録「dotfiles 側の課題」は、移した先では不要になる（同じリポジトリで直せる）。残っている課題は、dotfiles の `docs/log.md` などへ移す。
- 移した文書から workbase のノートへの `[[wikilink]]` は、リンク切れになる。GitHub の URL か名前に置き換える（移す前に `grep '\[\['` で確認）。

## 割る（要判断）

| ファイル | dotfiles 固有の部分 | 汎用の部分（残す） |
|---|---|---|
| `exmem/lessons/pc-setup-manuals.md` | 「場所」「Facts」（`GHQ_ROOT`、`lib.sh` の関数）、「初回の取得」、`scripts/wsl` の改名 | 手順書の分け方（パッケージ系統）、Rufus、git の SSL バックエンドと credential の判断 |
| `exmem/lessons/zed-dotfiles.md` | 「管理しているもの」「Windowsでの配置」（dotfiles のパスとリンク） | Zed の設定の置き場、extension と ACP エージェントの管理方針、目の負担の設定。名前を `zed-config.md` などに変える案 |
| `exmem/lessons/shell-command-usecases.md` | 「正本はこのノート。dotfiles の種ファイルはここから機械的に作る」。履歴の種（`history.seed.*`）の元のコードブロック | コマンドの使いどころの判断基準。種は PC に置かれるものなので、線に従えば正本は dotfiles 側 |
| `exmem/lessons/obsidian-vault.md` | 「現在の状態」の環境変数と `.obsidian` のジャンクション、dotfiles の試験結果（51/51） | Vault の構造と原則。構造は workbase の規約（kit）の側なので残す |

## 削る（実物の写しを、リンクか名前に置き換える）

| ファイル | 削る対象（例） |
|---|---|
| `exmem/lessons/app-config-placement.md` | `.obsidian` の実体のパス（`windows/obsidian/.obsidian`）。判断と理由は残す |
| `exmem/lessons/claude-code-permissions.md` | `links.map`、`w2a_copy_dotfiles.bat`、`home/.claude/settings.json` などの配置（「dotfiles の `README.md` が正」と既に書いてある） |
| `exmem/lessons/claude-code-auth-providers.md` | `windows/claude/` のファイル一覧とリンク先 |
| `exmem/lessons/claude-code-storage.md` | `home/.claude/settings.json` へのリンクの確認 |
| `exmem/lessons/claude-code-project-settings.md` | 実体のパス（1 か所） |
| `exmem/lessons/terminal-cursor-blink.md` | 「確認済み（dotfiles の実物）」の節 |
| `exmem/lessons/shell-fzf-keybindings.md` | 「dotfiles の実物」の行。既に「現仕様は dotfiles の `docs/decisions.md`」とある |
| `exmem/lessons/shell-script-testing-wsl.md` | `30_link.sh` などの名前は例として残す。`lib.sh` の中身の写し |
| `exmem/lessons/notepad-plus-plus.md` | `windows/notepadpp/` と `links.map` の中身 |
| `exmem/lessons/scoop-app-management.md` | `20_apps.bat` の行番号と中身 |
| `exmem/lessons/fonts.md` | `home/.config/zed/settings.json` の確認 |
| `exmem/lessons/gh-release-download.md` | `24_fonts.*` の検索結果 |
| `exmem/lessons/git-line-endings.md` | dotfiles での `git ls-files --eol` の結果 |
| `exmem/lessons/git-rebase-chronology.md` | 「dotfiles の `AGENTS.md` の33行目」 |
| `exmem/lessons/obsidian-appearance.md` | スニペットのパス（出典だけなら残す） |
| `exmem/lessons/zed-acp.md` | `profile.ps1` のリンク先の旧パス（`C:\vault\...`） |
| `exmem/lessons/wsl-file-placement.md`、`office-ai-workspace.md` | 旧配置（`C:\vault\repos\...`）。既に古い。現状への付記か削除 |

## 直す（移動に合わせて書き換える）

| ファイル | 書き換え |
|---|---|
| `guides/guides-index.md` | win11 / debian-family / fonts-setup の行を、dotfiles の `docs/setup/` への1行のリンクにまとめる |
| `guides/CLAUDE.md` | 「手順書(howto/)の作り方」のうち dotfiles に依存する規則（スクリプトが正、付録、作る流れの 2 と 5、リポジトリごとのコミット）を dotfiles へ移す。書式・文体の規則は残すか、一緒に移すか（**要判断**） |
| `exmem/README.md` | 33 行目「dotfiles は exmem を読み取り専用で参照」。一方向の規則として残し、文言をそろえる |
| `exmem/lessons/ai-development-workflow.md` | 「作業ログはリポジトリ側、知識は exmem」。今回の線（置かれる・実行される／読まれる）を足す |
| `exmem/lessons/app-config-placement.md` | 原則「相互に参照させない」を、リポジトリ全体の一方向の規則に広げる（反映先の第一候補） |
| `workflow-kit/docs-rules.md` | 102 行目の push の規則「共有リポジトリと dotfiles は、公開範囲が決まるまで対象外」。両方 public 前提なら、対象外のまま理由を書き換えるか（**要判断**） |

## 残す（名前・例・出典だけ。一方向の規則に反しない）

- `workflow-kit/init-workspace.md`、`init-hook.md`、`README.md`、`templates/workspace/AGENTS.md`、`examples/setup-example.md`: `resources/` の clone と `.obsidian` のリンクは外の担当（dotfiles の `50_repos` / `30_link`）、という契約。スクリプト名は名前として残してよい。中身は書いていない。
- `workflow-kit/README.md` 84 行目: dotfiles のスキルが kit を読む。dotfiles → workbase の向きなので正しい。
- `workflow-kit/start-hook.md`、`docs-rules.md` 91 行目: 例・発生元として触れるだけ。
- `exmem/lessons/dotfiles-shell-tuning.md`: 汎用の知見として書かれている。名前に dotfiles を含むが、そのままでよい（変えるなら割るの判断と一緒に）。
- `exmem/lessons/reference-doc-types.md`: 手順書の見本として dotfiles の README を指す。URL に直すだけでよい。
- `exmem/lessons/vscode-workspace.md`、`workflow-kit.md`、`human-ai-decision-loop.md`、`ai-harness-concepts.md`、`zed-vim.md`、`exmem/tags.md`: 例・経緯として触れるだけ。
- `topics/ai-workspace-boundary/notes/ai-boundary-design.md`: 「Obsidian / Zed の設定は dotfiles 側」。今回の線と一致。
