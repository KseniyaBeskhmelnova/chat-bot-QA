#!/bin/bash

echo "🚀 Starting Telegram bot with full initialization"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "📦 Created new virtual environment"
fi

source .venv/bin/activate

pip install --upgrade pip
pip install python-dotenv black ruff pytest

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "📥 Installed project dependencies"
fi

pip freeze > requirements.txt

black .
ruff check . --fix

if [ -d "tests" ]; then
    echo "🧪 Executing test suite"
    PYTHONPATH=. pytest tests/ -v
fi

echo "🗃️ Initializing database"
PYTHONPATH=. python3 bot/recreate_database_postgres.py

echo "🤖 Launching bot"
PYTHONPATH=. python3 -m bot
