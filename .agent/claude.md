# Claude Code Configuration

When interacting via **Claude Code**, prioritize deep architectural reasoning and cross-file refactoring.

## Tool Usage
- Use your file editing tools carefully; prefer targeted replacements over full file rewrites.
- Always verify cross-platform compatibilities. You are running in a terminal environment; assume standard bash/zsh or powershell depending on the OS.

## Directives
- If a user asks for a structural change, cross-reference `agent.md` to ensure it aligns with V3.
- Claude should utilize `comprehensive-testing.md` to run `pytest` and validate its own work before presenting it to the user.
