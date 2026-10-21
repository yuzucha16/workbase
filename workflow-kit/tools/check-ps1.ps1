#Requires -Version 7
<#
.SYNOPSIS
  Windows で実行するスクリプト（.ps1 と、それを呼ぶ起動用 .bat）を、実行せずに点検する。
  dev-deliverable-guide.md の「Windows で実行するスクリプト」の規約のうち、機械的に確認できる項目を見る。
  AI 作業部屋（Linux の pwsh 7）でも、Windows の pwsh 7 でも同じ結果になる。

.PARAMETER Path
  点検するファイルまたはディレクトリ（ディレクトリは、中の .ps1 .psm1 .psd1 .bat .cmd を再帰で集める）。
  複数のときは、パスを空白で並べる（-Path は付けない）か、-Path a,b（カンマ区切り）にする。

.PARAMETER RunTests
  点検に加えて、見つけた *.Tests.ps1 を Pester 5 で実行する（モジュールが無ければ WARN）。

.PARAMETER ShowPass
  PASS の行も出す。既定は FAIL と WARN の行と、最後の RESULT の行だけ（読む量を絞るため）。

.EXAMPLE
  pwsh -NoProfile -File check-ps1.ps1 ai/out/setup-tool
  pwsh -NoProfile -File check-ps1.ps1 -RunTests ai/out/setup-tool

.NOTES
  終了コード = FAIL の数。WARN は数えない。
  見る項目: 文字コードが UTF-8、改行が混在していない、構文（Parser）、#Requires -Version 7、
  $ErrorActionPreference と Set-StrictMode、PSScriptAnalyzer（Error は FAIL、Warning は WARN）、
  起動用 .bat が 3 行の型（@echo off / pwsh -NoProfile -File "%~dp0<名前>.ps1" / pause）で、ASCII・CRLF・BOM なし、呼び先の .ps1 が同じ場所にある。
  見ないもの（人が Windows で実行して確かめる）: Windows 固有のコマンド（レジストリ、scoop、setx）、Windows のパス、PowerShell 5.1 との差。
#>
[CmdletBinding(PositionalBinding = $false)]
param(
  [Parameter(ValueFromRemainingArguments = $true)] [string[]]$Path,
  [switch]$RunTests,
  [switch]$ShowPass
)

$Path = @($Path | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
if (-not $Path) { Write-Host '点検する Path が無い（ファイルかディレクトリを指定する）'; exit 1 }

$script:fail = 0; $script:warn = 0; $script:pass = 0
function Report([bool]$ok, [string]$name, [string]$level = 'FAIL', [string]$detail = '') {
  if ($ok) { $script:pass++; if ($ShowPass) { Write-Host "  PASS: $name" }; return }
  if ($level -eq 'WARN') { $script:warn++ } else { $script:fail++ }
  $d = if ($detail) { " ($detail)" } else { '' }
  Write-Host "  ${level}: $name$d"
}

# PSScriptAnalyzer の対象外にする規則。pwsh 7 を前提にするので BOM の規則は外す。画面に出す前提の道具なので Write-Host も許す
$analyzerExclude = 'PSAvoidUsingWriteHost', 'PSUseBOMForUnicodeEncodedFile', 'PSUseShouldProcessForStateChangingFunctions', 'PSUseSingularNouns'
$extensions = '.ps1', '.psm1', '.psd1', '.bat', '.cmd'
$skipDirs = '[\\/](\.git|node_modules|\.venv)[\\/]'

$files = [System.Collections.Generic.List[IO.FileInfo]]::new()
foreach ($p in $Path) {
  if (-not (Test-Path -LiteralPath $p)) { Write-Host "  FAIL: パスが無い ($p)"; $script:fail++; continue }
  $item = Get-Item -LiteralPath $p
  if ($item.PSIsContainer) {
    Get-ChildItem -LiteralPath $item.FullName -Recurse -File |
      Where-Object { $extensions -contains $_.Extension.ToLowerInvariant() -and $_.FullName -notmatch $skipDirs } |
      ForEach-Object { $files.Add($_) }
  } else { $files.Add($item) }
}
if ($files.Count -eq 0 -and $script:fail -eq 0) { Write-Host '点検するファイルが無い（.ps1 .psm1 .psd1 .bat .cmd）'; exit 0 }

$analyzer = Get-Module -ListAvailable PSScriptAnalyzer | Sort-Object Version -Descending | Select-Object -First 1
if ($analyzer) { Import-Module $analyzer -ErrorAction SilentlyContinue }
$analyzerWarned = $false
$strictUtf8 = [Text.UTF8Encoding]::new($false, $true)

function Test-Launcher([IO.FileInfo]$file) {
  $bytes = [IO.File]::ReadAllBytes($file.FullName)
  Report (-not ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)) '起動用 bat に BOM が無い'
  Report (-not ($bytes | Where-Object { $_ -gt 127 } | Select-Object -First 1)) '起動用 bat 全体が ASCII（日本語のコメントや表示は書かない）'
  $text = [Text.Encoding]::ASCII.GetString($bytes)
  Report ($text -notmatch "(?<!\r)\n") '起動用 bat の改行が CRLF（LF だけの行がある）'
  $lines = @($text -split "\r?\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
  $target = $null; $shape = $true
  foreach ($l in $lines) {
    if ($l -imatch '^@echo off$' -or $l -imatch '^pause$') { continue }
    $m = [regex]::Match($l, '^pwsh -NoProfile -File "%~dp0(?<n>[^"\\/%]+\.ps1)"( %\*)?$', 'IgnoreCase')
    if ($m.Success -and -not $target) { $target = $m.Groups['n'].Value; continue }
    $shape = $false
  }
  Report ($shape -and $target) '起動用 bat が 3 行の型だけ（@echo off / pwsh -NoProfile -File "%~dp0<名前>.ps1" / pause）。ロジックは ps1 に書く'
  if ($target) {
    $targetPath = Join-Path $file.DirectoryName $target
    $exists = Test-Path -LiteralPath $targetPath
    Report $exists "起動用 bat の呼び先 $target が同じ場所にある"
    if ($exists) {  # 束ねる ps1 は、-Log のときだけ ai/work/<名前>.log の 1 本にログを出す機能を持つ（既定は出さない。型は dev-deliverable-guide.md）
      $body = [IO.File]::ReadAllText($targetPath)
      Report ($body -match 'Start-Transcript' -and $body -match 'Stop-Transcript' -and $body -match "'work'" -and $body -match '\[switch\]\$Log\b') "束ねる $target が -Log のときのログ出力の機能を持つ（[switch]`$Log、Start-Transcript と Stop-Transcript、'work'）" 'WARN'
    }
  }
  $last = if ($lines.Count) { $lines[-1] } else { '' }
  Report ($last -imatch '^pause$') '起動用 bat の最後が pause（終わっても画面が閉じない）'
}

function Test-PowerShellFile([IO.FileInfo]$file) {
  $bytes = [IO.File]::ReadAllBytes($file.FullName)
  $text = $null
  try { $text = $strictUtf8.GetString($bytes) } catch { }
  Report ($null -ne $text) '文字コードが UTF-8' 'FAIL' 'cp932 や UTF-16 の可能性。UTF-8 で保存し直す'
  if ($null -eq $text) { return }
  $crlf = [regex]::Matches($text, "\r\n").Count
  $lf = [regex]::Matches($text, "(?<!\r)\n").Count
  Report (-not ($crlf -gt 0 -and $lf -gt 0)) '改行が混在していない' 'WARN' "CRLF $crlf 行、LF $lf 行"

  $tokens = $null; $errs = $null
  $ast = [Management.Automation.Language.Parser]::ParseFile($file.FullName, [ref]$tokens, [ref]$errs)
  foreach ($e in $errs) { Report $false '構文エラー' 'FAIL' "行 $($e.Extent.StartLineNumber): $($e.Message)" }
  Report ($errs.Count -eq 0) '構文が通る'
  if ($errs.Count -gt 0) { return }

  if ($file.Extension -ieq '.ps1' -and $file.Name -notlike '*.Tests.ps1') {
    $req = $ast.ScriptRequirements
    Report ($req -and $req.RequiredPSVersion -and $req.RequiredPSVersion.Major -ge 7) '#Requires -Version 7 がある（5.1 で動かしたときに、文字化けでなく明示のエラーで止める）' 'WARN'
    $eap = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.AssignmentStatementAst] -and $n.Left.Extent.Text -match 'ErrorActionPreference' }, $true)
    Report ($eap.Count -gt 0) '$ErrorActionPreference を宣言している（失敗で止める。通常は Stop）' 'WARN'
    $strict = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.GetCommandName() -eq 'Set-StrictMode' }, $true)
    Report ($strict.Count -gt 0) 'Set-StrictMode を使っている（未定義の変数の誤りを検出する）' 'WARN'
  }

  if ($analyzer) {
    $found = @(Invoke-ScriptAnalyzer -Path $file.FullName -Severity Error, Warning -ExcludeRule $analyzerExclude)
    foreach ($f in $found) {
      $lvl = if ($f.Severity -eq 'Error') { 'FAIL' } else { 'WARN' }
      Report $false "PSScriptAnalyzer $($f.RuleName)" $lvl "行 $($f.Line): $($f.Message)"
    }
    if ($found.Count -eq 0) { Report $true 'PSScriptAnalyzer の指摘が無い' }  # 指摘は上で 1 件ずつ数えた（まとめの行で二重に数えない）
  } elseif (-not $script:analyzerWarned) {
    $script:analyzerWarned = $true
    Report $false 'PSScriptAnalyzer が無い（部屋の init で入る）。静的解析を省いた' 'WARN'
  }
}

$here = (Get-Location).Path
foreach ($f in $files) {
  $rel = if ($f.FullName.StartsWith($here)) { $f.FullName.Substring($here.Length).TrimStart('\', '/') } else { $f.FullName }
  Write-Host "== $rel"
  if ($f.Extension -ieq '.bat' -or $f.Extension -ieq '.cmd') { Test-Launcher $f } else { Test-PowerShellFile $f }
}

if ($RunTests) {
  $tests = @($files | Where-Object { $_.Name -like '*.Tests.ps1' } | ForEach-Object FullName)
  $pester = Get-Module -ListAvailable Pester | Where-Object { $_.Version.Major -ge 5 } | Sort-Object Version -Descending | Select-Object -First 1
  if (-not $tests) {
    Write-Host '== Pester'; Report $false '*.Tests.ps1 が見つからない' 'WARN'
  } elseif (-not $pester) {
    Write-Host '== Pester'; Report $false 'Pester 5 が無い（部屋の init で入る）。テストを実行していない' 'WARN'
  } else {
    Write-Host '== Pester'
    Import-Module $pester
    $cfg = New-PesterConfiguration
    $cfg.Run.Path = $tests
    $cfg.Run.PassThru = $true
    $cfg.Output.Verbosity = 'Minimal'
    $res = Invoke-Pester -Configuration $cfg
    Report ($res.FailedCount -eq 0 -and $res.TotalCount -gt 0) 'Pester のテストが全件合格' 'FAIL' "合格 $($res.PassedCount) / 失敗 $($res.FailedCount) / 全 $($res.TotalCount)"
  }
}

Write-Host "RESULT: files=$($files.Count) pass=$($script:pass) fail=$($script:fail) warn=$($script:warn)"
exit $script:fail
