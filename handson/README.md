# ai-handson

AI活用のタスクを、ハーネス6要素の表で設計し、実装し、育てるためのディレクトリ。
PARAの Areas 直下に置いて使う想定(例: `PARA/Areas/ai-handson/`)。

## 構成

```
ai-handson/
├── README.md                    人間向けの説明(このファイル)
├── CLAUDE.md                    Claude Codeへの進め方とルール(自動で読まれる)
├── templates/
│   ├── task-template.md         新しいタスクを作るときの記入テンプレート
│   └── changelog.md             テンプレート自体の改訂ログ
└── tasks/
    └── comms-digest.md          タスクの記入例(1タスク1ファイル)
```

## 各ファイルの役割

| ファイル | 誰が読む | 役割 |
|---|---|---|
| README.md | 人間 | 全体像と使い方 |
| CLAUDE.md | Claude Code | 進め方とルール。毎回自動で読まれる |
| templates/task-template.md | Claude | 新しいタスクを作るときの型 |
| templates/changelog.md | 人間とClaude | テンプレートを育てた履歴 |
| tasks/*.md | 人間とClaude | 個別タスクの設計、実装状況、失敗ログ |

## 使い方

1. このディレクトリで Claude Code を起動する(`ai-handson/` をカレントにして `claude`)
2. 「新しいタスク〇〇を作って。前提は…」と依頼する。Claudeが `tasks/〇〇.md` を作り、6要素の表を埋める
3. 表の「実装担当」に従って実装する(AIができるものはAI、権限が絡むものは人間)
4. 詰まった点や失敗を、そのタスクファイルの「失敗ログ」に書き、Claudeに表の更新を依頼する
5. タスクが2〜3個たまったら、Claudeに「抽象化タスク」(`templates/changelog.md` 参照)を依頼し、テンプレートを改訂する

## 注意

- 個別タスクの記録は `tasks/` に集める。テンプレートや進め方を直接いじるのは、抽象化タスクのときだけにする
- メール由来のダイジェストなど外部由来のテキストをAIに読ませる場合は、書き込み権限を持たせない構成にする
