# 🚀 Quick Start Guide

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed  
- Docker Desktop (optional, for containerized deployment)
- API Keys (see .env.example)

## Step 1: Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the backend
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The app will open at: http://localhost:3000

## Step 3: Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Start Planning Your Trip"
3. Describe your dream trip (e.g., "Plan a 7-day cultural trip to Japan in autumn on a moderate budget")
4. Click "Generate Itinerary"
5. View your personalized travel plan!

## Docker Deployment (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Troubleshooting

### Backend won't start
- Ensure all API keys are set in .env
- Check Python version: `python --version` (should be 3.10+)
- Try: `pip install --upgrade pip setuptools wheel`

### Frontend won't start  
- Check Node version: `node --version` (should be 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`

### API Connection Errors
- Verify backend is running on port 8000
- Check CORS settings in backend/main.py
- Ensure REACT_APP_API_URL is set correctly

## Next Steps

- Explore the API documentation at /docs
- Try different travel queries
- Export itineraries as PDF, iCal, or interactive maps
- Save trips by providing your email

## Need Help?

Check AGENTS.md for full documentation and architecture details.
