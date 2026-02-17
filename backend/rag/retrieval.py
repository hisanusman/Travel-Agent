"""
Vector retrieval using Pinecone for travel knowledge
"""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from backend.config import settings
from backend.rag.embeddings import embedding_generator
from loguru import logger
import time

class TravelKnowledgeRetriever:
    """Retrieve relevant travel information using Pinecone vector database"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.dimension = 1536  # OpenAI ada-002 embedding dimension
        
        # Initialize or connect to index
        self._init_index()
    
    def _init_index(self):
        """Initialize Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            existing_names = [idx['name'] for idx in existing_indexes.get('indexes', [])]
            
            if self.index_name not in existing_names:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec={
                        "serverless": {
                            "cloud": "aws",
                            "region": "us-east-1"
                        }
                    }
                )
                # Wait for index to be ready
                time.sleep(1)
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.warning(f"Pinecone index initialization issue (non-critical): {e}")
            # Create a dummy index for now
            self.index = None
    
    def add_documents(self, documents: List[Dict[str, Any]], namespace: str = "travel-guides"):
        """
        Add documents to the vector database
        
        Args:
            documents: List of documents with 'id', 'text', and 'metadata' fields
            namespace: Pinecone namespace for organizing vectors
        """
        try:
            vectors = []
            for doc in documents:
                # Generate embedding for document text
                embedding = embedding_generator.generate_embedding(doc['text'])
                
                vectors.append({
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': doc.get('metadata', {})
                })
            
            # Upsert vectors in batches of 100
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch, namespace=namespace)
            
            logger.info(f"Added {len(documents)} documents to Pinecone")
            
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {e}")
            raise
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        namespace: str = "travel-guides",
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on query
        
        Args:
            query: Search query text
            top_k: Number of results to return
            namespace: Pinecone namespace to search in
            filter_dict: Optional metadata filters
            
        Returns:
            List of relevant documents with scores
        """
        try:
            if not self.index:
                logger.warning("Pinecone index not available, returning empty results")
                return []
            
            # Generate query embedding
            query_embedding = embedding_generator.generate_embedding(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=namespace,
                filter=filter_dict,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results['matches']:
                documents.append({
                    'id': match['id'],
                    'score': match['score'],
                    'metadata': match.get('metadata', {})
                })
            
            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.warning(f"Error retrieving documents (non-critical): {e}")
            return []
    
    def delete_namespace(self, namespace: str):
        """Delete all vectors in a namespace"""
        try:
            self.index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Deleted namespace: {namespace}")
        except Exception as e:
            logger.error(f"Error deleting namespace: {e}")
            raise

# Global retriever instance
travel_retriever = TravelKnowledgeRetriever()
