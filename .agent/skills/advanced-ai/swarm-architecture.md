---
name: swarm-architecture
description: Guidelines for managing subagents, the ReAct loop, and GenAI SDK integrations.
effort_level: Expert
required_tools: Google GenAI SDK, Anthropic SDK
triggers: ["creating subagents", "modifying ReAct loop", "LLM integrations"]
---
# Skill: Swarm Architecture & GenAI SDKs

## Overview
This defines how agents interact with one another and how we communicate with upstream LLM APIs.

## V3 Forward-Focus: State Recovery
Any new subagent logic must include state-recovery mechanisms. If a subagent process crashes, the orchestrator must be able to revive it from its last known context state.

## Strict Rules
1. **GenAI SDKs:** Use the official `google-genai` or Anthropic SDKs. Do not write raw HTTP wrapper classes for LLMs. This ensures we stay aligned with upstream tool-calling schema changes.
2. **Conflict Resolution:** If multiple subagents attempt to modify the same file (e.g., `config.yaml`), implement a FileLock mechanism or route all edits through a designated "Writer Agent".
3. **The ReAct Loop:** When modifying the Reason-Act parser, ensure it is defensive. If an LLM returns a malformed JSON tool call, the parser must catch the exception, formulate an error message, and prompt the LLM to fix its own syntax.
