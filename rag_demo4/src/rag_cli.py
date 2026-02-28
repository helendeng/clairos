"""CLI demo for category-constrained RAG using selectable LLM provider.

This is the 'deliverable' demo version of RAG integration:
- Assume categories_to_search provided upstream
- Retrieve top_k chunks within those categories
- (No PII filtering in this demo)
- Send context to selected LLM and print answer + sources

Run:
  python -m src.rag_cli
"""

from .retriever import DomainRetriever
from .llm_client import generate
from .domain_router import get_domains_to_search
import os

MODEL = "qwen2.5:14b-instruct"
TOP_K = 5

PROMPT_TMPL = """You are ClairOS (RAG PoC). Answer ONLY using the context.
If the answer is not in the context, say: I don't know.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


def format_context(hits):
    lines = []
    for h in hits:
        preview = h.text.replace("\n", " ")
        lines.append(f"[{h.domain}|{h.chunk_id}|{h.method}|score={h.score:.3f}] {preview}")
    return "\n\n".join(lines)


def main():
    question = input("question: ").strip()
    retriever_backend = os.getenv("RAG_RETRIEVER_BACKEND", "auto")
    bypass_router = os.getenv("RAG_BYPASS_ROUTER", "0").strip().lower() in {"1", "true", "yes"}

    if bypass_router:
        categories_to_search = []
        print("domain_router bypassed: querying all available Qdrant chunks")
    else:
        try:
            categories_to_search = get_domains_to_search(question)
            print(f"domains_to_search (auto): {categories_to_search}")
            if not categories_to_search and retriever_backend not in {"qdrant", "auto"}:
                print("No routed domains. Unable to retrieve context.")
                return
        except Exception as exc:
            if retriever_backend in {"qdrant", "auto"}:
                categories_to_search = []
                print(f"domain_router failed ({exc}); falling back to all-domain Qdrant search")
            else:
                raise

    llm_provider = input("llm_provider [deepseek_api/ollama] (default: deepseek_api): ").strip() or "deepseek_api"
    llm_model = input("llm_model (blank for provider default): ").strip() or None

    retriever = DomainRetriever()
    print(f"retriever_backend: {retriever_backend}")
    hits = retriever.search(
        question,
        categories_to_search,
        top_k=TOP_K,
        use_bm25=True,
        backend=retriever_backend,
    )

    context = format_context(hits)
    prompt = PROMPT_TMPL.format(context=context, question=question)

    selected_model = llm_model or (MODEL if llm_provider.lower() in {"ollama", "local", "local_ollama"} else None)
    answer = generate(prompt, provider=llm_provider, model=selected_model)

    print("\n=== SOURCES (top-k) ===")
    for h in hits:
        src = h.source or {}
        print(f"- {h.domain} | {h.chunk_id} | {h.method} | {h.score:.3f} | {src.get('email_id','')} | {src.get('subject','')}")

    print("\n=== ANSWER ===")
    print(answer)


if __name__ == "__main__":
    main()
