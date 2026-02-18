# 🌍 Agentic Travel Planner

An intelligent, conversational travel planning system powered by multi-agent architecture using Google's Agent Development Kit.

## 📋 Project Overview

This application provides an AI-powered travel assistant that can:
- Generate personalized itineraries based on natural language queries
- Create day-by-day travel plans with activities, transportation, and timing
- Provide weather-aware recommendations
- Estimate budgets and optimize costs
- Export itineraries as PDF, iCal, interactive maps, and budget reports
- Support follow-up conversations to refine plans

## 🏗️ Architecture

### Multi-Agent System

The system uses specialized MCP (Model Context Protocol) agents:

1. **Profile Agent** - Manages user preferences, budget, dates, and interests
2. **Destination & Attractions Agent** - Retrieves POIs, attractions, and local tips using RAG
3. **Itinerary Planner Agent** - Creates optimized day-by-day schedules
4. **Weather & Timing Agent** - Provides weather-based recommendations
5. **Budget & Costs Agent** - Estimates costs and optimizes expenses
6. **Decision & Fusion Agent** - Orchestrates agents and consolidates outputs

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React
- **Agent Framework**: Google Agent Development Kit
- **Vector Database**: Pinecone (RAG for travel knowledge)
- **Database**: SQLite (user profiles, trips)
- **Deployment**: Vercel
- **Containerization**: Docker

## 📁 Project Structure

```
TravelAgent/
├── backend/
│   ├── agents/              # MCP agent implementations
│   │   ├── __init__.py
│   │   ├── profile_agent.py
│   │   ├── destination_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── weather_agent.py
│   │   ├── budget_agent.py
│   │   └── orchestrator.py
│   ├── api/                 # FastAPI routes
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── database/            # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── db.py
│   ├── rag/                 # RAG implementation
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   └── retrieval.py
│   ├── exports/             # Export handlers (PDF, iCal, etc.)
│   │   ├── __init__.py
│   │   ├── pdf_export.py
│   │   ├── ical_export.py
│   │   └── map_export.py
│   ├── config.py            # Configuration management
│   └── main.py              # FastAPI application entry
├── frontend/                # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── data/                    # Travel guide data for RAG
│   └── guides/
├── .env.example             # Example environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── vercel.json              # Vercel deployment config
└── AGENTS.md                # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker Desktop (running)

### Backend Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your API keys to .env
```

4. Initialize database:
```bash
python -m backend.database.db
```

5. Run the backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm start
```

## 🔐 Security Notes

- API keys are stored securely in `.env` file (never committed to version control)
- Rate limiting implemented to prevent API abuse
- Input validation on all endpoints
- Environment variables validated on startup

## 📊 Database Schema

### Users Table
- id (primary key)
- email
- preferences (JSON)
- created_at

### Trips Table
- id (primary key)
- user_id (foreign key)
- destination
- start_date
- end_date
- budget
- itinerary (JSON)
- created_at
- updated_at

## 🧪 Testing

Run tests with:
```bash
pytest tests/
```

## 🚢 Deployment

The application is deployed on Vercel with the following configuration:
- Backend: Python serverless functions
- Frontend: Static React build
- Database: Vercel Postgres or external service

Deploy command:
```bash
vercel --prod
```

## 📝 Development Progress

- [x] Project structure created
- [x] Virtual environment and dependencies installed
- [x] Environment configuration with secure API key management
- [x] MCP agent system with Google Agent Development Kit
- [x] RAG backend with Pinecone vector database
- [x] Specialized agents implementation (Profile, Destination, Weather, Budget, Itinerary)
- [x] FastAPI backend with comprehensive API endpoints
- [x] React frontend with beautiful UI
- [x] Export features (PDF, iCal, interactive maps)
- [x] Database setup with SQLAlchemy (SQLite)
- [x] Code structure and syntax validation
- [ ] Full end-to-end testing with real API calls
- [ ] Vercel deployment (ready for deployment)

## 🔄 Version History

### v0.1.0 (Current - February 17, 2026)
- ✅ Complete project structure
- ✅ Multi-agent system with 5 specialized agents
- ✅ RAG backend with Pinecone integration
- ✅ FastAPI REST API with comprehensive endpoints
- ✅ Modern React frontend with responsive design
- ✅ Export functionality (PDF, iCal, Maps)
- ✅ SQLite database for trip storage
- ✅ Docker containerization support
- ✅ Ready for Vercel deployment

## 🚀 Quick Start

See `README_SETUP.md` for detailed setup instructions.

### Quick Commands:

**Backend:**
```bash
./run_backend.sh
```

**Frontend:**
```bash
./run_frontend.sh
```

**Docker:**
```bash
docker-compose up --build
```

## 🌐 API Endpoints

### Core Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/plan` - Create new travel plan
- `PUT /api/v1/plan/update` - Update existing plan
- `POST /api/v1/export` - Export itinerary (PDF/iCal/Map)
- `GET /api/v1/users/{email}` - Get user info
- `GET /api/v1/users/{user_id}/trips` - Get user's trips
- `GET /api/v1/trips/{trip_id}` - Get specific trip
- `DELETE /api/v1/trips/{trip_id}` - Delete trip

Full API documentation available at `/docs` when running the backend.

## 🎨 Features

### Intelligent Planning
- Natural language processing for trip requests
- Multi-agent system for specialized tasks
- RAG-powered destination recommendations
- Weather-aware activity planning
- Budget optimization

### Export Options
- **PDF**: Beautifully formatted itinerary documents
- **iCal**: Import directly into calendar apps
- **Interactive Maps**: View all locations on a map

### User Experience
- Clean, modern interface
- Real-time itinerary generation
- Conversational trip planning
- Mobile-responsive design

## 📊 Agent Architecture

### 1. Profile Agent
- Extracts user preferences from natural language
- Identifies destination, budget, interests, dates
- Maintains conversation context

### 2. Destination Agent
- Retrieves POIs and attractions using RAG
- Provides local experiences and hidden gems
- Recommends restaurants and neighborhoods

### 3. Weather Agent
- Fetches real-time weather forecasts
- Suggests weather-appropriate activities
- Provides packing recommendations

### 4. Budget Agent
- Estimates trip costs
- Breaks down expenses by category
- Suggests cost-saving tips

### 5. Itinerary Agent
- Creates optimized day-by-day schedules
- Minimizes travel time between locations
- Balances activities based on interests
- Provides timing and logistics

### 6. Orchestrator Agent
- Coordinates all specialized agents
- Manages data flow and dependencies
- Consolidates results into final plan
- Handles error recovery

## 🔧 Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Google Generative AI (LLM for agents)
- Pinecone (Vector database for RAG)
- SQLAlchemy (Database ORM)
- ReportLab (PDF generation)
- Folium (Interactive maps)

**Frontend:**
- React 18
- React Router (Navigation)
- Axios (API client)
- Lucide React (Icons)
- Modern CSS with gradients

**Infrastructure:**
- Docker & Docker Compose
- Vercel (Deployment platform)
- SQLite (Development database)

## 🔐 Security Best Practices

- API keys stored in `.env` (never committed)
- Environment variables validated on startup
- Input sanitization on all endpoints
- CORS properly configured
- Rate limiting ready to implement
- Secure database connections

## 📈 Performance Considerations

- Async/await for non-blocking operations
- Parallel agent execution where possible
- Efficient vector similarity search
- Optimized database queries
- Frontend code splitting ready

## 🐛 Known Limitations

- Pinecone index needs to be populated with travel data
- Weather API has rate limits
- Google API may take time to initialize
- Export files stored locally (not in cloud storage yet)

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Trip sharing and collaboration
- [ ] Flight and hotel booking integration
- [ ] Real-time price tracking
- [ ] Multi-destination trip planning
- [ ] Mobile app (React Native)
- [ ] Social features (reviews, photos)
- [ ] AI-powered travel assistant chat

## 🌍 Available Destinations

The system now includes **11 destinations** with full interactive customization:

### European Cities (7)
1. **Amsterdam** 🇳🇱 - 3 hotels, 5 activities, 4 restaurants
2. **Barcelona** 🇪🇸 - 3 hotels, 6 activities, 4 restaurants  
3. **Budapest** 🇭🇺 - 3 hotels, 5 activities, 4 restaurants
4. **London** 🇬🇧 - 3 hotels, 6 activities, 4 restaurants
5. **Madrid** 🇪🇸 - 3 hotels, 6 activities, 4 restaurants
6. **Prague** 🇨🇿 - 3 hotels, 5 activities, 4 restaurants
7. **Rome** 🇮🇹 - 3 hotels, 5 activities, 4 restaurants
8. **Vienna** 🇦🇹 - 3 hotels, 5 activities, 4 restaurants

### Other Destinations (3)
9. **Maldives** 🇲🇻 - 3 resorts, 5 activities, 4 restaurants
10. **Paris** 🇫🇷 - 3 hotels, 5 activities, 4 restaurants
11. **Tokyo** 🇯🇵 - 3 accommodations, 5 activities, 4 restaurants

For these destinations, users get:
- ✅ Real hotel/restaurant/activity options to choose from
- ✅ Interactive customization with "🎨 Customize Your Trip" button
- ✅ Personalized calendar after making selections
- ✅ Detailed prices, ratings, descriptions, amenities

**Any other destination**: AI-generated recommendations with detailed itinerary (but no interactive customization yet)

---

*Last updated: February 17, 2026*
*Status: Ready for testing and deployment*
