"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Request Models

class TravelRequest(BaseModel):
    """Request model for creating a new travel plan"""
    user_request: str = Field(..., description="Natural language travel request")
    email: Optional[EmailStr] = Field(None, description="User email for saving the plan")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_request": "Plan a 7-day cultural trip to Japan in autumn on a moderate budget",
                "email": "user@example.com"
            }
        }

class UpdateTravelRequest(BaseModel):
    """Request model for updating an existing travel plan"""
    trip_id: int = Field(..., description="ID of the trip to update")
    update_request: str = Field(..., description="What to update in the plan")
    
    class Config:
        json_schema_extra = {
            "example": {
                "trip_id": 1,
                "update_request": "Add a food tour on day 3"
            }
        }

class ExportRequest(BaseModel):
    """Request model for exporting itinerary"""
    trip_id: int = Field(..., description="ID of the trip to export")
    format: str = Field(..., description="Export format: pdf, ical, or map")
    
    class Config:
        json_schema_extra = {
            "example": {
                "trip_id": 1,
                "format": "pdf"
            }
        }

class UserCreate(BaseModel):
    """Model for creating a new user"""
    email: EmailStr
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}

# Response Models

class TravelPlanResponse(BaseModel):
    """Response model for travel plan"""
    success: bool
    message: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    trip_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Travel plan created successfully",
                "trip_id": 1,
                "plan": {
                    "destination": "Japan",
                    "summary": "7-day cultural trip...",
                    "itinerary": {}
                }
            }
        }

class ExportResponse(BaseModel):
    """Response model for export operations"""
    success: bool
    message: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None

class UserResponse(BaseModel):
    """Response model for user data"""
    id: int
    email: str
    name: Optional[str]
    preferences: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    """Response model for trip data"""
    id: int
    title: str
    destination: str
    start_date: datetime
    end_date: datetime
    budget: Optional[float]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
