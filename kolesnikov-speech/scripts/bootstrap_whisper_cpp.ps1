param(
    [string]$Model = "large-v3-turbo",
    [string]$RepoUrl = "https://github.com/ggml-org/whisper.cpp.git"
)

$ErrorActionPreference = "Stop"

$SkillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$RuntimeDir = Join-Path $SkillRoot "runtime"
$RepoDir = Join-Path $RuntimeDir "whisper.cpp"

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null

if (-not (Test-Path -LiteralPath $RepoDir)) {
    git clone $RepoUrl $RepoDir
}
else {
    git -C $RepoDir pull --ff-only
}

cmake -S $RepoDir -B (Join-Path $RepoDir "build") -DCMAKE_BUILD_TYPE=Release
cmake --build (Join-Path $RepoDir "build") --config Release

$DownloadCmd = Join-Path $RepoDir "models\download-ggml-model.cmd"
if (-not (Test-Path -LiteralPath $DownloadCmd)) {
    throw "Model downloader not found: $DownloadCmd"
}

& $DownloadCmd $Model

python (Join-Path $SkillRoot "scripts\preflight.py")
