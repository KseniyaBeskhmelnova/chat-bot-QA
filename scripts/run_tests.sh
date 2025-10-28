#!/bin/bash

echo "🔧 Setting up development environment"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

source .venv/bin/activate

echo "🆙 Upgrading pip and installing development tools"
pip install --upgrade pip
pip install python-dotenv black ruff pytest

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "📦 Project dependencies installed"
else
    echo "⚠️ requirements.txt not found"
fi

echo "💾 Saving current package list"
pip freeze > requirements.txt

echo "🎨 Formatting code with Black"
black .

echo "🧹 Linting and fixing code with Ruff"
ruff check . --fix

echo "🧪 Running tests"
PYTHONPATH=. pytest tests/ -v

echo "✨ Development setup complete"