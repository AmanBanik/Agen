import os
import subprocess
import asyncio
from pathlib import Path
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from backend.mcp_registry import get_server_info
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from backend.swarm import swarm

# Security Boundary: Restrict the agent to the directory where Agen was launched
WORKSPACE_DIR = os.path.abspath(os.getcwd())

def _validate_path(path: str) -> str:
    """Ensures the requested path is within the allowed workspace directory."""
    requested_path = os.path.abspath(path)
    if not requested_path.startswith(WORKSPACE_DIR):
        raise PermissionError(f"Access Denied: Path '{path}' is outside the allowed workspace ({WORKSPACE_DIR}).")
    return requested_path

@tool
def read_file_tool(path: str) -> str:
    """Reads the contents of a file on the disk."""
    try:
        safe_path = _validate_path(path)
        with open(safe_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def list_dir_tool(path: str) -> str:
    """Lists the contents of a directory on the disk (Workspace Access)."""
    try:
        safe_path = _validate_path(path)
        if not os.path.isdir(safe_path):
            return f"Error: {safe_path} is not a valid directory."
        
        items = os.listdir(safe_path)
        if not items:
            return f"Directory {safe_path} is empty."
            
        result = [f"Contents of {safe_path}:"]
        for item in items:
            item_path = os.path.join(safe_path, item)
            item_type = "DIR" if os.path.isdir(item_path) else "FILE"
            result.append(f"[{item_type}] {item}")
        return "\n".join(result)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def write_file_tool(path: str, content: str) -> str:
    """Writes content to a file on the disk (overwrites if exists)."""
    try:
        safe_path = _validate_path(path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {safe_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

class ExecuteShellInput(BaseModel):
    command: str = Field(..., description="The shell command to execute.")

@tool(args_schema=ExecuteShellInput)
def execute_shell_tool(command: str) -> str:
    """Execute a shell command. Use this for testing scripts, inspecting the environment, or installing dependencies."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = f"Command executed successfully.\nSTDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 120 seconds."
    except Exception as e:
        return f"Error executing shell command: {str(e)}"

class ExecuteMCPInput(BaseModel):
    server_name: str = Field(..., description="The name of the MCP server (e.g. 'github', 'tavily').")
    tool_name: str = Field(..., description="The name of the tool to execute on the MCP server.")
    tool_arguments: dict = Field(default_factory=dict, description="A dictionary of arguments to pass to the MCP tool.")

@tool(args_schema=ExecuteMCPInput)
def execute_mcp_tool(server_name: str, tool_name: str, tool_arguments: dict) -> str:
    """Execute a tool on an external Model Context Protocol (MCP) server."""
    info = get_server_info(server_name)
    if not info:
        return f"Error: MCP server '{server_name}' not found in registry."
    
    return asyncio.run(_run_mcp(info, tool_name, tool_arguments))

async def _run_mcp(info: dict, tool_name: str, tool_arguments: dict) -> str:
    command = info.get("command")
    args = info.get("args", [])
    
    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=os.environ.copy() # Inherit environment variables so API keys (like TAVILY_API_KEY) are passed
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Check if tool exists
                tools = await session.list_tools()
                tool_exists = any(t.name == tool_name for t in tools.tools)
                if not tool_exists:
                    return f"Error: Tool '{tool_name}' not found on server '{info['type']}'. Available tools: {[t.name for t in tools.tools]}"
                
                result = await session.call_tool(tool_name, tool_arguments)
                
                text_output = ""
                if result.content:
                    for content in result.content:
                        if content.type == "text":
                            text_output += content.text + "\n"
                
                return text_output.strip() or "Tool executed successfully but returned no text output."
    except Exception as e:
        return f"Error connecting to or executing tool on MCP server: {str(e)}"

class InvokeSubagentInput(BaseModel):
    role: str = Field(..., description="The role of the subagent (e.g. 'Server Monitor', 'Web Scraper').")
    prompt: str = Field(..., description="The initial task or instruction for the subagent.")

@tool(args_schema=InvokeSubagentInput)
def invoke_subagent(role: str, prompt: str) -> str:
    """Spawns an autonomous subagent in the background to handle a specific role and prompt."""
    # We will grab a default LLM for the subagent. Ideally, we pass the current one, but for simplicity:
    from backend.main import get_gemini_llm
    llm = get_gemini_llm("gemini-3.5-flash") # Free tier or default
    
    agent_id = swarm.spawn_agent(role, prompt, llm)
    return f"Subagent '{role}' spawned successfully with ID: {agent_id}. It is now running in the background. Use send_message to communicate with it, and check_messages to read its responses."

class SendMessageInput(BaseModel):
    recipient_id: str = Field(..., description="The ID of the subagent to send the message to.")
    message: str = Field(..., description="The message content.")

@tool(args_schema=SendMessageInput)
def send_message(recipient_id: str, message: str) -> str:
    """Send a message to a background subagent."""
    success = asyncio.run(swarm.send_message(recipient_id, message))
    if success:
        return f"Message sent to {recipient_id}."
    return f"Error: Subagent {recipient_id} not found."

class CheckMessagesInput(BaseModel):
    agent_id: str = Field(..., description="Your own agent ID to check messages for. If you are the main agent, use 'main'.")

@tool(args_schema=CheckMessagesInput)
def check_messages(agent_id: str) -> str:
    """Check if you have received any new messages from other agents."""
    msgs = asyncio.run(swarm.get_messages(agent_id))
    if not msgs:
        return "No new messages."
    return "New Messages:\n" + "\n".join(msgs)

GET_ALL_TOOLS = [read_file_tool, list_dir_tool, write_file_tool, execute_shell_tool, execute_mcp_tool, invoke_subagent, send_message, check_messages]
