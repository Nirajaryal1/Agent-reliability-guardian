"""Parallel health check agent for fast monitoring of agent health metrics."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

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
class HealthCheckResult:
    """Result of a single health check."""
    metric_name: str
    value: float
    threshold: float
    status: str  # "healthy", "warning", "critical"
    checked_at: str

# --- Tool Definitions ---

def run_health_checks(agent_name: str) -> str:
    """
    Runs parallel health checks for a specific agent.
    
    Args:
        agent_name: The name of the agent to check.
    """
    logger.info(f"Starting health checks for agent: {agent_name}")
    
    thresholds = {
        "response_time_ms": 1000,
        "error_rate_percent": 5,
        "cpu_percent": 80,
        "memory_percent": 85
    }
    
    # Simulate checks
    checks = [
        HealthCheckResult(
            metric_name="response_time_ms",
            value=350,
            threshold=thresholds["response_time_ms"],
            status="healthy",
            checked_at=datetime.now().isoformat()
        ),
        HealthCheckResult(
            metric_name="error_rate_percent",
            value=1.2,
            threshold=thresholds["error_rate_percent"],
            status="healthy",
            checked_at=datetime.now().isoformat()
        ),
        HealthCheckResult(
            metric_name="cpu_percent",
            value=45,
            threshold=thresholds["cpu_percent"],
            status="healthy",
            checked_at=datetime.now().isoformat()
        ),
        HealthCheckResult(
            metric_name="memory_percent",
            value=62,
            threshold=thresholds["memory_percent"],
            status="healthy",
            checked_at=datetime.now().isoformat()
        )
    ]
    
    # Aggregate results
    critical_count = sum(1 for c in checks if c.status == "critical")
    warning_count = sum(1 for c in checks if c.status == "warning")
    
    if critical_count > 0:
        overall_status = "critical"
    elif warning_count > 0:
        overall_status = "warning"
    else:
        overall_status = "healthy"
        
    results = {
        "check_type": "parallel_health_check",
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "checks": [
            {
                "metric": check.metric_name,
                "value": check.value,
                "threshold": check.threshold,
                "status": check.status,
                "checked_at": check.checked_at
            }
            for check in checks
        ],
        "overall_status": overall_status,
        "total_checks": len(checks),
        "healthy_checks": sum(1 for c in checks if c.status == "healthy"),
        "warning_checks": sum(1 for c in checks if c.status == "warning"),
        "critical_checks": sum(1 for c in checks if c.status == "critical")
    }
    
    logger.info(f"Health check complete: {overall_status}")
    return json.dumps(results, indent=2)

# --- Agent Definition ---

health_check_tool = FunctionTool(run_health_checks)

# Create singleton instance
health_checker = Agent(
    name="health_check",
    model="gemini-2.0-flash",
    instruction="""
    You are the Health Check Agent.
    Your job is to check the health of other agents.
    Use the `check_health` tool to perform the check.
    """,
    tools=[health_check_tool]
)

# Compatibility class
class HealthCheckAgent:
    def __new__(cls):
        return health_checker

# Backwards-compatible alias for imports that expect a different name
health_check_agent = health_checker

async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=health_checker)
    
    from google.genai.types import Content, Part

    # Create a session first
    await runner.session_service.create_session(user_id="ops_team", session_id="demo_session", app_name="InMemoryRunner")

    async for event in runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message=Content(role="user", parts=[Part(text="Check health of ProductionChatAgent")])
    ):
        parsed = parse_adk_event(event)
        print(to_json(parsed))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
