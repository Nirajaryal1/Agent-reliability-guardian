"""Analysis tools for pattern detection and anomaly identification."""

from typing import List, Dict


def detect_timeout_cascade(traces: List[Dict]) -> bool:
    """Detect timeout cascade pattern in traces."""
    timeout_count = sum(1 for t in traces if t.get("error_type") == "timeout")
    return timeout_count > len(traces) * 0.1  # More than 10% timeouts


def detect_memory_leak(memory_readings: List[float]) -> bool:
    """Detect memory leak pattern."""
    if len(memory_readings) < 2:
        return False
    
    # Check if memory is consistently increasing
    increases = sum(1 for i in range(1, len(memory_readings))
                   if memory_readings[i] > memory_readings[i-1])
    return increases > len(memory_readings) * 0.7


def detect_api_rate_limit(traces: List[Dict]) -> bool:
    """Detect external API rate limiting."""
    rate_limit_count = sum(1 for t in traces if t.get("status_code") == 429)
    return rate_limit_count > 0


def calculate_anomaly_score(current_value: float, mean: float, std_dev: float) -> float:
    """Calculate anomaly score (standard deviations from mean)."""
    if std_dev == 0:
        return 0.0
    return abs(current_value - mean) / std_dev
