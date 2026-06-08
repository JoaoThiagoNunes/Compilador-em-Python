# Uso: .\scripts\commit.ps1 "titulo" "corpo opcional"
param(
    [Parameter(Mandatory = $true)][string]$Title,
    [string]$Body = ""
)

$ErrorActionPreference = "Stop"
$msgFile = Join-Path (Get-Location) ".git\COMMIT_MSG_CLEAN"

if ($Body) {
    "$Title`n`n$Body" | Set-Content -Path $msgFile -Encoding UTF8
} else {
    $Title | Set-Content -Path $msgFile -Encoding UTF8
}

git commit -F $msgFile

$log = git log -1 --format=%B
if ($log -match "Co-authored-by:\s*Cursor") {
    git commit --amend -F $msgFile
}

Remove-Item $msgFile -ErrorAction SilentlyContinue
git log -1 --format="commit %h%nAuthor: %an <%ae>%n%n%s%n"
