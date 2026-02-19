"""
Database models for the Travel Agent application
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User model for storing user information and preferences"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    preferences = Column(JSON, default={})  # Store user preferences as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to trips
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Trip(Base):
    """Trip model for storing travel itineraries"""
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Trip basic info
    title = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Trip details
    budget = Column(Float, nullable=True)
    budget_type = Column(String, default="moderate")  # budget, moderate, luxury
    interests = Column(JSON, default=[])  # List of interests
    
    # Generated itinerary
    itinerary = Column(JSON, default={})  # Complete day-by-day itinerary
    weather_info = Column(JSON, default={})  # Weather forecast data
    cost_breakdown = Column(JSON, default={})  # Budget breakdown
    
    # Metadata
    status = Column(String, default="draft")  # draft, finalized, completed
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User", back_populates="trips")
    
    def __repr__(self):
        return f"<Trip(id={self.id}, destination={self.destination}, user_id={self.user_id})>"


class Conversation(Base):
    """Conversation history for tracking user interactions"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    
    # Conversation details
    messages = Column(JSON, default=[])  # List of messages with role and content
    context = Column(JSON, default={})  # Additional context data
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"
