"""Domain-constrained retriever: vector search (FAISS) + optional BM25.

Key point: the upstream router provides domains_to_search.
The retriever only searches within those domain indexes.
"""

import json
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "indexes"


@dataclass
class Hit:
    domain: str
    chunk_id: str
    score: float
    method: str
    text: str
    source: dict


class DomainRetriever:
    def __init__(self, index_dir: Path = INDEX_DIR):
        self.index_dir = Path(index_dir)
        self._embedder = None
        self._np = None
        self._faiss = None
        self._vector_ready = False

    @staticmethod
    def _dedupe_keep_best(hits: list[Hit]) -> list[Hit]:
        best = {}
        for h in hits:
            key = (h.domain, h.chunk_id)
            if key not in best or h.score > best[key].score:
                best[key] = h
        return list(best.values())

    @staticmethod
    def _rrf_fuse(vector_hits: list[Hit], bm25_hits: list[Hit], rrf_k: int = 60) -> list[Hit]:
        vector_ranked = sorted(DomainRetriever._dedupe_keep_best(vector_hits), key=lambda h: h.score, reverse=True)
        bm25_ranked = sorted(DomainRetriever._dedupe_keep_best(bm25_hits), key=lambda h: h.score, reverse=True)

        score_map = {}
        hit_map = {}

        for rank, h in enumerate(vector_ranked, start=1):
            key = (h.domain, h.chunk_id)
            score_map[key] = score_map.get(key, 0.0) + 1.0 / (rrf_k + rank)
            hit_map[key] = h

        for rank, h in enumerate(bm25_ranked, start=1):
            key = (h.domain, h.chunk_id)
            score_map[key] = score_map.get(key, 0.0) + 1.0 / (rrf_k + rank)
            hit_map[key] = h

        fused = []
        for key, h in hit_map.items():
            fused.append(
                Hit(
                    domain=h.domain,
                    chunk_id=h.chunk_id,
                    score=score_map.get(key, 0.0),
                    method="hybrid_rrf",
                    text=h.text,
                    source=h.source,
                )
            )
        return sorted(fused, key=lambda h: h.score, reverse=True)

    def _ensure_vector_backend(self):
        if self._vector_ready:
            return
        try:
            import numpy as np
            import faiss
            from sentence_transformers import SentenceTransformer
        except Exception as exc:  # pragma: no cover - depends on local env
            raise RuntimeError(
                "Vector backend unavailable. Install/repair numpy, faiss, and sentence-transformers "
                "or call search(..., use_vector=False)."
            ) from exc
        self._np = np
        self._faiss = faiss
        self._embedder = SentenceTransformer(EMB_MODEL)
        self._vector_ready = True

    def _load_domain(self, domain: str, need_index: bool):
        idx_path = self.index_dir / f"{domain}.faiss"
        chunks_path = self.index_dir / f"{domain}.chunks.json"
        if not chunks_path.exists():
            raise FileNotFoundError(f"Missing chunks for domain '{domain}'. Build indexes first.")
        chunks = json.load(open(chunks_path, "r", encoding="utf-8"))
        index = None
        if need_index:
            if not idx_path.exists():
                raise FileNotFoundError(f"Missing index for domain '{domain}'. Build indexes first.")
            self._ensure_vector_backend()
            index = self._faiss.read_index(str(idx_path))
        return index, chunks

    @staticmethod
    def _bm25_scores(tokenized_docs: list[list[str]], query_tokens: list[str]):
        if not tokenized_docs:
            return []
        doc_freqs = []
        df = Counter()
        doc_lens = []
        for doc in tokenized_docs:
            freqs = Counter(doc)
            doc_freqs.append(freqs)
            doc_lens.append(len(doc))
            df.update(freqs.keys())
        n_docs = len(tokenized_docs)
        avgdl = sum(doc_lens) / max(n_docs, 1)
        k1 = 1.5
        b = 0.75

        idf = {}
        for term, f in df.items():
            idf[term] = log((n_docs - f + 0.5) / (f + 0.5) + 1)

        scores = [0.0] * n_docs
        for i, freqs in enumerate(doc_freqs):
            dl = doc_lens[i]
            denom_const = k1 * (1 - b + b * (dl / avgdl)) if avgdl > 0 else k1
            score = 0.0
            for term in query_tokens:
                tf = freqs.get(term)
                if not tf:
                    continue
                term_idf = idf.get(term, 0.0)
                score += term_idf * (tf * (k1 + 1)) / (tf + denom_const)
            scores[i] = score
        return scores

    def search(
        self,
        question: str,
        domains_to_search: list[str],
        top_k: int = 5,
        use_bm25: bool = True,
        use_vector: bool = True,
        fusion: str = "rrf",
    ) -> list[Hit]:
        # Query vector (optional)
        if use_vector:
            self._ensure_vector_backend()
            qv = self._embedder.encode([question], normalize_embeddings=True)
            qv = self._np.array(qv, dtype="float32")
        else:
            qv = None

        vector_hits = []
        bm25_hits = []

        for domain in domains_to_search:
            index, chunks = self._load_domain(domain, need_index=use_vector)

            # Vector search
            if use_vector and index is not None:
                scores, ids = index.search(qv, top_k)
                for s, i in zip(scores[0], ids[0]):
                    if i == -1:
                        continue
                    c = chunks[int(i)]
                    vector_hits.append(
                        Hit(
                            domain=domain,
                            chunk_id=c["chunk_id"],
                            score=float(s),
                            method="vector",
                            text=c["text"],
                            source=c.get("source", {}),
                        )
                    )

            # BM25 search (optional)
            if use_bm25:
                tokenized = [c["text"].split() for c in chunks]
                bm_scores = self._bm25_scores(tokenized, question.split())
                top_ids = sorted(range(len(bm_scores)), key=lambda i: bm_scores[i], reverse=True)[:top_k]
                for i in top_ids:
                    c = chunks[int(i)]
                    bm25_hits.append(
                        Hit(
                            domain=domain,
                            chunk_id=c["chunk_id"],
                            score=float(bm_scores[int(i)]),
                            method="bm25",
                            text=c["text"],
                            source=c.get("source", {}),
                        )
                    )

        if use_vector and use_bm25 and fusion.lower() == "rrf":
            return self._rrf_fuse(vector_hits, bm25_hits)[:top_k]

        merged = self._dedupe_keep_best(vector_hits + bm25_hits)
        return sorted(merged, key=lambda h: h.score, reverse=True)[:top_k]
