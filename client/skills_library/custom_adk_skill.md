# Skill: Custom Agent Development Kit (ADK) & Multi-Agent Architecture

## 1. Tool & Function Calling Design
When building agentic systems or defining custom LLM tools:
1. **Strict Pydantic Schemas**: Every tool or API integration MUST be backed by an explicit Pydantic `BaseModel` schema with comprehensive descriptions on every field using `Field(description="...")`. LLM tool routers rely on field descriptions to make accurate routing decisions.
2. **Idempotency & Safe Execution**: Side-effecting tools (file execution, database modifications, API POST requests) should be idempotent where possible and return clear execution summaries or diff blocks.
3. **Structured Error Feedback**: If a tool fails (e.g., syntax error in generated code, SQL query syntax exception), NEVER crash the agent loop. Catch the error and return a structured JSON feedback payload to the LLM: `{"status": "error", "error_type": "SyntaxError", "details": "...", "suggestion": "..."}` so the LLM can self-correct in the next turn.

## 2. Multi-Agent Orchestration Patterns
* **Split-Brain Separation**: Keep high-speed UI/CLI communication (the "Client/Hands") separate from heavy reasoning and tool execution (the "Backend/Brain").
* **Subagent Delegation**:
  * Use lightweight models (`gemini-3.1-flash-lite`) for routing, simple file reads, formatting, and classification.
  * Delegate deep reasoning, architecture synthesis, multi-file code refactors, and mathematical proofs to heavy reasoning models (`gemini-3.5-flash`).
* **State Management**: Persist agent conversation trajectories and workspace modifications in structured JSONL logs or local SQLite storage to allow seamless resuming after restarts.
