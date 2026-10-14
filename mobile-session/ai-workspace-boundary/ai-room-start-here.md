# 窓口: AI 作業部屋（次のセッションは、ここから始める）

- 作成: 2026-10-14（PC のセッション）。更新するときは、末尾の「この窓口の更新」に従う。
- 役割: 新しいセッション（PC でもモバイルでも）が、**何を読み、どこから始めるか**を決める。状態の正本は [[ai-room-roadmap]]。この文書には、状態の写しを置かない（古くなるため）。

## 何の取り組みか（3行）

顧客データ・社外秘を AI に見せないまま AI を使うため、Project の作業を **WSL の専用ディストリビューション（部屋）の中**で行い、部屋には作業中の Project の `ai/` だけを渡す。原本と対応表は部屋の外（`_noai/`）に置き、マスク・復元は人が実行する `room` コマンドが行う。理由と経緯は `guides/explain/ai-room-why.md`、導入の手順は `guides/howto/ai-room-setup.md`（どちらも草稿。別のセッションでレビュー予定）。

## 読む順

1. [[ai-room-roadmap]]: 優先順位8項目と、各項目の状態（実装済み / PC の確認待ち）、モバイルと PC の分担。**最初に読む**
2. 始める項目の引き継ぎ（下の表）の「PC で確認すること」
3. 必要なときだけ [[ai-room-next-steps]]（決定の一覧は「2」、実機の検証の結果は「1」）、[[ai-room-handover]]（背景）、[[ai-room-design]]（詳細）、[[ai-room-mask-spec]]（マスクの仕様）、[[ai-room-hook-taxonomy]]（フックの整理）

| 項目（roadmap の番号） | 引き継ぎ | 場所 |
|---|---|---|
| 1 マスク・復元 | [[ai-room-mask-handover]] | PC |
| 2 共有知を部屋へ入れる | [[ai-room-shared-push-handover]] | PC |
| 4 出る方向（`stock`） | [[ai-room-stock-handover]] | PC |
| 5 部屋の運用（`room init`、reap、対応表のバックアップ） | [[ai-room-ops-handover]] | PC |
| 8 実 Project での試行 | roadmap の 8 | PC |

## PC のセッションが最初にやること

1. `git log --oneline -15` と `git status` で、現在の状態を確認する（このリポジトリと、Vault（`$HOME\works`）の両方）。
2. 単体テスト: `cd workflow-kit\room; uv run python -m unittest discover -s tests`（2026-10-14 に、この PC で45件が通った）。
3. roadmap の 1 → 2 → 4 → 5 の順に、各引き継ぎの「PC で確認すること」を進める。1つ終えるごとに、引き継ぎと roadmap の状態を更新して、コミットする。
4. 実機で確認できない・決められないことは、ユーザーに1つずつ聞く（まとめて聞かない）。

## リポジトリにないローカルの状態（2026-10-14 時点）

- WSL のディストリビューション: `Ubuntu-24.04`（普段使い。**触らない**）、`ai-room-test`（検証のサンプル。`wsl --unregister` で消せる）、`room-<Area>`（Area 用の部屋。1つ作成済みで、Claude Code はログイン済み）。
- Vault（`$HOME\works`、リモートなしのローカル git）: 試験で完了させた Project が `archives/` にある。`projects/_spike-room/` は、検証用のダミー（`.git/info/exclude` で git から除外）。ワークスペースの `.gitignore` に、`**/_noai/`、`~$*`、`!**/ai/out/`、`**/ai/ctx/` を入れてある。
- Python は uv で 3.13.14 に固定している（`workflow-kit/room/`）。Windows に uv が入っている。
- 検証の結果、**設計に影響したこと**は [[ai-room-next-steps]] の「1」にある。特に: 部屋の root は C: をマウントできる（AI は一般ユーザーで動かす）、WSL への標準入力は LF 固定（CRLF だとマウントが積み重なる）、個人のグローバル ignore の `out/` が `ai/out/` を無視する、Zed は WSL リモートで開いたときだけ境界が効く。

## 作業の約束（ユーザーの方針）

- **1項目ずつ**進める。前の項目が完了の目安を満たしてから次へ。設計の未決は、ユーザーに1つずつ確認する。
- `workflow-kit/` の変更は、`workflow-kit/AGENTS.md` のとおり、**ユーザーの承認を得てから**行う。コミットは main に直接。メッセージは `[領域] 変更内容`。
- このリポジトリは公開されうる前提。会社名、顧客名、実在の Project 名、ユーザー名を書かない。ローカル（Vault）のファイルへ `[[リンク]]` を張らない。
- 顧客データを扱う実 Project は、roadmap の 8（最後）で行う。それまでは、使い捨てのダミーデータで試す。
- `room` コマンドは、人が実行するもの。AI に実行させない（マスクと復元の工程が、原本と対応表を読むため）。
- 部屋の中の AI に境界を破るよう頼んでも検証にならない（モデルが断るだけ）。境界の確認は、一般ユーザーでの直接の探索で行う。

## 決めることが残っている点（ユーザーの決定待ち）

- 対応表（`_noai/map/mapping.json`、追跡しない）のバックアップ方針。案: `room close` で `archives/` へ移る `_noai/` ごと、Windows 側のバックアップの対象にする（[[ai-room-ops-handover]]）。Vault が漏れた場合の対策（Vault の外に置く、暗号化する、保持期間を短くする）は、運用しながら決める。
- Obsidian の中で AI と話す件（Claudian は部屋につながらない）。優先度を下げている。

## 完了したときの片付け

PC の確認が済んだら、次を行う（[[ai-room-next-steps]] の TODO の末尾）。

1. 検証用の環境を消す: `wsl --unregister ai-room-test`、`projects/_spike-room/`、`%TEMP%\s5\`。
2. `guides/explain/ai-room-why.md` と `guides/howto/ai-room-setup.md` の「草稿（未レビュー）」の注記を、レビューが済んだ時点で外す。
3. `mobile-session/ai-workspace-boundary/` を削除する（履歴は git に残る）。`mobile-session-index.md` の行も消す。

## この窓口の更新

- 状態が変わったら、roadmap と各引き継ぎを更新する。**この文書は、読む順と、リポジトリにないローカルの状態が変わったときだけ**直す。
- 新しい引き継ぎを足したら、上の表に1行足す。
