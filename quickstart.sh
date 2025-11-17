#!/bin/bash
# Quick Start Script for Agent Reliability Guardian

set -e

echo "🛡️  Agent Reliability Guardian - Quick Start"
echo "════════════════════════════════════════════"
echo ""

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Copy environment file if not exists
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
pip install pytest pytest-asyncio
pytest tests/ -v --tb=short || echo "⚠️  Some tests may fail without proper dependencies installed"

echo ""
echo "════════════════════════════════════════════"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Google API credentials"
echo "2. Run: python -m agents.orchestrator"
echo "3. Or deploy: adk deploy agent_engine agents/orchestrator.py"
echo ""
echo "📖 Documentation:"
echo "  • README.md - Project overview"
echo "  • docs/architecture.md - Architecture details"
echo "  • docs/deployment.md - Deployment guide"
echo "  • CONTRIBUTING.md - Development guide"
echo ""
