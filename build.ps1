# Gera lexer e parser ANTLR4 para Python 3
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$jar = Join-Path $root "tools\antlr-4.13.2-complete.jar"
$src = Join-Path $root "src"

if (-not (Test-Path $jar)) {
    Write-Host "Baixando ANTLR 4.13.2..."
    New-Item -ItemType Directory -Force -Path (Join-Path $root "tools") | Out-Null
    Invoke-WebRequest -Uri "https://www.antlr.org/download/antlr-4.13.2-complete.jar" `
        -OutFile $jar
}

Push-Location $src
try {
    java -jar $jar -Dlanguage=Python3 LangLexer.g4 2>&1
    java -jar $jar -Dlanguage=Python3 -visitor LangParser.g4 2>&1
    Write-Host "Build concluido."
}
finally {
    Pop-Location
}
