"""
Orchestrator Agent - Coordinates all agents and consolidates results
"""

from typing import Dict, Any
from backend.agents.profile_agent import ProfileAgent
from backend.agents.destination_agent import DestinationAgent
from backend.agents.weather_agent import WeatherAgent
from backend.agents.budget_agent import BudgetAgent
from backend.agents.itinerary_agent import ItineraryAgent
from backend.agents.mock_agent import MockAgentResponse
from backend.config import settings
from loguru import logger
import asyncio
import os

# Use mock mode if environment variable is set or if we detect quota issues
USE_MOCK = os.getenv("USE_MOCK_AGENTS", "false").lower() == "true"

class OrchestratorAgent:
    """
    Main orchestrator that coordinates all specialized agents
    and consolidates their outputs into a complete travel plan
    """
    
    def __init__(self):
        self.profile_agent = ProfileAgent()
        self.destination_agent = DestinationAgent()
        self.weather_agent = WeatherAgent()
        self.budget_agent = BudgetAgent()
        self.itinerary_agent = ItineraryAgent()
        logger.info("Orchestrator initialized with all agents")
    
    async def create_travel_plan(self, user_request: str) -> Dict[str, Any]:
        """
        Main method to create a complete travel plan
        
        Args:
            user_request: Natural language travel request from user
            
        Returns:
            Complete travel plan with itinerary, budget, and recommendations
        """
        try:
            logger.info(f"Orchestrator creating travel plan for: {user_request[:100]}...")
            
            # Use mock mode if enabled (for testing when APIs are unavailable)
            if USE_MOCK:
                logger.info("Using MOCK mode for travel plan generation")
                return self._create_mock_plan(user_request)
            
            # Step 1: Extract user profile and preferences
            profile_result = await self.profile_agent.process({
                'user_request': user_request
            })
            
            if not profile_result.get('success'):
                return self._error_response("Failed to extract travel preferences", profile_result)
            
            profile = profile_result.get('profile', {})
            destination = profile.get('destination', 'unknown')
            
            # Step 2: Run parallel queries for destination, weather, and initial data
            logger.info("Running parallel agent queries...")
            destination_task = self.destination_agent.process({'profile': profile})
            weather_task = self.weather_agent.process({
                'destination': destination,
                'dates': profile.get('dates', 'Not specified')
            })
            
            destination_result, weather_result = await asyncio.gather(
                destination_task,
                weather_task
            )
            
            # Step 3: Get budget estimation based on destination and activities
            budget_result = await self.budget_agent.process({
                'profile': profile,
                'activities': destination_result.get('recommendations', {}).get('top_attractions', [])
            })
            
            # Step 4: Create final itinerary with all information
            itinerary_result = await self.itinerary_agent.process({
                'profile': profile,
                'attractions': destination_result.get('recommendations', {}),
                'weather': weather_result.get('weather', {}),
                'budget': budget_result.get('budget', {})
            })
            
            # Step 5: Consolidate all results
            travel_plan = self._consolidate_results(
                profile=profile,
                destination=destination_result,
                weather=weather_result,
                budget=budget_result,
                itinerary=itinerary_result
            )
            
            logger.info("Travel plan created successfully")
            return travel_plan
            
        except Exception as e:
            logger.error(f"Error in orchestrator: {e}")
            return self._error_response(f"Failed to create travel plan: {str(e)}")
    
    async def update_travel_plan(
        self,
        current_plan: Dict[str, Any],
        update_request: str
    ) -> Dict[str, Any]:
        """
        Update an existing travel plan based on user feedback
        
        Args:
            current_plan: Existing travel plan
            update_request: User's update request
            
        Returns:
            Updated travel plan
        """
        try:
            logger.info(f"Updating travel plan: {update_request[:100]}...")
            
            # Analyze what needs to be updated
            profile = current_plan.get('profile', {})
            
            # Update the relevant components
            # For now, recreate the plan with updated preferences
            # In future, can make this more granular
            
            return await self.create_travel_plan(update_request)
            
        except Exception as e:
            logger.error(f"Error updating travel plan: {e}")
            return self._error_response(f"Failed to update travel plan: {str(e)}")
    
    def _consolidate_results(
        self,
        profile: Dict[str, Any],
        destination: Dict[str, Any],
        weather: Dict[str, Any],
        budget: Dict[str, Any],
        itinerary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolidate all agent results into a unified travel plan"""
        
        # Check if we have rich destination data (accommodations, activities, restaurants)
        destination_data = {}
        if destination.get('accommodations'):
            destination_data = {
                'accommodations': destination.get('accommodations', []),
                'activities': destination.get('activities', []),
                'restaurants': destination.get('restaurants', [])
            }
        
        return {
            'success': True,
            'plan': {
                'profile': profile,
                'destination': destination.get('destination', 'unknown'),
                'summary': self._create_summary(profile, itinerary, budget),
                'itinerary': itinerary.get('itinerary', {}),
                'destination_info': destination.get('recommendations', {}),
                'destination_data': destination_data,  # Rich data for customization
                'weather_info': weather.get('weather', {}),
                'budget_breakdown': budget.get('budget', {}),
                'metadata': {
                    'created_at': self._get_timestamp(),
                    'agents_used': [
                        'ProfileAgent',
                        'DestinationAgent',
                        'WeatherAgent',
                        'BudgetAgent',
                        'ItineraryAgent'
                    ]
                }
            }
        }
    
    def _create_summary(
        self,
        profile: Dict[str, Any],
        itinerary: Dict[str, Any],
        budget: Dict[str, Any]
    ) -> str:
        """Create a human-readable summary of the travel plan"""
        
        destination = profile.get('destination', 'your destination')
        duration = profile.get('duration', 'N/A')
        budget_level = profile.get('budget_level', 'moderate')
        total_cost = budget.get('budget', {}).get('total_estimated', 'N/A')
        
        summary = f"Your {duration}-day {budget_level} trip to {destination} "
        summary += f"with an estimated cost of ${total_cost}. "
        summary += "The itinerary is optimized for your interests and includes "
        summary += "accommodations, activities, dining, and transportation."
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def _error_response(self, message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized error response"""
        response = {
            'success': False,
            'error': message,
            'timestamp': self._get_timestamp()
        }
        
        if details:
            response['details'] = details
        
        return response
    
    def _create_mock_plan(self, user_request: str) -> Dict[str, Any]:
        """Create a mock travel plan for testing"""
        logger.info("Generating mock travel plan...")
        
        profile = MockAgentResponse.mock_profile(user_request)
        destination_info = MockAgentResponse.mock_destination()
        weather_info = MockAgentResponse.mock_weather()
        budget_info = MockAgentResponse.mock_budget()
        itinerary_info = MockAgentResponse.mock_itinerary()
        
        return self._consolidate_results(
            profile=profile,
            destination={'destination': profile['destination'], 'recommendations': destination_info},
            weather={'weather': weather_info},
            budget={'budget': budget_info},
            itinerary={'itinerary': itinerary_info}
        )

# Global orchestrator instance
orchestrator = OrchestratorAgent()
