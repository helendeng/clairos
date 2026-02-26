"""
Main script to run the ingestion pipeline
Loads test cases and uploads all chunks to Qdrant
Demonstrates domain/subdomain separation
"""

from database.core.ingest_chunks import ChunkIngestion
from database.Schemas.test_cases import TEST_CHUNKS

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
    
    # TEST_CHUNKS is now a flat list - each chunk knows its own subdomain
    print(f"\nPreparing to upload {len(TEST_CHUNKS)} chunks")
    print("Chunks are self-describing - database will route by subdomain tag")
    print()
    
    # Batch upload - ingestion reads subdomain from each chunk
    ingestion.upload_batch(TEST_CHUNKS)
    
    print("\n" + "="*70)
    print("✓ Ingestion complete!")
    print("="*70)
    print("\nHow it works:")
    print("  1. Parser assigns subdomain tag to each chunk")
    print("  2. Database reads subdomain field")
    print("  3. Chunk routed to correct isolated block")
    print("  4. No pre-organization needed!")
    print()
    print("Next steps:")
    print("  1. Run visualize_database.py to see subdomain distribution")
    print("  2. Run test_database_metrics.py to validate isolation")
    print("  3. Run generate_subdomain_json.py to export by subdomain")

if __name__ == "__main__":
    main()