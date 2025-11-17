"""Monitoring tools for health checks and observability."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HealthMetric:
    """Single health metric."""
    name: str
    value: float
    threshold: float
    unit: str


def check_response_time(response_time_ms: float, threshold_ms: float = 1000) -> str:
    """Check if response time is acceptable."""
    if response_time_ms > threshold_ms * 1.5:
        return "critical"
    elif response_time_ms > threshold_ms:
        return "warning"
    else:
        return "healthy"


def check_error_rate(error_rate: float, threshold: float = 5.0) -> str:
    """Check if error rate is acceptable."""
    if error_rate > threshold * 2:
        return "critical"
    elif error_rate > threshold:
        return "warning"
    else:
        return "healthy"


def check_resource_utilization(utilization: float, threshold: float = 80.0) -> str:
    """Check if resource utilization is acceptable."""
    if utilization > threshold + 10:
        return "critical"
    elif utilization > threshold:
        return "warning"
    else:
        return "healthy"


def aggregate_health_checks(checks: List[str]) -> str:
    """Aggregate multiple health check results."""
    if "critical" in checks:
        return "critical"
    elif "warning" in checks:
        return "warning"
    else:
        return "healthy"
