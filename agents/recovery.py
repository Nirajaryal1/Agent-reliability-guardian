"""Recovery pipeline agent for automated incident response."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

from dotenv import load_dotenv
load_dotenv()

# Ensure repo root is on Python path so `from utils import ...` works when running modules
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Real ADK imports
from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner

logger = logging.getLogger(__name__)

# Utils
from utils import to_json, parse_adk_event


@dataclass
class RecoveryStep:
    """Single step in the recovery process."""
    step_number: int
    action: str
    status: str  # "pending", "in_progress", "completed", "failed"
    duration_ms: int
    details: str

# --- Tool Definitions ---

def execute_recovery(agent_name: str) -> str:
    """
    Executes the recovery pipeline for a specific agent.
    
    Args:
        agent_name: The name of the agent to recover.
    """
    logger.info(f"Starting recovery pipeline for: {agent_name}")
    
    # Simulate recovery steps
    steps = [
        RecoveryStep(
            step_number=1,
            action="circuit_breaker_activation",
            status="completed",
            duration_ms=150,
            details="Circuit breaker activated to prevent cascade failures"
        ),
        RecoveryStep(
            step_number=2,
            action="rollback_version",
            status="completed",
            duration_ms=2500,
            details="Rolled back to v2.2.5 (previous stable version)"
        ),
        RecoveryStep(
            step_number=3,
            action="restore_state",
            status="completed",
            duration_ms=800,
            details="Restored application state from checkpoint-2025-11-17T14:30:00Z"
        ),
        RecoveryStep(
            step_number=4,
            action="verify_health",
            status="completed",
            duration_ms=1200,
            details="Verified agent health: response_time=250ms, error_rate=0.2%"
        ),
        RecoveryStep(
            step_number=5,
            action="notify_team",
            status="completed",
            duration_ms=300,
            details="Sent incident report to ops_team via Slack and PagerDuty"
        )
    ]
    
    results = {
        "recovery_type": "automated_incident_response",
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "recovery_steps": [
            {
                "step_number": step.step_number,
                "action": step.action,
                "status": step.status,
                "duration_ms": step.duration_ms,
                "details": step.details
            }
            for step in steps
        ],
        "total_recovery_time_ms": sum(step.duration_ms for step in steps),
        "steps_completed": sum(1 for s in steps if s.status == "completed"),
        "recovery_successful": all(s.status == "completed" for s in steps),
        "actions_taken": [step.action for step in steps if step.status == "completed"]
    }
    
    logger.info(f"Recovery pipeline complete: Success={results['recovery_successful']}")
    return json.dumps(results, indent=2)

# --- Agent Definition ---

recovery_tool = FunctionTool(execute_recovery)

# Create singleton instance
recovery_agent = Agent(
    name="recovery_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are the Recovery Agent.
    Your job is to initiate recovery procedures for failing agents.
    Use the `recover_agent` tool to perform the recovery.
    """,
    tools=[recovery_tool]
)

# Compatibility class
class RecoveryPipelineAgent:
    def __new__(cls):
        return recovery_agent

async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=recovery_agent)
    
    from google.genai.types import Content, Part

    # Create a session first
    await runner.session_service.create_session(user_id="ops_team", session_id="demo_session", app_name="InMemoryRunner")

    async for event in runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message=Content(role="user", parts=[Part(text="Recover ProductionChatAgent")])
    ):
        parsed = parse_adk_event(event)
        print(to_json(parsed))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
