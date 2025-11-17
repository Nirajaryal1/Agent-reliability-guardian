"""Tests for analysis tools."""

from tools.analysis.pattern_detection import (
    detect_timeout_cascade,
    detect_memory_leak,
    detect_api_rate_limit,
    calculate_anomaly_score
)


def test_detect_timeout_cascade():
    """Test timeout cascade detection."""
    traces = [{"error_type": "timeout"} for _ in range(20)]
    assert detect_timeout_cascade(traces) == True
    
    traces = [{"error_type": "other"} for _ in range(20)]
    assert detect_timeout_cascade(traces) == False


def test_detect_memory_leak():
    """Test memory leak detection."""
    # Increasing memory
    memory_readings = [100, 110, 120, 130, 140, 150, 160, 170]
    assert detect_memory_leak(memory_readings) == True
    
    # Stable memory
    memory_readings = [100, 100, 100, 100, 100, 100]
    assert detect_memory_leak(memory_readings) == False


def test_detect_api_rate_limit():
    """Test API rate limit detection."""
    traces = [{"status_code": 429}]
    assert detect_api_rate_limit(traces) == True
    
    traces = [{"status_code": 200}]
    assert detect_api_rate_limit(traces) == False


def test_calculate_anomaly_score():
    """Test anomaly score calculation."""
    # Normal value
    score = calculate_anomaly_score(100, 100, 10)
    assert score == 0.0
    
    # 2 std devs away
    score = calculate_anomaly_score(120, 100, 10)
    assert score == 2.0
    
    # 3 std devs away
    score = calculate_anomaly_score(130, 100, 10)
    assert score == 3.0
