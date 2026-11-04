---
type: knowledge
title: ZedとWSLのファイル配置方針
status: active
tags:
  - tool/wsl
  - tool/zed
  - windows
  - setup
  - backup
aliases:
  - WSLのファイル配置
  - Windows側とWSL側の置き場所
triggers: [WSL, ファイル配置, Windows側, WSL側, 置き場所, /mnt/c, パフォーマンス, Zed, 配置方針, ホーム, open wsl, projects: open wsl, open folder in wsl, リモート接続, remote development, ext4, df -T, 9p, drvfs, wsl$, LSP, Agent, ACP, git clone, 専用 distro]
created: 2026-10-02
updated: 2026-11-04
sources:
  - ChatGPT conversation "ZedとWSLのファイル配置方針" (2026-10-02)
  - "%APPDATA%\\Zed\\settings.json、C:\\vault の構成（2026-10-02 に確認）"
  - "`wsl -l -q`、WSL の `$USER` と環境変数（2026-10-06 に確認。「Open Questions」を更新）"
  - Claude Code conversation "works の再定義と開発リポジトリの置き場（Zed から WSL が見えるか）" (2026-10-31)
---

# ZedとWSLのファイル配置方針

## Purpose

ZedからWSLを使う開発環境で、プロジェクトや各種ファイルをWindows側とWSL側のどちらに置くかを決める。

## Principles

- 開発用ファイルはWSL側に置く（暫定）。Linuxの開発ツール、Git、言語ランタイムを一貫して扱えるうえ、`/mnt/c` 越しの大量I/Oは遅くなりやすい。
- WindowsアプリやWindowsとの同期・共有が目的のデータ（Documents、Downloads、Pictures、OneDrive同期対象、Windows専用アプリの作業データ）はWindows側に置く。
- 受け渡しは必要なときだけ。`/mnt/c/...` か、エクスプローラーの `\\wsl.localhost\<Distro>\home\<user>\` を使う。
- ファイルを共有できることと、どちらを主配置先にするかは別の問題。
- WSL 側のコードは ext4 に置いたまま、Zed の WSL リモート接続で開く。`/mnt/c` や `\wsl$` を跨がない。理由: 実機で、編集、言語サーバーのハイライト、git の表示、Agent が動いた（2026-10-31）。
- 置き場が ext4 かは `df -T <パス>` の Type 列で確かめる。`ext4` なら WSL の仮想ディスク上、`9p` や `drvfs` なら Windows 側を跨いでいる（`~` の見かけでは分からない）。
- 公開リポジトリの clone が通っても、認証が要るリポジトリの clone / push が通るとは言えない（認証の経路を通っていない）。非公開で確かめるときは、push が拒否されることまで見る（読み取り専用の鍵の確認）。

## Decisions

### 開発用ファイルはWSL側に置く（暫定、2026-10-02）

- 想定パス: `/home/<user>/src/<project>`。新規Gitリポジトリは原則WSL側にcloneする。
- 却下案: すべてWindows側に置く（WSLからの大量I/OとLinux開発ツールの整合性で不利）。OneDrive同期対象をWSLホームに直接構築する（同期・ファイル監視・権限の複雑さ）。

## Facts

- WSLからWindows側は通常 `/mnt/c/...`。WSL内のホームは通常 `/home/<user>/`。
- 仮説・環境依存: WSL側のファイルシステムは、Gitや依存管理が大量のファイルを扱う場面で `/mnt/c` より有利になりやすい。

- Zed の公式 docs の WSL 向けの操作は 2 つ。WSL 内のフォルダは `projects: open wsl` で distro を選び、Windows 側のフォルダを WSL で開くのは `projects: open folder in wsl`。docs は、UI がローカル、LSP・タスク・ターミナルがサーバー側という分担を SSH 接続の話として書いていて、WSL にも同じ分担が当てはまるとは明記していない（確認: 2026-10-31、根拠: zed.dev/docs/remote-development の取得）。
- Windows 版の Zed から、専用の WSL distro に接続して、そこの `~` で `git clone` したリポジトリを読めた。`df -T` は `/dev/sdd`、Type `ext4`、Mounted on `/`（確認: 2026-10-31、根拠: ユーザーの実機の出力）。
- 同じ接続で、編集、LSP によるハイライト、git の表示、Agent が動いた（確認: 2026-10-31、根拠: ユーザーの発言）。
- clone したのは公開リポジトリで、認証なしで通った（確認: 2026-10-31、根拠: ユーザーの発言）。
- 同日、専用 distro の中で、非公開リポジトリを読み取り専用の deploy key（SSH、ed25519）で `git clone` できた。`push` は「The key you are authenticating with has been marked as read only」で拒否され、期待どおりだった（確認: 2026-10-31、根拠: ユーザーの実機の結果）。push は room に許さない方針で、認証の決定は `ai-isolated-work-room.md` の 10-31 の項にある。

### 実物との照合（2026-10-02）

メモの前提と、現在のこのPCの実態には食い違いがある。

- Zedのターミナルは `pwsh.exe`（`settings.json`）。2026-09-26 時点では `wsl.exe` だった。現在、ZedのターミナルはWSLではない。
- リポジトリはWindows側にある（記述時点。2026-10-06 以降は `$HOME\works\repos\...`）: `C:\vault\repos\github.com\yuzucha16\`（`areas_shared`、`dotfiles`）。「開発用ファイルはWSL側」という暫定方針とは逆の配置。
- Zedのプロジェクトは、Windowsのパス（記述時点の例: `C:\vault\notes\areas_shared\exmem`。現在の Vault のトップは `$HOME\works`。2026-10-06 に `C:\vault\works` から移した）で開いている（[[claude-code-storage]]）。ZedのWSLプロジェクト連携（ファイルシステム・Language Server・ツール実行をWSL側に寄せる方式）を使っているかは、今回も確認できていない。
- WSLにはZsh、`rg`、`fzf`、`zoxide` などが入っているが、`nvim` と `ghq` は入っていない（[[modern-cli-tools]]）。

## Gotchas

### ターミナルだけWSLにしても、プロジェクトやLanguage ServerはWindows側のまま

- ターミナル設定と、リモート/WSLプロジェクト連携は別。どちらがWSL側で動いているか、区別して確認する。

### `/mnt/c` 上のリポジトリは遅くなることがある

- `git`、`rg`、`npm install` などは、ファイル数やI/Oパターンによって遅くなる。

## Open Questions

- 一部解決（2026-10-31）: 方式は `projects: open wsl`（WSL リモート接続）。専用 distro では、編集・LSP のハイライト・git の表示・Agent が動いた。ただしファイル操作、LSP、git、ターミナルの各処理がどちら側で動くかの内訳は、docs が WSL について明記しておらず未確認。
- 現在Windows側にあるリポジトリ（`C:\vault\repos`）を、この方針でWSL側へ移すのか。それとも「Windowsで編集するリポジトリ」と「WSL側の開発用リポジトリ」を分けるのか。vaultとdotfilesは、Windows側から使う前提（ジャンクション・シンボリックリンク）なので、移すと崩れる（[[obsidian-vault]]）。（2026-10-05 の修正: vault のトップは実ディレクトリになり、ジャンクションは `.obsidian` だけになったので、vault については記述が古い。dotfiles の `links.map` は Windows のリンクを使う前提のまま。）
- Windows側のアプリと頻繁に編集・同期するプロジェクトはあるか。
- 提案（AI の提案。方針の議論の途中で、未承認）: 開発用のリポジトリを WSL の ext4 に置き、PC ローカルの台帳（remote を持たない作業フォルダ）と 1:N で対応づける。
- 解決（2026-10-06）: WSLのディストロ名は Ubuntu-24.04、ユーザー名は Windows と違う（確認: `wsl -l -q` と `$USER`）。標準のプロジェクトディレクトリは、`~/works/repos`（ghq の root）にそろえると決めたが、この PC の WSL は未移行で、実際は `~/vault/repos`（[[obsidian-vault]] の「置き場を `$HOME\works` へ移す」）。
- WSL のユーザー名が Windows と違うので、`/mnt/c/Users/$USER/...` の組み立ては外れる。Windows のパスは、環境変数と `WSLENV` の `/p` で渡す設計。`WSLENV` の区切りは `:`（`;` では渡らない。2026-10-18 に実機で確認。詳細は `obsidian-vault.md`）。

## Next Actions

- ZedのWSL連携の各処理の実行側と、プロジェクトの実際のパスを確認する。
- 未 push の clone を、人が room の外から push する運用を確かめる（2026-10-31 時点）。
- WSL側に `~/src` など開発用ルートを作る。
- 代表的なプロジェクトで、Git操作・検索・ビルド・Language Serverの動作と速度を確認し、方針を確定する。

## Related

- [[zed-dotfiles]]
- [[modern-cli-tools]]
- [[vscode-workspace]]
- [[claude-code-vs-cowork]]
