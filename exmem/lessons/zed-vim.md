---
type: knowledge
title: Zed Vim環境
status: active
tags:
  - tool/zed
  - tool/vim
  - tool/neovim
  - keymap
  - setup
aliases:
  - Zed Vim環境
  - ZedへのVim環境移行
created: 2026-09-26
updated: 2026-10-10
sources:
  - Claude Code conversation "Zed の設定を最適化する（目の負担軽減・claude-acp・Obsidian 併用）" (2026-10-04)
  - ChatGPT conversation "ZedへのVim環境移行" (2026-09-26)
  - "%APPDATA%\\Zed\\settings.json / keymap.json（2026-09-26 に内容を確認、2026-10-02 に再確認）"
---

# Zed Vim環境

## Purpose

`.vimrc` で構築していた編集環境をZedへ移行する。

Vim設定を1:1で再現せず、Zed標準機能 + ZedのVim modeを基本とし、必要な操作だけ `keymap.json` で補う。
「VimをZed上で再現する」のではなく、**Zedの機能をVimの操作体系から使う**。

## Principles

- 優先順位は Zed標準 → Vim/Neovim標準 → 個人設定。
- Vim Pluginを再現しない。Zed標準機能と重複し、不要な設定が増える。
- `keymap.json` を先に作り込まない。実際に使って不足した操作だけ追加する。過去のキーマップを機械的に移植すると、Zed標準との衝突やNeovimとの共通操作からの逸脱につながる。
- ツールではなく目的で判断する（例: fzfが欲しいのではなく、floating panelでのあいまいファイル検索が欲しい）。

## Vim → Zed 対応表

設定キーは 2026-09-26 時点の `settings.json` で確認済み。

| Vim | Zed |
|---|---|
| `set number` | `gutter.line_numbers: true` |
| `set autoindent` | `auto_indent: true` |
| `set expandtab` | `hard_tabs: false` |
| `set tabstop=4` | `tab_size: 4` |
| `clipboard=unnamedplus` | `vim.use_system_clipboard: "always"` |
| `ignorecase` + `smartcase` | `use_smartcase_search: true` |
| `syntax enable` / `filetype plugin indent on` | Zedの言語サポート / Tree-sitter（設定不要） |

## Plugin → Zed 標準機能

| Plugin | Zed | 状態 |
|---|---|---|
| Fern | Project Panel | 移行方針のみ。ディレクトリ操作は未確認 |
| fzf | Go to File（`Ctrl-P`） | 仮説: Go to Fileで足りる。未確認 |
| GitGutter / Fugitive | Zed Git | 移行方針のみ。操作の対応は未確認 |
| Airline | Status Bar / Tab UI | 方針確定。追加設定は最小限 |
| gtags | LSP の定義・参照・Symbol検索 | 移行方針のみ。具体的な置換は未確認 |

Vim modeにはVimの基本操作に加えて、ZedのPane（`Ctrl-W h/j/k/l`）、LSP、Git、Project Panelと統合された操作が含まれるため、Pluginなしでもかなりの操作が成立する。

## Current Settings

2026-10-02 に `settings.json` を再確認した。

- `vim_mode: true`
- テーマ: Gruvbox Dark（dark）/ One Light（light）
- アイコンテーマ: Zed (Default)
- フォントサイズ: UI 16 / buffer 15
- ターミナルのシェル: `pwsh.exe`（2026-09-26 時点では `wsl.exe`。変更されている）
- Status Bar: active language / cursor position / line endings / encoding を表示
- 上の対応表の設定キー（`gutter.line_numbers`、`auto_indent`、`hard_tabs`、`tab_size`、`use_smartcase_search`、`vim.use_system_clipboard`）は、2026-10-02 時点でも同じ値で残っている。

`keymap.json` は、テンプレートのコメント（`j k` → `vim::NormalBefore` のコメントアウト行を含む）以外に次の設定だけを持つ（2026-10-02 時点も同じ）。

```json
{
  "context": "Terminal",
  "bindings": {
    "ctrl-p": ["terminal::SendKeystroke", "ctrl-p"],
    "ctrl-n": ["terminal::SendKeystroke", "ctrl-n"],
    "ctrl-shift-m": ["terminal::SendKeystroke", "ctrl-shift-m"]
  }
}
```

ターミナル内では `Ctrl-P` / `Ctrl-N` をZedに取られず、シェルへそのまま送る。エディタ上の `Ctrl-P` はGo to File、ターミナル内ではシェルの履歴操作、という使い分けになる。ターミナルのシェルは現在PowerShell（`pwsh.exe`）で、プロファイルにも `Ctrl+p` の履歴検索のキーバインドがある。シェルを `wsl.exe` から変えた経緯は未確認（[[wsl-file-placement]]）。

## Decisions

### Vim固有Pluginは基本的に破棄する（2026-09-26）

- 根拠: ZedにはProject Panel、Git、Status Bar、LSPなどの標準機能があり、Pluginを再現するよりZed標準へ移管する方が設定を簡潔にできる。
- 却下案: Vim Pluginの機能をZedで1:1再現する。

### 過去のキーマップは原則リセットする（2026-09-26）

- 根拠: 過去の `Ctrl-N` / `Ctrl-P` には、FernのProject Panel開閉、Airlineの前タブ、シェルのEmacs風next/prevなど異なる思想が混在していた。
- 却下案: `.vimrc` のキーマップを機械的に移植する。

### エディタの `Ctrl-P` はZed標準のGo to File（2026-09-26）

- 根拠: 目的はfloating panelでのあいまいファイル検索であり、fzf自体は目的ではない。Go to Fileで目的を満たすならfzfは導入しない。
- 却下案: fzfを導入する。

### `Ctrl-N` に過去のFern用設定を復活させない（2026-09-26）

- 根拠: Project PanelはZed標準のまま使う。

### Leaderは現時点では変更しない（2026-09-26）

- 根拠: Zed標準の `Ctrl+Shift+...` 系は使いづらいが、先に標準操作を使い込んでから設計する。
- 候補（未決）:
  1. キーボード側で `Ctrl+Shift` を1キー化する
  2. Zed側でleaderを変更する
  3. Neovimとの親和性を考え `Space` をleaderにし、一部を共通キーバインドにする

### Vim mode を1週間オフにして試す（2026-10-04）

- 決めたこと: `vim_mode: false`（2026-10-04 の `settings.json` で確認）。2026-10-11 頃に戻すか判断する。
- 根拠: エージェント画面は Ctrl+C でコピーなので、エディタもヤンクでなく Ctrl+C にそろえると操作が対称になる。操作が非対称になる設定は、無理に合わせるより片方を標準に寄せて試す。
- 戻す場合: `vim_mode: true` と `vim.use_system_clipboard: "always"`。必要な Vim 風キーは keymap で足す案もある（未実施）。
- 上の「Current Settings」の `vim_mode: true`、`tab_size: 4`、テーマ、ターミナルのシェルは 2026-10-02 時点の値。2026-10-04 時点では `vim_mode` がオフ、`tab_size` が 2（Notepad++ にそろえた。[[notepad-plus-plus]]）、テーマが自作の Material Gruvbox Dark、`terminal.shell` は削除済み（OS 既定。[[zed-dotfiles]]）。

## Open Questions

`contexts/zed-vim-migration` から移した（2026-10-10）。2026-10-04 に `vim_mode` をオフにしたため、前提が変わっている可能性がある。

- `Space` を leader として、Zed の一部の操作を Neovim と共通化するか。
- leader を Zed 側で変更するか、キーボード側で `Ctrl+Shift` を1キー化するか。
- Fern 時代のディレクトリ操作を、どこまで Zed 標準のまま使うか。
- gtags の操作を、LSP / Symbol 検索へ具体的にどう置き換えるか。
- GitGutter で使っていた操作を、Zed Git のどの標準操作へ対応させるか。
- 会話メモでは「`keymap.json` は空」としていたが、実際にはターミナル用の設定がある（`Ctrl-P` / `Ctrl-N` / `Ctrl-Shift-M` をシェルへ送る）。残す意図か（確認: 2026-10-02）。

## Next Actions

1. Project Panel で、Fern 相当のディレクトリ操作を確定する。
2. Go to File で、fzf なしのファジー検索の目的を満たせるか確認する。
3. Status Bar を基本とし、Airline 相当の追加設定を最小限にする。
4. gtags の代わりに、LSP の定義・参照・Symbol 検索を使う。
5. Zed Git + Vim mode の標準操作で、GitGutter / Fugitive の操作を試す。
6. 不足した操作だけ `keymap.json` へ追加する。
7. 最後に、Neovim との共通化を目的として Space leader を設計する。

## Related

- [[zed-acp]]
- [[wsl-file-placement]]
- [[vscode-workspace]]
