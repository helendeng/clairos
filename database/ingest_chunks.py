"""
Ingest parsed email chunks into Qdrant
main database upload script
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME
from embedding_service import EmbeddingService

class ChunkIngestion:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.embedding_service = EmbeddingService()
        print(f"✓ Connected to Qdrant collection: {COLLECTION_NAME}")
    
    def upload_chunk(self, parsed_chunk: dict):
        """
        Upload a single chunk to Qdrant
        
        Input format (from your teammate):
        {
            "chunk_id": "scheduling_001",
            "domain": "scheduling",
            "subdomain": "meeting time",
            "text": "Meeting set for 3pm PST...",
            "source": {...}
        }
        """
        
        # Generate embedding from text
        vector = self.embedding_service.embed(parsed_chunk["text"])
        
        # Create Qdrant point (only storing the 4 fields you specified)
        point = PointStruct(
            id=str(uuid.uuid4()),  # Qdrant needs unique ID
            vector=vector,
            payload={
                "chunk_id": parsed_chunk["chunk_id"],
                "domain": parsed_chunk["domain"],
                "subdomain": parsed_chunk["subdomain"],
                "text": parsed_chunk["text"]
            }
        )
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        
        print(f"✓ Uploaded chunk: {parsed_chunk['chunk_id']}")
    
    def upload_batch(self, parsed_chunks: list):
        """
        Upload multiple chunks at once (faster)
        
        Input: List of parsed_chunk dicts
        """
        if not parsed_chunks:
            print("No chunks to upload")
            return
        
        # Extract all text for batch embedding
        texts = [chunk["text"] for chunk in parsed_chunks]
        vectors = self.embedding_service.embed_batch(texts)
        
        # Create points
        points = []
        for chunk, vector in zip(parsed_chunks, vectors):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "domain": chunk["domain"],
                    "subdomain": chunk["subdomain"],
                    "text": chunk["text"]
                }
            ))
        
        # Batch upload
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        print(f"✓ Uploaded {len(parsed_chunks)} chunks")