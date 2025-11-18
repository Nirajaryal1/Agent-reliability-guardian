"""Core orchestrator agent that routes monitoring requests and coordinates sub-agents."""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure repo root is on Python path so `from utils import ...` works when running modules
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Real ADK imports
from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utils
from utils import to_json, parse_adk_event

# --- Tool Definitions ---

def monitor_agent(agent_name: str) -> str:
    """
    Starts monitoring for a specific agent and returns initial status.
    
    Args:
        agent_name: The name of the agent to monitor.
    """
    logger.info(f"Processing monitoring request for {agent_name}")
    
    response = {
        "status": "monitoring_started",
        "agent": agent_name,
        "timestamp": datetime.now().isoformat(),
        "checks": [
            "response_time",
            "error_rate",
            "tool_usage",
            "memory_consumption"
        ]
    }
    
    logger.info(f"Started monitoring for {agent_name}")
    return json.dumps(response, indent=2)

def generate_reliability_report(agent_name: str) -> str:
    """
    Generates a reliability report for a specific agent.
    
    Args:
        agent_name: The name of the agent to report on.
    """
    logger.info(f"Processing report request for {agent_name}")
    
    # Mock metrics for now - in production this would query a DB
    metrics = {
        "response_time_ms": 150,
        "error_rate": 0.02,
        "status": "healthy"
    }
    
    reliability_score = 96.5
    grade = "A"
    
    report = {
        "report_type": "reliability_assessment",
        "agent": agent_name,
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "reliability_score": reliability_score,
        "grade": grade,
        "sla_compliance": {
            "target_uptime": "99.7%",
            "achieved_uptime": "99.5%",
            "compliant": True
        }
    }
    
    logger.info(f"Generated report for {agent_name}")
    return json.dumps(report, indent=2)

def initiate_recovery(agent_name: str) -> str:
    """
    Initiates automated recovery for a specific agent.
    
    Args:
        agent_name: The name of the agent to recover.
    """
    logger.info(f"Processing recovery request for {agent_name}")
    
    recovery_plan = {
        "status": "recovery_initiated",
        "agent": agent_name,
        "timestamp": datetime.now().isoformat(),
        "recovery_steps": [
            {"step": 1, "action": "circuit_breaker_activated", "status": "completed"},
            {"step": 2, "action": "rollback_to_stable_version", "status": "in_progress"}
        ],
        "estimated_recovery_time_ms": 2000
    }
    
    logger.info(f"Initiated recovery for {agent_name}")
    return json.dumps(recovery_plan, indent=2)

def analyze_traces(agent_name: str) -> str:
    """
    Analyzes traces for a specific agent to find patterns.
    
    Args:
        agent_name: The name of the agent to analyze.
    """
    logger.info(f"Processing trace analysis request for {agent_name}")
    
    analysis = {
        "status": "analysis_in_progress",
        "timestamp": datetime.now().isoformat(),
        "patterns_detected": [
            {"pattern": "timeout_cascade", "severity": "high"},
            {"pattern": "memory_leak", "severity": "medium"}
        ]
    }
    
    logger.info(f"Completed trace analysis for {agent_name}")
    return json.dumps(analysis, indent=2)

# --- Agent Definition ---

# Create tools
monitor_tool = FunctionTool(monitor_agent)
report_tool = FunctionTool(generate_reliability_report)
recovery_tool = FunctionTool(initiate_recovery)
trace_tool = FunctionTool(analyze_traces)

# Create singleton instance
orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.0-flash",
    instruction="""
    You are the Orchestrator Agent for the Agent Reliability Guardian system.
    Your job is to route user requests to the appropriate tools.
    
    - If the user wants to monitor an agent, use the `monitor_agent` tool.
    - If the user wants a report or SLA check, use the `generate_reliability_report` tool.
    - If the user wants to recover an agent, use the `initiate_recovery` tool.
    - If the user wants to analyze traces, use the `analyze_traces` tool.
    
    Always return the JSON output from the tools directly, or summarize it if requested.
    If the user asks for help, explain your capabilities.
    """,
    tools=[monitor_tool, report_tool, recovery_tool, trace_tool]
)

# Compatibility class
class OrchestratorAgent:
    def __new__(cls):
        return orchestrator

async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=orchestrator)
    
    print("Running Orchestrator Agent...")
    
    # Example monitoring request
    from google.genai.types import Content, Part
    
    # Create a session first
    await runner.session_service.create_session(user_id="ops_team", session_id="demo_session", app_name="InMemoryRunner")

    async for event in runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message=Content(role="user", parts=[Part(text="Monitor ProductionChatAgent for reliability issues")])
    ):
        parsed = parse_adk_event(event)
        print(to_json(parsed))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
