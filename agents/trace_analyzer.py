"""Loop-based trace analyzer agent for identifying failure patterns."""

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
class TracePattern:
    """Identified pattern in trace data."""
    pattern_name: str
    frequency: int
    severity: str  # "low", "medium", "high", "critical"
    first_occurrence: str
    last_occurrence: str
    affected_operations: List[str]
    recommendation: str

# --- Tool Definitions ---

def analyze_traces(agent_name: str) -> str:
    """
    Analyzes traces for a specific agent to identify failure patterns.
    
    Args:
        agent_name: The name of the agent to analyze.
    """
    logger.info(f"Starting trace analysis for: {agent_name}")
    
    # Simulate iterative trace analysis
    patterns = [
        TracePattern(
            pattern_name="timeout_cascade",
            frequency=28,
            severity="critical",
            first_occurrence="2025-11-17T10:15:00Z",
            last_occurrence="2025-11-17T14:45:00Z",
            affected_operations=["api_call_1", "api_call_2", "retry_handler"],
            recommendation="Implement circuit breaker pattern with exponential backoff"
        ),
        TracePattern(
            pattern_name="memory_leak_in_cache",
            frequency=12,
            severity="high",
            first_occurrence="2025-11-17T09:00:00Z",
            last_occurrence="2025-11-17T15:30:00Z",
            affected_operations=["cache_manager", "object_serialization"],
            recommendation="Review cache eviction policy and add memory monitoring"
        ),
        TracePattern(
            pattern_name="external_api_rate_limit",
            frequency=45,
            severity="high",
            first_occurrence="2025-11-17T08:30:00Z",
            last_occurrence="2025-11-17T15:45:00Z",
            affected_operations=["external_service_client"],
            recommendation="Implement rate limiting and request queuing"
        )
    ]
    
    results = {
        "analysis_type": "iterative_trace_analysis",
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "iterations_completed": 5,
        "traces_analyzed": 147,
        "patterns_detected": [
            {
                "pattern_name": pattern.pattern_name,
                "frequency": pattern.frequency,
                "severity": pattern.severity,
                "first_occurrence": pattern.first_occurrence,
                "last_occurrence": pattern.last_occurrence,
                "affected_operations": pattern.affected_operations,
                "recommendation": pattern.recommendation
            }
            for pattern in patterns
        ],
        "critical_patterns": sum(1 for p in patterns if p.severity == "critical"),
        "high_patterns": sum(1 for p in patterns if p.severity == "high"),
        "analysis_complete": True
    }
    
    logger.info(f"Trace analysis complete: Found {len(patterns)} patterns")
    return json.dumps(results, indent=2)

# --- Agent Definition ---

trace_tool = FunctionTool(analyze_traces)

# Create singleton instance
trace_analyzer = Agent(
    name="trace_analyzer",
    model="gemini-2.0-flash",
    instruction="""
    You are the Trace Analyzer Agent.
    Your job is to analyze execution traces.
    Use the `analyze_trace` tool to perform the analysis.
    """,
    tools=[trace_tool]
)

# Compatibility class
class TraceAnalyzerAgent:
    def __new__(cls):
        return trace_analyzer

# Backwards-compatible alias for imports that expect a different name
trace_analyzer_agent = trace_analyzer

async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=trace_analyzer)
    
    from google.genai.types import Content, Part

    # Create a session first
    await runner.session_service.create_session(user_id="ops_team", session_id="demo_session", app_name="InMemoryRunner")

    async for event in runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message=Content(role="user", parts=[Part(text="Analyze traces for ProductionChatAgent")])
    ):
        parsed = parse_adk_event(event)
        print(to_json(parsed))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
