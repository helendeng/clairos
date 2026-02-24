# backend/rag/rag_service.py
from typing import Any, Dict, List
from .retriever import DomainRetriever
from .llm_client import generate

DEFAULT_TOP_K = 5


def _format_context(hits) -> str:
    parts = []
    for h in hits:
        parts.append(
            f"[{h.domain} | {h.chunk_id} | {h.method} | score={h.score:.3f}]\n{h.text}"
        )
    return "\n\n".join(parts)


def run_rag(
    question: str,
    categories_to_search: List[str],
    top_k: int = DEFAULT_TOP_K,
    llm_provider: str = "deepseek_api",
    llm_model: str | None = None,
) -> Dict[str, Any]:
    retriever = DomainRetriever()  # uses backend/indexes automatically

    hits = retriever.search(
        question=question,
        domains_to_search=categories_to_search,
        top_k=top_k,
        use_bm25=True,
        use_vector=True,
    )

    context = _format_context(hits)

    prompt = f"""You are ClairOS (RAG demo).
Answer ONLY using the provided CONTEXT.
If the answer is not in the context, respond with NOT_FOUND.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    answer = generate(prompt, provider=llm_provider, model=llm_model)

    sources = []
    for h in hits:
        src = h.source or {}
        sources.append(
            {
                "domain": h.domain,
                "chunk_id": h.chunk_id,
                "score": h.score,
                "method": h.method,
                "email_id": src.get("email_id", ""),
                "subject": src.get("subject", ""),
                "timestamp": src.get("timestamp", ""),
            }
        )

    return {"answer": answer, "sources": sources}
