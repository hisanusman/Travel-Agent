#!/bin/bash

# Script to run the Travel Agent frontend

echo "🚀 Starting Travel Agent Frontend..."

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "✅ Starting server on http://localhost:3000"
npm start
