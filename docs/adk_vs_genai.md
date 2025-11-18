# ADK vs google-genai: When to use which

This short guide explains the recommended pattern for using the Google ADK (`google.adk`) and
the lower-level Generative AI client (`google.genai.Client`) in this repository.

Goals
- Avoid confusion about which client to use where.
- Keep orchestration and agent lifecycle code isolated to the ADK.
- Use the genai Client for direct single-shot model calls (not agent orchestration).

Recommended patterns

1. Agents & Orchestration — `google.adk`

- Use `google.adk.Agent`, `FunctionTool`, and `InMemoryRunner` (or other ADK runners) for building
  multi-agent workflows, tool invocation, sessions, and long-running agent logic.
- Agent modules in `agents/` should depend on `google.adk` only for agent definitions and runners.
- Agents should expose a singleton `Agent` and, optionally, a compatibility alias (e.g., `orchestrator_agent`).

2. Direct Model Calls — `google.genai.Client`

- Use `google.genai.Client` for ad-hoc, single-request model calls (e.g., in notebooks, utility scripts,
  or places where you don't need the full ADK agent lifecycle).
- Keep these uses in the demo notebook (`Agent_Reliability_Guardian_Demo.ipynb`) and tooling scripts that
  do one-off generation, evaluation, or scoring.

3. Shared utilities

- Centralize `google.genai.Client` creation in a single factory helper so credentials and config
  are handled consistently across the repo.
- Prefer to call the client factory from notebooks and scripts, and avoid constructing clients inside
  agent modules (agents should focus on agent logic using ADK APIs).

Implementation notes for this repo

- Agents: `agents/*` use `google.adk` and `InMemoryRunner` for local runs and testing.
- Notebooks and demo scripts: use `google.genai.Client` for single-shot evaluations and the red-team/judge
  pipeline where agent sessions are not required.
- A small helper `tools/clients.py` provides `get_genai_client()` so notebooks/scripts can import it
  and avoid duplicating environment parsing.

When to move code between libraries

- If you need session management, tool routing, or functions-as-tools behavior, migrate the logic into
  an ADK Agent module.
- If you only need to call the model once (no tools, no sessions), use `google.genai.Client`.

Security and operational notes

- Do not store API keys in code. Use environment variables (e.g., `GOOGLE_API_KEY`) or secret managers.
- If moving client creation into production, add retry/backoff and request tracing as appropriate.

Examples

Agent-only (ADK):
```py
from google.adk import Agent
from google.adk.tools import FunctionTool
```

One-off model call (genai client):
```py
from tools.clients import get_genai_client
client = get_genai_client()
response = client.aio.models.generate_content(...)
```

This document serves as the single source of truth for future contributors.
