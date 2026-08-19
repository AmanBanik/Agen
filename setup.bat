@echo off
setlocal

echo       ▄▄████▄▄      
echo     ▄██████████▄    
echo    ████▀▀  ▀▀████   
echo   ████        ████  
echo  ██████████████████ 
echo █████▀▀▀▀▀▀▀▀▀▀█████
echo ████            ████
echo ███              ███
echo.
echo Initializing Agen V2 Autonomous Swarm Setup (Windows Source Build)...

set TARGET_DIR=%USERPROFILE%\.agen-src
set REPO_URL=https://github.com/AmanBanik/Agen.git

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from python.org and try again.
    pause
    exit /b 1
)

if exist "%TARGET_DIR%" (
    echo ^> Removing existing source...
    rmdir /s /q "%TARGET_DIR%"
)

echo ^> Cloning repository (v2-stable)...
git clone --branch v2-stable --depth 1 "%REPO_URL%" "%TARGET_DIR%"

echo ^> Building isolated Python environment...
python -m venv "%TARGET_DIR%\venv"

echo ^> Installing dependencies...
call "%TARGET_DIR%\venv\Scripts\pip.exe" install --quiet -e "%TARGET_DIR%"

echo.
echo =========================================================
echo Source Installation Complete!
echo You can run the agent by activating the venv:
echo   %TARGET_DIR%\venv\Scripts\agen.exe
echo Or, we recommend using the standalone executable via setup.ps1!
echo =========================================================
pause
