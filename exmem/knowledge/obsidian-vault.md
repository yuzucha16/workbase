---
type: knowledge
title: Obsidian Vault
status: active
tags:
  - tool/obsidian
  - knowledge-management
  - setup
  - backup
  - windows
aliases:
  - Obsidian Vault
  - Obsidianの設定
  - vaultのバックアップ
created: 2026-10-01
updated: 2026-10-04
sources:
  - Claude Code conversation "exmemの整理" (2026-09-26〜2026-10-01)
  - Claude Code conversation "ディレクトリ構造の見直し" (2026-10-02〜2026-10-03)
  - Claude conversation "vaultの置き場所とバックアップ方針" (2026-10-02)
  - "C:\\vault の構成とタスクスケジューラ（2026-10-02 に確認）"
  - "C:\\vault\\notes\\.obsidian の設定ファイル（2026-10-01 に確認）"
  - "C:\\vault\\notes\\.obsidian の設定ファイルと `git log -- .obsidian`（2026-10-04 に確認。「設定」節を更新）"
---

# Obsidian Vault

## Purpose

このナレッジベース（exmem）を閲覧・管理しているObsidian Vaultの環境と、ナレッジベースから使っている機能をまとめる。

## Vault

### 目標の構造（2026-10-02 決定）

- Vaultのルート: `C:\vault\notes`。ここがそのまま Gitリポジトリ（GitHub: `yuzucha16/notes`）のルートになる。
- 直下はPARA形式: `projects/` / `areas/` / `resources/` / `archives/`
- 共有（Git管理）するのは `resources/` と `.obsidian/` だけ。`projects/` `areas/` `archives/` はローカル専用で、`.gitignore` のホワイトリストで除外する。
- このナレッジベースの場所: `resources/exmem`

```text
notes/                 # Git root
├── .gitignore / .gitattributes
├── .obsidian/         # 共有（workspace*.json は除外）
├── resources/         # 共有（唯一）
│   ├── exmem/
│   ├── cheatsheets/
│   ├── handson/
│   ├── office/        # Officeテンプレ・リボン設定
│   ├── fonts/         # Git LFS
│   ├── wallpapers/    # Git LFS
│   └── _archive/      # 共有の古い資料（旧 obsolete/）
├── projects/  areas/  archives/   # ローカル専用
```

### 移行の状況（2026-10-03 時点）

- 済み（2026-10-02）: `areas_shared` リポジトリ内の配置換え（`exmem` `cheatsheets` `handson` を `resources/` 配下へ、`obsolete` を `resources/_archive/obsolete` へ）、`.gitignore` / `.gitattributes` の作成、`office` の dotfiles からのコピー、ドキュメントの更新。GitHub 側の `areas_shared` → `notes` の rename。
- 済み（2026-10-03）: 実体は `C:\vault\repos\github.com\yuzucha16\notes`（ghq 管理）。`C:\vault\notes` はその実体へのジャンクション。`.obsidian` を dotfiles から取り込み（`workspace.json` は除外）。dotfiles 側の `windows/office` と `windows/obsidian` を削除し、`links.map` のリンク元を `..\notes\resources\office\...` に変更。`%APPDATA%` 側の Office のリンク7本を新しい実体へ張り直した。
- 注意: `C:\vault` に置かれていた `notes.lnk` は Windows のショートカットで、パスとして辿れない（ジャンクション / シンボリックリンクとは別物）。`C:\vault\notes` は 2026-10-03 にジャンクションとして作り直した。
- 済み（2026-10-03 確認）: `C:\vault\notes` は実体 `repos\...\notes` へのジャンクション。`C:\vault\notes.lnk` は無くなっている。`_local/` のコミット（`27d1d08`）は `origin/main` より1つ先で、未 push。
- 未実施: 旧 `areas_shared` クローン（`C:\vault\repos\github.com\yuzucha16\areas_shared`）と `C:\vault\notes_old` の削除（2026-10-03 時点でどちらも残っている。旧クローンは clean で未 push の変更なし）。Obsidian で `C:\vault\notes` を Vault として開き直す確認。`resources/fonts/` には `README.md` だけで、HackGen はまだ無い。

### dotfiles との関係（2026-10-03 時点）

- `notes` は dotfiles の隣のリポジトリ。`links.map` が `..\notes|%NOTES_DIR%`（Vault）を張る。Office のテンプレ・リボン設定は、その後の dotfiles の見直しで `links.map` から外れ、初回に手で配置する運用になった。
- **撤回済み（2026-10-05。dotfiles へ戻す。理由は [[app-config-placement]] の Decisions）**: `.obsidian` は `notes` に置き続け、dotfiles には戻さない（2026-10-04 決定）。根拠: Obsidian は Vault 直下の `.obsidian` を読む（dotfiles に置くとジャンクションが必須）、設定の中身が Vault と連動する、dotfiles → `notes` の片方向の依存を保てる、プラグインで dotfiles の履歴が重くなるのを避ける。dotfiles に置いてリンクすると、clone 順の循環、リンク前に Obsidian を開いたときの衝突、コミット先の分離が起きる。設定を変える作業は `notes` のルートで Claude を開いて行い、`.obsidian/` 専用の `AGENTS.md` と `docs/` は置かない。判断基準の全体は [[app-config-placement]]。
- セットアップの順序は「`notes` を先に clone → `30_link.bat`」（旧 `w2a`。スクリプトは2026-10-03 に `NN_<内容>` へ改名された）。`NOTES_DIR` はリンクで作られる。
- ローカル専用の `projects/` `areas/` `archives/` は gitignore のため、clone 直後には存在しない。必要に応じて手で作る。

### 移行前の構造（2026-10-01 時点）

一部のフォルダはGitリポジトリへのジャンクションになっていた。

| Vault内のパス      | 実体                                                                        | Gitリモート                                     |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------------- |
| `.obsidian`    | `C:\vault\repos\github.com\yuzucha16\dotfiles\windows\obsidian\.obsidian` | dotfiles                                    |
| `areas_shared` | `C:\vault\repos\github.com\yuzucha16\areas_shared`                        | `https://github.com/yuzucha16/areas_shared` |

Git の管理境界が `notes`（管理外）・`areas_shared`・`dotfiles` の3つに分かれていた。

## 設定

2026-10-04 時点で `.obsidian` の設定ファイルから確認した内容。2026-10-01 時点の記述から、2026-10-03 の整理（`notes` の `git log -- .obsidian` の `82953b7` ほか）で大きく変わった。変更の理由は、履歴から読み取れないものが多い（下に「不明」と書く）。

### Principles（設定）

- **Obsidian は参照専用にする。** 新規ノートの作成や、日付・テンプレート系の機能を持たない。ノートの読み書きは AI がファイルを直接行い、人間は閲覧と軽い編集だけをする。
- **Obsidian の中で AI を呼ぶプラグイン（意味検索、文章生成、REST API 経由の連携など）は入れない。** AI（Claude Code）はファイルを直接読めるので役割が重なり、ノートを外部に送る経路や API キーの管理が増える。
- **コミュニティプラグインは、使うものだけに絞る。** 導入と取り消しが繰り返されている（2025-09-22 に9つを追加して翌日に取り消し、2026-10-03 に `calendar` と `obsidian-icon-folder` を削除）。
- **設定の方針は、ツールの実際の出力を確認してから決める。** Obsidian が書く改行コードを確かめずに CRLF へ揃え、すぐ LF に直すことになった。
- **アプリが起動中は、そのアプリの設定ファイルを編集しない。** 起動中のアプリが、メモリ上の状態で設定を上書きして、編集が消える（`notes/AGENTS.md` にも同じ規則がある）。
- **設定を記述するナレッジには「いつ時点か」を書き、設定ファイルから再確認できる形にする。** 2026-10-01 時点の記述が、2日後には実物と食い違っていた。
- 端末ごとの状態（`workspace.json`）は追跡しない。アプリが自動で書き換えるファイルを一律に外すのではなく、再現したい設定か・共有ノートから決まるか・差分が意図と対応するか・共有して問題ないか・再生成できるかの5項目で決める（[[app-config-placement]]）。`colored-tags` の `data.json` は、この基準で追跡と決まった。

### Decisions（設定。2026-10-03〜04）

- プラグインの削除と `properties` の有効化: 使っていないコア・コミュニティプラグインを外した（`calendar`、`obsidian-icon-folder`、`graph`、`canvas`、`daily-notes`、`templates`、`note-composer`）。`properties` は frontmatter の確認に使う。却下案: 念のため残す（用途が参照専用になり、起動や設定画面の負担だけが増える）。
- テーマ Typora-Vue は、未使用でも残す。ライトテーマが必要になったときのサブ。却下案: 削除。
- `colored-tags` を残し、`data.json` を追跡して色の割り当てを固定する。色はタグを見つけた順の連番で決まるので、追跡すると別の端末でも同じ色になる（diff が出るのは新しいタグが増えたときだけ。運用は、新しいタグを使い始めたコミットに追記分を含める）。判断の詳細は [[app-config-placement]]。却下案: 追跡しない（clone 後に色が変わる）、CSS スニペットで色を固定する（タグが増えて必要になったら移る）。
- ファイル一覧は、行の余白を詰め、フォントサイズをエディタと同じにし、アイコンを CSS の `mask` だけで付ける（Lucide と同じ形）。プラグインを読み込まないので起動が重くならない。却下案: Iconize プラグイン（JS を読み込むため起動が重くなる可能性）。
- 改行コードは `.gitattributes` の `* text=auto eol=lf` で LF に統一する。Obsidian が `app.json` と `appearance.json` を LF で書き戻した（2026-10-03、CRLF で書いたファイルが数分後に LF になっていた）。AI と WSL/Linux の出力も LF。却下案: CRLF に統一する（一度実施したが、Obsidian が保存するたびに全行が変更扱いになる）。
- 本文の幅は、フォントサイズに比例させる（`--file-line-width: 58em`）。既定の固定 700px は、拡大しても幅が変わらず1行の文字数だけが減る。却下案: 幅の制限をなくす、64em（試して 58em にした。1週間の試用で確定する）。
- 新規ノートの保存先は現在のフォルダにし、`_local/` は検索対象のままにする。新規作成はほぼしない。`exmem/inbox` は AI 出力をナレッジ化する入口で別の用途。`_local/` は PC ローカルのデータなので検索できる必要がある。
- 検索から除外するフィルターは `.tmp.`、`_archive/`、`.claude/`。AI が書き込み途中に作る一時ファイル、古い資料、エージェントの設定を検索やリンク補完に出さない。
- Vault のルートに共有の `AGENTS.md` と `CLAUDE.md`（`@AGENTS.md`）を置く。ルートで起動した AI に、共有とローカルの境界、`_local/`、リンクの規則、`.obsidian` の編集時の注意、書式を伝える。内容に機密が無いので共有する。却下案: ローカル専用にする。

### コアプラグイン

- 有効: `file-explorer`、`global-search`、`switcher`、`backlink`、`outgoing-link`、`tag-pane`、`properties`、`page-preview`、`command-palette`、`editor-status`、`bookmarks`、`outline`、`word-count`、`file-recovery`、`sync`、`bases`
- 無効: `graph`、`canvas`、`daily-notes`、`templates`、`note-composer`、`footnotes`、`slash-command`、`markdown-importer`、`zk-prefixer`、`random-note`、`slides`、`audio-recorder`、`workspaces`、`publish`、`webviewer`
- 2026-10-01 時点では `graph`、`canvas`、`daily-notes`、`templates`、`note-composer` が有効で、`properties` が無効だった。2026-10-03 の `82953b7`（コミットメッセージは「使っていないプラグインと古い設定を削除」）で逆になった。

### コミュニティプラグイン

- `colored-tags`（タグを色分けする。階層タグの親ごとに色が変わる）だけ。
- 2026-10-01 時点で入っていた `calendar` と `obsidian-icon-folder` は、2026-10-03 に削除した（`82953b7`）。
- `plugins/colored-tags/data.json`（タグの色の設定）は、2026-10-03 に追跡をやめ（`22b9fc0`。端末ごとのキャッシュとコミットメッセージにある）、約1.5時間後に再び追跡した（`76d3fec`）。履歴からは反転の理由が読み取れなかったが、追跡して色を固定する方針に決まった（上の Decisions）。実物（2026-10-04）: `data.json` は追跡されている。新しいタグが増えると、Obsidian が書き換えた変更が未コミットで出る。

### テーマ・フォント・スニペット

- テーマ: Material Gruvbox（`themes/` には `Typora-Vue` も入っている）。2026-10-03 の `78e3975` で、Obsidian gruvbox と Everforest から変更した。理由は不明。
- フォント: UI・本文・等幅とも `PlemolJP Console NF`（次候補 `Moralerspace Neon HW`、`Meiryo UI`）、基本のフォントサイズ 14。2026-10-03 の `1d75fce` で、Noto Sans JP などから変更した。理由は不明。
- 有効なスニペット: `material-gruvbox-bold`、`file-explorer-compact`、`readable-width`。`readable-width` は、`--file-line-width: 58em` で本文の幅をフォントサイズに比例させる（拡大しても1行の文字数が保たれる。既定は固定 700px）。`readableLineLength` を有効にしている（2026-10-04、`0fdd679`）。

### その他

- 新規ノートの保存先 `newFileLocation`: `current`（現在のフォルダ）。2026-10-01 時点では、`newFileFolderPath: 0_inbox`（Vault に存在しないフォルダ）だった。
- 添付ファイルの保存先 `attachmentFolderPath`: `./`（ノートと同じフォルダ）。以前は `0_inbox`。
- 行番号を表示、削除の確認あり、タブ幅 2、検索から除外するフィルターは `.tmp.`、`_archive/`、`.claude/`。
- `types.json`: `created` と `updated` は `date` 型（2026-10-03、`e81182c`）。`aliases`、`cssclasses`（複数テキスト）、`tags` は既定。
- 改行コード: `notes` の `.gitattributes` が `* text=auto eol=lf` で LF に統一している（2026-10-04 に実物で確認）。Obsidian が設定ファイルを LF で書くことは、2026-10-03 に確認した（上の Decisions）。
- `readable-width` スニペットの `--file-line-width: 58em`、`app.json` の `readableLineLength: true`、`types.json` の `date` 型は、2026-10-04 に実物で確認した。ルートの `AGENTS.md` / `CLAUDE.md` も存在する。
- 未検証: フォントの指定は `PlemolJP Console NF, Moralerspace Neon HW, Meiryo UI` の順で、未インストールの端末では Meiryo UI に落ちる（実機での表示は未確認）。

## ナレッジベースから使っている機能

| 機能 | 使い方 |
|---|---|
| Obsidian Sync | モバイルアプリで `inbox/` に保存したノートをPCへ届ける（[[ai-development-workflow]] D4、未検証） |
| Bases | `knowledge.base` で知識・プロジェクト・inboxの一覧表を表示する（表示は未確認） |
| 階層タグ + `colored-tags` | `tags.md` の統制語彙（[[tags]]） |
| `aliases` | 英語ファイル名のノートを日本語でリンク補完・検索する |
| Backlinks | `## Related` の `[[リンク]]` でノート間のつながりを見る（Graph は 2026-10-03 に無効にした） |

## Vaultの置き場所とバックアップ

2026-10-02 のメモ（Claude conversation "vaultの置き場所とバックアップ方針"）から統合。

### Principles

- 作業場所とバックアップ先を分ける。OneDriveはバックアップ先として使い、作業場所にしない。
- バックアップは、まずrobocopyで始める。足りなければresticへ移行する。

### Decisions

#### Vaultを1つのGitリポジトリにして、共有は `resources/` だけにする（2026-10-02）

- 決めたこと: `areas_shared` ジャンクションをやめ、`notes` 自体をリポジトリにする。共有は `resources/` と `.obsidian/` だけ。共有かローカルかは、名前（`_shared`）ではなく `.gitignore` のホワイトリスト（`/*` を除外して `resources/` などだけ許可）で決める。
- 根拠: Gitの管理境界を減らしたい。`areas_shared` の中身は実質 resource で、area ではなかった。共有を `resources/` の1つに決めれば、サフィックスで区別する必要がない。ホワイトリスト方式なら、新しく作ったディレクトリは既定でローカル扱いになり、会社固有の情報を誤って共有しにくい。
- 却下案: `_local/` にローカル専用をまとめる（PARAが二重になる）。`projects` `areas` `archives` の共有版を `_shared` で並べる。
- 共有の archive は `resources/_archive/` に置く。ローカルの `archives/` とは別。
- `.obsidian` は dotfiles から外して `notes` 管理にする。
- `exmem/projects/` は Vault の `projects/` と衝突するため `contexts/` に改名した（`contexts/<name>/context.md` の形は維持。`<name>.md` にすると `knowledge/<name>.md` と同名になり `[[リンク]]` が曖昧になるため）。
- 決定（2026-10-03）: `resources/` の中のローカル専用データは `_local/` に置く。`.gitignore` は場所ではなく名前で効かせる（`**/_local/*` を無視し、`!**/_local/.gitkeep` で `.gitkeep` だけ追跡する）。これで `resources/exmem/_local/` のように各トピックの隣にも置け、clone でディレクトリが出来る。却下案: 別の非公開リポジトリ（管理境界が増える）、暗号化（AI・Obsidian から読めず重い）。
- 注意: `resources/` 直下は新しいものが既定で共有になる（トップレベルと逆）。ローカル専用のものを `_local/` の外に置かない。`git add -f` や過去にコミット済みのファイルは ignore で防げない。
- 作成済みの `_local/`（2026-10-03 確認）: `resources/`、`resources/exmem/`、`resources/cheatsheets/`、`resources/handson/`、`resources/office/`。いずれも `.gitkeep` あり。
- 未決: トップレベルの `projects/` `areas/` `archives/`（全体がローカル）と `resources/_local/` の使い分けの基準。目安は、責任領域や業務の継続的な管理なら `areas/`、資料・知識なら `_local/`。

#### `.gitignore` はホワイトリスト、バイナリは Git LFS（2026-10-03）

- `.gitignore` は `/*` で全部除外し、`!/.obsidian/` `!/resources/` などだけ許可する（2026-10-03 に実物で確認）。`workspace*.json`（端末ごとの状態）と `**/.claude/settings.local.json` も除外。
- `resources/fonts/**` と `resources/wallpapers/**` は Git LFS。`*.md` `*.txt` `.gitkeep` は LFS の対象外。フォントは HackGen Console NF Regular だけ置く予定で、ライセンス文書も同じ場所に置く。Office のテンプレは小さいので LFS にしない。
- 履歴: `areas_shared` → `notes` は GitHub の rename と `git mv` で履歴を保つ。dotfiles からの `.obsidian` と Office テンプレの移管は履歴なしのコピー。

#### Office テンプレは `resources/office/`、リンクの仕組みは dotfiles

- 配置対象の7ファイル（`Blank.potx` `Book.xltx` `Sheet.xltx` `Normal.dotm` と `*.exportedUI` 3つ）と参照用の残りを `resources/office/` に置く。dotfiles の `links.map` のリンク元は `..\notes\resources\office\...`。
- 順序の制約（`notes` を先に clone してから `w2a`）は受け入れた。実機のリンク7本は張り直して確認済み（2026-10-03）。

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
- 仮説: ユーザー名が日本語やスペース入りなら `C:\vault` のほうがツール不具合を避けやすい。会社PCではC直下がIT部門のポリシーで制限される可能性がある（いずれも未確認）。

### Gotchas

- robocopyの `/XJ` はジャンクションをたどらない。実体が別のGitリポジトリ（移行前は `.obsidian` → dotfiles、`areas_shared`。移行後はジャンクションが無くなる）なので、バックアップに含めたいか、`/XD` で外すかを決める。含めたいなら、リポジトリ側（GitHub）が別のバックアップになっている点も考える。
- PCが閉じていた日のバックアップを取りこぼさないよう、タスクスケジューラで「スケジュールされた時刻に開始できなかった場合、すぐにタスクを実行する」をオンにする。
- robocopyは「最新のコピー」しか持たず、過去の状態には戻れない。OneDriveのバージョン履歴とごみ箱で一部補える。
- 注意: このvaultはObsidian Syncも有効（上記）。OneDriveのバックアップ先とは独立している。

### Open Questions

- バックアップ対象: ジャンクションは `C:\vault\notes` の1つになった。`/XJ` は実体を辿らないので、実体側（`repos\...\notes`）を対象にするか決める。`_local/` はGitに載らないので、バックアップが唯一の保険。
- `notes` リポジトリが公開か非公開か（未確認。`gh` は scoop に入っているので、`gh repo view` で確認できる）。公開なら `.obsidian` と `_local/` 以外が全部見える。
- `30_link.bat`（旧 `w2a`）を通しで実行したとき、`..\notes|%NOTES_DIR%` のリンクが期待どおりに張られるか（今の `C:\vault\notes` は手で作ったジャンクション。未検証）。
- `50_repos.bat`（旧 `w4`）に `notes` の clone を足すか、README の手動手順のままにするか（現状は取得対象が例のコメント行のみ）。
- 仮説（未検証）: Obsidian Sync は `_local/` も含めて Vault 全体を同期する。
- 仮説（未検証）: `.claude/settings.local.json` は、Claude Code を起動したディレクトリの `.claude/` から読まれる。
- dotfiles の `notepadpp\config.xml` に、古い `areas_shared\exmem\inbox` のパスが残っている（ユーザーの未コミット変更）。
- 使っているPCが会社PCか（C直下の制約やバックアップポリシーに影響）。
- robocopyで足りるか、世代管理が必要になってresticへ移行するか。
- 本文幅 58em は、1週間の試用で十分か（2026-10-04 に試用開始）。
- Obsidian Sync を使うか（モバイルから inbox に送る運用をするか。未検証）。
- Linter など、書式を整えるプラグインを入れるか。AI が整形する仕組みと競合しうる。
- 設定を記述するナレッジを、実物とずれないように保つ手段（設定ファイルから自動で確認するか）。

### Next Actions

- `vault-backup.bat` を作り、ジャンクションの扱いを決めて `schtasks` に登録する（取りこぼし防止設定をオン）。
- 別フォルダへ復元し、Obsidianで開けるか確認する。

## Gotchas

### 2026-10-03 の再構成で遭遇したもの

- **ディレクトリの `git mv` が Permission denied**: `git mv exmem resources/exmem` が失敗した。`exmem` がエージェントの作業ディレクトリで、Windows が使用中のディレクトリの名前変更を拒否したため。中身を1つずつ `git mv` して回避した。空になった旧 `exmem/` はセッション終了後に削除する（2026-10-03 時点で `notes` 直下に `exmem/` は残っていない）。
- **`C:\vault\notes` が存在しない扱いになる**: 実体は `notes.lnk`（Windows のショートカット）だった。`.lnk` はシェルが解釈する普通のファイルで、PowerShell・git・Obsidian は辿らない。`New-Item -ItemType Junction`（管理者権限は不要）で作り直した。
- **LFS の除外設定の前に `git add` すると、README が LFS ポインタになる**: `.gitattributes` が `resources/fonts/**` を LFS にしていて、`fonts/README.md` までポインタとして登録された。除外行を足して `git rm --cached` と再 `git add` で直し、未 push のコミットを amend した。`.gitattributes` を先に完成させてから `git add` する。
- **`.gitignore` の途中に `/` を含むパターンはルート基準になる**: `_local/*` は深い階層の `_local/` に効かない。`**/_local/*` と `!**/_local/.gitkeep` にして `check-ignore` で確認した。
- **ファイルを書き込めなかった（一時的）**: PowerShell の `Set-Content` が「別のプロセスが使用中」で失敗した（原因は不明。Obsidian か Sync が掴んでいた可能性、未確認）。Edit ツールでの置換は成功した。

### 2026-10-03〜04 の設定整理で遭遇したもの

- **Obsidian の起動中に `appearance.json` を編集して、有効にしたスニペットを追記したら消えた**: Obsidian が追記前の内容で設定を上書きしたため（仮説）。追記し直してコミットし、設定画面でスニペットがオンか確認した。
- **`git commit` が `.git/index.lock` の存在で失敗した**: Git の GUI（Fork）が動いていて、リポジトリを更新していた（仮説。確認時にはロックが消えていた）。数秒後の再実行で成功した。
- **`obsidian-vault.md` の編集がロックで失敗することがある**: 2026-10-04 に Edit ツールで `EPERM`（アトミック書き込みの rename 失敗）が出た。Obsidian が開いているファイルで起きるとみられ、再実行で成功した。

### Vaultを移したあと、古い場所を編集していた

- 状況: 2026-10-01 にナレッジベースを `C:\Users\ck\vault\notes` 配下から `C:\vault\notes\areas_shared\exmem` へ移したが、AIエージェントは古い場所を作業ディレクトリとして開いたまま編集を続けた。
- 解決: 変更を exmem へ移し、古い場所は削除した。エージェントは `C:\vault\notes\areas_shared\exmem` を作業ディレクトリとして起動した（2026-10-02 の構造見直しで `C:\vault\notes\resources\exmem` に変わる）。

## Proposals

Vault全体に影響し、Syncで他の端末にも伝わる。2026-10-03 時点の扱いを、項目ごとに書く（適用済み・却下・見送り）。

- 新規ノートの保存先を `resources/exmem/inbox` にする。モバイルで新規ノートを作るだけで inbox に入る。**2026-10-03 に、現在のフォルダにする（`newFileLocation: current`）と決めた**（`exmem/inbox` は AI 出力をナレッジ化する入口で、新規ノートとは別の用途のため。却下）。
- `created` / `updated` のプロパティ型を「日付」にする。**採用済み**（2026-10-03、`types.json`）。
- Templatesで知識ノート用のテンプレートを作る。Templates は参照専用の方針で無効にした（2026-10-03）ので、見送り。

## Related

- [[ai-development-workflow]]
- [[ai-development-workflow/context]]
- [[app-config-placement]]
- [[tags]]
