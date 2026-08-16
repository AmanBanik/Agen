---
name: agent-boundaries
description: Rules covering what the autonomous agent must NOT do without explicit human confirmation.
effort_level: Medium
required_tools: Git, File System
triggers: ["git operations", "modifying permissions", "deleting files", "managing PRs"]
---
# Skill: Agent Boundaries

## Overview
Autonomous agents are powerful, but that power must be constrained to prevent catastrophic damage to the repository or CI/CD pipelines.

## Strict Rules
You must **NOT** perform any of the following actions without explicitly asking the human user for confirmation first:
1. **Destructive Git Operations:** Never force-push (`git push -f`) or rewrite published git history (`git rebase` on main branches).
2. **Out-of-Scope Deletion:** Never delete files or directories that fall outside the explicit scope of your current task.
3. **Security Mutations:** Never modify CI/CD secrets or GitHub Actions workflow permissions (`.github/workflows/*.yml` `permissions:` blocks).
4. **Pull Requests:** Never auto-merge PRs.
5. **Dependencies:** Do not install or remove dependencies without noting the exact changes in the PR description.
