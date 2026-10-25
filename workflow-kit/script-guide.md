# スクリプトの作り方・動かし方

スクリプトや変換を作る・動かすときの、全 type 共通（`dev` `inv` とも）の規約。`dev-deliverable-guide.md` から移した（2026-10-24、ユーザーの承認。本文は原文のまま。節の見出しを `##` のまま移した）。部屋で完結させる方針、言語の選び方（Python → ps1 → bat）、Windows で実行するスクリプトの型を持つ。**スクリプトを書く・動かすときに読む**（`dev` の成果物の構成、文書、テスト、チェックは `dev-deliverable-guide.md`）。

## 実行の方針: 部屋で完結させ、Windows 依存部を小さくする

スクリプトや変換を作る・動かすときの方針（2026-10-21 のユーザーの依頼。全 type 共通）。

1. **部屋で完結できるなら、すべて部屋（WSL）で実行する。** 作って終わりにせず、部屋で実行して結果を確かめる。人に回すのは、部屋で実行できない部分だけ。
2. **Excel・COM などの Windows 依存部は、できるだけ小さくし、人の手数を少なくする。**

**言語の選び方（2026-10-21 のユーザーの依頼。AI は「Python でよいか」「ps1 がよいか」とユーザーに聞かず、この順で自分で決める）**: Windows 依存を減らすため、優先順位は **Python → ps1 → bat**。

1. **Python**（既定。2026-10-21 のユーザーの決定で、Windows 依存の薄い層も Python にした）。部屋で実行できる処理に加え、Windows 依存の操作（Excel の COM は `pywin32`、レジストリは `winreg`、アプリの起動は `subprocess`）も Python で書く。実行は `uv run --script`（Windows の実行先に Python と uv があることは確認済み）。
2. **ps1**。実行先に Python（uv）が無いと分かっているとき、または PowerShell の cmdlet でしか操作できない Windows 依存の操作のときだけ。薄い層にする。
3. **bat**。`uv run`（または ps1）を起動するだけの 3 行（下の「Windows で実行するスクリプト」）。ロジックは書かない。

上の順で決められない事情（実行先の制約が不明など）があるときだけ、ユーザーに聞く。決めたら、報告に使った言語と理由を 1 行書く。

部屋で使える道具（確認: 2026-10-21、実機の部屋 Ubuntu 26.04.1。`room init` が入れる。AI は入れ足さない）:

| 道具 | 版 | 注意 |
|---|---|---|
| Python | 3.14.4（システムの `python3`） | `pip` は無い。依存が要るときは `uv`（`uv run --script`、`uv add`）で版を固定する。外部の取得はネットワークと証明書に依存する（未確認）。テストは標準ライブラリの `unittest` |
| uv | 0.13.4 | Python の版・依存・仮想環境の管理 |
| git | 2.53.0 | 部屋のローカルの git（`room-context.md`） |
| PowerShell 7 | 7.6.7（Linux 版）+ PSScriptAnalyzer 1.25.0 + Pester 5.9.1 | 下の節の点検とテスト用。Windows 固有の動作は再現しない |
| Node.js | 24 | |
| LibreOffice / pandoc / Chromium（`room-chrome`）/ mermaid-cli（`room-mmdc`） | 26.2 / 3.7 / — / 12.0.0 | xlsx・docx・pptx の変換と再計算、Markdown の HTML 化、mermaid の画像化、HTML の PDF 化 |

切り分けの手順:

1. 処理を工程に分け、工程ごとに「部屋で実行できるか」を判定する。判定の目安は、Windows のアプリ（Excel の VBA 実行、ピボットの作成、COM）、レジストリ、Windows のパスと権限、実行先の環境（インストール、環境変数）に触れるかどうか。触れなければ部屋で完結する。
2. **Excel は、LibreOffice で足りないかを先に確かめる。** xlsx の読み書き、変換、再計算は、部屋で完結できる。Windows に回すのは、VBA の実行確認、ピボットの作成、見た目の完全な再現だけ（LibreOffice は Excel と結果が違う）。
3. 部屋で完結する工程（判定、変換、検証、整形、ファイルの生成）は、部屋で Python（または部屋の道具）で書き、**部屋で実行してテストする**。部屋の Python と同じ言語で書くので、薄い層との境目は「Windows 依存の操作を、小さな関数に包むかどうか」で決まる。
4. Windows 依存の工程だけを、**薄い層**として切り出す（成果物の中の専用ディレクトリ、例: `windows/`）。薄い層は、部屋が作った入力ファイルを読み、Windows 依存の操作だけを行い、結果をファイルに書く。判定や変換を持たない。部屋で実行できないので、検証項目に「人が実行」と書き、報告の「実環境で未確認の点」に書く。
5. **人の手数を減らす。** 人が打つのは 1 コマンドにする（下の「束ねる ps1」と起動用 bat）。実行の前提（Excel を閉じる、入力ファイルの有無、実行場所）は、束ねる側が先に確認して、満たされなければ、何をすればよいかを表示して止まる。人が覚える手順を、スクリプトの外に残さない。結果は、人が見るべき要約（成否、件数、出力の場所）を最後に表示する。

## Windows で実行するスクリプト（Python が既定、ps1 は例外。起動用 bat）

上の方針で残った、**Windows 依存の薄い層**を、人が Windows で実行するときの規約（2026-10-21 のユーザーの決定。全 type 共通。Python を既定にしたのも同日のユーザーの決定）。bat は、束ねる役を 1 回で実行したいという人の手間を省くための入口にすぎず、bat 自体に価値は無い。bat の失敗（日本語の文字化け、LF でラベルが見つからない、`call` 忘れ）は、bat にロジックを書くから起きる。

### Python の薄い層（既定）

- **個別の処理は `<名前>.py`（snake_case）、それらを順に呼ぶ束ねる役を 1 本（例: `run_all.py`）にする。** 失敗したら止まる、最後に結果を出す、ログを 1 か所に出す、を束ねる側に持たせる。人は `uv run --script run_all.py` を 1 回打つだけにする。判定・変換・検証は薄い層に置かない（上の「切り分けの手順」の 4）。
- **依存は、各 `.py` の先頭の `# /// script`（PEP 723）に書く**（`requires-python`、`dependencies`。Excel の COM なら `pywin32`）。実行は `uv run --script`。束ねる役が個別の処理を呼ぶときも `uv run --script` で呼ぶ（自分の Python には、呼び先の依存が無い）。
- **bat は、起動用の 3 行だけ許す**。ロジックは書かない。型は固定（`%*` は引数を渡したいときだけ。全体 ASCII、CRLF、BOM なし、`pause` を最後に必ず置く）:

  ```bat
  @echo off
  uv run --script "%~dp0run_all.py" %*
  pause
  ```
- **束ねる役に、ログ出力の機能を持たせる。ただし既定では出さない**（ps1 と同じ決定。理由と実データの注意は、下の ps1 の節）。`--log` を付けると、Project の `ai/work/<束ねる役の名前>.log` の 1 本に出す。`--log-dir <パス>` なら、その場所に出す。個別の処理は、ログを作らない。型（動作確認済み: Windows の Python 3.13 と uv 0.13.0。既定ではログが出ない、`--log` で `ai/work/` に出る、失敗した工程・終了コード・スタックがログに残り終了コードが 1 になる。bat 経由の `--log` も同じ）:

  ```python
  # /// script
  # requires-python = ">=3.12"
  # dependencies = []
  # ///
  """工程を順に実行する束ねる役。失敗したら止まり、最後に結果を出す。--log のときだけログを出す。"""
  import argparse
  import os
  import subprocess
  import sys
  import traceback
  from pathlib import Path

  STEPS = ["step1.py", "step2.py"]  # 実際の工程名に変える
  HERE = Path(__file__).resolve().parent


  def find_ai_work() -> Path:
      for d in (HERE, *HERE.parents):
          if d.name == "ai" and (d / "work").is_dir():
              return d / "work"
      return HERE / "work"  # Project の外（配布先）で実行したとき


  class Tee:
      def __init__(self, *streams):
          self.streams = streams

      def write(self, s):
          for st in self.streams:
              st.write(s)
          return len(s)

      def flush(self):
          for st in self.streams:
              st.flush()


  def run_steps() -> int:
      try:
          for step in STEPS:
              print(f"[STEP] {step}", flush=True)
              p = subprocess.Popen(
                  ["uv", "run", "--script", str(HERE / step)],
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                  text=True, encoding="utf-8", errors="replace",
                  env={**os.environ, "PYTHONUTF8": "1"},
              )
              for line in p.stdout:
                  print(line, end="")
              if p.wait() != 0:
                  raise RuntimeError(f"{step} が終了コード {p.returncode} で終わった")
          print("[OK] すべて完了")
          return 0
      except Exception as e:  # ログに残すため、ここで書く
          print(f"[ERROR] {e}")
          traceback.print_exc(file=sys.stdout)
          return 1


  def main() -> int:
      ap = argparse.ArgumentParser()
      ap.add_argument("--log", action="store_true", help="ai/work/<名前>.log に出す")
      ap.add_argument("--log-dir", type=Path, help="この場所にログを出す（--log は不要）")
      a = ap.parse_args()
      sys.stdout.reconfigure(errors="replace")
      if not (a.log or a.log_dir):  # 既定ではログを出さない
          return run_steps()
      log_path = (a.log_dir or find_ai_work()) / f"{Path(__file__).stem}.log"
      log_path.parent.mkdir(parents=True, exist_ok=True)
      with open(log_path, "w", encoding="utf-8") as f:  # 実行のたびに上書きする
          real = sys.stdout
          sys.stdout = Tee(real, f)
          try:
              print(f"[LOG] {log_path}")
              return run_steps()
          finally:
              sys.stdout = real


  if __name__ == "__main__":
      sys.exit(main())
  ```

  Python 版のログには、ps1 の transcript のようなヘッダー（ユーザー名とマシン名）は入らない。ただし、パス（ユーザー名を含みうる）とエラー文は入るので、`ai/` の中に出るログが部屋の AI から読める点は同じ（実データの扱いは ps1 の節）。
- **Windows 固有の操作（COM、レジストリ）は、小さな関数に包む。** `pywin32` は Windows 専用で、部屋では import できない。関数の中で import するか、`sys.platform` で分け、部屋のテストでは `unittest.mock.patch` で関数ごと差し替える。差し替えない本物の動作は、人が Windows で実行する層に回し、検証項目に「人が実行」と書く。
- **部屋の中で、作った直後に静的チェッカーを実行する**（標準ライブラリだけ。実行はしない）:

  ```
  python3 ~/shared/workflow-kit/tools/check_py.py <成果物のディレクトリ>
  python3 ~/shared/workflow-kit/tools/check_py.py --run-tests <成果物のディレクトリ>   # test*.py を unittest で実行する
  ```

  FAIL は直してから人に渡す。WARN は理由を見て判断する。終了コードは FAIL の数。見るもの: UTF-8、改行の混在、構文、起動用 bat の型（上の 3 行、呼び先の存在）、束ねる役のログ機能、ruff（入っていれば。`room init` は入れないので、通常は WARN。未定義の名前の誤りは、部屋のテストで補う）。
- **部屋の中では分からないこと**（報告の「実環境で未確認の点」に書く）: Windows 固有の動作（COM、レジストリ、パス、権限）、実行先の `uv` による依存の取得（ネットワークと証明書。型の確認では依存が空だった）。結果を AI に戻すときは、`--log` を付けて再実行し、ログを読むよう AI に伝える（ps1 と同じ）。

### 人が叩くスクリプトの名前: `run` / `verify` / `release`（2026-10-24 の仮決め）

人が Windows で叩くスクリプトは、**工程で名前を固定する**。`.py`（束ねる役）と、起動用の `.bat`（上の 3 行）を、同じ名前で成果物の `tools/` に置く。AI への合図も同じ語（「verify して」「release OK」）。必要な工程だけ作る。

| 工程 | 名前 | 役目 |
|---|---|---|
| 本番実行 | `run.py` / `run.bat` | 実データに対して使う（繰り返し使うツールだけ）。ログは `ai/` の外（`_noai/`） |
| 動作確認 | `verify.py` / `verify.bat` | Windows でしか動かない層の実行、実アプリでの単体テスト、目視の確認 |
| リリース | `release.py` / `release.bat` | 動作確認の済んだ成果物に版を振り、記録する（束ね先は未決） |

`finalize` は使わない（release と意味が紛れる）。`verify` の「束ねる役」は、上の型（`run_all.py`）の名前を `verify.py` に変えたもの。

**`verify` の手順**（1 回叩けば済むようにする）:

1. プリフライト: 前提（uv、Excel を閉じる、入力の有無）を確かめ、満たさなければ何をすればよいかを出して止まる。
2. 工程を順に実行する。
3. 目視の項目を 1 つずつ y/n（とひとこと）で聞く。
4. `ai/work/verify-result.json` を**毎回**上書きで出す（環境の事実、工程ごとの結果、失敗の型と場所、目視の回答、`ai/out/<成果物名>/` のハッシュ）。業務の値・ユーザー名は入れない。全文ログは今まで通り `--log` のとき。
5. 人が AI に返すのは「verify 済み」の一言。AI は結果ファイルを読む。

**`release` の手順**（2026-10-24 に見直し中。`artifacts/` に束ねる案は取り下げ。置き場は未決）:

1. `verify-result.json` が全部 OK で、そのハッシュが今の成果物と一致しなければ、止まる（古い版を出さない）。
2. 版を振り、日付と `verify-result.json` を添えて、README の状況表に記録する。束ねる先（Project の成果物の置き場）は未決。

Project の成果物は、`ai/out/`（マスクした Project は復元後の `_noai/final/`）の1本（ユーザー、2026-10-25。人の成果物を別の置き場から混ぜる案は取り下げ）。人が `ai/out/` を直接直すのは、マスクに関係しない箇所だけ。`release` の入力はこの成果物で、束ね先は未決。

未実装（2026-10-24）: 上の手順の型と、`check_py.py` での点検（名前、`verify-result.json` を出す機能）は、まだ書いていない。

### ps1 の薄い層（Python が使えないときだけ）

下の規約は、実行先に Python（uv）が無いと分かっているとき、または PowerShell の cmdlet でしか操作できないときの、ps1 の薄い層に適用する。

- **Windows 側の処理は ps1 に書く（Windows 依存の操作だけ。判定・変換・検証は部屋側）。束ねる役も ps1 にする**: 個別の処理を `<名前>.ps1` に分け、それらを順に呼ぶ 1 本（例: `run-all.ps1`）を置く。失敗したら止まる、ログを 1 か所に出す、最後に結果の一覧を出す、を束ねる側に持たせる。人は `pwsh -File run-all.ps1` を 1 回打つだけにする。
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
