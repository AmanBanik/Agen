---
name: secure-scripting
description: Best practices for writing robust Python and shell scripts in the Agen repo.
effort_level: High
required_tools: Python, Bash/PowerShell
triggers: ["writing scripts", "using subprocess", "calling external APIs"]
---
# Skill: Secure Scripting

## Overview
As the swarm scales, insecure scripts become severe vulnerabilities. This skill dictates how to write bulletproof Python and shell scripts that can handle the chaotic environment of autonomous agents.

## V3 Forward-Focus
All new scripts must be `async` compatible. Synchronous code bottlenecks the event loop and prevents the distributed swarm from scaling.

## Strict Rules
1. **No Raw Shell Injection:** Never interpolate user input directly into a shell command. Always use `subprocess.run()` with a list of arguments.
   - *Bad:* `os.system(f"ls {user_dir}")`
   - *Good:* `subprocess.run(["ls", user_dir], check=True)`
2. **Timeouts are Mandatory:** All external requests, API calls, or subprocesses must have strict timeouts. An agent waiting forever is a dead agent.
3. **Cross-Platform Compatibility:** Always use Python's `pathlib` for file paths. Do not assume `/` or `\` path separators.
   - *Good:* `Path(base_dir) / "config.json"`
4. **Rate Limits & Backoff:** When hitting external APIs, implement exponential backoff.
