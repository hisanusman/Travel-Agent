"""
Budget Agent - Estimates costs and optimizes expenses
"""

from typing import Dict, Any
from backend.agents.multi_provider_agent import MultiProviderAgent
from loguru import logger

class BudgetAgent(MultiProviderAgent):
    """Agent responsible for budget estimation and cost optimization"""
    
    def __init__(self):
        super().__init__(name="BudgetAgent")
        self.budget_prompt = """
You are a travel budget expert for {destination}.

Trip Details:
- Duration: {duration} days
- Budget Level: {budget_level}
- Number of travelers: {travelers}
- Planned activities: {activities}
- Accommodation preferences: {accommodation}

Provide a detailed budget breakdown in JSON format:
- accommodation: Daily cost and total (hotel name suggestions, type)
- meals: Daily food budget breakdown (breakfast, lunch, dinner)
- transportation: Local transport costs (metro, taxi, etc.)
- activities: Cost for each planned activity
- miscellaneous: Other expenses (tips, souvenirs, etc.)
- total_estimated: Total trip cost
- daily_average: Average daily spending
- budget_tips: Tips to save money or splurge wisely
- cost_comparison: How this compares to typical costs

Return ONLY a valid JSON object with all costs in USD.
"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process budget query and provide cost estimates
        
        Args:
            input_data: Dict with trip details and preferences
            
        Returns:
            Budget breakdown and recommendations
        """
        try:
            profile = input_data.get('profile', {})
            destination = profile.get('destination', 'unknown')
            activities = input_data.get('activities', [])
            
            logger.info(f"BudgetAgent processing budget for: {destination}")
            
            # Generate prompt
            prompt = self._create_prompt(
                self.budget_prompt,
                destination=destination,
                duration=profile.get('duration', 7),
                budget_level=profile.get('budget_level', 'moderate'),
                travelers=1,  # Can be updated based on travel_style
                activities=self._format_activities(activities),
                accommodation=self._get_accommodation_pref(profile.get('budget_level', 'moderate'))
            )
            
            # Get response from model
            response = await self._generate_response(prompt)
            
            # Parse JSON response
            budget_data = self._parse_json_response(response)
            
            logger.info(f"BudgetAgent generated budget for {destination}")
            
            return {
                'success': True,
                'agent': self.name,
                'destination': destination,
                'budget': budget_data
            }
            
        except Exception as e:
            logger.error(f"Error in BudgetAgent: {e}")
            return {
                'success': False,
                'agent': self.name,
                'error': str(e)
            }
    
    def _format_activities(self, activities: list) -> str:
        """Format activities list for prompt"""
        if not activities:
            return "Standard sightseeing activities"
        return ", ".join([act.get('name', str(act)) for act in activities])
    
    def _get_accommodation_pref(self, budget_level: str) -> str:
        """Get accommodation preference based on budget level"""
        prefs = {
            'budget': 'Hostels, budget hotels, or Airbnb',
            'moderate': '3-star hotels or mid-range Airbnb',
            'luxury': '4-5 star hotels or luxury accommodations'
        }
        return prefs.get(budget_level, 'Mid-range options')
