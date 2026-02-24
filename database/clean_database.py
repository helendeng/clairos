"""
Clean/Reset Qdrant Database
Deletes all data and recreates collection from scratch
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_DIM

def clean_database():
    """Delete and recreate collection - removes all data"""
    
    print("=" * 70)
    print("CLEAN QDRANT DATABASE")
    print("=" * 70)
    print()
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✓ Connected to Qdrant")
    print(f"  Collection: {COLLECTION_NAME}")
    print()
    
    # Check if collection exists
    try:
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME in collection_names:
            # Get current count
            info = client.get_collection(COLLECTION_NAME)
            current_count = info.points_count
            
            print(f"Current collection has {current_count} chunks")
            print()
            
            # Confirm deletion
            if current_count > 0:
                response = input(f"⚠️  Delete all {current_count} chunks? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    print("Cancelled - no data deleted")
                    return False
            
            # Delete collection
            print("Deleting collection...")
            client.delete_collection(collection_name=COLLECTION_NAME)
            print(f"✓ Deleted collection '{COLLECTION_NAME}'")
            print()
        else:
            print(f"Collection '{COLLECTION_NAME}' doesn't exist (nothing to delete)")
            print()
    
    except Exception as e:
        print(f"⚠️  Error checking collection: {e}")
        print("Proceeding to create new collection...")
        print()
    
    # Create fresh collection
    print("Creating fresh collection...")
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
        
        print(f"✓ Created collection '{COLLECTION_NAME}'")
        print(f"  Vector size: {EMBEDDING_DIM}")
        print(f"  Distance metric: COSINE")
        print(f"  Points count: 0")
        print()
        
        print("=" * 70)
        print("✓ DATABASE CLEANED!")
        print("=" * 70)
        print()
        print("Collection is now empty and ready for fresh data.")
        print("Run main.py to upload test chunks.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating collection: {e}")
        return False


def view_current_data():
    """View what's currently in the database"""
    
    print("=" * 70)
    print("CURRENT DATABASE CONTENTS")
    print("=" * 70)
    print()
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    try:
        # Get collection info
        info = client.get_collection(COLLECTION_NAME)
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Total chunks: {info.points_count}")
        print()
        
        if info.points_count == 0:
            print("Database is empty - no data to show")
            return
        
        # Get sample of data
        result = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        
        points = result[0]
        
        # Count by subdomain
        from collections import Counter
        subdomain_counts = Counter(p.payload.get('subdomain') for p in points)
        
        print("Chunks by subdomain:")
        print("-" * 70)
        for subdomain, count in sorted(subdomain_counts.items()):
            print(f"  {subdomain:30} | {count:3} chunks")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Collection may not exist - run fix_collection.py first")


def main():
    """Main menu"""
    
    print()
    print("=" * 70)
    print("QDRANT DATABASE CLEANER")
    print("=" * 70)
    print()
    print("What would you like to do?")
    print()
    print("  1. View current data")
    print("  2. Clean database (delete all and recreate)")
    print("  3. Exit")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print()
        view_current_data()
    
    elif choice == "2":
        print()
        clean_database()
    
    elif choice == "3":
        print("Goodbye!")
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()