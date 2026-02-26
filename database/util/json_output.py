"""
Export Qdrant Database to JSON Files
Creates one JSON file per subdomain with all its chunks
Output: ../RAG_demo3/json_output/
"""

from qdrant_client import QdrantClient
from database.Schemas.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME
import json
import os
import shutil
from datetime import datetime
from collections import defaultdict


def sanitize_filename(name):
    """Convert subdomain name to valid filename"""
    name = name.replace(' ', '_')
    name = name.replace('/', '_')
    name = name.replace('&', 'and')
    name = name.replace('\\', '_')
    # Remove other special characters
    name = ''.join(c for c in name if c.isalnum() or c == '_')
    return name.lower()


def export_database_to_json():
    """Export entire database to separate JSON files per subdomain"""
    
    # Fixed output directory
    output_dir = "../RAG_demo3/json_output"
    
    print("=" * 70)
    print("EXPORT DATABASE TO JSON FILES")
    print("=" * 70)
    print()
    print(f"Output directory: {output_dir}")
    print()
    
    # Handle existing directory
    if os.path.exists(output_dir):
        print(f"⚠️  Directory already exists - will overwrite files")
        # Remove old files
        for file in os.listdir(output_dir):
            filepath = os.path.join(output_dir, file)
            if file.endswith('.json'):
                os.remove(filepath)
        print(f"✓ Cleared old JSON files")
    else:
        # Create directory and parent if needed
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Created directory: {output_dir}")
    
    print()
    
    # Connect to Qdrant
    print(f"Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✓ Connected to collection: {COLLECTION_NAME}")
    print()
    
    # Get all chunks from database
    print("Fetching data from database...")
    try:
        result = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=10000,  # Adjust if you have more chunks
            with_payload=True,
            with_vectors=False  # Don't export vectors (too large)
        )
        
        points = result[0]
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        print()
        print("Possible issues:")
        print("  - Collection doesn't exist (run fix_collection.py)")
        print("  - Wrong credentials in config.py")
        print("  - No internet connection")
        return
    
    if not points:
        print("❌ No data found in database!")
        print("   Database is empty - nothing to export")
        print()
        print("Run main.py to upload test chunks first")
        return
    
    print(f"✓ Retrieved {len(points)} chunks from database")
    print()
    
    # Group chunks by subdomain
    print("Organizing by subdomain...")
    subdomain_data = defaultdict(list)
    
    for point in points:
        subdomain = point.payload.get('subdomain', 'Unknown')
        
        # Create clean chunk data
        chunk_data = {
            'chunk_id': point.payload.get('chunk_id'),
            'subdomain': subdomain,
            'domain': point.payload.get('domain'),
            'text': point.payload.get('text'),
            'source': {
                'email_id': point.payload.get('source', {}).get('email_id'),
                'from': point.payload.get('source', {}).get('from'),
                'cc': point.payload.get('source', {}).get('cc', ''),
                'bcc': point.payload.get('source', {}).get('bcc', ''),
                'subject': point.payload.get('source', {}).get('subject'),
                'timestamp': point.payload.get('source', {}).get('timestamp')
            }
        }
        
        subdomain_data[subdomain].append(chunk_data)
    
    print(f"✓ Found {len(subdomain_data)} unique subdomains")
    print()
    
    # Export each subdomain to its own JSON file
    print("=" * 70)
    print("CREATING JSON FILES")
    print("=" * 70)
    print()
    
    total_files = 0
    total_chunks = 0
    file_list = []
    
    for subdomain, chunks in sorted(subdomain_data.items()):
        # Create filename from subdomain name
        filename = sanitize_filename(subdomain) + '.json'
        filepath = os.path.join(output_dir, filename)
        
        # Get domain (all chunks in subdomain should have same domain)
        domain = chunks[0]['domain'] if chunks else 'Unknown'
        
        # Create JSON structure
        json_data = {
            'metadata': {
                'subdomain': subdomain,
                'domain': domain,
                'chunk_count': len(chunks),
                'collection_name': COLLECTION_NAME,
                'exported_at': datetime.now().isoformat(),
                'export_date': datetime.now().strftime('%Y-%m-%d'),
                'export_time': datetime.now().strftime('%H:%M:%S')
            },
            'chunks': chunks
        }
        
        # Write to file with pretty formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        total_files += 1
        total_chunks += len(chunks)
        
        # Track file info
        file_list.append({
            'subdomain': subdomain,
            'domain': domain,
            'filename': filename,
            'chunk_count': len(chunks)
        })
        
        print(f"✓ {filename:40} | {len(chunks):3} chunks | Domain: {domain}")
    
    # Create index file
    print()
    print("Creating index file...")
    
    index_data = {
        'metadata': {
            'collection_name': COLLECTION_NAME,
            'total_subdomains': len(subdomain_data),
            'total_chunks': total_chunks,
            'total_files': total_files,
            'exported_at': datetime.now().isoformat(),
            'export_date': datetime.now().strftime('%Y-%m-%d')
        },
        'files': file_list,
        'summary': {
            subdomain: {
                'domain': subdomain_data[subdomain][0]['domain'],
                'chunk_count': len(chunks),
                'filename': sanitize_filename(subdomain) + '.json'
            }
            for subdomain, chunks in sorted(subdomain_data.items())
        }
    }
    
    index_filepath = os.path.join(output_dir, 'index.json')
    with open(index_filepath, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ index.json")
    print()
    
    # Summary
    print("=" * 70)
    print("✓ EXPORT COMPLETE!")
    print("=" * 70)
    print()
    print(f"Output directory: {output_dir}")
    print(f"Files created: {total_files + 1} ({total_files} subdomain files + 1 index)")
    print(f"Total chunks exported: {total_chunks}")
    print()
    
    print("Files created:")
    print("-" * 70)
    print(f"  index.json                          - Overview of all subdomains")
    for file_info in sorted(file_list, key=lambda x: x['filename']):
        print(f"  {file_info['filename']:40} - {file_info['chunk_count']:3} chunks")
    print()
    
    # Show absolute path
    abs_path = os.path.abspath(output_dir)
    print(f"Full path: {abs_path}")
    print()
    
    return subdomain_data, output_dir


def view_json_file(filepath):
    """View contents of a JSON file"""
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data.get('metadata', {})
    chunks = data.get('chunks', [])
    
    print("=" * 70)
    print(f"FILE: {os.path.basename(filepath)}")
    print("=" * 70)
    print()
    print(f"Subdomain: {metadata.get('subdomain')}")
    print(f"Domain: {metadata.get('domain')}")
    print(f"Chunks: {metadata.get('chunk_count')}")
    print(f"Exported: {metadata.get('exported_at')}")
    print()
    
    print("Sample chunks:")
    print("-" * 70)
    for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
        print(f"\n{i}. Chunk ID: {chunk.get('chunk_id')}")
        print(f"   Text: {chunk.get('text')[:80]}...")
        print(f"   From: {chunk.get('source', {}).get('from')}")
        print(f"   Subject: {chunk.get('source', {}).get('subject')}")
    
    if len(chunks) > 3:
        print(f"\n... and {len(chunks) - 3} more chunks")
    print()


def main():
    """Main function - no user input needed"""
    
    print()
    print("=" * 70)
    print("DATABASE TO JSON EXPORTER")
    print("=" * 70)
    print()
    print("This script exports your Qdrant database to:")
    print("  ../RAG_demo3/json_output/")
    print()
    print("One JSON file will be created per subdomain.")
    print("Existing files will be overwritten.")
    print()
    
    # Export database (no user input needed)
    result = export_database_to_json()
    
    if not result:
        return
    
    subdomain_data, output_dir = result
    
    # Offer to view a file
    print()
    view_option = input("View a JSON file? (y/n) [n]: ").strip().lower()
    
    if view_option == 'y':
        print("\nAvailable JSON files:")
        files = sorted(os.listdir(output_dir))
        json_files = [f for f in files if f.endswith('.json') and f != 'index.json']
        
        for i, filename in enumerate(json_files, 1):
            # Get chunk count from filename
            subdomain = None
            for sub in subdomain_data.keys():
                if sanitize_filename(sub) + '.json' == filename:
                    subdomain = sub
                    break
            
            count = len(subdomain_data.get(subdomain, [])) if subdomain else 0
            print(f"  {i}. {filename:40} ({count} chunks)")
        
        try:
            choice = int(input("\nEnter file number: ")) - 1
            if 0 <= choice < len(json_files):
                filepath = os.path.join(output_dir, json_files[choice])
                print()
                view_json_file(filepath)
        except (ValueError, IndexError):
            print("Invalid choice")
    
    print()
    print("=" * 70)
    print("Done! Your JSON files are in ../RAG_demo3/json_output/")
    print("=" * 70)


if __name__ == "__main__":
    main()