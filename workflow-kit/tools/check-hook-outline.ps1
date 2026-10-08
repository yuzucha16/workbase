#Requires -Version 7
<#
.SYNOPSIS
  *-hook.md の章立ての共通部を点検する。共通の4章が、すべてのフックにあり、この順に並んでいることを見る。

.DESCRIPTION
  共通部: 場所と書き込みの制約 → 手順 → 報告の型 → このフックの改善（H2）。
  これ以外の章（実測、未決、各フック固有の仕様など）は固有部で、点検しない。
  新しいフックを足すときも、この4章を同じ名前・順序で置く。

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
  if ($missing -or $dup -or -not $ordered) {
    $fail++
    $msg = @()
    if ($missing) { $msg += "欠け: $($missing -join '、')" }
    if ($dup) { $msg += "重複: $($dup -join '、')" }
    if (-not $ordered) { $msg += "順序: $($found -join ' → ')" }
    Write-Output "FAIL  $($f.Name)  $($msg -join ' / ')"
  } else {
    Write-Output "OK    $($f.Name)"
  }
}
exit $fail
