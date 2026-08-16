---
name: dependency-management
description: Policy on adding and pinning dependencies in pyproject.toml.
effort_level: Medium
required_tools: pip, pyproject.toml
triggers: ["adding dependencies", "pyproject.toml", "pip install", "hidden-imports"]
---
# Skill: Dependency Management

## Overview
Careless dependency addition bloats the PyInstaller binary and introduces security risks.

## Strict Rules
1. **Justification:** Every new dependency added to `pyproject.toml` must be heavily justified. If a standard library module can do the job, use it instead.
2. **Pinning:** Always pin dependencies using strict or compatible release specifiers (e.g., `>=1.2.0,<2.0.0`).
3. **Cross-Platform Builds Interaction:** If you add a library that relies on dynamic imports (like a new LLM provider in LangChain), you *must* consult `cross-platform-builds.md` and add it to the PyInstaller hidden-imports list.
