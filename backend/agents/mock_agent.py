"""
Mock agent for testing when API quotas are exhausted
"""

from typing import Dict, Any
from loguru import logger

class MockAgentResponse:
    """Mock responses for testing"""
    
    @staticmethod
    def mock_profile(user_request: str) -> Dict[str, Any]:
        """Mock profile extraction"""
        return {
            "destination": "San Francisco",
            "duration": 3,
            "dates": "upcoming weekend",
            "budget_level": "moderate",
            "interests": ["food", "culture", "sightseeing"],
            "travel_style": "couple",
            "special_requirements": "none",
            "preferences": {}
        }
    
    @staticmethod
    def mock_destination() -> Dict[str, Any]:
        """Mock destination recommendations"""
        return {
            "top_attractions": [
                {
                    "name": "Golden Gate Bridge",
                    "description": "Iconic suspension bridge offering stunning views",
                    "estimated_time": "2 hours",
                    "cost_level": "free"
                },
                {
                    "name": "Ferry Building Marketplace",
                    "description": "Historic food hall with local artisan vendors",
                    "estimated_time": "2 hours",
                    "cost_level": "moderate"
                },
                {
                    "name": "Chinatown",
                    "description": "Oldest Chinatown in North America with authentic cuisine",
                    "estimated_time": "3 hours",
                    "cost_level": "budget"
                }
            ],
            "local_experiences": [
                "Food tour in Mission District",
                "Cable car ride",
                "Sunset at Twin Peaks"
            ],
            "restaurants": [
                "Tartine Bakery - Famous pastries",
                "Swan Oyster Depot - Fresh seafood",
                "Mission Chinese Food - Modern Chinese"
            ],
            "neighborhoods": ["Mission District", "North Beach", "Hayes Valley"],
            "transportation": "BART, Muni, walking",
            "local_tips": ["Get a Clipper Card", "Layer clothing", "Book restaurants ahead"],
            "hidden_gems": ["Lands End Trail", "Sutro Baths ruins", "Clarion Alley murals"]
        }
    
    @staticmethod
    def mock_weather() -> Dict[str, Any]:
        """Mock weather recommendations"""
        return {
            "daily_conditions": [
                "Day 1: Sunny, 65°F, light breeze",
                "Day 2: Partly cloudy, 63°F, morning fog",
                "Day 3: Clear, 68°F, perfect weather"
            ],
            "best_times": "Afternoons are warmest, mornings can be foggy",
            "weather_appropriate_activities": {
                "Day 1": "Perfect for Golden Gate Bridge visit",
                "Day 2": "Indoor activities in morning, outdoor in afternoon",
                "Day 3": "Full day outdoor exploration"
            },
            "packing_suggestions": [
                "Light jacket or sweater",
                "Comfortable walking shoes",
                "Layers for variable temps",
                "Sunglasses"
            ],
            "weather_warnings": "SF can be cooler than expected. Dress in layers!"
        }
    
    @staticmethod
    def mock_budget() -> Dict[str, Any]:
        """Mock budget estimation"""
        return {
            "accommodation": {
                "daily": 200,
                "total": 600,
                "type": "Mid-range hotel or Airbnb"
            },
            "meals": {
                "breakfast": 15,
                "lunch": 25,
                "dinner": 50,
                "daily_total": 90
            },
            "transportation": {
                "daily": 20,
                "total": 60,
                "details": "Muni passes and occasional Uber"
            },
            "activities": {
                "total": 150,
                "breakdown": "Museum entries, food tours, misc"
            },
            "miscellaneous": {
                "daily": 30,
                "total": 90
            },
            "total_estimated": 1170,
            "daily_average": 390,
            "budget_tips": [
                "Buy CityPASS for attraction savings",
                "Happy hour deals abound",
                "Free walking tours available",
                "BART from airport saves money"
            ],
            "cost_comparison": "Moderate budget. Well-planned for SF pricing."
        }
    
    @staticmethod
    def mock_itinerary() -> Dict[str, Any]:
        """Mock day-by-day itinerary"""
        return {
            "days": [
                {
                    "day_number": 1,
                    "theme": "Classic San Francisco",
                    "morning": {
                        "time": "9:00 AM",
                        "location": "Ferry Building Marketplace",
                        "duration": 2,
                        "description": "Start with artisan breakfast and explore local vendors",
                        "cost": 30
                    },
                    "afternoon": {
                        "time": "12:00 PM",
                        "location": "Golden Gate Bridge & Fort Point",
                        "duration": 3,
                        "description": "Walk or bike across the iconic bridge, explore Fort Point",
                        "cost": 40
                    },
                    "evening": {
                        "time": "6:00 PM",
                        "location": "North Beach - Italian District",
                        "duration": 3,
                        "description": "Dinner at authentic Italian restaurant, gelato at Tony's",
                        "cost": 75
                    },
                    "meals": {
                        "breakfast": "Ferry Building",
                        "lunch": "Warming Hut near bridge",
                        "dinner": "Mama's on Washington Square"
                    },
                    "transportation": "Muni F-line, walking",
                    "estimated_cost": 145,
                    "notes": "Book dinner reservation ahead. Bring layers for bridge walk."
                },
                {
                    "day_number": 2,
                    "theme": "Culture & Food",
                    "morning": {
                        "time": "10:00 AM",
                        "location": "Chinatown",
                        "duration": 3,
                        "description": "Explore oldest Chinatown, visit Golden Gate Fortune Cookie Factory",
                        "cost": 25
                    },
                    "afternoon": {
                        "time": "2:00 PM",
                        "location": "Mission District Food Tour",
                        "duration": 3,
                        "description": "Guided food tour sampling tacos, burritos, and murals",
                        "cost": 75
                    },
                    "evening": {
                        "time": "7:00 PM",
                        "location": "Hayes Valley",
                        "duration": 2,
                        "description": "Trendy neighborhood dining and boutique browsing",
                        "cost": 65
                    },
                    "meals": {
                        "breakfast": "Hotel",
                        "lunch": "Dim sum in Chinatown",
                        "dinner": "Zuni Café"
                    },
                    "transportation": "Cable car, Muni, walking",
                    "estimated_cost": 165,
                    "notes": "Food tour includes tastings. Leave room for all the delicious stops!"
                },
                {
                    "day_number": 3,
                    "theme": "Views & Local Gems",
                    "morning": {
                        "time": "9:00 AM",
                        "location": "Lands End Trail",
                        "duration": 2,
                        "description": "Scenic coastal trail to Sutro Baths ruins",
                        "cost": 0
                    },
                    "afternoon": {
                        "time": "12:00 PM",
                        "location": "Tartine Bakery & Mission murals",
                        "duration": 3,
                        "description": "Famous bakery lunch, Clarion Alley street art",
                        "cost": 35
                    },
                    "evening": {
                        "time": "5:00 PM",
                        "location": "Twin Peaks sunset",
                        "duration": 2,
                        "description": "360° views of SF at golden hour, farewell dinner",
                        "cost": 80
                    },
                    "meals": {
                        "breakfast": "Café",
                        "lunch": "Tartine",
                        "dinner": "Foreign Cinema"
                    },
                    "transportation": "Uber/Lyft to Twin Peaks, walking",
                    "estimated_cost": 115,
                    "notes": "Check sunset time. Arrive 30min early at Twin Peaks for parking."
                }
            ]
        }
