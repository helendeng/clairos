"""RAGAS evaluation for RAG QA (retrieval + generation quality).

This script builds a small dataset from data/tests.json, retrieves contexts,
generates answers via local Ollama, then runs RAGAS metrics.
"""

import json
import os
from typing import Optional
from pathlib import Path

from .retriever import DomainRetriever
from .ollama_llm import generate

ROOT = Path(__file__).resolve().parents[1]
TESTS_PATH = ROOT / "data" / "tests.json"

MODEL = "qwen2.5:14b-instruct"
TOP_K = 5

PROMPT_TMPL = """You are ClairOS (RAG PoC). Use ONLY the context.
Return ONLY the exact answer value, with no extra words.
If not found, return: NOT_FOUND

CONTEXT:
{context}

QUESTION:
{question}

ANSWER VALUE:
"""


def format_context(hits):
    return "\n\n".join([f"[{h.domain}|{h.chunk_id}] {h.text}" for h in hits])


def _check_ollama(base_url: str) -> bool:
    try:
        import requests

        resp = requests.get(f"{base_url}/api/tags", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def _build_llm(model: str, base_url: Optional[str]):
    try:
        from langchain_ollama import OllamaLLM

        return OllamaLLM(model=model, base_url=base_url)
    except Exception:
        try:
            from langchain_community.llms import Ollama

            return Ollama(model=model, base_url=base_url)
        except Exception as exc:
            raise RuntimeError(
                "Missing LangChain Ollama integration. Install langchain-ollama "
                "(preferred) or langchain-community."
            ) from exc


def main():
    # Avoid datasets importing torch (can fail on Windows if torch isn't installed properly).
    os.environ.setdefault("HF_DATASETS_DISABLE_TORCH", "1")
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.run_config import RunConfig

        # Import from the old metrics API which still works with LangChain LLMs
        from ragas.metrics import (
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        )

        # Use LangChain embeddings which have the embed_query method
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
    except Exception as exc:
        raise RuntimeError("Missing RAGAS dependencies. Install 'ragas' (and datasets).") from exc

    tests = json.load(open(TESTS_PATH, "r", encoding="utf-8"))
    retriever = DomainRetriever()

    rows = []
    for t in tests:
        if "expected_answer" not in t:
            continue
        hits = retriever.search(
            t["question"],
            t["domains_to_search"],
            top_k=TOP_K,
            use_bm25=True,
            use_vector=False,
        )
        contexts = [h.text for h in hits]
        prompt = PROMPT_TMPL.format(context=format_context(hits), question=t["question"])
        answer = generate(prompt, model=MODEL).strip()

        # RAGAS expects specific field names and formats
        row = {
            "question": t["question"],
            "answer": answer,
            "contexts": contexts,
            "ground_truth": t["expected_answer"],
        }
        rows.append(row)

    if not rows:
        print("No tests with expected_answer found.")
        return

    dataset = Dataset.from_list(rows)
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    if not _check_ollama(base_url):
        print(
            "Ollama is not reachable at "
            f"{base_url}. Start Ollama or set OLLAMA_BASE_URL."
        )
        return

    llm = _build_llm(MODEL, base_url)

    # Use LangChain's HuggingFace embeddings (has embed_query method needed by answer_relevancy)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Verify embeddings has the required methods
    if not hasattr(embeddings, 'embed_query'):
        print("WARNING: embeddings object missing embed_query method!")
        print(f"Available methods: {[m for m in dir(embeddings) if not m.startswith('_')]}")

    # Use pre-configured metric instances from ragas.metrics (old API but still works)
    # These are already initialized and will use the llm/embeddings passed to evaluate()
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]

    # Print all data points for debugging
    print("\n" + "=" * 70)
    print("RAGAS EVALUATION - ALL SAMPLES")
    print("=" * 70)
    print(f"Dataset size: {len(rows)} samples\n")

    for idx, sample in enumerate(rows, 1):
        print(f"Sample #{idx}:")
        print(f"  Question: {sample['question']}")
        print(f"  Answer: {sample['answer']}")
        print(f"  Ground truth: {sample['ground_truth']}")
        print(f"  Contexts ({len(sample['contexts'])} chunks):")
        for i, ctx in enumerate(sample['contexts'], 1):
            print(f"    [{i}] {ctx[:80]}{'...' if len(ctx) > 80 else ''}")

        # Check if answer matches ground truth
        exact_match = sample['answer'] == sample['ground_truth']
        contains = sample['ground_truth'].lower() in sample['answer'].lower()
        print(f"  Exact match: {exact_match} | Contains GT: {contains}")
        print()

    print("=" * 70 + "\n")

    run_config = RunConfig(max_workers=1, timeout=120, max_retries=2)
    results = evaluate(
        dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
        run_config=run_config,
    )

    print("\n" + "=" * 70)
    print("RAGAS RESULTS")
    print("=" * 70)
    print(results)
    print("=" * 70)


if __name__ == "__main__":
    main()
