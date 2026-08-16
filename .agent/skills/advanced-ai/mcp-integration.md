---
name: mcp-integration
description: Building and consuming Model Context Protocol (MCP) servers.
effort_level: High
required_tools: MCP SDKs
triggers: ["adding MCP tools", "JSON-RPC", "connecting external servers"]
---
# Skill: MCP Integration

## Overview
Agen uses the Model Context Protocol (MCP) to standardize how tools are exposed to the swarm. 

## V3 Forward-Focus
Design tools that can operate over remote network boundaries. Do not assume the MCP server is running on localhost.

## Strict Rules
1. **Adhere to the Spec:** All tools must strictly follow the JSON-RPC MCP specification.
2. **Tool Descriptions:** The description string of an MCP tool is critical. It must explain to the LLM exactly *when* and *how* to use the tool, including edge cases.
3. **Graceful Degradation:** If an MCP server disconnects, the swarm must catch the connection error and attempt to reconnect, rather than crashing the entire CLI.
