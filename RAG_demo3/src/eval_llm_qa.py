"""Optional: LLM answer check (very simple).

We ask the model to output ONLY the requested value (exact string), then
score as correct if expected_answer is a substring of the model output.

This is a crude but practical demo metric.
"""

import json
import re
from difflib import SequenceMatcher
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


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fuzzy_match(expected: str, output: str) -> bool:
    exp = _normalize(expected)
    out = _normalize(output)
    if not exp:
        return False
    if exp in out:
        return True
    exp_tokens = exp.split()
    out_tokens = out.split()
    if len(exp_tokens) <= 3:
        return all(t in out_tokens for t in exp_tokens)
    ratio = SequenceMatcher(None, exp, out).ratio()
    return ratio >= 0.8


def main():
    tests = json.load(open(TESTS_PATH, "r", encoding="utf-8"))
    retriever = DomainRetriever()

    correct = 0
    total = 0

    print("=" * 70)
    print("LLM QA EVAL (substring match on expected_answer)")
    print("=" * 70)

    for i, t in enumerate(tests, 1):
        if "expected_answer" not in t:
            continue
        hits = retriever.search(
            t["question"],
            t["domains_to_search"],
            top_k=TOP_K,
            use_bm25=True,
            use_vector=False,
        )
        prompt = PROMPT_TMPL.format(context=format_context(hits), question=t["question"])
        out = generate(prompt, model=MODEL).strip()

        ok = _fuzzy_match(t["expected_answer"], out)
        correct += 1 if ok else 0
        total += 1

        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Test {i}: {t['id']} expected={t['expected_answer']}")
        print(f"    model_out: {out}\n")

    acc = correct / max(total, 1)
    print("=" * 70)
    print(f"Accuracy: {correct}/{total} = {acc:.2%}")
    print("=" * 70)


if __name__ == "__main__":
    main()
