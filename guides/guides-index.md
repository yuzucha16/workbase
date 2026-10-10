---
type: index
title: guides の索引
tags:
  - knowledge-management
aliases:
  - guides
  - 手順書の索引
created: 2026-10-10
updated: 2026-10-10
---

# guides の索引

やりたいこと・場面から、見る文書を引く。`guides/` の入口。
文書の種類（手順書・理解ガイド・クイックリファレンス）の分け方と作り方は [[reference-doc-types]]。

## 場面から引く

### PC をセットアップする

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| Windows 11 を入れて、dotfiles のスクリプトまで通す | [[win11]] | 手順書 |
| Windows と Linux のマルチブートにする（Windows 側の準備） | [[win11#Linux とデュアルブートする場合]] | 手順書 |
| Debian 系 Linux（MX / Ubuntu / Mint）を入れて、dotfiles のスクリプトまで通す | [[debian-family]] | 手順書 |
| Linux の EFI・パーティション・起動メニュー・時計のずれ | [[debian-family]] の 2〜4 章 | 手順書 |
| Linux で SSH 鍵を作り、GitHub につなぐ | [[debian-family#10. SSH と GitHub]] | 手順書 |
| WSL2 / Ubuntu を入れる | [[win11#8. 任意設定]] | 手順書 |
| エディタ・ターミナルのフォント（PlemolJP）を入れる | [[fonts-setup]] | 手順書 |
| Claude Code の設定を PC に入れる・入れ替える | dotfiles の `windows/claude/README.md`（このリポジトリの外。スクリプトの隣に置く手順書） | 手順書 |

### エラー・困りごとを切り分ける

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| `SSL certificate problem` などの証明書エラーが出た（会社のプロキシ環境） | [[ssl-inspection#3. チェックリスト（症状 → 原因 → 対処）]] | 理解ガイド |
| ブラウザは通るのに git / WSL / docker / pip / npm だけ通らない | [[ssl-inspection]] | 理解ガイド |
| SSL インスペクションの仕組みを、自分で説明できるようにする | [[ssl-inspection#2. 理解のための基礎知識]] | 理解ガイド |

### コマンド・書き方を思い出す

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| パッケージを調べる・入れる・更新する・消す（Debian 系） | [[apt]] | クイックリファレンス |
| git の clone・commit・push・ブランチ・submodule・取り消し | [[git]] | クイックリファレンス |
| docker のイメージ・コンテナ、docker-compose の起動・ログ・停止 | [[docker]] | クイックリファレンス |
| シェルのプロセス・権限・ディレクトリ・シンボリックリンク・リダイレクト | [[shell]] | クイックリファレンス |
| SSH サーバーを入れる・設定する、クライアントの `~/.ssh/config` | [[ssh]] | クイックリファレンス |
| Markdown の記法（見出し・表・コードブロック・チェックボックス） | [[markdown]] | クイックリファレンス |

## 種類から引く

| 種類 | 読む人の問い | 文書 |
|---|---|---|
| 手順書（`howto/`） | どの順で何をやるんだっけ | [[win11]]、[[debian-family]]、[[fonts-setup]] |
| 理解ガイド（`explain/`） | なぜそうなる？ どう動いている？ | [[ssl-inspection]] |
| クイックリファレンス（`quickref/`） | あのコマンドは何だっけ | [[apt]]、[[git]]、[[docker]]、[[shell]]、[[ssh]]、[[markdown]] |

## この索引の更新

- `guides/` に文書を足したら、「場面から引く」に1行以上と、「種類から引く」の文書の欄に足す。消したら、両方から消す。
- 行は、やりたいこと・場面（読む人の言葉）で書く。ファイル名やコマンド名だけの行にしない。
- 場面に合う節が無ければ、節を足す。
