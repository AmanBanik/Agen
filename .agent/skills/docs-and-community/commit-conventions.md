---
name: commit-conventions
description: Commit message format, changelog expectations, and task completion standards.
effort_level: Low
required_tools: Git
triggers: ["git commit", "changelog", "finishing a task", "writing PR descriptions"]
---
# Skill: Commit Conventions

## Overview
Standardizing how the swarm records history ensures that humans and other agents can trace the evolution to V3.

## Strict Rules
1. **Commit Format:** Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `chore:`). The first line must be under 72 characters.
2. **Changelog:** Major features must include a bullet point in the repository's `CHANGELOG.md`.
3. **Definition of "Done":** A task is not "done" until tests pass, documentation is updated, and the user has been presented with a clear summary of the changes. Never hand a task back to the user with "I left a placeholder for you."
