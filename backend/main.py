import os
import json
import asyncio
from typing import AsyncGenerator, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from backend.rag import index_directory, get_rag_context
from backend.agent import run_autonomous_agent

# V2: Load environment robustly
env_path = os.path.join(os.path.dirname(__file__), ".env")
home_env = os.path.expanduser("~/.agent_env")
if os.path.exists(home_env):
    load_dotenv(dotenv_path=home_env)
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Terminal Agent V2 Backend (Streaming & Autonomous)")

def get_gemini_llm(model_name: str = "gemini-3.5-flash"):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        home_env = os.path.expanduser("~/.agent_env")
        if os.path.exists(home_env):
            load_dotenv(dotenv_path=home_env, override=True)
            api_key = os.getenv("GEMINI_API_KEY")
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if not api_key and os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path, override=True)
            api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured! Run 'agen key <KEY>' to set it.")
    return ChatGoogleGenerativeAI(model=model_name, api_key=api_key)

class ChatRequest(BaseModel):
    prompt: str
    task_type: str = "light"
    system_context: str = ""
    session_id: str = "default"
    provider: str = "gemini"
    model: Optional[str] = None

class IndexRequest(BaseModel):
    directory: str

import traceback

@app.post("/index_repo")
async def index_repo_endpoint(req: IndexRequest):
    try:
        chunks = index_directory(req.directory)
        return {"status": "success", "chunks_indexed": chunks}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream_chat")
async def stream_chat_endpoint(req: ChatRequest):
    """V2 SSE Streaming endpoint"""
    async def sse_generator() -> AsyncGenerator[str, None]:
        try:
            messages = []
            
            # Fetch semantic context from RAG!
            rag_context = get_rag_context(req.prompt)
            final_system_context = req.system_context
            if rag_context:
                final_system_context += f"\n\n{rag_context}"
                
            if final_system_context:
                messages.append(SystemMessage(content=final_system_context))
            messages.append(HumanMessage(content=req.prompt))
            
            if req.provider in ("ollama", "local"):
                from langchain_community.chat_models import ChatOllama
                model_str = req.model or "llama3"
                llm = ChatOllama(model=model_str)
                
                if req.task_type == "tough":
                    async for chunk in run_autonomous_agent(llm, messages):
                        yield chunk
                else:
                    async for chunk in llm.astream(messages):
                        content = chunk.content
                        if isinstance(content, list):
                            content = "".join([i.get("text", "") for i in content if isinstance(i, dict)])
                        elif not isinstance(content, str):
                            content = str(content)
                        if content:
                            yield f"data: {json.dumps({'type': 'text', 'content': content})}\n\n"
                    yield "data: [DONE]\n\n"
            else:
                model_str = "gemini-3.5-flash" if req.task_type == "tough" else "gemini-3.1-flash-lite"
                llm = get_gemini_llm(model_str)
                
                if req.task_type == "tough":
                    # Autonomous Mode (Agent Loop)
                    async for chunk in run_autonomous_agent(llm, messages):
                        yield chunk
                else:
                    # Standard Chat Mode
                    async for chunk in llm.astream(messages):
                        content = chunk.content
                        if isinstance(content, list):
                            content = "".join([i.get("text", "") for i in content if isinstance(i, dict)])
                        elif not isinstance(content, str):
                            content = str(content)
                            
                        if content:
                            payload = json.dumps({"type": "text", "content": content})
                            yield f"data: {payload}\n\n"
                            
                    yield "data: [DONE]\n\n"
        except Exception as e:
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
