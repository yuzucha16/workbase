---
type: explain
title: WSL で Windows 側の bash 用 shim が動いて壊れる仕組み
tags:
  - tool/wsl
  - tool/volta
  - path
  - interop
triggers: [volta: command not found, WSL node, command not found, appendWindowsPath, interop, shim, Windows の PATH, /mnt/c, node が壊れる, npm が動かない]
---

# WSL で Windows 側の bash 用 shim が動いて壊れる仕組み

## 冒頭
WSL で `node` や `npm` が `volta: command not found` で失敗する理由を、自分で説明できるようにする。前提: Windows に Volta（scoop 経由）が入り、WSL の Ubuntu には node も Volta も入れていない。確認状況: 実機で PATH、shim の中身、該当ファイルの一覧を確認した（下に日付と根拠）。

## ダイジェスト
- 状況: Ubuntu で `node` を呼ぶと `volta: command not found` になる。Ubuntu に node は入れていない。
- 原因: WSL は Windows の PATH を Linux の PATH の後ろに足す（`appendWindowsPath`、既定で有効）。その中に、Volta が置いた拡張子なしの `node`（`#!/bin/bash` で始まるシェルスクリプト）があり、Linux の bash がそれをそのまま実行する。中の `volta` は Ubuntu の PATH から探されるので見つからない。
- 解決: Ubuntu に node を入れる（Linux 側が PATH の先に来て勝つ）か、`/etc/wsl.conf` の `[interop]` に `appendWindowsPath=false` を書く。使わないなら放置でよい。

## 基礎知識
- 用語: interop は、WSL から Windows の exe を呼べる仕組み。PATH の共有は、Windows の PATH を `/mnt/c/...` の形で Linux の PATH の後ろに足す設定。
- Linux は実行ファイルを、拡張子ではなく名前の完全一致で PATH から探す。`node` と打つと、`node.exe` ではなく、拡張子なしの `node` が候補になる。`/mnt/c` 配下は全ファイルが実行可能に見える。
- 実行の分かれ方: `.exe` を見つけたときは Windows 側で動く（interop）。拡張子なしのファイルで `#!/bin/bash` 始まりなら、Ubuntu の bash が実行する。スクリプトの中のコマンドは、Ubuntu の PATH から探される。
- Volta の `bin/` には、`node.exe`、`node.cmd`、`node`（43 バイトのスクリプト）が並ぶ。スクリプトは Git Bash などの Windows 上の bash 向けで、中身は `volta run "$(basename $0)" "$@"`（確認: 2026-11-07、根拠: ファイルを開いて確認）。
- 自分で説明するときの一言: 「WSL は Windows の PATH も見る。そこにある bash 用の `node` スクリプトを Ubuntu の bash が動かし、中の `volta` が Ubuntu に無くて失敗する」

## チェックリスト
| 症状 | 原因 | 対処 |
|---|---|---|
| `node`、`npm`、`pnpm`、`yarn` が `volta: command not found` | Windows 側 Volta の bash 用 shim が Ubuntu の bash で動いた | Ubuntu に node を入れる、または `appendWindowsPath=false` |
| `node.exe` と打つと動く | `.exe` は interop で Windows 側が動く | 区別したいときは拡張子を付けて呼ぶ |
| Ubuntu に入れていないコマンドで、見覚えのない失敗が出る | Windows の PATH に同名のスクリプトがある | `command -v 名前` で解決先が `/mnt/c` か確認する |
| `appendWindowsPath=false` にした後、`code` や `pwsh` が呼べない | Windows の PATH が見えなくなった | フルパスで呼ぶ。または元に戻す |

## 補足
同じ形になりうるものの調べ方: Ubuntu から見える Windows 側の PATH（`/mnt/c/...`）で、拡張子なしの `#!` 始まりのファイルを探す。この環境で見つかったもの（確認: 2026-11-07、根拠: 走査スクリプトの出力）:

| 場所 | 対象 | 影響 |
|---|---|---|
| Volta の `bin/` | `node`、`npm`、`npx`、`pnpm`、`yarn`、`defuddle`（グローバルパッケージの shim） | `volta` が無く失敗する |
| Volta の node 本体のフォルダ | `corepack`、`npm`、`npx` | PATH にこのフォルダが入っているため見える |
| scoop の `shims/` | `scoop`、`sudo` | `/usr/bin` が先なので Linux の `sudo` が勝つ。`scoop` は無意味 |

`uv` は `.local/bin` に `.exe` だけがあり、スクリプトは無いので踏まない。パッケージ管理系の CLI（Volta、scoop など）は、bash 用の shim を PATH に置くことがあるので、同じ形になりやすい。

## 要確認事項
- node 本体のフォルダの `npm`、`npx` を Ubuntu で実行したときの失敗の仕方は、実行して確かめていない（仮説）。
- `appendWindowsPath=false` にしたときの副作用を、この環境では試していない。
