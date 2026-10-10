---
type: knowledge
title: Zed ACP
status: active
tags:
  - tool/zed
  - acp
  - setup
  - ai/codex
  - ai/claude
  - tool/powershell
  - windows
aliases:
  - Zed ACP
created: 2026-09-26
updated: 2026-10-08
sources:
  - Claude Code conversation "Claude Code のセッション履歴の復元" (2026-10-07。Zed のスレッドの復元)
  - Claude Code conversation "Zed の設定を最適化する（目の負担軽減・claude-acp・Obsidian 併用）" (2026-10-04)
  - ChatGPT conversation "Zed ACP ハンズオン" (2026-09-26)
  - ChatGPT conversation "Zed ACPとAI横断ナレッジワークフロー" (2026-10-02)
  - Claude conversation "ZedのACP経由でClaudeが起動しない問題(PowerShellプロファイルが原因)" (2026-10-02)
  - "%APPDATA%\\Zed\\settings.json、PowerShellプロファイル、Zedのexternal_agents（2026-10-02 に確認）"
---

# Zed ACP

## Purpose

ZedをAI開発の統合UIとして使い、複数のExternal AgentをACP経由で接続する。

ZedのExternal AgentsはACPを介して別プロセスとして動作し、認証・モデル・課金・ネイティブ設定などは基本的に各Agent側が管理する。ZedはAgent Panel / Threads Sidebarでそれらをホストする。

## Current Agents

バージョンは 2026-09-26 時点。

### Codex

- ACP Registryからインストール
- Version: 1.13.1
- ChatGPT認証を使用
- 最小通信テスト成功

### Claude Agent

- ACP Registryからインストール
- Version: 0.81.2
- Claude Subscription認証を使用
- 最小通信テスト成功
- ACPアダプタ `@agentclientprotocol/claude-agent-acp` は、2026-10-02 の確認で 0.85.1（`external_agents\registry\npx\claude-acp`）。2026-10-02 のトラブル対応時のメモでは 0.84.0 で、Registryの更新で上がっている。
- `settings.json` で `claude-acp` の `default_config_options.model` を `"sonnet"` にしている（2026-10-02 確認）。
- アダプタがClaude Code本体を内包しているため、ターミナルに `claude` コマンドが無くても（Claude Desktopだけでも）起動できる。

## Setup Steps

1. ZedのACP RegistryからAgentをインストールする。
2. 認証する。
   - Codex: ChatGPT認証
   - Claude Agent: `/login` を実行し、`Claude Subscription` を選ぶ
3. 最小通信テストを送る。

```text
Hello. Reply with exactly: ACP connection OK
```

期待する応答:

```text
ACP connection OK
```

Registryからインストールすると、`settings.json` に次の設定が入る（2026-09-26 に確認）。

```json
"agent_servers": {
  "claude-acp": { "type": "registry" },
  "codex-acp": { "type": "registry" }
}
```

2026-10-02 時点の実物では、`claude-acp` に `"default_config_options": { "model": "sonnet" }` が加わっている。`"type": "registry"` のままでも `env` を追記して環境変数を渡せる（今回は不要だった）。

## Setup Pattern

```text
Zed
  |
  +-- ACP --> Codex
  |             |
  |             +-- ChatGPT authentication
  |
  +-- ACP --> Claude Agent
                |
                +-- Claude Subscription authentication
```

## Important Boundary

ACPはAIサービス間の会話履歴同期プロトコルではない。

ACPの役割は、

```text
Editor / Client
      |
     ACP
      |
External Agent
```

というAgent接続。

したがって、ZedのACPセッションをChatGPT通常チャット履歴やClaude通常チャット履歴へ自動同期する仕組みとは考えない。

## Zed Thread History

Zedは設定済みExternal Agentから既存ThreadをImportできる。

これは、

```text
External Agent
      ↓
     ACP
      ↓
Zed Thread History
```

という方向。

### スレッドの実体と、作業フォルダが旧パスのときの復元（2026-10-07 追記）

作業フォルダを移したあと、Zed のエージェントパネルで、移動前のスレッド（アーカイブ済みを含む）を開けるようにした。開けなかった原因は、Zed が覚えている作業フォルダが旧パスのままだったこと。Claude 側の履歴（jsonl）の復元は [[claude-code-storage]]。

**Principles**

- Zed のスレッドは、会話の中身（エージェント側の jsonl）と、一覧の管理情報（Zed 側の DB）の2か所に分かれる。復元は両方の整合を見る。理由: 片方だけ直すと、一覧に出ても開けない、または開けても一覧に出ない。
- アプリの内部 DB は、アプリを終了してから書き換える。更新の前に、WAL を含めてバックアップする。理由: 起動中は DB が更新され続けていて、書き換えと競合する。
- アプリの中で動くエージェントが、そのアプリの終了を要する作業をするときは、終了を待って自動で実行するスクリプトを別プロセスで起動する。理由: アプリを閉じるとエージェントも止まり、終了の報告ができない。

**Decisions**

- **Zed の `sidebar_threads` の `folder_paths` と `main_worktree_paths` を、各セッションの現在の `cwd` に更新する**（2026-10-07）。根拠: Zed は `folder_paths` を作業フォルダとしてエージェントを起動し、エージェントはその `cwd` から対応する jsonl を探す。旧パスが残ると、エージェントの起動か、jsonl の検索で失敗する。ユーザーが、Zed を終了して実行することを了承した。却下案: 新しいパスのプロジェクトでスレッドを作り直す（過去の会話が使えない）。

**Facts**

- スレッド一覧の実体は `%LOCALAPPDATA%\Zed\db\0-stable\db.sqlite` の `sidebar_threads` テーブル。列は `thread_id` `session_id` `agent_id` `title` `updated_at` `created_at` `folder_paths` `archived` `main_worktree_paths` など（確認: 2026-10-07、根拠: DB のコピーを sqlite で読んだ。2026-10-08 に、DB のコピーを読み取り専用で開いて列を再確認）。
- `agent_id` は `claude-acp` と `codex-acp`。2026-10-07 の記録は92件（Claude 61、Codex 31）、アーカイブ済みは66件。2026-10-08 の実測は Claude 70（アーカイブ 56）、Codex 31（アーカイブ 30）で、その後もスレッドが増えている。
- Claude のスレッドの `session_id` は、`~\.claude\projects\<cwd 由来>\<ID>.jsonl` のファイル名と一致する。61件中56件が一致し、5件は jsonl が無かった（うち2件は `session_id` が空の空スレッド）（確認: 2026-10-07、根拠: DB とファイル名の突き合わせ）。
- `%LOCALAPPDATA%\Zed\threads\threads.db` は、2026-08-13 から更新されていない（確認: 2026-10-07、根拠: ファイルの更新日時。2026-10-08 にも同じ日時）。現在の一覧に使われていないかは、未確認（仮説）。
- `%LOCALAPPDATA%\Zed\logs\Zed.log` に、エージェントの起動の段階（`session/create` の `validate-cwd` `read-transcript` `resume-transcript`、`session/load` の `session-ready` `replay`）が出る（確認: 2026-10-07、根拠: ログの内容）。
- アーカイブは `archived` フラグで、jsonl は消えない。履歴（時計アイコン）から開くと復元される。今回の DB 更新では `archived` は変えていない（確認: 2026-10-07、根拠: 更新前後の DB の比較とユーザーの報告）。
- Zed のスレッド履歴は、`ctrl-alt-j` のサイドバーの時計アイコン、またはコマンド `agents sidebar: toggle thread history` で開く。アーカイブは、スレッドにカーソルを合わせたアイコンか `shift-backspace`（確認: 2026-10-07、根拠: 公式ドキュメント `zed.dev/docs/ai/agent-panel` と `external-agents`）。
- 別プロセスの `Start-Process pwsh -WindowStyle Hidden` は、Zed を閉じても生き残り、終了を検知して処理を実行した（確認: 2026-10-07、根拠: ログに `Zed exited, running fix` と結果が残った）。
- 2026-10-08 に、`folder_paths` に `vault` を含む行が37件残っていた（根拠: DB のコピーの集計。内訳〔Codex の31件か、移動後に作られたものか〕は未確認）。

**Gotchas**

- **旧パスのスレッドを開くと、`failed to spawn command "…pwsh.exe" "-C" "…node.exe '…claude-agent-acp\dist\index.js'"` で失敗する**: Zed が覚えている作業フォルダ（`folder_paths`）が、移動前のパスで存在しない（仮説。パスを直したあとに開けたことから推定）。Zed を終了してから、`sidebar_threads` の `folder_paths` を、セッションの現在の `cwd` に更新する。
- **Zed の中のエージェントから、Zed の DB を直したい。Zed を閉じると、エージェントも止まる**: エージェントが Zed の子プロセスとして動いている。Zed の終了を待って、バックアップと更新を行うスクリプトを、別プロセスで起動する。結果はログファイルに残し、Zed の再起動後に確認する。

## Decisions

### Claude AgentはClaude Subscription認証を使う（2026-09-26）

- 根拠: 定額のClaude契約を使うため。
- 却下案: Anthropic Console（API従量課金）。

### 承認は Claude Code に一本化し、Zed 側は安全網だけ持つ（2026-10-04）

- 決めたこと: `agent.tool_permissions.default` を `allow` にする。Zed 側には `always_deny`（`.env`、`secrets/`、`*.pem`、`*.key` の編集）と `always_confirm`（`git reset --hard`、`git push --force`）だけ残す。
- 根拠: Zed の `default.json` の `tool_permissions` のコメントに「外部エージェント（独自の権限モードを持つもの）では、Zed の `deny` と `confirm` が優先され、エージェント側の権限は Zed が許可するときだけ使われる」とある（2026-10-04 に確認）。既定の `confirm` のままだと二重確認になる。
- 却下案: `confirm` のまま運用する。
- 未確認: `always_deny` / `always_confirm` のパターンが claude-acp のツール名と一致して実際に効くか。

### 送信は Ctrl+Enter、起動モードと既定モデルは設定で決める（2026-10-04）

- `agent.use_modifier_to_send: true`: IME の変換確定の Enter で送信されるのを防ぐ。
- claude-acp のモデルと起動モードは `agent_servers.claude-acp.default_config_options`（`model`、`mode`）で決める。`mode: "plan"` を入れると、新しいセッションがプランモードで始まる。`model` は `sonnet` 固定（トークン量を優先）。
- 設定の全体は [[zed-dotfiles]]。

## Gotchas

### Codex: `Missing optional dependency @openai/codex-win32-x64`

- 状況: Codex初回起動時に発生。PowerShellからは `node` / `npm` が使えない環境だった。
- 原因の見立て: ZedのACP Registryは自前のNode.js環境でAgentを動かすため、システムにNode.jsがないこと自体は問題ではない。インストールが不完全だった可能性が高い。
- 解決: Codexを再インストールしたら解消した。

### Claude Agent: `/login` が入力候補に出ない

- 状況: `/login` の候補表示に出てこない。
- 解決: `/login` を直接入力して実行すると認証画面が出る。

### Claude Agent: 認証直後の `Session not found`

- 状況: 認証後、最初のThreadで会話を始めると `An Error Happened / Session not found` が出る。
- 解決: `+` から新しいThreadを作ると会話できる。
- 原因は未特定（Thread固有の状態かACP側の一時的な問題かは未確認）。

### Claude Agent: `Incoming transport closed`（`session/new`）で起動しない

- 状況: Windowsで、Claude Agentを起動すると認証プロンプトも出ず、いきなり「fail to launch」になる。ACPログ（`dev: open acp logs`）では `initialize` は成功し、`method: session/new` の段階で `Incoming transport closed`。
- 原因: PowerShellプロファイルの16行目 `Set-PSReadLineOption -PredictionViewStyle ListView` が、非対話の起動で失敗していた（"console output doesn't support virtual terminal"）。`ListView` はANSI/仮想ターミナルによる画面描画が要り、パイプ上では動かない。原因は `zed: open log` に出ていた（ACPログの `initialize` 応答だけでは分からない）。
- 解決: プロファイルの先頭に、非対話起動なら抜けるガードを入れる。
  ```powershell
  if ([Console]::IsOutputRedirected -or [Console]::IsInputRedirected) { return }
  ```
  該当行だけをコメントアウトしても開通したが、プロンプト装飾や `zoxide init` など他の対話向けの行が同じ問題を起こしうるので、恒久策はガード。
- 実物との照合（2026-10-02）: `profile.ps1` の2行目にこのガードがある。`profile.ps1` はdotfilesへのシンボリックリンク（`C:\vault\repos\github.com\yuzucha16\dotfiles\profile.ps1`）。ガードの前のコメントは「日対話式」（「非対話式」の誤字）。`PredictionViewStyle` の行はガードの後ろにあり、そのまま残っている。
- 副作用: プロファイルでPATHや環境変数を設定していると、非対話起動では反映されない。環境変数として設定する。
- 切り分けで誤誘導されやすかった点: `claude` コマンドが無いこと、Claude Desktopのみのインストール、`CLAUDE_CODE_GIT_BASH_PATH` の設定は、原因ではなかった。`claude-agent-acp` を手動起動しても入力待ちになるだけで、`session/new` まで進まず切り分けにならない。
- 認証切れの場合はZedがログイン導線を出す。それが出ない「いきなりクラッシュ」は、プロセスの異常終了を疑う。
- プロセスの関係: Zed → node（claude-agent-acp、stdin/stdoutのJSON-RPC。Zed同梱のNode v24.11.0）→ Claude Code本体 → pwsh（セッション作成時に起動）。
- 仮説（未確認）: プロファイルのエラーや装飾出力が、Claude Code側が解析するシェル出力に混ざった、またはシェル初期化の失敗が致命的に扱われ、`session/new` 中にプロセスが終了してZedからは transport closed としか見えなかった。
- 一般的な落とし穴（今回の原因ではない）: WindowsのClaude CodeはGit Bashを要求する。Scoopのgitはシム（`scoop\shims\git.EXE`）なので、`git.exe` からの相対位置で `bash.exe` を探す実装だと見つからない可能性がある（仮説）。
- 今後ACP/エージェント系の起動で原因不明の失敗が出たら、まずシェルのプロファイル出力を疑う。

### Agentの作業フォルダはZedのプロジェクトのルート

- 状況: チャットで `cd` しても作業フォルダは変わらず、そのフォルダの `CLAUDE.md` / `AGENTS.md` も読まれない。
- 解決: 作業したいフォルダをZedのプロジェクトとして開いてから、新しいThreadを作る（[[claude-code-storage]]）。

### 通信ログの確認

ACPの通信ログはZed Command Paletteの `dev: open acp logs` で確認できる。

## Open Questions

- Claude Agentで `session/new` が失敗したとき、どのプロセス（Claude Codeのシェルスナップショットか、Zedの起動処理か）がpwshを起動してプロファイルを読ませたのか。接続が切れた直接の理由は出力の混入か、シェル初期化失敗の扱いか。
- プロファイル内に、他にも非対話で問題を起こす行（starship、PSFzf、scoop-completionのimportなど）があるか。現在はガードより後ろに置いてあるので、起動では読まれない。
- `pwsh -NoProfile -c "..."` と `pwsh -c "..."` の出力を比べ、プロファイルが余計な出力を出していないか確認する。
- Zed上のClaude / Codexセッションの保存場所とImport Threadsの挙動を、実環境でどこまで活用できるか（[[claude-code-storage]]）。
- Codex のスレッド（31件）にも、同じ旧パスの問題があるか（2026-10-07 時点で未確認。2026-10-08 の `vault` を含む37件との関係も未確認）。
- アーカイブを解除する専用の操作があるか（未確認。履歴から開けば復元できることは確認した）。

## Next Actions

- Codex のスレッドを開いて、旧パスで失敗するか確認する（2026-10-07 時点）。

## Related

- [[ai-development-workflow]]
- [[zed-vim]]
- [[zed-dotfiles]]
- [[claude-code-storage]]

## Reference

- Zed External Agents:
  https://zed.dev/docs/ai/external-agents
- Zed Agent:
  https://zed.dev/docs/ai/agents
- Agent Settings:
  https://zed.dev/docs/ai/agent-settings
