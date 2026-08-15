$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "      ▄▄████▄▄      " -ForegroundColor Green
Write-Host "    ▄██████████▄    " -ForegroundColor Green
Write-Host "   ████▀▀  ▀▀████   " -ForegroundColor Yellow
Write-Host "  ████        ████  " -ForegroundColor Yellow
Write-Host " ██████████████████ " -ForegroundColor DarkYellow
Write-Host "█████▀▀▀▀▀▀▀▀▀▀█████" -ForegroundColor DarkYellow
Write-Host "████            ████" -ForegroundColor Red
Write-Host "███              ███" -ForegroundColor Red
Write-Host ""
Write-Host "Initializing Agen V2 Autonomous Swarm Setup..." -ForegroundColor Cyan

$targetDir = "$env:LOCALAPPDATA\Agen\bin"
$exePath = "$targetDir\agen.exe"
$downloadUrl = "https://github.com/AmanBanik/Agen/releases/latest/download/agen.exe"

if (-not (Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

Write-Host ">>> Fetching standalone executable from GitHub Releases (~60MB)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $downloadUrl -OutFile $exePath -UseBasicParsing

Write-Host ">>> Binary secured." -ForegroundColor Green

# Add to User PATH if not present
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notmatch [regex]::Escape($targetDir)) {
    Write-Host ">>> Updating User PATH..." -ForegroundColor Yellow
    $newPath = $userPath + ";" + $targetDir
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    # Update current session PATH so it works immediately
    $env:PATH += ";$targetDir"
    Write-Host ">>> Path updated." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "You can now type 'agen' in your terminal to start the swarm." -ForegroundColor White
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""