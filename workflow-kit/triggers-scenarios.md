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
| S17 | ターミナルのカーソルの点滅を止める | カーソル 点滅 | `exmem/lessons/terminal-cursor-blink.md` | 案（保留用） |
| S18 | VS Code の拡張機能を整理する | VS Code 拡張機能 | `exmem/lessons/vscode-workspace.md` | 案（保留用） |
| S20 | 作業を新しいセッションに引き継ぐ | 引き継ぎ 新しい会話 セッション | `exmem/lessons/session-handoff.md` | 案（保留用） |
| S21 | 人が読む手順書・理解ガイドを新しく作る | 手順書 理解ガイド クイックリファレンス | `exmem/lessons/reference-doc-types.md` | 案（保留用） |
| S22 | Claude Code のチャット履歴やメモリの保存場所を知りたい | チャット履歴 メモリ 保存場所 | `exmem/lessons/claude-code-storage.md` | 案（保留用） |
| S23 | fzf のキー割り当てを調べる | fzf キー割り当て Ctrl-R | `exmem/lessons/shell-fzf-keybindings.md` | 案（保留用） |
| S24 | 履歴を保ったまま、サブディレクトリを別リポジトリに切り出す | 切り出し サブディレクトリ 履歴 | `exmem/lessons/git-subdirectory-split.md` | 案（保留用） |
| S25 | AI の出力のブレを抑える | 出力 ブレ 校正 | `exmem/lessons/ai-output-consistency.md` | 案（保留用） |
| S26 | Power Automate で業務を自動化する | Power Automate Office Scripts | `exmem/lessons/power-automate-office-automation.md` | 案（保留用） |

S13〜S26 は、`triggers:` を付ける前の言葉で、依頼文に自然に出る言い方で書いた（「保留用」= `triggers` の付与に使わず、後から測るための場面。S14 は S01 の言い換え）。ただし、書いた AI（私）は S01〜S09 の `triggers:` も書いたので、完全な盲検ではない。


## 盲検に近い再測定（2026-10-25。Next Actions 2）

`triggers:` を読まずに書いた依頼文 18 件（B01〜B18）。期待ノートはファイル名だけから選び、S01〜S26 が指していないノートを中心にした。測り方は本番の経路（`python -I workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"`、既定の上位 5 件）で、期待ノートの順位を見る（`mdreach.py` の表ではない。ID を B にしたので `mdreach.py` は読まない）。

- 書いた AI（私）はファイル名を見ており、過去のセッションの AI が `triggers:` を書いたので、完全な盲検ではない。ユーザーが場面を足すと確かさが上がる。

| ID | 依頼文（そのまま渡した） | 期待ノート | 順位 / 出た件数 |
|---|---|---|---|
| B01 | WSL からWindows側のフォルダのファイルを編集すると遅いので、どこに置けばいいか | `exmem/lessons/wsl-file-placement.md` | 1/5 |
| B02 | Obsidian のテーマと文字の大きさを変えたい | `exmem/lessons/obsidian-appearance.md` | 1/3 |
| B03 | 新しいPCで Obsidian の Vault を開いて同期したい | `exmem/lessons/obsidian-vault.md` | 1/5 |
| B05 | Notepad++ で正規表現置換をしたい | `exmem/lessons/notepad-plus-plus.md` | 1/1 |
| B06 | ls や grep の代わりになる新しいコマンドを入れたい | `exmem/lessons/modern-cli-tools.md` | 1/1 |
| B07 | 1台のPCにWindowsとUbuntuを両方入れて起動を選べるようにしたい | `exmem/lessons/linux-multiboot-setup.md` | なし |
| B08 | Zed から Claude Code をエージェントとして使いたい | `exmem/lessons/zed-acp.md` | 1/5 |
| B09 | Claude Code にサードパーティのプラグインを入れていいか | `exmem/lessons/claude-code-external-plugins.md` | 4/5 |
| B10 | このリポジトリ用の .claude/settings.json を作る | `exmem/lessons/claude-code-project-settings.md` | 1/5 |
| B11 | Cowork と Claude Code のどちらを使うべきか | `exmem/lessons/claude-code-vs-cowork.md` | 4/4 |
| B12 | bashrc の起動が遅いので速くしたい | `exmem/lessons/dotfiles-shell-tuning.md` | 2/2 |
| B13 | 組込みCのコードがMISRAの制約を守っているか確認したい | `exmem/lessons/embedded-c-constraint-checks.md` | 1/1 |
| B14 | 新しい案件のフォルダを Projects と Areas のどちらに作るか | `exmem/lessons/para-operations.md` | 1/2 |
| B15 | TLS 検査のあるプロキシで証明書エラーが出て pip や npm が通らない | `guides/explain/ssl-inspection.md` | 1/3 |
| B16 | 長いセッションだとコストが増えるのはなぜか | `guides/explain/claude-code-cost-session-size.md` | 1/2 |
| B17 | 部屋で Word を PDF に変換したい | `guides/explain/ai-room-convert-tools-explain.md` | 2/2 |
| B18 | 調べ物のやり方を決めて、ネットで調査して比較表を作って | `exmem/lessons/research-method.md` | 3/3 |

結果: 上位 5 件に入った 17/18、1 位 12/18。取りこぼしは B07（「両方入れて起動を選べる」。ノートの語は `デュアルブート` `マルチブート` など名詞だけ）。1 位でないのは B09・B11（`Claude Code` の 1 語が当たる他のノートと同点で、パス順で後ろ）、B12、B17、B18。並べ方は、当たった語の数 → 当たった語の最長の長さ → パス（`find_knowledge.py` の `lookup_triggers` を読んで確かめた）。

同じ経路で S01〜S26 の「場面」の文（作業の言葉の列ではなく、依頼の例の文）も測った（lessons が期待の 24 件）: 1 位 17/24、上位 5 件に入らないのは S16（「Zed のキー割り当てを変える」。6 位）だけ。`mdreach.py` の「届かない 1/26」は語の列で測った数で、依頼の文で測ると順位の問題が見える。

並べ方の試し（scratch で試算。`find_knowledge.py` は変えていない）: 語に「付いているノートの数が少ないほど重い」重み（IDF）を付けると、B は 1 位 12→11/18（B09・B11・B12 は上がるが B01 が下がる）、S は 1 位 17→14/24。今の並べ方のほうがよい。

改善の案（未決。ユーザーが決める）:

1. B07: `linux-multiboot-setup.md` の `triggers:` に、動詞の言い方（例: `起動を選べる` `両方入れる`）を足す（15 語の枠に 6 語の空き）。
2. S16: `zed-vim.md` の `triggers:` に `キー割り当て` が無い（`キーマップ` `キーバインド` はある）。`Zed` の 1 語で 5 本と同点になり、パス順で 6 位。`キー割り当て` を足せば 2 語で 1 位になる（確かめた: `--top 7` の出力）。
3. 並べ方は変えない（上の試算）。

## 追加の候補（未記入）

- `log-history.md` と `decisions.md` に、ほかの見落とし（「知らずに作って、後で既存の規則に当たった」）があれば足す。S01〜S03 以外は、まだ実際の事例を探していない。
