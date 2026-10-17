# AGENTS.md

`workbase` 全体の規約。汎用ナレッジと共通機能を育てる共有リポジトリ。Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。
各ディレクトリに固有のルールがある場合は、そのディレクトリの `AGENTS.md` / `CLAUDE.md` が優先される（例: `exmem/AGENTS.md`）。

ノートの読み書きは、エージェントがファイルを直接行う。人間は Obsidian で閲覧・編集する。

構成は `README.md`。このリポジトリは単独で clone しても自己完結する。作業ディレクトリに期待することは、`workflow-kit/hooks.md` の「契約」だけ。通常は Obsidian Vault の `resources/` として clone して使う。Vault 全体（PARA の各区分、PC ごとのローカルの作業）は、このリポジトリの外にある。

## 共通ルール

共通ルールの置き場は `workflow-kit/`（`$HOME\works\resources\workflow-kit`）。ユーザーが合言葉（手順書を呼ぶ短い言葉。日本語の別名つき）を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する（言われたときだけ）。`docs-rules.md` は、`docs/` を更新するときと、コミット・push の前に読む。読めない場合は、記憶で代用せず、ユーザーに伝えて止まる。

## 読む順番

1. `README.md`（窓口）
2. `docs/log.md`（開始時に読むのはここまで。「期日」の節があれば、今日以前または3日以内の項目を、最初の返答で知らせて判断を求める）
3. `docs/decisions.md` と `docs/log-history.md` は開始時に読まない。何かを決める・変える前に `decisions.md` を検索する。経緯が要るときは `log-history.md` を検索する。

下位の単位（トピック、`guides/` など）の「<名前> の続き」は、`workflow-kit/docs-rules.md` の「上の階層で起動して…」に従う。

## wrap の記録先

`wrap`（`workflow-kit/wrap-hook.md`）は次を使う。

- **既定の対象**: トピックの続きで作業したときは、そのトピックの `docs/`。トピックの外で作業したときは、このリポジトリ直下の `docs/`。`workflow-kit/` `exmem/` `guides/` などの kit 改善の記録は、`topics/kit-growth/docs/`（kit の改善の受け皿）。

## 共有の範囲

- このリポジトリの内容は、すべて共有（Git 管理）する。機密、勤務先固有の情報、PC ごとのデータを入れない。このリポジトリは公開（PUBLIC。2026-10-16 に確認）なので、世界に読まれる前提で書く。
- dotfiles の挙動（スクリプトの中身・配置）をこのリポジトリに書かない。名前とリンクで指す。依存は dotfiles → workbase の一方向だけ（理由は `exmem/lessons/app-config-placement.md`）。
- ローカルのデータ（勤務先・個人の作業）は、このリポジトリの外に置く。このリポジトリのノートから、外のファイルへ `[[リンク]]` を張らない。他の PC でリンク切れになる。
- `.claude/settings.local.json` は端末ごとの許可設定なので、追跡しない（`.gitignore` 済み）。

## リンク

- ノート間のリンクは wikilink（`[[名前]]`）。ファイル名はリポジトリ内（Vault 内）で一意に保つ（最短パスで解決されるため）。

## 書式とコミット

- 改行コードは LF（`.gitattributes` で統一）。
- コミットメッセージは `[領域] 変更内容` の形式（例: `[exmem] ...`、`[workflow-kit] ...`、`[guides] ...`）。
- `git add` はパスを指定する（パスなしの `git add -A` と `git add .` は使わない）。コミット・push の前に、`workflow-kit/docs-rules.md` の「コミットと push」を、そのセッションで読んでいなければ読む（身元・トレーラー・機密の検索もそこに従う）。
- push は、このリポジトリ（`yuzucha16/workbase`。公開）の `main` を、エージェントが行ってよい（2026-10-16 ユーザーの決定。公開のまま）。条件は `workflow-kit/docs-rules.md` の「push」（公開のため、機密の検索を広げる）。禁止のコマンド（`--force` など）は、`workflow-kit/docs-rules.md` の「しないこと」に従う（`settings.json` の deny が機械的に止める）。
