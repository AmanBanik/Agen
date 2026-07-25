# Terminal Agent Deployment Guide (Windows x64)

This directory contains the deployment pipelines for distributing **Terminal Agent** on **Windows 64-bit (x64)** architectures in two official formats:

---

## Method 1: PowerShell One-Liner Web Installer (`irm | iex`)
Designed for rapid developers and CI/CD environments. This installer pulls the latest release, builds an isolated virtual environment, installs dependencies, and configures global PATH variables.

### Usage:
Run the following command in any PowerShell (Administrator or standard user) window:
```powershell
irm https://raw.githubusercontent.com/<user>/agentic/main/deploy/install.ps1 | iex
```

### What It Does:
1. **Architecture Audit**: Verifies Windows x64 (`AMD64`) OS.
2. **Environment Isolation**: Creates `C:\Users\<user>\.local\share\TerminalAgent\venv`.
3. **Core Installation**: Installs the split-brain FastAPI backend and Typer CLI client.
4. **Global Shell Access**: Registers `agen.bat` and `agent.bat` in your Windows `PATH`.
5. **Self-Healing Launcher**: Automatically starts the AI uvicorn server in the background whenever `agen` is invoked if it is not already running.

---

## Method 2: Standalone MSI / EXE Installer (PyInstaller + WiX / Inno Setup)
Designed for enterprise workstations, offline machines, and standard GUI installation workflows.

### Building the Standalone Executable:
1. Open PowerShell and navigate to the `deploy/` directory:
   ```powershell
   cd deploy
   ```
2. Execute the automated MSI / Binary builder pipeline:
   ```powershell
   .\build_msi.ps1
   ```
3. Once completed, the standalone binaries will be output to `deploy\dist\agen.exe` and `deploy\dist\agent.exe`.
4. Compile `installer.iss` using **Inno Setup Compiler** (`ISCC.exe`) or **WiX Toolset** to produce `TerminalAgent-Setup-x64.msi`.

### Enterprise Features:
* **Zero Dependencies**: Packs Python runtime, FastAPI, Rich, Typer, and LangChain into a single native Windows x64 executable.
* **Registry Integration**: Automatically registers `C:\Program Files\TerminalAgent` in system `PATH`.
* **Start Menu Shortcuts**: Installs command-prompt launchers and documentation shortcuts.
