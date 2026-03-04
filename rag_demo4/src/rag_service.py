# rag_demo4/src/rag_service.py
from typing import Any, Dict, List
from .retriever import DomainRetriever
from .llm_client import generate

DEFAULT_TOP_K = 15 #increased number of chunks retrieved to provide more context to the LLM, since we're now using a more powerful model (Qwen2.5-14B) that can handle longer inputs

_retriever = None

def _get_retriever() -> DomainRetriever:
    global _retriever
    if _retriever is None:
        _retriever = DomainRetriever()
        _retriever._ensure_qdrant_backend()
        _retriever._ensure_vector_backend()
    return _retriever

def _format_context(hits) -> str:
    parts = []
    for h in hits:
        src = h.source or {}
        subject = src.get("subject", "unknown subject")
        timestamp = src.get("timestamp", "")
        parts.append(
            f"[Email: '{subject}' ({timestamp})]\n{h.text}"
        )
    return "\n\n".join(parts)

def run_rag(question, categories_to_search, top_k=DEFAULT_TOP_K, llm_provider="deepseek_api", llm_model=None):
    retriever = _get_retriever()
    hits = retriever.search(question=question, domains_to_search=[], top_k=top_k, use_bm25=False, use_vector=True, backend="qdrant")

    print(f"DEBUG: got {len(hits)} hits from Qdrant")
    if hits:
        print(f"DEBUG first hit: {hits[0].text[:200]}")

    context = _format_context(hits)
    prompt = f"""You are a helpful assistant answering questions about an employee's role at a company based on their files and inbox.
Answer directly and concisely, as helpfully as possible, using only the email context below.
Do not mention your own reasoning process. 
Do not say "based on the context" or "the emails show" — just answer as fact.
Do not say "based on the context" or "the emails show" - just answer as fact.
If the excerpts are only partially relevant, synthesize what you can from them and answer as best you can. 
Cite the email subject in your answer where relevant.
If it's hard to find relevant context, still try to provide helpful context from other documents in the source file that you have ingested and chunked.
Use the best of your reasoning ability to connect the dots and provide a helpful answer, but be clear about the limits of what you can infer from the available information.
Try to avoid, but as a last resort: If relevant information is truly not at all available, or if the excerpts are completely unrelated to the question, you can say "I don't have enough information about that."
Where relevant, cite the email subject in your answer.
Be extremely professional, concise, and formal in your tone. Avoid any casual language or speculation.

EMAIL EXCERPTS/CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    answer = generate(prompt, provider=llm_provider, model=llm_model)
    sources = [{"domain": h.domain, "chunk_id": h.chunk_id, "score": h.score, "method": h.method,
                "email_id": (h.source or {}).get("email_id",""), "subject": (h.source or {}).get("subject",""),
                "timestamp": (h.source or {}).get("timestamp","")} for h in hits]
    return {"answer": answer, "sources": sources}

# # rag_demo4/src/rag_service.py
# from typing import Any, Dict, List
# from .retriever import DomainRetriever
# from .llm_client import generate

# DEFAULT_TOP_K = 5

# # Module-level singleton — loaded once, reused on every query
# _retriever = DomainRetriever()


# def _format_context(hits) -> str:
#     parts = []
#     for h in hits:
#         parts.append(
#             f"[{h.domain} | {h.chunk_id} | {h.method} | score={h.score:.3f}]\n{h.text}"
#         )
#     return "\n\n".join(parts)


# def run_rag(
#     question: str,
#     categories_to_search: List[str],
#     top_k: int = DEFAULT_TOP_K,
#     llm_provider: str = "deepseek_api",
#     llm_model: str | None = None,
# ) -> Dict[str, Any]:

#     hits = _retriever.search(
#         question=question,
#         domains_to_search=[],
#         top_k=top_k,
#         use_bm25=False,
#         use_vector=True,
#         backend="qdrant",
#     )

#     # TEMP DEBUG — remove before demo
#     print(f"DEBUG: got {len(hits)} hits from Qdrant")
#     if hits:
#         print(f"DEBUG first hit: {hits[0].text[:200]}")


#     context = _format_context(hits)

#     prompt = f"""You are a helpful assistant answering questions about an employee's role based on their emails.
# Answer directly and concisely using only the email context below.
# Do not mention the context, documents, or your own reasoning process.
# Do not say "based on the context" or "the emails show" — just answer as fact.
# If the information is not available, say "I don't have enough information about that."
# Be extremely professional, concise, and formal in your tone. Avoid any casual language or speculation.
# Provide as much context as is helpful for the employee, and cite the specific source documentation (not just "[domain | chunk_id]"
# but rather a user friendly identifier like "From email titled 'Project Update - Q1 2024'") for each distinct piece of information
# you use from the emails.

# EMAIL CONTEXT:
# {context}

# QUESTION: {question}

# ANSWER:"""

#     answer = generate(prompt, provider=llm_provider, model=llm_model)

#     sources = []
#     for h in hits:
#         src = h.source or {}
#         sources.append(
#             {
#                 "domain": h.domain,
#                 "chunk_id": h.chunk_id,
#                 "score": h.score,
#                 "method": h.method,
#                 "email_id": src.get("email_id", ""),
#                 "subject": src.get("subject", ""),
#                 "timestamp": src.get("timestamp", ""),
#             }
#         )

#     return {"answer": answer, "sources": sources}