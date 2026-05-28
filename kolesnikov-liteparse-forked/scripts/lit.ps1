$SkillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$LocalLit = Join-Path $SkillRoot "tools\liteparse-node\node_modules\.bin\lit.cmd"

if (-not (Test-Path -LiteralPath $LocalLit)) {
    Write-Error "LiteParse is not installed in this skill. Expected: $LocalLit"
    exit 1
}

& $LocalLit @args
exit $LASTEXITCODE
