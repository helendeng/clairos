"""RAGAS evaluation for RAG QA (retrieval + generation quality).

This script builds a small dataset from data/tests.json, retrieves contexts,
generates natural-language answers via configurable LLM provider, then runs RAGAS metrics.
"""

import json
import os
import math
from typing import Optional
from pathlib import Path

from .retriever import DomainRetriever
from .llm_client import generate

ROOT = Path(__file__).resolve().parents[1]
TESTS_PATH = Path(os.getenv("EVAL_TESTS_PATH", str(ROOT / "data" / "tests.json")))

MODEL = "qwen2.5:14b-instruct"
PROVIDER = os.getenv("EVAL_LLM_PROVIDER", "deepseek_api")
API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://api.deepseek.com")
API_MODEL = os.getenv("LLM_API_MODEL", "deepseek-chat")
API_KEY = os.getenv("LLM_API_KEY", "sk-acb050a499c64547b5a5af2321aee72d")
TOP_K = int(os.getenv("RAGAS_TOP_K", "5"))        # wider candidate pool for reranker
_rerank_top_k_env = os.getenv("RERANK_TOP_K")
if _rerank_top_k_env is not None:
    RERANK_TOP_K = int(_rerank_top_k_env)
else:
    # Multi-hop usually needs two supporting chunks; keep one extra for stability.
    RERANK_TOP_K = 3 if "multihop" in TESTS_PATH.name.lower() else 2
USE_BM25 = os.getenv("RAGAS_USE_BM25", "1").strip() not in {"0", "false", "False"}
USE_VECTOR = os.getenv("RAGAS_USE_VECTOR", "1").strip() not in {"0", "false", "False"}
ENABLE_ANSWER_RELEVANCY = os.getenv("RAGAS_ENABLE_ANSWER_RELEVANCY", "1").strip() not in {"0", "false", "False"}
RAISE_EXCEPTIONS = os.getenv("RAGAS_RAISE_EXCEPTIONS", "0").strip() in {"1", "true", "True"}

PROMPT_TMPL = """You are ClairOS (RAG PoC). Use ONLY the context below.
Answer in one or two complete, concise sentences.
Your answer must be self-contained: restate the key subject from the question, then provide all requested facts.
If multiple facts are needed, connect them naturally (e.g., "X is A and Y is B").
Do not add background knowledge or details not present in the context.
If the answer is not present in context, return exactly: NOT_FOUND

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

_cross_encoder = None
_cross_encoder_tried = False


def _get_cross_encoder():
    """Lazy-load the cross-encoder reranker (singleton).

    Uses a separate boolean flag so that _cross_encoder stays typed as
    CrossEncoder | None, avoiding spurious 'Literal[True]' type-checker errors.
    """
    global _cross_encoder, _cross_encoder_tried
    if not _cross_encoder_tried:
        _cross_encoder_tried = True
        try:
            from sentence_transformers import CrossEncoder
            _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except Exception:
            _cross_encoder = None
    return _cross_encoder


def rerank_hits(hits, question: str, keep_top_k: int = RERANK_TOP_K):
    """Rerank hits with a cross-encoder and return the top *keep_top_k* results.

    Strategy: score every (question, chunk) pair and keep only the highest-scoring
    ones.  This removes low-relevance "noise" chunks that survive BM25/vector fusion
    (e.g. a scheduling fragment retrieved for an unrelated scheduling question) while
    still preserving multiple relevant chunks for multi-hop questions (each of which
    answers a different sub-question and may score differently).

    Falls back to hits[:keep_top_k] when the cross-encoder is unavailable.
    """
    if len(hits) <= keep_top_k:
        return hits
    reranker = _get_cross_encoder()
    if reranker is None:
        return hits[:keep_top_k]
    pairs = [(question, h.text) for h in hits]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, hits), key=lambda x: x[0], reverse=True)
    return [h for _, h in ranked[:keep_top_k]]


def format_context(hits):
    return "\n\n".join([f"[{h.domain}|{h.chunk_id}] {h.text}" for h in hits])


def _check_ollama(base_url: str) -> bool:
    try:
        import requests

        resp = requests.get(f"{base_url}/api/tags", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def _build_ollama_llm(model: str, base_url: Optional[str]):
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


def _build_openai_compatible_chat(model: str, base_url: str, api_key: str):
    try:
        from langchain_openai import ChatOpenAI
    except Exception as exc:
        raise RuntimeError(
            "Missing langchain-openai dependency. Install langchain-openai to use deepseek/api provider."
        ) from exc

    return ChatOpenAI(model=model, base_url=base_url, api_key=api_key, temperature=0)


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
    print(
        f"Eval config: top_k={TOP_K}, rerank_top_k={RERANK_TOP_K}, use_bm25={USE_BM25}, use_vector={USE_VECTOR}, provider={PROVIDER}"
    )

    rows = []
    for t in tests:
        if "expected_answer" not in t:
            continue
        hits = retriever.search(
            t["question"],
            t["domains_to_search"],
            top_k=TOP_K,
            use_bm25=USE_BM25,
            use_vector=USE_VECTOR,
        )
        hits = rerank_hits(hits, t["question"])
        contexts = [h.text for h in hits]
        prompt = PROMPT_TMPL.format(context=format_context(hits), question=t["question"])
        selected_model = MODEL if PROVIDER.lower() in {"ollama", "local", "local_ollama"} else API_MODEL
        answer = generate(prompt, provider=PROVIDER, model=selected_model).strip()
        answer = " ".join(answer.split())
        if not answer:
            answer = "NOT_FOUND"

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
    provider_name = PROVIDER.lower()

    if provider_name in {"ollama", "local", "local_ollama"}:
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        if not _check_ollama(base_url):
            print(
                "Ollama is not reachable at "
                f"{base_url}. Start Ollama or set OLLAMA_BASE_URL."
            )
            return
        llm = _build_ollama_llm(MODEL, base_url)
    elif provider_name in {"deepseek", "deepseek_api", "api", "openai_compatible"}:
        llm = _build_openai_compatible_chat(API_MODEL, API_BASE_URL, API_KEY)
    else:
        raise ValueError(
            f"Unsupported EVAL_LLM_PROVIDER '{PROVIDER}'. Use deepseek_api or ollama."
        )

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
        context_precision,
        context_recall,
    ]
    if ENABLE_ANSWER_RELEVANCY:
        # DeepSeek OpenAI-compatible endpoint supports only n=1.
        # answer_relevancy may request multiple generations via strictness>1.
        if provider_name in {"deepseek", "deepseek_api", "api", "openai_compatible"}:
            try:
                answer_relevancy.strictness = 1
            except Exception:
                pass
        metrics.insert(1, answer_relevancy)

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
        raise_exceptions=RAISE_EXCEPTIONS,
    )

    print("\n" + "=" * 70)
    print("RAGAS RESULTS")
    print("=" * 70)
    print(results)
    try:
        result_dict = dict(results)
        v = result_dict.get("answer_relevancy")
        if isinstance(v, float) and math.isnan(v):
            print(
                "NOTE: answer_relevancy is NaN. Metric computation failed for most/all samples "
                "(often evaluator LLM output-format mismatch or parsing failure). "
                "Set RAGAS_RAISE_EXCEPTIONS=1 to see exact exceptions."
            )
    except Exception:
        pass
    print("=" * 70)


if __name__ == "__main__":
    main()

