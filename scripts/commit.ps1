# Uso: .\scripts\commit.ps1 "titulo" "corpo opcional"
# Remove automaticamente o Co-authored-by do Cursor, se aparecer.
param(
    [Parameter(Mandatory = $true)][string]$Title,
    [string]$Body = ""
)

$ErrorActionPreference = "Stop"
$msgFile = Join-Path (Get-Location) ".git\COMMIT_MSG_CLEAN"

if ($Body) {
    $text = "$Title`r`n`r`n$Body"
} else {
    $text = $Title
}

[System.IO.File]::WriteAllText($msgFile, $text)

git add -A
git commit -F $msgFile

$log = git log -1 --format=%B
if ($log -match "Co-authored-by:\s*Cursor") {
    $env:FILTER_BRANCH_SQUELCH_WARNING = "1"
    git filter-branch -f --msg-filter "grep -v 'Co-authored-by: Cursor'" HEAD~1..HEAD
}

Remove-Item $msgFile -ErrorAction SilentlyContinue
git log -1 --format="commit %h%nAuthor: %an <%ae>%n%n%s%n"
