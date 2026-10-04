---
type: knowledge
title: Windows のアプリを scoop で管理し、管理外を最小にする
status: active
tags:
  - tool/scoop
  - tool/winget
  - windows
  - setup
aliases:
  - scoop管理
  - scoopと管理外アプリ
  - アプリの整理
created: 2026-10-04
updated: 2026-10-04
sources:
  - Claude Code conversation "scoop 管理下と管理外アプリの整理" (2026-10-04)
  - "winget list / pnputil の出力（2026-10-04、Windows 11 Home 10.0.26200）"
---

# Windows のアプリを scoop で管理し、管理外を最小にする

## Purpose

Windows 11 のアプリを「scoop で管理するもの」と「それ以外」に分け、再構築でも手で入れ直すものを最小の一覧で持てる状態にする。scoop 側の一覧は dotfiles の `manifests/apps.txt`（[[pc-setup-manuals]]）。

## Principles

- scoop を正本にする。同じアプリが scoop と他の経路（winget、手動、Store）に二重に入っている場合は、scoop 側に統一する。
- 「管理外一覧」には、自分が意図して入れたアプリだけを載せる。Windows 標準、Microsoft 製のアプリ・ランタイム、ハードウェアドライバは載せない（依存や OS 更新で変わり、手動管理の対象にならないため）。
- 削除前に、重複に見える項目が本当に別のインストールかを確認する。
- 一覧と manifest は実機の状態に合わせる。実機に無いものを manifest に残さない。

## Decisions

### 二重管理は scoop 版に統一する（2026-10-04）

- 決めたこと: winget に出る二重管理のうち、実体が別だった Notepad++（`C:\Program Files`）と Zed（`AppData\Local\Programs`）は削除し、scoop 版に統一した。
- 根拠: 実体が別で、scoop 側に設定の置き場があるため（[[notepad-plus-plus]]、[[zed-dotfiles]]）。
- 却下案: 重複を残して注記だけにする（バージョンが食い違い、更新対象が曖昧になる）。

### 削除しないもの

- AutoHotkey: winget に出る項目は scoop 自身が登録したものだった。
- Windows Terminal: Win11 標準の Store 版を残す。標準の端末で、scoop 版と並んでも実害が無い。却下案: Store 版の削除（標準アプリを消すリスクが大きい）。

### manifest は実機に合わせる方向で直す

- 未インストールの項目を外し、入っている項目を追記する。却下案: manifest に合わせて scoop install / uninstall する（使っていないものを新たに入れることになる）。

## Facts

2026-10-04、Windows 11 Home 10.0.26200 で確認。

- `winget list` には、scoop が登録した項目も出る。AutoHotkey は、アンインストーラーの場所が scoop の `apps` ディレクトリを指していた。
- 同じ Notepad++ が winget 版 8.8.7（`C:\Program Files\Notepad++`）と scoop 版 8.9.8.1 の両方に入っていた。PATH では scoop の shim が先に使われていた。
- Zed の Inno Setup 版は、アンインストールしても `%APPDATA%\Zed\settings.json` が残った。
- アンインストールしても、レジストリの登録だけが残るケースがある（Emacs で確認）。`winget list` にも残って表示される。
- 管理外一覧を最小にした結果、残ったのは winget の uv、Steam、Sunshine、ViGEm Bus Driver、Bambu Studio と、手動の Dell SupportAssist。
- 仮説（未確認）: KiCad 5.1 のアンインストーラーは KiCad 10 と同じフォルダの直下にある（10 は `10.0` サブフォルダ）ため、フォルダごと消える可能性がある。今回は両方削除済み。

## Gotchas

- **管理者権限のないシェルでは、Program Files のアンインストール、HKLM のレジストリ削除、ドライバの削除ができない**。管理者の PowerShell で別途実行する。
- **ドライバパッケージの `oemNN.inf` の番号は環境ごとに違う**。`pnputil /enum-drivers` の出力を Provider 名（SEGGER、Nordic など）で絞って番号を取り出してから、`pnputil /delete-driver <oemNN.inf> /uninstall /force` を使う。
- **`.vimrc` が `global`（gtags）を呼んでいる場合、manifest から `global` を外すとキーマップが動かなくなる**。外すなら `.vimrc` の記述も一緒に消す。

## Open Questions

- 「管理外一覧」の置き場。dotfiles の `manifests/` には見当たらない（2026-10-04 時点）。README か `docs/` か、どこに持つか未確認。
- Windows Terminal の scoop 版と Store 版を、今後も並べておくか。
- ViGEm Bus Driver は、Sunshine を使わなくなったら一緒に消すか。
- 削除の残骸（J-Link と Nordic のドライバ、Visual Studio Installer、Emacs の登録エントリ）の管理者での削除と、削除後の `winget list` / `pnputil /enum-drivers` での確認（作業は未完了とみられる）。

## Related

- [[pc-setup-manuals]]
- [[notepad-plus-plus]]
- [[zed-dotfiles]]
