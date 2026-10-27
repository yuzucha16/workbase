---
type: knowledge
title: Obsidian Vault の構造（works・PARA・共有とローカルの分離）
status: active
tags:
  - tool/obsidian
  - knowledge-management
  - setup
aliases:
  - obsidian-vault-structure
triggers: [Vault の構造, works, PARA, resources, areas, projects, archives, 共有とローカル, 入れ子, clone, ジャンクション, .obsidian, 検索, ripgrep]
created: 2026-10-05
updated: 2026-10-27
sources:
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05)
---

# Obsidian Vault の構造（works・PARA・共有とローカルの分離）

全体の方針は [[obsidian-vault]]（2026-10-27 に、追記の節を切り出した）。

## Vault

### 現在の構造（2026-10-05）
<!-- 版依存: 一方向 / 確認: 2026-10-06 -->

2026-10-06 の変更: トップの名前を `notes` から `works` に改め（`C:\vault\works`、環境変数は `NOTES_DIR` から `WORKS_DIR`）、`C:\vault\certs` を `works\areas\dev-env\certs\`（`CERTS_DIR`）へ移すと決めた（同日のうちに、置き場を `$HOME\.certs` に変更した。[[obsidian-vault-rename]] の Decisions）。以下の図は `works` に直した。本文の `notes` は、2026-10-05 時点の名前のまま残す（旧 `notes` は、アーカイブ済みの GitHub リポジトリの呼称でもある）。根拠と却下案は、トップの `docs/decisions.md`。

2026-10-06 の第2の変更（同日の夕方）: トップを `C:\vault\works` から `$HOME\works`（Windows は `%USERPROFILE%\works`）へ移し、ghq の root を `$HOME\works\repos` にした。置き場は1つだけなので、親の `C:\vault` を畳んだ（ユーザーの決定）。以下の現在形の記述（図、環境変数、場所）は `$HOME\works` に直した。`C:\vault\works` と書かれた日付つきの履歴は、当時のパスのまま残す。Linux 側（WSL・ネイティブ）も `~/works`、`~/works/repos` にそろえた。この移動の原則・決定・事実・遭遇したことは、[[obsidian-vault-home-works]]にまとめた。

**現在の状態（確認: 2026-10-06、根拠: ユーザーの確認、起動したセッション、dotfiles の試験）**: 環境変数は `WORKS_DIR=%USERPROFILE%\works`、`GHQ_ROOT=%WORKS_DIR%\repos`、`CERTS_DIR` は `%USERPROFILE%\.certs`（`VAULT_HOME` は廃止。`NOTES_DIR` は未設定）。Obsidian と Claude Code は、新しい場所で動いた。`.obsidian` は dotfiles へのジャンクション。WSL へは `WSLENV` の `WORKS_DIR/p` で渡す設計だが、実機の WSL では渡っていなかった（確認: 2026-10-06、[[obsidian-vault-home-works]]の Facts）。dotfiles の Linux の試験は 51/51 合格（再実行で再確認: 2026-10-06）。未了は、Claude Code の旧セッションの `--resume` が新パスで通らないこと（`cwd` の書き換えだけでは足りなかった。原因は未特定。[[claude-code-storage]]）。旧 `C:\vault`（旧 clone とバックアップ）は、この `--resume` の試験のために、削除せずに残している（ユーザーの指示）。rename の判断・原則・遭遇したことは、[[obsidian-vault-rename]]にまとめた。
2026-10-05 に、2026-10-02 に決めた目標の構造から変更した。経緯は、下の「過去の構造」と、Decisions の「撤回済み」の注記に残す。

```text
$HOME\works\           # PC ごとのローカルなリポジトリ（実ディレクトリ。ジャンクションではない）
├── .gitignore / .ignore / AGENTS.md / CLAUDE.md / docs/
├── .obsidian/         # dotfiles へのジャンクション（実体は dotfiles の windows\obsidian\.obsidian）
├── projects/  areas/  archives/   # ローカルの PARA
└── resources/         # 共有リポジトリ workbase の clone（別リポジトリ）
    ├── exmem/  workflow-kit/  guides/  handson/
```

- Vault のトップは、PC ごとのローカルなリポジトリ（業務用 PC は remote なし、個人用 PC は非公開 remote を使える）。`areas/` `projects/` `archives/`、`docs/`（作業ログ）、PC 用の `AGENTS.md` を持つ。作り方は、`workflow-kit` の導入フック（項目 5「ワークスペースの生成」）。
- `resources/` は、共有リポジトリ `workbase`（GitHub: `yuzucha16/workbase`、非公開。公開範囲は未定）を、**直接 `git clone` したもの**（ghq の管理外。ジャンクションにしない）。トップの `.gitignore` が除外する。`workbase` は、単独で clone しても自己完結する（Vault のローカル側を知らない）。
- `.obsidian/` の実体は dotfiles。トップへジャンクションで張る。`workspace*.json` は追跡しない。
- 変更の理由: 業務用 PC で、ローカルの作業もコミットしたい。共有（GitHub）とローカルを、1つの作業ツリーに混ぜられない。1つのリポジトリの作業ツリーは連続している必要があり、入れ子の `.git` の中は、外側のリポジトリから追跡できない。共有側がローカルの存在を知らない構成にして、共有側を汎用ナレッジとして育てられるようにした。境界の数は、公開範囲の種類（共有 / PC ローカル / 設定）に合わせた。
- 却下案: 1つの作業ツリーに2つの git を重ねる（ルートの `.gitignore` が両方に効き、片方は `git add -f` 前提になる）、共有リポジトリをトップに置いて `company/` を入れ子にする（共有側がローカルの存在を知る）、トップをリポジトリにしない（`AGENTS.md` と `docs/` の持ち主がいない）、`resources/` を ghq の位置に置いてジャンクションで出す（下の検索の項）。
- 検索（確認: 2026-10-05）: ripgrep（Claude Code の Grep を含む）は `.gitignore` を尊重するので、トップの `.gitignore` が除外する `resources/` は、検索から黙って外れる。トップの `.ignore` に `!/resources/` を置くと含まれる。ジャンクション越しのディレクトリは、Grep / Glob / `rg`（既定）が辿らない（`rg --follow` なら辿る）。
- `fonts/` `wallpapers/` `_archive/` は、履歴ごと削除した（LFS も不要になった）。`office/` は dotfiles（`windows/office/`）へ移した。ローカル専用の `_local/` は廃止した。切り出しの手順は [[git-subdirectory-split]]。
- GitHub 側は `workbase` を新設し、旧 `notes` はアーカイブにした。根拠: `notes` が共有部分を表す名前でなくなった。履歴（`.obsidian`、PARA の経緯）が旧リポジトリに残る。却下案: `notes` を別の名前に改名して履歴を書き換えて push する（リスクが高い）。
- `.obsidian` の実体を dotfiles に置く判断（2026-10-03 の「`notes` へ移す」と、2026-10-04 の「`notes` に置き続ける」の撤回）の根拠: トップは PC 間で共有されないので、トップに置くと設定が PC ごとに別管理になる。dotfiles は全 PC に clone する。「同じ公開範囲は同じリポジトリ」とも合う。
- 新しい構成（実ディレクトリの入れ子の clone と、`.obsidian` のジャンクション）で、Obsidian は問題なく動いた（確認: 2026-10-05、根拠: ユーザーの発言「Obsidian の実機確認：OKです」）。
- 旧トップ（ジャンクションだった `C:\vault\notes`）を実ディレクトリに替えるとき、ジャンクションは `rmdir` でリンクだけが消え、実体（旧リポジトリ）は無傷だった（確認: 2026-10-05、根拠: 直後の `.git` の存在確認）。
- Claude Code のチャット履歴とメモリは、作業ディレクトリごとのキー（パスを変換した名前）で保存される。作業ディレクトリを移すと、新しいパスは別のキーになる。前のチャットの再開は、旧パスで開いて行う（確認: 2026-10-05、根拠: `~/.claude/projects` の一覧が、パスごとに別のディレクトリ。新しいパスで開いたときの一覧は未実施で、仮説。[[claude-code-storage]]）。

#### 設計の原則（リポジトリの境界。2026-10-05）

- git の境界と、AI に見せる範囲は別物。AI が見える範囲は、起動したディレクトリ（cwd）と権限設定で決まり、git の追跡では決まらない。追跡しないことと、AI から隠すことを混同すると、境界の設計を誤る。
- 1つのリポジトリの作業ツリーは連続していて、リポジトリのルートの中に、外側の別リポジトリが追跡するファイルは置けない（入れ子の `.git` は、外側から不透明）。「共有リポジトリの中の非共有の区画」を、別のリポジトリでは追跡できない。
- リポジトリの分け方は、「どこへ push するか」（公開範囲の種類）で決める。同じ公開範囲のものは同じリポジトリに置く。境界が多いほど、clone、push、コミットの分離といった運用が増える。検討の途中で、用途（業務 PC でローカルの作業もコミットしたい）が分かり、判断の軸が「AI に見せる境界」から「push 先の分離」に変わった。構造変更の検討は、案を列挙する前に用途を確認する（[[human-ai-decision-loop]]）。
- 共有側は、ローカル側の存在を知らない（一方向の依存）。検査は「共有側を単独で clone して、リンク切れや参照切れが無いか」。共有側を汎用の知識として育てるとき、ローカルの事情が混ざらない。
- 誤 push の防止は、ルール（ignore の書き方）でなく、構造で保証する。remote を持たないリポジトリには push できない。ignore の1行の間違いで、共有側に漏れる設計を避ける。
- 構造を変えるときは、旧環境の全ファイルを棚卸しして、引き継ぐか捨てるかを1つずつ決める。新しい構成を雛形から作ると、旧環境が暗黙に持っていた設定（改行コードの設定など）が落ちる（[[obsidian-vault-rename]] の Gotchas）。

### 過去の構造（2026-10-01〜05。畳んだ）

- 2026-10-15 に、今の構造に置き換わった4つの節（目標の構造 2026-10-02、移行の状況 2026-10-03、dotfiles との関係 2026-10-03、移行前の構造 2026-10-01）を畳んだ。全文は git の履歴にある（畳む前のコミット `33e9fe3`。`git show 33e9fe3:exmem/lessons/obsidian-vault.md`）。
- 要点: 2026-10-01 は `.obsidian` と `areas_shared` がジャンクションで、Git の管理境界が `notes`（管理外）・`areas_shared`・dotfiles の3つに分かれていた。2026-10-02 に、Vault のルートを1つの Git リポジトリ（`notes`。共有は `resources/` と `.obsidian/` だけ）にする目標を決めた。2026-10-05 に、上の「現在の構造」（共有の `workbase` と、PC ローカルの Vault の分離）へ変えた。
- **撤回済み（2026-10-05）**: `.obsidian` を `notes` に置き続ける決定（2026-10-04）は撤回し、dotfiles へ戻した。理由は [[app-config-placement]] の Decisions。

## 切り出したノート

- [[obsidian-vault-rename]]: `notes` → `works` の rename と旧名の扱い、`certs` の置き場（2026-10-06）
- [[obsidian-vault-home-works]]: 置き場を `$HOME\works` へ移した件、旧 `notes` リポジトリの削除（未決）（2026-10-06）

## Related

- [[obsidian-vault]]
