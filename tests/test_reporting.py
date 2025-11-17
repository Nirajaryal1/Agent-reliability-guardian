"""Tests for reporting tools."""

from tools.reporting.audit_trail import (
    AuditTrail,
    calculate_sla_compliance,
    generate_reliability_score
)


def test_audit_trail():
    """Test audit trail logging."""
    trail = AuditTrail()
    
    event_id = trail.log("test_event", "test_actor", "test details")
    assert event_id is not None
    
    entries = trail.get_entries()
    assert len(entries) == 1
    assert entries[0]["event_type"] == "test_event"
    assert entries[0]["actor"] == "test_actor"


def test_sla_compliance():
    """Test SLA compliance calculation."""
    result = calculate_sla_compliance(728, 99.7)
    assert result["compliant"] == True
    
    result = calculate_sla_compliance(700, 99.7)
    assert result["compliant"] == False


def test_generate_reliability_score():
    """Test reliability score generation."""
    # Good performance: low error rate, high uptime, fast response
    result = generate_reliability_score(0.5, 99.7, 300, 1000)
    assert result["score"] >= 75
    assert result["grade"] in ["A", "B", "C", "D"]
    
    # Poor performance: high error rate, lower uptime, slower response
    result = generate_reliability_score(8.0, 95.0, 2000, 1000)
    assert result["score"] < 85
