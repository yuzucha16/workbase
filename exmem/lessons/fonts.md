---
type: knowledge
title: フォントの選定と導入
status: active
tags:
  - font
  - setup
  - windows
  - tool/zed
aliases:
  - フォント
  - PlemolJP
  - メインフォント
created: 2026-10-03
updated: 2026-10-05
sources:
  - Claude conversation "Win11メインフォントの採用基準と選定" (2026-10-03)
  - Claude Code conversation "フォント導入 (PlemolJP / Moralerspace) と Zed・Terminal・Notepad++ のフォント統一" (2026-10-03)
  - "dotfiles の zed / terminal 設定と manifests/fonts.txt（2026-10-03 に確認）"
---

# フォントの選定と導入

## Purpose

Win11 のメインフォントを、目の負担を最優先に選び、Zed / Windows Terminal / Notepad++ で揃える。フォントの取得スクリプトは dotfiles リポジトリにある。手順書は `resources/guides/howto/fonts-setup.md`（旧 `cheatsheets/env/fonts.md`）（[[pc-setup-manuals]]）。

## Principles

- **目の負担を最優先にする**（閃輝暗点のある偏頭痛持ちのため）。疲れやすさの傾向は、細すぎるとにじみ、太すぎると画数の多い字が潰れてギラつく。本人の体感では「太すぎると疲れる」。
- 必須条件: 半角1:全角2の等幅、Nerd Font 同梱、OFL 等の緩いライセンスで更新が続いている。Markdown の表やコンソールの桁ずれを防ぐため。
- 比較軸: 判別性（`0O` `1lI` `` ` `` `'`）、全角スペースが見分けられるか、記号の見やすさ、ウェイトの均質さ、字面の大きさと字間、導入の手軽さ。
- 最終判断は本人の体感。疲れにくいフォントの一般的な傾向（中庸の太さ、英数字と日本語の濃さが揃う、背景はオフホワイトか暗いグレー）は医学的な保証ではない（仮説）。

## Decisions

### メインは PlemolJP Console NF の Light、1週間試す（2026-10-03）

- 根拠: 比較ページで見比べて一番良さそうだった。PlemolJP は Thin〜Bold の8ウェイトがあり太さを調整できる。Moralerspace v2.0.0 は Regular / Bold / Italic / BoldItalic のみ。
- 却下案: Moralerspace Neon HW（ウェイトを選べない。サブには採用）、UDEV Gothic NF（形は好きだが太く感じる）、HackGen（現行だったが決定的な理由がなく、当時の印象で残していただけ）、Myrica（以前は細すぎて止めた。今は許容範囲だがもう少し太いほうがよく、参照点にとどめた）。
- 35系（半角3:全角5。`Moralerspace Neon`、`UDEV Gothic 35NF`）は、2:1の必須条件を満たさないので除外した。
- インストールするウェイトは最小限にする。Light（main）、Regular（sub）、Text（sub）、Bold（Markdown の太字用）、Italic。Moralerspace は `MoralerspaceNeonHW-Regular.ttf` だけ（sub）。全部入れるとフォント一覧が膨大になるため。

### フォント指定はファミリー名 + ウェイト（2026-10-03）

- 決めたこと: Light 専用名は使わず、ファミリー `PlemolJP Console NF` に `font_weight` 300 を指定する。Moralerspace のファミリー名は `Moralerspace Neon HW`（スペースあり）。
- Zed は UI・エディタ・ターミナル・エージェントを同じ設定にする: フォールバックは `Moralerspace Neon HW`、`Meiryo UI`。サイズは4項目を 15 に統一した。Windows Terminal と Notepad++ も同じフォントにした。
- 確認済み（2026-10-03）: dotfiles の `home/.config/zed/settings.json` に上記の設定が入っている。Zed での反映（細くなる、`ui_font_*` で claude-acp のチャット本文も変わる）は、ユーザーが実機で確認した。

### フォントの取得はスクリプト、インストールは手動（2026-10-03）

- `scripts/windows/24_fonts.bat` と `scripts/linux/24_fonts.sh`、一覧は `manifests/fonts.txt`（`owner/repo:asset glob`）。取得は `gh release download`、保存先は `~/download`（WSL は WSL 側）。番号 24 は、23 が Linux 専用の日本語入力のため。
- 2026-10-04 に、`--dry-run` と `gh auth status` の確認はスクリプトから削除した（未ログインでも `gh release download` が通り、`--dry-run` は1行の表示にすぎないため。[[gh-release-download]]）。2026-10-03 時点では `--dry-run` が `gh` の認証不要で動いていた。
- 取得対象: `yuru7/PlemolJP:PlemolJP_NF_v*.zip`、`yuru7/moralerspace:MoralerspaceHW_v*.zip`（v2.0.0 から NF のグリフが全バリエーションに入り、NF 専用 zip はない。1:2幅は HW 版）。
- `gh` は `manifests/apps.txt`（scoop）と `manifests/apt.txt` に追加した。
- 却下案: `gh` で asset 名を事前に解決する（`gh release list` などは未ログインだと失敗する。[[gh-release-download]]）。

## Facts

- PlemolJP のバリエーション: 通常、Console、35、35 Console。Console は IBM Plex Mono の字体を全面適用し、矢印などの記号が半角になる。通常版は記号の一部が日本語フォント側の幅になる。**行間の違いではない**。
- PlemolJP v3.1.0 の Assets: `PlemolJP_v3.1.0.zip`、`PlemolJP_NF_v3.1.0.zip`（NF 入り、146MB）、`PlemolJP_HS_v3.1.0.zip`（全角スペース不可視版）。全角スペースは標準で可視化される。
- Moralerspace v2.0.0 の Assets: `MoralerspaceHW_v2.0.0.zip`、`MoralerspaceHWJPDOC_v2.0.0.zip`、`Moralerspace_v2.0.0.zip`、`MoralerspaceJPDOC_v2.0.0.zip`。Neon / Argon / Xenon / Radon / Krypton の5スタイル。
- UDEV Gothic NF は NF 専用 zip がある。ファイル名に「35」が付かないものが半角1:全角2。
- PlemolJP のリリースノートは、Windows でのフォント更新時は、既存フォントを削除してから新規インストールすることを勧めている。
- Windows 上のファミリー名（WPF の `GlyphTypeface` で確認）: `PlemolJP Console NF`（Light = ウェイト Light、Text = 450）、`Moralerspace Neon HW`、`Moralerspace Neon`、`HackGen Console NF`、`UDEV Gothic NF`、`UDEV Gothic 35NF`、`MyricaMMonospace Nerd Font`。2026-10-03 に実物でも、`PlemolJP Console NF`、`Moralerspace Neon HW`、`Moralerspace Neon`、`HackGen Console NF` がインストール済みであることを確認した。
- Windows Terminal のフォントフェイス欄にウェイト違いは出ない。ファミリー名を選び、「フォントの太さ」で細字を指定する。
- 仮説（未確認）: Zed の `terminal.font_weight` と `font_fallbacks` の設定名。`agent_buffer_font_size` と `agent_ui_font_size` のどちらが claude-acp のチャット入力欄に効くか。Notepad++ の `fontName="PlemolJP Console NF Light"` が旧来の描画（GDI 系）で通るか。Zed のターミナルは `font_size` 未指定ならエディタのサイズに従う。
- `gh` は scoop に入っている（2026-10-03 確認。2026-10-04 に 2.102.0）。公開リリースの取得は未ログインでも通る（2026-10-04、実機で PlemolJP の NF 版約153MBと Moralerspace の HW 版約102MBを取得）。

## Gotchas

- **`PlemolJP Console NF Light` を指定しても細くならない**: Light は別ファミリーではなくファミリー内のウェイト。名前が見つからずフォールバックに落ちていた。ファミリー + ウェイト 300 で解決。
- **`MoralerspaceNeonHW` が効かない**: 正しくは `Moralerspace Neon HW`（スペースあり）。
- **Windows Terminal でフォント名に Light を入力しても選べない**: 太さは別項目。
- **Windows Terminal の `settings.json` が全行差分になる**: アプリが書き直して改行が CRLF から LF に変わっていた。CRLF に戻してコミットした（`"source": "Microsoft.WSL"` の追加はアプリによるもので、同じコミットに含めた）。
- **`ghq get` で zip が取れない**: clone するだけで Releases の Assets は取れない。`gh release download` か `curl -L`。
- **MoralerspaceNF の専用 zip が見つからない**: v2.0.0 で NF が標準に統合された。HW 版を使う。
- **Myrica のフォント名が想定と違う**: `MyricaMMonospace Nerd Font`（`Myrica M` ではない）。`Proportional` は使わない。
- **「Console は行間を詰めた派生」は誤りだった**。実際は記号の幅の違い。
- **比較ページで全フォントが「未検出」**: スマホで開いていた、フォント名の不一致、ブラウザ再起動が必要、埋め込み表示の制限が原因。ページ内の `queryLocalFonts` ボタンで実名を取得して解決した。「全部同じ見た目」は、HTML の style 属性内で `font-family` の引用符が二重引用符になり属性が壊れていたため。
- **`Set-Content` が失敗**: 同じファイルを `Get-Content -Raw` した直後の書き戻しで、ファイルロックのエラー（[[obsidian-vault]] の同種の事例も参照）。Edit ツールで解決した。

## Open Questions

- Light で細すぎないか。細ければ Text（Regular の上）を試す。1週間後に、夕方の目の疲れやちらつき、細くて読みにくい字、全角スペースの見分けを確認して「Light で続ける / Text に上げる / HackGen に戻す」を決める。
- Console にするか通常版にするか。ターミナルは Console、文章中心のアプリは通常版という使い分けも可能。本人の「詰めてない（通常）ほうがよい」は、Console を行間の派生と誤解した上での発言だった。
- Zed の claude-acp のチャット入力欄のサイズが他より大きく見える。どの設定が効いているか未特定（`agent_buffer_font_size` を一時的に極端な値にして切り分ける）。
- サイズがアプリ間で揃っていない（Zed 15 / Notepad++ 12 / Windows Terminal 既定の 12。単位が違うので見え方も違う）。
- Obsidian のフォント（CSS スニペットで `font-family` と `font-weight: 300`）は未設定。
- 背景色（オフホワイト、ダークグレー）を変えたときの太さの感じ方。Moralerspace の他のスタイル（Argon 等）を試すか。
- `24_fonts.*` スクリプト自体の通し実行（`gh release download` のコマンド単体は、2026-10-04 に実機で成功を確認）。インストールは手動。
- `resources/fonts/` への HackGen 配置の予定（[[obsidian-vault]]）は、メインが PlemolJP に変わる見込みなので、置くフォントを見直すか（未決）。2026-10-05 に、`fonts/` は履歴ごと削除した（フォントは Vault に置かない。取得は dotfiles の `24_fonts`）。

## Related

- [[gh-release-download]]
- [[pc-setup-manuals]]
- [[zed-dotfiles]]
- [[obsidian-vault]]
