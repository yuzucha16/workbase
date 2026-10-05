#Requires -Version 7
<#
.SYNOPSIS
  「ナレッジ化して」の手順 5（既存の知識と重なるか確認する）の検索を行う。
  exmem/knowledge/ のファイル名、見出し（^#）、frontmatter の tags と aliases の行を、キーワードで検索し、
  ヒットしたキーワードの種類が多い順に、ファイルを最大3件まで示す。

.PARAMETER Keyword
  検索キーワード。空白で並べる（-Keyword は付けない）。日本語と英語の両方を含める。大文字小文字は区別しない。

.PARAMETER Top
  示すファイルの最大数。既定は3（手順 5-3 は最大2件を選ぶ。選ぶのはエージェント）。

.EXAMPLE
  pwsh -NoProfile -File tools/find-knowledge.ps1 git 改行 gitattributes autocrlf

.NOTES
  読み取り専用。knowledge/ は編集しない。リテラル一致（正規表現ではない）。PowerShell 7 以降。
#>
[CmdletBinding(PositionalBinding = $false)]
param(
  [Parameter(ValueFromRemainingArguments = $true)] [string[]]$Keyword,
  [int]$Top = 3
)

$Keyword = @($Keyword | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
if (-not $Keyword) { Write-Host 'キーワードを2〜4語、空白で並べる'; exit 1 }

$kitRoot = Split-Path -Parent $PSScriptRoot
$dir = Join-Path (Split-Path -Parent $kitRoot) 'exmem/knowledge'
if (-not (Test-Path $dir)) { Write-Host "knowledge/ が無い: $dir"; exit 1 }

$results = foreach ($f in Get-ChildItem -Path $dir -Recurse -Filter *.md -File) {
  $lines = [IO.File]::ReadAllLines($f.FullName, [Text.Encoding]::UTF8)
  $hitKw = [System.Collections.Generic.HashSet[string]]::new()
  $evidence = [System.Collections.Generic.List[string]]::new()
  $inFront = $false
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($i -eq 0 -and $l -eq '---') { $inFront = $true; continue }
    if ($inFront -and $l -eq '---') { $inFront = $false; continue }
    # 対象: frontmatter 内の tags / aliases とその項目（- …）、本文の見出し
    $target = $false
    if ($inFront) { $target = ($l -match '^(tags|aliases):' ) -or ($l -match '^\s+-\s' ) -or ($l -match '^(title):') }
    elseif ($l -match '^#') { $target = $true }
    if (-not $target) { continue }
    foreach ($k in $Keyword) {
      if ($l.IndexOf($k, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
        [void]$hitKw.Add($k)
        $ev = "L$($i + 1): $($l.Trim())"
        if ($evidence.Count -lt 3 -and -not $evidence.Contains($ev)) { $evidence.Add($ev) }
      }
    }
  }
  foreach ($k in $Keyword) {   # ファイル名
    if ($f.BaseName.IndexOf($k, [StringComparison]::OrdinalIgnoreCase) -ge 0) { [void]$hitKw.Add($k); $evidence.Add("ファイル名: $($f.Name)") }
  }
  if ($hitKw.Count -gt 0) {
    [pscustomobject]@{ File = $f.FullName.Substring($dir.Length + 1).Replace('\', '/'); Kinds = $hitKw.Count; Keywords = ($hitKw -join ', '); Evidence = $evidence }
  }
}

if (-not $results) { Write-Host "ヒット無し（キーワード: $($Keyword -join ', ')）。統合先の候補は「新規トピック」"; exit 0 }
foreach ($r in $results | Sort-Object -Property @{ Expression = 'Kinds'; Descending = $true }, File | Select-Object -First $Top) {
  Write-Host "knowledge/$($r.File)  [$($r.Kinds)/$($Keyword.Count) 語: $($r.Keywords)]"
  foreach ($e in $r.Evidence) { Write-Host "    $e" }
}
