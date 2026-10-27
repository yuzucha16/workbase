---
type: knowledge
title: Windows 向けスクリプトを隔離した Linux で作って検査する
status: active
tags:
  - tool/wsl
  - shell
  - testing
  - windows
aliases:
  - windows-script-isolated-linux
triggers: [ps1, bat, 静的検査, 隔離, pwsh, 部屋, Windows 向けスクリプト, shellcheck, PSScriptAnalyzer]
created: 2026-10-21
updated: 2026-10-27
sources:
  - Claude Code conversation "部屋での bat・ps1 の作成と静的チェック" (2026-10-21)
---

# Windows 向けスクリプトを隔離した Linux で作って検査する

全体の方針は [[shell-script-testing-wsl]]（2026-10-27 に、追記の節を切り出した）。

## Windows で実行するスクリプトを、隔離した Linux の環境で作って検査する（2026-10-21 追記）

Windows を呼べない隔離した WSL（AI 作業部屋。[[ai-isolated-work-room]]）で AI が bat・ps1 を作ると、構文や文字コードの誤りが Windows で初めて見つかり、デバッグが多かった。実行できない前提で、構成と検査をどうするかを決めた。

### Principles（ps1・bat の構成と検査）

- 人が複数のスクリプトを1回で実行したいだけなら、束ねる役も個別の処理と同じ言語（ps1）で書き、bat は起動用の定型だけにする。理由: bat 固有の失敗（文字コード、LF でラベルが見つからない、`call` 忘れ）は、bat にロジックを書くから起き、ロジックを持たなければ出ない。
- 隔離環境で実行できる処理は、その環境で実行して確かめる。Windows 依存の操作（Excel の VBA・COM、レジストリ、インストール）だけを薄い層に切り出し、判定・変換・検証はその外に置く。理由: 外側は環境内の実行でテストでき、人が Windows で試す範囲が狭まる。
- 実行できない層にも、構文解析・静的解析・差し替えテストはできるよう、処理系（Linux 版の pwsh 7）と解析・テストの道具を、版を固定して隔離環境に入れる。理由: 「Windows で初めて気づく」誤りの大半（構文、未定義の変数、引用符）を、人が実行する前に取れる。
- AI が読める場所へ自動で出すログは、マスクを通らない。出力先と、出すかどうかを、最初に決める（既定では出さず、人が付けたときだけ出す）。理由: 一度出ると、実データの語、ユーザー名、パスが AI に渡る。
- 人の手数は、人が打つ1コマンドにする。実行の前提（Excel を閉じる、入力の有無）は束ねる側が確認し、満たされなければ何をすればよいかを表示して止まる。理由: 手順を人が覚えていると、忘れて未実行になる。

### Decisions（ps1・bat）

- **起動用 bat は、3行の型（`@echo off` は省略可、`pwsh -NoProfile -File "%~dp0<名前>.ps1"`、`pause`）だけ許す。束ねる役は ps1 にする**（2026-10-21）
  - 根拠: bat は、ps1 を束ねて1回で実行する人の手間を省く入口にすぎず、bat 自体に価値は無い（ユーザーの決定）。
  - 却下案: bat にロジックを書く（文字コードとラベルの失敗が出る）、AI が Windows で実行する承認つきの仕組み（用途に対して過剰で、結果を AI に戻す経路も無い）。
- **隔離環境の静的検査は、Linux 版 pwsh 7 を版固定で入れる案にする（PSScriptAnalyzer と Pester を含む。pwsh は 7 に固定）**（2026-10-21）
  - 根拠: ps1 の誤りの大半は構文・変数・引用符で、Parser と PSScriptAnalyzer で取れる。Python では PowerShell の構文を解析できない（ユーザーの承認）。
  - 却下案: Python だけで検査する（BOM・改行などの規約の一部しか見られない）。
- **束ねる ps1 のログ出力は、機能として残し、既定では出さない（`-Log` のときだけ）**（2026-10-21）
  - 根拠: ログを AI が読める領域に自動で出すと、マスクを通らない（ユーザーの指摘で、失念していたと訂正）。
  - 却下案: 常に AI の作業領域へ出す（初案）、成果物の隣へ出す（配布物に混ざる）。

### Facts（ps1・bat）

- PowerShell の公式リリースの `hashes.sha256` は UTF-16 LE で配られる。UTF-8 として読むと文字の間に空白が入り、検索に当たらない。Unicode でデコードすると `linux-x64.tar.gz` の行が取れた（確認: 2026-10-21、根拠: v7.6.7 の `hashes.sha256` を取得してデコードを比べた）。
- 公式の Linux 版 tarball の SHA-256 は、取得したファイルの `Get-FileHash` と、`hashes.sha256` の値が一致した（確認: 2026-10-21、根拠: v7.6.7 の x64 を取得して照合した）。
- Linux 版 pwsh は、tarball を展開するだけで動く。ICU に頼らないよう `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` を指定した包みから、Ubuntu 26.04 の部屋で `pwsh --version` が 7.6.7 と出た（確認: 2026-10-21、根拠: 部屋の一般ユーザーで実行した）。この指定では、日付や数値の書式など、文化に依存する動作が Windows と違いうる（仮説）。
- PSScriptAnalyzer と Pester 5 は、pwsh 7.6.7 に同梱されていない。Windows 側の Modules にも無く、Windows PowerShell 5.1 側には Pester 3.4.0 だけがあった（確認: 2026-10-21、根拠: `Get-Module -ListAvailable`）。
- PSScriptAnalyzer 1.25.0 は Linux 版 pwsh で、`Invoke-Expression`、未使用の変数、未使用の引数を Warning として検出した。Pester 5.9.1 は `Mock` を含むテストが通った（確認: 2026-10-21、根拠: 一時ディレクトリでの実行）。
- `Find-PSResource -Version '5.*'` は5系に絞らず、6系も返した。5系に絞るには `'[5.0.0,5.99.99]'` と書く（確認: 2026-10-21、根拠: 実行の出力）。
- `Start-Transcript` の先頭には、Windows のユーザー名とマシン名が入る（確認: 2026-10-21、根拠: 出力されたログのヘッダー）。
- 未処理のエラーの表示は、`finally` で `Stop-Transcript` した後になるので、ログに入らない。ログに残したいエラーは、`catch` の中で書く（仮説）。補足: 初めから `catch` で書く型にしたので、入らない状況は再現していない。
- 上の案は、部屋を作る `init` の手順として実装されている: pwsh 7（公式 tarball、チェックサム確認つき）、PSScriptAnalyzer と Pester（版を固定、`-Scope AllUsers`）、`DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` の包み（確認: 2026-10-21、根拠: `room.py` の `PWSH_INSTALL` と単体テストを読んだ）。

### Gotchas（ps1・bat）

- 状況: 工程を順に呼ぶ束ねる ps1 で、`Set-StrictMode -Version Latest` の下、`$LASTEXITCODE` で成否を見た
  - 原因: 外部コマンドをまだ呼んでいない状態の `$LASTEXITCODE` は未設定で、読むと「has not been set」のエラーで止まる
  - 解決: 呼ぶ前に `$global:LASTEXITCODE = 0` を入れ、`-ne 0` で判定した
- 状況: 一時の `HOME` で `Install-PSResource` を実行した
  - 原因: `HOME` 配下の `.local/share` が無く、リポジトリの設定を読めなかった。また、`-TrustRepository` が無いと、対話の確認で止まる
  - 解決: `.local/share` と `.config` を先に作り、`-TrustRepository` を付けた
- 状況: 検査スクリプトで、指摘を1件ずつ数えたうえで、「指摘が無い」というまとめの行も数えた
  - 原因: まとめの行の既定の重大度が FAIL で、Warning だけでも FAIL が1件増えた
  - 解決: まとめの行は、指摘が0件のときだけ PASS として数えた

### Open Questions（ps1・bat）

- 実行先の Windows に Python（または uv）があるか。あれば、Windows 依存の薄い層も Python にできる。
- TLS 検査のあるネットワークで、GitHub と PSGallery からの取得が通るか。
- 隔離環境の AI が、案内に従って束ねる ps1 と3行の bat を作り、検査を使うか。

### Next Actions（ps1・bat）

- 実行先の Windows で、Python と uv の有無を確かめる（2026-10-21 時点）。
- 部屋の AI に束ねる ps1 を1本作らせ、検査と `-Log` の使われ方を観察する（2026-10-21 時点）。

## Related

- [[shell-script-testing-wsl]]
