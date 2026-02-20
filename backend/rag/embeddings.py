"""
Generate embeddings using sentence-transformers (local, no API needed)
"""

from typing import List
from sentence_transformers import SentenceTransformer
from loguru import logger

class EmbeddingGenerator:
    """Generate embeddings using local transformer model"""
    
    def __init__(self):
        # Use fast, efficient model (384 dimensions)
        self.model_name = "all-MiniLM-L6-v2"
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.dimension = 384
        logger.info(f"✅ Embedding model loaded (dimension: {self.dimension})")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text
        
        Args:
            text: Input text
            
        Returns:
            List of floats representing the embedding
        """
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * self.dimension
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient)
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [[0.0] * self.dimension] * len(texts)

# Global instance
embedding_generator = EmbeddingGenerator()
