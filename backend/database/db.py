"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from backend.config import settings
from backend.database.models import Base
from contextlib import contextmanager
from loguru import logger

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in settings.DATABASE_URL else None,
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_db() -> Session:
    """
    Dependency function to get database session
    Used with FastAPI's dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager for database session
    Use when not working with FastAPI dependencies
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Initialize database on import
init_db()
