"""Simple retrieval Precision/Recall/F1 evaluation.

This evaluates the retriever (not the LLM) using ground-truth chunk_ids.
For each test case:
- retrieve top_k within provided domains
- precision = (# relevant retrieved) / k
- recall = (# relevant retrieved) / (# relevant total)
- F1 computed from precision and recall

This is a reasonable sanity test for RAG retrieval (often reported as Recall@K).
"""

import json
from pathlib import Path

from .retriever import DomainRetriever

ROOT = Path(__file__).resolve().parents[1]
TESTS_PATH = ROOT / "data" / "tests.json"


def prf(retrieved_ids, relevant_ids, k):
    retrieved_set = set(retrieved_ids)
    relevant_set = set(relevant_ids)
    tp = len(retrieved_set & relevant_set)
    precision = tp / max(k, 1)
    recall = tp / max(len(relevant_set), 1)
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1, tp


def main():
    tests = json.load(open(TESTS_PATH, "r", encoding="utf-8"))
    retriever = DomainRetriever()

    top_k = 5
    totals = {"p": 0.0, "r": 0.0, "f1": 0.0}

    print("=" * 70)
    print("RETRIEVAL EVAL (Precision/Recall/F1 over chunk IDs)")
    print("=" * 70)

    for i, t in enumerate(tests, 1):
        hits = retriever.search(
            t["question"],
            t["domains_to_search"],
            top_k=top_k,
            use_bm25=True,
            use_vector=False,
        )
        retrieved = [h.chunk_id for h in hits]
        p, r, f1, tp = prf(retrieved, t["relevant_chunk_ids"], top_k)
        totals["p"] += p
        totals["r"] += r
        totals["f1"] += f1

        status = "PASS" if tp > 0 else "FAIL"
        print(f"[{status}] Test {i}: {t['id']} | domains={t['domains_to_search']}")
        print(f"    Q: {t['question']}")
        print(f"    Relevant: {t['relevant_chunk_ids']}")
        print(f"    Retrieved: {retrieved}")
        print(f"    P={p:.2f} R={r:.2f} F1={f1:.2f}\n")

    n = max(len(tests), 1)
    print("=" * 70)
    print(f"AVERAGE @K={top_k}:  P={totals['p']/n:.2f}  R={totals['r']/n:.2f}  F1={totals['f1']/n:.2f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
