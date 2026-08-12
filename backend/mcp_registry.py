# Model Context Protocol (MCP) Server Registry
from typing import Dict, Any, List

MCP_REGISTRY: Dict[str, Dict[str, Any]] = {
    "filesystem": {
        "description": "Secure read/write access to local WSL2 directories and bare-metal filesystem for code execution, dataset parsing, and artifact generation.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"],
        "env_vars": [],
        "tools": ["read_file", "write_file", "list_directory", "get_file_info", "move_file", "search_files"],
        "type": "official"
    },
    "github": {
        "description": "Remote repository management, codebase analysis, and pull request manipulation for version control integration.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        "tools": ["search_repositories", "get_file_contents", "create_or_update_file", "push_files", "create_issue", "create_pull_request"],
        "type": "official"
    },
    "motherduck": {
        "description": "High-performance analytical SQL query engine for processing massive datasets and predictive model CSVs natively using local DuckDB.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-motherduck"],
        "env_vars": ["MOTHERDUCK_TOKEN"],
        "tools": ["execute_sql", "list_tables", "describe_table", "query_csv"],
        "type": "data_science"
    },
    "postgresql": {
        "description": "Direct database interaction and schema inspection for structured relational data pipelines.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:password@localhost:5432/db"],
        "env_vars": ["POSTGRES_CONNECTION_STRING"],
        "tools": ["query", "list_tables", "describe_table"],
        "type": "official"
    },
    "gdrive": {
        "description": "Cloud storage connector for securely fetching remote datasets, spreadsheets, and external research documents.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gdrive"],
        "env_vars": ["GDRIVE_CREDENTIALS_JSON"],
        "tools": ["search_files", "read_spreadsheet", "download_file"],
        "type": "official"
    },
    "sequential_thinking": {
        "description": "Forces dynamic, step-by-step cognitive planning before executing complex architectural refactors or algorithmic problem-solving.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        "env_vars": [],
        "tools": ["sequentialthinking"],
        "type": "cognitive"
    },
    "memory": {
        "description": "Persistent knowledge-graph implementation that builds long-term project awareness and context retention across multiple terminal sessions.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env_vars": [],
        "tools": ["create_entities", "create_relations", "add_observations", "delete_entities", "delete_relations", "delete_observations", "read_graph", "search_nodes", "open_nodes"],
        "type": "official"
    },
    "tavily": {
        "description": "Optimized AI search engine connector designed for scraping and extracting up-to-date technical documentation, whitepapers, and framework specs.",
        "command": "npx",
        "args": ["-y", "@tavily/mcp-server"],
        "env_vars": ["TAVILY_API_KEY"],
        "tools": ["tavily_search", "tavily_extract"],
        "type": "search"
    },
    "puppeteer": {
        "description": "Headless browser automation engine for advanced web scraping, dynamic page inspection, and bypassing basic bot protections.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
        "env_vars": [],
        "tools": ["navigate", "screenshot", "click", "fill", "select", "hover", "evaluate"],
        "type": "official"
    },
    "fetch": {
        "description": "Lightweight web content retrieval tool optimized for converting raw HTML into clean, LLM-digestible markdown.",
        "command": "uvx",
        "args": ["mcp-server-fetch"],
        "env_vars": [],
        "tools": ["fetch"],
        "type": "official"
    },
    "sqlite": {
        "description": "Local lightweight database inspector and query executor for rapid tabular prototyping without setting up a full Postgres server.",
        "command": "uvx",
        "args": ["mcp-server-sqlite", "--db-path", "local.db"],
        "env_vars": [],
        "tools": ["read_query", "write_query", "create_table", "list_tables", "describe_table"],
        "type": "data_science"
    },
    "docker": {
        "description": "Container management, image building, and isolated sandbox execution for testing scripts in reproducible environments.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-docker"],
        "env_vars": [],
        "tools": ["list_containers", "start_container", "stop_container", "run_command_in_container", "list_images"],
        "type": "engineering"
    },
    "brave_search": {
        "description": "Privacy-first, high-speed web search API for technical research and error traceback debugging.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env_vars": ["BRAVE_API_KEY"],
        "tools": ["brave_web_search", "brave_local_search"],
        "type": "search"
    },
    "bigquery": {
        "description": "Google Cloud enterprise analytical warehouse connector for querying petabyte-scale datasets and BigQuery ML pipelines.",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-bigquery"],
        "env_vars": ["GOOGLE_APPLICATION_CREDENTIALS"],
        "tools": ["bq_execute_query", "bq_list_datasets", "bq_get_table_schema"],
        "type": "data_science"
    }
}

def get_all_servers() -> Dict[str, Dict[str, Any]]:
    return MCP_REGISTRY

def get_server_info(name: str) -> Dict[str, Any]:
    return MCP_REGISTRY.get(name, {})

def format_mcp_context(active_servers: List[str]) -> str:
    if not active_servers:
        return ""
    
    context_lines = ["\n# ACTIVE MODEL CONTEXT PROTOCOL (MCP) INTEGRATIONS:"]
    context_lines.append("You have access to the following connected MCP servers and their capabilities. Format your instructions or scripts to leverage these external tools when required:\n")
    
    for server_name in active_servers:
        info = MCP_REGISTRY.get(server_name)
        if info:
            tools_str = ", ".join([f"`{t}`" for t in info["tools"]])
            context_lines.append(f"## {server_name.upper()} ({info['type']})")
            context_lines.append(f"- **Description**: {info['description']}")
            context_lines.append(f"- **Available MCP Tools**: {tools_str}")
            if info["env_vars"]:
                context_lines.append(f"- **Required Env Vars**: {', '.join(info['env_vars'])}")
            context_lines.append("")
            
    return "\n".join(context_lines)
