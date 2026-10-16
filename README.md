# workbase

汎用ナレッジと共通機能を育てる共有リポジトリ。通常は、Obsidian Vault の `resources/` として clone して使う（Windows: `$HOME\works\resources`、WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources`）。単独で clone しても自己完結する。規約は `AGENTS.md`。

## 構成

| ディレクトリ | 内容 |
|---|---|
| `exmem/` | AI が今後の参考にするナレッジ（external memory）。判断・原則・落とし穴の記録は `exmem/lessons/` |
| `workflow-kit/` | 作業ディレクトリに導入する共通機能（`docs/` の運用と、合言葉で呼ぶフック。呼び出し表は `hooks.md`）の正本。AI 作業部屋の操作コマンドは `room/` |
| `guides/` | 人（ユーザー）が手順や仕組みを思い出すための文書。`howto/`（手順書）、`explain/`（理解ガイド）、`quickref/`（クイックリファレンス）。入口は `guides/guides-index.md` |
| `topics/` | 大きな取り組み（トピック）を、セッションと端末をまたいで進める置き場。一覧は `topics/topics-index.md`。反映が済んだトピックは `topics/AGENTS.md` の「トピックを終わらせるとき」に従って削除する |

## 入口

- 現在の状態と次にやること: `docs/log.md`
- 下位の単位（トピック、`guides/` など）の続き: 「<名前> の続き」と言う。読み方は `workflow-kit/docs-rules.md` の「読む順番」
