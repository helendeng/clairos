"""Build FAISS vector indexes (cosine via normalized embeddings) for each domain.

Supports two input formats under data/:
1) Legacy list format: data/<domain>.chunks.json
2) New export format:  data/<domain>.json with top-level {"chunks": [...]}

Outputs:
  indexes/<domain>.faiss
  indexes/<domain>.chunks.json

Run:
  python -m src.build_indexes
"""

import json
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INDEX_DIR = ROOT / "indexes"


def _load_chunks_for_domain(domain: str):
    legacy_path = DATA_DIR / f"{domain}.chunks.json"
    new_path = DATA_DIR / f"{domain}.json"

    if legacy_path.exists():
        payload = json.load(open(legacy_path, "r", encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        raise ValueError(f"Unexpected legacy chunk file format: {legacy_path}")

    if new_path.exists():
        payload = json.load(open(new_path, "r", encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("chunks"), list):
            return payload["chunks"]
        raise ValueError(f"Unexpected new export file format: {new_path}")

    return None


def build_one(domain: str):
    chunks = _load_chunks_for_domain(domain)
    if not chunks:
        return False

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
    domains = set()
    for p in DATA_DIR.glob("*.chunks.json"):
        domains.add(p.stem.replace(".chunks", ""))
    for p in DATA_DIR.glob("*.json"):
        if p.stem in {"index", "tests", "tests_singlehop", "tests_multihop"}:
            continue
        domains.add(p.stem)
    domains = sorted(domains)
    if not domains:
        raise SystemExit("No chunk files found under data/")

    for d in domains:
        build_one(d)


if __name__ == "__main__":
    main()
