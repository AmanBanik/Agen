# Local Offline LLM Provider (Ollama / Gemma Support)
import httpx
import os
from typing import List, Dict, Any, Optional

DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_LOCAL_MODEL = os.getenv("DEFAULT_LOCAL_MODEL", "gemma:7b")

async def list_local_models(base_url: str = DEFAULT_OLLAMA_URL) -> List[Dict[str, Any]]:
    """Fetch installed local models from Ollama API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(f"{base_url}/api/tags")
            if res.status_code == 200:
                data = res.json()
                return data.get("models", [])
            return []
    except Exception:
        return []

async def call_local_llm(
    messages: List[Any],
    model: Optional[str] = None,
    base_url: str = DEFAULT_OLLAMA_URL
) -> str:
    """Execute chat completion against local Ollama instance (Gemma, Llama, etc.)"""
    target_model = model or DEFAULT_LOCAL_MODEL
    
    # Convert LangChain / internal message objects to Ollama API format
    ollama_messages = []
    for msg in messages:
        role = "user"
        content = ""
        
        if hasattr(msg, "type"):
            if msg.type == "system":
                role = "system"
            elif msg.type == "human" or msg.type == "user":
                role = "user"
            elif msg.type == "ai" or msg.type == "assistant":
                role = "assistant"
            content = msg.content
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
        else:
            content = str(msg)
            
        if isinstance(content, list):
            # Handle multimodal text parts if present
            text_parts = [item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"]
            content = "\n".join(text_parts)
        elif not isinstance(content, str):
            content = str(content)
            
        if content.strip():
            ollama_messages.append({"role": role, "content": content})

    payload = {
        "model": target_model,
        "messages": ollama_messages,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        res = await client.post(f"{base_url}/api/chat", json=payload)
        res.raise_for_status()
        data = res.json()
        
        msg_obj = data.get("message", {})
        response_text = msg_obj.get("content", "")
        return response_text.strip()
