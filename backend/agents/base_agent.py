"""
Base agent class for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.config import settings
from loguru import logger
from huggingface_hub import InferenceClient

# Use Hugging Face - completely free, no API key limits!
hf_client = InferenceClient(token=None)  # Public models don't need token

class BaseAgent(ABC):
    """Base class for all travel planning agents"""
    
    def __init__(self, name: str, model_name: str = "meta-llama/Llama-3.2-3B-Instruct"):
        self.name = name
        self.model_name = model_name
        self.client = hf_client
        logger.info(f"Initialized {name} agent with model {model_name}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and return results
        
        Args:
            input_data: Input data specific to the agent
            
        Returns:
            Dictionary with agent's output
        """
        pass
    
    def _create_prompt(self, template: str, **kwargs) -> str:
        """Create a formatted prompt from template and arguments"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing key in prompt template: {e}")
            raise
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response from the model"""
        try:
            # Use Hugging Face Inference API - completely free!
            response = self.client.chat_completion(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response in {self.name}: {e}")
            raise
    
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
