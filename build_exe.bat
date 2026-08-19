@echo off
echo Installing PyInstaller...
echo Installing dependencies...
pip install -e .
pip install pyinstaller

echo Building standalone Agen executable...
pyinstaller --name "agen" --onefile --hidden-import "typer" --hidden-import "rich" --hidden-import "pylatexenc" --hidden-import "langchain_community" --hidden-import "langchain_google_genai" --hidden-import "mcp" --exclude-module "pandas" --exclude-module "matplotlib" --exclude-module "scipy" --exclude-module "cv2" --exclude-module "tkinter" --exclude-module "IPython" --exclude-module "pytest" --add-data "backend;backend" --add-data "client;client" --add-data "pyproject.toml;." --add-data ".agent;.agent" client/cli.py

echo Cleaning up PyInstaller artifacts...
rmdir /s /q build
del /q agen.spec

echo Build complete! The executable is located in the 'dist' folder.
