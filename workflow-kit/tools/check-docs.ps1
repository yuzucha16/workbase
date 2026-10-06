#Requires -Version 7
<#
.SYNOPSIS
  docs/decisions.md の各項目に、ラベル（【汎用】【この件】）と「行き先」があるかを、機械的に点検する。
  どこにも行き先が決まっていないデータ（滞留）を見つけるための棚卸し。docs-rules.md の「decisions.md の項目の行き先」の機械的な点検。

.PARAMETER Path
  点検する decisions.md。省略すると、カレントディレクトリの docs/decisions.md。

.PARAMETER MaxPending
  「転記待ち」の上限。超えると FAIL（既定 20。人が目視と手入力で運ぶ量の上限）。

.EXAMPLE
  pwsh -NoProfile -File <kit>/tools/check-docs.ps1                       # カレントディレクトリの docs/decisions.md を点検する
  pwsh -NoProfile -File <kit>/tools/check-docs.ps1 -Path <作業ディレクトリ>/docs/decisions.md -MaxPending 10

.NOTES
  項目 = Principles / Facts / Gotchas の最上位の箇条書き（行頭が `- `。中身が空の `-` は数えない）と、Decisions の `###` 節。
  行き先の書式: `行き先: <状態>` または `行き先: <状態>（詳細）`。
    状態: 未仕分け / 転記待ち / 転記済 / local / 滞留 / 破棄
    転記済は `（YYYY-MM-DD → <先>）`、local・滞留・破棄は `（<理由>）` が要る。
  終了コード = FAIL の数。WARN は数えない。PowerShell 7 以降（UTF-8 のファイルを読むため）。
#>
[CmdletBinding(PositionalBinding = $false)]
param(
  [string]$Path = (Join-Path (Get-Location) 'docs/decisions.md'),
  [int]$MaxPending = 20
)

if (-not (Test-Path -LiteralPath $Path)) { Write-Host "decisions.md が無い: $Path"; exit 1 }

$script:fail = 0; $script:warn = 0; $script:pass = 0
function Report([bool]$ok, [string]$name, [string]$level = 'FAIL', [string]$detail = '') {
  if ($ok) { $script:pass++; return }
  if ($level -eq 'WARN') { $script:warn++ } else { $script:fail++ }
  $d = if ($detail) { " ($detail)" } else { '' }
  Write-Host "  ${level}: $name$d"
}

$states = '未仕分け', '転記待ち', '転記済', 'local', '滞留', '破棄'
$raw = [IO.File]::ReadAllText((Resolve-Path -LiteralPath $Path).Path, [Text.Encoding]::UTF8).Replace("`r`n", "`n")
$lines = $raw -split "`n"

# 項目に分ける。Decisions は `###` が項目の頭、それ以外の節は行頭の `- ` が項目の頭。
$items = [System.Collections.Generic.List[object]]::new()
$section = ''; $cur = $null
for ($i = 0; $i -lt $lines.Count; $i++) {
  $l = $lines[$i]
  if ($l -match '^## (.+)$') { $section = $Matches[1].Trim(); $cur = $null; continue }
  if ($section -notin 'Principles', 'Decisions', 'Facts', 'Gotchas') { continue }
  $isHead = if ($section -eq 'Decisions') { $l -match '^### ' } else { $l -match '^- \S' }
  if ($isHead) {
    $cur = [pscustomobject]@{ Section = $section; Line = $i + 1; Head = $l; Text = $l }
    $items.Add($cur)
  } elseif ($cur) {
    $cur.Text += "`n$l"
  }
}

$count = @{}; foreach ($s in $states) { $count[$s] = 0 }
$count['行き先なし'] = 0
$stuck = [System.Collections.Generic.List[string]]::new()
$unsorted = [System.Collections.Generic.List[string]]::new()

foreach ($it in $items) {
  $title = $it.Head -replace '^(### |- )', ''
  if ($title.Length -gt 40) { $title = $title.Substring(0, 40) + '…' }
  $id = "$($it.Section):$($it.Line) $title"

  Report ($it.Text -match '【汎用】|【この件】') "ラベル（【汎用】か【この件】）がある [$id]" 'WARN'

  $m = [regex]::Match($it.Text, '行き先:\s*(未仕分け|転記待ち|転記済|local|滞留|破棄)(（([^）]*)）)?')
  if (-not $m.Success) {
    if ($it.Text -match '行き先:') { Report $false "行き先の状態が、定められた6つのどれでもない [$id]" } else { Report $false "行き先がない [$id]" }
    $count['行き先なし']++; continue
  }
  $state = $m.Groups[1].Value; $detail = $m.Groups[3].Value.Trim()
  $count[$state]++
  switch ($state) {
    '転記済' { Report ($detail -match '^\d{4}-\d{2}-\d{2}\s*→\s*\S') "転記済に（YYYY-MM-DD → 先）がある [$id]" }
    { $_ -in 'local', '滞留', '破棄' } { Report ($detail.Length -gt 0) "$state に（理由）がある [$id]" }
  }
  if ($state -eq '未仕分け') { $unsorted.Add($id) }
  if ($state -eq '滞留') { $stuck.Add($id) }
}

Report ($count['転記待ち'] -le $MaxPending) "転記待ちが上限以内（$($count['転記待ち']) 件 / 上限 $MaxPending）"
Report ($count['未仕分け'] -eq 0) "未仕分けが無い（$($count['未仕分け']) 件）" 'WARN'

Write-Host "== $(Split-Path -Leaf (Split-Path -Parent $Path))/$(Split-Path -Leaf $Path): 項目 $($items.Count) 件"
Write-Host ("  内訳: " + (($states + '行き先なし' | ForEach-Object { "$_ $($count[$_])" }) -join ' / '))
if ($stuck.Count) {
  Write-Host '  滞留（再試行の問い: 固有情報を剥がすと、何が言えるか）:'
  $stuck | ForEach-Object { Write-Host "    - $_" }
}
Write-Host "  結果: FAIL $script:fail / WARN $script:warn / 点検 PASS $script:pass"
exit $script:fail
