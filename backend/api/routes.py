"""
API routes for Travel Agent
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.api.models import (
    TravelRequest, UpdateTravelRequest, ExportRequest,
    TravelPlanResponse, ExportResponse, UserResponse, TripResponse, HealthResponse
)
from backend.database.db import get_db
from backend.database.models import User, Trip
from backend.agents.orchestrator import orchestrator
from backend.exports.pdf_export import pdf_exporter
from backend.exports.ical_export import ical_exporter
from backend.exports.map_export import map_exporter
from loguru import logger

router = APIRouter()

# Health Check
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.utcnow()
    }

# Travel Planning Endpoints

@router.post("/plan", response_model=TravelPlanResponse)
async def create_travel_plan(
    request: TravelRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new travel plan based on natural language request
    """
    try:
        logger.info(f"Creating travel plan for request: {request.user_request[:100]}...")
        
        # Generate travel plan using orchestrator
        result = await orchestrator.create_travel_plan(request.user_request)
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail="Failed to create travel plan")
        
        plan = result.get('plan', {})
        
        # Save to database if email provided
        trip_id = None
        if request.email:
            user = db.query(User).filter(User.email == request.email).first()
            if not user:
                user = User(email=request.email, preferences={})
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Create trip record
            profile = plan.get('profile', {})
            
            # Extract and format destination (convert list to string if needed)
            destination = profile.get('destination', 'Unknown')
            if isinstance(destination, list):
                destination = ', '.join(str(d) for d in destination)
            
            trip = Trip(
                user_id=user.id,
                title=f"Trip to {destination}",
                destination=destination,
                start_date=datetime.utcnow(),  # Should parse from profile
                end_date=datetime.utcnow(),     # Should calculate from duration
                budget=0.0,  # Should extract from budget data
                itinerary=plan.get('itinerary', {}),
                weather_info=plan.get('weather_info', {}),
                cost_breakdown=plan.get('budget_breakdown', {}),
                status='draft'
            )
            db.add(trip)
            db.commit()
            db.refresh(trip)
            trip_id = trip.id
        
        return {
            "success": True,
            "message": "Travel plan created successfully",
            "plan": plan,
            "trip_id": trip_id
        }
        
    except Exception as e:
        logger.error(f"Error creating travel plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/plan/update", response_model=TravelPlanResponse)
async def update_travel_plan(
    request: UpdateTravelRequest,
    db: Session = Depends(get_db)
):
    """
    Update an existing travel plan
    """
    try:
        # Get existing trip
        trip = db.query(Trip).filter(Trip.id == request.trip_id).first()
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        # Get current plan
        current_plan = {
            'profile': {},  # Reconstruct from trip data
            'itinerary': trip.itinerary,
            'destination': trip.destination
        }
        
        # Update plan using orchestrator
        result = await orchestrator.update_travel_plan(current_plan, request.update_request)
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail="Failed to update travel plan")
        
        # Update database
        plan = result.get('plan', {})
        trip.itinerary = plan.get('itinerary', {})
        trip.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": "Travel plan updated successfully",
            "plan": plan,
            "trip_id": trip.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating travel plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Export Endpoints

@router.post("/export", response_model=ExportResponse)
async def export_itinerary(
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """
    Export itinerary in specified format (pdf, ical, map)
    """
    try:
        # Get trip
        trip = db.query(Trip).filter(Trip.id == request.trip_id).first()
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        # Prepare travel plan data
        travel_plan = {
            'plan': {
                'destination': trip.destination,
                'summary': f"Trip to {trip.destination}",
                'profile': {},
                'itinerary': trip.itinerary,
                'budget_breakdown': trip.cost_breakdown,
                'weather_info': trip.weather_info
            }
        }
        
        # Export based on format
        file_path = None
        if request.format.lower() == 'pdf':
            file_path = pdf_exporter.export_itinerary(travel_plan)
        elif request.format.lower() == 'ical':
            file_path = ical_exporter.export_itinerary(travel_plan)
        elif request.format.lower() == 'map':
            file_path = map_exporter.export_map(travel_plan)
        else:
            raise HTTPException(status_code=400, detail="Invalid export format")
        
        return {
            "success": True,
            "message": f"Itinerary exported as {request.format}",
            "file_path": file_path,
            "download_url": f"/downloads/{file_path.split('/')[-1]}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# User Management Endpoints

@router.get("/users/{email}", response_model=UserResponse)
async def get_user(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}/trips", response_model=List[TripResponse])
async def get_user_trips(user_id: int, db: Session = Depends(get_db)):
    """Get all trips for a user"""
    trips = db.query(Trip).filter(Trip.user_id == user_id).all()
    return trips

@router.get("/trips/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Get specific trip by ID"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.delete("/trips/{trip_id}")
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete a trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    
    return {"success": True, "message": "Trip deleted successfully"}
