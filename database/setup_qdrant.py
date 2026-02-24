"""
Setup Qdrant collection for ClairOS email chunks
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_DIM

def delete_collection_if_exists():
    """Delete existing collection to start fresh"""
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME in collection_names:
            print(f"⚠️  Collection '{COLLECTION_NAME}' already exists")
            print(f"🗑️  Deleting existing collection...")
            client.delete_collection(collection_name=COLLECTION_NAME)
            print(f"✓ Collection deleted")
        else:
            print(f"✓ No existing collection found")
    except Exception as e:
        print(f"Error checking/deleting collection: {e}")

def create_collection():
    """Create fresh Qdrant collection"""
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    print(f"\n{'='*70}")
    print(f"Creating collection: {COLLECTION_NAME}")
    print(f"Vector dimension: {EMBEDDING_DIM}")
    print(f"{'='*70}\n")
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE
        )
    )
    
    print(f"✓ Collection '{COLLECTION_NAME}' created successfully!\n")

if __name__ == "__main__":
    print("="*70)
    print("QDRANT COLLECTION SETUP")
    print("="*70)
    
    # Delete existing collection first
    delete_collection_if_exists()
    
    # Create fresh collection
    create_collection()
    
    print("="*70)
    print("✓ Setup complete!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Run main.py to ingest test chunks")
    print("  2. Run visualize_database.py to verify")