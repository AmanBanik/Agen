@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building standalone Agen executable...
pyinstaller --name "agen" --onefile --add-data "backend;backend" --add-data "client;client" --add-data "pyproject.toml;." client/cli.py

echo Build complete! The executable is located in the 'dist' folder.
pause
