# AGENTS.md

<このワークスペースの役割を1〜2行で。例: 業務用 PC の作業場。PARA でこの PC のローカルの作業を管理し、共有ナレッジ（`resources/`）を参照する。>

Obsidian の Vault のトップ。この PC だけのローカルなリポジトリ（remote: <なし / 非公開リポジトリの URL>）。共有ナレッジは `resources/`（別リポジトリ `workbase` の clone）にあり、Vault 全体の規約は `resources/AGENTS.md`。

## 共通ルール

共通ルールの置き場は `$HOME\works\resources\workflow-kit`（WSL: `/mnt/c/Users/<Windows のユーザー名>/works/resources/workflow-kit`）。ユーザーが合言葉（手順書を呼ぶ短い言葉。日本語の別名つき）を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する（言われたときだけ）。`docs-rules.md` は、`docs/` を更新するときと、コミット・push の前に読む。

上のファイルが読めない場合（`resources/` を clone していない PC など）は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `README.md`（窓口。構成と管理。Vault 全体の規約は `resources/AGENTS.md`。`resources/` の作業のときに読む）
2. `docs/log.md`（開始時に読むのはここまで。「期日」の節があれば、今日以前または3日以内の項目を、最初の返答で知らせて判断を求める）
3. `docs/decisions.md` と `docs/log-history.md` は開始時に読まない。何かを決める・変える前に `decisions.md` を検索する。経緯が要るときは `log-history.md` を検索する。

下位の単位の「<名前> の続き」は、kit の `docs-rules.md` の「上の階層で起動して…」に従う。

## 構成と管理

構成の表は `README.md`（`areas/` `projects/` `archives/`、`docs/`、`resources/`、`repos/`、`.obsidian/` など）。`resources/` と `repos/` の各リポジトリは別の git リポジトリで、git 操作はそれぞれの中で行い、作業の前にその `AGENTS.md` を読む。`resources_p/` は PC ローカルの resources（この PC だけの情報の置き場。追跡しない。Vault 側の AI は読み書きしてよく、`areas/` などのような deny はしない）。

## AI 作業部屋（`projects/` `areas/` `archives/` を扱うとき）

- この 3 つの中の作業は、AI 作業部屋（専用の WSL ディストリビューション）の中で行う。Vault 側の AI（この `AGENTS.md` を読む AI）は、`projects/` `areas/` `archives/` を読まない・編集しない。`.claude/settings.json` で `Read` と `Edit` を deny している（雛形: `resources/workflow-kit/templates/workspace/claude-settings.template.json`。安全網であって境界の保証ではない。効くのは、このリポジトリのトップで起動したときだけ）。
- `.claude/` は、プロジェクト固有の規則が要るリポジトリだけ `settings.json` を置いて追跡する。`settings.local.json` は、どのリポジトリでも追跡しない。
- `room`（`resources/workflow-kit/room/`）は人が端末で実行する。AI は実行しない。
- 部屋の使い方と読み替えは `resources/workflow-kit/room/README.md` と `resources/workflow-kit/room-context.md`。
- `.gitignore` に `**/_noai/`（AI に見せない領域。追跡しない）と `!**/ai/out/` を入れる（雛形: `gitignore.template`）。

## このワークスペース固有のルール

- <remote の方針に合わせて書く。remote が無いとき: このリポジトリに remote を足さない。push しない（誤って push しないよう、`.git/hooks/pre-push` で止めてある）。>
- ローカル側から共有側（`resources/`）への `[[リンク]]` は張ってよい。共有側のノートから、ローカル側（`areas/` `projects/` `archives/` `resources_p/`）へは張らない。他の PC でリンク切れになる。
- この PC のローカルの情報（業務固有のもの、個人的なもの）を、`resources/`（共有）に書かない。`resources/` の変更は、`resources/` の中でコミットする（このリポジトリのコミットには含まれない）。
- `git add -f` で、ignore 済みのファイルを追加しない。
- <その他の固有ルール。無ければ「なし」>

## コミット

- メッセージは `[領域] 変更内容`。`git add` はパスを指定する。
