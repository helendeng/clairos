# rag_demo4/src/rag_service.py
from typing import Any, Dict, List
from .retriever import DomainRetriever
from .llm_client import generate

DEFAULT_TOP_K = 5

# Module-level singleton — loaded once, reused on every query
_retriever = DomainRetriever()


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

    hits = _retriever.search(
        question=question,
        domains_to_search=[],
        top_k=top_k,
        use_bm25=False,
        use_vector=True,
        backend="qdrant",
    )

    context = _format_context(hits)

    prompt = f"""You are a helpful assistant answering questions about an employee's role based on their emails.
Answer directly and concisely using only the email context below.
Do not mention the context, documents, or your own reasoning process.
Do not say "based on the context" or "the emails show" — just answer as fact.
If the information is not available, say "I don't have enough information about that."
Be extremely professional, concise, and formal in your tone. Avoid any casual language or speculation.
Provide as much context as is helpful for the employee, and cite the specific source documentation (not just "[domain | chunk_id]"
but rather a user friendly identifier like "From email titled 'Project Update - Q1 2024'") for each distinct piece of information
you use from the emails.

EMAIL CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

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