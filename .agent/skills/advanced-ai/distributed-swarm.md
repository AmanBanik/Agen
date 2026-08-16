---
name: distributed-swarm
description: Expanding the swarm beyond a single terminal via Websockets, gRPC, and multi-machine orchestration.
effort_level: Expert
required_tools: Websockets, gRPC, Asyncio
triggers: ["websockets", "gRPC", "remote subagents", "inter-agent networking"]
---
# Skill: Distributed Swarm (V3)

## Overview
V3 is about scale. The swarm will no longer be confined to a single laptop; subagents may run in Docker containers, cloud VMs, or remote edge devices.

## Architectural Directives
1. **Assume Latency:** All agent-to-agent communication must be asynchronous. Use message queues or websockets.
2. **Stateless Operations:** Subagents should be as stateless as possible. They receive a payload, execute a task, and return a result.
3. **Serialization:** All data passed between nodes must be strictly JSON serializable or compiled via Protobuf/gRPC.
