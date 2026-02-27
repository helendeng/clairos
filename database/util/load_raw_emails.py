"""
Simple Raw Email CSV Ingestion
Just run this script with raw_emails.csv in the same directory
"""

import csv
import json
import os
from database.core.ingest_chunks import ChunkIngestion


def ingest_raw_emails(csv_filepath="../raw_emails.csv"):
    """
    Load and ingest raw emails from CSV file
    
    CSV columns (in order):
        email_id, sender, recipients, cc, bcc, subject, body, timestamp, attachments
    
    Or with header row:
        email_id,sender,recipients,cc,bcc,subject,body,timestamp,attachments
    """
    
    print("=" * 70)
    print("RAW EMAIL CSV INGESTION")
    print("=" * 70)
    print()
    
    # Check if file exists
    if not os.path.exists(csv_filepath):
        print(f"❌ File not found: {csv_filepath}")
        print()
        print("Please provide a CSV file with raw emails.")
        print()
        print("Expected format:")
        print("  email_id,sender,recipients,cc,bcc,subject,body,timestamp,attachments")
        print()
        print("Example:")
        print("  123,john@company.com,team@company.com,,,Meeting Tomorrow,Email body here...,2026-01-18T10:30:00,")
        return
    
    print(f"Reading: {csv_filepath}")
    print()
    
    # Load CSV
    db_chunks = []
    
    try:
        with open(csv_filepath, 'r', encoding='utf-8') as f:
            # Try to detect if first row is header
            sample = f.read(1024)
            f.seek(0)
            has_header = csv.Sniffer().has_header(sample)
            
            if has_header:
                reader = csv.DictReader(f)
                print("✓ Detected CSV header")
            else:
                # No header - use default column names
                reader = csv.DictReader(f, fieldnames=[
                    'email_id', 'sender', 'recipients', 'cc', 'bcc', 
                    'subject', 'body', 'timestamp', 'attachments'
                ])
                print("✓ Using default column names")
            
            print()
            
            for row_num, row in enumerate(reader, start=1):
                # Get fields
                email_id = row.get('email_id', str(row_num))
                sender = row.get('sender', '')
                recipients = row.get('recipients', '')
                cc = row.get('cc', '')
                bcc = row.get('bcc', '')
                subject = row.get('subject', '')
                body = row.get('body', '')
                timestamp = row.get('timestamp', '')
                attachments = row.get('attachments', '')
                
                # Create database format
                db_chunk = {
                    "chunk_id": f"raw_email_{email_id}",
                    "domain": "Raw Email",
                    "subdomain": "Raw Email",
                    "text": body,
                    "source": {
                        "email_id": str(email_id),
                        "from": sender,
                        "to": recipients,
                        "cc": cc,
                        "bcc": bcc,
                        "subject": subject,
                        "timestamp": timestamp
                    }
                }
                
                # Parse attachments if present
                if attachments:
                    try:
                        db_chunk["source"]["attachments"] = json.loads(attachments)
                    except:
                        db_chunk["source"]["attachments"] = attachments
                
                db_chunks.append(db_chunk)
                
                # Show progress
                if row_num % 100 == 0:
                    print(f"  Processed {row_num} emails...")
        
        print(f"✓ Loaded {len(db_chunks)} raw emails")
        print()
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        print()
        return
    
    # Ingest to database
    print("=" * 70)
    print("INGESTING TO DATABASE")
    print("=" * 70)
    print()
    
    try:
        ingestion = ChunkIngestion()
        ingestion.upload_batch(db_chunks)
        
        print()
        print("=" * 70)
        print("✓ SUCCESS!")
        print("=" * 70)
        print(f"\nIngested {len(db_chunks)} raw emails")
        print("  Domain: 'Raw Email'")
        print("  Subdomain: 'Raw Email'")
        print()
        print("Next steps:")
        print("  1. Run: python export_to_json.py")
        print("  2. Check: ../RAG_demo3/json_output/raw_email.json")
        print()
        
    except Exception as e:
        print(f"❌ Error ingesting to database: {e}")
        print()


if __name__ == "__main__":
    ingest_raw_emails()