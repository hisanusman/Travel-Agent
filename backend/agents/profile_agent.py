"""
Profile Agent - Handles user preferences and context
"""

from typing import Dict, Any
from backend.agents.multi_provider_agent import MultiProviderAgent
from loguru import logger

class ProfileAgent(MultiProviderAgent):
    """Agent responsible for managing user preferences and trip context"""
    
    def __init__(self):
        super().__init__(name="ProfileAgent")
        self.profile_prompt = """
You are a travel preferences expert. Analyze the user's travel request and extract key information.

User Request: {user_request}

Extract and structure the following information in JSON format:
- destination: Primary destination(s)
- duration: Number of days
- dates: Preferred travel dates (if mentioned)
- budget_level: "budget", "moderate", or "luxury"
- interests: List of travel interests (culture, food, adventure, relaxation, etc.)
- travel_style: Type of traveler (solo, couple, family, group)
- special_requirements: Any special needs or requirements
- preferences: Any other preferences mentioned

Return ONLY a valid JSON object with these fields.
"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and extract travel preferences
        
        Args:
            input_data: Dict with 'user_request' key containing the user's travel query
            
        Returns:
            Structured profile data
        """
        try:
            user_request = input_data.get('user_request', '')
            logger.info(f"ProfileAgent processing request: {user_request[:100]}...")
            
            # Generate prompt
            prompt = self._create_prompt(
                self.profile_prompt,
                user_request=user_request
            )
            
            # Get response from model
            response = await self._generate_response(prompt)
            
            # Parse JSON response
            profile_data = self._parse_json_response(response)
            
            logger.info(f"ProfileAgent extracted profile: {profile_data}")
            
            return {
                'success': True,
                'agent': self.name,
                'profile': profile_data
            }
            
        except Exception as e:
            logger.error(f"Error in ProfileAgent: {e}")
            return {
                'success': False,
                'agent': self.name,
                'error': str(e)
            }
    
    async def update_profile(self, current_profile: Dict[str, Any], update_request: str) -> Dict[str, Any]:
        """Update existing profile based on new user input"""
        try:
            prompt = f"""
Current travel profile:
{current_profile}

User wants to update: {update_request}

Return the UPDATED profile as a JSON object with the same structure, incorporating the requested changes.
"""
            response = await self._generate_response(prompt)
            updated_profile = self._parse_json_response(response)
            
            return {
                'success': True,
                'profile': updated_profile
            }
            
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return {
                'success': False,
                'error': str(e)
            }
