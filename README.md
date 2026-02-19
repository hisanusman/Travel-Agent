# 🌍 AI Travel Agent

An intelligent travel planning application powered by multi-agent AI architecture, featuring natural language processing, RAG (Retrieval-Augmented Generation), and real-time itinerary generation.

## ✨ Features

- **🤖 Multi-Agent AI System**: Specialized agents for profile extraction, destination recommendations, weather analysis, budget planning, and itinerary creation
- **🔄 Smart Fallback**: Automatic provider switching (OpenAI → Google Gemini → Groq) for high availability
- **📚 RAG-Powered Recommendations**: Pinecone vector database for intelligent destination insights
- **💰 Budget Planning**: Automated cost estimation with accommodation, food, transport, and activities
- **🌤️ Weather-Aware**: Dynamic recommendations based on weather conditions
- **📅 Export Options**: PDF itineraries, iCal calendar events, interactive maps
- **💾 Persistent Storage**: SQLite database for user profiles and trip history
- **🎨 Modern UI**: Beautiful React frontend with responsive design

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Profile Agent**: Extracts travel preferences from natural language
- **Destination Agent**: RAG-powered attraction and POI recommendations
- **Weather Agent**: Real-time weather data and climate-based suggestions
- **Budget Agent**: Cost breakdown and budget optimization
- **Itinerary Agent**: Day-by-day schedule with activities and timings
- **Orchestrator**: Coordinates all agents and consolidates results

### Frontend (React)
- Natural language trip planning interface
- Real-time plan generation with loading states
- Interactive trip details and export options
- Responsive design for all devices

### Tech Stack
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy, Pinecone, OpenAI/Google/Groq APIs
- **Frontend**: React 18, React Router, Axios, Lucide Icons
- **Database**: SQLite (dev), PostgreSQL ready (prod)
- **Deployment**: Docker, Docker Compose, Vercel ready

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys: OpenAI/Google AI/Groq (at least one), Pinecone

### 1. Clone the Repository
```bash
git clone https://github.com/hisanusman/Travel-Agent.git
cd Travel-Agent
```

### 2. Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run backend
python -m uvicorn backend.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000  
API Docs: http://localhost:8000/docs

### 3. Frontend Setup
```bash
# In a new terminal
cd frontend
npm install
PORT=5173 npm start
```

Frontend will run at: http://localhost:5173

## 📝 Environment Variables

Create a `.env` file in the project root:

```env
# AI Providers (at least one required)
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key

# Vector Database
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=travel-agent

# Application
DEBUG=True
LOG_LEVEL=INFO
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

## 🎯 Usage

1. **Open the app**: Navigate to http://localhost:5173
2. **Describe your trip**: Use natural language, e.g., "Plan a 7-day cultural trip to Japan in autumn on a moderate budget"
3. **Get your itinerary**: The AI will generate a complete plan with:
   - Day-by-day activities
   - Restaurant recommendations
   - Transportation details
   - Weather considerations
   - Budget breakdown
   - Packing suggestions
4. **Export**: Download as PDF, add to calendar, or view on an interactive map

## 📦 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Test API directly
python test_api.py
```

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/plan` | POST | Create travel plan |
| `/api/v1/plan/update` | PUT | Update existing plan |
| `/api/v1/export` | POST | Export itinerary |
| `/api/v1/trips/{id}` | GET | Get trip details |
| `/api/v1/users/{id}/trips` | GET | Get user's trips |

Full API documentation: http://localhost:8000/docs

## 🗂️ Project Structure

```
TravelAgent/
├── backend/
│   ├── agents/           # AI agent implementations
│   ├── api/             # FastAPI routes and models
│   ├── database/        # SQLAlchemy models and DB setup
│   ├── exports/         # PDF, iCal, map exporters
│   ├── rag/             # Pinecone RAG implementation
│   ├── config.py        # Configuration management
│   └── main.py          # FastAPI application
├── frontend/
│   ├── public/          # Static assets
│   └── src/
│       ├── components/  # React components
│       ├── pages/       # Page components
│       ├── services/    # API client
│       └── App.jsx      # Main app component
├── data/                # Travel guides and knowledge base
├── exports/             # Generated exports
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker orchestration
└── vercel.json         # Vercel deployment config
```

## 🔒 Security Notes

- API keys are stored in `.env` (never committed)
- `.gitignore` excludes all sensitive files
- CORS configured for specific origins
- Input validation on all endpoints
- Secure error handling without leaking internals

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI, Google AI, and Groq for LLM APIs
- Pinecone for vector database
- FastAPI for the excellent web framework
- React team for the frontend library

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using AI-powered development**
