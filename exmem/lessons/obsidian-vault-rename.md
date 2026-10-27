---
type: knowledge
title: Obsidian Vault の rename と旧名の扱い（notes → works、certs の移動）
status: active
tags:
  - tool/obsidian
  - knowledge-management
  - setup
aliases:
  - obsidian-vault-rename
triggers: [rename, notes, works, 旧名, certs, 証明書, NOTES_DIR, WORKS_DIR, 置換, 履歴, Obsidian レジストリ, WSLENV]
created: 2026-10-06
updated: 2026-10-27
sources:
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05)
---

# Obsidian Vault の rename と旧名の扱い（notes → works、certs の移動）

全体の方針は [[obsidian-vault-structure]]（Vault の構造）。2026-10-27 に、obsidian-vault-structure から切り出した。

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
- **`certs` を `works\areas\dev-env\certs\` に移す。置くのは CA 証明書だけ**（同日のうちに、次の項目（`$HOME\.certs` に変える）で置き換えた。以下は履歴）。根拠: 勤務先固有の CA 証明書はローカルの情報で、共有の `resources/` には置けない。継続して維持するものは `areas/` が合い、Area は責任領域の名前にするので `areas/dev-env/` の下にした。却下案: `areas/certs/`（環境の設定が増えると名前が合わなくなる）、`areas/` に SSH の秘密鍵まで集約、`C:\vault\certs` のまま。
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

## Related

- [[obsidian-vault-structure]]
- [[obsidian-vault-home-works]]
