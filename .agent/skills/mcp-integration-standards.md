---
name: MCP Integration Standards
description: Strict guidelines for how Agen subagents should utilize and connect to Model Context Protocol (MCP) servers.
---

# MCP Integration Standards

As an autonomous AI agent in the Agen Swarm, you have the ability to dynamically load and utilize external tools through the Model Context Protocol (MCP). When interacting with MCP tools, you must adhere to the following standards:

## 1. Tool Discovery and Context
- **Query First:** Before attempting a complex operation (e.g., searching the web, querying a Postgres database), always check if an appropriate MCP tool is already loaded in your context.
- **Understand the Schema:** MCP tools are dynamically loaded. Always read the tool's parameter schema carefully. Do not assume the parameter names are identical to internal ReAct tools.

## 2. Execution Boundaries
- **Idempotency:** When using MCP tools that mutate external state (e.g., `github_create_pr` or `postgres_execute_write`), ensure your actions are idempotent if possible.
- **Data Privacy:** Do not pass sensitive workspace environment variables (like API keys) into external MCP servers like Tavily or public search providers.
- **Fallbacks:** If an MCP server connection drops or a tool returns an error, gracefully fallback to native tools (e.g., if a web search fails, use native `curl` or `read_browser_page` if necessary).

## 3. Asynchronous Execution
MCP servers may be running remotely. Always await their responses gracefully. If an MCP tool is taking too long, use internal swarm coordination to spawn a dedicated subagent to wait for the result so the main thread remains unblocked.
