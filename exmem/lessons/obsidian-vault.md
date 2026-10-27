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
  - tool/wsl
  - dotfiles
aliases:
  - Obsidian Vault
  - Obsidianの設定
  - vaultのバックアップ
triggers: [Obsidian, Vault, vault, バックアップ, 設定, プラグイン, リンク, wikilink, 同期, .obsidian, 日付, ノート]
created: 2026-10-01
updated: 2026-10-27
sources:
  - Claude Code conversation "exmemの整理" (2026-09-26〜2026-10-01)
  - Claude Code conversation "ディレクトリ構造の見直し" (2026-10-02〜2026-10-03)
  - Claude conversation "vaultの置き場所とバックアップ方針" (2026-10-02)
  - "C:\\vault の構成とタスクスケジューラ（2026-10-02 に確認）"
  - "C:\\vault\\notes\\.obsidian の設定ファイル（2026-10-01 に確認）"
  - "C:\\vault\\notes\\.obsidian の設定ファイルと `git log -- .obsidian`（2026-10-04 に確認。「設定」節を更新）"
  - Claude Code conversation "Vault の構造変更（共有とローカルのリポジトリ分離）と workflow の拡張" (2026-10-05。「設計の原則」「構造変更で遭遇したもの」)
  - Claude Code conversation "workflow の導入フックで作るリポジトリ構成の見直し" (2026-10-06。トップの `notes` → `works` の rename と `certs` の移動)
  - Claude Code conversation "Vault のトップの rename と certs の移動" / "Vault のトップの rename の完了確認と旧パスの整理" (2026-10-06。「rename と旧名の扱い」)
  - Claude Code conversation "Vault を $HOME\works へ移し、Linux 側の並びをそろえる" (2026-10-06。現在形のパスを `$HOME\works` に直した)
---

# Obsidian Vault

## Purpose

このナレッジベース（exmem）を閲覧・管理しているObsidian Vaultの環境と、ナレッジベースから使っている機能をまとめる。

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
- ファイル一覧は、行の余白を詰め、フォントサイズをエディタと同じにし、アイコンを CSS の `mask` だけで付ける（Lucide と同じ形）。プラグインを読み込まないので起動が重くならない。却下案: Iconize プラグイン（JS を読み込むため起動が重くなる可能性）。2026-10-04 に、種類ごとの色分け、開閉フォルダの色、タブ・タイトルバーの色の上書きを足した。インデントは CSS で変えられず見送った。詳細は [[obsidian-appearance]]。
- 改行コードは `.gitattributes` の `* text=auto eol=lf` で LF に統一する。Obsidian が `app.json` と `appearance.json` を LF で書き戻した（2026-10-03、CRLF で書いたファイルが数分後に LF になっていた）。AI と WSL/Linux の出力も LF。却下案: CRLF に統一する（一度実施したが、Obsidian が保存するたびに全行が変更扱いになる）。
- 本文の幅は、フォントサイズに比例させる（`--file-line-width: 58em`）。既定の固定 700px は、拡大しても幅が変わらず1行の文字数だけが減る。却下案: 幅の制限をなくす、64em（試して 58em にした。1週間の試用で確定する）。
- 新規ノートの保存先は現在のフォルダにし、`_local/` は検索対象のままにする。新規作成はほぼしない。`exmem/inbox` は AI 出力をナレッジ化する入口で別の用途。`_local/` は PC ローカルのデータなので検索できる必要がある。
- 検索から除外するフィルターは `.tmp.`、`_archive/`、`.claude/`。AI が書き込み途中に作る一時ファイル、古い資料、エージェントの設定を検索やリンク補完に出さない。
- （2026-10-05 に変更: トップの `AGENTS.md` は PC ごとのローカルなファイルになり、Vault 全体の規約は `workbase` のルートの `AGENTS.md` に移った。以下は当時の記述）Vault のルートに共有の `AGENTS.md` と `CLAUDE.md`（`@AGENTS.md`）を置く。ルートで起動した AI に、共有とローカルの境界、`_local/`、リンクの規則、`.obsidian` の編集時の注意、書式を伝える。内容に機密が無いので共有する。却下案: ローカル専用にする。

### コアプラグイン
<!-- 版依存: 一方向 / 確認: 2026-10-04 -->

- 有効: `file-explorer`、`global-search`、`switcher`、`backlink`、`outgoing-link`、`tag-pane`、`properties`、`page-preview`、`command-palette`、`editor-status`、`bookmarks`、`outline`、`word-count`、`file-recovery`、`sync`、`bases`
- 無効: `graph`、`canvas`、`daily-notes`、`templates`、`note-composer`、`footnotes`、`slash-command`、`markdown-importer`、`zk-prefixer`、`random-note`、`slides`、`audio-recorder`、`workspaces`、`publish`、`webviewer`
- 2026-10-01 時点では `graph`、`canvas`、`daily-notes`、`templates`、`note-composer` が有効で、`properties` が無効だった。2026-10-03 の `82953b7`（コミットメッセージは「使っていないプラグインと古い設定を削除」）で逆になった。

### コミュニティプラグイン
<!-- 版依存: 一方向 / 確認: 2026-10-04 -->

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

## Gotchas

### 2026-10-03 の再構成で遭遇したもの

- **ディレクトリの `git mv` が Permission denied**: `git mv exmem resources/exmem` が失敗した。`exmem` がエージェントの作業ディレクトリで、Windows が使用中のディレクトリの名前変更を拒否したため。中身を1つずつ `git mv` して回避した。空になった旧 `exmem/` はセッション終了後に削除する（2026-10-03 時点で `notes` 直下に `exmem/` は残っていない）。
- **`C:\vault\notes` が存在しない扱いになる**: 実体は `notes.lnk`（Windows のショートカット）だった。`.lnk` はシェルが解釈する普通のファイルで、PowerShell・git・Obsidian は辿らない。`New-Item -ItemType Junction`（管理者権限は不要）で作り直した。
- **LFS の除外設定の前に `git add` すると、README が LFS ポインタになる**: `.gitattributes` が `resources/fonts/**` を LFS にしていて、`fonts/README.md` までポインタとして登録された。除外行を足して `git rm --cached` と再 `git add` で直し、未 push のコミットを amend した。`.gitattributes` を先に完成させてから `git add` する。
- **`.gitignore` の途中に `/` を含むパターンはルート基準になる**: `_local/*` は深い階層の `_local/` に効かない。`**/_local/*` と `!**/_local/.gitkeep` にして `check-ignore` で確認した。
- **ファイルを書き込めなかった（一時的）**: PowerShell の `Set-Content` が「別のプロセスが使用中」で失敗した（原因は不明。Obsidian か Sync が掴んでいた可能性、未確認）。Edit ツールでの置換は成功した。

### 2026-10-06 の Project の移動（`projects/` → `archives/`）で遭遇したもの

- **ディレクトリごとの `git mv` が、再び `Permission denied` で失敗した**: 原因は未特定（上の 2026-10-03 と同種の可能性）。ファイル単位で `git mv` するとリネームとして履歴が保たれた。詳しくは [[windows-cli-pitfalls]]、PARA の運用は [[para-operations]]。

### 2026-10-05 の構造変更（共有とローカルの分離）で遭遇したもの

- **新しいトップを雛形から作ったとき、旧ルートにあった `.gitattributes`（改行コードを LF に統一）が引き継がれなかった**: 旧ルートの全ファイルを棚卸ししなかった（切り替えの後の点検で発見）。トップに `.gitattributes` を置き、雛形にも足した（確認: 2026-10-05、根拠: `C:\vault\notes\.gitattributes` が `* text=auto eol=lf`）。
- **PowerShell の `Set-Content` で作ったファイルを `git add` したとき、「CRLF will be replaced by LF」の警告が出た**: `Set-Content` が Windows の改行（CRLF）で書く。`.gitattributes` があるので、コミットされる内容は LF に正規化される。害は無いが、作業ツリーを LF にするなら、LF で書き直す（.NET の `WriteAllText` など）。

### 2026-10-03〜04 の設定整理で遭遇したもの

- **Obsidian の起動中に `appearance.json` を編集して、有効にしたスニペットを追記したら消えた**: Obsidian が追記前の内容で設定を上書きしたため（仮説）。追記し直してコミットし、設定画面でスニペットがオンか確認した。
- **`git commit` が `.git/index.lock` の存在で失敗した**: Git の GUI（Fork）が動いていて、リポジトリを更新していた（仮説。確認時にはロックが消えていた）。数秒後の再実行で成功した。
- **`obsidian-vault.md` の編集がロックで失敗することがある**: 2026-10-04 に Edit ツールで `EPERM`（アトミック書き込みの rename 失敗）が出た。Obsidian が開いているファイルで起きるとみられ、再実行で成功した。

### Vaultを移したあと、古い場所を編集していた

- 状況: 2026-10-01 にナレッジベースを `C:\Users\<ユーザー名>\vault\notes` 配下から `C:\vault\notes\areas_shared\exmem` へ移したが、AIエージェントは古い場所を作業ディレクトリとして開いたまま編集を続けた。
- 解決: 変更を exmem へ移し、古い場所は削除した。エージェントは `C:\vault\notes\areas_shared\exmem` を作業ディレクトリとして起動した（2026-10-02 の構造見直しで `C:\vault\notes\resources\exmem` に変わる）。

## Proposals

Vault全体に影響し、Syncで他の端末にも伝わる。2026-10-03 時点の扱いを、項目ごとに書く（適用済み・却下・見送り）。

- 新規ノートの保存先を `resources/exmem/inbox` にする。モバイルで新規ノートを作るだけで inbox に入る。**2026-10-03 に、現在のフォルダにする（`newFileLocation: current`）と決めた**（`exmem/inbox` は AI 出力をナレッジ化する入口で、新規ノートとは別の用途のため。却下）。
- `created` / `updated` のプロパティ型を「日付」にする。**採用済み**（2026-10-03、`types.json`）。
- Templatesで知識ノート用のテンプレートを作る。Templates は参照専用の方針で無効にした（2026-10-03）ので、見送り。

## Related

- [[ai-development-workflow]]
- [[app-config-placement]]
- [[obsidian-appearance]]
- [[git-subdirectory-split]]
- [[modern-cli-tools]]
- [[tags]]
- [[obsidian-vault-structure]]
- [[obsidian-vault-backup]]
