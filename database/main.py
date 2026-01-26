"""
Main script to run the ingestion pipeline
run to upload chunks to Qdrant
"""

from ingest_chunks import ChunkIngestion

# Example:provides this format
example_parsed_chunks = [
    {
        "chunk_id": "scheduling_001",
        "domain": "scheduling",
        "subdomain": "meeting time",
        "text": "Meeting set for 3pm PST / 6pm EST tomorrow to review onboarding.",
        "source": {
            "email_id": "sch_email_001",
            "subject": "Onboarding meeting",
            "timestamp": "2026-01-18"
        }
    },
    {
        "chunk_id": "scheduling_002",
        "domain": "project_update",
        "subdomain": "Atlas project",
        "text": "The Atlas project environmental assessment is progressing well.",
        "source": {
            "email_id": "proj_email_002",
            "subject": "Atlas Update",
            "timestamp": "2026-01-19"
        }
    }
]

def main():
    """Main ingestion function"""
    
    # Initialize ingestion service
    ingestion = ChunkIngestion()
    
    # Option 2: Batch upload (recommended, faster)
    ingestion.upload_batch(example_parsed_chunks)
    
    print("\n✓ Ingestion complete!")

if __name__ == "__main__":
    main()