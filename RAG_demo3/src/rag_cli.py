"""CLI demo for category-constrained RAG using local Ollama (Qwen2.5:14b-instruct).

This is the 'deliverable' demo version of RAG integration:
- Assume categories_to_search provided upstream
- Retrieve top_k chunks within those categories
- (No PII filtering in this demo)
- Send context to Ollama and print answer + sources

Run:
  python -m src.rag_cli
"""

from .retriever import DomainRetriever
from .ollama_llm import generate

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
    categories = input("categories_to_search (comma-separated, e.g., financial,legal): ").strip()
    categories_to_search = [d.strip() for d in categories.split(",") if d.strip()]
    question = input("question: ").strip()

    retriever = DomainRetriever()
    hits = retriever.search(question, categories_to_search, top_k=TOP_K, use_bm25=True)

    context = format_context(hits)
    prompt = PROMPT_TMPL.format(context=context, question=question)

    answer = generate(prompt, model=MODEL)

    print("\n=== SOURCES (top-k) ===")
    for h in hits:
        src = h.source or {}
        print(f"- {h.domain} | {h.chunk_id} | {h.method} | {h.score:.3f} | {src.get('email_id','')} | {src.get('subject','')}")

    print("\n=== ANSWER ===")
    print(answer)


if __name__ == "__main__":
    main()
