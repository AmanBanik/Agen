---
name: long-term-memory
description: Session persistence across reboots using SQLite or Graph DBs.
effort_level: High
required_tools: SQLite, JSON, NetworkX
triggers: ["session persistence", "SQLite", "saving context", "agent memory"]
---
# Skill: Long-Term Memory

## Overview
Agents need persistence. If the user closes the terminal, the swarm must remember the context of the conversation and the project's state upon reboot.

## V3 Forward-Focus
Memory must be serializable and portable across remote nodes.

## Strict Rules
1. **Storage Mechanism:** Use SQLite for tabular/structured logs (e.g., past tool calls, errors) and JSON files for conversation histories.
2. **State Recovery:** Implement a bootstrap routine. When the CLI starts, it checks for a `.agen/session.db` and loads the last known state.
3. **Graph Memory:** For complex projects, explore Graph structures (e.g., representing dependencies or agent relationships).
