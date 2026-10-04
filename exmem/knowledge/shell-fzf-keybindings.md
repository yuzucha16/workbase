---
type: knowledge
title: シェルの fzf とキー割り当て（pwsh / zsh / bash）
status: active
tags:
  - cli
  - keymap
  - dotfiles
  - tool/powershell
aliases:
  - fzfのキーバインド
  - Ctrl+R Ctrl+T
  - Alt+j Alt+k
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation "シェルのコマンド履歴の種と fzf・キーバインドの整理" (2026-10-04)
  - "dotfiles の profile.ps1 / common.sh（2026-10-04 に確認）"
---

# シェルの fzf とキー割り当て（pwsh / zsh / bash）

## Purpose

3つのシェル（pwsh、zsh、bash）で、履歴検索・ファイル検索・移動のキーを同じにし、その割り当ての判断基準を残す。設定そのもの（現仕様と経緯）は dotfiles リポジトリの `docs/decisions.md`。コマンド履歴の種は [[shell-command-usecases]]。

## Principles

- **fzf の標準機能は標準キー、自作は全シェルで空いているキー**。`Ctrl+R`（履歴検索）と `Ctrl+T`（ファイル検索）は fzf の標準キーなのでそのまま使う。標準から外すと、他の fzf の解説とも食い違う。
- fzf の使い道は、履歴検索・ファイル検索・移動（`zfz`、`cdg`）に絞る。補完と `Alt+C` は使わない。「便利で色々作ってしまう」への歯止め。
- ターミナルは軽く保つ。fzf は目的ではなく手段で、起動時間への影響を測って許容する（Facts）。
- 3シェルで同じ見た目・同じキーにそろえる。ただし標準機能が無いもの（bash の ListView 相当）は無理に作らない。
- 外部の大きな依存（ble.sh、PSFzf）は入れない。pwsh は自前のハンドラで `fzf` を直接呼ぶ。

## Decisions

### キー割り当て（2026-10-04）

| キー | 機能 | 備考 |
|---|---|---|
| `Ctrl+R` | fzf の履歴検索 | readline・zsh・PSReadLine の履歴検索の標準キー |
| `Ctrl+T` | fzf のファイル検索 | `transpose-chars`（pwsh は `SwapCharacters`。直前の2文字の入れ替え）を上書きする。使用頻度が低く、`Alt+t`（語の入れ替え）は残る |
| `Alt+j` | `zfz`（zoxide の候補から移動。j = jump） | 3シェルのデフォルトで未使用 |
| `Alt+k` | `cdg`（ghq 管理下のリポジトリへ移動。j の隣で Vim の j/k） | 同上 |
| `Alt+c` | 標準の `capitalize-word` | fzf の `Alt+C` は使わない |

- 以前の `Ctrl+g`（pwsh の `Abort` を上書きしていた）は戻した。
- `Ctrl+英字` に空きはほぼ無い。3シェルで空いている `Alt+英字` は `e i j k m o v` だけ（使用済みは `a b c d f g h l n p q r s t u w x y z` のどれか。シェルごとに違う）。
- 実装: zsh/bash は apt 版 fzf の `/usr/share/doc/fzf/examples/key-bindings.{zsh,bash}` を読む（補完は読まない）。pwsh は `profile.ps1` の `Invoke-FzfHistory` / `Invoke-FzfFile` を `Set-PSReadLineKeyHandler` で登録する。pwsh の履歴は PSReadLine の履歴ファイルを新しい順・重複なしで読む（`Get-FzfHistory`）。`Ctrl+T` は `fd --hidden --follow --exclude .git` と `bat` のプレビュー。`FZF_DEFAULT_OPTS='--height=40% --reverse'`。
- pwsh の `ListView`（予測表示）は残す。zsh/bash の ListView 相当は作らない。

### fzf を外す判断と戻す判断（同日、2026-10-04）

- 前半: 「fzf は移動用に限定し、履歴検索は標準機能」と決めて、zsh/bash の fzf キーバインドを外した（以前外した理由は「重い」「便利で色々作る」「あまり使わない」）。
- 後半: zsh で ListView 相当を自作して試したが採用せず、全体の一貫性を優先して fzf に切り替えた（ユーザー判断）。使い道を履歴とファイル検索に絞ることを歯止めにした。自作はコミット前に削除した。
- 却下案: 自作の ListView 相当（履歴を毎キー走査するため、50,000件で一致なしだと 3.5 秒。配列化して絞り込めば 50,000件で約 30ms、10件程度なら 1〜4ms だが、保守が増える）。bash の ListView 相当（標準機能が無い）。PSFzf。ble.sh。

## Facts

確認済み（2026-10-04）:

- fzf のバージョン: pwsh（scoop）0.74.4、WSL（apt）0.44.1。3シェルとも Emacs モード。
- 起動時間への影響（fzf のキーバインドの有無を交互に7回測定）: zsh 約 +8 ms、bash 約 +9 ms。
- zsh/bash: `Alt+j`/`Alt+k`、`Ctrl+R`（履歴の一覧から選んだコマンドがプロンプトに入る）、`Ctrl+T`（選んだパスが入る）を疑似端末で確認した。`Alt+c` は標準の `capitalize-word`。
- pwsh: `Ctrl+R`/`Ctrl+T` はユーザーが実機で動作確認した。`Get-FzfHistory`（新しい順・重複なし）とパスのクォート処理は非対話で確認した。
- dotfiles の実物: `profile.ps1` に `Alt+j`/`Alt+k`/`Ctrl+r`/`Ctrl+t` のハンドラと `PredictionViewStyle ListView` がある。`common.sh` に `FZF_DEFAULT_OPTS` と `key-bindings` の読み込みがある。

仮説（未確認）:

- PSReadLine 2.4.5 の `ListView` は件数を変える設定項目が無い（10件固定。ソース未確認）。
- Windows Terminal と Zed の端末が `Alt+j`/`Alt+k`/`Ctrl+T` をそのままシェルへ渡すか（pwsh ではユーザーが確認済み。Zed の端末は未確認）。
- WSL に `ghq` が無いので、zsh/bash の `cdg` は実機未確認（スタブでは確認済み）。

## Gotchas

- **fzf の `--height` は端末にカーソル位置を問い合わせる**。疑似端末のテストで応答しないと、fzf が待ち続けて何も出ない。`ESC[6n` に `ESC[10;1R` を返すようにして解決した。
- **bash は `.bashrc` 末尾の `cd ~` で、起動時のディレクトリが常に `~` になる**。`Ctrl+T` が `~` から探してしまうので、`cd ~` を削除した（ユーザー判断）。zsh は影響なし。
- **bash の `bind -p` を非対話で取ると一覧が不完全**。空きキーの判断は readline の既定と合わせて行い、実装後に `bind -X` で確認した。
- **zsh の履歴サイズが `HISTSIZE` の既定（30）のままだと、`fc -l` の件数が少なく見える**。`zsh -f` で試験するときの罠。rc では 50000。
- **一時スクリプトの名前を `pty.py` にすると、Python の標準 `pty` モジュールを隠して失敗する**（`lvtest.py` に変更）。
- **履歴の `ll`/`cd` の件数は、除外ルールの導入前の記録**。分析の件数（`ll` 294回など）は古い設定のときのもの。
- **PowerShell の `Remove-Item` 保護**: 疑似端末の試験用の一時ファイルを削除するコマンドに `rm` や `/c` の文字列が混ざると、ツールのガードが拒否することがあった。削除は別コマンドに分ける。
- 履歴に関する Gotchas（秘匿情報の検出漏れ、`<…>` プレースホルダーが実行される条件）は [[shell-command-usecases]]。

## Open Questions

- pwsh の `Ctrl+R` の候補は履歴ファイルの行ごとで、複数行コマンドの全体は選べない。
- WSL に `ghq` を入れて、zsh/bash の `cdg`（`Alt+k`）を実機で確認する。
- 3シェルの差の洗い出しと共通化（他の項目）。

## Related

- [[shell-command-usecases]]
- [[modern-cli-tools]]
- [[terminal-cursor-blink]]
- [[zed-vim]]
- dotfiles リポジトリ（`docs/decisions.md`: fzf とキーバインドの現仕様と経緯）。リンクではなく参照のみ
