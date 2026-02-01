"""
Embedding service to convert text into vectors
Used by ingest_chunks.py
"""

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"✓ Loaded embedding model: {EMBEDDING_MODEL}")
    
    def embed(self, text: str) -> list:
        """Generate embedding for a single text"""
        return self.model.encode(text).tolist()
    
    def embed_batch(self, texts: list) -> list:
        """Generate embeddings for multiple texts (faster)"""
        return self.model.encode(texts).tolist()
    