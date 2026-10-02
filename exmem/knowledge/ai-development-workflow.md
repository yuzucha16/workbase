---
type: knowledge
title: AI開発ワークフロー
status: active
tags:
  - workflow
  - knowledge-management
  - context-engineering
  - mobile
  - tool/zed
  - tool/obsidian
aliases:
  - AI開発ワークフロー
created: 2026-09-26
updated: 2026-10-02
sources:
  - ChatGPT conversation "AI開発ワークフロー検討" (2026-09-26)
  - ChatGPT conversation "Zed ACPとAI横断ナレッジワークフロー" (2026-10-02)
  - Claude Code conversation "exmemの整理" (2026-09-26〜2026-10-01)
---

# AI開発ワークフロー

## 1. 目的

モバイルでAIと壁打ちした内容を、PC上のZedで継続・拡張し、最終的に実装や検証へつなげる。

重要なのは、**AIサービス間の会話履歴を同期することではなく、AIをまたいで利用できる知識を共有すること**。

## 2. 基本モデル

```text
モバイル
  ChatGPT / Claude
       |
       | 壁打ち・発散
       v
  inbox（一時置き場）
       |
       | 決定・根拠・ハマりどころを抽出
       v
  knowledge / project context
       |
       v
      PC
      Zed
       |
       +-- Codex ACP
       +-- Claude ACP
       +-- Copilot ACP
       |
       v
  実装・検証・レビュー
```

## 3. 会話と知識の扱い

会話ログは常設の層として持たない。会話は `inbox/` に一時的に置き、知識へ統合したら削除する。

会話ログの価値は主に次の2つであり、これらは知識ファイルの中に残す。

| 会話にあった情報 | 知識ファイルでの置き場 |
|---|---|
| 判断の拠り所になる方針 | `## Principles` |
| なぜそう決めたか・捨てた案 | `## Decisions` |
| 実際に遭遇したエラーと解決方法 | `## Gotchas` |

知識は「現在、何を前提としているか」の記録。

- 決定事項（根拠と却下案を含む）
- 制約
- 設計原則
- 現在の仮説（確認済みの事実と区別する）
- 未解決事項
- 次の検証項目

例:

```text
現時点ではPower Automate + Office Script + SharePointを基本構成とする。
ファイル操作と例外処理はExcel Macroで補完する。
```

元の会話全文が必要になった場合は、各AIサービスの履歴を `sources` から辿る。

## 4. AIをまたぐための原則

AI固有の会話形式や指示形式を知識ファイルに埋め込まない。

### 推奨

```markdown
# Current Context

## Goal
...

## Constraints
...

## Decisions
...

## Open Questions
...
```

### 避ける

```text
Claude専用プロンプト
GPT専用メモリ
Copilot専用命令
```

AIごとの追加指示が必要なら、AI固有の設定ファイルへ分離する。
各エージェントの入口は `AGENTS.md` に一本化し、Claude Code向けの `CLAUDE.md` は `@AGENTS.md` を読み込むだけにする。

## 5. 情報のライフサイクル

```text
壁打ち（モバイル / PC）
  ↓
inbox に保存（テンプレート形式）
  ↓
決定・根拠・ハマりどころ・未決事項を抽出
  ↓
knowledge に統合 → inbox から削除
  ↓
project context（現状・次にやること）
  ↓
AIによる実装・検証
  ↓
結果
  ↓
knowledge / context を更新
```

この構造にすると、AIをClaudeからGPTへ、GPTからCopilotへ変更しても、プロジェクトの知識は残る。

## 6. コンテキストエンジニアリングとの関係

このワークフローでは、MarkdownがAIへの入力コンテキストの中間表現になる。

```text
人間の会話
  ↓
情報
  ↓
構造化されたMarkdown
  ↓
AIのコンテキスト
```

したがって、会話を大量に保存することよりも、**AIが再利用しやすい状態へ情報を変換すること**を重視する。

## 7. 現時点の設計方針

- モバイルは発散・壁打ちに使う
- PCはZedをAI開発の統合UIとして使う
- ACPはZedと外部Agentを接続する層として使う
- MarkdownをAI横断の知識交換フォーマットとして使う
- Git等でMarkdownを同期する
- 会話ログは常設せず、根拠とハマりどころを知識へ統合する
- プロジェクトごとの現在状態を `context.md` にまとめる

## Principles

- オリジナルの仕組みを作るより、既存のお作法（`AGENTS.md`、YAML frontmatter、統制語彙のタグなど）を優先する。
- 会話ログを溜めずに、知識として育てる。会話の価値は「なぜそう決めたか」と「ハマりどころ」に集約される。
- 会話から作ったメモは実物と食い違うことがある。統合時は設定ファイルやコードと照合し、実物を正とする。
- タグは横断的な分類、特定ノートとの関係は `[[リンク]]` で表す。

## Decisions

### D1: AIサービス間の会話履歴同期は目指さない（2026-09-26）

- 決定: Markdownを共通の中間表現とし、知識をAI横断で共有する。
- 根拠: 本当に必要なのは「モバイルでの壁打ちをPCで拡張すること」であり、履歴そのものではない。また、ACPはエディタと外部Agentの接続プロトコルであって、履歴同期の仕組みではない（[[zed-acp]]）。
- 却下案: ZedのACPセッションの会話を、ChatGPT / Claudeアプリの履歴でも見られるように同期する。

### D2: 会話ログを常設の層にしない（2026-09-26）

- 決定: `conversations/` を廃止し、`inbox/` を一時置き場とする。会話の根拠・ハマりどころは知識ファイルの `Decisions` / `Gotchas` に統合する。
- 根拠: 会話と知識を別々に持つと情報量が倍になり、根拠が点在する。会話ログの価値は「なぜ」と「ハマりどころ」にほぼ集約される。
- 却下案: `conversations/` と `knowledge/` の2層で並行管理する（当初案）。実際に、会話から知識への抽出でCodexのエラー対処などが抜け落ちた。

### D3: AI固有の形式を知識に持ち込まない（2026-09-26）

- 決定: Markdown + YAML frontmatter + 通常の見出しを基本とし、AI固有の指示は設定ファイルへ分離する。
- 根拠: AIを変更しても知識資産が残るようにするため。

### D4: モバイルからの保存はObsidian Syncを使う（2026-09-26）

- 決定: モバイルAIの出力を、Obsidianモバイルアプリで `inbox/` に新規ノートとして貼り付ける。Obsidian SyncでPCへ届く。
- 根拠: VaultでObsidian Syncが既に有効になっており、追加の仕組みがいらない。
- 状態: 仮説。モバイルからの保存はまだ試していない。

### D5: タグは統制語彙の階層タグにする（2026-09-26）

- 決定: タグは `tags.md` の語彙から選び、ソフトウェアは `tool/*`、AIは `ai/*` の階層タグにする。`type` / `status` はタグにしない。
- 根拠: 複数のAIが自由にタグを付けると表記揺れ（`zed` / `Zed` / `zed-editor`）が起き、Obsidianでの絞り込みが効かなくなる。階層タグはObsidianで親タグ検索ができ、`colored-tags` で色分けもされる。
- 却下案: 自由タグ。`type` の値をタグにも入れる（プロパティと重複する）。

### D6: エージェントの入口を `AGENTS.md` に一本化する（2026-09-26）

- 決定: 読む順番・書き方・inbox整理の手順を `AGENTS.md` にまとめる。Claude Code向けの `CLAUDE.md` は `@AGENTS.md` の1行だけにする。
- 根拠: Codex・Copilot・Zedが `AGENTS.md` を読む。指示を1か所にして重複と食い違いを避ける。
- 却下案: AIごとに個別の指示ファイルを書く。

### D7: `context.md` を引き継ぎメモとして使う（2026-09-26）

- 決定: `context.md` の先頭に `Current State` / `Next Actions` を置き、作業の終わりに更新する。
- 根拠: 次に作業するAI・端末が、そこから再開できる。

### D8: 知識ファイルの見出しを `Principles` / `Decisions` / `Gotchas` で使い分ける（2026-09-26）

- 決定: `Gotchas` は実際に遭遇したエラーに限定し、方針や一般的な注意点は `Principles` に書く。
- 根拠: Vim移行のinboxメモで、方針的な注意点が `Gotchas` に書かれ、`Decisions` と重複した（[[zed-vim]]）。

### D9: `aliases` に日本語名を入れる（2026-09-26）

- 決定: ファイル名は英語の kebab-case、`aliases` に日本語名・別名を入れる。
- 根拠: Obsidianのリンク補完・検索を日本語で行える。

## Gotchas

### 会話から知識への抽出で情報が抜け落ちた

- 状況: Zed ACPハンズオンの会話にあった、Codexの `Missing optional dependency` エラーの対処と、`/login` が入力候補に出ない件が、知識ファイルに入っていなかった。
- 解決: 知識ファイルに `Gotchas` 欄を設けて移した（[[zed-acp]]）。D2の根拠にもなった。

### inboxメモの内容が実際の設定と食い違った

- 状況: Vim移行のメモでは「`keymap.json` は空」だったが、実際にはターミナル用の設定があった。
- 解決: 実物を正として記録し、食い違いを `Open Questions` に残した（[[zed-vim]]）。統合時に実物と照合する手順を `AGENTS.md` に追加した。

### READMEの構成図が実態とずれていた

- 状況: 存在しない `projects/zed-acp/context.md` が載り、ルートのフォルダ名も実際と違っていた。
- 解決: 構成図を直し、新しいファイルを作ったら README を更新する手順を `AGENTS.md` に入れた。

### 初期案の `conversations/` は採用されなかった

- 状況: 2026-10-02 にinboxへ届いたメモ「Zed ACPとAI横断ナレッジワークフロー」は、`inbox/`・`knowledge/`・`projects/<project>/context.md` に加えて `conversations/` を置く最小構造と、「会話ログと知識を分離する」考えを書いていた。これは2026-09-26 の初期案で、D2で廃止済み。
- 解決: 実物（`inbox/` → `knowledge/` → `projects/`）を正とした。メモの Next Actions にあった `conversations/` の作成は行わない。

## 8. 未決事項

- Obsidian Vaultと開発リポジトリの境界
- AIにどこまで自動整理させるか
- GitとObsidian Syncの使い分け。2026-10-01 からexmemは `areas_shared` リポジトリでGit管理されている（[[obsidian-vault]]）。
- 知識ファイルの `sources` に元の会話のURLを残すか。現状はタイトルと日付のみ。

## Related

- [[obsidian-vault]]
- [[zed-acp]]
- [[ai-harness-concepts]]
- [[ai-handson-framework]]
- [[human-ai-decision-loop]]
- [[ai-development-workflow/context]]
- [[tags]]
