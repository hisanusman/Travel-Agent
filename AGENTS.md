# 🌍 Agentic Travel Planner

An intelligent, **conversational** travel planning system powered by multi-agent architecture with natural language interaction.

## 📋 Project Overview

This application provides an AI-powered travel assistant that can:
- **Converse naturally** with users to understand their travel needs
- Generate personalized itineraries based on natural language queries
- Ask smart follow-up questions to gather missing information
- Provide context-aware recommendations (opening hours, entry fees, best times)
- Intelligently filter options based on budget constraints
- Create day-by-day travel plans with activities, transportation, and timing
- Provide weather-aware recommendations
- Estimate budgets and optimize costs
- Export itineraries as PDF, iCal, interactive maps, and budget reports
- Support multi-turn conversations to refine plans

## 🏗️ Architecture

### Multi-Agent System

The system uses specialized agents coordinated through a conversational interface:

1. **Conversation Agent** - Manages multi-turn dialogue, extracts information progressively, asks clarifying questions
2. **Profile Agent** - Manages user preferences, budget, dates, and interests
3. **Destination & Attractions Agent** - Retrieves POIs, attractions, and local tips from knowledge base
4. **Itinerary Planner Agent** - Creates optimized day-by-day schedules
5. **Weather & Timing Agent** - Provides weather-based recommendations
6. **Budget & Costs Agent** - Estimates costs and optimizes expenses
7. **Orchestrator Agent** - Coordinates all agents and consolidates outputs

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React
- **AI Providers**: OpenAI → Google Gemini → Groq (automatic fallback)
- **Knowledge Base**: Local JSON database with 19 European cities (855 items)
- **Vector Database**: Pinecone (optional RAG enhancement)
- **Database**: SQLite (user profiles, trips, conversations)
- **Deployment**: Docker, Vercel-ready
- **Containerization**: Docker

## 📁 Project Structure

```
TravelAgent/
├── backend/
│   ├── agents/              # Agent implementations
│   │   ├── __init__.py
│   │   ├── multi_provider_agent.py  # Base agent with AI fallback
│   │   ├── profile_agent.py
│   │   ├── destination_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── weather_agent.py
│   │   ├── budget_agent.py
│   │   └── orchestrator.py
│   ├── conversation/        # Conversational interface
│   │   ├── __init__.py
│   │   ├── agent.py         # ConversationAgent
│   │   └── state.py         # State management
│   ├── api/                 # FastAPI routes
│   │   ├── __init__.py
│   │   ├── routes.py        # Main travel planning routes
│   │   └── conversation_routes.py  # Conversation routes
│   ├── database/            # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── db.py
│   ├── rag/                 # Knowledge retrieval
│   │   ├── __init__.py
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
│   │   │   ├── ChatInterface.jsx     # Conversational UI
│   │   │   └── OptionCard.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ConversationPage.jsx  # Chat page
│   │   │   ├── PlanPage.jsx          # Classic form
│   │   │   ├── SelectionPage.jsx     # Customization
│   │   │   └── TripDetailsPage.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── data/                    # Travel database
│   └── travel_database.json  # 19 European cities, 855 items
├── .env.example             # Example environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── Dockerfile
├── docker-compose.yml
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

### v0.6.0 (Current - February 18, 2026) 🆕
- ✅ **Conversational Interface**: Natural language multi-turn dialogue system
- ✅ ConversationAgent for intelligent question flow
- ✅ Progressive information gathering with completeness tracking
- ✅ Context-aware follow-up questions
- ✅ Budget-intelligent filtering (auto-applies constraints)
- ✅ Beautiful chat UI with message bubbles and quick replies
- ✅ Real-time progress indicator
- ✅ New routes: `/chat` (conversational), `/plan` (classic form)
- ✅ Smart extraction of destination, duration, budget, interests from natural language

### v0.5.0 (February 18, 2026)
- ✅ Massive database expansion to 19 European cities
- ✅ Each city now has 15+ hotels, activities, and restaurants (855 total items)
- ✅ Added opening hours, entry fees, best times to visit for all activities
- ✅ Removed non-European destinations (Maldives, Tokyo)
- ✅ Added new cities: Venice, Florence, Athens, Santorini, Lisbon, Edinburgh, Dubrovnik, Berlin, Munich, Copenhagen
- ✅ Database file: 13,897 lines, 402KB

### v0.4.0 (February 18, 2026)
- ✅ Added 7 European destinations with basic data
- ✅ Cleaned up repository documentation

### v0.3.0 (February 18, 2026)
- ✅ Fixed itinerary generation bug
- ✅ Added Madrid to database
- ✅ Full interactive customization UI

### v0.2.0 (February 17, 2026)
- ✅ Multi-provider AI fallback system (OpenAI → Google → Groq)

### v0.1.0 (February 17, 2026)
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

The system now includes **19 European destinations** with full interactive customization:

### Western Europe
1. **Amsterdam** 🇳🇱 - 15 hotels, 15 activities, 15 restaurants
2. **Barcelona** 🇪🇸 - 15 hotels, 15 activities, 15 restaurants
3. **Berlin** 🇩🇪 - 15 hotels, 15 activities, 15 restaurants
4. **Edinburgh** 🏴󠁧󠁢󠁳󠁣󠁴󠁿 - 15 hotels, 15 activities, 15 restaurants
5. **Lisbon** 🇵🇹 - 15 hotels, 15 activities, 15 restaurants
6. **London** 🇬🇧 - 15 hotels, 15 activities, 15 restaurants
7. **Madrid** 🇪🇸 - 15 hotels, 15 activities, 15 restaurants
8. **Munich** 🇩🇪 - 15 hotels, 15 activities, 15 restaurants
9. **Paris** 🇫🇷 - 15 hotels, 15 activities, 15 restaurants

### Central & Eastern Europe
10. **Budapest** 🇭🇺 - 15 hotels, 15 activities, 15 restaurants
11. **Copenhagen** 🇩🇰 - 15 hotels, 15 activities, 15 restaurants
12. **Prague** 🇨🇿 - 15 hotels, 15 activities, 15 restaurants
13. **Vienna** 🇦🇹 - 15 hotels, 15 activities, 15 restaurants

### Southern Europe & Islands
14. **Athens** 🇬🇷 - 15 hotels, 15 activities, 15 restaurants
15. **Dubrovnik** 🇭🇷 - 15 hotels, 15 activities, 15 restaurants
16. **Florence** 🇮🇹 - 15 hotels, 15 activities, 15 restaurants
17. **Rome** 🇮🇹 - 15 hotels, 15 activities, 15 restaurants
18. **Santorini** 🇬🇷 - 15 hotels, 15 activities, 15 restaurants
19. **Venice** 🇮🇹 - 15 hotels, 15 activities, 15 restaurants

### Database Statistics
- **Total Items:** 855 (285 accommodations, 285 activities, 285 restaurants)
- **Each destination includes:** Opening hours, entry fees, best times to visit, price ranges, ratings, detailed descriptions
- **Interactive Features:** Users can select specific hotels, activities, and restaurants to create personalized itineraries

**Any other destination**: AI-generated recommendations with detailed itinerary (but no interactive customization yet)

---

*Last updated: February 18, 2026*  
*Status: ✅ Conversational interface fully implemented and ready for testing*  
*Version: 0.6.0*
