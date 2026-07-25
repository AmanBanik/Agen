# Skill: Model Context Protocol (MCP) Tool Integration & Usage

## 1. Core MCP Principles
When active Model Context Protocol (MCP) servers are enabled in your project session:
1. **Dynamic Tool Access**: You have direct access to external data silos, database engines, and web scrapers without requiring manual API scripting or hardcoded credentials.
2. **Actionable Tool Commands**: When instructed to perform operations covered by active MCP servers (e.g., querying DuckDB/Postgres, searching GitHub repos, scraping web pages via Puppeteer/Tavily), formulate exact tool calls or Python execution scripts leveraging these connectors.
3. **Security & Least Privilege**: Never output raw API tokens, connection strings, or credentials to terminal logs or user-facing Markdown responses.

## 2. Standard MCP Server Patterns
* **`filesystem`**: Use for local file inspections, directory tree traversals, and reading/writing project data files safely.
* **`motherduck` / `postgresql` / `sqlite`**: Use SQL queries for schema inspection (`list_tables`, `describe_table`) before writing complex analytics queries.
* **`github`**: Search remote repositories, inspect pull requests, and analyze branch diffs directly from terminal history.
* **`sequential_thinking`**: When tackling complex refactors or multi-step algorithmic challenges, invoke structured step-by-step cognitive planning before generating final code.
