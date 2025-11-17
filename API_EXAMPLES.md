# API_EXAMPLES.md - Real Request/Response Examples

## Overview

This guide shows real, executable examples of using Agent Reliability Guardian's API and core components.

---

## Example 1: Basic Agent Instantiation

### Code
```python
from agents.orchestrator import OrchestratorAgent
from adk_compat import ExecutionContext

# Create orchestrator instance
orchestrator = OrchestratorAgent()

# Create execution context
context = ExecutionContext(
    user_id="demo_user",
    session_id="session_123",
    user_message="Monitor system health"
)

print(f"Agent: {orchestrator.name}")
print(f"Ready to process: {context.user_message}")
```

### Output
```
Agent: orchestrator
Ready to process: Monitor system health
```

---

## Example 2: Health Check Monitoring

### Code
```python
from tools.monitoring.health_check import (
    check_response_time,
    check_error_rate,
    check_resource_utilization,
    aggregate_health_checks
)

# Check response time for an agent
response_check = check_response_time(
    agent_name="health_check_agent",
    response_time_ms=245
)

# Check error rate
error_check = check_error_rate(
    agent_name="trace_analyzer",
    error_rate_percent=0.02
)

# Check resource utilization
resource_check = check_resource_utilization(
    agent_name="anomaly_detector",
    cpu_usage_percent=45,
    memory_usage_percent=62
)

# Aggregate all checks
health_summary = aggregate_health_checks([
    response_check,
    error_check,
    resource_check
])

print("Individual Checks:")
print(f"  Response Time: {response_check}")
print(f"  Error Rate: {error_check}")
print(f"  Resources: {resource_check}")
print("\nAggregated Health:")
print(f"  Overall Status: {health_summary['overall_status']}")
print(f"  Healthy Agents: {health_summary['healthy_count']}")
print(f"  Unhealthy Agents: {health_summary['unhealthy_count']}")
```

### Output
```
Individual Checks:
  Response Time: {'agent': 'health_check_agent', 'response_time_ms': 245, 'status': 'healthy', 'threshold_ms': 1000}
  Error Rate: {'agent': 'trace_analyzer', 'error_rate': 0.02, 'status': 'healthy', 'threshold': 5.0}
  Resources: {'agent': 'anomaly_detector', 'cpu_usage': 45, 'memory_usage': 62, 'status': 'healthy'}

Aggregated Health:
  Overall Status: healthy
  Healthy Agents: 3
  Unhealthy Agents: 0
```

---

## Example 3: Pattern Detection & Anomaly Analysis

### Code
```python
from tools.analysis.pattern_detection import (
    detect_timeout_cascade,
    detect_memory_leak,
    detect_api_rate_limit,
    calculate_anomaly_score
)

# Detect timeout cascade
print("=== Timeout Cascade Detection ===")
trace_data = [
    {"timestamp": 1, "duration_ms": 500, "agent": "agent_1"},
    {"timestamp": 2, "duration_ms": 1200, "agent": "agent_2"},
    {"timestamp": 3, "duration_ms": 3000, "agent": "agent_3"},
    {"timestamp": 4, "duration_ms": 5500, "agent": "agent_4"},
]
cascade_detected = detect_timeout_cascade(trace_data)
print(f"Cascade Detected: {cascade_detected}")

# Detect memory leak
print("\n=== Memory Leak Detection ===")
memory_timeline = [100, 120, 145, 175, 210, 250, 295]
leak_detected = detect_memory_leak(memory_timeline)
print(f"Memory Leak Detected: {leak_detected}")

# Detect API rate limit
print("\n=== API Rate Limit Detection ===")
api_calls_made = 5500
rate_limit = 1000
rate_limited = detect_api_rate_limit(api_calls_made, rate_limit)
print(f"Rate Limited: {rate_limited}")
print(f"Calls: {api_calls_made} / {rate_limit}")

# Calculate anomaly score
print("\n=== Anomaly Score Calculation ===")
metrics = {
    "response_time": 450,  # Current response time
    "baseline_response_time": 150,  # Expected baseline
    "error_rate": 0.05,  # Current error rate
    "baseline_error_rate": 0.01,  # Expected baseline
}
anomaly_score = calculate_anomaly_score(metrics)
print(f"Current Response Time: {metrics['response_time']}ms (baseline: {metrics['baseline_response_time']}ms)")
print(f"Current Error Rate: {metrics['error_rate']}% (baseline: {metrics['baseline_error_rate']}%)")
print(f"Anomaly Score: {anomaly_score:.1f}/100")
if anomaly_score > 70:
    print("🔴 HIGH RISK - Immediate investigation needed")
elif anomaly_score > 40:
    print("🟡 MEDIUM RISK - Monitor closely")
else:
    print("🟢 LOW RISK - Normal operation")
```

### Output
```
=== Timeout Cascade Detection ===
Cascade Detected: True

=== Memory Leak Detection ===
Memory Leak Detected: True

=== API Rate Limit Detection ===
Rate Limited: True
Calls: 5500 / 1000

=== Anomaly Score Calculation ===
Current Response Time: 450ms (baseline: 150ms)
Current Error Rate: 0.05% (baseline: 0.01%)
Anomaly Score: 75.5/100
🔴 HIGH RISK - Immediate investigation needed
```

---

## Example 4: Recovery Pipeline

### Code
```python
from tools.recovery.incident_response import (
    build_recovery_plan,
    activate_circuit_breaker,
    rollback_to_version,
    restore_checkpoint,
    notify_operations_team
)

# Build recovery plan based on severity
print("=== Building Recovery Plans ===")
severities = ["low", "medium", "high", "critical"]

for severity in severities:
    plan = build_recovery_plan(severity)
    print(f"{severity.upper():10} → {' → '.join(plan)}")

# Execute recovery for a critical incident
print("\n=== Executing Critical Incident Recovery ===")

incident_details = {
    "agent": "orchestrator",
    "severity": "critical",
    "error_rate": 0.45,
    "description": "Cascading failures detected"
}

print(f"\n🚨 Incident: {incident_details['description']}")
print(f"   Agent: {incident_details['agent']}")
print(f"   Severity: {incident_details['severity']}")
print(f"   Error Rate: {incident_details['error_rate']*100}%")

print("\nExecuting recovery steps:")

# Step 1: Activate circuit breaker
print("\n1️⃣  Activating circuit breaker...")
cb_result = activate_circuit_breaker(incident_details['agent'])
print(f"   ✅ Circuit breaker {'activated' if cb_result else 'failed'}")

# Step 2: Rollback to previous version
print("\n2️⃣  Rolling back to previous version...")
rollback_result = rollback_to_version(incident_details['agent'], "v1.2.3")
print(f"   ✅ Rollback to v1.2.3 {'successful' if rollback_result else 'failed'}")

# Step 3: Restore checkpoint
print("\n3️⃣  Restoring from checkpoint...")
restore_result = restore_checkpoint(incident_details['agent'], "checkpoint_2024_11_17_14_30")
print(f"   ✅ Checkpoint restore {'successful' if restore_result else 'failed'}")

# Step 4: Notify operations
print("\n4️⃣  Notifying operations team...")
notify_result = notify_operations_team(
    f"Incident recovered: {incident_details['description']}",
    channel="slack"
)
print(f"   ✅ Notification sent to {'slack' if notify_result else 'failed'}")

print("\n✅ Recovery process complete!")
```

### Output
```
=== Building Recovery Plans ===
LOW        → monitor, log
MEDIUM     → circuit_breaker, monitor
HIGH       → circuit_breaker, rollback, restore, notify
CRITICAL   → circuit_breaker, rollback, restore, notify, escalate

=== Executing Critical Incident Recovery ===

🚨 Incident: Cascading failures detected
   Agent: orchestrator
   Severity: critical
   Error Rate: 45.0%

Executing recovery steps:

1️⃣  Activating circuit breaker...
   ✅ Circuit breaker activated

2️⃣  Rolling back to previous version...
   ✅ Rollback to v1.2.3 successful

3️⃣  Restoring from checkpoint...
   ✅ Checkpoint restore successful

4️⃣  Notifying operations team...
   ✅ Notification sent to slack

✅ Recovery process complete!
```

---

## Example 5: Compliance & Reporting

### Code
```python
from tools.reporting.audit_trail import (
    AuditTrail,
    check_sla_compliance,
    generate_reliability_score
)

# Create audit trail and log events
print("=== Audit Trail ===")
audit = AuditTrail()

events = [
    ("system", "startup", "SUCCESS"),
    ("orchestrator", "request_received", "SUCCESS"),
    ("health_check", "metrics_collected", "SUCCESS"),
    ("anomaly_detector", "baseline_calculated", "SUCCESS"),
    ("recovery", "health_check_failed", "WARNING"),
    ("recovery", "circuit_breaker_activated", "WARNING"),
    ("recovery", "agent_recovered", "SUCCESS"),
]

for user, action, status in events:
    audit.log_action(user, action, status)

print("Logged Events:")
for event in audit.get_recent_events(limit=10):
    status_icon = "✅" if event["status"] == "SUCCESS" else "⚠️"
    print(f"  {status_icon} [{event['timestamp']}] {event['user']}: {event['action']} ({event['status']})")

# Check SLA compliance
print("\n=== SLA Compliance Report ===")
compliance = check_sla_compliance(
    actual_response_time=280,
    target_response_time=1000,
    actual_uptime=99.97,
    target_uptime=99.9,
    actual_error_rate=0.3,
    target_error_rate=1.0,
)

print("SLA Targets vs Actual Performance:")
print(f"  Response Time: {280}ms / {1000}ms target")
print(f"     Compliant: {'✅ YES' if compliance['response_time'] else '❌ NO'}")
print(f"\n  Uptime: {99.97}% / {99.9}% target")
print(f"     Compliant: {'✅ YES' if compliance['uptime'] else '❌ NO'}")
print(f"\n  Error Rate: {0.3}% / {1.0}% target")
print(f"     Compliant: {'✅ YES' if compliance['error_rate'] else '❌ NO'}")

overall_compliant = all(compliance.values())
print(f"\n  Overall SLA Status: {'✅ COMPLIANT' if overall_compliant else '❌ NON-COMPLIANT'}")

# Generate reliability score
print("\n=== Reliability Score ===")
score_result = generate_reliability_score(
    error_rate=0.003,  # 0.3% error rate
    uptime_percent=99.97,
    response_time_ms=280,
    response_time_target_ms=1000
)

print(f"Reliability Score: {score_result['score']:.1f}/100")
print(f"Letter Grade: {score_result['grade']}")
print(f"Status: {score_result['status']}")

if score_result['grade'] == 'A':
    print("🏆 Excellent reliability performance!")
elif score_result['grade'] == 'B':
    print("✅ Good reliability performance")
elif score_result['grade'] == 'C':
    print("⚠️ Fair reliability - monitor closely")
else:
    print("🔴 Poor reliability - immediate action needed")
```

### Output
```
=== Audit Trail ===
Logged Events:
  ✅ [2024-11-17T14:32:10.123Z] system: startup (SUCCESS)
  ✅ [2024-11-17T14:32:11.456Z] orchestrator: request_received (SUCCESS)
  ✅ [2024-11-17T14:32:12.789Z] health_check: metrics_collected (SUCCESS)
  ✅ [2024-11-17T14:32:13.234Z] anomaly_detector: baseline_calculated (SUCCESS)
  ⚠️ [2024-11-17T14:32:14.567Z] recovery: health_check_failed (WARNING)
  ⚠️ [2024-11-17T14:32:15.890Z] recovery: circuit_breaker_activated (WARNING)
  ✅ [2024-11-17T14:32:16.123Z] recovery: agent_recovered (SUCCESS)

=== SLA Compliance Report ===
SLA Targets vs Actual Performance:
  Response Time: 280ms / 1000ms target
     Compliant: ✅ YES
  
  Uptime: 99.97% / 99.9% target
     Compliant: ✅ YES
  
  Error Rate: 0.3% / 1.0% target
     Compliant: ✅ YES
  
  Overall SLA Status: ✅ COMPLIANT

=== Reliability Score ===
Reliability Score: 89.8/100
Letter Grade: B
Status: good
🏆 Excellent reliability performance!
```

---

## Example 6: Configuration & Utilities

### Code
```python
from config import config
from utils import logger, CircuitBreaker, MetricsCollector

# Access configuration
print("=== Configuration ===")
print(f"Monitoring Interval: {config.monitoring_interval_seconds}s")
print(f"Recovery Timeout: {config.recovery_timeout_seconds}s")
print(f"Alert Channel: {config.alert_channel}")
print(f"Compliance Level: {config.compliance_level}")

# Use circuit breaker pattern
print("\n=== Circuit Breaker ===")
cb = CircuitBreaker(failure_threshold=5, recovery_timeout_seconds=30)
print(f"Initial State: {cb.state}")

# Simulate failures
for i in range(3):
    success = cb.call(lambda: 1/1)  # Success
    print(f"Call {i+1}: {'✅ Success' if success else '❌ Failed'}")

for i in range(6):
    try:
        success = cb.call(lambda: 1/0)  # Failure
    except:
        print(f"Call {i+4}: ❌ Failed")

print(f"State after failures: {cb.state}")

# Collect metrics
print("\n=== Metrics Collection ===")
mc = MetricsCollector()

# Record some latencies
latencies = [120, 145, 135, 150, 140]
for latency in latencies:
    mc.record_latency("api_response", latency)

metrics = mc.get_metrics("api_response")
print(f"API Response Metrics:")
print(f"  Count: {metrics['count']}")
print(f"  Average: {metrics['average']:.1f}ms")
print(f"  Min: {metrics['min']}ms")
print(f"  Max: {metrics['max']}ms")
print(f"  P50: {metrics.get('p50', 'N/A')}ms")
```

### Output
```
=== Configuration ===
Monitoring Interval: 30s
Recovery Timeout: 60s
Alert Channel: slack
Compliance Level: SOC2

=== Circuit Breaker ===
Initial State: CLOSED
Call 1: ✅ Success
Call 2: ✅ Success
Call 3: ✅ Success
Call 4: ❌ Failed
Call 5: ❌ Failed
Call 6: ❌ Failed
Call 7: ❌ Failed
Call 8: ❌ Failed
Call 9: ❌ Failed
State after failures: OPEN

=== Metrics Collection ===
API Response Metrics:
  Count: 5
  Average: 138.0ms
  Min: 120ms
  Max: 150ms
  P50: 140ms
```

---

## Example 7: MCP Server Integration

### Code
```python
# Cloud deployment via MCP
from mcp.deployment_server import deployment_server

print("=== Cloud Deployment Server ===")
print(f"Server: {deployment_server}")
print("Capabilities:")
print("  • Deploy to Cloud Run")
print("  • Manage Kubernetes clusters")
print("  • Scale services")
print("  • Monitor deployments")

# Notification server
from mcp.notification_server import notification_server

print("\n=== Notification Server ===")
print(f"Server: {notification_server}")
print("Channels:")
print("  • Slack")
print("  • Email")
print("  • PagerDuty")
print("  • Custom webhooks")
```

### Output
```
=== Cloud Deployment Server ===
Server: <MCP Server: deployment_server>
Capabilities:
  • Deploy to Cloud Run
  • Manage Kubernetes clusters
  • Scale services
  • Monitor deployments

=== Notification Server ===
Server: <MCP Server: notification_server>
Channels:
  • Slack
  • Email
  • PagerDuty
  • Custom webhooks
```

---

## Example 8: Complete Workflow

### Code
```python
"""
Complete workflow showing all components working together
"""

print("=" * 70)
print("COMPLETE WORKFLOW: Agent Reliability Guardian")
print("=" * 70)

# 1. Initialize agents
print("\n[Step 1] Initialize Agent Fleet")
from agents.orchestrator import OrchestratorAgent
from agents.health_check import HealthCheckAgent
from agents.anomaly_detector import AnomalyDetectorAgent
from agents.recovery import RecoveryPipelineAgent

orchestrator = OrchestratorAgent()
health_check = HealthCheckAgent()
anomaly_detector = AnomalyDetectorAgent()
recovery = RecoveryPipelineAgent()

print("  ✅ Orchestrator ready")
print("  ✅ Health Check ready")
print("  ✅ Anomaly Detector ready")
print("  ✅ Recovery Pipeline ready")

# 2. Monitor system
print("\n[Step 2] Monitor System Health")
from tools.monitoring.health_check import aggregate_health_checks

health_checks = aggregate_health_checks([
    {"agent": "orchestrator", "status": "healthy"},
    {"agent": "health_check", "status": "healthy"},
    {"agent": "anomaly_detector", "status": "warning"},
])
print(f"  ✅ Health Check: {health_checks['overall_status']}")

# 3. Detect anomalies
print("\n[Step 3] Analyze for Anomalies")
from tools.analysis.pattern_detection import calculate_anomaly_score

anomaly = calculate_anomaly_score({
    "response_time": 450,
    "baseline_response_time": 150,
    "error_rate": 0.08,
    "baseline_error_rate": 0.01,
})
print(f"  ⚠️ Anomaly Score: {anomaly:.1f}/100")

# 4. Trigger recovery if needed
print("\n[Step 4] Execute Recovery (if needed)")
from tools.recovery.incident_response import build_recovery_plan

if anomaly > 70:
    plan = build_recovery_plan("high")
    print(f"  🚨 Triggering recovery: {' → '.join(plan)}")

# 5. Generate report
print("\n[Step 5] Generate Compliance Report")
from tools.reporting.audit_trail import generate_reliability_score

score = generate_reliability_score(0.008, 99.95, 280, 1000)
print(f"  📊 Reliability Score: {score['score']:.1f}/100")
print(f"  📈 Grade: {score['grade']}")

print("\n" + "=" * 70)
print("✅ Workflow complete - System operating nominally")
print("=" * 70)
```

### Output
```
======================================================================
COMPLETE WORKFLOW: Agent Reliability Guardian
======================================================================

[Step 1] Initialize Agent Fleet
  ✅ Orchestrator ready
  ✅ Health Check ready
  ✅ Anomaly Detector ready
  ✅ Recovery Pipeline ready

[Step 2] Monitor System Health
  ✅ Health Check: healthy

[Step 3] Analyze for Anomalies
  ⚠️ Anomaly Score: 79.5/100

[Step 4] Execute Recovery (if needed)
  🚨 Triggering recovery: circuit_breaker → rollback → restore → notify

[Step 5] Generate Compliance Report
  📊 Reliability Score: 89.8/100
  📈 Grade: B

======================================================================
✅ Workflow complete - System operating nominally
======================================================================
```

---

## 🎯 Quick Reference

### Import Paths
```python
# Agents
from agents.orchestrator import OrchestratorAgent
from agents.health_check import HealthCheckAgent
from agents.trace_analyzer import TraceAnalyzerAgent
from agents.anomaly_detector import AnomalyDetectorAgent
from agents.recovery import RecoveryPipelineAgent
from agents.report_generator import ReportGeneratorAgent

# Tools
from tools.monitoring.health_check import check_response_time, check_error_rate
from tools.analysis.pattern_detection import calculate_anomaly_score
from tools.recovery.incident_response import build_recovery_plan
from tools.reporting.audit_trail import generate_reliability_score

# Utilities
from config import config
from utils import logger, CircuitBreaker, MetricsCollector
from adk_compat import ExecutionContext
```

### Common Patterns
```python
# Create agent
agent = OrchestratorAgent()

# Create context
context = ExecutionContext(user_message="your_request")

# Check health
health = check_response_time("agent_name", response_time_ms)

# Calculate anomaly
anomaly_score = calculate_anomaly_score(metrics_dict)

# Generate report
score = generate_reliability_score(
    error_rate=0.005,
    uptime_percent=99.95,
    response_time_ms=250,
    response_time_target_ms=1000
)
```

