"""
Conversation Agent - Orchestrates multi-turn dialogue
"""

from typing import Dict, List, Any, Optional, Tuple
from backend.agents.multi_provider_agent import MultiProviderAgent
from backend.conversation.state import ConversationContext, ConversationState
from loguru import logger
import json
import re


class ConversationAgent(MultiProviderAgent):
    """Manages conversational flow and information gathering"""
    
    def __init__(self):
        super().__init__("ConversationAgent")
        
        self.system_prompt = """You are a friendly, intelligent travel planning assistant. Your goal is to gather information from users to help plan their perfect trip.

Guidelines:
1. Be conversational and warm, not robotic
2. Ask ONE question at a time to avoid overwhelming users
3. If user provides clear information (like "tight budget of $100"), don't ask about budget - use that info
4. When user mentions country (like "France"), ask which cities they want to visit
5. Provide helpful context (opening hours, best times, prices) when recommending
6. If user gives complete info upfront, acknowledge it and move to planning
7. Use natural language, emojis occasionally 🎉

IMPORTANT: Once you have DESTINATION and DURATION (number of days), set next_action to "ready_to_plan"
- Don't keep asking endless questions
- After 2-3 exchanges, if you have destination and duration, you're ready
- Optional info (budget, interests) is nice but NOT required
- User responses like "ok", "great", "sounds good" mean they're ready to see the plan

Your responses should be in JSON format:
{
    "message": "Your conversational message to user",
    "question": "The specific question you're asking (null if no question)",
    "suggestions": ["Quick reply option 1", "Quick reply option 2"],  // optional
    "extracted_info": {"field": "value"},  // what you learned from this message
    "next_action": "gather_more" | "ready_to_plan"
}

Set next_action to "ready_to_plan" when:
- You have destination AND duration
- User says they're ready (ok, yes, great, sounds good, let's do it)
- You've asked more than 2 clarifying questions"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Required implementation for MultiProviderAgent"""
        # This is handled by process_message instead
        return {"success": True}

    async def process_message(
        self,
        user_message: str,
        context: ConversationContext
    ) -> Dict[str, Any]:
        """Process user message and decide next step"""
        
        logger.info(f"Processing message in conversation {context.conversation_id}")
        
        # Add user message to history
        context.add_message('user', user_message)
        
        # Build prompt with context
        prompt = self._build_prompt(user_message, context)
        
        # Get AI response
        response_text = await self._generate_response(prompt)
        
        # Parse AI response
        try:
            response = self._parse_json_response(response_text)
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            response = {
                "message": response_text,
                "question": None,
                "extracted_info": {},
                "next_action": "gather_more"
            }
        
        # Update context with extracted info
        if response.get('extracted_info'):
            context.update_profile(response['extracted_info'])
        
        # Force ready state if we have minimum requirements and user seems ready
        user_message_lower = user_message.lower()
        ready_phrases = ['ok', 'great', 'yes', 'sure', 'sounds good', 'let\'s do it', 'perfect', 'awesome']
        has_minimum = context.profile.get('destination') and context.profile.get('duration')
        user_seems_ready = any(phrase in user_message_lower for phrase in ready_phrases)
        
        # Override next_action if conditions met
        if has_minimum and (user_seems_ready or len(context.messages) > 8):
            response['next_action'] = 'ready_to_plan'
            response['message'] = "Perfect! I have everything I need. Click the 'Generate My Travel Plan' button below when you're ready to see your personalized itinerary! 🎉"
            response['question'] = None
        
        # Add agent response to history
        context.add_message('agent', response.get('message', ''), {
            'question': response.get('question'),
            'suggestions': response.get('suggestions', [])
        })
        
        # Update state
        if response.get('next_action') == 'ready_to_plan':
            context.state = ConversationState.FINALIZING
        elif context.completeness < 50:
            context.state = ConversationState.GATHERING_INFO
        else:
            context.state = ConversationState.CLARIFYING
        
        return response
    
    def _build_prompt(self, user_message: str, context: ConversationContext) -> str:
        """Build prompt with conversation context"""
        
        # Get conversation history (last 3 exchanges)
        recent_messages = context.messages[-6:] if len(context.messages) > 6 else context.messages
        history = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in recent_messages
        ])
        
        # Current profile state
        profile_summary = self._summarize_profile(context.profile)
        
        # Missing information
        missing = context.get_missing_info()
        
        prompt = f"""{self.system_prompt}

Current conversation:
{history}

USER: {user_message}

Current information gathered:
{profile_summary}

Missing required info: {', '.join(missing) if missing else 'None - ready to plan!'}

Questions already asked: {', '.join(context.questions_asked)}

Based on the conversation above, respond with JSON containing:
- A warm, conversational message
- A follow-up question if needed (or null if ready to plan)
- Quick reply suggestions if appropriate
- Any new information you extracted from user's message
- Whether you need more info or are ready to plan

Remember:
- If user said "tight budget" or gave specific amount, extract that - don't ask again
- If destination is clear, don't ask again
- If duration is clear, don't ask again
- Ask about missing required info first, then optional info
- Be helpful with opening hours and prices when discussing activities

Respond ONLY with valid JSON."""
        
        return prompt
    
    def _summarize_profile(self, profile: Dict[str, Any]) -> str:
        """Create human-readable summary of profile"""
        parts = []
        
        if profile.get('destination'):
            dest = profile['destination']
            if isinstance(dest, list):
                parts.append(f"Destinations: {', '.join(dest)}")
            else:
                parts.append(f"Destination: {dest}")
        
        if profile.get('duration'):
            parts.append(f"Duration: {profile['duration']} days")
        
        if profile.get('budget'):
            parts.append(f"Budget: {profile['budget']}")
        
        if profile.get('interests'):
            parts.append(f"Interests: {', '.join(profile['interests'])}")
        
        if profile.get('travel_style'):
            parts.append(f"Travel style: {profile['travel_style']}")
        
        return '\n'.join(parts) if parts else 'No information yet'
    
    async def generate_initial_greeting(self) -> str:
        """Generate friendly greeting to start conversation"""
        greetings = [
            "Hi! 👋 I'm your travel planning assistant. Where would you like to go?",
            "Hello! 🌍 I'm here to help plan your perfect trip. Tell me about your travel dreams!",
            "Hey there! ✈️ Ready to plan an amazing trip? Where are you thinking of going?",
        ]
        
        import random
        return random.choice(greetings)
    
    def should_ask_budget(self, context: ConversationContext) -> bool:
        """Check if we should ask about budget"""
        return (
            not context.profile.get('budget') and
            'budget' not in context.questions_asked and
            context.profile.get('destination') is not None
        )
    
    def should_ask_interests(self, context: ConversationContext) -> bool:
        """Check if we should ask about interests"""
        return (
            len(context.profile.get('interests', [])) == 0 and
            'interests' not in context.questions_asked and
            context.is_ready_to_plan()
        )
    
    def extract_budget_amount(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract budget information from text"""
        text_lower = text.lower()
        
        # Check for keywords
        if any(word in text_lower for word in ['tight', 'low', 'cheap', 'budget']):
            return {'budget': 'tight'}
        elif any(word in text_lower for word in ['luxury', 'high-end', 'expensive', 'lavish']):
            return {'budget': 'luxury'}
        elif any(word in text_lower for word in ['moderate', 'mid-range', 'average', 'normal']):
            return {'budget': 'moderate'}
        
        # Check for specific amounts
        amount_match = re.search(r'\$?(\d+(?:,\d+)?)', text)
        if amount_match:
            amount = int(amount_match.group(1).replace(',', ''))
            return {'budget': f'${amount}', 'budget_amount': amount}
        
        return None
    
    def extract_duration(self, text: str) -> Optional[int]:
        """Extract trip duration from text"""
        # Look for patterns like "5 days", "3 day", "week"
        day_match = re.search(r'(\d+)\s*days?', text.lower())
        if day_match:
            return int(day_match.group(1))
        
        # Look for just a number before "trip" or "day"
        trip_match = re.search(r'(\d+)\s*(?:day\s+)?trip', text.lower())
        if trip_match:
            return int(trip_match.group(1))
        
        if 'week' in text.lower():
            return 7
        elif 'weekend' in text.lower():
            return 3
        
        return None
