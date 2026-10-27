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
triggers: [Vault の構造, works, PARA, resources, areas, projects, archives, 共有とローカル, rename, certs]
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

2026-10-06 の変更: トップの名前を `notes` から `works` に改め（`C:\vault\works`、環境変数は `NOTES_DIR` から `WORKS_DIR`）、`C:\vault\certs` を `works\areas\dev-env\certs\`（`CERTS_DIR`）へ移すと決めた（同日のうちに、置き場を `$HOME\.certs` に変更した。下の「rename と旧名の扱い」の Decisions）。以下の図は `works` に直した。本文の `notes` は、2026-10-05 時点の名前のまま残す（旧 `notes` は、アーカイブ済みの GitHub リポジトリの呼称でもある）。根拠と却下案は、トップの `docs/decisions.md`。

2026-10-06 の第2の変更（同日の夕方）: トップを `C:\vault\works` から `$HOME\works`（Windows は `%USERPROFILE%\works`）へ移し、ghq の root を `$HOME\works\repos` にした。置き場は1つだけなので、親の `C:\vault` を畳んだ（ユーザーの決定）。以下の現在形の記述（図、環境変数、場所）は `$HOME\works` に直した。`C:\vault\works` と書かれた日付つきの履歴は、当時のパスのまま残す。Linux 側（WSL・ネイティブ）も `~/works`、`~/works/repos` にそろえた。この移動の原則・決定・事実・遭遇したことは、下の「置き場を `$HOME\works` へ移す」にまとめた。

**現在の状態（確認: 2026-10-06、根拠: ユーザーの確認、起動したセッション、dotfiles の試験）**: 環境変数は `WORKS_DIR=%USERPROFILE%\works`、`GHQ_ROOT=%WORKS_DIR%\repos`、`CERTS_DIR` は `%USERPROFILE%\.certs`（`VAULT_HOME` は廃止。`NOTES_DIR` は未設定）。Obsidian と Claude Code は、新しい場所で動いた。`.obsidian` は dotfiles へのジャンクション。WSL へは `WSLENV` の `WORKS_DIR/p` で渡す設計だが、実機の WSL では渡っていなかった（確認: 2026-10-06、下の「置き場を `$HOME\works` へ移す」の Facts）。dotfiles の Linux の試験は 51/51 合格（再実行で再確認: 2026-10-06）。未了は、Claude Code の旧セッションの `--resume` が新パスで通らないこと（`cwd` の書き換えだけでは足りなかった。原因は未特定。[[claude-code-storage]]）。旧 `C:\vault`（旧 clone とバックアップ）は、この `--resume` の試験のために、削除せずに残している（ユーザーの指示）。rename の判断・原則・遭遇したことは、下の「rename と旧名の扱い」にまとめた。
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
- 構造を変えるときは、旧環境の全ファイルを棚卸しして、引き継ぐか捨てるかを1つずつ決める。新しい構成を雛形から作ると、旧環境が暗黙に持っていた設定（改行コードの設定など）が落ちる（下の Gotchas）。

#### rename と旧名の扱い（2026-10-06）

トップの `notes` → `works` の rename と、`certs` の移動から得た教訓。名前そのものより、進め方を残す。

**Principles**

- ディレクトリの rename は、リポジトリの中の文字列と、パスをキーや登録に持つ外の状態（アプリの Vault 登録、Claude Code の履歴、環境変数）を分けて棚卸しする。前者は置換で済むが、後者は壊れても気づきにくい。
- 旧名は、記述の時制で扱いを分ける。現在形の記述（いまの置き場、既定値、構造の図、Next Actions）は新名に直し、日付つきの履歴は書き換えない。AI は現在形の記述を事実として読んで動くので、そこに残る旧名が最も害になる。履歴の旧名は「いつの時点の何か」の目印で、消すと記録が壊れる。
- 旧名の全面置換はしない。旧名が別のもの（アーカイブ済みの GitHub リポジトリ、旧 clone、バックアップ）の名前も兼ねていて、機械置換すると存在しない名前が生まれる。`notes` は 28 ファイルで 205 件ヒットし、機械置換はできなかった。
- ナレッジに残すのは名前ではなく教訓。rename の経緯は日付つきの短い1行にとどめる。次の rename でナレッジを書き換えずに済む。
- 認証系ファイルの置き場は、「どの経路に乗るか」（push、バックアップ、AI の検索、同期）で選ぶ。公開情報の CA 証明書は置けても、秘密鍵は経路のどれかで漏れ得るので、Vault に入れない。
- ツールが固定パスで読む資産は、環境変数越しに参照する。置き場を変えても、直す箇所が変数の定義だけになる。
- PC ローカルの認証系ファイル（社内 CA 証明書など）は、ワークスペースの構造に依存しない `$HOME` 直下に置く。構成が変わっても参照が壊れず、リポジトリの外なので共有の経路も `.gitignore` の除外行も要らない。
- Windows のパスを WSL へ渡すときは、`/mnt/c/...` を直書きせず、環境変数と `WSLENV` の `/p` を使う。ユーザー名や配置の直書きを避けられ、Windows 側の1か所の定義が正本になる。Windows と WSL で同じ値を使うものは、環境変数を共通の窓口にし、未設定のときの既定値を `common.sh` 側に持たせる。
- アプリの履歴を新パスのキーへ移すときは、旧キーを消さず、コピーで行う。再開できる保証がなく、旧キーが唯一の確実な履歴になる。
- 作業ディレクトリの rename は、そのディレクトリを cwd にするアプリとセッションをすべて閉じた、別のシェルから行う。使用中のディレクトリは、Windows が名前変更を拒否する。
- 共有リポジトリの固定パスを変える変更は、他の PC に波及する（未移行の PC では、共有側の `AGENTS.md` のパスが存在しなくなる）。展開の方針（この PC だけ、橋渡しのジャンクション、全 PC 同時）を、実施の前に決める。

**Decisions**（すべて 2026-10-06）

- **トップを `notes` から `works` に rename する**。根拠: 役割が、ノートではなく、業務と個人開発のデータ構造（PARA）になっていて、名前が体を表していなかった。却下案: `notes` のまま。
- **環境変数 `NOTES_DIR` を `WORKS_DIR` に改名する**。根拠: rename の目的と合わせる。却下案: `NOTES_DIR` のまま（名前だけが古く残る）。
- **`certs` を `works\areas\dev-env\certs\` に移す。置くのは CA 証明書だけ**（同日のうちに、下の「置き場を `$HOME\.certs` に変える」で置き換えた。以下は履歴）。根拠: 勤務先固有の CA 証明書はローカルの情報で、共有の `resources/` には置けない。継続して維持するものは `areas/` が合い、Area は責任領域の名前にするので `areas/dev-env/` の下にした。却下案: `areas/certs/`（環境の設定が増えると名前が合わなくなる）、`areas/` に SSH の秘密鍵まで集約、`C:\vault\certs` のまま。
- **社内 CA 証明書の置き場を `$HOME\.certs`（Windows は `%USERPROFILE%\.certs`）に変える。WSL へは `WSLENV` の `CERTS_DIR/p` で渡し、WSL 側は `${CERTS_DIR:-$HOME/.certs}` を読む。環境変数 `CERTS_DIR` は残し、ディレクトリは `SSH_DIR` と同じ扱いで環境構築のスクリプト（`10_env.bat`）が作る**（2026-10-06。上の `areas/dev-env/certs` を置き換えた）。根拠: ユーザーの指示。ワークスペースの構造に依存させない。リポジトリの外なので、誤って共有する経路も、`.gitignore` の除外行も要らない。以前の置き場は、`/mnt/c` の直読みで WSL との二重管理を避けるためだけの選択だった（ユーザーの発言）。今後も WSL へは環境変数で寄せていく方針（ユーザーの発言）。却下案: 現状維持、WSL にも `~/.certs` を置く（2か所管理）、`wslpath` で求める（シェルの起動が遅くなる）、環境変数をやめて固定パスにする（参照側の変更が要る）。ワークスペースの `.gitignore` の雛形からは `/areas/dev-env/certs/` を除いた（kit 版 `2026-10-06.15`）。
- **展開はこの PC だけ。他の PC は導入前なので、新規扱いで始める**。却下案: 橋渡しのジャンクション（`works` → `notes`）、全 PC の同時移行（どちらも、移行済みの PC が無いので不要）。
- **旧名の扱いは時制で分ける**（上の Principles）。ユーザーは「rename 自体は重要でないので全削除でもよい」と考えていたが、整合が取れなくなる懸念も挙げ、現在形だけ直す折衷を選んだ。

**Facts**

- この Vault の `areas/` と `resources/` の区別は、PARA の意味（責任領域か参考資料か）ではなく、共有かローカルかで決まっている（確認: 2026-10-06、根拠: トップの `AGENTS.md` の構成の表）。
- 旧 `C:\vault\certs` は空で、参照は PowerShell のプロファイルが `CERTS_DIR` 経由、WSL 側の `common.sh` が絶対パスの直書きだった。
- Obsidian のレジストリ（`%APPDATA%\obsidian\obsidian.json`）は、Vault のパスをそのまま持つ。Obsidian Sync の紐付けと `workspace.json` が、パスが変わっても保たれるかは未確認。
- 旧 `notes` の完全な履歴（58 コミット）は、GitHub、旧ローカル clone、バックアップ（`.git` を含む）の3か所にある。`workbase` は切り出し時に 30 コミットで、`.obsidian`、`_archive`、`office`、`fonts`、`wallpapers` の履歴を持たない（切り出しは [[git-subdirectory-split]]）。
- 旧ローカル clone は、未 push 0、stash 0、未追跡ファイルは inbox のメモ1件。このメモの内容は統合先に入っているように見える（仮説。全文の突き合わせは未実施）。
- dotfiles のコードと共有リポジトリのノートに、旧 GitHub リポジトリの URL への依存は無い（URL は日付つきの記述だけ）。
- Vault のバックアップを定期実行するタスクは、タスクスケジューラに見当たらない（2026-10-06 に再確認。`Backup` などは Windows 標準のもの）。手でコピーしたバックアップが、同じディスク上に1つあるだけ。
- rename の確認に使ったスクリプトの事前確認は、`git status --short --untracked-files=no`。未追跡の inbox のメモ（規則でコミットしない）で止まらないため。

**Gotchas**

- 履歴が再開できず、ディレクトリ名だけを元に戻したら、環境変数と Obsidian のレジストリが `works` のままで食い違った。環境変数とレジストリは、ディレクトリの名前を戻しても戻らない（別の状態）。仕上げのスクリプトで、ディレクトリを `works` に rename し直して揃えた。
- Claude Code の履歴をコピーして `--resume` が通らなかった件は [[claude-code-storage]] の Gotchas。

#### 置き場を `$HOME\works` へ移す（2026-10-06）

`C:\vault\works` から `%USERPROFILE%\works` へ移し、Windows・WSL・ネイティブ Linux で並び（`works/` と `works/repos/`）をそろえた。

**Principles**

- 作業の置き場は、固定の絶対パスではなく、ホーム基準（`%USERPROFILE%` / `$HOME`）にする。理由: 置き場を1つしか持たないなら、固定の親ディレクトリは要らず、ユーザー名を含むパスを文書やスクリプトに直書きせずに済む。
- OS ごとに置き場の名前と並びをそろえる（`works/`、その下に `repos/`）。理由: 手順書とスクリプトの分岐が減り、どの OS でも同じ言い方で説明できる。
- Windows のパスを WSL に渡すときは、パスを組み立てずに、環境変数を `WSLENV` の `/p` 付きで渡す（上の「rename と旧名の扱い」の Principles と同じ。理由: WSL のユーザー名は Windows と違うことがある。この PC は Windows と WSL で実際に違った）。

**Decisions**（すべて 2026-10-06）

- **作業の置き場（Vault のトップ）を `C:\vault\works` から `%USERPROFILE%\works` に移し、ghq の root を `%USERPROFILE%\works\repos` にする**。根拠: 置き場は1つだけで、親の `C:\vault` が要らない（ユーザーの決定）。却下案: 未検討（承認のみ）。
- **Linux 側も `~/works`、ghq の root を `~/works/repos` にする。WSL の ghq の root は、Windows 側を共有せず、WSL 自身の `~/works/repos` に置く**。根拠: 対称性のため（ユーザーの指示）。WSL の git を `/mnt/c` に置かないのは、`.profile` の既存の設計（遅いため）をそのまま維持した。却下案: 未検討（承認のみ）。
- **旧 `C:\vault` は、削除せずに残す**。根拠: `claude --resume` で旧セッションを復活できるかの試験に、旧パスの実体と履歴を使うため（ユーザーの指示。過去に成功した例が無い）。却下案: 未検討（承認のみ）。

**Facts**

- `WORKS_DIR` を `WSLENV` の `WORKS_DIR/p` で WSL に渡す実装は、一時ディレクトリと偽の HOME の試験でだけ確認していた。**実機では渡っていなかった**（確認: 2026-10-06、根拠: Windows 側で `WORKS_DIR=C:\Users\<Windows のユーザー名>\works`、`WSLENV=CERTS_DIR/p;WORKS_DIR/p` を確認したうえで、`wsl -e bash -c 'printenv WORKS_DIR CERTS_DIR'` が何も出さず rc=1。WSL 側の `WSLENV` は同じ値で見えている）。**原因は `WSLENV` の区切りが `;` だったこと**（確認: 2026-10-18、根拠: 同じ `WSLENV` の値で区切りだけを `;` と `:` に変えて `printenv` を比べた。`;` では何も渡らず、`:` では `/mnt/c/Users/<名前>/works` と `/mnt/c/Users/<名前>/.certs` が渡った）。`WSLENV` の区切りは `:` を使う（`;` は Windows の `PATH` の区切りで、`WSLENV` では効かない）。`10_env.bat` を `:` に直し、この PC の User の `WSLENV` を `CERTS_DIR/p:WORKS_DIR/p` に直して、`wsl --shutdown` の後に渡ることを確認した（確認: 2026-10-18、根拠: `printenv WORKS_DIR CERTS_DIR` が rc=0）。
- 渡らないときの `~/.profile` の既定値 `/mnt/c/Users/$USER/works` は外れる（確認: 2026-10-06、根拠: Ubuntu-24.04 のログインシェルが `WORKS_DIR=/mnt/c/Users/<WSL のユーザー名>/works` を返した。Windows のユーザー名とは違う）。
- この PC の WSL（Ubuntu-24.04）は、未移行（確認: 2026-10-06、根拠: `~/works` は無く、`GHQ_ROOT=/home/<WSL のユーザー名>/vault/repos`。`~/.profile` などは旧 `/mnt/c/vault/repos/…/dotfiles/home/` へのシンボリックリンク。`C:\vault` を残しているので、リンクは切れていない）。

**Gotchas**

- 状況: スクリプトの `ghq get` をコメントアウトしたあと、試験が `ghq` のスタブの呼び出しを期待したままで、2件失敗した。原因: スクリプトの変更時に、試験を回していなかった。解決: 試験を現状の仕様（`ghq` を呼ばない）に合わせて直した。

**旧 GitHub リポジトリ（`notes`）の削除（未決）**

- 切り出し元は、完全な履歴の保管場所として扱う。削除の前に、削除に依存しない形（`git bundle create <名前>.bundle --all`、`git bundle verify`）で、Vault のディスクの外にも複製する。切り出し先は、除外したパスの履歴を持たない。
- アーカイブは費用がかからず戻せる。削除は戻せない（GitHub が復元できる期間は、設定画面で確認する。仮説）。削除は急がず、前提の確認が済んでから、期限を決めて行う。
- 削除すると決めたら、順は「GitHub 側 → 復元期間が過ぎてから旧 clone → バックアップは最後」。削除したら、「旧 `notes` はアーカイブにした」の決定を撤回済みにして、旧 URL が無効になったことを1行足す（履歴の URL は書き換えない）。
- 旧 clone のディレクトリを消すと、そこを cwd にした `--resume` ができなくなる。Claude Code の旧キー（`…-yuzucha16-notes` 系統の4つ）は、GitHub 側の削除では影響を受けない。

### 過去の構造（2026-10-01〜05。畳んだ）

- 2026-10-15 に、今の構造に置き換わった4つの節（目標の構造 2026-10-02、移行の状況 2026-10-03、dotfiles との関係 2026-10-03、移行前の構造 2026-10-01）を畳んだ。全文は git の履歴にある（畳む前のコミット `33e9fe3`。`git show 33e9fe3:exmem/lessons/obsidian-vault.md`）。
- 要点: 2026-10-01 は `.obsidian` と `areas_shared` がジャンクションで、Git の管理境界が `notes`（管理外）・`areas_shared`・dotfiles の3つに分かれていた。2026-10-02 に、Vault のルートを1つの Git リポジトリ（`notes`。共有は `resources/` と `.obsidian/` だけ）にする目標を決めた。2026-10-05 に、上の「現在の構造」（共有の `workbase` と、PC ローカルの Vault の分離）へ変えた。
- **撤回済み（2026-10-05）**: `.obsidian` を `notes` に置き続ける決定（2026-10-04）は撤回し、dotfiles へ戻した。理由は [[app-config-placement]] の Decisions。

## Related

- [[obsidian-vault]]
