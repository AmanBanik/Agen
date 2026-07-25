import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import json

try:
    from backend.mcp_registry import get_all_servers, get_server_info, format_mcp_context
    from backend.local_provider import list_local_models, call_local_llm
except ImportError:
    from mcp_registry import get_all_servers, get_server_info, format_mcp_context
    from local_provider import list_local_models, call_local_llm
from typing import Optional

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Terminal Agent Backend")

# Initialize models
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Using the available model strings
llm_tough = ChatGoogleGenerativeAI(model="gemini-3.5-flash", api_key=api_key)
llm_light = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", api_key=api_key)

class ChatRequest(BaseModel):
    prompt: str
    task_type: str = "light" # "light" or "tough"
    system_context: str = ""
    session_id: str = "default"
    mcp_servers: list[str] = []
    provider: str = "gemini"
    model: Optional[str] = None

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), ".agent_sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

def get_session_file(session_id: str):
    clean_id = "".join([c for c in session_id if c.isalnum() or c in "-_"]) or "default"
    return os.path.join(SESSIONS_DIR, f"{clean_id}.json")

def load_history(session_id: str):
    path = get_session_file(session_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(session_id: str, history: list):
    path = get_session_file(session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

class ExecRequest(BaseModel):
    prompt: str
    system_context: str = ""
    mcp_servers: list[str] = []
    provider: str = "gemini"
    model: Optional[str] = None

class VisionRequest(BaseModel):
    prompt: str
    image_base64: str
    system_context: str = ""
    mcp_servers: list[str] = []
    provider: str = "gemini"
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        llm = llm_tough if req.task_type == "tough" else llm_light
        
        messages = []
        full_context = req.system_context + format_mcp_context(req.mcp_servers)
        if full_context.strip():
            messages.append(SystemMessage(content=full_context))
            
        history = load_history(req.session_id)
        for item in history:
            if item["role"] == "user":
                messages.append(HumanMessage(content=item["content"]))
            elif item["role"] == "assistant":
                messages.append(AIMessage(content=item["content"]))
                
        messages.append(HumanMessage(content=req.prompt))
        
        if req.provider in ("ollama", "local"):
            content = await call_local_llm(messages, model=req.model)
        else:
            response = llm.invoke(messages)
            content = response.content
            if isinstance(content, list):
                content = "".join([item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"])
            elif not isinstance(content, str):
                content = str(content)
            
        history.append({"role": "user", "content": req.prompt})
        history.append({"role": "assistant", "content": content})
        save_history(req.session_id, history)
        
        return ChatResponse(response=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/sessions")
async def list_sessions():
    sessions = [f[:-5] for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    return {"sessions": sessions}

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    path = get_session_file(session_id)
    if os.path.exists(path):
        os.remove(path)
    return {"status": "cleared"}

@app.get("/mcp")
async def list_mcp_servers():
    return {"servers": get_all_servers()}

@app.get("/mcp/{name}")
async def get_mcp_server(name: str):
    info = get_server_info(name)
    if not info:
        raise HTTPException(status_code=404, detail="MCP server not found in registry")
    return info

@app.get("/local/models")
async def get_local_models():
    models = await list_local_models()
    return {"models": models}

@app.post("/exec", response_model=ChatResponse)
async def exec_endpoint(req: ExecRequest):
    try:
        full_context = req.system_context + format_mcp_context(req.mcp_servers)
        system_msg = SystemMessage(content="You are a python code generator. Write only valid, raw python code. Do not include markdown formatting like ```python. " + full_context)
        messages = [system_msg, HumanMessage(content=req.prompt)]
        
        if req.provider in ("ollama", "local"):
            content = await call_local_llm(messages, model=req.model)
        else:
            response = llm_tough.invoke(messages)
            content = response.content
            if isinstance(content, list):
                content = "".join([item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"])
            elif not isinstance(content, str):
                content = str(content)
            
        if content.startswith("```python"):
            content = content[9:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        return ChatResponse(response=content.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vision", response_model=ChatResponse)
async def vision_endpoint(req: VisionRequest):
    try:
        messages = []
        full_context = req.system_context + format_mcp_context(req.mcp_servers)
        if full_context.strip():
            messages.append(SystemMessage(content=full_context))
        
        human_msg = HumanMessage(
            content=[
                {"type": "text", "text": req.prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"}
                }
            ]
        )
        messages.append(human_msg)
        
        if req.provider in ("ollama", "local"):
            content = await call_local_llm(messages, model=req.model)
        else:
            response = llm_tough.invoke(messages)
            content = response.content
            if isinstance(content, list):
                content = "".join([item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"])
            elif not isinstance(content, str):
                content = str(content)
            
        return ChatResponse(response=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
