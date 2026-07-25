<#
.SYNOPSIS
    Terminal Agent Windows x64 Web Installer (irm | iex)
.DESCRIPTION
    One-liner installer for Google Antigravity Terminal Agent on Windows x64.
    Usage:
        irm https://raw.githubusercontent.com/AmanBanik/Agen/main/deploy/install.ps1 | iex
#>

$ErrorActionPreference = "Stop"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "   TERMINAL AGENT v0.2.0 - Windows x64 Installer" -ForegroundColor Cyan
Write-Host "   Split-Brain Architecture (FastAPI + Typer CLI)" -ForegroundColor DarkPurple
Write-Host "==========================================================`n" -ForegroundColor Cyan

# 1. Verify Architecture & OS
if ($env:PROCESSOR_ARCHITECTURE -ne "AMD64" -and $env:PROCESSOR_ARCHITEW6432 -ne "AMD64") {
    Write-Warning "This installer is designed for Windows 64-bit (x64) architecture."
}

# 2. Check for Python 3.10+
Write-Host "[1/5] Checking Python 3 x64 environment..." -ForegroundColor Yellow
try {
    $pythonVer = & python --version 2>&1
    if ($pythonVer -match "Python 3\.(1[0-9]|[2-9][0-9])") {
        Write-Host "  -> Found: $pythonVer" -ForegroundColor Green
    } else {
        throw "Python 3.10+ is required."
    }
} catch {
    Write-Host "  [Error] Python 3.10+ (x64) not found in PATH." -ForegroundColor Red
    Write-Host "  Please install Python 3.10+ from https://www.python.org/downloads/windows/" -ForegroundColor Yellow
    exit 1
}

# 3. Setup Install Directory
$installDir = "$env:USERPROFILE\.local\share\TerminalAgent"
Write-Host "[2/5] Preparing installation folder: $installDir..." -ForegroundColor Yellow
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
}

# Copy current project files if running locally, or clone repo if running via remote Web Installer
if (Test-Path ".\pyproject.toml") {
    Write-Host "  -> Local repository detected, syncing files..." -ForegroundColor Green
    Copy-Item -Path ".\*" -Destination $installDir -Recurse -Force -Exclude "venv",".git",".agent_sessions",".agent_skills"
} else {
    Write-Host "  -> Downloading latest release for Windows x64..." -ForegroundColor Green
    git clone https://github.com/AmanBanik/Agen.git $installDir
}

# 4. Create Virtual Environment & Install Package
Write-Host "[3/5] Building isolated virtual environment (x64)..." -ForegroundColor Yellow
Set-Location $installDir
if (!(Test-Path ".\venv")) {
    & python -m venv venv
}

Write-Host "[4/5] Installing Terminal Agent core package and dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -m pip install --upgrade pip quiet
& .\venv\Scripts\pip.exe install -e . --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Package installation successful!" -ForegroundColor Green
} else {
    Write-Host "  [Error] Package installation failed." -ForegroundColor Red
    exit 1
}

# 5. Configure PATH & Global Command Access
Write-Host "[5/5] Registering global 'agen' and 'agent' commands..." -ForegroundColor Yellow
$binDir = "$installDir\venv\Scripts"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binDir*") {
    $newPath = "$userPath;$binDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    $env:Path = "$env:Path;$binDir"
    Write-Host "  -> Added $binDir to User PATH variable." -ForegroundColor Green
} else {
    Write-Host "  -> PATH already configured." -ForegroundColor Green
}

# Generate self-healing launcher scripts
$launcherBat = "$binDir\agen.bat"
$launcherContent = @"
@echo off
REM Self-healing launcher for Terminal Agent on Windows x64
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [Notice] Starting local AI backend server...
    start /b "" "%installDir%\venv\Scripts\uvicorn.exe" backend.main:app --host 127.0.0.1 --port 8000 >nul 2>&1
    timeout /t 2 /nobreak >nul
)
"%installDir%\venv\Scripts\python.exe" "%installDir%\client\cli.py" %*
"@
Set-Content -Path $launcherBat -Value $launcherContent -Encoding ASCII
Copy-Item -Path $launcherBat -Destination "$binDir\agent.bat" -Force

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "   SUCCESS! Terminal Agent installed and ready." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Try it now in any new PowerShell or CMD window:" -ForegroundColor Cyan
Write-Host "  agen --help" -ForegroundColor Yellow
Write-Host "  agen init --profile ds" -ForegroundColor Yellow
Write-Host "  agen chat `@README.md `"Summarize this project`"" -ForegroundColor Yellow
Write-Host "==========================================================`n" -ForegroundColor Cyan
