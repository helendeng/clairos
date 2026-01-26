"""
Visualize and test  Qdrant database
Run this to see what chunks are stored and test basic retrieval
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_MODEL
import pandas as pd

class DatabaseVisualizer:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
    def get_collection_info(self):
        """Display basic collection information"""
        print("=" * 70)
        print("COLLECTION INFORMATION")
        print("=" * 70)
        
        info = self.client.get_collection(COLLECTION_NAME)
        print(f"Collection Name: {COLLECTION_NAME}")
        print(f"Vector Size: {info.config.params.vectors.size}")
        print(f"Distance Metric: {info.config.params.vectors.distance}")
        print(f"Total Points (Chunks): {info.points_count}")
        print()
    
    def view_all_chunks(self):
        """Display all chunks in the database"""
        print("=" * 70)
        print("ALL STORED CHUNKS")
        print("=" * 70)
        
        # Scroll through all points
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        
        points = result[0]
        
        if not points:
            print("⚠️  No chunks found in database!")
            print("   Run main.py to upload some chunks first.")
            return []
        
        # Create a readable table
        data = []
        for point in points:
            data.append({
                'Chunk ID': point.payload.get('chunk_id', 'N/A'),
                'Domain': point.payload.get('domain', 'N/A'),
                'Subdomain': point.payload.get('subdomain', 'N/A'),
                'Text Preview': point.payload.get('text', '')[:80] + '...'
            })
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        print(f"\nTotal chunks: {len(points)}")
        print()
        
        return points
    
    def view_chunk_detail(self, chunk_id):
        """View full details of a specific chunk"""
        print("=" * 70)
        print(f"CHUNK DETAIL: {chunk_id}")
        print("=" * 70)
        
        # Get all points and search through them
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Find the chunk manually
        found_chunk = None
        for point in points:
            if point.payload.get('chunk_id') == chunk_id:
                found_chunk = point
                break
        
        if not found_chunk:
            print(f"❌ Chunk '{chunk_id}' not found!")
            print(f"Available chunks: {[p.payload.get('chunk_id') for p in points]}")
            return
        
        chunk = found_chunk.payload
        print(f"Chunk ID: {chunk.get('chunk_id')}")
        print(f"Domain: {chunk.get('domain')}")
        print(f"Subdomain: {chunk.get('subdomain')}")
        print(f"\nFull Text:")
        print("-" * 70)
        print(chunk.get('text', 'N/A'))
        print("-" * 70)
        print()
    
    def test_semantic_search(self, query, top_k=3):
        """Test semantic search with a query"""
        print("=" * 70)
        print(f"SEMANTIC SEARCH TEST")
        print("=" * 70)
        print(f"Query: '{query}'")
        print(f"Top {top_k} results:\n")
        
        # Generate query embedding
        query_vector = self.embedding_model.encode(query).tolist()
        
        # FIXED: Use query() instead of search()
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k
        )
        
        # Handle the results - they're in results.points
        if not results.points:
            print("❌ No results found!")
            return
        
        for i, result in enumerate(results.points, 1):
            print(f"Result {i}:")
            print(f"  Chunk ID: {result.payload.get('chunk_id')}")
            print(f"  Domain: {result.payload.get('domain')}")
            print(f"  Similarity Score: {result.score:.4f}")
            print(f"  Text: {result.payload.get('text', '')[:100]}...")
            print()
    
    def test_keyword_search(self, keyword):
        """Test keyword search by looking through all chunks"""
        print("=" * 70)
        print(f"KEYWORD SEARCH TEST")
        print("=" * 70)
        print(f"Keyword: '{keyword}'\n")
        
        # Get all chunks
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Filter manually for keyword
        matching_points = [
            p for p in points 
            if keyword.lower() in p.payload.get('text', '').lower()
        ]
        
        if not matching_points:
            print(f"❌ No chunks containing '{keyword}' found!")
            return
        
        print(f"Found {len(matching_points)} chunks containing '{keyword}':\n")
        for i, point in enumerate(matching_points, 1):
            print(f"Result {i}:")
            print(f"  Chunk ID: {point.payload.get('chunk_id')}")
            print(f"  Domain: {point.payload.get('domain')}")
            print(f"  Text: {point.payload.get('text', '')[:100]}...")
            print()
    
    def test_domain_filter(self, domain):
        """Test filtering by domain"""
        print("=" * 70)
        print(f"DOMAIN FILTER TEST")
        print("=" * 70)
        print(f"Domain: '{domain}'\n")
        
        # Get all chunks
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Filter manually by domain
        matching_points = [
            p for p in points 
            if p.payload.get('domain') == domain
        ]
        
        if not matching_points:
            print(f"❌ No chunks in domain '{domain}' found!")
            available_domains = set(p.payload.get('domain') for p in points)
            print(f"Available domains: {available_domains}")
            return
        
        print(f"Found {len(matching_points)} chunks in domain '{domain}':\n")
        for point in matching_points:
            print(f"  - {point.payload.get('chunk_id')}: {point.payload.get('subdomain')}")
        print()

def main():
    """Run all visualization and tests"""
    viz = DatabaseVisualizer()
    
    # 1. Show collection info
    viz.get_collection_info()
    
    # 2. View all chunks
    viz.view_all_chunks()
    
    # 3. View detail of a specific chunk
    viz.view_chunk_detail("scheduling_001")
    
    # 4. Test semantic search
    viz.test_semantic_search("What is the meeting time?")
    
    # 5. Test keyword search
    viz.test_keyword_search("meeting")
    
    # 6. Test domain filtering
    viz.test_domain_filter("scheduling")
    
    print("=" * 70)
    print("✓ Visualization and testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()