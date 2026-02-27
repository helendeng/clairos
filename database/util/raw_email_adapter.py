"""
Raw Email Storage Adapter
Stores complete original emails in the database
Domain: "Raw Email", Subdomain: "Raw Email"
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class RawEmailSchema:
    """
    Schema for raw/original email from ingestion part
    """
    email_id: int
    sender: List[str]
    recipients: List[str]
    cc: List[str]
    bcc: List[str]
    subject: str
    body: str  # Full email body
    timestamp: str
    attachments: Optional[List[dict]] = None  # Optional attachment info


def convert_raw_email_to_db_format(raw_emails: List[RawEmailSchema]) -> list:
    """
    Convert raw email format to database ingestion format
    Stores as domain="Raw Email", subdomain="Raw Email"
    
    Args:
        raw_emails: List of RawEmailSchema objects
        
    Returns:
        List of dicts ready for database ingestion
    """
    
    db_chunks = []
    
    for email in raw_emails:
        # Create a "chunk" for the full email
        # Chunk ID format: "raw_email_{email_id}"
        db_chunk = {
            "chunk_id": f"raw_email_{email.email_id}",
            "domain": "Raw Email",
            "subdomain": "Raw Email",
            "text": email.body,  # Full email body as text
            "source": {
                "email_id": str(email.email_id),
                "from": ", ".join(email.sender),
                "to": ", ".join(email.recipients),  # NEW: store recipients
                "cc": ", ".join(email.cc),
                "bcc": ", ".join(email.bcc),
                "subject": email.subject,
                "timestamp": email.timestamp
            }
        }
        
        # Add attachment info if present
        if email.attachments:
            db_chunk["source"]["attachments"] = email.attachments
        
        db_chunks.append(db_chunk)
    
    return db_chunks


def convert_single_raw_email(email: RawEmailSchema) -> dict:
    """
    Convert a single raw email to database format
    
    Args:
        email: Single RawEmailSchema object
        
    Returns:
        Dict ready for database ingestion
    """
    
    db_chunk = {
        "chunk_id": f"raw_email_{email.email_id}",
        "domain": "Raw Email",
        "subdomain": "Raw Email",
        "text": email.body,
        "source": {
            "email_id": str(email.email_id),
            "from": ", ".join(email.sender),
            "to": ", ".join(email.recipients),
            "cc": ", ".join(email.cc),
            "bcc": ", ".join(email.bcc),
            "subject": email.subject,
            "timestamp": email.timestamp
        }
    }
    
    if email.attachments:
        db_chunk["source"]["attachments"] = email.attachments
    
    return db_chunk


