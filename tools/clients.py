"""Client factory helpers for google-genai.

Keep client construction in one place so notebooks and scripts don't duplicate
environment parsing or configuration. This file intentionally does NOT import
the client at module import time in a way that forces network calls.
"""
import os
from typing import Optional

try:
    from google.genai import Client
except Exception:  # pragma: no cover - library may not be installed in some environments
    Client = None  # type: ignore


def get_genai_client(api_key: Optional[str] = None) -> Client:
    """Return a configured `google.genai.Client`.

    Args:
        api_key: optional API key override. If not provided, environment variable
                 `GOOGLE_API_KEY` is used.

    Raises:
        RuntimeError: when the `google.genai` package is not available or API key is missing.
    """
    if Client is None:
        raise RuntimeError("google.genai.Client is not available. Install `google-genai`.")

    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY environment variable is not set")

    return Client(api_key=key)
