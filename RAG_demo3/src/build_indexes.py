"""Build FAISS vector indexes (cosine via normalized embeddings) for each domain.

Assumes per-domain chunk files at data/<domain>.chunks.json.
Outputs:
  indexes/<domain>.faiss
  indexes/<domain>.chunks.json   (copied)

Run:
  python -m src.build_indexes
"""

import json
import os
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INDEX_DIR = ROOT / "indexes"


def build_one(domain: str):
    chunks_path = DATA_DIR / f"{domain}.chunks.json"
    if not chunks_path.exists():
        return False

    chunks = json.load(open(chunks_path, "r", encoding="utf-8"))
    texts = [c["text"] for c in chunks]

    embedder = SentenceTransformer(EMB_MODEL)
    vecs = embedder.encode(texts, normalize_embeddings=True)
    vecs = np.array(vecs, dtype="float32")

    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / f"{domain}.faiss"))
    json.dump(chunks, open(INDEX_DIR / f"{domain}.chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[OK] Built domain={domain} chunks={len(chunks)}")
    return True


def main():
    domains = [p.stem.replace(".chunks", "") for p in DATA_DIR.glob("*.chunks.json")]
    domains = sorted(set(domains))
    if not domains:
        raise SystemExit("No chunk files found under data/")

    for d in domains:
        build_one(d)


if __name__ == "__main__":
    main()
