import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
build_exe_options = {
    "packages": ["os", "typer", "rich", "fastapi", "uvicorn", "langchain", "httpx"],
    "excludes": ["tkinter", "test"],
    "include_files": ["backend/", "client/", "README.md", "pyproject.toml"]
}

setup(
    name="Agen V2",
    version="0.3.0",
    description="Terminal Agent v2.0 - Autonomous AI CLI",
    options={"build_exe": build_exe_options},
    executables=[Executable("client/cli.py", target_name="agen.exe")]
)
