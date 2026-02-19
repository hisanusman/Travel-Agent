#!/bin/bash

# Script to run the Travel Agent backend

echo "🚀 Starting Travel Agent Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys before continuing."
    exit 1
fi

# Run the backend
echo "✅ Starting server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
