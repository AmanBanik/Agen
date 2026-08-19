import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
build_exe_options = {
    "packages": ["os", "typer", "rich", "fastapi", "uvicorn", "langchain", "httpx", "langchain_google_genai", "mcp"],
    "excludes": ["tkinter", "test", "pandas", "matplotlib", "scipy", "cv2", "IPython", "pytest"],
    "include_files": ["backend/", "client/", "README.md", "pyproject.toml", ".agent/", ".agent_skills/"]
}

setup(
    name="Agen V2",
    version="2.0.0",
    description="Terminal Agent V2 - Autonomous AI Swarm CLI with RAG & MCP",
    options={"build_exe": build_exe_options},
    executables=[Executable("client/cli.py", target_name="agen.exe")]
)
