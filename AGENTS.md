# AGENTS.md

`workbase` 全体の規約。汎用ナレッジと共通機能を育てる共有リポジトリ。Claude / Codex / Copilot など、どのエージェントも同じルールで読み書きする。
各ディレクトリに固有のルールがある場合は、そのディレクトリの `AGENTS.md` / `CLAUDE.md` が優先される（例: `exmem/AGENTS.md`）。

ノートの読み書きは、エージェントがファイルを直接行う。人間は Obsidian で閲覧・編集する。

構成は `README.md`。このリポジトリは単独で clone しても自己完結する。作業ディレクトリに期待することは、`workflow-kit/hooks.md` の「契約」だけ。通常は works（Obsidian の Vault）の `resources/` として clone して使う。works 全体（PARA の各区分、PC ごとのローカルの作業）は、このリポジトリの外にある。

## 共通ルール

共通ルールの置き場は `workflow-kit/`（`$HOME\works\resources\workflow-kit`）。ユーザーが合言葉（手順書を呼ぶ短い言葉。日本語の別名つき）を言ったら、そこの `hooks.md` の表に従って手順書を読み、実行する（言われたときだけ）。`docs-rules.md` は `docs/` を更新するときに、`commit-push-rules.md` はコミットの前に、`push-rules.md` は push の前に読む。読めない場合は、記憶で代用せず、ユーザーに伝えて止まる。

## 知識を引く（作業の前）

作業を始める前に、依頼の言葉で `python -I workflow-kit/tools/find_knowledge.py --triggers "<依頼文>"` を実行し、出たノートを読む（`exmem/lessons/`、`guides/explain/`、未統合の `exmem/inbox/` の `triggers:` と照合する。2026-10-25 ユーザーの決定。設計は `topics/md-link-graph/records/design-triggers.md`）。

## 読み込みの量を抑える

読んだ内容は、以後の全応答に乗る（日本語は約 0.47 トークン/バイト。2026-10-26 ユーザーの決定。根拠は `topics/token-cap/records/2026-10-26-review-digest-100k.md`）。

- Grep は、まず `files_with_matches` か `count` で件数とファイル名を見てから、必要なファイルだけ内容を見る。広い語で行の内容つきの出力を一度に取らない（旧名の読み替えの掃除では、1 回 12〜19KB の出力が 3 回あった）。
- ファイルは、必要な節だけ `offset` と `limit` で読む。全文を読むのは、全体を書き換えるときだけ。

## 返答の並び

返答は、ユーザーに求めること・確認してほしいことを最後（一番下）に置き、結論・結果をその直前に置く（ユーザーが下からスクロールして読むため。2026-10-28 ユーザーの決定。試行 1 週間、11-04 に続けるか判断）。フックの報告の順は `workflow-kit/hook-common.md` の「報告の型」。

## 読む順番

1. `README.md`（窓口）
2. `docs/log.md`（開始時に読むのはここまで。期日は `docs/due.md` にあり、開始時には読まない。`review 消化` が拾う。2026-10-29）
3. `docs/decisions.md` と `docs/log-history.md` は開始時に読まない。何かを決める・変える前に `decisions.md` を検索する。経緯が要るときは `log-history.md` を検索する。

下位の単位（トピック、`guides/` など）の「<名前> の続き」は、`workflow-kit/docs-rules.md` の「上の階層で起動して…」の節（24 行付近の 3 行。`offset` 24・`limit` 5 で読む。Grep と全文読みはしない）に従う。

## wrap の記録先

`wrap`（`workflow-kit/wrap-hook.md`）は次を使う。

- **既定の対象**: トピックの続きで作業したときは、そのトピックの `docs/`。トピックの外で作業したときは、このリポジトリ直下の `docs/`。`workflow-kit/` `exmem/` `guides/` などの kit 改善の記録も、このリポジトリ直下の `docs/`（2026-10-18 に `topics/kit-growth/docs/` から統合した）。`topics/kit-growth/` には、窓口、`inbox.md`、`records/` を置く。

## review の記録先

`review`（`workflow-kit/review-hook.md`）の記録 `reviews` は、このリポジトリ直下の `docs/metrics/reviews.csv`（列は先頭行。1回に1行を追記する。2026-10-25 ユーザーの決定）。飛ばした入力は `skipped` 列に書き、同じ入力を3回続けて飛ばしたら警告する。

## 共有の範囲

- このリポジトリの内容は、すべて共有（Git 管理）する。機密、勤務先に固有の情報、PC ごとのデータを入れない。このリポジトリは公開（PUBLIC。2026-10-16 に確認）なので、世界に読まれる前提で書く。
- dotfiles の挙動（スクリプトの中身・配置）をこのリポジトリに書かない。名前とリンクで指す。依存は dotfiles → workbase の一方向だけ（理由は `exmem/lessons/app-config-placement.md`）。
- ローカルのデータ（業務・個人の作業）は、このリポジトリの外に置く。このリポジトリのノートから、外のファイルへ `[[リンク]]` を張らない。他の PC でリンク切れになる。
- `.claude/settings.local.json` は端末ごとの許可設定なので、追跡しない（`.gitignore` 済み）。

## リンク

- ノート間のリンクは wikilink（`[[名前]]`）。ファイル名はリポジトリ内（Vault 内）で一意に保つ（最短パスで解決されるため）。

## 書式とコミット

- 改行コードは LF（`.gitattributes` で統一）。
- コミットメッセージは `[領域] 変更内容` の形式（例: `[exmem] ...`、`[workflow-kit] ...`、`[guides] ...`）。
- `git add` はパスを指定する（パスなしの `git add -A` と `git add .` は使わない）。コミット・push の前に、`workflow-kit/commit-push-rules.md` を、そのセッションで読んでいなければ読む（身元・トレーラーもそこに従う）。push の前は `workflow-kit/push-rules.md`（機密の検索もそこに従う）も読む。
- push は、このリポジトリ（`yuzucha16/workbase`。公開）の `main` を、エージェントが行ってよい（2026-10-16 ユーザーの決定。公開のまま）。条件は `workflow-kit/push-rules.md`（公開のため、機密の検索を広げる）。禁止のコマンド（`--force` など）は、`workflow-kit/commit-push-rules.md` の「しないこと」に従う（`settings.json` の deny が機械的に止める）。
