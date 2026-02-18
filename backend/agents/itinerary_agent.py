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

Available Attractions and Activities:
{attractions}

Weather Considerations:
{weather_info}

Budget Constraints:
{budget_info}

Create a detailed day-by-day itinerary in JSON format:
- day_number: Day 1, 2, etc.
- date: Actual date if available
- theme: Theme or focus for the day
- morning: Activity with time, location, duration, description, cost
- afternoon: Activity with time, location, duration, description, cost
- evening: Activity with time, location, duration, description, cost
- meals: Breakfast, lunch, dinner recommendations
- transportation: How to get between locations
- estimated_cost: Daily cost
- notes: Tips, alternatives, or important information

Optimize for:
- Geographical proximity (minimize travel time)
- Logical flow and pacing
- Weather suitability
- Budget adherence
- Interest alignment

Return ONLY a valid JSON object with an array of daily plans.
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
        """Format attractions data for prompt"""
        if not attractions:
            return "Use your knowledge of popular attractions"
        
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
        total = budget_data.get('total_estimated', 'N/A')
        daily = budget_data.get('daily_average', 'N/A')
        
        return f"Total Budget: ${total}, Daily Average: ${daily}"
