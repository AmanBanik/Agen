---
name: cross-platform-builds
description: Handling PyInstaller and platform-specific fallback scripts.
effort_level: High
required_tools: PyInstaller, Shell/Bash, PowerShell
triggers: ["PyInstaller", "install.sh", "setup.ps1", "binary compilation"]
---
# Skill: Cross-Platform Builds

## Overview
Agen ships as a 170MB standalone `.exe` for Windows, but relies on robust install scripts (`install.sh`, `setup.ps1`) for other platforms.

## Strict Rules
1. **PyInstaller Hidden Imports:** Heavy AI libraries (`langchain`, `typer`, `pydantic`) often rely on dynamic imports. When modifying dependencies, you *must* update the `.spec` file's `hiddenimports` array.
2. **Environment Variables:** Compiled binaries bundle their environment. Avoid reading `.env` files that won't exist on the user's target machine. 
3. **Install Scripts:** `install.sh` and `setup.ps1` must be idempotent. They should safely update an existing installation without wiping user configuration.
