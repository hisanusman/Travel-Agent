"""
Destination Agent - Retrieves POIs, attractions, and local tips using RAG
"""

from typing import Dict, Any, List
from backend.agents.multi_provider_agent import MultiProviderAgent
from backend.rag.retrieval import travel_retriever
from loguru import logger

class DestinationAgent(MultiProviderAgent):
    """Agent responsible for gathering destination information"""
    
    def __init__(self):
        super().__init__(name="DestinationAgent")
        self.destination_prompt = """
You are a destination expert with deep knowledge about {destination}.

Based on the following context from travel guides:
{context}

And considering the traveler profile:
- Budget Level: {budget_level}
- Interests: {interests}
- Duration: {duration} days
- Travel Style: {travel_style}

Provide a comprehensive destination overview in JSON format with:
- top_attractions: List of must-see places (name, description, estimated_time, cost_level)
- local_experiences: Authentic local activities
- restaurants: Recommended dining options
- neighborhoods: Best areas to explore
- transportation: Getting around options
- local_tips: Important tips for visitors
- hidden_gems: Off-the-beaten-path recommendations

Return ONLY a valid JSON object.
"""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process destination query and return recommendations with full database options
        
        Args:
            input_data: Dict with profile information and destination
            
        Returns:
            Destination recommendations with selectable options
        """
        try:
            profile = input_data.get('profile', {})
            destination = profile.get('destination', 'unknown')
            
            # Handle list destinations (e.g., ['Maldives', 'islands'])
            if isinstance(destination, list):
                destination = destination[0] if destination else 'unknown'
            
            logger.info(f"DestinationAgent processing destination: {destination}")
            
            # Get full destination data from local database
            dest_data = travel_retriever.get_destination_data(destination)
            
            # If we have rich local data, use it directly
            if dest_data and any(dest_data.values()):
                logger.info(f"✅ Using rich local database for {destination}")
                return {
                    'success': True,
                    'agent': self.name,
                    'destination': destination,
                    'accommodations': dest_data.get('accommodations', []),
                    'activities': dest_data.get('activities', []),
                    'restaurants': dest_data.get('restaurants', []),
                    'has_detailed_options': True
                }
            
            # Fallback to AI-generated recommendations if no local data
            logger.info(f"No local data for {destination}, generating with AI...")
            context_docs = self._retrieve_context(destination, profile)
            context_text = self._format_context(context_docs)
            
            # Generate prompt
            prompt = self._create_prompt(
                self.destination_prompt,
                destination=destination,
                context=context_text,
                budget_level=profile.get('budget_level', 'moderate'),
                interests=', '.join(profile.get('interests', [])) if isinstance(profile.get('interests', []), list) else str(profile.get('interests', '')),
                duration=profile.get('duration', 'N/A'),
                travel_style=profile.get('travel_style', 'general')
            )
            
            # Get response from model
            response = await self._generate_response(prompt)
            
            # Parse JSON response
            destination_data = self._parse_json_response(response)
            
            logger.info(f"DestinationAgent generated AI recommendations for {destination}")
            
            return {
                'success': True,
                'agent': self.name,
                'destination': destination,
                'recommendations': destination_data,
                'has_detailed_options': False
            }
            
        except Exception as e:
            logger.error(f"Error in DestinationAgent: {e}")
            return {
                'success': False,
                'agent': self.name,
                'error': str(e)
            }
    
    def _retrieve_context(self, destination: str, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector database"""
        try:
            # Build search query
            interests = profile.get('interests', [])
            query = f"{destination} {' '.join(interests)} attractions restaurants things to do"
            
            # Retrieve from Pinecone
            docs = travel_retriever.retrieve(
                query=query,
                top_k=5,
                filter_dict={'destination': destination} if destination else None
            )
            
            return docs
            
        except Exception as e:
            logger.warning(f"Could not retrieve context from RAG: {e}")
            return []
    
    def _format_context(self, docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string"""
        if not docs:
            return "No specific guide information available. Use general knowledge."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            metadata = doc.get('metadata', {})
            text = metadata.get('text', metadata.get('content', 'N/A'))
            context_parts.append(f"{i}. {text}")
        
        return "\n\n".join(context_parts)
