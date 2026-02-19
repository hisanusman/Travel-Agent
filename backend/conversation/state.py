"""
Conversation State Management
Stores context between turns in a conversation
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json

class ConversationState(str, Enum):
    """States in the conversation flow"""
    INITIAL = "initial"
    GATHERING_INFO = "gathering_info"
    CLARIFYING = "clarifying"
    RECOMMENDING = "recommending"
    REFINING = "refining"
    FINALIZING = "finalizing"
    COMPLETED = "completed"

class ConversationContext:
    """Manages conversation state and extracted information"""
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.state = ConversationState.INITIAL
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Message history
        self.messages: List[Dict[str, Any]] = []
        
        # Extracted information (progressively filled)
        self.profile = {
            'destination': None,  # city name or list of cities
            'duration': None,  # number of days
            'budget': None,  # 'tight'/'moderate'/'luxury' or specific amount
            'budget_per_night': None,  # calculated if total budget given
            'interests': [],  # list of interests
            'dates': None,  # specific dates or season
            'travel_style': None,  # solo/couple/family/group
            'special_requirements': [],  # any special needs
        }
        
        # Questions asked (to avoid repeating)
        self.questions_asked = []
        
        # Information completeness score (0-100)
        self.completeness = 0
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to history"""
        message = {
            'role': role,  # 'user' or 'agent'
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def update_profile(self, updates: Dict[str, Any]):
        """Update profile information"""
        # Ensure duration is an integer
        if 'duration' in updates:
            duration_value = updates['duration']
            if isinstance(duration_value, str):
                # Try to extract number from strings like "5 days"
                import re
                match = re.search(r'(\d+)', duration_value)
                if match:
                    updates['duration'] = int(match.group(1))
        
        self.profile.update(updates)
        self.updated_at = datetime.now()
        self._calculate_completeness()
    
    def _calculate_completeness(self) -> int:
        """Calculate how much information we have (0-100)"""
        required_fields = ['destination', 'duration']
        optional_fields = ['budget', 'interests', 'dates', 'travel_style']
        
        score = 0
        
        # Required fields: 40% each = 80%
        for field in required_fields:
            if self.profile.get(field):
                score += 40
        
        # Optional fields: 5% each = 20%
        for field in optional_fields:
            value = self.profile.get(field)
            if value and (isinstance(value, list) and len(value) > 0 or value):
                score += 5
        
        self.completeness = min(score, 100)
        return self.completeness
    
    def get_missing_info(self) -> List[str]:
        """Get list of missing required information"""
        missing = []
        
        if not self.profile.get('destination'):
            missing.append('destination')
        if not self.profile.get('duration'):
            missing.append('duration')
        
        return missing
    
    def is_ready_to_plan(self) -> bool:
        """Check if we have enough info to generate a plan"""
        return len(self.get_missing_info()) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'conversation_id': self.conversation_id,
            'state': self.state.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': self.messages,
            'profile': self.profile,
            'questions_asked': self.questions_asked,
            'completeness': self.completeness
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationContext':
        """Deserialize from dictionary"""
        context = cls(data['conversation_id'])
        context.state = ConversationState(data['state'])
        context.created_at = datetime.fromisoformat(data['created_at'])
        context.updated_at = datetime.fromisoformat(data['updated_at'])
        context.messages = data['messages']
        context.profile = data['profile']
        context.questions_asked = data['questions_asked']
        context.completeness = data['completeness']
        return context


# In-memory storage (will be replaced with DB in production)
_conversations: Dict[str, ConversationContext] = {}

def get_conversation(conversation_id: str) -> Optional[ConversationContext]:
    """Retrieve a conversation by ID"""
    return _conversations.get(conversation_id)

def save_conversation(context: ConversationContext):
    """Save conversation context"""
    _conversations[context.conversation_id] = context

def create_conversation() -> ConversationContext:
    """Create a new conversation"""
    import uuid
    conversation_id = str(uuid.uuid4())
    context = ConversationContext(conversation_id)
    save_conversation(context)
    return context
