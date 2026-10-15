# AI 作業部屋: ローカルの状態と作業の約束

旧窓口（2026-10-15 に分けた）から移した。リポジトリにないローカルの状態が変わったときに直す。

## リポジトリにないローカルの状態（2026-10-14 時点）

- WSL のディストリビューション: `Ubuntu-24.04`（普段使い。**触らない**）、`ai-room-test`（検証のサンプル。`wsl --unregister` で消せる）、`room-<Area>`（Area 用の部屋。1つ作成済みで、Claude Code はログイン済み）。
- Vault（`$HOME\works`、リモートなしのローカル git）: 試験で完了させた Project が `archives/` にある。`projects/_spike-room/` は、検証用のダミー（`.git/info/exclude` で git から除外）。ワークスペースの `.gitignore` に、`**/_noai/`、`~$*`、`!**/ai/out/`、`**/ai/ctx/` を入れてある。
- 確認用のダミー Project `dummy-mask`（Vault の `projects/`。架空データ。`resources/workflow-kit/room/tests/dummy_fixture.py` で `_noai/` を作り直せる）。部屋には、PowerShell の `room-sh <Area>`（dotfiles の `profile.ps1`）で入る。Windows Terminal は、部屋を出さない設定にした（WSL の動的プロファイルを無効にして、`Ubuntu-24.04` だけ固定。dotfiles の `windows/terminal/settings.json`）。
- 2026-10-14 の PC のセッションで、マスク・復元（ダミー）、共有知の送付、`stock`（ダミー）の実機の確認が済んだ。各 handover の「PC での確認の結果」を読む。残りと保留は `docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） の TODO。
- Python は uv で 3.13.14 に固定している（`workflow-kit/room/`）。Windows に uv が入っている。
- 検証の結果、**設計に影響したこと**は `docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） の「1」にある。特に: 部屋の root は C: をマウントできる（AI は一般ユーザーで動かす）、WSL への標準入力は LF 固定（CRLF だとマウントが積み重なる）、個人のグローバル ignore の `out/` が `ai/out/` を無視する、Zed は WSL リモートで開いたときだけ境界が効く。

## 作業の約束（ユーザーの方針）

- **1項目ずつ**進める。前の項目が完了の目安を満たしてから次へ。設計の未決は、ユーザーに1つずつ確認する。
- `workflow-kit/` の変更は、`workflow-kit/AGENTS.md` のとおり、**ユーザーの承認を得てから**行う。コミットは main に直接。メッセージは `[領域] 変更内容`。
- このリポジトリは公開されうる前提。勤務先名、顧客名、実在の Project 名、ユーザー名を書かない。ローカル（Vault）のファイルへ `[[リンク]]` を張らない。
- 顧客データを扱う実 Project は、roadmap の 8（最後）で行う。それまでは、使い捨てのダミーデータで試す。
- `room` コマンドは、人が実行するもの。AI に実行させない（マスクと復元の工程が、原本と対応表を読むため）。
- 部屋の中の AI に境界を破るよう頼んでも検証にならない（モデルが断るだけ）。境界の確認は、一般ユーザーでの直接の探索で行う。

## 完了したときの片付け

PC の確認が済んだら、次を行う（`docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） の TODO の末尾）。

1. 検証用の環境を消す: `wsl --unregister ai-room-test`、`projects/_spike-room/`、`%TEMP%\s5\`。
2. `guides/explain/ai-room-why.md` と `guides/howto/ai-room-setup.md` の「草稿（未レビュー）」の注記を、レビューが済んだ時点で外す。
3. `topics/ai-workspace-boundary/` を削除する（履歴は git に残る）。`topics-index.md` の行も消す。

