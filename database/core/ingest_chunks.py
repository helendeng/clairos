"""
Ingest parsed email chunks into Qdrant
SUBDOMAIN is the primary classification (27 separate blocks)
Domain is stored as metadata for context [1]
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from collections import Counter

from database.Schemas.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, SUBDOMAINS, SUBDOMAIN_TO_DOMAIN
from database.util.embedding_service import EmbeddingService

class ChunkIngestion:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.embedding_service = EmbeddingService()
        print(f"✓ Connected to Qdrant collection: {COLLECTION_NAME}")
        print(f"  Organization: SUBDOMAIN-based (27 blocks)")
    
    def validate_chunk(self, chunk: dict) -> bool:
        """
        Validate chunk format
        SUBDOMAIN is primary classification, domain is metadata
        """
        required_fields = ["chunk_id", "domain", "subdomain", "text", "source"]
        
        for field in required_fields:
            if field not in chunk:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate subdomain exists (primary classification)
        subdomain = chunk["subdomain"]
        if subdomain not in SUBDOMAINS:
            print(f"❌ Invalid subdomain: {subdomain}")
            print(f"   Valid subdomains: {SUBDOMAINS}")
            return False
        
        # Validate that domain matches subdomain mapping
        expected_domain = SUBDOMAIN_TO_DOMAIN.get(subdomain)
        if expected_domain and chunk["domain"] != expected_domain:
            print(f"⚠️  Warning: Domain mismatch for subdomain '{subdomain}'")
            print(f"   Expected: {expected_domain}, Got: {chunk['domain']}")
        
        # Validate source fields
        required_source_fields = ["email_id", "from", "subject", "timestamp"]
        for field in required_source_fields:
            if field not in chunk["source"]:
                print(f"❌ Missing source field: {field}")
                return False
        
        return True
    
    def upload_chunk(self, parsed_chunk: dict):
        """
        Upload a single chunk to Qdrant
        Stored in SUBDOMAIN block (primary classification)
        """
        
        if not self.validate_chunk(parsed_chunk):
            print(f"⚠️  Skipping invalid chunk")
            return
        
        # Generate embedding
        vector = self.embedding_service.embed(parsed_chunk["text"])
        
        # Create Qdrant point
        # SUBDOMAIN is the main searchable field
        # Domain is metadata for context
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "chunk_id": parsed_chunk["chunk_id"],  # String identifier within subdomain
                "subdomain": parsed_chunk["subdomain"],  # PRIMARY: 27 blocks
                "domain": parsed_chunk["domain"],  # METADATA: for context
                "text": parsed_chunk["text"],
                "source": {
                    "email_id": parsed_chunk["source"]["email_id"],
                    "cc": parsed_chunk["source"].get("cc", ""),
                    "bcc": parsed_chunk["source"].get("bcc", ""),
                    "from": parsed_chunk["source"]["from"],
                    "subject": parsed_chunk["source"]["subject"],
                    "timestamp": parsed_chunk["source"]["timestamp"]
                }
            }
        )
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        
        subdomain = parsed_chunk["subdomain"]
        domain = parsed_chunk["domain"]
        chunk_id = parsed_chunk["chunk_id"]
        print(f"✓ Uploaded: [{subdomain}] chunk #{chunk_id} (domain: {domain})")
    
    def upload_batch(self, parsed_chunks: list):
        """
        Batch upload maintaining subdomain-based separation
        """
        if not parsed_chunks:
            print("⚠️  No chunks to upload")
            return
        
        # Validate all chunks
        valid_chunks = [c for c in parsed_chunks if self.validate_chunk(c)]
        
        if not valid_chunks:
            print("❌ No valid chunks in batch")
            return
        
        # Extract texts for batch embedding
        texts = [chunk["text"] for chunk in valid_chunks]
        vectors = self.embedding_service.embed_batch(texts)
        
        # Create points
        points = []
        for chunk, vector in zip(valid_chunks, vectors):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "subdomain": chunk["subdomain"],  # PRIMARY
                    "domain": chunk["domain"],  # METADATA
                    "text": chunk["text"],
                    "source": {
                        "email_id": chunk["source"]["email_id"],
                        "cc": chunk["source"].get("cc", ""),
                        "bcc": chunk["source"].get("bcc", ""),
                        "from": chunk["source"]["from"],
                        "subject": chunk["source"]["subject"],
                        "timestamp": chunk["source"]["timestamp"]
                    }
                }
            ))
        
        # Batch upload
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        print(f"✓ Uploaded {len(valid_chunks)} chunks")
        
        # Show SUBDOMAIN distribution (primary classification)
        subdomain_counts = Counter(c["subdomain"] for c in valid_chunks)
        print("\nSubdomain distribution (27 blocks):")
        for subdomain, count in subdomain_counts.items():
            # Get domain from mapping for this subdomain
            domain = SUBDOMAIN_TO_DOMAIN.get(subdomain, "Unknown")
            print(f"  [{subdomain}]: {count} chunks (domain: {domain})")