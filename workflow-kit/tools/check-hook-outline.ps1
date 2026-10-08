#Requires -Version 7
<#
.SYNOPSIS
  *-hook.md の章立ての共通部を点検する。共通の5章が、すべてのフックにあり、この順に並んでいることを見る。

.DESCRIPTION
  共通部: 目的と契機 → 場所と書き込みの制約 → 手順 → 報告の型（H2）。
  固有の章は、報告の型より後ろに置く（例外: 導入項目の一覧、入力）。「このフックの改善」は任意で、固有の確認項目があるフックだけが持つ（持つなら hook-common.md を指す）。
  あわせて共通部の中身（hook-common.md）を見る: 冒頭の hooks.md、報告の型の改善案、改善の章の hook-common.md への参照。
  これ以外の章（実測、未決、各フック固有の仕様など）は固有部で、点検しない。
  新しいフックを足すときも、この5章を同じ名前・順序で置く。
  手順の参照は、番号でなく手順の見出しの名前で書く（番号参照が無いこと、名前の実在を見る）。
  あわせて、hooks.md と README.md の表の行に、全フックが載っていること、
  表にあるフック名のファイルが存在すること（削除・改名の漏れ）を見る。

.EXAMPLE
  pwsh -NoProfile -File tools/check-hook-outline.ps1

.NOTES
  終了コード = FAIL のフックの数。PowerShell 7 以降（UTF-8 のファイルを読むため）。
#>
[CmdletBinding()]
param()

$common = '目的と契機', '場所と書き込みの制約', '手順', '報告の型'
# 任意の共通章（固有の確認項目があるフックだけが持つ。持つなら hook-common.md を指す）
$optional = 'このフックの改善'
# 共通部より前に置いてよい固有の章（init の表は目次を兼ねる。入力は手順の入力）
$beforeOk = '導入項目の一覧', '入力'
$kitRoot = Split-Path -Parent $PSScriptRoot
$fail = 0
$common_text = Get-Content -LiteralPath (Join-Path $kitRoot 'hook-common.md') -Raw -Encoding utf8

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
  $last = [array]::IndexOf($h2, ($h2 | Where-Object { $_ -eq '報告の型' -or $_.StartsWith('報告の型（') } | Select-Object -First 1))
  $early = @(for ($i = 0; $i -lt $last; $i++) { if (-not ($common | Where-Object { $h2[$i] -eq $_ -or $h2[$i].StartsWith("$_（") }) -and $h2[$i] -notin $beforeOk) { $h2[$i] } })
  if ($early) { $content += "固有の章が共通部の途中にある: $($early -join '、')" }
  # 手順の参照は番号でなく見出し（太字）の名前で書く。番号参照が無く、名前が同じファイルの手順に実在すること
  if ($raw -match '手順 ?[0-9０-９]|手順の ?[0-9０-９]|」の [0-9０-９] ') { $content += '手順を番号で参照している（手順「名前」で書く）' }
  $titles = @([regex]::Matches($raw, '(?m)^\s*[0-9]+\. \*\*(.+?)\*\*') | ForEach-Object { $_.Groups[1].Value.TrimEnd('。', ':', '：') })
  $refs = @([regex]::Matches($raw, '手順「([^」]+)」|「手順」の「([^」]+)」') | ForEach-Object { if ($_.Groups[1].Success) { $_.Groups[1].Value } else { $_.Groups[2].Value } })
  $dead = @($refs | Where-Object { $r = $_; -not ($titles | Where-Object { $_.StartsWith($r) }) } | Sort-Object -Unique)
  if ($dead) { $content += "手順の参照先が無い: $($dead -join '、')" }
  if (-not $head.Contains('`hooks.md`')) { $content += '冒頭に正本 hooks.md の記載が無い' }
  if (-not $body['報告の型'].Contains('改善案')) { $content += '報告の型に「改善案」が無い' }
  $imp = [regex]::Match($raw, '(?ms)^## このフックの改善[^\r\n]*\r?\n(.*?)(?=^## |\z)')
  if ($imp.Success -and -not $imp.Groups[1].Value.Contains('hook-common.md')) { $content += '改善の章が hook-common.md を指していない' }
  if ($common_text -notmatch ('(?m)^\| `' + $f.BaseName.Replace('-hook','') + '` \|')) { $content += 'hook-common.md の記録の表に行が無い' }
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
