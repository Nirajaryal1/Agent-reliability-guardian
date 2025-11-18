"""Small helper to run ADK agents locally using InMemoryRunner.

Provides a simple sync wrapper for running an agent with a single user message
and returning parsed ADK events as JSON-friendly dictionaries.
"""
from typing import Any, List, Dict
import asyncio

# Local utils and ADK runner imports are resolved at runtime
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

from utils import parse_adk_event, to_json


async def run_agent_async(agent: Any, message: str, user_id: str = "ops_team", session_id: str = "demo_session", max_events: int = 20) -> List[Dict]:
    """Run an ADK agent once and collect up to `max_events` parsed events.

    Returns a list of parsed event dictionaries.
    """
    runner = InMemoryRunner(agent=agent)

    # Ensure a session exists
    await runner.session_service.create_session(user_id=user_id, session_id=session_id, app_name="InMemoryRunner")

    results: List[Dict] = []
    count = 0

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=Content(role="user", parts=[Part(text=message)])
    ):
        parsed = parse_adk_event(event)
        results.append(parsed)
        count += 1
        if count >= max_events:
            break

    return results


def run_agent(agent: Any, message: str, user_id: str = "ops_team", session_id: str = "demo_session", max_events: int = 20) -> List[Dict]:
    """Synchronous wrapper around `run_agent_async` for convenience in scripts.

    Example:
        from agents.orchestrator import orchestrator
        from agents.runner import run_agent

        events = run_agent(orchestrator, "Monitor PaymentProcessorAgent")
        for ev in events:
            print(to_json(ev))
    """
    return asyncio.run(run_agent_async(agent, message, user_id=user_id, session_id=session_id, max_events=max_events))
