'''"""
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

'''

"""
Main script to run the ingestion pipeline
Handles:
  1. Parser OutputSchema format (parsed chunks)
  2. RawEmailSchema format (original emails)
  3. Raw emails from CSV file
  4. Test cases (for testing)
Database automatically routes based on subdomain tag
"""

from database.core.ingest_chunks import ChunkIngestion

# Try to import adapters
try:
    from parser_adapter import OutputSchema, convert_parser_output_to_db_format
    HAS_PARSER_ADAPTER = True
except ImportError:
    HAS_PARSER_ADAPTER = False

try:
    from database.util.raw_email_adapter import RawEmailSchema, convert_raw_email_to_db_format
    HAS_RAW_EMAIL_ADAPTER = True
except ImportError:
    HAS_RAW_EMAIL_ADAPTER = False

try:
    from database.util.load_raw_emails import ingest_raw_emails as load_csv_raw_emails
    HAS_CSV_LOADER = True
except ImportError:
    HAS_CSV_LOADER = False

# Try to import test cases (optional)
try:
    from database.Schemas.test_cases import TEST_CHUNKS
    HAS_TEST_CASES = True
except ImportError:
    HAS_TEST_CASES = False
    TEST_CHUNKS = []


def flatten_test_chunks():
    """
    Flatten nested test cases into a single list
    TEST_CHUNKS is organized as: {domain: {subdomain: [chunks]}}
    """
    if not TEST_CHUNKS:
        return []
    
    # Check if already flat
    if isinstance(TEST_CHUNKS, list):
        return TEST_CHUNKS
    
    # Flatten nested structure
    all_chunks = []
    for domain, subdomains in TEST_CHUNKS.items():
        for subdomain, chunks in subdomains.items():
            all_chunks.extend(chunks)
    
    return all_chunks


def ingest_from_parser(parser_chunks):
    """
    Ingest parsed chunks from parser output (OutputSchema format)
    
    Args:
        parser_chunks: List of OutputSchema objects from parser
    """
    
    if not HAS_PARSER_ADAPTER:
        print("❌ parser_adapter.py not found!")
        print("   Make sure parser_adapter.py is in the same directory")
        return
    
    print("="*70)
    print("ClairOS DATABASE INGESTION - PARSED CHUNKS")
    print("="*70)
    
    # Initialize ingestion service
    ingestion = ChunkIngestion()
    
    print(f"\nReceived {len(parser_chunks)} parsed chunks from parser")
    print("Converting parser format to database format...")
    
    # Convert parser format to database format
    db_chunks = convert_parser_output_to_db_format(parser_chunks)
    
    print(f"✓ Converted {len(db_chunks)} chunks")
    print("Chunks routed to their respective subdomains")
    print()
    
    # Batch upload
    ingestion.upload_batch(db_chunks)
    
    print("\n" + "="*70)
    print("✓ Parsed chunks ingested!")
    print("="*70)


def ingest_raw_emails(raw_emails):
    """
    Ingest original/raw emails (RawEmailSchema format)
    Stores as domain="Raw Email", subdomain="Raw Email"
    
    Args:
        raw_emails: List of RawEmailSchema objects
    """
    
    if not HAS_RAW_EMAIL_ADAPTER:
        print("❌ raw_email_adapter.py not found!")
        print("   Make sure raw_email_adapter.py is in the same directory")
        return
    
    print("="*70)
    print("ClairOS DATABASE INGESTION - RAW EMAILS")
    print("="*70)
    
    # Initialize ingestion service
    ingestion = ChunkIngestion()
    
    print(f"\nReceived {len(raw_emails)} raw emails")
    print("Converting to database format...")
    
    # Convert raw email format to database format
    db_chunks = convert_raw_email_to_db_format(raw_emails)
    
    print(f"✓ Converted {len(db_chunks)} emails")
    print("Storing as: Domain='Raw Email', Subdomain='Raw Email'")
    print()
    
    # Batch upload
    ingestion.upload_batch(db_chunks)
    
    print("\n" + "="*70)
    print("✓ Raw emails ingested!")
    print("="*70)


def ingest_raw_emails_from_csv(csv_filepath="raw_emails.csv"):
    """
    Ingest raw emails from CSV file
    
    Args:
        csv_filepath: Path to CSV file
    """
    
    if not HAS_CSV_LOADER:
        print("❌ load_raw_emails.py not found!")
        print("   Make sure load_raw_emails.py is in the same directory")
        return
    
    load_csv_raw_emails(csv_filepath)


def ingest_complete_pipeline(parser_chunks, raw_emails):
    """
    Ingest both parsed chunks AND raw emails in one go
    This is the typical workflow
    
    Args:
        parser_chunks: List of OutputSchema (parsed chunks)
        raw_emails: List of RawEmailSchema (original emails)
    """
    
    print("="*70)
    print("ClairOS DATABASE INGESTION - COMPLETE PIPELINE")
    print("="*70)
    print()
    
    # Ingest parsed chunks
    print("1. Ingesting parsed chunks...")
    print("-" * 70)
    ingest_from_parser(parser_chunks)
    
    print()
    
    # Ingest raw emails
    print("2. Ingesting raw emails...")
    print("-" * 70)
    ingest_raw_emails(raw_emails)
    
    print()
    print("="*70)
    print("✓ COMPLETE PIPELINE FINISHED!")
    print("="*70)
    print(f"\nIngested:")
    print(f"  - {len(parser_chunks)} parsed chunks (classified by subdomain)")
    print(f"  - {len(raw_emails)} raw emails (stored in 'Raw Email' subdomain)")


def ingest_from_test_cases():
    """
    Ingest chunks from test_cases.py (for testing without parser)
    """
    
    if not HAS_TEST_CASES or not TEST_CHUNKS:
        print("❌ No test cases available")
        print("   Create database/Schemas/test_cases.py with TEST_CHUNKS")
        return
    
    print("="*70)
    print("ClairOS DATABASE INGESTION - TEST CASES")
    print("="*70)
    
    # Initialize ingestion service
    ingestion = ChunkIngestion()
    
    # Flatten if needed
    flat_chunks = flatten_test_chunks()
    
    print(f"\nPreparing to upload {len(flat_chunks)} test chunks")
    print("Chunks are self-describing - database will route by subdomain tag")
    print()
    
    # Batch upload
    ingestion.upload_batch(flat_chunks)
    
    print("\n" + "="*70)
    print("✓ Ingestion complete!")
    print("="*70)


def main():
    """Main ingestion function with menu"""
    
    print()
    print("="*70)
    print("CLAIROS DATABASE INGESTION")
    print("="*70)
    print()
    print("This script can ingest:")
    print("  1. Test cases (database/Schemas/test_cases.py)")
    print("  2. Parsed chunks (OutputSchema format)")
    print("  3. Raw emails (RawEmailSchema format)")
    print("  4. Raw emails from CSV file")
    print("  5. Complete pipeline (parsed + raw)")
    print()
    
    # Show what's available
    if HAS_TEST_CASES and TEST_CHUNKS:
        flat_chunks = flatten_test_chunks()
        print(f"✓ Test cases available: {len(flat_chunks)} chunks")
    else:
        print("⚠️  No test cases found")
    
    if HAS_PARSER_ADAPTER:
        print("✓ Parser adapter available")
    else:
        print("⚠️  Parser adapter not found")
    
    if HAS_RAW_EMAIL_ADAPTER:
        print("✓ Raw email adapter available")
    else:
        print("⚠️  Raw email adapter not found")
    
    if HAS_CSV_LOADER:
        print("✓ CSV loader available")
    else:
        print("⚠️  CSV loader not found")
    
    print()
    
    # Menu
    choice = input("Choose option (1-5) or 'help' for examples [1]: ").strip().lower() or "1"
    print()
    
    if choice == "1":
        ingest_from_test_cases()
    
    elif choice == "2":
        print("To use parser output, call from your code:")
        print()
        print("  from main import ingest_from_parser")
        print("  from your_parser import parse_email")
        print()
        print("  parser_chunks = parse_email(raw_email)")
        print("  ingest_from_parser(parser_chunks)")
        print()
    
    elif choice == "3":
        print("To use raw email objects, call from your code:")
        print()
        print("  from main import ingest_raw_emails")
        print("  from your_ingestion import load_emails")
        print()
        print("  raw_emails = load_emails()")
        print("  ingest_raw_emails(raw_emails)")
        print()
    
    elif choice == "4":
        csv_path = input("CSV file path [raw_emails.csv]: ").strip() or "raw_emails.csv"
        print()
        ingest_raw_emails_from_csv(csv_path)
    
    elif choice == "5":
        print("To use complete pipeline, call from your code:")
        print()
        print("  from main import ingest_complete_pipeline")
        print()
        print("  parser_chunks = parse_email(email)")
        print("  raw_emails = [email_obj]")
        print("  ingest_complete_pipeline(parser_chunks, raw_emails)")
        print()
    
    elif choice == "help":
        show_examples()
    
    else:
        print("Invalid choice")
    
    print()
    print("Next steps:")
    print("  1. Run: python visualize_database.py")
    print("  2. Run: python test_database_metrics.py")
    print("  3. Run: python export_to_json.py")


def show_examples():
    """Show integration examples"""
    
    print("="*70)
    print("INTEGRATION EXAMPLES")
    print("="*70)
    print()
    
    print("Example 1: Ingest from test cases")
    print("-" * 70)
    print("""
# Just run main.py and choose option 1
python main.py
""")
    
    print()
    print("Example 2: Ingest parsed chunks from your code")
    print("-" * 70)
    print("""
from main import ingest_from_parser

# Your parser outputs List[OutputSchema]
parser_chunks = your_parser.parse(email)

# Ingest
ingest_from_parser(parser_chunks)
""")
    
    print()
    print("Example 3: Ingest raw emails from CSV")
    print("-" * 70)
    print("""
from main import ingest_raw_emails_from_csv

# Load from CSV file
ingest_raw_emails_from_csv("raw_emails.csv")
""")
    
    print()
    print("Example 4: Complete pipeline")
    print("-" * 70)
    print("""
from main import ingest_complete_pipeline

# Get both from your ingestion
parser_chunks = parse_email(email)
raw_emails = [email_object]

# Ingest everything
ingest_complete_pipeline(parser_chunks, raw_emails)
""")


if __name__ == "__main__":
    main()