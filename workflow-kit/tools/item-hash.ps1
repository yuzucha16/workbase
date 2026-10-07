# decisions.md の項目の本文ハッシュを出す（review の転記の確定で、項目が転記待ちの後に変わっていないかを見る）。
# 使い方: pwsh -NoProfile -File item-hash.ps1 -Match <項目の見出しの一部> [-Path docs/decisions.md]
#         pwsh -NoProfile -File item-hash.ps1 -All [-Path ...]   （全項目を一覧）
# ハッシュ = 項目の本文（`行き先:` から行末までを除く。各行の末尾の空白と空行を除く）の SHA-256 の先頭 8 桁。
# 項目の分け方は check-docs.ps1 と同じ。読み取り専用。
param(
  [string]$Match = '',
  [switch]$All,
  [string]$Path = (Join-Path (Get-Location) 'docs/decisions.md')
)

if (-not (Test-Path -LiteralPath $Path)) { Write-Host "decisions.md が無い: $Path"; exit 1 }
if (-not $All -and -not $Match) { Write-Host '-Match か -All が要る'; exit 1 }

$raw = [IO.File]::ReadAllText((Resolve-Path -LiteralPath $Path).Path, [Text.Encoding]::UTF8).Replace("`r`n", "`n")
$lines = $raw -split "`n"

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

function Get-ItemHash([string]$text) {
  $body = ($text -split "`n" | ForEach-Object { ($_ -replace '行き先:.*$', '').TrimEnd() } | Where-Object { $_ -ne '' }) -join "`n"
  $sha = [Security.Cryptography.SHA256]::Create()
  $bytes = $sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($body))
  (($bytes | ForEach-Object { $_.ToString('x2') }) -join '').Substring(0, 8)
}

$hits = if ($All) { $items } else { @($items | Where-Object { $_.Head.Contains($Match) }) }
if ($hits.Count -eq 0) { Write-Host "一致する項目が無い: $Match"; exit 1 }
if (-not $All -and $hits.Count -gt 1) {
  Write-Host "複数の項目に一致した（$($hits.Count) 件）。-Match を絞る:"
  foreach ($h in $hits) { Write-Host "  $($h.Section):$($h.Line) $($h.Head)" }
  exit 1
}
foreach ($h in $hits) {
  $title = $h.Head -replace '^(### |- )', ''
  if ($title.Length -gt 50) { $title = $title.Substring(0, 50) + '…' }
  "{0}`t{1}:{2}`t{3}" -f (Get-ItemHash $h.Text), $h.Section, $h.Line, $title
}
