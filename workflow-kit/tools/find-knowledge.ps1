#Requires -Version 7
<#
.SYNOPSIS
  「ナレッジ化して」の手順「既存の知識と重なるか確認する」の検索を行う。
  exmem/knowledge/ のファイル名、見出し（^#）、frontmatter の tags と aliases の行を、キーワードで検索し、
  ヒットしたキーワードの種類が多い順に、ファイルを最大3件まで示す。

.PARAMETER Keyword
  検索キーワード。空白で並べる（-Keyword は付けない）。日本語と英語の両方を含める。大文字小文字は区別しない。

.PARAMETER Body
  本文の行も検索する（既定は、ファイル名・見出し・tags・aliases・title だけ）。見出しに無い語（コマンド名、エラー文言、変数名）で探すときに使う。
  ヒットしたキーワードの種類が同じなら、ヒットした行の数が多いファイルを上位にする。

.PARAMETER Top
  示すファイルの最大数。既定は3（手順「既存の知識と重なるか確認する」の3は最大2件を選ぶ。選ぶのはエージェント）。

.EXAMPLE
  pwsh -NoProfile -File tools/find-knowledge.ps1 git 改行 gitattributes autocrlf

.NOTES
  読み取り専用。knowledge/ は編集しない。リテラル一致（正規表現ではない）。PowerShell 7 以降。
#>
[CmdletBinding(PositionalBinding = $false)]
param(
  [Parameter(ValueFromRemainingArguments = $true)] [string[]]$Keyword,
  [int]$Top = 3,
  [switch]$Body
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
  $bodyEv = [System.Collections.Generic.List[string]]::new()
  $hits = 0
  $inFront = $false
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($i -eq 0 -and $l -eq '---') { $inFront = $true; continue }
    if ($inFront -and $l -eq '---') { $inFront = $false; continue }
    # 対象: frontmatter 内の tags / aliases とその項目（- …）、本文の見出し
    $target = $false
    if ($inFront) { $target = ($l -match '^(tags|aliases):' ) -or ($l -match '^\s+-\s' ) -or ($l -match '^(title):') }
    elseif ($l -match '^#') { $target = $true }
    $isBody = $false
    if (-not $target -and $Body -and -not $inFront) { $target = $true; $isBody = $true }
    if (-not $target) { continue }
    $lineHit = $false
    foreach ($k in $Keyword) {
      if ($l.IndexOf($k, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
        [void]$hitKw.Add($k)
        $lineHit = $true
        if (-not $isBody) {
          $ev = "L$($i + 1): $($l.Trim())"
          if ($evidence.Count -lt 3 -and -not $evidence.Contains($ev)) { $evidence.Add($ev) }
        }
      }
    }
    if ($lineHit) {
      $hits++
      if ($isBody -and $bodyEv.Count -lt 2) { $t = $l.Trim(); if ($t.Length -gt 110) { $t = $t.Substring(0, 110) + '…' }; $bodyEv.Add("L$($i + 1): $t") }
    }
  }
  foreach ($k in $Keyword) {   # ファイル名
    if ($f.BaseName.IndexOf($k, [StringComparison]::OrdinalIgnoreCase) -ge 0) { [void]$hitKw.Add($k); $evidence.Add("ファイル名: $($f.Name)") }
  }
  if ($hitKw.Count -gt 0) {
    foreach ($b in $bodyEv) { $evidence.Add("本文 $b") }
    [pscustomobject]@{ File = $f.FullName.Substring($dir.Length + 1).Replace('\', '/'); Kinds = $hitKw.Count; Hits = $hits; Keywords = ($hitKw -join ', '); Evidence = $evidence }
  }
}

if (-not $results) { Write-Host "ヒット無し（キーワード: $($Keyword -join ', ')）。統合先の候補は「新規トピック」"; exit 0 }
$order = if ($Body) { @(@{ Expression = 'Kinds'; Descending = $true }, @{ Expression = 'Hits'; Descending = $true }, 'File') } else { @(@{ Expression = 'Kinds'; Descending = $true }, 'File') }   # 既定の並びは変えない
foreach ($r in $results | Sort-Object -Property $order | Select-Object -First $Top) {
  Write-Host "knowledge/$($r.File)  [$($r.Kinds)/$($Keyword.Count) 語: $($r.Keywords)]"
  foreach ($e in $r.Evidence) { Write-Host "    $e" }
}
