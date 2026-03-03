"""
Creates the clairos_email_chunks collection in local Qdrant.
Run once before ingestion.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from database.Schemas.config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_DIM

def create_collection():
    client = QdrantClient(url=QDRANT_URL)
    
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        print(f"✓ Collection '{COLLECTION_NAME}' already exists")
        return
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE
        )
    )
    print(f"✓ Created collection '{COLLECTION_NAME}' with {EMBEDDING_DIM} dimensions")

if __name__ == "__main__":
    create_collection()