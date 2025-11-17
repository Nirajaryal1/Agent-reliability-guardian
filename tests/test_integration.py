"""Integration tests for Agent Reliability Guardian."""

import pytest
from unittest.mock import Mock, patch


class TestOrchestrator:
    """Test orchestrator agent."""
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        from agents.orchestrator import orchestrator
        assert orchestrator is not None
        assert orchestrator.name == "orchestrator"


class TestHealthCheck:
    """Test health check agent."""
    
    def test_health_check_initialization(self):
        """Test health check agent initialization."""
        from agents.health_check import health_check_agent
        assert health_check_agent is not None
        assert health_check_agent.name == "health_check"


class TestTraceAnalyzer:
    """Test trace analyzer agent."""
    
    def test_trace_analyzer_initialization(self):
        """Test trace analyzer initialization."""
        from agents.trace_analyzer import trace_analyzer_agent
        assert trace_analyzer_agent is not None
        assert trace_analyzer_agent.name == "trace_analyzer"


class TestRecoveryPipeline:
    """Test recovery pipeline agent."""
    
    def test_recovery_pipeline_initialization(self):
        """Test recovery pipeline initialization."""
        from agents.recovery import recovery_pipeline_agent
        assert recovery_pipeline_agent is not None
        assert recovery_pipeline_agent.name == "recovery_pipeline"


class TestAnomalyDetector:
    """Test anomaly detector agent."""
    
    def test_anomaly_detector_initialization(self):
        """Test anomaly detector initialization."""
        from agents.anomaly_detector import anomaly_detector_agent
        assert anomaly_detector_agent is not None
        assert anomaly_detector_agent.name == "anomaly_detector"
