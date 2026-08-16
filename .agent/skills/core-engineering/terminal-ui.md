---
name: terminal-ui
description: The aesthetic engine. Rules for using Typer and Rich.
effort_level: Medium
required_tools: Python (typer, rich)
triggers: ["adding CLI output", "modifying console/Rich formatting", "new Typer command"]
---
# Skill: Terminal UI & Aesthetics

## Overview
Agen has a highly specific terminal aesthetic. We do not output raw, unformatted text. We use deep obsidian backgrounds, warning orange accents, and turquoise/teal highlights. 

## Required Libraries
- **Typer:** Use for all CLI routing, commands, and argument parsing.
- **Rich:** Use for formatting all terminal output.

## Strict Rules
1. **Never use `print()`:** Standard `print()` is forbidden for user-facing output. You must use `rich.console.Console`.
2. **Feedback & Spinners:** Long-running agent tasks must be wrapped in `with console.status("[cyan]Agent is thinking...[/cyan]"):` to show the user that the system hasn't frozen.
3. **Color Palette:**
   - Success: `[bold green]`
   - Warnings/Stats: `[bold orange3]`
   - Primary accents/Links: `[bold cyan]`
4. **Markdown Support:** Utilize Rich's `Markdown` class to render LLM responses beautifully in the terminal.

## Headless Remote Nodes (V3 Compatibility)
When subagents run headless on remote nodes, there is no local TTY for Rich to render to. 
- *Rule:* Remote subagents must ship structured JSON logs back to the orchestrator.
- The client-side orchestrator is exclusively responsible for interpreting these logs and rendering them via Rich.
