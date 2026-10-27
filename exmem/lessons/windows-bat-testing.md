---
type: knowledge
title: Windows の .bat の試験（dry-run・偽コマンド）
status: active
tags:
  - tool/wsl
  - shell
  - testing
  - windows
aliases:
  - windows-bat-testing
triggers: [.bat, バッチ, バッチファイル, 20_apps, scoop, dry-run, 偽物, PS_EXE, PowerShell 1行, 試験, バッチの試験]
created: 2026-10-06
updated: 2026-10-27
sources:
  - Claude Code conversation "release.bat の文字化け" (2026-10-19)
  - Claude Code conversation "セットアップ bat の pause・SKIP ログ・環境変数ログ" (2026-10-10)
---

# Windows の .bat の試験（dry-run・偽コマンド）

全体の方針は [[shell-script-testing-wsl]]（2026-10-27 に、追記の節を切り出した）。

## Windows のバッチスクリプトの試験（2026-10-06 追記）

Scoop でアプリを入れる Windows のバッチ（dotfiles の `20_apps.bat`）を、ネットワークにも実環境の scoop にも触れずに試験する方法。WSL 側の `tests/linux/` と対称にした。【汎用】は他のバッチにも使える内容、【この件】は dotfiles の `tests/windows/test_20_apps.ps1`（2026-10-06）に固有の内容。導入の中身は [[scoop-app-management]]。

### Principles（バッチ）

- 【汎用】数十 MiB を超える導入（ダウンロードを伴うインストール）は、試験では実行せず dry-run にする。外部コマンドを、引数を記録するだけの偽物に差し替える。通信とストレージの負荷を避け、再実行しても同じ結果になる。
- 【汎用】スクリプトが外部実行ファイルを完全パスで呼ぶときは、差し替え用の環境変数（未設定なら本来の完全パス）を1つ用意する。完全パスの呼び出しは PATH の先頭に偽物を置いても差し替わらない。
- 【汎用】ホームを指す環境変数（`USERPROFILE`）を一時ディレクトリに差し替え、実環境の scoop や設定に触れない。Linux の「偽の HOME」と同じ。
- 【汎用】バッチ内に埋め込んだ PowerShell の1行は、呼び出し記録の文字列照合だけでなく、取り出して実際に実行し、コマンドレットを偽物に差し替えて分岐を試験する。文字列が合っていても、分岐の条件が正しいかは実行しないと分からない。

### Decisions（バッチ）

- **導入そのものは実行せず dry-run とし、数十 MiB を超える導入は試験に含めない**（2026-10-06）
  - 根拠: ユーザーの制約。通信とストレージの負荷になる。
  - 却下案: 使い捨て環境で実際に導入する（負荷が大きい。実際の導入は、新しいアカウントか VM での確認に回す）。
- **試験を `tests/windows/test_20_apps.ps1` として保存する**（2026-10-06）
  - 根拠: ユーザーの依頼で、`tests/linux/` と対称にする。スクリプトを変えるたびに再実行できる。
  - 却下案: 試験のたびに使い捨てる（再利用できない。WSL 側も同じ理由で保存に改めた）。

### Facts（バッチ）

- 【汎用】偽の `scoop.cmd`（引数をログに追記するだけ）と、偽の `powershell.exe` の代わりの `.cmd`（引数を記録し、成功時は偽の `scoop.cmd` を作る）で、「scoop が無く導入成功」「導入失敗」「scoop が既にある」の3場面を試験できる（確認: 2026-10-06、根拠: 12項目が合格）。
- 【汎用】バッチの末尾の `pause` は、標準入力を `< nul` にすると EOF で抜けるので、試験が止まらない（確認: 2026-10-06、根拠: `cmd /c "<bat> < nul"` の試験が完了した）。
- 【汎用】PowerShell の関数は、同名のコマンドレットより優先される。`function Set-ExecutionPolicy { ... }` で偽物に差し替えた状態で、取り出した1行を実行できる（確認: 2026-10-06、根拠: 分岐6項目が合格し、実機の CurrentUser ポリシーは試験の前後で RemoteSigned のまま）。
- 【汎用】`powershell.exe -ExecutionPolicy <値>`（Process スコープ）で、実効ポリシーを作れる。レジストリは書かないので、実機の設定を変えずに試験できる（確認: 2026-10-06、根拠: 同上）。
- 【この件】試験は18項目: バッチの3場面12項目と、埋め込み PowerShell の6項目（`Restricted` `AllSigned` は設定して導入、`RemoteSigned` `Unrestricted` `Bypass` は設定せず導入、設定失敗は警告して続行）。すべて合格した（確認: 2026-10-06、根拠: メモに記録された出力 `failures=0`）。
- 【この件】`tests/windows/test_20_apps.ps1` と `tests/linux/test_scripts.sh` が dotfiles にある。`20_apps.bat` に `PS_EXE`（未設定なら `%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe`）が足されている（確認: 2026-10-06、根拠: ファイルの存在）。Linux 側の試験の保存（`tests/linux/`）も、上の WSL 節の Open Questions（置き場）の答えになっている。
- 【この件】実機の新しい Windows アカウントでの導入は未確認（仮説: 実機でも試験と同じ分岐になる）。

### Gotchas（バッチ）

- **偽の `powershell` を `.cmd` で作り、バッチから `"%PS_EXE%" ...` と呼んだら、バッチがそこで終わり、後続の `scoop install` に進まなかった**: バッチから別の `.cmd` を `call` なしで呼ぶと、制御が戻らない（本物の `.exe` では起きない）。呼び出しを `call "%PS_EXE%" ...` にした。`.exe` に `call` を付けても挙動は変わらない。

### Open Questions（バッチ）

- 差し替え用の `PS_EXE` を本番のバッチに残すか、試験用の包みスクリプトで差し替えるか（未決。WSL 側の `PROC_VERSION_FILE` と同じ論点）。AI は本番に残す現状を採った（AI の判断。未承認）。
- 実機（新しい Windows アカウント）で、導入が通るかは未確認。本物の導入を1回は確認する必要がある。
- 試験の対象は `20_apps.bat` だけ。ほかの `.bat`（`30_link.bat` など）への展開は未定。

## 切り出したノート

- [[windows-bat-pitfalls]]: 全体 ASCII の正、cp932 の草稿、`set /p`・`errorlevel`・ANSI の落とし穴（2026-10-06〜10-20）
- [[windows-bat-eol-and-log]]: 生成した `.bat` の LF とラベル、セットアップ用 `.bat` の pause・SKIP・環境変数のログ（2026-10-10）

## Related

- [[shell-script-testing-wsl]]
