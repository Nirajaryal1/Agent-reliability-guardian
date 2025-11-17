# Agent Reliability Guardian - Contributing Guide

## Development Setup

### Prerequisites
- Python 3.10+
- Git
- Virtual environment

### Getting Started

```bash
# Clone repository
git clone https://github.com/Nirajaryal1/agent-reliability-guardian.git
cd agent-reliability-guardian

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov

# Set environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Code Style

We follow PEP 8 and use:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

```bash
# Format code
black agents/ tools/ tests/ *.py

# Lint
flake8 agents/ tools/ tests/ *.py

# Type check
mypy agents/ tools/ *.py
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=tools --cov-report=html

# Run specific test file
pytest tests/test_integration.py

# Run async tests
pytest -v tests/ -k "test_orchestrator"
```

## Project Structure

```
agent-reliability-guardian/
├── agents/              # Core agent implementations
├── tools/              # Tool implementations for agents
├── mcp/                # MCP server implementations
├── tests/              # Test suite
├── docs/               # Documentation
├── config.py           # Configuration management
├── utils.py            # Utility functions
└── requirements.txt    # Python dependencies
```

## Adding New Agents

1. Create new file in `agents/` directory
2. Inherit from `google.adk.agents.Agent`
3. Implement `async execute()` method
4. Add tests in `tests/test_*.py`
5. Document in docstring

Example:

```python
import google.adk.agents as agents
from google.adk.context import ExecutionContext

class MyNewAgent(agents.Agent):
    def __init__(self):
        super().__init__(name="my_agent")
    
    async def execute(self, context: ExecutionContext) -> str:
        # Implementation
        return "result"
```

## Adding New Tools

1. Create tool module in `tools/category/`
2. Implement tool functions
3. Add tests in `tests/test_category.py`
4. Update agent to use tool

## Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push to fork: `git push origin feature/my-feature`
4. Open pull request with description
5. Address review comments
6. Merge once approved

## Commit Message Guidelines

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement

Example:
```
feat: Add memory learning to anomaly detector

Implement long-term memory bank for baseline learning
and historical pattern storage.

Closes #123
```

## Documentation

- Update README.md for user-facing changes
- Update docs/ for architecture/deployment changes
- Include docstrings in code
- Add examples for new features

## Performance Considerations

- Keep agent execution time <5 seconds
- Minimize memory footprint
- Batch operations where possible
- Use async/await for I/O operations

## Security

- Never hardcode credentials
- Use environment variables for secrets
- Validate all inputs
- Follow OWASP guidelines
- Update dependencies regularly

## Reporting Issues

Include:
- Python version
- Exact error message
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## Getting Help

- Check existing issues
- Review documentation
- Ask in discussions
- Open issue if stuck

## License

By contributing, you agree your code will be licensed under MIT License.

---

**Thank you for contributing!**
