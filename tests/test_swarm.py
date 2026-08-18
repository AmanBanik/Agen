import pytest
import asyncio
from backend.swarm import swarm

def test_swarm_messaging():
    """Test the internal queue messaging system used by the Swarm Manager to coordinate subagents."""
    async def run_test():
        # Clean state
        swarm.active_agents.clear()
        swarm.message_queues.clear()
        
        agent_id = "test_agent_123"
        swarm.message_queues[agent_id] = asyncio.Queue()
        
        # Test sending message
        success = await swarm.send_message(agent_id, "Hello Swarm")
        assert success is True
        
        # Test receiving message
        msgs = await swarm.get_messages(agent_id)
        assert len(msgs) == 1
        assert msgs[0] == "Hello Swarm"
        
        # Test receiving when queue is empty
        msgs = await swarm.get_messages(agent_id)
        assert len(msgs) == 0
        
        # Test sending to non-existent agent
        success = await swarm.send_message("fake_agent", "Lost in the void")
        assert success is False
        
    asyncio.run(run_test())
