---
type: knowledge
title: Obsidian Vault の置き場を $HOME\works へ移す
status: active
tags:
  - tool/obsidian
  - knowledge-management
  - setup
aliases:
  - obsidian-vault-home-works
triggers: [C:\vault, USERPROFILE, ホーム基準, ghq root, GHQ_ROOT, WSLENV, WORKS_DIR, 置き場の移動, 旧 notes リポジトリ, 削除, bundle]
created: 2026-10-06
updated: 2026-10-27
sources:
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05)
---

# Obsidian Vault の置き場を $HOME\works へ移す

全体の方針は [[obsidian-vault-structure]]（Vault の構造）。2026-10-27 に、obsidian-vault-structure から切り出した。

`C:\vault\works` から `%USERPROFILE%\works` へ移し、Windows・WSL・ネイティブ Linux で並び（`works/` と `works/repos/`）をそろえた。

**Principles**

- 作業の置き場は、固定の絶対パスではなく、ホーム基準（`%USERPROFILE%` / `$HOME`）にする。理由: 置き場を1つしか持たないなら、固定の親ディレクトリは要らず、ユーザー名を含むパスを文書やスクリプトに直書きせずに済む。
- OS ごとに置き場の名前と並びをそろえる（`works/`、その下に `repos/`）。理由: 手順書とスクリプトの分岐が減り、どの OS でも同じ言い方で説明できる。
- Windows のパスを WSL に渡すときは、パスを組み立てずに、環境変数を `WSLENV` の `/p` 付きで渡す（[[obsidian-vault-rename]] の Principles と同じ。理由: WSL のユーザー名は Windows と違うことがある。この PC は Windows と WSL で実際に違った）。

**Decisions**（すべて 2026-10-06）

- **作業の置き場（Vault のトップ）を `C:\vault\works` から `%USERPROFILE%\works` に移し、ghq の root を `%USERPROFILE%\works\repos` にする**。根拠: 置き場は1つだけで、親の `C:\vault` が要らない（ユーザーの決定）。却下案: 未検討（承認のみ）。
- **Linux 側も `~/works`、ghq の root を `~/works/repos` にする。WSL の ghq の root は、Windows 側を共有せず、WSL 自身の `~/works/repos` に置く**。根拠: 対称性のため（ユーザーの指示）。WSL の git を `/mnt/c` に置かないのは、`.profile` の既存の設計（遅いため）をそのまま維持した。却下案: 未検討（承認のみ）。
- **旧 `C:\vault` は、削除せずに残す**（2026-10-27 にユーザーが削除した。この項は履歴）。根拠: `claude --resume` で旧セッションを復活できるかの試験に、旧パスの実体と履歴を使うため（ユーザーの指示。過去に成功した例が無い）。却下案: 未検討（承認のみ）。

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

## Related

- [[obsidian-vault-structure]]
- [[obsidian-vault-rename]]
