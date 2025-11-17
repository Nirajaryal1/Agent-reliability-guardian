"""Compatibility layer for Google ADK imports."""

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExecutionContext:
    """Mock ExecutionContext for ADK agents."""
    user_id: str = "default_user"
    session_id: str = "default_session"
    user_message: str = ""


class Agent:
    """Base Agent class for ADK compatibility."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def execute(self, context: ExecutionContext) -> str:
        """Execute the agent."""
        return f"Agent {self.name} executed"


class InMemoryRunner:
    """Mock InMemoryRunner for testing."""
    
    def __init__(self, agent: Agent):
        self.agent = agent
    
    async def run_async(
        self,
        user_id: str = "default_user",
        session_id: str = "default_session",
        new_message: str = ""
    ) -> str:
        """Run the agent asynchronously."""
        context = ExecutionContext(
            user_id=user_id,
            session_id=session_id,
            user_message=new_message
        )
        return await self.agent.execute(context)
