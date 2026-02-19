"""
Itinerary Planner Agent - Creates optimized day-by-day schedules
"""

from typing import Dict, Any, List
from backend.agents.multi_provider_agent import MultiProviderAgent
from loguru import logger

class ItineraryAgent(MultiProviderAgent):
    """Agent responsible for creating structured travel itineraries"""
    
    def __init__(self):
        super().__init__(name="ItineraryAgent")
        self.itinerary_prompt = """
You are an expert travel itinerary planner creating a {duration}-day trip to {destination}.

Traveler Profile:
- Interests: {interests}
- Budget Level: {budget_level}
- Travel Style: {travel_style}

Available Hotels, Activities & Restaurants:
{attractions}

Weather Considerations:
{weather_info}

Budget Constraints:
{budget_info}

IMPORTANT: Create a COMPLETE day-by-day itinerary that MUST include:
1. Specific hotel recommendations from the available hotels list
2. Specific activities with times (morning/afternoon/evening) from the activities list
3. Specific restaurant recommendations for meals from the restaurants list
4. Include entry fees, opening hours, and other details
5. Estimated costs for each day

Return a JSON object with this EXACT structure:
{{
  "days": [
    {{
      "day_number": 1,
      "theme": "Arrival & Historic Center",
      "activities": [
        {{
          "time": "Morning (9:00 AM)",
          "name": "Specific activity name from the available activities",
          "description": "What you'll do and see",
          "location": "Specific location",
          "duration": "2 hours",
          "cost": "$25"
        }},
        {{
          "time": "Afternoon (2:00 PM)",
          "name": "Another specific activity",
          "description": "Description",
          "location": "Location",
          "duration": "3 hours",
          "cost": "$40"
        }},
        {{
          "time": "Evening (7:00 PM)",
          "name": "Dinner at [Specific Restaurant Name]",
          "description": "Cuisine type and specialties",
          "location": "Restaurant location",
          "duration": "2 hours",
          "cost": "$45"
        }}
      ],
      "accommodation": "Specific hotel name from available hotels with price per night",
      "estimated_cost": "$200"
    }}
  ]
}}

Create all {duration} days following this structure. Use REAL names from the available lists above!
"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process itinerary creation request
        
        Args:
            input_data: Dict with profile, destination data, weather, and budget
            
        Returns:
            Complete day-by-day itinerary
        """
        try:
            profile = input_data.get('profile', {})
            destination = profile.get('destination', 'unknown')
            attractions = input_data.get('attractions', {})
            weather = input_data.get('weather', {})
            budget = input_data.get('budget', {})
            
            logger.info(f"ItineraryAgent creating itinerary for: {destination}")
            
            # Generate prompt
            interests = profile.get('interests', [])
            if isinstance(interests, list):
                interests_str = ', '.join(str(i) for i in interests)
            else:
                interests_str = str(interests)
            
            prompt = self._create_prompt(
                self.itinerary_prompt,
                duration=profile.get('duration', 7),
                destination=destination,
                interests=interests_str,
                budget_level=profile.get('budget_level', 'moderate'),
                travel_style=profile.get('travel_style', 'general'),
                attractions=self._format_attractions(attractions),
                weather_info=self._format_weather(weather),
                budget_info=self._format_budget(budget)
            )
            
            # Get response from model
            response = await self._generate_response(prompt)
            
            # Parse JSON response
            try:
                itinerary_data = self._parse_json_response(response)
                # Ensure itinerary_data is a dict
                if not isinstance(itinerary_data, dict):
                    logger.warning(f"Itinerary data is not a dict: {type(itinerary_data)}")
                    itinerary_data = {'days': itinerary_data if isinstance(itinerary_data, list) else []}
            except Exception as parse_error:
                logger.error(f"Failed to parse itinerary JSON: {parse_error}")
                itinerary_data = {'days': []}
            
            days_count = len(itinerary_data.get('days', [])) if isinstance(itinerary_data, dict) else 0
            logger.info(f"ItineraryAgent created {days_count} day itinerary")
            
            return {
                'success': True,
                'agent': self.name,
                'destination': destination,
                'itinerary': itinerary_data
            }
            
        except Exception as e:
            logger.error(f"Error in ItineraryAgent: {e}")
            return {
                'success': False,
                'agent': self.name,
                'error': str(e)
            }
    
    def _format_attractions(self, attractions: Dict[str, Any]) -> str:
        """Format attractions data for prompt with rich details"""
        if not attractions:
            return "General attractions and activities available"
        
        # Check if we have rich structured data (from local database)
        if attractions.get('accommodations') or attractions.get('activities') or attractions.get('restaurants'):
            formatted = []
            
            # Format Hotels
            if attractions.get('accommodations'):
                formatted.append("\n**AVAILABLE HOTELS:**")
                for hotel in attractions['accommodations'][:10]:  # Top 10
                    formatted.append(f"  - {hotel.get('name')} ({hotel.get('category', 'Standard')})")
                    formatted.append(f"    Price: {hotel.get('price_per_night', 'TBD')}/night, Rating: {hotel.get('rating', 'N/A')}")
                    if hotel.get('amenities'):
                        formatted.append(f"    Amenities: {', '.join(hotel['amenities'][:3])}")
            
            # Format Activities
            if attractions.get('activities'):
                formatted.append("\n**AVAILABLE ACTIVITIES:**")
                for activity in attractions['activities'][:15]:  # Top 15
                    formatted.append(f"  - {activity.get('name')} ({activity.get('category', 'Activity')})")
                    formatted.append(f"    {activity.get('description', '')[:100]}")
                    if activity.get('entry_fee'):
                        formatted.append(f"    Entry Fee: {activity['entry_fee']}")
                    if activity.get('opening_hours'):
                        formatted.append(f"    Hours: {activity['opening_hours']}")
                    if activity.get('best_time'):
                        formatted.append(f"    Best Time: {activity['best_time']}")
            
            # Format Restaurants
            if attractions.get('restaurants'):
                formatted.append("\n**AVAILABLE RESTAURANTS:**")
                for restaurant in attractions['restaurants'][:10]:  # Top 10
                    formatted.append(f"  - {restaurant.get('name')} ({restaurant.get('cuisine', 'Local')})")
                    formatted.append(f"    Price: {restaurant.get('price_range', 'Moderate')}, Rating: {restaurant.get('rating', 'N/A')}")
                    if restaurant.get('specialties'):
                        formatted.append(f"    Specialties: {', '.join(restaurant['specialties'][:2])}")
            
            return '\n'.join(formatted)
        
        # Fallback for text-based recommendations
        recs = attractions.get('recommendations', {})
        formatted = []
        
        for category, items in recs.items():
            if isinstance(items, list):
                for item in items[:5]:  # Limit to top 5 per category
                    if isinstance(item, dict):
                        name = item.get('name', 'Unknown')
                        desc = item.get('description', '')
                        formatted.append(f"- {name}: {desc}")
        
        return "\n".join(formatted) if formatted else "Use general destination knowledge"
    
    def _format_weather(self, weather: Dict[str, Any]) -> str:
        """Format weather data for prompt"""
        if not weather or not weather.get('weather'):
            return "No specific weather data available"
        
        weather_data = weather.get('weather', {})
        conditions = weather_data.get('daily_conditions', [])
        
        if isinstance(conditions, list):
            return "\n".join([f"Day {i+1}: {cond}" for i, cond in enumerate(conditions)])
        
        return str(weather_data.get('daily_conditions', 'Variable conditions'))
    
    def _format_budget(self, budget: Dict[str, Any]) -> str:
        """Format budget data for prompt"""
        if not budget or not budget.get('budget'):
            return "No specific budget constraints"
        
        budget_data = budget.get('budget', {})
        return f"Total budget: ${budget_data.get('total_cost', 'flexible')}, Daily average: ${budget_data.get('daily_average', 'flexible')}"
