"""
Main script to run the ingestion pipeline
Loads test cases and uploads all chunks to Qdrant
Demonstrates domain/subdomain separation
"""

from ingest_chunks import ChunkIngestion
from test_cases import TEST_CHUNKS

def flatten_test_chunks():
    """
    Flatten nested test cases into a single list
    TEST_CHUNKS is organized as: {domain: {subdomain: [chunks]}}
    """
    all_chunks = []
    
    for domain, subdomains in TEST_CHUNKS.items():
        for subdomain, chunks in subdomains.items():
            all_chunks.extend(chunks)
    
    return all_chunks

def main():
    """Main ingestion function"""
    
    print("="*70)
    print("ClairOS DATABASE INGESTION")
    print("="*70)
    
    # Initialize ingestion service
    ingestion = ChunkIngestion()
    
    # Get all test chunks
    all_chunks = flatten_test_chunks()
    
    print(f"\nPreparing to upload {len(all_chunks)} chunks")
    print(f"Covering {len(TEST_CHUNKS)} domains")
    print()
    
    # Batch upload (recommended, faster)
    ingestion.upload_batch(all_chunks)
    
    print("\n" + "="*70)
    print("✓ Ingestion complete!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Run visualize_database.py to see what was stored")
    print("  2. Run test_database_metrics.py to validate separation")
    print("  3. Test domain filtering to ensure no cross-contamination")

if __name__ == "__main__":
    main()