---
type: knowledge
title: Zedのdotfiles管理
status: active
tags:
  - tool/zed
  - dotfiles
  - setup
  - acp
aliases:
  - Zedのdotfiles管理
  - Zedの設定の再現
triggers: [Zed, dotfiles, settings.json, 設定の再現, 同期, 管理, シンボリックリンク, エディタ設定, 配置, ハイライト, highlight, 色が付かない, ps1, PowerShell, extension, Zed.log, failed to load language, NUL, .scm, theme_overrides, テーマ切り替え]
created: 2026-10-01
updated: 2026-11-04
sources:
  - Claude (Claude Code via Zed ACP) conversation "Zedのextension/ACPエージェントのdotfiles管理" (2026-10-01)
  - "%APPDATA%\\Zed / %LOCALAPPDATA%\\Zed / dotfilesリポジトリ（2026-10-01 に確認）"
  - "%APPDATA%\\Zed\\settings.json、PowerShellプロファイル（2026-10-02 に再確認）"
---

# Zedのdotfiles管理

## Purpose

Zedの設定・extension・ACPエージェントをdotfilesリポジトリで管理し、PCを変えてもすぐ再現できるようにする。

## Principles

- 手で書く設定だけを管理する。Zedが自動生成するキャッシュや本体は管理しない。（アプリが自動で書き換えるファイルを一律に外すのではなく、5項目で決める基準が別にある。[[app-config-placement]]。Zed の設定への当てはめは未見直し）
- 管理対象のファイルを増やさない。できるだけ `settings.json` 1ファイルに寄せる。

## 管理しているもの

管理の実体（リンク先のパス、`settings.json` の中身）は dotfiles が正（`README.md`、`windows/README.md`、`home/.config/zed/`。2026-10-16 に、ここにあった写しを削った）。ここには、管理の考え方だけを残す。

- `auto_install_extensions`: 起動時に不足しているextensionを自動インストールする。
- `agent_servers`: ACPエージェントの設定。Registryからインストールした時点で自動的に記録される（[[zed-acp]]）。`claude-acp` には `default_config_options.model`（既定モデル）を持たせられる。
- PowerShell のプロファイルの先頭には、非対話起動なら抜けるガードがあり、ZedのClaude Agent起動に必要（[[zed-acp]]）。

## 目の負担を減らす設定と、AIの窓口の設定（2026-10-04）

閃輝暗点を伴う片頭痛があり、光の反射や点滅を減らして長時間作業できる Zed にする。AI は Zed の claude-acp を窓口にし、Markdown は Obsidian と併用する。設定の正本は dotfiles の `home/.config/zed/settings.json`（2026-10-04 に実物で確認）。

### Principles

- 眩しさを減らす: ダークテーマ固定、文字色は純白寄りにせず暖色の低コントラスト（`#d4be98`）、点滅を止める（[[terminal-cursor-blink]]）。
- Obsidian と共有するファイルは、Obsidian 側の書式（タブ幅 2、タブ字下げ、行末スペース2つの強制改行）を壊さない。保存時の自動整形はオフにする。
- 外部エージェントの権限判断は、Zed と Claude Code で二重にしない（[[zed-acp]]）。
- 日本語入力では、Enter 送信にしない（変換確定の Enter が誤送信になる）。
- 設定を共有する環境（WSL/Linux）があるときは、OS 固有の値（`terminal.shell` など）を書かない。

### Decisions

- **自作テーマ "Material Gruvbox Dark" を使う**。Obsidian の Material Gruvbox テーマ（`theme.css`）の配色を移植した（背景 `#282828`、サイドバー・パネル `#1d2021`、文字 `#d4be98`、アクセント `#7daea3`、見出し `#a7b85a`）。置き場は dotfiles（`%APPDATA%\zed\themes` へのジャンクション。2026-10-04 に確認）。根拠: Zed 標準の Gruvbox Dark は文字色が `#ebdbb2` で明るい。却下案: 標準の Gruvbox Dark のまま。
- **メッセージ送信は Ctrl+Enter**（`agent.use_modifier_to_send: true`）。IME の変換確定の Enter で送信されるのを防ぐ。
- **エージェントパネルは左ドック、プロジェクトパネルは右ドック**。同じドックに置いたパネルは上下に並ばず、どちらか一方の表示になる（実機で確認）。
- **モデルは `sonnet` 固定**（賢さよりトークン量を優先）。codex-acp は別環境で使うので据え置き。`mode: "plan"` を入れてあり、新しいセッションはプランモードで始まる。
- **Markdown だけ別設定**: `soft_wrap: editor_width`、`tab_size: 2`、`hard_tabs: true`、`format_on_save: off`、`remove_trailing_whitespace_on_save: false`。Obsidian の `app.json` は `tabSize: 2` で `useTab` 未設定（既定でタブ字下げ）。
- **`file_scan_exclusions` に `**/.obsidian/plugins` と `**/.obsidian/workspace*.json` を足す**。`.obsidian/snippets` は除外しない（Zed から CSS を編集できる）。このキーは既定の除外リストを上書きするので、足すときは既定を再掲する。
- **チャット画面の見出し緑・強調オレンジは諦める**。チャットの Markdown は `MarkdownStyle` で描画され、見出しはフォントサイズだけ、強調の専用項目は見つからなかった（`crates/markdown/src/markdown.rs` を確認。ソース全文は未読なので仮説）。コードブロックの中身だけがテーマの `syntax` 色に従う。強調色は Obsidian 側の CSS スニペットで表現する。
- Vim は1週間オフにして試す。

### Facts

- `agent` の主な設定: `dock`、`use_modifier_to_send`、`play_sound_when_agent_done`、`notify_when_agent_waiting`、`show_turn_stats`、`message_editor_min_lines`、`limit_content_width` / `max_content_width`（既定 850）、`threads_sidebar`、`single_file_review`、`auto_compact`（既定 90%）。`default_model` は Zed 内蔵エージェント用で、claude-acp には効かない。根拠は Zed の `assets/settings/default.json`（main、2026-10-04 に取得）。
- スレッドをエージェントパネルのタブにする設定は無い（`threads_sidebar` は位置と自動表示のみ）。
- 設定していないもの: IME の挙動（Zed に項目なし）、全角文字の幅（フォント依存、[[fonts]]）。

### Gotchas

- **テーマ JSON の重複キー**（`link_text.hover` を二重に書いた）。テーマは Zed のスキーマ（`https://zed.dev/schema/themes/v0.2.0.json`）違反があると、警告が出るか読み込まれない。
- **`%APPDATA%\zed\themes` が空の実ディレクトリだと、dotfiles のリンクスクリプトが `[ERR]` を出す**。空であることを確認して削除し、ジャンクションにした。
- **GitHub のコード検索ページは未ログインでは取得できない**。Zed のソースを読むときは `raw.githubusercontent.com` のファイル URL を使う。

### ハイライトが消えたときの切り分けと復旧（2026-11-03）

- Principles:
  - ハイライトが消えたら、テーマのせいにする前に、文字列やコメントを含む全要素が無色かを見る。テーマの違いなら文字列やキーワードの色は変わっても消えない。全部が無色なら言語そのものが読み込めていない。
  - 言語の読み込み失敗は、画面ではなく `Zed.log` で確かめる。`failed to load language <名前>` としてログにだけ残る。
  - 壊れた拡張は `extensions\installed\<名前>` を消して再取得させる。拡張は Zed が自動生成するキャッシュで、`auto_install_extensions` に載っていれば、再起動で入り直す。
- Decisions:
  - **標準の Gruvbox Dark と自作の Material Gruvbox Dark を、テーマセレクタ（Ctrl+K Ctrl+T）で行き来する**（2026-11-03）。根拠: Material は低コントラストで、この環境では暗すぎて見えない。標準は見えるが明るい。状況で使い分けたい（ユーザーの要望）。却下案: 中間の明るさの第 3 テーマ（必要になったら足す）／システムのライト・ダーク設定への連動（ライト・ダークの意味とずれる）。
  - **`theme_overrides` は、行き来する両方のテーマ名のキーに、同じ内容を書く**（2026-11-03）。根拠: テーマ名ごとのキーで効くので、片方にしか書かないと切り替えた側で上書きが消える。却下案: なし（実機で両テーマに効くことを確認した）。
- Facts:
  - `%LOCALAPPDATA%\Zed\extensions\installed\powershell` の `brackets.scm` `indents.scm` `outline.scm` と、`html` の `.scm` 5 個が、中身すべて NUL（0x00）になっていた。`.wasm` や `highlights.scm`（PowerShell）は無事だった（確認: 2026-11-03、根拠: バイト列の先頭が `00` かの検査）。
  - そのときの `Zed.log` は、`failed to load language PowerShell: Error loading brackets query … Query error at 1:1. Invalid syntax`。1 つのクエリが壊れるだけで、その言語全体が読み込めない（Zed.log）。
  - 2 拡張の `installed` ディレクトリを削除して Zed を再起動すると、`.ps1` のハイライトが戻り、両テーマで `theme_overrides` も効いた（確認: 2026-11-03、根拠: ユーザーの目視）。
  - NUL 埋めの原因は、クラッシュなどで書き込みが途中で切れたこと（仮説）。
- Gotchas: テーマ変更の直後に `.ps1` のハイライトが全部消えたが、原因はテーマではなく拡張のキャッシュ（`.scm`）の NUL 埋めで、時期が重なっただけ。`Zed.log` で `failed to load language` を探し、壊れた拡張の `installed\<名前>` を削除して再起動する。ほかの拡張も、`.scm` が全部 NUL でないか検査する。

### 未確認（仮説）

- Zed を再起動しての見た目。`tool_permissions` のパターンが claude-acp のツール名と一致して効くか。

## Windowsでの配置

2026-10-01 時点で確認済み。

| パス | 中身 | 管理 |
|---|---|---|
| `%APPDATA%\Zed\settings.json` / `keymap.json` | 設定 | dotfiles |
| `%APPDATA%\Zed\AGENTS.md` | Zed全体のエージェント向けルール | 未管理 |
| `%LOCALAPPDATA%\Zed\extensions\installed\` | extension本体（このPCでは `html` と `powershell`） | しない |
| `%LOCALAPPDATA%\Zed\extensions\index.json` | 自動生成の索引 | しない |
| `%LOCALAPPDATA%\Zed\external_agents\registry\` | ACPエージェント本体（npx経由） | しない |
| `%LOCALAPPDATA%\Zed\node\` | Zed同梱のNode（v24.11.0） | しない |
| `%LOCALAPPDATA%\Zed\threads\threads.db` | Zedのスレッド履歴 | しない |

- Zedには「インストール済みextensionの一覧」を書いた設定ファイルはない。
- `powershell` はPowerShellのextension（`id = "powershell"`、リポジトリは zed-extensions/powershell）。`html` はZedが標準で入れるもの。
- `threads.db` は 2026-08-13 から更新されていない。Claude AgentのACPチャットはここではなく、Claude Code側に保存される（[[claude-code-storage]]）。

## Decisions

### extensionは `auto_install_extensions` で管理する（2026-10-01）

- 根拠: 起動時に不足分を自動インストールしてくれる。すでにGit管理している `settings.json` 1ファイルで済む。
- 却下案: `extensions\installed\` や `index.json` をdotfilesに入れる。Zedが自動生成する本体・キャッシュで、管理に向かない。

### ACPエージェントは `agent_servers` の記録だけで管理する（2026-10-01）

- 根拠: `agent_servers` はセットアップ時に `settings.json` へ記録済みで、本体は必要なときに自動取得される。
- 却下案: `external_agents\` をGit管理する。自動生成のキャッシュなので不要。

## 仮説（未検証）

- 新しいPCで `auto_install_extensions` により `powershell` が自動で入る。
- 新しいPCで `agent_servers` から2つのエージェントが自動取得される。ClaudeとCodexへのログインはPCごとに必要と思われる。

## Open Questions

- `%APPDATA%\Zed\AGENTS.md` もdotfilesで管理するか。
- `tool_permissions` の `always_deny` / `always_confirm` が claude-acp で実際に効くか。承認を Claude Code に一本化した運用感（確認が足りない/多すぎないか）。
- チャット画面の見出しや強調に色を付ける方法が、本当に無いか。

## Next Actions

- 別のPC、またはextensionを消した状態で、`powershell` が自動インストールされるか確認する。
- Zed を再起動して、テーマ・送信キー・パネル配置・Markdown の見え方を確認する（2026-10-04 の設定変更後）。

## Related

- [[zed-acp]]
- [[terminal-cursor-blink]]
- [[fonts]]
- [[claude-code-storage]]
- [[vscode-workspace]]
