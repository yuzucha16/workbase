---
type: knowledge
title: ターミナルのカーソル点滅を止める（DECSCUSR）
status: active
tags:
  - accessibility
  - tool/windows-terminal
  - tool/zed
  - tool/powershell
  - cli
aliases:
  - カーソル点滅の停止
  - DECSCUSR
  - 点滅を止める
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation "ターミナルのカーソル点滅を止める（Zed・Windows Terminal・WSL）" (2026-10-04)
  - "dotfiles の profile.ps1 / .bashrc / common.sh / home/.config/zed/settings.json（2026-10-04 に確認）"
---

# ターミナルのカーソル点滅を止める（DECSCUSR）

## Purpose

光の点滅が片頭痛の負担になるため、Zed と Windows Terminal（pwsh、WSL の bash と zsh）のカーソル点滅を止める。アプリに設定項目が無い端末でも止められる方法をまとめる。目の負担に関する他の設定は [[fonts]]（フォント）と [[zed-dotfiles]]（テーマ）。

## Principles

- 点滅のような視覚の負担は、アプリ内の設定とシェル側の両方で止める。どれか1つでは漏れる。
- OS 全体に効く設定（全アプリのカーソル点滅）は、影響範囲が広いので、頼まれてから変える。

## Decisions

### シェル側で DECSCUSR の `ESC[2 q`（点滅なしブロックカーソル）を送る（2026-10-04）

- 根拠: Windows Terminal の `settings.json` にはカーソル点滅の項目が無く、点滅は Windows のカーソル点滅の設定に従う（`cursorShape` などはあるが点滅は無い）。ターミナルのエスケープシーケンスなら、設定項目が無くても指定できる。
- pwsh: プロファイルの先頭（非対話起動の早期 return の後）で `[Console]::Write("$([char]27)[2 q")` を1回送る。
- bash: `.bashrc`（対話シェルだけ通る箇所）で `printf '\e[2 q'` を1回送る。
- zsh: `precmd_functions` に関数を登録して、プロンプトごとに `printf '\e[2 q'` を送る。起動時に1回だけだと、プロンプトの再描画で点滅が戻る（Gotchas）。
- 却下案: 起動時に1回だけ送る方式を zsh にも使う（戻る）。

### Zed は設定で止める（2026-10-04）

- エディタは `cursor_blink: false`、ターミナルは `terminal.blinking: "off"`（`off` / `on` / `terminal_controlled`）。

### OS 全体の点滅停止は見送る

- レジストリ `HKCU\Control Panel\Desktop\CursorBlinkRate` を `-1`。全アプリに効くため、必要になったら検討する。

## Facts

確認済み（2026-10-04、dotfiles の実物）:

- `windows/powershell/profile.ps1` に `[Console]::Write("$([char]27)[2 q")`、`home/.bashrc` に `printf '\e[2 q'`、`home/.config/shell/common.sh` に zsh の `_steady_cursor() { printf '\e[2 q' }` がある。
- `home/.config/zed/settings.json` に `"cursor_blink": false` と `"terminal": { "blinking": "off" }` がある。

実機での観察（会話の時点）:

- 起動時に1回だけ送った zsh は、Windows Terminal で点滅していた。`precmd` で毎回送る方式に直した。

仮説（未確認）:

- 修正後の zsh、および bash と pwsh で、Windows Terminal が `ESC[2 q` に従って点滅を止めるか（DECSCUSR は標準的な指定）。
- WSL 以外の端末や別のPCでも同じ指定で止まるか。

## Gotchas

- **zsh だけ点滅が戻る**: 起動時に1回送るだけだと、zsh はプロンプトのたびに画面を再描画するので上書きされる。`precmd_functions+=(関数)` で毎回送って解決する。
- **starship の警告 `Scanning current directory timed out`**: カーソルの件とは無関係。`starship.toml` の `scan_timeout`（ミリ秒）を意図的に短くしているため、ファイル数の多いディレクトリで出る。

## Open Questions

- 新しいシェル（pwsh、bash、zsh）で点滅が止まっているか。止まらないシェルがあれば、経路（プロンプトの再描画、tmux などの中継）を調べる。
- Zed の端末が `ESC[2 q` をそのまま扱うか（Zed 側の `terminal.blinking` と二重になるが害は無い見込み）。
- OS 全体の点滅停止（`CursorBlinkRate`）を入れるか。

## Related

- [[fonts]]
- [[zed-dotfiles]]
- [[notepad-plus-plus]]
- [[shell-fzf-keybindings]]
