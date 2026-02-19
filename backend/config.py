"""
Configuration management for the Travel Agent application
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    GROQ_API_KEY: str
    
    # Pinecone Configuration
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "travel-agent"
    
    # Database
    DATABASE_URL: str = "sqlite:///./travel_agent.db"
    
    # Application Settings
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Frontend URL (for CORS)
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Backend URL
    BACKEND_URL: str = "http://localhost:8000"
    
    # Project paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    GUIDES_DIR: Path = DATA_DIR / "guides"
    EXPORTS_DIR: Path = BASE_DIR / "exports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Ensure required directories exist
settings.DATA_DIR.mkdir(exist_ok=True)
settings.GUIDES_DIR.mkdir(exist_ok=True)
settings.EXPORTS_DIR.mkdir(exist_ok=True, parents=True)

# Validate critical settings - at least one AI provider must be available
ai_providers = [
    settings.GOOGLE_API_KEY,
    settings.OPENAI_API_KEY,
    settings.GROQ_API_KEY
]
if not any(ai_providers):
    raise ValueError("At least one AI API key (GOOGLE_API_KEY, OPENAI_API_KEY, or GROQ_API_KEY) must be set in .env file")
