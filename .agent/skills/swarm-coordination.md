---
name: Swarm Coordination Guidelines
description: Rules for asynchronous communication, delegation, and lifecycle management of Swarm subagents.
---

# Swarm Coordination Guidelines

Agen operates as a multi-agent swarm. The primary agent can spawn independent background tasks (subagents) to handle parallel workloads. When operating in this architecture, you must follow these coordination protocols:

## 1. When to Spawn a Subagent
- **I/O Heavy Tasks:** Delegate long-running tasks like massive codebase indexing, web scraping, or waiting on remote MCP servers to a subagent using the `invoke_subagent` tool.
- **Context Isolation:** If a task requires researching an unrelated module that would pollute your current context window, spawn a "researcher" subagent.

## 2. Communication and Message Queues
- **Do not poll aggressively:** Subagents run asynchronously. Once you spawn an agent, do not write a tight loop waiting for it. Continue your work or yield your turn. 
- **Message passing:** Use `send_message` to pass data to subagents or return data to the parent agent. 
- **State Reporting:** Subagents must send a final summary message back to the primary agent right before they terminate, detailing exactly what was accomplished or if an error occurred.

## 3. Lifecycle Management
- **Task IDs:** Always keep track of the `Task ID` or `Agent ID` returned when a subagent is spawned.
- **Error Handling:** If a subagent crashes, it is the responsibility of the parent agent to read the final error state and decide whether to retry the task or report the failure to the user.
- **Zombie Prevention:** Do not spawn subagents that spawn other subagents recursively without a strict depth limit.
