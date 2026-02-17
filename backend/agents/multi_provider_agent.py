"""
Multi-provider agent with automatic fallback
Tries OpenAI/Google first, falls back to Groq if they fail
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.config import settings
from loguru import logger
from groq import Groq
import openai
from google import genai

class MultiProviderAgent(ABC):
    """Base class with multi-provider support and automatic fallback"""
    
    def __init__(self, name: str):
        self.name = name
        
        # Initialize all available clients
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.google_client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Provider configurations
        self.providers = [
            {
                'name': 'OpenAI',
                'model': 'gpt-4o-mini',
                'client': self.openai_client,
                'type': 'openai'
            },
            {
                'name': 'Google',
                'model': 'gemini-2.5-flash',
                'client': self.google_client,
                'type': 'google'
            },
            {
                'name': 'Groq',
                'model': 'llama-3.3-70b-versatile',
                'client': self.groq_client,
                'type': 'groq'
            }
        ]
        
        logger.info(f"Initialized {name} with multi-provider support (OpenAI → Google → Groq)")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    def _create_prompt(self, template: str, **kwargs) -> str:
        """Create a formatted prompt from template and arguments"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing key in prompt template: {e}")
            raise
    
    async def _generate_response(self, prompt: str) -> str:
        """
        Generate response with automatic fallback
        Tries providers in order until one succeeds
        """
        last_error = None
        
        for provider in self.providers:
            try:
                logger.info(f"{self.name} trying {provider['name']}...")
                
                if provider['type'] == 'openai':
                    response = self.openai_client.chat.completions.create(
                        model=provider['model'],
                        messages=[
                            {"role": "system", "content": "You are a helpful travel planning assistant. Always respond with valid JSON when requested."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )
                    result = response.choices[0].message.content
                    logger.info(f"✅ {provider['name']} succeeded")
                    return result
                
                elif provider['type'] == 'google':
                    response = provider['client'].models.generate_content(
                        model=provider['model'],
                        contents=prompt
                    )
                    result = response.text
                    logger.info(f"✅ {provider['name']} succeeded")
                    return result
                
                elif provider['type'] == 'groq':
                    response = provider['client'].chat.completions.create(
                        model=provider['model'],
                        messages=[
                            {"role": "system", "content": "You are a helpful travel planning assistant. Always respond with valid JSON when requested."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    result = response.choices[0].message.content
                    logger.info(f"✅ {provider['name']} succeeded")
                    return result
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"❌ {provider['name']} failed: {error_msg[:100]}...")
                last_error = e
                continue
        
        # If all providers failed
        logger.error(f"All providers failed for {self.name}")
        raise Exception(f"All AI providers failed. Last error: {last_error}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from model response"""
        import json
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                response = response[start:end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            logger.error(f"Response was: {response[:200]}")
            raise
