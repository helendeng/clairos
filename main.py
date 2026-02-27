"""
Entry point for the ClairOS data ingestion pipeline.

Usage:
    python main.py path/to/inbox.mbox
"""
import sys

from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
from Ingestion.util.parseMbox import controller


def run_ingestion(mbox_fp: str):
    """Runs the full ingestion pipeline on an .mbox file."""
    print(f"Starting ingestion: {mbox_fp}")
    results = controller(mbox_fp, zero_shot_classify)
    print(f"Done. {len(results)} tagged chunks produced.")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/inbox.mbox")
        sys.exit(1)

    run_ingestion(sys.argv[1])
