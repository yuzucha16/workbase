#Requires -Version 7
<#
.SYNOPSIS
  「ナレッジ化して」で作った inbox のメモを、機械的に点検する。
  stock-hook.md の「自己点検」のうち、機械的に確認できる項目だけを見る（手で確認する項目は、最後に一覧する）。

.PARAMETER Path
  点検するメモ。複数のときは、パスを空白で並べる（-Path は付けない）か、-Path a,b（カンマ区切り）にする。
  省略すると、exmem/inbox/ の今日の日付のメモ（README.md を除く）を点検する。

.PARAMETER Today
  今日の日付（YYYY-MM-DD）。省略すると、実行した日。

.EXAMPLE
  pwsh -NoProfile -File tools/check-inbox.ps1 exmem/inbox/2026-10-05-a-topic.md exmem/inbox/2026-10-05-b-topic.md
  pwsh -NoProfile -File tools/check-inbox.ps1                       # 今日の日付のメモを、すべて点検する

.NOTES
  終了コード = FAIL の数。WARN は数えない。PowerShell 7 以降（UTF-8 のファイルを読むため）。
#>
[CmdletBinding(PositionalBinding = $false)]
param(
  [Parameter(ValueFromRemainingArguments = $true)] [string[]]$Path,
  [string]$Today = (Get-Date -Format 'yyyy-MM-dd')
)

$Path = @($Path | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$kitRoot = Split-Path -Parent $PSScriptRoot
if (-not $Path) {
  $inbox = Join-Path (Split-Path -Parent $kitRoot) 'exmem/inbox'
  $Path = Get-ChildItem -Path $inbox -Filter "$Today-*.md" -File -ErrorAction SilentlyContinue | ForEach-Object FullName
}
if (-not $Path) { Write-Host "点検するメモが無い（Path 未指定で、$Today のメモも無い）"; exit 0 }

$script:fail = 0; $script:warn = 0; $script:pass = 0
function Report([bool]$ok, [string]$name, [string]$level = 'FAIL', [string]$detail = '') {
  if ($ok) { $script:pass++; Write-Host "  PASS: $name"; return }
  if ($level -eq 'WARN') { $script:warn++ } else { $script:fail++ }
  $d = if ($detail) { " ($detail)" } else { '' }
  Write-Host "  ${level}: $name$d"
}
function Section([string]$text, [string]$name, [string]$next) {
  $i = $text.IndexOf("`n## $name`n"); if ($i -lt 0) { return '' }
  $body = $text.Substring($i + $name.Length + 5)
  if ($next) { $j = $body.IndexOf("`n## $next`n"); if ($j -ge 0) { $body = $body.Substring(0, $j) } }
  return $body.Trim()
}
function Count([string]$text, [string]$pattern) { return ([regex]::Matches($text, $pattern)).Count }

$order = 'Goal', 'Principles', 'Decisions', 'Facts', 'Gotchas', 'Open Questions', 'Next Actions'
$script:spans = @{}   # インラインコード（8文字以上）→ それを Facts / Gotchas に含むメモ。メモをまたぐ重複の候補を見つける

foreach ($p in $Path) {
  $file = Get-Item -LiteralPath $p
  Write-Host "== $($file.Name)"
  $raw = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8).Replace("`r`n", "`n")

  Report ($file.Name -match '^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+){1,4}\.md$') 'ファイル名が YYYY-MM-DD-<英単語2〜5語の kebab-case>.md' 'FAIL' $file.Name

  # frontmatter
  $fm = [regex]::Match($raw, '(?s)^---\n(.*?)\n---\n')
  Report $fm.Success 'frontmatter がある'
  $front = $fm.Groups[1].Value
  $get = { param($k) ([regex]::Match($front, "(?m)^${k}:\s*(.*)$")).Groups[1].Value.Trim() }
  Report ((& $get 'type') -eq 'inbox') 'type が inbox'
  Report ((& $get 'title') -ne '') 'title がある'
  $created = & $get 'created'
  Report ($created -match '^\d{4}-\d{2}-\d{2}$') 'created が YYYY-MM-DD'
  Report ($created -eq $Today) "created が今日（$Today）" 'WARN' $created
  $tagBlock = [regex]::Match($front, '(?s)tags:\n(.*?)(?=\n\S|\z)').Groups[1].Value
  $tags = [regex]::Matches($tagBlock, '(?m)^\s+-\s+(\S+)\s*$') | ForEach-Object { $_.Groups[1].Value }
  Report (($tags.Count -ge 3) -and ($tags.Count -le 6)) 'tags が3〜6個' 'FAIL' "$($tags.Count)個"
  Report (-not ($tags | Where-Object { $_ -notmatch '^[a-z0-9]+([-/][a-z0-9]+)*$' })) 'tags が英小文字の kebab-case（階層は /）'
  Report (-not ($tags | Where-Object { $_ -in 'inbox', 'knowledge', 'active', 'superseded', 'project', 'index' })) 'tags に type / status の値を含まない'
  $srcBlock = [regex]::Match($front, '(?s)sources:\n(.*)').Groups[1].Value
  $srcs = [regex]::Matches($srcBlock, '(?m)^\s+-\s+(.+)$') | ForEach-Object { $_.Groups[1].Value }
  Report (($srcs.Count -ge 1) -and -not ($srcs | Where-Object { $_ -notmatch '^.+ conversation ".+"$' })) 'sources が `<AI名> conversation "<テーマ>"` の形'

  # 見出し
  $heads = [regex]::Matches($raw, '(?m)^## (.+?)\s*$') | ForEach-Object { $_.Groups[1].Value }
  Report (($heads -join '|') -eq ($order -join '|')) '見出し7つが、定められた順番で、すべてある' 'FAIL' ($heads -join ', ')

  # Goal 末尾
  $goal = Section $raw 'Goal' 'Principles'
  $lastLine = ($goal -split "`n")[-1]
  Report ($lastLine -match '^統合先の候補: .*(knowledge/\S+?\.md|新規トピック)（キーワード: .+）') 'Goal の末尾が「統合先の候補: …（キーワード: …）」の行' 'FAIL' $lastLine

  # 「なし」は、見出しの直後に1語だけの行にする。補足が付くと、項目ありとみなされ、後続の点検（3行セットなど）が意味を成さない
  $badNone = @{}
  foreach ($pair in @(@('Principles', 'Decisions'), @('Decisions', 'Facts'), @('Facts', 'Gotchas'), @('Gotchas', 'Open Questions'), @('Open Questions', 'Next Actions'), @('Next Actions', ''))) {
    if ((Section $raw $pair[0] $pair[1]) -match '(?s)^なし.+') {
      $badNone[$pair[0]] = $true
      Report $false "$($pair[0]) の「なし」が単独の行になっている" 'FAIL' '「なし」は見出しの直後に1語だけで書く。補足は別の見出しか別のファイルに書く'
    }
  }
  if ($badNone.Count -eq 0) { Report $true '「なし」と書いた見出しは、単独の行になっている' }

  # Decisions
  $dec = Section $raw 'Decisions' 'Facts'
  if (($dec -ne 'なし') -and -not $badNone['Decisions']) {
    $n = Count $dec '(?m)^- \*\*'
    Report ($n -ge 1) 'Decisions が「なし」でなければ、項目がある'
    Report ((Count $dec '(?m)^- \*\*.+\*\*（\d{4}-\d{2}-\d{2}') -eq $n) 'Decisions の全項目に日付がある'
    Report ((Count $dec '(?m)^  - 根拠:') -eq $n) 'Decisions の全項目に根拠がある' 'FAIL' "項目$n、根拠$(Count $dec '(?m)^  - 根拠:')"
    Report ((Count $dec '(?m)^  - 却下案:') -eq $n) 'Decisions の全項目に却下案がある' 'FAIL' "項目$n、却下案$(Count $dec '(?m)^  - 却下案:')"
    # 「AI の提案」と「未承認」が同じ行にある、または「- 提案:」で始まる行を、未承認の提案の混入とみなす。
    # 語だけで見ると、「AI の提案への承認」のような説明まで拾う（2026-10-06 の誤検知）。
    Report ($dec -notmatch '(?m)(AI の提案[^\r\n]*未承認|^\s*- 提案[:：])') 'Decisions に未承認の「AI の提案」が混ざっていない（提案は Open Questions へ）' 'WARN'
  }

  # Facts
  $facts = Section $raw 'Facts' 'Gotchas'
  if (($facts -ne 'なし') -and -not $badNone['Facts']) {
    $bad = [regex]::Matches($facts, '(?m)^- .+$') | ForEach-Object Value | Where-Object { $_ -notmatch '（確認: .+、根拠: .+）|（仮説' }
    Report (-not $bad) 'Facts の全項目に「（確認: …、根拠: …）」か「（仮説）」がある' 'FAIL' (($bad | Select-Object -First 1) -replace '^(.{40}).*$', '$1…')
  }

  # Gotchas
  $got = Section $raw 'Gotchas' 'Open Questions'
  if (($got -ne 'なし') -and -not $badNone['Gotchas']) {
    $s = Count $got '(?m)^- 状況:'; $c = Count $got '(?m)^  - 原因:'; $r = Count $got '(?m)^  - 解決:'
    Report (($s -ge 1) -and ($s -eq $c) -and ($s -eq $r)) 'Gotchas の全項目が「状況・原因・解決」の3行セット' 'FAIL' "状況$s、原因$c、解決$r"
  }

  # メモをまたぐ重複の候補を集める（Facts / Gotchas のインラインコード。判定は、ループの後）
  foreach ($m in [regex]::Matches($facts + "`n" + $got, '`([^`\n]+)`')) {   # 長さで絞る前に全部取る（先に絞ると、バッククォートの対応がずれる）
    $s = $m.Groups[1].Value
    if ($s.Length -lt 8) { continue }
    if (-not $script:spans.ContainsKey($s)) { $script:spans[$s] = [System.Collections.Generic.HashSet[string]]::new() }
    [void]$script:spans[$s].Add($file.Name)
  }

  # 文章の規則
  Report ($raw -notmatch 'この会話|上記|さっき|先ほど|前述') '会話に依存する表現（この会話、上記、さっき、先ほど、前述）が無い'
  Report (($raw -notmatch '(?i)[A-Za-z]:\\Users\\(?![<%$])[^\\\s`]+') -and ($raw -notmatch '[\w.+-]+@(?!(?:[\w-]+\.)*(?:example\.(?:com|org|net)|local|invalid|test|example)(?![\w-]|\.\w))[\w-]+\.[\w.]+')) '共有したくない値（ユーザー名を含むパス、メールアドレス。example.com / *.local / *.invalid / *.test は例示用なので除く）が無い'
  Report ($raw -notmatch '(?i)(token|secret|password|bearer)\s*[:=]\s*\S') '秘匿値らしき行（token / secret / password / bearer の値）が無い'
  $lines = ($raw -split "`n").Count
  Report ($lines -le 150) 'ファイル全体が150行以内（目安）' 'WARN' "$lines 行"
  $noCode = [regex]::Replace($raw, '`[^`\n]*`', '')   # インラインコード内の <…> はコマンドの書式なので除く
  Report ((Count $noCode '<[^>\n]+>') -eq 0) '`<…>` が残っていない（インラインコード内は除く）' 'WARN' "$(Count $noCode '<[^>\n]+>') 件"
}

# メモをまたぐ重複（2件以上のメモを点検するときだけ）。同じ事実・落とし穴を、分けたメモの両方に書いていないか、手で確認する
if ($Path.Count -ge 2) {
  Write-Host '== メモの間'
  $dups = @($script:spans.GetEnumerator() | Where-Object { $_.Value.Count -ge 2 } | Sort-Object Name)
  Report ($dups.Count -eq 0) '同じインラインコードが、複数のメモの Facts / Gotchas に重複していない（候補があれば、同じ事実・落とし穴を重複して書いていないか確認する）' 'WARN' ((@($dups | Select-Object -First 5 | ForEach-Object { '`' + $_.Key + '`（' + (($_.Value | Sort-Object) -join ', ') + '）' }) -join '、') + $(if ($dups.Count -gt 5) { " ほか$($dups.Count - 5)件" } else { '' }))
}

Write-Host ''
Write-Host "RESULT: files=$($Path.Count) pass=$($script:pass) fail=$($script:fail) warn=$($script:warn)"
Write-Host '手で確認する項目: 1ファイル1テーマ / 同じ日の既存メモとの重複 / 作業ログ（何をいつやったか）の混在 / Decisions が、ユーザーの明示または承認した決定か / 確認した事実の根拠が本当か / 範囲を限定された場合は、その範囲だけか'
exit $script:fail
