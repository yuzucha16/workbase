---
type: knowledge
title: Obsidian Vault の置き場所とバックアップ
status: active
tags:
  - tool/obsidian
  - knowledge-management
  - setup
aliases:
  - obsidian-vault-backup
triggers: [バックアップ, robocopy, restic, OneDrive, git bundle, 置き場所, タスクスケジューラ, 旧 clone]
created: 2026-10-02
updated: 2026-10-27
sources:
  - Claude conversation "vaultの置き場所とバックアップ方針" (2026-10-02)
---

# Obsidian Vault の置き場所とバックアップ

全体の方針は [[obsidian-vault]]（2026-10-27 に、追記の節を切り出した）。

## Vaultの置き場所とバックアップ

2026-10-02 のメモ（Claude conversation "vaultの置き場所とバックアップ方針"）から統合。

### Principles

- 作業場所とバックアップ先を分ける。OneDriveはバックアップ先として使い、作業場所にしない。
- バックアップは、まずrobocopyで始める。足りなければresticへ移行する。

### Decisions

#### Vaultを1つのGitリポジトリにして、共有は `resources/` だけにする（2026-10-02。2026-10-05 に撤回: 「現在の構造」を参照。以下は履歴）

- `areas_shared` をやめ、`notes` 全体を 1 リポジトリにして共有は `resources/` だけにする案（ホワイトリスト、`_local/`、`contexts/` への改名を含む）。「現在の構造」（[[obsidian-vault-structure]]）に置き換わった。詳細は git の履歴。

#### `.gitignore` はホワイトリスト、バイナリは Git LFS（2026-10-03。2026-10-05 に撤回: ホワイトリストは無くなり、LFS は不要になった。以下は履歴）

- ホワイトリスト方式の `.gitignore` と Git LFS（`fonts/` `wallpapers/`）は、ホワイトリストが無くなり LFS が不要になったので廃止した。

#### Office テンプレは `resources/office/`、リンクの仕組みは dotfiles（2026-10-05 に dotfiles の `windows/office/` へ戻した。以下は履歴）

- Office テンプレ 7 ファイルを `resources/office/` に置く構成は、dotfiles の `windows/office/` に戻した。

#### vaultをOneDrive直下ではなくC直下に置く（2026-10-02）

- 根拠: 単一PC運用で複数端末の予定がなく、OneDrive同期のメリットが小さい。同期競合・ファイルロック・Files On-Demandによる遅延などを避けられる。
- 却下案: OneDrive直下のまま運用（「常にこのデバイス上に保持」やキャッシュ系の除外で回避する案）。`C:\Users\<名前>\vault`（OneDriveの外なら同期されないが、プロファイルと運命を共にし、パスがやや長い）。
- 実物（2026-10-02 確認）: vaultは `C:\vault\notes`（`C:\vault` 直下に `bin` / `certs` / `notes` / `repos` / `tools`）。メモの `C:\vault` はvault全体の置き場で、Obsidianのルートは `notes`。
- 注意: 「vault配下の `.git` は1つだけ」というメモの記述は、2026-10-02 時点の実物と違った。`C:\vault\notes` 直下に `.git` は無く、`.obsidian` と `areas_shared` がそれぞれ別のGitリポジトリへのジャンクションだった（移行前の表）。移行後は `notes` 直下に `.git` を置いて1つにする方針。

#### バックアップはOneDriveへの定期コピー（robocopy + タスクスケジューラ）

- 根拠: C直下にすると自動バックアップが無くなるため。
- 初回は `/E`（追加・更新のみ、削除は反映しない）で運用する。`/MIR` は誤削除がバックアップにも波及するので見送る。
- 却下案: 最初から `restic`（世代管理付き）を導入する。
- コマンド案: `robocopy C:\vault "%OneDrive%\vault-backup" /E /XJ /R:2 /W:5 /XD .trash`
- 登録例: `schtasks /create /tn "vault-backup" /tr "C:\tools\vault-backup.bat" /sc daily /st 12:00`
- 実物（2026-10-02 確認）: `vault-backup` というタスクはタスクスケジューラに見当たらない。バックアップは未設定とみられる。

### Facts（メモ記載）

- OneDrive直下の問題: 同期競合コピー、ファイルロックによる保存失敗、Files On-Demandでgrep・AI読み込み時に遅延や一斉ダウンロード、小さなファイルの大量更新に弱い、パスが長く日本語・スペースを含みやすい、`.git` が壊れるリスク、同期停止に気づきにくい、組織アカウントのポリシー制約。`workspace.json` のような頻繁に書き換わる設定ファイルは競合の元で、シンボリックリンクの扱いも不安定。
- C直下の問題: 自動バックアップが無い、他端末・スマホから見られない。
- 「既知のフォルダーのバックアップ」が有効だと、Documents / Desktop / PicturesはOneDriveにリダイレクトされる。
- Windowsでシンボリックリンクを作るには開発者モードか管理者権限が必要。
- 仮説: ユーザー名が日本語やスペース入りなら `C:\vault` のほうがツール不具合を避けやすい。PC1 ではC直下が管理側のポリシーで制限される可能性がある（いずれも未確認）。

### Gotchas

- robocopyの `/XJ` はジャンクションをたどらない。実体が別のGitリポジトリ（移行前は `.obsidian` → dotfiles、`areas_shared`。移行後はジャンクションが無くなる）なので、バックアップに含めたいか、`/XD` で外すかを決める。含めたいなら、リポジトリ側（GitHub）が別のバックアップになっている点も考える。
- PCが閉じていた日のバックアップを取りこぼさないよう、タスクスケジューラで「スケジュールされた時刻に開始できなかった場合、すぐにタスクを実行する」をオンにする。
- robocopyは「最新のコピー」しか持たず、過去の状態には戻れない。OneDriveのバージョン履歴とごみ箱で一部補える。
- 注意: このvaultはObsidian Syncも有効（上記）。OneDriveのバックアップ先とは独立している。

### Open Questions

- バックアップ対象: （2026-10-03 時点の記述。2026-10-05 にトップは実ディレクトリ `C:\vault\works`（旧 `notes`）になり、ジャンクションではなくなった。2026-10-06 にさらに `$HOME\works` へ移った。見直しが必要）ジャンクションは `C:\vault\notes` の1つになった。`/XJ` は実体を辿らないので、実体側（`repos\...\notes`）を対象にするか決める。`_local/` はGitに載らないので、バックアップが唯一の保険。
- 新しい業務用 PC で、dotfiles の `50_repos` から `room mkworks`（旧「workflowを導入して」）までの順で、この構造を再現して確認する。
- 仮説（未検証）: Obsidian Sync は `_local/` も含めて Vault 全体を同期する。
- 仮説（未検証）: `.claude/settings.local.json` は、Claude Code を起動したディレクトリの `.claude/` から読まれる。
- dotfiles の `notepadpp\config.xml` に、古い `areas_shared\exmem\inbox` のパスが残っている（ユーザーの未コミット変更）。
- 使っているPCが PC1（管理側のポリシーがある PC）か（C直下の制約やバックアップポリシーに影響）。
- robocopyで足りるか、世代管理が必要になってresticへ移行するか。
- Obsidian Sync を使うか（モバイルから inbox に送る運用をするか。未検証）。
- Linter など、書式を整えるプラグインを入れるか。AI が整形する仕組みと競合しうる。
- 設定を記述するナレッジを、実物とずれないように保つ手段（設定ファイルから自動で確認するか）。

### Next Actions

- `vault-backup.bat` を作り、ジャンクションの扱いを決めて `schtasks` に登録する（取りこぼし防止設定をオン）。
- 別フォルダへ復元し、Obsidianで開けるか確認する。
- `10_env.bat` を再実行し、新しいターミナルと WSL の新しいセッションで、`CERTS_DIR`（`%USERPROFILE%\.certs`）と `WSLENV` が期待どおりになることを確認する。2026-10-06 時点のこの PC は未移行で、`CERTS_DIR` は旧置き場を指し、`WSLENV` は空、`~\.certs` は無い（確認: 2026-10-06、根拠: 環境変数の取得と `Test-Path`）。
- WSL の dotfiles を新パスで張り直す（2026-10-06 時点）。`WORKS_DIR` は 2026-10-18 に渡るようになった。同日のログインシェルで `GHQ_ROOT` は空だった（未調査）。他の PC では、`10_env.bat` を再実行して `WSLENV` の `;` を `:` に直す。
- （旧 `C:\vault` と旧 clone の後始末は、ユーザーが `C:\vault` を削除して閉じた。2026-10-27）

## Related

- [[obsidian-vault]]
