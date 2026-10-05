# AGENTS.md

<このワークスペースの役割を1〜2行で。例: 業務用 PC の作業場。PARA でこの PC のローカルの作業を管理し、共有ナレッジ（`resources/`）を参照する。>

Obsidian の Vault のトップ。この PC だけのローカルなリポジトリ（remote: <なし / 非公開リポジトリの URL>）。共有ナレッジは `resources/`（別リポジトリ `workbase` の clone）にあり、Vault 全体の規約は `resources/AGENTS.md`。

## 共通ルール

共通ルールの置き場は、このワークスペースの `resources/workflow-kit/`（Windows の標準の場所なら `C:\vault\notes\resources\workflow-kit`）。次の時機に、該当のファイルを読む。

- `docs-rules.md`: 作業を始める前と、`docs/` を更新するときに読む。`docs/` の運用。作業の終わりに `docs/log.md` と `docs/decisions.md` を更新する。
- `knowledge-hook.md`: ユーザーが「ナレッジ化して」と言ったときに読み、実行する（言われたときだけ）。書き込みは `exmem/inbox/` の新規ファイルだけ。
- `setup-hook.md`: ユーザーが「workflowを導入して」と言ったときに読み、実行する（言われたときだけ。このワークスペース配下の作業ディレクトリへの導入の入口）。

上のファイルが読めない場合（`resources/` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `docs/log.md`
2. `resources/AGENTS.md`（Vault 全体の規約）
3. `docs/decisions.md`

## 構成と管理

| パス | 内容 | 管理 |
|---|---|---|
| `areas/` `projects/` `archives/` | PARA。この PC のローカルの作業 | このリポジトリ |
| `docs/` `AGENTS.md` `CLAUDE.md` | この PC の作業ログと規約 | このリポジトリ |
| `resources/` | 共有ナレッジ（`workbase`）。このリポジトリの `.gitignore` で除外する | 別リポジトリ（git 操作は `resources/` の中で行う） |
| `.obsidian/` | Obsidian の設定。dotfiles からのジャンクション。このリポジトリでは追跡しない | dotfiles |

## このワークスペース固有のルール

- <remote の方針に合わせて書く。remote が無いとき: このリポジトリに remote を足さない。push しない（誤って push しないよう、`.git/hooks/pre-push` で止めてある）。>
- ローカル側から共有側（`resources/`）への `[[リンク]]` は張ってよい。共有側のノートから、ローカル側（`areas/` `projects/` `archives/`）へは張らない。他の PC でリンク切れになる。
- この PC のローカルの情報（業務固有のもの、個人的なもの）を、`resources/`（共有）に書かない。`resources/` の変更は、`resources/` の中でコミットする（このリポジトリのコミットには含まれない）。
- `git add -f` で、ignore 済みのファイルを追加しない。
- <その他の固有ルール。無ければ「なし」>

## コミット

- メッセージは `[領域] 変更内容`。`git add` はパスを指定する。
