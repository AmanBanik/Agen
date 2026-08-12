import json
import asyncio
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.tools import GET_ALL_TOOLS
from backend.mcp_registry import format_mcp_context, get_all_servers

def get_agent_system_prompt() -> str:
    mcp_context = format_mcp_context(list(get_all_servers().keys()))
    
    return f"""You are Agen, a highly capable autonomous AI Engineering CLI assistant.
You have access to native tools for reading/writing files and executing shell commands.
You ALSO have access to a vast registry of external tools via the Model Context Protocol (MCP).
Use the 'execute_mcp_tool' to dynamically spin up an MCP server, execute a tool on it, and retrieve the result.

{mcp_context}

When asked a task, plan out the steps required.
Use your tools to gather information, execute code, and write files.
Always answer directly and concisely. Ensure your output is cleanly formatted."""

async def run_autonomous_agent(llm, messages, is_subagent=False, agent_id=None) -> AsyncGenerator[str, None]:
    """
    Runs a ReAct-style loop manually, streaming output and tool executions.
    """
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(GET_ALL_TOOLS)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", get_agent_system_prompt()),
        ("placeholder", "{messages}")
    ])
    
    max_iterations = 15
    iterations = 0
    
    while iterations < max_iterations:
        iterations += 1
        
        # We will collect the full response to check for tool calls
        # while simultaneously yielding text chunks to the frontend.
        full_msg = None
        
        try:
            # Stream the LLM response
            formatted_messages = prompt_template.invoke({"messages": messages})
            async for chunk in llm_with_tools.astream(formatted_messages):
                if full_msg is None:
                    full_msg = chunk
                else:
                    full_msg += chunk
                
                # Yield text content
                if chunk.content:
                    text = chunk.content
                    if isinstance(text, list):
                        text = "".join([i.get("text", "") for i in text if isinstance(i, dict)])
                    elif not isinstance(text, str):
                        text = str(text)
                    if text:
                        yield f"data: {json.dumps({'type': 'text', 'content': text})}\n\n"
                        
            messages.append(full_msg)
            
            # If no tools were called, we are done!
            if not full_msg.tool_calls:
                break
                
            # If tools were called, execute them
            for tool_call in full_msg.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                # Notify frontend that a tool is starting
                yield f"data: {json.dumps({'type': 'tool_start', 'tool_name': tool_name, 'tool_args': tool_args})}\n\n"
                
                # Find the tool
                tool_instance = next((t for t in GET_ALL_TOOLS if t.name == tool_name), None)
                if not tool_instance:
                    result = f"Error: Tool {tool_name} not found."
                else:
                    try:
                        # Execute the tool synchronously for simplicity
                        result = tool_instance.invoke(tool_args)
                    except Exception as e:
                        result = f"Error executing tool: {str(e)}"
                
                # Append result to messages so the LLM can observe it
                messages.append(ToolMessage(content=str(result), tool_call_id=tool_id))
                
                # Notify frontend that tool finished
                yield f"data: {json.dumps({'type': 'tool_end', 'tool_name': tool_name, 'result': str(result)})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
            break
            
    yield "data: [DONE]\n\n"
