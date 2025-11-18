"""Utilities and helper functions for Agent Reliability Guardian."""

import logging
import json
from typing import Any, Dict
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def to_json(data: Any, indent: int = 2) -> str:
    """Convert data to JSON string."""
    return json.dumps(data, cls=JSONEncoder, indent=indent)


def from_json(data: str) -> Any:
    """Parse JSON string to data."""
    return json.loads(data)


class MetricsCollector:
    """Collect and aggregate metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
    
    def record(self, name: str, value: float, metadata: Dict[str, Any] = None):
        """Record a metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append({
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        if name not in self.metrics:
            return {}
        
        values = [m["value"] for m in self.metrics[name]]
        return {
            "count": len(values),
            "mean": sum(values) / len(values) if values else 0,
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
            "last": values[-1] if values else 0
        }


class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(self, failure_threshold: int = 10, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
    
    def record_success(self):
        """Record successful operation."""
        self.failure_count = 0
        self.state = "closed"
    
    def record_failure(self):
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
    
    def is_available(self) -> bool:
        """Check if circuit is available."""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout_seconds:
                    self.state = "half_open"
                    return True
            return False
        
        # half_open state - allow single attempt
        return True


logger = setup_logging()

def parse_adk_event(event) -> Dict[str, Any]:
    """
    Parse an event emitted by the ADK `run_async` loop and return a structured
    dictionary containing the most useful fields (model_version, role, text,
    function_call, function_response, finish_reason, usage). This makes demo
    output and tests easier to inspect.
    """
    out: Dict[str, Any] = {}

    try:
        # model version
        out["model_version"] = getattr(event, "model_version", None)

        content = getattr(event, "content", None)
        if content is None:
            return out

        out["role"] = getattr(content, "role", None)

        # collect text parts
        texts = []
        def _safe(v):
            if v is None or isinstance(v, (str, int, float, bool)):
                return v
            try:
                json.dumps(v)
                return v
            except Exception:
                return str(v)

        for part in getattr(content, "parts", []) or []:
            # function call requested by model
            if hasattr(part, "function_call") and getattr(part, "function_call") is not None:
                fc = part.function_call
                out["function_call"] = {"name": fc.name, "id": fc.id, "args": _safe(fc.args)}
                continue

            # function response from tool
            if hasattr(part, "function_response") and getattr(part, "function_response") is not None:
                fr = part.function_response
                # try to parse result if it's JSON-like
                resp = fr.response if hasattr(fr, "response") else None
                out.setdefault("function_responses", []).append({"id": fr.id, "name": fr.name, "response": _safe(resp)})
                continue

            # text part
            text = getattr(part, "text", None)
            if text:
                texts.append(text)

        if texts:
            out["text"] = "\n".join(texts)

        # finish reason and usage metadata if present
        out["finish_reason"] = getattr(event, "finish_reason", None)
        usage = getattr(event, "usage_metadata", None)
        if usage is not None:
            # usage objects often contain complex non-serializable types; stringify safely
            out["usage"] = _safe(usage)

    except Exception as e:
        out["_parse_error"] = str(e)

    return out
