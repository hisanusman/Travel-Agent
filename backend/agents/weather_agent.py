"""
Weather Agent - Provides weather-based recommendations and timing
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from backend.agents.multi_provider_agent import MultiProviderAgent
from loguru import logger
import python_weather
import asyncio

class WeatherAgent(MultiProviderAgent):
    """Agent responsible for weather information and recommendations"""
    
    def __init__(self):
        super().__init__(name="WeatherAgent")
        self.weather_prompt = """
You are a weather and timing expert for travel planning.

Destination: {destination}
Travel Dates: {dates}
Weather Forecast: {weather_data}

Based on the weather conditions, provide recommendations in JSON format:
- daily_conditions: Summary of expected conditions each day
- best_times: Best times of day for outdoor activities
- weather_appropriate_activities: Activities suited for each day's weather
- packing_suggestions: What to pack based on weather
- weather_warnings: Any weather concerns or precautions

Return ONLY a valid JSON object.
"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process weather query and provide recommendations
        
        Args:
            input_data: Dict with destination and travel dates
            
        Returns:
            Weather information and recommendations
        """
        try:
            destination = input_data.get('destination', '')
            dates = input_data.get('dates', '')
            
            logger.info(f"WeatherAgent processing weather for: {destination}")
            
            # Get weather data
            weather_data = await self._get_weather(destination)
            
            # Generate prompt
            prompt = self._create_prompt(
                self.weather_prompt,
                destination=destination,
                dates=dates,
                weather_data=weather_data
            )
            
            # Get response from model
            response = await self._generate_response(prompt)
            
            # Parse JSON response
            weather_recommendations = self._parse_json_response(response)
            
            logger.info(f"WeatherAgent generated recommendations for {destination}")
            
            return {
                'success': True,
                'agent': self.name,
                'destination': destination,
                'weather': weather_recommendations
            }
            
        except Exception as e:
            logger.error(f"Error in WeatherAgent: {e}")
            return {
                'success': False,
                'agent': self.name,
                'error': str(e)
            }
    
    async def _get_weather(self, location: str) -> str:
        """Fetch weather forecast for location"""
        try:
            async with python_weather.Client(unit=python_weather.METRIC) as client:
                weather = await client.get(location)
                
                # Format weather data
                weather_info = []
                weather_info.append(f"Current: {weather.temperature}°C, {weather.description}")
                
                for daily in weather.daily_forecasts[:7]:  # Get 7-day forecast
                    date_str = daily.date.strftime('%Y-%m-%d')
                    weather_info.append(
                        f"{date_str}: High {daily.highest_temperature}°C, "
                        f"Low {daily.lowest_temperature}°C"
                    )
                
                return "\n".join(weather_info)
                
        except Exception as e:
            logger.warning(f"Could not fetch weather data: {e}")
            return "Weather data unavailable. Recommend checking closer to travel date."
