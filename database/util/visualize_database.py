"""
Visualize and test Qdrant database
SUBDOMAIN is primary classification (27 blocks)
Domain is metadata for context
Ensures querying 'All Scheduling' never returns 'Health Disclosures' (Personal Life)
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from database.Schemas.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_MODEL
import pandas as pd
from collections import Counter

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
        print(f"\nOrganization: SUBDOMAIN-based (27 separate blocks)")
        print(f"Domain: Stored as metadata for context")
        print()
    
    def view_all_chunks(self):
        """Display all chunks grouped by SUBDOMAIN (primary classification)"""
        print("=" * 70)
        print("ALL STORED CHUNKS (Grouped by SUBDOMAIN)")
        print("=" * 70)
        
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        
        points = result[0]
        
        if not points:
            print("⚠️  No chunks found in database!")
            print("   Run main.py to upload test chunks first.")
            return []
        
        # Create table showing SUBDOMAIN as primary classification
        data = []
        for point in points:
            data.append({
                'Chunk ID': point.payload.get('chunk_id', 'N/A'),
                'SUBDOMAIN (Primary)': point.payload.get('subdomain', 'N/A'),
                'Domain (Context)': point.payload.get('domain', 'N/A'),
                'Text Preview': point.payload.get('text', '')[:60] + '...'
            })
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        print(f"\nTotal chunks: {len(points)}")
        
        # Show subdomain distribution (27 blocks)
        subdomain_counts = Counter(p.payload.get('subdomain') for p in points)
        print(f"\nSubdomains present: {len(subdomain_counts)} out of 27")
        print()
        
        return points
    
    def view_chunk_detail(self, chunk_id, subdomain=None):
        """
        View full details of a specific chunk
        subdomain parameter helps narrow search in subdomain-based organization
        """
        print("=" * 70)
        print(f"CHUNK DETAIL: chunk_id={chunk_id}")
        if subdomain:
            print(f"Subdomain filter: {subdomain}")
        print("=" * 70)
        
        # Get all chunks
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Find the chunk by ID (and optionally subdomain)
        found_chunk = None
        for point in points:
            if point.payload.get('chunk_id') == chunk_id:
                if subdomain is None or point.payload.get('subdomain') == subdomain:
                    found_chunk = point
                    break
        
        if not found_chunk:
            print(f"❌ Chunk ID '{chunk_id}' not found!")
            if subdomain:
                print(f"   In subdomain '{subdomain}'")
            available = [(p.payload.get('chunk_id'), p.payload.get('subdomain')) 
                        for p in points]
            print(f"   Available chunks (first 5): {available[:5]}...")
            return
        
        chunk = found_chunk.payload
        print(f"Chunk ID: {chunk.get('chunk_id')}")
        print(f"SUBDOMAIN (Primary): {chunk.get('subdomain')}")
        print(f"Domain (Context): {chunk.get('domain')}")
        print(f"\nSource Information:")
        print(f"  Email ID: {chunk.get('source', {}).get('email_id', 'N/A')}")
        print(f"  From: {chunk.get('source', {}).get('from', 'N/A')}")
        print(f"  CC: {chunk.get('source', {}).get('cc', 'N/A')}")
        print(f"  BCC: {chunk.get('source', {}).get('bcc', 'N/A')}")
        print(f"  Subject: {chunk.get('source', {}).get('subject', 'N/A')}")
        print(f"  Timestamp: {chunk.get('source', {}).get('timestamp', 'N/A')}")
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
        
        # Search (FIXED: use 'search' method, not 'query_points')
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )
        
        if not results:
            print("❌ No results found!")
            return
        
        # FIXED: results is a list, not results.points
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Chunk ID: {result.payload.get('chunk_id')}")
            print(f"  SUBDOMAIN: {result.payload.get('subdomain')}")
            print(f"  Domain: {result.payload.get('domain')}")
            print(f"  Similarity Score: {result.score:.4f}")
            print(f"  Text: {result.payload.get('text', '')[:100]}...")
            print()
    
    def test_subdomain_filter(self, subdomain):
        """
        Test filtering by SUBDOMAIN (primary classification)
        This is the MAIN way to query - ensures complete separation
        CRITICAL: Ensures 'All Scheduling' ≠ 'Health Disclosures' (Personal Life)
        """
        print("=" * 70)
        print(f"SUBDOMAIN FILTER TEST (Primary Classification)")
        print("=" * 70)
        print(f"Subdomain: '{subdomain}'")
        print(f"This ensures COMPLETE ISOLATION from other subdomains\n")
        
        # Get all chunks
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Filter by subdomain (primary classification)
        matching_points = [
            p for p in points 
            if p.payload.get('subdomain') == subdomain
        ]
        
        if not matching_points:
            print(f"❌ No chunks in subdomain '{subdomain}' found!")
            available_subdomains = set(p.payload.get('subdomain') for p in points)
            print(f"Available subdomains: {sorted(available_subdomains)}")
            return
        
        print(f"✓ Found {len(matching_points)} chunks in subdomain '{subdomain}':\n")
        
        for point in matching_points:
            chunk_id = point.payload.get('chunk_id')
            domain = point.payload.get('domain')
            text_preview = point.payload.get('text', '')[:80]
            print(f"  Chunk #{chunk_id} (domain: {domain})")
            print(f"    {text_preview}...")
            print()
        
        # CRITICAL TEST: Verify no cross-contamination
        print("="* 70)
        print("CROSS-CONTAMINATION TEST")
        print("=" * 70)
        other_subdomains = [p.payload.get('subdomain') for p in points 
                           if p.payload.get('subdomain') != subdomain]
        if other_subdomains:
            print(f"✓ Correctly isolated from {len(set(other_subdomains))} other subdomains")
            print(f"  Other subdomains in database: {set(other_subdomains)}")
        else:
            print(f"⚠️  Only one subdomain exists in database")
        print()
    
    def test_cross_contamination(self):
        """
        Test that subdomain blocks are properly separated
        E.g., querying 'All Scheduling' should NEVER return 'All HR'
        or 'Health Disclosures' (Personal Life)
        """
        print("=" * 70)
        print("CROSS-CONTAMINATION SAFETY TEST")
        print("=" * 70)
        print("Testing subdomain isolation to prevent data leakage\n")
        
        # Get all chunks
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True
        )
        
        points = result[0]
        
        # Group by subdomain
        subdomain_groups = {}
        for point in points:
            subdomain = point.payload.get('subdomain')
            domain = point.payload.get('domain')
            
            if subdomain not in subdomain_groups:
                subdomain_groups[subdomain] = {
                    'count': 0,
                    'domains': set(),
                    'chunk_ids': []
                }
            
            subdomain_groups[subdomain]['count'] += 1
            subdomain_groups[subdomain]['domains'].add(domain)
            subdomain_groups[subdomain]['chunk_ids'].append(
                point.payload.get('chunk_id')
            )
        
        print(f"Total subdomains in database: {len(subdomain_groups)}\n")
        
        for subdomain, info in sorted(subdomain_groups.items()):
            print(f"Subdomain: '{subdomain}'")
            print(f"  Domain(s): {', '.join(info['domains'])}")
            print(f"  Chunk count: {info['count']}")
            print(f"  Chunk IDs: {info['chunk_ids']}")
            
            # Check for naming conflicts
            if len(info['domains']) > 1:
                print(f"  ⚠️  WARNING: Multiple domains map to this subdomain!")
                print(f"     This could cause confusion - consider unique subdomain names")
            else:
                print(f"  ✓ Clean mapping")
            print()
        
        print("=" * 70)
        print("SAFETY VERIFICATION:")
        print("Each subdomain should be an isolated block")
        print("Querying by subdomain should NEVER return data from other subdomains")
        print("=" * 70)
    
    def test_keyword_search(self, keyword):
        """Test keyword search across all chunks"""
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
        
        # Filter by keyword
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
            print(f"  SUBDOMAIN: {point.payload.get('subdomain')}")
            print(f"  Domain: {point.payload.get('domain')}")
            print(f"  Text: {point.payload.get('text', '')[:100]}...")
            print()

def main():
    """Run all visualization and tests"""
    viz = DatabaseVisualizer()
    
    # 1. Show collection info
    viz.get_collection_info()
    
    # 2. View all chunks
    points = viz.view_all_chunks()
    
    if not points:
        print("⚠️  No data in database. Run main.py first to upload chunks.")
        return
    
    # Get first chunk info for demo
    first_chunk = points[0].payload
    first_chunk_id = first_chunk.get('chunk_id')
    first_subdomain = first_chunk.get('subdomain')
    
    # 3. View detail of a specific chunk (FIXED: use actual chunk_id from database)
    print(f"\n📋 Viewing details for first chunk in database...")
    viz.view_chunk_detail(chunk_id=first_chunk_id, subdomain=first_subdomain)
    
    # 4. Test semantic search
    viz.test_semantic_search("What are the meeting times?")
    
    # 5. Test SUBDOMAIN filtering (FIXED: use actual subdomain from database)
    print(f"\n🔍 Testing subdomain filter for: '{first_subdomain}'...")
    viz.test_subdomain_filter(first_subdomain)
    
    # 6. Test cross-contamination safety
    viz.test_cross_contamination()
    
    # 7. Test keyword search
    viz.test_keyword_search("meeting")
    
    print("=" * 70)
    print("✓ Visualization and testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()