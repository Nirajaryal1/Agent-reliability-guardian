"""Report generation agent for audit trails and compliance."""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta

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

# --- Tool Definitions ---

def generate_report(agent_name: str) -> str:
    """
    Generates a comprehensive reliability report for a specific agent.
    
    Args:
        agent_name: The name of the agent to report on.
    """
    logger.info(f"Generating report for: {agent_name}")
    
    report = {
        "report_type": "comprehensive_reliability_assessment",
        "report_id": "rpt_2025_11_17_001",
        "generated_at": datetime.now().isoformat(),
        "period": {
            "start": (datetime.now() - timedelta(days=7)).isoformat(),
            "end": datetime.now().isoformat(),
            "duration_days": 7
        },
        "agent": agent_name,
        "executive_summary": {
            "overall_reliability_score": 96.5,
            "grade": "A",
            "status": "healthy",
            "incidents": 2,
            "mean_time_to_recovery": "2m 15s",
            "uptime_percent": 99.7
        },
        "detailed_metrics": {
            "availability": {
                "uptime_hours": 167.4,
                "downtime_hours": 0.6,
                "uptime_percent": 99.64,
                "sla_target": 99.7,
                "sla_compliant": False
            },
            "performance": {
                "avg_response_time_ms": 287,
                "p95_response_time_ms": 612,
                "p99_response_time_ms": 1245,
                "max_response_time_ms": 3421
            },
            "reliability": {
                "total_requests": 2847362,
                "successful_requests": 2836841,
                "failed_requests": 10521,
                "error_rate_percent": 0.37,
                "critical_errors": 3,
                "warning_errors": 142
            },
            "resource_utilization": {
                "avg_cpu_percent": 42.3,
                "avg_memory_percent": 58.7,
                "peak_cpu_percent": 89.2,
                "peak_memory_percent": 92.1
            }
        },
        "incident_summary": [
            {
                "incident_id": "inc_001",
                "timestamp": "2025-11-16T14:30:00Z",
                "severity": "high",
                "duration_minutes": 2,
                "root_cause": "External API rate limit",
                "resolution": "Circuit breaker activated, rollback executed",
                "impact": "450 failed requests"
            },
            {
                "incident_id": "inc_002",
                "timestamp": "2025-11-14T09:15:00Z",
                "severity": "medium",
                "duration_minutes": 1,
                "root_cause": "Memory spike in cache",
                "resolution": "Cache eviction policy triggered",
                "impact": "120 failed requests"
            }
        ],
        "sla_compliance": {
            "target_availability": "99.7%",
            "achieved_availability": "99.64%",
            "compliant": False,
            "compliance_percent": 99.94,
            "incidents_violating_sla": 1
        },
        "recommendations": [
            {
                "priority": "high",
                "recommendation": "Implement exponential backoff for external API calls",
                "estimated_impact": "Reduce error rate by 40%"
            },
            {
                "priority": "high",
                "recommendation": "Increase database connection pool size",
                "estimated_impact": "Reduce timeout errors by 60%"
            },
            {
                "priority": "medium",
                "recommendation": "Add distributed tracing for end-to-end observability",
                "estimated_impact": "Reduce MTTR by 50%"
            }
        ],
        "audit_trail": [
            {
                "timestamp": "2025-11-17T15:30:00Z",
                "event": "health_check_completed",
                "actor": "health_check_agent",
                "details": "All metrics within normal range"
            },
            {
                "timestamp": "2025-11-17T14:30:00Z",
                "event": "recovery_executed",
                "actor": "recovery_pipeline_agent",
                "details": "Rollback to v2.2.5 completed successfully"
            },
            {
                "timestamp": "2025-11-17T13:45:00Z",
                "event": "anomaly_detected",
                "actor": "anomaly_detector_agent",
                "details": "High error rate detected: 8.5%"
            }
        ]
    }
    
    logger.info(f"Report generated with {len(report['audit_trail'])} audit entries")
    return json.dumps(report, indent=2)

# --- Agent Definition ---

report_tool = FunctionTool(generate_report)

# Create singleton instance
report_generator = Agent(
    name="report_generator",
    model="gemini-2.0-flash",
    instruction="""
    You are the Report Generator Agent.
    Your job is to generate reliability reports.
    Use the `generate_report` tool to create the report.
    """,
    tools=[report_tool]
)

# Compatibility class
class ReportGeneratorAgent:
    def __new__(cls):
        return report_generator

async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=report_generator)
    
    from google.genai.types import Content, Part

    # Create a session first
    await runner.session_service.create_session(user_id="ops_team", session_id="demo_session", app_name="InMemoryRunner")

    async for event in runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message=Content(role="user", parts=[Part(text="Generate report for ProductionChatAgent")])
    ):
        parsed = parse_adk_event(event)
        print(to_json(parsed))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
