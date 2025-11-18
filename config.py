"""Configuration management for Agent Reliability Guardian."""

import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional


# Load environment variables from .env file
load_dotenv()


@dataclass
class MonitoringConfig:
    """Configuration for monitoring settings."""
    response_time_threshold_ms: int = 1000
    error_rate_threshold_percent: float = 5.0
    cpu_threshold_percent: float = 80.0
    memory_threshold_percent: float = 85.0
    check_interval_seconds: int = 60


@dataclass
class RecoveryConfig:
    """Configuration for recovery settings."""
    enable_circuit_breaker: bool = True
    circuit_breaker_threshold_errors: int = 10
    circuit_breaker_timeout_seconds: int = 60
    enable_automatic_rollback: bool = True
    enable_state_restoration: bool = True
    max_recovery_attempts: int = 3


@dataclass
class ComplianceConfig:
    """Configuration for compliance and auditing."""
    enable_audit_logging: bool = True
    enable_immutable_logs: bool = True
    sla_target_uptime_percent: float = 99.7
    sla_check_interval_minutes: int = 60
    retention_days: int = 90


@dataclass
class Config:
    """Main configuration class."""
    
    # Google Cloud settings
    google_api_key: Optional[str] = None
    google_cloud_project: Optional[str] = None
    
    # Monitoring
    monitoring: MonitoringConfig = None
    
    # Recovery
    recovery: RecoveryConfig = None
    
    # Compliance
    compliance: ComplianceConfig = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def __post_init__(self):
        """Initialize nested config objects if not provided."""
        if self.monitoring is None:
            self.monitoring = MonitoringConfig()
        if self.recovery is None:
            self.recovery = RecoveryConfig()
        if self.compliance is None:
            self.compliance = ComplianceConfig()
        
        # Load from environment variables
        self.google_api_key = os.getenv("GOOGLE_API_KEY", self.google_api_key)
        self.google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT", self.google_cloud_project)
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)


# Create global config instance
config = Config()
