"""Parallel health check agent for fast monitoring of agent health metrics."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from adk_compat import Agent, ExecutionContext

logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    metric_name: str
    value: float
    threshold: float
    status: str  # "healthy", "warning", "critical"
    checked_at: str


class HealthCheckAgent(Agent):
    """
    Parallel health check agent for real-time monitoring.
    
    Performs concurrent health checks including:
    - Response time monitoring
    - Error rate tracking
    - Tool usage analysis
    - Resource consumption
    """
    
    def __init__(self):
        super().__init__(name="health_check")
        self.thresholds = {
            "response_time_ms": 1000,  # Critical if > 1s
            "error_rate_percent": 5,   # Critical if > 5%
            "cpu_percent": 80,         # Critical if > 80%
            "memory_percent": 85       # Critical if > 85%
        }
    
    async def execute(self, context: ExecutionContext) -> str:
        """Execute parallel health checks."""
        logger.info(f"Starting health checks for agent: {context.user_message}")
        
        # Simulate parallel health checks
        checks = await self._run_parallel_checks()
        
        # Aggregate results
        results = {
            "check_type": "parallel_health_check",
            "timestamp": datetime.now().isoformat(),
            "agent_name": context.user_message,
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
            "overall_status": self._determine_overall_status(checks),
            "total_checks": len(checks),
            "healthy_checks": sum(1 for c in checks if c.status == "healthy"),
            "warning_checks": sum(1 for c in checks if c.status == "warning"),
            "critical_checks": sum(1 for c in checks if c.status == "critical")
        }
        
        logger.info(f"Health check complete: {results['overall_status']}")
        return json.dumps(results, indent=2)
    
    async def _run_parallel_checks(self) -> List[HealthCheckResult]:
        """Run all health checks in parallel."""
        checks = [
            HealthCheckResult(
                metric_name="response_time_ms",
                value=350,
                threshold=self.thresholds["response_time_ms"],
                status="healthy",
                checked_at=datetime.now().isoformat()
            ),
            HealthCheckResult(
                metric_name="error_rate_percent",
                value=1.2,
                threshold=self.thresholds["error_rate_percent"],
                status="healthy",
                checked_at=datetime.now().isoformat()
            ),
            HealthCheckResult(
                metric_name="cpu_percent",
                value=45,
                threshold=self.thresholds["cpu_percent"],
                status="healthy",
                checked_at=datetime.now().isoformat()
            ),
            HealthCheckResult(
                metric_name="memory_percent",
                value=62,
                threshold=self.thresholds["memory_percent"],
                status="healthy",
                checked_at=datetime.now().isoformat()
            ),
            HealthCheckResult(
                metric_name="request_queue_length",
                value=12,
                threshold=100,
                status="healthy",
                checked_at=datetime.now().isoformat()
            ),
            HealthCheckResult(
                metric_name="active_connections",
                value=42,
                threshold=500,
                status="healthy",
                checked_at=datetime.now().isoformat()
            )
        ]
        
        return checks
    
    def _determine_overall_status(self, checks: List[HealthCheckResult]) -> str:
        """Determine overall health status from individual checks."""
        critical_count = sum(1 for c in checks if c.status == "critical")
        warning_count = sum(1 for c in checks if c.status == "warning")
        
        if critical_count > 0:
            return "critical"
        elif warning_count > 0:
            return "warning"
        else:
            return "healthy"


# Create singleton instance
health_check_agent = HealthCheckAgent()
