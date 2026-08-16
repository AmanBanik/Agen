# Agen V3: Universal Agent Ruleset

You are an autonomous AI contributor operating within the Agen repository. Your prime directive is to evolve the codebase toward **V3 (Scale & Distribution)**. 

## Precedence Rule
When instructions conflict, authority flows in this order:
1. **Specific Skill Files** (e.g., `secure-scripting.md`) override general configs.
2. **CLI-Specific Configs** (`claude.md` or `gemini.md`) override `agent.md` for tool-specific details.
3. **`agent.md`** provides the baseline.
*However, `agent.md`'s V3 Scaling Philosophy overrides ALL other files on architectural direction.*

## The V3 Scaling Philosophy
1. **No Technical Debt:** Do not write synchronous wrappers or blocking code. V3 requires fully asynchronous, non-blocking execution (`asyncio`). Any new library introduced must have async support.
2. **Network Agnostic & Distributed:** Assume any tool or subagent might eventually run on a remote server. Avoid hardcoded local paths (`C:\` or `/home/`). Use relative paths and `pathlib`.
3. **Robustness Over Speed:** The swarm must not crash. All rate limits, network drops, corrupted contexts, and missing files must be caught and gracefully handled. Log warnings instead of throwing fatal exceptions.

## Mandatory Workflow
1. **Understand Context:** Before writing code, use your reading tools to analyze the current state of the file. 
2. **Consult Skills:** Always refer to the specific skills in `.agent/skills/` relevant to your task (e.g., if touching UI, read `terminal-ui.md`).
3. **Validate:** Do not assume your code works. If testing is required, consult `comprehensive-testing.md`.
