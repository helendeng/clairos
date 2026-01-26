"""
ONE-TIME SETUP: Create Qdrant collection
Run this file once, then you don't need it again
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_DIM

def create_collection():
    """Create Qdrant collection for email chunks"""
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Create collection with vector configuration
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE
        )
    )
    
    print(f"✓ Collection '{COLLECTION_NAME}' created successfully")
    print(f"  - Vector size: {EMBEDDING_DIM}")
    print(f"  - Distance metric: COSINE")

if __name__ == "__main__":
    create_collection()