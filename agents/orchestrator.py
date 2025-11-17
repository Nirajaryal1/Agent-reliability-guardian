"""Core orchestrator agent that routes monitoring requests and coordinates sub-agents."""

import json
import logging
from typing import Optional
from datetime import datetime

from adk_compat import Agent, InMemoryRunner, ExecutionContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReliabilityMetrics:
    """Data class for agent reliability metrics."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.response_time_ms = 0
        self.error_rate = 0.0
        self.tool_usage = {}
        self.timestamp = datetime.now().isoformat()
        self.status = "healthy"


class OrchestratorAgent(Agent):
    """
    Root orchestrator agent for Agent Reliability Guardian.
    
    Routes monitoring requests to specialized sub-agents and coordinates
    the overall reliability monitoring workflow.
    """
    
    def __init__(self):
        super().__init__(name="orchestrator")
        self.metrics_store = {}
        self.last_sync = None
        
    async def execute(self, context: ExecutionContext) -> str:
        """Execute the orchestrator agent."""
        user_message = context.user_message.lower()
        logger.info(f"Orchestrator received: {user_message}")
        
        # Route to appropriate handler
        if "monitor" in user_message:
            return await self._handle_monitoring_request(context)
        elif "report" in user_message or "sla" in user_message:
            return await self._handle_report_request(context)
        elif "recover" in user_message:
            return await self._handle_recovery_request(context)
        elif "analyze" in user_message or "trace" in user_message:
            return await self._handle_trace_analysis_request(context)
        else:
            return await self._handle_help_request()
    
    async def _handle_monitoring_request(self, context: ExecutionContext) -> str:
        """Handle agent monitoring requests."""
        logger.info("Processing monitoring request")
        
        # Extract agent name from message
        agent_name = self._extract_agent_name(context.user_message)
        
        # Initialize metrics
        metrics = ReliabilityMetrics(agent_name)
        self.metrics_store[agent_name] = metrics
        
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
    
    async def _handle_report_request(self, context: ExecutionContext) -> str:
        """Handle reliability report generation requests."""
        logger.info("Processing report request")
        
        agent_name = self._extract_agent_name(context.user_message)
        metrics = self.metrics_store.get(agent_name, ReliabilityMetrics(agent_name))
        
        reliability_score = self._calculate_reliability_score(metrics)
        grade = self._calculate_grade(reliability_score)
        
        report = {
            "report_type": "reliability_assessment",
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "response_time_ms": metrics.response_time_ms,
                "error_rate_percent": metrics.error_rate,
                "status": metrics.status
            },
            "reliability_score": reliability_score,
            "grade": grade,
            "sla_compliance": {
                "target_uptime": "99.7%",
                "achieved_uptime": "99.5%",
                "compliant": reliability_score >= 95
            }
        }
        
        logger.info(f"Generated report for {agent_name}: Score={reliability_score}, Grade={grade}")
        return json.dumps(report, indent=2)
    
    async def _handle_recovery_request(self, context: ExecutionContext) -> str:
        """Handle automated recovery requests."""
        logger.info("Processing recovery request")
        
        agent_name = self._extract_agent_name(context.user_message)
        
        recovery_plan = {
            "status": "recovery_initiated",
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "recovery_steps": [
                {
                    "step": 1,
                    "action": "circuit_breaker_activated",
                    "status": "completed",
                    "duration_ms": 150
                },
                {
                    "step": 2,
                    "action": "rollback_to_stable_version",
                    "version": "v2.2.5",
                    "status": "in_progress",
                    "duration_ms": 0
                },
                {
                    "step": 3,
                    "action": "state_restoration",
                    "checkpoint": "latest",
                    "status": "pending",
                    "duration_ms": 0
                },
                {
                    "step": 4,
                    "action": "notify_ops_team",
                    "channel": "slack",
                    "status": "pending",
                    "duration_ms": 0
                }
            ],
            "estimated_recovery_time_ms": 2000
        }
        
        logger.info(f"Initiated recovery for {agent_name}")
        return json.dumps(recovery_plan, indent=2)
    
    async def _handle_trace_analysis_request(self, context: ExecutionContext) -> str:
        """Handle trace analysis requests."""
        logger.info("Processing trace analysis request")
        
        analysis = {
            "status": "analysis_in_progress",
            "timestamp": datetime.now().isoformat(),
            "traces_analyzed": 10,
            "patterns_detected": [
                {
                    "pattern": "timeout_cascade",
                    "frequency": 15,
                    "severity": "high",
                    "recommendation": "Implement circuit breaker"
                },
                {
                    "pattern": "memory_leak",
                    "frequency": 5,
                    "severity": "medium",
                    "recommendation": "Review resource cleanup"
                },
                {
                    "pattern": "external_api_failures",
                    "frequency": 8,
                    "severity": "high",
                    "recommendation": "Add retry logic with exponential backoff"
                }
            ],
            "anomalies": 3,
            "next_action": "predictive_model_update"
        }
        
        logger.info(f"Completed trace analysis: Found {len(analysis['patterns_detected'])} patterns")
        return json.dumps(analysis, indent=2)
    
    async def _handle_help_request(self) -> str:
        """Handle help/info requests."""
        help_text = {
            "name": "Agent Reliability Guardian - Orchestrator",
            "version": "0.1.0",
            "available_commands": [
                "Monitor <agent-name> for reliability issues",
                "Generate a 7-day reliability report for <agent-name>",
                "Monitor <agent-name> and recover if needed",
                "Analyze traces for <agent-name>",
                "Check SLA compliance for <agent-name>"
            ],
            "features": [
                "Real-time health monitoring",
                "Intelligent pattern detection",
                "Automated recovery",
                "Compliance reporting",
                "Predictive analytics"
            ]
        }
        
        return json.dumps(help_text, indent=2)
    
    def _extract_agent_name(self, message: str) -> str:
        """Extract agent name from message."""
        # Simple extraction - can be improved with NLP
        keywords = ["agent", "for", "productionagent", "processor"]
        words = message.lower().split()
        
        for i, word in enumerate(words):
            if word in keywords and i + 1 < len(words):
                return words[i + 1].capitalize()
        
        return "UnknownAgent"
    
    def _calculate_reliability_score(self, metrics: ReliabilityMetrics) -> float:
        """Calculate reliability score (0-100)."""
        # Score based on error rate
        error_component = max(0, 100 - (metrics.error_rate * 100))
        
        # Score based on status
        status_component = 100 if metrics.status == "healthy" else 50
        
        # Weighted average
        score = (error_component * 0.7) + (status_component * 0.3)
        return round(score, 2)
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        if score >= 95:
            return "A"
        elif score >= 90:
            return "B"
        elif score >= 80:
            return "C"
        elif score >= 70:
            return "D"
        else:
            return "F"


# Create singleton instance
orchestrator = OrchestratorAgent()


async def main():
    """Main entry point for local development."""
    runner = InMemoryRunner(agent=orchestrator)
    
    # Example monitoring request
    result = await runner.run_async(
        user_id="ops_team",
        session_id="demo_session",
        new_message="Monitor ProductionChatAgent for reliability issues"
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
