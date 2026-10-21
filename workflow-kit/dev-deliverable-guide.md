# `type: dev` の成果物の作り方

`type: dev` の Project で、AI に作らせて AI に保守させるツール（成果物）の、構成・文書・テスト・チェックの型。`open` と `start` が、`type` が `dev` `dev-env` `dev-test` のときだけ読む（`dev-env` `dev-test` は、末尾の「`dev-env` と `dev-test`」の差分で読み替える）。理由と根拠は `exmem/lessons/ai-tool-deliverable-structure.md`（他環境1か所の実績に基づく。この環境では未検証）。Excel VBA 固有の落とし穴は `exmem/lessons/excel-vba-ai-development.md`。

記号: `<Area>` は責任領域、`<Project>` は作業の単位、`<成果物名>` は配布する成果物1つ。1 Project = 1 成果物（`open-hook.md` の判断基準）。複数なら Project を分ける。

## 置き場（AI 作業部屋の Project）

```
projects/<Project>/
├─ README.md            Project の窓口（目的・完了条件）。部屋の AI は書けない。写しが ai/ctx/ に入る
├─ ai/                  部屋の AI が見えるのはここだけ
│  ├─ docs/             作業の記録（log.md と decisions.md）だけ。仕様書は入れない
│  ├─ in/               受け取った参考資料、マスク済みの入力
│  ├─ work/             中間成果物、使い捨てのスクリプト
│  └─ out/<成果物名>/   配布する成果物（下の構成）。close.md や stock/ とは別のサブフォルダ
└─ _noai/               AI に見せない（raw/ 元データ、map/ 対応表、final/ 復元済みの成果物）
```

Area の共通ルール（Project を跨ぐ約束）は、Area の README に書く。部屋の AI は `ai/ctx/area-README.md` で読む。Project 固有の約束は、成果物の README か、Project の `ai/docs/decisions.md` に置く。

## 成果物の構成（`ai/out/<成果物名>/`）

| パス | 内容 |
|---|---|
| `README.md` | 利用者向けの入口。章立ては下の「README の型」 |
| `src/` | ソース。正本と、そこから生成する派生物（実行環境が要求する形式） |
| `docs/` | 正本の文書（要求仕様書、機能仕様書、運用マニュアル） |
| `tests/` | 自動テスト。末尾に「範囲外（実環境で確認する）」 |
| `tools/` | 変換・検査・生成のスクリプト |

HTML など、`docs/` から生成するものは派生物。直接編集しない。

## 守ること

- 編集するのは正本だけ。派生物はスクリプトで生成する。検査に失敗したら何も書き出さない。
- 仕様書の識別子（関数名・定数名・シート名・セル番地）は、ソースと同じにする。食い違ったらソースが正で、文書を直す。
- 異常を見つけたら、何も書かずに中止する、または「要チェック」にして人に渡す。
- 設定値は先頭の定数に集め、一覧を機能仕様書に載せる。色・文言・書式は、決めたら1か所に書く。
- 未確認を確認済みと書かない。README の状況表に、実環境での確認の有無を書く。
- 同日の仕様変更は、要求 → 機能 → 運用 → README → テスト → 派生物の順に、全層をそろえる。

## 文書の型

- 3点セットは、「変更」（`methods.md`）の基準文書を兼ねる（`work/` の中間成果物は作業中の下書きで、別物）。
- 3点セット: 要求仕様書（何を満たすか。ID 付き、1 ID = 1要求 = 検証できる文）→ 機能仕様書（どう実現するか）→ 運用マニュアル（使い方と困ったとき）。ID は、既存の最後の番号の次から振る（欠番や振り直しをしない）。
- 要求は「〜する」で言い切り、数値・文言まで具体的に書く。中止の条件を列挙する。未確認は明記する。
- 図は1章に全体図を入れ、入力・本体・出力の3区分で説明する。用語表で、同じ概念に別の語を使わない。
- README の型: 状況（実環境での確認の有無を含む表）→ 実行環境 → ファイル構成（何が正本で、どれが生成物か、再生成のコマンド）→ 変更後の標準手順 → 導入 → 使い方 → 設定 → 注意。README と `docs/` で、同じ表を重複させない。
- 保守を AI に頼むため、運用マニュアルに変更依頼のひな形を持たせる。順序は、背景 → 入力 → 守ること → 出力の形式 → 注意 → 変更依頼。記入欄は、種類・したいこと・期待する動作・現在の動作・変えてはいけないこと・確認方法の希望。不具合のときは、再現手順、エラー全文（工程名つき）、結果の全文、期待値と実際の値を足す。

## テスト

- 2層に分ける。部屋の中で完結する層（合成データの自動テスト）は AI が実行する。実環境が要る層（Excel などのアプリ、実データでの見た目）は人が Windows で実行する。
- 合成データはスクリプトの中で作る。実データ・個人名・金額は使わない。
- 出力は `PASS <名前>` / `FAIL <名前> <詳細>` と最後の件数。終了コードは全件合格で 0、不合格ありで 1。所要は1分未満を目安にする。
- 区分の型: 準備、正常系（対象外と入力ファイルが不変であることを含む）、ログ、別モード、中止（何も書かれていないことを確認）。
- 実環境で実行した結果を AI に渡すときは、人が実データの語を伏せてから渡す（`ai/` と `_noai/` の往復を減らすため、できるだけ部屋の中のテストで済ませる）。

## チェック

立ち上げ（`open` / 最初の `start`）:

1. 曖昧な点を先に聞く（入力の取り方、置き場所、既定の挙動、境界ケース）。答えは `ai/docs/decisions.md` に「ユーザー回答」として残す。依頼文の誤記は、解釈の根拠を備考に残す。
2. 正本ソースを書く（定数を先頭に集める）。検査して派生物を生成する。
3. 合成データのテストを、ソースと並行して育てる。
4. 文書を、要求 → 機能 → 運用 → README の順に、ソースを見て識別子を合わせて書く。
5. `ai/docs/log.md` と `decisions.md` を更新する。報告に、「実環境で未確認の点」と「利用者にお願いする確認」を書く。

完了の定義: 検査が通り派生物が最新 / 自動テストが全件合格（件数を記録）/ 文書が最新で識別子がソースと一致 / 派生物を再生成済み / README の状況表に実環境での確認の有無を正直に書いた / 記録を更新した。

## `dev-env` と `dev-test`

`dev` の工程のうち、環境構築とテストだけを成果物にする Project（2026-10-16 に足した叩き台。実測が無い）。`dev-env` が想定するのは、主に**テスト環境を作る**こと。上の型（置き場、守ること、README の型、テストの2層、完了の定義）は、そのまま使う。違いだけをここに書く。

`dev` との関係: 子の Project ではなく、独立の Project（1 Project = 1 成果物。Project は入れ子にしない）。成果物の受け渡しは、ほかの Project と同じく、人が次の Project の `ai/in/` に置き、`room start --adopt` で入力として記録する。例: `dev-env` の成果物 → `dev` の `ai/in/`、`dev` の要求仕様書とソース → `dev-test` の `ai/in/`。

| | `dev-env`（環境構築） | `dev-test`（テスト） |
|---|---|---|
| 成果物（`ai/out/<成果物名>/`） | 環境定義（`src/` にセットアップのスクリプト、コンテナ定義、版の固定ファイル）、`tools/` に確認スクリプト、README（導入手順）、`report.md`（確認の結果と版の一覧） | `tests/`、`tools/`（実行スクリプト）、`report.md`（実行結果。件数と、実環境での確認の有無） |
| 基準文書（`docs/`） | 環境の要求仕様（対象、道具と版、ID 付きの検証項目）と運用マニュアル（導入、困ったとき）。機能仕様書は省いてよい | テスト仕様（要求 ID とテストの対応表、観点、合否の基準）。正の向きは、テスト対象の要求仕様（`ai/in/`）。食い違いは対象の Project に返す |
| 立ち上げで聞くこと | 対象環境（OS、ネットワークの有無、管理者権限）、環境の置き場（下の表）、再現の方式（スクリプト、コンテナ、手順書）、版の固定の要否 | テスト対象と、その要求仕様の版、層（部屋の中の自動テスト / 実環境で人が実行）、合否の基準 |
| 完了条件の例 | 新しい環境でセットアップを実行し、確認スクリプトが全件 PASS する（版の一覧を `report.md` に記録） | 要求仕様のすべての ID にテストが対応し（対応表に欠けが無い）、部屋の中の自動テストが全件実行され、結果を `report.md` に記録した |

環境の置き場（`dev-env` で聞く。答えで、公開時の扱い、検証する人、基準文書の正の向きが決まる）:

| 置き場 | AI ができること | 注意 |
|---|---|---|
| ローカル（部屋の中） | 作って、検査まで実行する | 通常の `dev-env` |
| リモート・コンテナ（WSL から SSH で、user 権限で操作する場合を含む） | 部屋からは届かない。定義とスクリプトを作り、実行と確認は人が行う | ホスト名・認証情報はマスクして `ai/in/` に渡す。`remote` という type にする案がある（下の未決。`dev` でも使える） |
| リポジトリ（公開 / 非公開） | ファイルを作る | 公開なら秘匿値・社内のホスト名・絶対パスの検索を完了条件に入れる。正の向きはリポジトリ側（`open-hook.md` の未決） |
| GitHub / GitLab のようなサービス（CI、権限、設定） | できない（権限が無い）。ワークフローのファイルの案までで、設定と実行は人が行う | この仕組みでは AI に任せられない。人の作業として扱う |

- `dev-env` は、部屋の中では実環境を作れない。部屋の中で確かめるのは、スクリプトの静的な検査と、作れるならコンテナでの実行まで。実環境での実行と結果の記録は人が行う（検証項目に「人が実行」と書く）。
- `dev-test` は、テスト対象を直さない（`ai/in/` は読み取り専用）。不具合は `report.md` に書き、対象の Project に返す。テストの不合格は、成果物の失敗ではない（完了条件は「対応と実行と記録」）。
- テスト対象がリポジトリの clone のときの置き場は、`open-hook.md` の未決（リポジトリが正の `src`）に従う。

## Windows で実行するスクリプト（ps1 と起動用 bat）

成果物に、人が Windows で実行するスクリプトを含むときの規約（2026-10-21 のユーザーの決定。全 type 共通）。bat は、ps1 を束ねて 1 回で実行したいという人の手間を省くための入口にすぎず、bat 自体に価値は無い。bat の失敗（日本語の文字化け、LF でラベルが見つからない、`call` 忘れ）は、bat にロジックを書くから起きる。

- **ロジックは ps1 に書く。束ねる役も ps1 にする**: 個別の処理を `<名前>.ps1` に分け、それらを順に呼ぶ 1 本（例: `run-all.ps1`）を置く。失敗したら止まる、ログを 1 か所に出す、最後に結果の一覧を出す、を束ねる側に持たせる。人は `pwsh -File run-all.ps1` を 1 回打つだけにする。
- **bat は、起動用の 3 行だけ許す**。ダブルクリックで動かしたい場合の入口で、ロジック（`if`、`goto`、ラベル、変数、`setlocal`）は書かない。型は固定:

  ```bat
  @echo off
  pwsh -NoProfile -File "%~dp0run-all.ps1"
  pause
  ```

  1 行目は省いてよい。2 行目の `run-all.ps1` は、同じ場所にある呼び先の名前に変える。ファイルは全体 ASCII、CRLF、BOM なしで書く（`exmem/lessons/shell-script-testing-wsl.md` の bat の落とし穴は、この型に従えば出ない）。`pause` を最後に必ず置く（終わっても画面が閉じない）。
- **束ねる ps1 に、ログ出力の機能を持たせる。ただし既定では出さない**（2026-10-21 のユーザーの依頼と訂正。ログは `ai/` の中に出ると部屋の AI から読めるので、人が付けたときだけ出す）。`-Log` を付けると、Project の `ai/work/<束ねる ps1 の名前>.log` の 1 本に出す。`-LogDir <パス>` なら、その場所に出す（`-Log` は不要）。成果物（`ai/out/<成果物名>/`）の中には出さない（配布物に混ざるため）。`ai/work/` は、束ねる ps1 の置き場から親をたどって、`work/` を持つ `ai` ディレクトリを探す。見つからないとき（Project の外、配布先で実行したとき）は、束ねる ps1 の隣の `work/`。実行のたびに上書きする。個別の ps1 は、ログを作らない。エラーが出たら、人が `-Log` を付けて再実行し、AI に「`ai/work/<名前>.log` を読んで」と伝える。起動用 bat に引数を渡したいときは、2 行目の末尾に ` %*` を足してよい（`run-all.bat -Log`）。型（動作確認済み: Windows の pwsh 7.6.7、失敗した工程・終了コード・スタックがログに残る）:

  ```powershell
  #Requires -Version 7
  param([switch]$Log, [string]$LogDir)
  Set-StrictMode -Version Latest
  $ErrorActionPreference = 'Stop'

  function Find-AiWork {
    $dir = Get-Item -LiteralPath $PSScriptRoot
    while ($dir) {
      if ($dir.Name -eq 'ai' -and (Test-Path -LiteralPath (Join-Path $dir.FullName 'work'))) { return Join-Path $dir.FullName 'work' }
      $dir = $dir.Parent
    }
    return Join-Path $PSScriptRoot 'work'             # Project の外で実行したとき
  }
  $logging = $Log -or [bool]$LogDir                   # 既定ではログを出さない（-Log か -LogDir を付けたときだけ）
  if ($logging) {
    if (-not $LogDir) { $LogDir = Find-AiWork }
    $logPath = Join-Path $LogDir ([IO.Path]::GetFileNameWithoutExtension($PSCommandPath) + '.log')
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    Start-Transcript -Path $logPath -Force | Out-Null
    Write-Host "[LOG] $logPath"
  }
  $exitCode = 0
  try {
    foreach ($step in 'step1.ps1', 'step2.ps1') {   # 実際の工程名に変える
      Write-Host "[STEP] $step"
      $global:LASTEXITCODE = 0                        # Set-StrictMode の下で、未設定の参照を避ける
      & (Join-Path $PSScriptRoot $step)
      if ($LASTEXITCODE -ne 0) { throw "$step が終了コード $LASTEXITCODE で終わった" }
    }
    Write-Host '[OK] すべて完了'
  } catch {
    Write-Host "[ERROR] $($_.Exception.Message)"      # catch の中で書く（finally の後ではログに入らない）
    Write-Host $_.ScriptStackTrace
    $exitCode = 1
  } finally {
    if ($logging) { Stop-Transcript | Out-Null }
  }
  exit $exitCode
  ```

  **`-Log` のログは `ai/` の中に出るので、部屋の AI から読める**（マスクを通らない）。ログの先頭（transcript のヘッダー）に Windows のユーザー名とマシン名が入り、パス（ユーザー名を含みうる）やエラー文も入る。実データを処理する実行（マスクして復元する Project の本番）では、実データの語がログに出ないことを確認するか、`-LogDir` で `ai/` の外（例: `_noai/user/`）に出す。部屋の AI に見せるのは、人が伏せてからにする。
- **実行は PowerShell 7（`pwsh`）に固定する**。ps1 の先頭に `#Requires -Version 7`、`Set-StrictMode -Version Latest`、`$ErrorActionPreference = 'Stop'` を置く。5.1（`powershell.exe`）では動かさない（UTF-8 の扱いと文字化けの差を避けるため）。ps1 は UTF-8 で保存する。
- **部屋の中で、作った直後に静的チェッカーを実行する**。実行はしない（部屋には Windows が無い）が、構文と規約の誤りは、人が Windows で実行する前に取れる:

  ```
  pwsh -NoProfile -File ~/shared/workflow-kit/tools/check-ps1.ps1 <成果物のディレクトリ>
  pwsh -NoProfile -File ~/shared/workflow-kit/tools/check-ps1.ps1 -RunTests <成果物のディレクトリ>   # *.Tests.ps1 を Pester 5 で実行する
  ```

  FAIL は直してから人に渡す。WARN は、理由を見て判断する。終了コードは FAIL の数。見るもの: UTF-8、改行の混在、構文、`#Requires`、`$ErrorActionPreference`、`Set-StrictMode`、PSScriptAnalyzer、起動用 bat の型（上の 3 行、呼び先の存在）。
- **部屋の中のテストは、外部とのやり取りを差し替える**。Windows 固有の部分（レジストリ、scoop、`setx`、Windows のパス）は、関数に包んで、Pester の `Mock` で差し替えて分岐を試す。差し替えない本物の動作は、人が Windows で実行する層（上の「テスト」の 2 層目）に回し、検証項目に「人が実行」と書く。
- **部屋の中では分からないこと**（報告の「実環境で未確認の点」に書く）: Windows 固有のコマンドの実際の動き、Windows のパスと権限、実行ポリシー、ネットワーク。部屋の pwsh は Linux 版（globalization は invariant）なので、文化依存の動作（日付や数値の書式）も本物と違いうる。
- 人が実行した結果を AI に戻すときは、`-Log` を付けて再実行し、ログ（`ai/work/<束ねる ps1 の名前>.log`。標準出力とエラーの全文、工程名つき）を読むよう AI に伝える。ログが `ai/` の外にあるときは、人が伏せてから `ai/in/` に置く（上の「テスト」と同じ）。`room run` のような、AI が Windows で実行する仕組みは無い。
