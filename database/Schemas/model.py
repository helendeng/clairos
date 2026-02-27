"""
Data models for email chunks
Matches parser output + ClairOS requirements [1]
"""
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class EmailChunk:
    """
    need to provides: chunk_id, domain, subdomain, text, source
    """
    # From  parser
    chunk_id: str
    domain: str
    subdomain: str
    text: str
    source: Dict[str, str]  # Contains: email_id, subject, timestamp
    
    approval_status: str = "pending"  # "pending" | "approved" | "redacted"
    chunk_type: str = "standard"      # "micro" | "standard" | "macro"
    thread_id: Optional[str] = None   # Will come from TRC component [1]
    manager_notes: str = ""
    
    def to_qdrant_payload(self) -> dict:
        """Convert to Qdrant storage format"""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "chunk_type": self.chunk_type,
            "source": self.source  # Nested: email_id, subject, timestamp
        }
    
    @classmethod
    def from_parsed(cls, parsed_chunk: dict):
        """
        
        
        Input format:
        {
            "chunk_id": "scheduling_001",
            "domain": "scheduling",
            "subdomain": "meeting time",
            "text": "Meeting set for 3pm PST...",
            "source": {
                "email_id": "sch_email_001",
                "subject": "Onboarding meeting",
                "timestamp": "2026-01-18"
            }
        }
        """
        return cls(
            chunk_id=parsed_chunk["chunk_id"],
            domain=parsed_chunk["domain"],
            subdomain=parsed_chunk["subdomain"],
            text=parsed_chunk["text"],
            source=parsed_chunk["source"],
        )