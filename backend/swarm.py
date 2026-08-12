import asyncio
import uuid
from typing import Dict, Any

class SwarmManager:
    def __init__(self):
        self.active_agents: Dict[str, asyncio.Task] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.agent_results: Dict[str, str] = {}

    def spawn_agent(self, role: str, prompt: str, llm: Any) -> str:
        agent_id = f"{role.replace(' ', '_').lower()}_{str(uuid.uuid4())[:8]}"
        self.message_queues[agent_id] = asyncio.Queue()
        
        # We will circular import run_autonomous_agent, so we pass a callback or wrap it
        from backend.agent import run_autonomous_agent
        from langchain_core.messages import SystemMessage, HumanMessage
        
        messages = [
            SystemMessage(content=f"You are a Subagent with the role: {role}. You can communicate via tools. Your initial task is: {prompt}"),
            HumanMessage(content=prompt)
        ]
        
        async def agent_task():
            try:
                async for chunk in run_autonomous_agent(llm, messages, is_subagent=True, agent_id=agent_id):
                    pass
                self.agent_results[agent_id] = "Completed"
            except Exception as e:
                self.agent_results[agent_id] = f"Error: {str(e)}"
                
        self.active_agents[agent_id] = asyncio.create_task(agent_task())
        return agent_id

    async def send_message(self, recipient_id: str, message: str):
        if recipient_id in self.message_queues:
            await self.message_queues[recipient_id].put(message)
            return True
        return False
        
    async def get_messages(self, agent_id: str):
        if agent_id not in self.message_queues:
            return []
        
        msgs = []
        q = self.message_queues[agent_id]
        while not q.empty():
            msgs.append(q.get_nowait())
        return msgs

swarm = SwarmManager()
