# 場面の一覧（下書き。2026-10-25）

論点 D の測り方 (a) の入力。各場面で、起点（`CLAUDE.md` が `@` で取り込む `AGENTS.md`、`README.md`、`docs/log.md`）から、作業の言葉が書かれたリンクの行だけを辿り、「読まれるべきノート」に何ホップで着くかを数える。着かない場面が「届かない」。

- 出典の「実際」は、過去に見落としが記録された場面。「案」は AI（私）が、`exmem/exmem-index.md` の題から作った例で、ユーザーの確認が要る。
- 期待ノートと作業の言葉は、ユーザーが足し・直す。着かなかったときは、構造と並んで、場面の書き方も疑う。

| ID | 場面（依頼の例） | 作業の言葉 | 読まれるべきノート | 出典 |
|---|---|---|---|---|
| S01 | works で Windows 用の `.bat` を作る | `.bat` `chcp` 文字化け | `exmem/lessons/shell-script-testing-wsl.md`（後ろの追記節） | 実際（2026-10-20） |
| S02 | アプリの設定ディレクトリ（`.obsidian` など）をどのリポジトリに置くか決める | `.obsidian` 設定ディレクトリ 置き場 | `exmem/lessons/app-config-placement.md`（Gotchas） | 実際（前提の見落とし） |
| S03 | 仕組みの方針を変える・決める | 決定 方針 変更 | `docs/decisions.md`（先に検索する）と `exmem/lessons/human-ai-decision-loop.md` | 実際（先行する決定の見落とし） |
| S04 | `.gitattributes` を足す、改行コードの警告を直す | 改行 LF CRLF `.gitattributes` | `exmem/lessons/git-line-endings.md` | 案 |
| S05 | 履歴を整理するために rebase する | rebase 時系列 | `exmem/lessons/git-rebase-chronology.md` | 案 |
| S06 | GitHub のリリースの成果物を取ってくる | `gh release download` | `exmem/lessons/gh-release-download.md` | 案 |
| S07 | Claude Code の権限の許可を足す | permissions allow deny | `exmem/lessons/claude-code-permissions.md` | 案 |
| S08 | Claude Code を Bedrock につなぐ | Bedrock 認証 モデル指定 | `exmem/lessons/claude-code-auth-providers.md` | 案 |
| S09 | フォントを選んで入れる | フォント 導入 | `exmem/lessons/fonts.md` | 案 |
| S10 | scoop でアプリを入れる・管理する | scoop | `exmem/lessons/scoop-app-management.md` | 案 |
| S11 | ノートの追加・統合で、置き場や書き方を確認する | frontmatter タグ 索引 | `exmem/AGENTS.md` と `exmem/tags.md` | 案 |
| S12 | シェルスクリプトを WSL で試験する | WSL シェル 試験 | `exmem/lessons/shell-script-testing-wsl.md` | 案 |
| S13 | PowerShell で git や外部コマンドを呼ぶと失敗・文字化けする | PowerShell git パイプ エンコード | `exmem/lessons/windows-cli-pitfalls.md` | 案（保留用。2026-10-25 追加） |
| S14 | 日本語のメッセージを出す Windows のバッチファイルを作る | バッチファイル 日本語表示 | `exmem/lessons/shell-script-testing-wsl.md` | 案（保留用。言い換えの確認） |
| S15 | Excel の VBA マクロを AI に作らせる | Excel VBA マクロ | `exmem/lessons/excel-vba-ai-development.md` | 案（保留用） |
| S16 | Zed のキー割り当てを変える | Zed キーバインド Vim | `exmem/lessons/zed-vim.md` | 案（保留用） |
| S17 | ターミナルのカーソルの点滅を止める | カーソル 点滅 | `exmem/lessons/terminal-cursor-blink.md` | 案（保留用） |
| S18 | VS Code の拡張機能を整理する | VS Code 拡張機能 | `exmem/lessons/vscode-workspace.md` | 案（保留用） |
| S19 | 自宅の PC に入れる Linux を選ぶ | Linux ディストロ | `exmem/lessons/linux-distro-selection.md` | 案（保留用） |
| S20 | 作業を新しいセッションに引き継ぐ | 引き継ぎ 新しい会話 セッション | `exmem/lessons/session-handoff.md` | 案（保留用） |
| S21 | 人が読む手順書・理解ガイドを新しく作る | 手順書 理解ガイド クイックリファレンス | `exmem/lessons/reference-doc-types.md` | 案（保留用） |
| S22 | Claude Code のチャット履歴やメモリの保存場所を知りたい | チャット履歴 メモリ 保存場所 | `exmem/lessons/claude-code-storage.md` | 案（保留用） |
| S23 | fzf のキー割り当てを調べる | fzf キー割り当て Ctrl-R | `exmem/lessons/shell-fzf-keybindings.md` | 案（保留用） |
| S24 | 履歴を保ったまま、サブディレクトリを別リポジトリに切り出す | 切り出し サブディレクトリ 履歴 | `exmem/lessons/git-subdirectory-split.md` | 案（保留用） |
| S25 | AI の出力のブレを抑える | 出力 ブレ 校正 | `exmem/lessons/ai-output-consistency.md` | 案（保留用） |
| S26 | Power Automate で業務を自動化する | Power Automate Office Scripts | `exmem/lessons/power-automate-office-automation.md` | 案（保留用） |

S13〜S26 は、`triggers:` を付ける前の言葉で、依頼文に自然に出る言い方で書いた（「保留用」= `triggers` の付与に使わず、後から測るための場面。S14 は S01 の言い換え）。ただし、書いた AI（私）は S01〜S09 の `triggers:` も書いたので、完全な盲検ではない。

## 追加の候補（未記入）

- `log-history.md` と `decisions.md` に、ほかの見落とし（「知らずに作って、後で既存の規則に当たった」）があれば足す。S01〜S03 以外は、まだ実際の事例を探していない。
