"""
Embedding generation and management for RAG
"""

from typing import List
import openai
from backend.config import settings
from loguru import logger

# Initialize OpenAI client
openai.api_key = settings.OPENAI_API_KEY

class EmbeddingGenerator:
    """Generate embeddings for text using OpenAI's embedding model"""
    
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

# Global instance
embedding_generator = EmbeddingGenerator()
