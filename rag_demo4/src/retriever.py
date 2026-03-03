"""Domain-constrained retriever with pluggable backend.

Supported backends:
- local: FAISS vector + optional BM25 over local index files
- qdrant: live vector search against shared database collection

Key point: the upstream router provides domains_to_search.
The retriever only searches within those routed domains/subdomains.
"""

import json
import importlib.util
import os
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

from networkx import hits

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "indexes"


# Map common routed/index names to database-side subdomain labels.
_RAG_DOMAIN_TO_SUBDOMAIN = {
    "accounting": "Accounting",
    "all_hr": "HR",
    "all_schedule": "Scheduling",
    "business_strategy": "Business_Strategy",
    "company_financial_strategy": "Financial_Strategy",
    "compliance_and_regulatory": "Compliance&Regulatory",
    "contact_identifiers": "Contact Identifier",
    "contractual": "Contractual",
    "crisis_sensitive_content": "Crisis_&_Sensitive",
    "direct_identifiers": "Direct Identifier",
    "financial_identifiers": "Financial Identifier",
    "health_disclosures": "Health_Disclosures",
    "litigation_sensitive": "Litigation Sensitive",
    "operational_security": "Operational_Security",
    "orgstructure_metadata": "Org_Structure_Metadata",
    "org_structure_metadata": "Org_Structure_Metadata",
    "privileged_communications": "Privileged_Communications",
    "project_metadata": "Project_Metadata",
    "scientific_and_ip_randd": "Scientific_&_IP",
    "security_behavioral_data": "Behavioral Data",
    "sensitive_vendor_documents": "Sensitive_Vendor_Docs",
    "support_and_escalation": "Support_&_Escalation",
    "system_operations": "System_Operations",
    "technical_randd": "Technical",
    "vendor_metadata": "Vendor_Metadata",
    # Already subdomain-shaped outputs from router:
    "financial_strategy": "Financial_Strategy",
    "hr": "HR",
    "technical": "Technical",
    "scientific_and_ip": "Scientific_&_IP",
}


def _normalize_domain_key(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("&", "and")
        .replace("-", "_")
    )


def _to_subdomain_candidates(domain: str) -> list[str]:
    domain_s = str(domain).strip()
    if not domain_s:
        return []
    key = _normalize_domain_key(domain_s)
    mapped = _RAG_DOMAIN_TO_SUBDOMAIN.get(key)
    cands = []
    if mapped:
        cands.append(mapped)
    # Also try original string as-is and light variants for compatibility.
    cands.extend(
        [
            domain_s,
            domain_s.replace("_", " "),
            domain_s.replace("_", "&"),
        ]
    )
    seen = set()
    out = []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _load_qdrant_config_from_database_file() -> tuple[str, str, str] | None:
    """Load Qdrant settings from sibling database config file if available."""
    cfg_path = ROOT.parent / "database" / "Schemas" / "config.py"
    if not cfg_path.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("clairos_database_config", str(cfg_path))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        url = str(getattr(module, "QDRANT_URL", "") or "").strip()
        api_key = str(getattr(module, "QDRANT_API_KEY", "") or "").strip()
        collection_name = str(getattr(module, "COLLECTION_NAME", "") or "").strip()
        if not url:
            return None
        return url, api_key, (collection_name or "clairos_email_chunks")
    except Exception:
        return None


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
        self._qdrant_client = None
        self._qdrant_models = None
        self._vector_ready = False
        self._qdrant_ready = False

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

    def _ensure_qdrant_backend(self):
        if self._qdrant_ready:
            return
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Filter, FieldCondition, MatchValue
        except Exception as exc:  # pragma: no cover - depends on local env
            raise RuntimeError(
                "Qdrant backend unavailable. Install qdrant-client."
            ) from exc

        qdrant_url = os.getenv("QDRANT_URL", "").strip()
        qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "clairos_email_chunks").strip() or "clairos_email_chunks"

        if not qdrant_url:
            loaded = _load_qdrant_config_from_database_file()
            if loaded:
                qdrant_url, qdrant_api_key, collection_name = loaded

        if not qdrant_url:
            raise RuntimeError(
                "QDRANT_URL is required for qdrant backend. Set env vars or provide "
                "database/Schemas/config.py with QDRANT_URL."
            )

        self._qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key or None)
        self._qdrant_models = {
            "Filter": Filter,
            "FieldCondition": FieldCondition,
            "MatchValue": MatchValue,
            "collection_name": collection_name,
        }
        self._qdrant_ready = True


    def _search_qdrant(
        self,
        question: str,
        domains_to_search: list[str],
        top_k: int,
    ) -> list[Hit]:
        self._ensure_qdrant_backend()
        self._ensure_vector_backend()

        qv = self._embedder.encode([question], normalize_embeddings=True)
        qvec = [float(x) for x in qv[0]]

        Filter = self._qdrant_models["Filter"]
        FieldCondition = self._qdrant_models["FieldCondition"]
        MatchValue = self._qdrant_models["MatchValue"]
        collection_name = self._qdrant_models["collection_name"]

        hits = []
        seen = set()

        if not domains_to_search:
            try:
                results = self._qdrant_client.query_points(
                    collection_name=collection_name,
                    query=qvec,
                    limit=top_k,
                    with_payload=True,
                ).points
            except Exception as e:
                print(f"Qdrant search error: {e}")
                return []

            for p in results:
                payload = p.payload or {}
                chunk_id = str(payload.get("chunk_id", ""))
                text = str(payload.get("text", ""))
                source = payload.get("source") or {}
                domain_name = str(payload.get("domain") or payload.get("subdomain") or "unknown")
                unique_key = (domain_name, chunk_id)
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                hits.append(Hit(
                    domain=domain_name,
                    chunk_id=chunk_id,
                    score=float(getattr(p, "score", 0.0) or 0.0),
                    method="qdrant_vector",
                    text=text,
                    source=source,
                ))
            return sorted(hits, key=lambda h: h.score, reverse=True)[:top_k]

        for routed_domain in domains_to_search:
            subdomain_cands = _to_subdomain_candidates(routed_domain)
            if not subdomain_cands:
                continue

            for sub in subdomain_cands:
                qfilter = Filter(
                    must=[FieldCondition(key="subdomain", match=MatchValue(value=sub))]
                )
                try:
                    results = self._qdrant_client.query_points(
                        collection_name=collection_name,
                        query=qvec,
                        query_filter=qfilter,
                        limit=top_k,
                        with_payload=True,
                    ).points
                except Exception as e:
                    print(f"Qdrant filtered search error ({sub}): {e}")
                    continue

                for p in results:
                    payload = p.payload or {}
                    chunk_id = str(payload.get("chunk_id", ""))
                    text = str(payload.get("text", ""))
                    source = payload.get("source") or {}
                    domain_name = str(payload.get("domain") or routed_domain)
                    unique_key = (domain_name, chunk_id)
                    # if unique_key in seen:
                    #    continue
                    seen.add(unique_key)
                    hits.append(Hit(
                        domain=domain_name,
                        chunk_id=chunk_id,
                        score=float(getattr(p, "score", 0.0) or 0.0),
                        method="qdrant_vector",
                        text=text,
                        source=source,
                    ))
        return sorted(hits, key=lambda h: h.score, reverse=True)[:top_k]

    # def _search_qdrant(
    #     self,
    #     question: str,
    #     domains_to_search: list[str],
    #     top_k: int,
    # ) -> list[Hit]:
    #     self._ensure_qdrant_backend()
    #     self._ensure_vector_backend()

    #     qv = self._embedder.encode([question], normalize_embeddings=True)
    #     qvec = [float(x) for x in qv[0]]

    #     Filter = self._qdrant_models["Filter"]
    #     FieldCondition = self._qdrant_models["FieldCondition"]
    #     MatchValue = self._qdrant_models["MatchValue"]
    #     collection_name = self._qdrant_models["collection_name"]

    #     hits = []
    #     seen = set()

    #     if not domains_to_search:
    #         try:
    #             results = self._qdrant_client.search(
    #                 collection_name=collection_name,
    #                 query_vector=qvec,
    #                 limit=top_k,
    #                 with_payload=True,
    #                 with_vectors=False,
    #             )
    #         except Exception:
    #             return []

    #         for p in results:
    #             payload = p.payload or {}
    #             chunk_id = str(payload.get("chunk_id", ""))
    #             text = str(payload.get("text", ""))
    #             source = payload.get("source") or {}
    #             domain_name = str(payload.get("domain") or payload.get("subdomain") or "unknown")
    #             unique_key = (domain_name, chunk_id)
    #             if unique_key in seen:
    #                 continue
    #             seen.add(unique_key)
    #             hits.append(
    #                 Hit(
    #                     domain=domain_name,
    #                     chunk_id=chunk_id,
    #                     score=float(getattr(p, "score", 0.0) or 0.0),
    #                     method="qdrant_vector",
    #                     text=text,
    #                     source=source,
    #                 )
    #             )
    #         return sorted(hits, key=lambda h: h.score, reverse=True)[:top_k]

    #     for routed_domain in domains_to_search:
    #         subdomain_cands = _to_subdomain_candidates(routed_domain)
    #         if not subdomain_cands:
    #             continue

    #         for sub in subdomain_cands:
    #             qfilter = Filter(
    #                 must=[
    #                     FieldCondition(key="subdomain", match=MatchValue(value=sub)),
    #                 ]
    #             )
    #             try:
    #                 results = self._qdrant_client.search(
    #                     collection_name=collection_name,
    #                     query_vector=qvec,
    #                     query_filter=qfilter,
    #                     limit=top_k,
    #                     with_payload=True,
    #                     with_vectors=False,
    #                 )
    #             except Exception:
    #                 continue

    #             for p in results:
    #                 payload = p.payload or {}
    #                 chunk_id = str(payload.get("chunk_id", ""))
    #                 text = str(payload.get("text", ""))
    #                 source = payload.get("source") or {}
    #                 domain_name = str(payload.get("domain") or routed_domain)
    #                 unique_key = (domain_name, chunk_id)
    #                 if unique_key in seen:
    #                     continue
    #                 seen.add(unique_key)
    #                 hits.append(
    #                     Hit(
    #                         domain=domain_name,
    #                         chunk_id=chunk_id,
    #                         score=float(getattr(p, "score", 0.0) or 0.0),
    #                         method="qdrant_vector",
    #                         text=text,
    #                         source=source,
    #                     )
    #                 )

    #     return sorted(hits, key=lambda h: h.score, reverse=True)[:top_k]

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
        backend: str | None = None,
    ) -> list[Hit]:
        backend_name = (backend or os.getenv("RAG_RETRIEVER_BACKEND", "auto")).strip().lower()

        if backend_name in {"qdrant", "auto"}:
            try:
                qdrant_hits = self._search_qdrant(question, domains_to_search, top_k)
                if qdrant_hits:
                    return qdrant_hits
                if backend_name == "qdrant":
                    return []
            except Exception:
                if backend_name == "qdrant":
                    raise

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
