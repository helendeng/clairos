"""Convert json_outputs files to data/*.chunks.json format.

This script:
1. Reads each JSON file from json_outputs/
2. Removes duplicate chunks
3. Converts to the format expected by build_indexes.py
4. Saves to data/{subdomain}.chunks.json
"""

import json
from pathlib import Path
from collections import OrderedDict

ROOT = Path(__file__).resolve().parent
JSON_OUTPUTS_DIR = ROOT / "json_outputs"
DATA_DIR = ROOT / "data"


def sanitize_subdomain_name(subdomain: str) -> str:
    """Convert subdomain name to lowercase filename-safe format."""
    # Replace spaces and special characters with underscores
    name = subdomain.lower()
    name = name.replace(" ", "_")
    name = name.replace("&", "and")
    name = name.replace("-", "_")
    return name


def convert_file(input_path: Path) -> bool:
    """Convert a single json_outputs file to data format."""
    if input_path.name == "index.json":
        return False

    print(f"Processing {input_path.name}...")

    # Load input file
    data = json.load(open(input_path, "r", encoding="utf-8"))
    subdomain = data["metadata"]["subdomain"]
    chunks = data["chunks"]

    # Remove duplicates based on chunk_id and text
    seen = {}
    unique_chunks = []
    for chunk in chunks:
        key = (chunk["chunk_id"], chunk["text"])
        if key not in seen:
            seen[key] = True
            unique_chunks.append(chunk)

    # Convert to output format
    sanitized_name = sanitize_subdomain_name(subdomain)
    output_chunks = []

    for i, chunk in enumerate(unique_chunks, 1):
        output_chunk = {
            "chunk_id": f"{sanitized_name}_{i:03d}",
            "domain": sanitized_name,
            "text": chunk["text"],
            "source": chunk.get("source", {})
        }
        output_chunks.append(output_chunk)

    # Save to data directory
    output_path = DATA_DIR / f"{sanitized_name}.chunks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_chunks, f, ensure_ascii=False, indent=2)

    print(f"  → Created {output_path.name} with {len(output_chunks)} chunks (removed {len(chunks) - len(output_chunks)} duplicates)")
    return True


def main():
    # Clear data directory (except tests.json)
    print("Clearing data directory...")
    for f in DATA_DIR.glob("*.chunks.json"):
        f.unlink()
        print(f"  Removed {f.name}")

    # Convert all files
    print("\nConverting json_outputs files...")
    count = 0
    for input_file in sorted(JSON_OUTPUTS_DIR.glob("*.json")):
        if convert_file(input_file):
            count += 1

    print(f"\n✓ Converted {count} files successfully")


if __name__ == "__main__":
    main()
