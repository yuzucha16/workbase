# room clean <Project> --path <Tab> で、Area の原本置き場 (areas/<Area>/_noai/source/) の中を補完する。
# 使い方: PowerShell のプロファイルから dot-source する（追加インストール不要。PowerShell 5.1 / 7 で動く）。
#   . "<works>\resources\workflow-kit\room\room-completion.ps1"
# 対象: `uv run [--script] room.py clean <Project> --path ...`、`room.py clean ...`、`python room.py clean ...`
# 置き場の探し方は room.py と同じ: $env:ROOM_VAULT、$env:WORKS_DIR、~/works の順。Area は projects/<Project>/README.md の area: から引く。

Register-ArgumentCompleter -Native -CommandName uv, python, py, python3 -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)

    $words = @($commandAst.CommandElements | ForEach-Object { $_.ToString().Trim("'", '"') })
    if (-not ($words | Where-Object { $_ -like '*room.py' })) { return }
    $ci = [array]::IndexOf($words, 'clean')
    if ($ci -lt 0) { return }

    # 補完中の語が --path の値か（直前の語が --path、または --path=…）
    $prev = if ($wordToComplete -eq '') { $words[-1] } else { if ($words.Count -ge 2) { $words[-2] } else { '' } }
    if ($prev -ne '--path') { return }

    # Project 名: clean の次の、- で始まらない語
    $project = $null
    for ($i = $ci + 1; $i -lt $words.Count; $i++) {
        if ($words[$i] -notlike '-*') { if ($words[$i-1] -ne '--path') { $project = $words[$i]; break } }
    }
    if (-not $project) { return }

    $vault = if ($env:ROOM_VAULT) { $env:ROOM_VAULT } elseif ($env:WORKS_DIR) { $env:WORKS_DIR } else { Join-Path $HOME 'works' }
    $readme = Join-Path $vault "projects/$project/README.md"
    if (-not (Test-Path -LiteralPath $readme)) { return }
    $area = $null
    foreach ($line in Get-Content -LiteralPath $readme -Encoding UTF8 -TotalCount 40) {
        if ($line -match '^area:\s*(.*?)\s*(#.*)?$') { $area = $Matches[1].Trim("'", '"'); break }
    }
    if (-not $area) { return }
    $src = Join-Path $vault "areas/$area/_noai/source"
    if (-not (Test-Path -LiteralPath $src)) { return }

    # 入力中の語を「親ディレクトリ + 前方一致」に分ける（区切りは / か \）
    $typed = $wordToComplete.Trim("'", '"') -replace '\\', '/'
    $slash = $typed.LastIndexOf('/')
    $dirPart = if ($slash -ge 0) { $typed.Substring(0, $slash + 1) } else { '' }
    $leaf = $typed.Substring($dirPart.Length)
    if ($dirPart -match '(^|/)\.\.(/|$)' -or $dirPart.StartsWith('/')) { return }   # room.py が拒否する指定は出さない
    $base = if ($dirPart) { Join-Path $src $dirPart } else { $src }
    if (-not (Test-Path -LiteralPath $base)) { return }

    Get-ChildItem -LiteralPath $base -Force |
        Where-Object { $_.Name -like "$([WildcardPattern]::Escape($leaf))*" -and -not ($dirPart -eq '' -and $_.Name -eq 'tmp') } |
        Sort-Object @{Expression = { -not $_.PSIsContainer }}, Name |
        ForEach-Object {
            $rel = $dirPart + $_.Name + $(if ($_.PSIsContainer) { '/' } else { '' })
            $text = if ($rel -match "[\s'`"()\[\]{}&;,#$]") { "'" + $rel.Replace("'", "''") + "'" } else { $rel }
            [System.Management.Automation.CompletionResult]::new($text, $rel, 'ParameterValue', $rel)
        }
}
