"""Tests for monitoring tools."""

from tools.monitoring.health_check import (
    check_response_time,
    check_error_rate,
    check_resource_utilization,
    aggregate_health_checks
)


def test_check_response_time():
    """Test response time checking."""
    assert check_response_time(500) == "healthy"
    assert check_response_time(1200) == "warning"
    assert check_response_time(1600) == "critical"


def test_check_error_rate():
    """Test error rate checking."""
    assert check_error_rate(2.0) == "healthy"
    assert check_error_rate(6.0) == "warning"
    assert check_error_rate(12.0) == "critical"


def test_check_resource_utilization():
    """Test resource utilization checking."""
    assert check_resource_utilization(60) == "healthy"
    assert check_resource_utilization(82) == "warning"
    assert check_resource_utilization(92) == "critical"


def test_aggregate_health_checks():
    """Test aggregating health checks."""
    assert aggregate_health_checks(["healthy", "healthy"]) == "healthy"
    assert aggregate_health_checks(["healthy", "warning"]) == "warning"
    assert aggregate_health_checks(["healthy", "critical"]) == "critical"
    assert aggregate_health_checks(["warning", "critical"]) == "critical"
