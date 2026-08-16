---
name: ci-cd-deployments
description: Managing GitHub Actions and automated releases.
effort_level: Medium
required_tools: GitHub Actions, YAML
triggers: ["GitHub actions", "secrets", "release matrix", "workflows"]
---
# Skill: CI/CD & Deployments

## Overview
Agen relies heavily on GitHub Actions for its matrix testing and release automation.

## Strict Rules
1. **Secret Management:** Ensure API keys (like `GEMINI_API_KEY` for integration tests) are injected securely via GitHub Secrets and never logged to `stdout`.
2. **Matrix Updates:** Any change to core dependencies requires ensuring the Python matrix (3.10, 3.11, 3.12) and OS matrix (Ubuntu, Windows, macOS) are still covered in the `.github/workflows/` YAML files.
3. **Automated Releases:** Tag pushes must trigger the PyInstaller build and automatically upload binaries to GitHub Releases.

## Examples
- *Bad:* Hardcoding API keys in a test script.
- *Good:* Passing secrets safely via environment variables in the action workflow:
  ```yaml
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  ```
