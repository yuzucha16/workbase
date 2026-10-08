#Requires -Version 7
<#
.SYNOPSIS
  *-hook.md の章立ての共通部を点検する。共通の4章が、すべてのフックにあり、この順に並んでいることを見る。

.DESCRIPTION
  共通部: 場所と書き込みの制約 → 手順 → 報告の型 → このフックの改善（H2）。
  あわせて共通部の中身（hook-common.md）を見る: 冒頭の hooks.md、状態の行と hooks.md の（試験運用）の一致、報告の型の改善案、改善の章の hook-common.md への参照。
  これ以外の章（実測、未決、各フック固有の仕様など）は固有部で、点検しない。
  新しいフックを足すときも、この4章を同じ名前・順序で置く。
  あわせて、hooks.md と README.md の表の行に、全フックが載っていること、
  表にあるフック名のファイルが存在すること（削除・改名の漏れ）を見る。

.EXAMPLE
  pwsh -NoProfile -File tools/check-hook-outline.ps1

.NOTES
  終了コード = FAIL のフックの数。PowerShell 7 以降（UTF-8 のファイルを読むため）。
#>
[CmdletBinding()]
param()

$common = '場所と書き込みの制約', '手順', '報告の型', 'このフックの改善'
$kitRoot = Split-Path -Parent $PSScriptRoot
$fail = 0
$hooksRows = @(Get-Content -LiteralPath (Join-Path $kitRoot 'hooks.md') -Encoding utf8 | Where-Object { $_ -match '^\|' })

foreach ($f in Get-ChildItem -Path $kitRoot -Filter '*-hook.md' | Sort-Object Name) {
  $h2 = @(Get-Content -LiteralPath $f.FullName -Encoding utf8 |
    Where-Object { $_ -match '^## ' } |
    ForEach-Object { ($_ -replace '^## ', '').Trim() })
  # 見出しが共通名そのもの、または「手順（…）」のように括弧つきの注記が続くものを、共通の章とみなす
  $found = @(foreach ($h in $h2) {
      $hit = $common | Where-Object { $h -eq $_ -or $h.StartsWith("$_（") }
      if ($hit) { $hit }
    })
  $missing = @($common | Where-Object { $_ -notin $found })
  $dup = @($found | Group-Object | Where-Object Count -gt 1 | ForEach-Object Name)
  $ordered = ($found -join ',') -eq (($common | Where-Object { $_ -in $found }) -join ',')
  # 共通部の中身（hook-common.md）: 冒頭の定型、報告の型の改善案、改善の章の参照
  $raw = Get-Content -LiteralPath $f.FullName -Raw -Encoding utf8
  $head = ($raw -split '(?m)^## ', 2)[0]
  $body = @{}
  foreach ($c in $common) {
    $m = [regex]::Match($raw, "(?ms)^## $([regex]::Escape($c))[^\r\n]*\r?\n(.*?)(?=^## |\z)")
    $body[$c] = $m.Groups[1].Value
  }
  $content = @()
  if (-not $head.Contains('`hooks.md`')) { $content += '冒頭に正本 hooks.md の記載が無い' }
  $trial = $hooksRows -match ('`' + [regex]::Escape($f.Name) + '`（試験運用）')
  $hasState = $head.Contains('状態: **試験運用**')
  if ([bool]$trial -ne $hasState) { $content += "状態の行と hooks.md の（試験運用）が不一致（hooks.md: $([bool]$trial)、本文: $hasState）" }
  if (-not $body['報告の型'].Contains('改善案')) { $content += '報告の型に「改善案」が無い' }
  if (-not $body['このフックの改善'].Contains('hook-common.md')) { $content += '改善の章が hook-common.md を指していない' }
  if ($missing -or $dup -or -not $ordered -or $content) {
    $fail++
    $msg = @()
    if ($missing) { $msg += "欠け: $($missing -join '、')" }
    if ($dup) { $msg += "重複: $($dup -join '、')" }
    if (-not $ordered) { $msg += "順序: $($found -join ' → ')" }
    if ($content) { $msg += $content }
    Write-Output "FAIL  $($f.Name)  $($msg -join ' / ')"
  } else {
    Write-Output "OK    $($f.Name)"
  }
}
# 参照の点検: フックの追加・削除で、表の更新漏れを見つける
# 正: 全フックが表にある。逆: 表の行にあるフック名のファイルが存在する（削除・改名の漏れ）
$hooks = @(Get-ChildItem -Path $kitRoot -Filter '*-hook.md' | ForEach-Object Name)
foreach ($t in 'hooks.md', 'README.md') {
  $path = Join-Path $kitRoot $t
  if (-not (Test-Path -LiteralPath $path)) { continue }
  $rows = @(Get-Content -LiteralPath $path -Encoding utf8 | Where-Object { $_ -match '^\|' })
  $text = $rows -join "`n"
  $absent = @($hooks | Where-Object { -not $text.Contains("``$_") })
  $ghost = @([regex]::Matches($text, '`([a-z]+-hook\.md)') | ForEach-Object { $_.Groups[1].Value } |
    Sort-Object -Unique | Where-Object { $_ -notin $hooks })
  if ($absent -or $ghost) {
    $fail++
    $msg = @()
    if ($absent) { $msg += "表に無い: $($absent -join '、')" }
    if ($ghost) { $msg += "存在しないフック: $($ghost -join '、')" }
    Write-Output "FAIL  $t  $($msg -join ' / ')"
  } else {
    Write-Output "OK    $t（表と全フックが一致）"
  }
}
exit $fail
