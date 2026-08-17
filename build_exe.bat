@echo off
echo Installing PyInstaller...
echo Installing dependencies...
pip install -e .
pip install pyinstaller

echo Building standalone Agen executable...
pyinstaller --name "agen" --onefile --hidden-import "typer" --hidden-import "rich" --hidden-import "pylatexenc" --hidden-import "langchain_community" --hidden-import "langchain_google_genai" --hidden-import "mcp" --add-data "backend;backend" --add-data "client;client" --add-data "pyproject.toml;." --add-data ".agent;.agent" client/cli.py

echo Build complete! The executable is located in the 'dist' folder.
pause
