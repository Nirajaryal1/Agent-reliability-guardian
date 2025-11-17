"""Reporting tools for audit trails and compliance."""

from typing import Dict, List, Any
from datetime import datetime


class AuditLog:
    """Immutable audit log entry."""
    
    def __init__(self, event_type: str, actor: str, details: str):
        self.timestamp = datetime.now().isoformat()
        self.event_type = event_type
        self.actor = actor
        self.details = details
        self.event_id = f"evt_{datetime.now().timestamp()}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor": self.actor,
            "details": self.details
        }


class AuditTrail:
    """Immutable audit trail for compliance."""
    
    def __init__(self):
        self.entries: List[AuditLog] = []
    
    def log(self, event_type: str, actor: str, details: str) -> str:
        """Log an event."""
        entry = AuditLog(event_type, actor, details)
        self.entries.append(entry)
        return entry.event_id
    
    def get_entries(self) -> List[Dict[str, Any]]:
        """Get all audit entries."""
        return [entry.to_dict() for entry in self.entries]


def calculate_sla_compliance(uptime_hours: float, target_uptime_percent: float) -> Dict[str, Any]:
    """Calculate SLA compliance metrics."""
    total_hours = 730  # 30 days
    achieved_uptime_percent = (uptime_hours / total_hours) * 100
    
    return {
        "target_uptime_percent": target_uptime_percent,
        "achieved_uptime_percent": round(achieved_uptime_percent, 2),
        "compliant": achieved_uptime_percent >= target_uptime_percent,
        "variance_percent": round(achieved_uptime_percent - target_uptime_percent, 2)
    }


def generate_reliability_score(
    error_rate: float,
    uptime_percent: float,
    response_time_ms: float,
    response_time_target_ms: float = 1000
) -> Dict[str, Any]:
    """Generate reliability score and grade."""
    # Components
    error_component = max(0, 100 - (error_rate * 100))
    uptime_component = uptime_percent
    response_component = min(100, (response_time_target_ms / response_time_ms) * 100)
    
    # Weighted average
    score = (error_component * 0.4) + (uptime_component * 0.4) + (response_component * 0.2)
    
    # Letter grade
    if score >= 95:
        grade = "A"
    elif score >= 90:
        grade = "B"
    elif score >= 80:
        grade = "C"
    elif score >= 70:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "score": round(score, 2),
        "grade": grade,
        "components": {
            "error_rate": round(error_component, 2),
            "uptime": round(uptime_component, 2),
            "response_time": round(response_component, 2)
        }
    }
