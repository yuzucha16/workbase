---
type: howto
title: room から非公開リポジトリを読む（読み取り専用 deploy key）
tags:
  - setup
  - security
  - tool/ssh
  - tool/gh
  - tool/wsl
---

# room から非公開リポジトリを読む（読み取り専用 deploy key）

AI 作業部屋（room）の中から、GitHub の非公開リポジトリを `git clone` できるようにし、`git push` は拒否されるようにする手順書。リポジトリ 1 つにつき deploy key を 1 つ作り、read only で登録する。仕組みと理由は [[ai-room-why]]、room の作り方は [[ai-room-setup]]。

- **ゴール（完了の目安）**: room の中で `git clone git@<別名>:<owner>/<repo>.git` が通り、同じ clone からの `git push` が `marked as read only` で拒否される
- **確認状況**: 2026-10-31 に、AI が実機で通した。同日、ユーザーが章4（指紋の一致）と章5（`read_only` の確認）を手で確かめた。章6 以降を手でやり直した結果は未反映（やってみて直した点は、この手順書に足す）
- **範囲**: 鍵の作成、`~/.ssh/config`、known_hosts、GitHub への登録、clone と push の確認、片付け。room の作成は範囲外
- **push を許さない理由**: room の AI にリポジトリを書き換えさせない。個人開発で push が要る場面が出たら、書き込み可の deploy key をリポジトリごとに足す（決定の根拠は `topics/room-type-consolidation/docs/decisions.md`）
- 名前は `<Area>`（部屋は `room-<Area>`）、`<owner>`、`<repo>`、`<別名>` のプレースホルダーで書く。自分の値に置き換えて読む

## 対応バージョン表

手順の確認日: 2026-10-31（実機）。

| 項目 | 確認した版 | 備考 |
|---|---|---|
| WSL / room のベース | Ubuntu 26.04 | 版は [[ai-room-setup]] の対応バージョン表を正とする |
| ホストの `gh` | ログイン済み | 要確認: 必要な権限（リポジトリの作成、deploy key の登録）。削除は `delete_repo` が別に要る |
| 鍵の種類 | ed25519 | 推奨 |
| GitHub の SSH 指紋 | `gh api meta` の `ssh_key_fingerprints` | 公式ドキュメント「GitHub's SSH key fingerprints」でも確認できる。値は書かない（変わりうる） |

## 全体の流れ

| 章 | 場所 | 内容 | 完了の目安 |
|---|---|---|---|
| 1 | ホスト | 前提を確認する | `gh auth status` が通る |
| 2 | ホスト | 練習用の空の非公開リポジトリを作る | リポジトリが GitHub に出る |
| 3 | room | 鍵を作る | 秘密鍵の権限が `600` |
| 4 | room | `~/.ssh/config` と known_hosts を整える | 指紋が公式の値と一致 |
| 5 | ホスト | 公開鍵を deploy key（read only）で登録する | 登録した鍵の一覧に出る |
| 6 | room | clone と push を確認する | clone 成功、push 拒否 |
| 7 | 両方 | 片付ける | 鍵、clone、練習用リポジトリが消えた |
| 8 | | うまくいかないとき | |

## 判断の分かれ目

| 選択肢 | 使う場面 | 状態 |
|---|---|---|
| リポジトリ単位の deploy key（read only） | room から 1 リポジトリを読む | 推奨（この手順書） |
| fine-grained PAT | 複数リポジトリを 1 つの認証で扱いたい | deploy key で足りなくなったら再検討 |
| ホストの `gh` のトークンを room に渡す | — | 使わない。AI から全リポジトリに書けてしまう |

## 1. 前提を確認する（ホスト）

```powershell
gh auth status          # ログイン済みであること
wsl -l -v               # room-<Area> があり、VERSION が 2
```

- 実リポジトリで試す場合も、この手順は同じ。ただし最初は練習用の空のリポジトリで通すほうが安全

## 2. 練習用の空の非公開リポジトリを作る（ホスト）

```powershell
gh repo create <owner>/<repo> --private
```

- 実リポジトリを読みたいだけなら、この章は飛ばす

## 3. 鍵を作る（room）

room の中に入る（`ai` ユーザー）。

```powershell
wsl -d room-<Area> -u ai
```

room の中で:

```sh
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_<別名> -N "" -C "room-<Area> <repo> read-only"
ls -l ~/.ssh/id_<別名>        # -rw------- (600) であること
```

- `-N ""` はパスフレーズなし。room の中の AI が使えるようにするため。その代わり、鍵は read only で 1 リポジトリ限りにする
- 鍵の名前に `<別名>` を入れる。複数のリポジトリを足したとき、取り違えない

**完了の目安**: `ls -l` の先頭が `-rw-------`。

## 4. `~/.ssh/config` と known_hosts を整える（room）

`~/.ssh/config` に別名を書く。

```sh
cat >> ~/.ssh/config <<'EOF'
Host <別名>
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_<別名>
  IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
```

- `IdentitiesOnly yes` を必ず付ける。付けないと、ほかの鍵を試して、意図しない鍵で認証される
- `<別名>` を使う理由: 同じ `github.com` に別のリポジトリ用の鍵を足せる

GitHub のホスト鍵を取り、指紋を見てから採用する。

```sh
ssh-keyscan -t ed25519 github.com > /tmp/gh_hostkey
ssh-keygen -lf /tmp/gh_hostkey        # 例: 256 SHA256:xxxx… github.com (ED25519)
```

`/tmp/gh_hostkey` は公開鍵そのもので、指紋は入っていない。比べるのは、コンソールに出た `SHA256:…` の部分。公式の値は、ホストの `gh api`（HTTPS で取るので、SSH の経路とは独立）で取る。

```powershell
gh api meta --jq '.ssh_key_fingerprints'     # SHA256_ED25519 の値と比べる
```

- 比べるのは **ED25519** の値で、**SHA256** 形式（`SHA256:` で始まる）。RSA / ECDSA の行や MD5 形式（`xx:xx:…`）と比べると、不一致になる
- **一致したときだけ**次へ進む。一致しないなら中断する（中間者攻撃の可能性。ネットワークを変えて再取得）

```sh
cat /tmp/gh_hostkey >> ~/.ssh/known_hosts
rm /tmp/gh_hostkey
```

**完了の目安**: コンソールの `SHA256:…` が、`gh api meta` の ED25519 の値と一致した。

## 5. 公開鍵を deploy key（read only）で登録する（ホスト）

公開鍵を room からホストに取り出す。

```powershell
wsl -d room-<Area> -u ai -- cat '~/.ssh/id_<別名>.pub' | Set-Content "$env:TEMP\id_room.pub"
gh repo deploy-key add "$env:TEMP\id_room.pub" -R <owner>/<repo> -t "room-<Area> read-only"
Remove-Item "$env:TEMP\id_room.pub"
gh api repos/<owner>/<repo>/keys --jq '.[] | {title, read_only}'
```

- `gh repo deploy-key add` は、`--allow-write` を付けない限り read only で登録される。**付けない**
- 登録するのは公開鍵（`.pub`）。秘密鍵は room の外に出さない

**完了の目安**: `gh api` の出力で、`room-<Area> read-only` の `read_only` が `true`。最終の確認は章6の push の拒否。

## 6. clone と push を確認する（room）

```sh
cd ~ && mkdir -p src && cd src
git clone <別名>:<owner>/<repo>.git
```

- 初回は `Are you sure you want to continue connecting` が出ないこと（出るなら章 4 の known_hosts が入っていない）
- 空のリポジトリだと `You appear to have cloned an empty repository` と出る。正常

push が拒否されることを確かめる。

```sh
cd <repo>
git commit --allow-empty -m "test"
git push origin HEAD
```

**完了の目安**: clone が成功し、push が `The key you are authenticating with has been marked as read only` で失敗する。

## 7. 片付ける

練習で作ったものを消す。

room の中:

```sh
rm -rf ~/src/<repo> ~/.ssh/id_<別名> ~/.ssh/id_<別名>.pub
# ~/.ssh/config の Host <別名> のブロックと、known_hosts の github.com の行も、不要なら消す
```

ホスト（練習用リポジトリを消す場合）:

```powershell
gh repo delete <owner>/<repo> --yes
```

- `gh repo delete` には `delete_repo` の権限が要る。無いと失敗する。`gh auth refresh -h github.com -s delete_repo` で足すか、GitHub の画面（Settings → Danger Zone）で消す
- 実リポジトリは消さない。deploy key だけ消すなら `gh repo deploy-key delete <key-id> -R <owner>/<repo>`

## 8. うまくいかないとき

| 症状 | 確認すること |
|---|---|
| `Permission denied (publickey)` | 別名の `IdentityFile` のパス、`IdentitiesOnly yes`、章 5 で登録した鍵と room の鍵が同じか（`ssh-keygen -lf ~/.ssh/id_<別名>.pub` と登録済みの指紋を比べる） |
| `Host key verification failed` | known_hosts に github.com が無い、または古い。章 4 をやり直す |
| clone で `Repository not found` | 別名の `<owner>/<repo>` の綴り、deploy key を登録したリポジトリが違う |
| `Bad permissions` / 鍵が無視される | `chmod 600 ~/.ssh/id_<別名> ~/.ssh/config`、`chmod 700 ~/.ssh` |
| `wsl.exe … sh -s` にスクリプトを渡すと `\r: command not found` | PowerShell の here-string は CRLF。渡す前に `\r\n` を `\n` に置換する |
| `gh repo delete` が権限エラー | 章 7 の `delete_repo` の注意 |

## よく忘れる点

- 指紋の照合を飛ばさない（飛ばすと、偽のホストに秘密を渡しうる）
- `--allow-write` を付けない（付けると read only でなくなる）
- 秘密鍵は room の中だけに置く。ホストの `~/.ssh` やリポジトリにコピーしない
- 手順書に鍵、トークン、自分の `<owner>` の実値を書かない
