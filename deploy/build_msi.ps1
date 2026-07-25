<#
.SYNOPSIS
    Windows x64 MSI / EXE Standalone Build Pipeline
.DESCRIPTION
    Compiles Terminal Agent into a standalone Windows x64 executable (agen.exe)
    and packages it into an MSI installer using WiX Toolset / Inno Setup.
#>

$ErrorActionPreference = "Stop"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "   TERMINAL AGENT - Windows x64 MSI / Binary Builder" -ForegroundColor Cyan
Write-Host "==========================================================`n" -ForegroundColor Cyan

# 1. Verify Virtual Environment
$venvPython = "..\venv\Scripts\python.exe"
$venvPip = "..\venv\Scripts\pip.exe"
$pyinstaller = "..\venv\Scripts\pyinstaller.exe"

if (!(Test-Path $venvPython)) {
    Write-Host "[1/4] Creating build virtual environment..." -ForegroundColor Yellow
    & python -m venv ..\venv
}

Write-Host "[2/4] Installing packaging tools (PyInstaller, setuptools)..." -ForegroundColor Yellow
& $venvPip install --upgrade pip pyinstaller wheel setuptools --quiet
& $venvPip install -e .. --quiet

# 2. Build Standalone Executable (agen.exe)
Write-Host "[3/4] Compiling standalone Windows x64 executable (agen.exe)..." -ForegroundColor Yellow
if (!(Test-Path ".\dist")) {
    New-Item -ItemType Directory -Force -Path ".\dist" | Out-Null
}

& $pyinstaller --clean --workpath .\build --distpath .\dist .\agent.spec

if (Test-Path ".\dist\agen.exe") {
    Write-Host "  -> Successfully generated: .\dist\agen.exe (Windows x64)" -ForegroundColor Green
    Copy-Item -Path ".\dist\agen.exe" -Destination ".\dist\agent.exe" -Force
} else {
    throw "PyInstaller compilation failed to produce agen.exe."
}

# 3. Generate MSI Installer / Self-Extracting Archive
Write-Host "[4/4] Packaging into Windows x64 MSI Installer..." -ForegroundColor Yellow

# Inno Setup Script template for Windows x64 Installer
$issTemplate = @"
[Setup]
AppName=Terminal Agent
AppVersion=0.2.0
DefaultDirName={autopf}\TerminalAgent
DefaultGroupName=Terminal Agent
UninstallDisplayIcon={app}\agen.exe
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
OutputBaseFilename=TerminalAgent-Setup-x64
OutputDir=.\dist

[Files]
Source: ".\dist\agen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\agent.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Terminal Agent"; Filename: "{app}\agen.exe"

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath('{app}')

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
"@

Set-Content -Path ".\installer.iss" -Value $issTemplate -Encoding ASCII
Write-Host "  -> Generated Inno Setup specification: .\installer.iss" -ForegroundColor Green
Write-Host "  -> Note: Compile installer.iss with Inno Setup Compiler (ISCC.exe) or WiX Toolset to build TerminalAgent-Setup-x64.msi" -ForegroundColor Yellow

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "   BUILD COMPLETE! Standalone binaries in deploy\dist\" -ForegroundColor Green
Write-Host "==========================================================`n" -ForegroundColor Cyan
