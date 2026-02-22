# ClairOS RAG Demo (Local, Ollama, Qwen2-14B) — Synthetic Data

This is a **CLI-only** RAG demo aligned with the “deliver-a-demo” assumptions:

- **Upstream semantic router provides** `domains_to_search` (RAG does not decide domains).
- Storage is assumed to be **domain-separated chunks** (pure-by-domain for this demo).
- **No PII / sensitive-matrix filtering is applied** in this demo. (Planned future step inserted **right before the LLM**.)
- Uses **local Ollama** with default model **Qwen2-14B**.

---

## Assumed input to the RAG module

RAG consumes:

```json
{
  "question": "...",
  "domains_to_search": ["financial"],
  "role": "employee"
}
```

Notes:
- `domains_to_search` comes from the **upstream router** (outside RAG).
- `role` comes from the **surrounding system/auth** (outside RAG).
- RAG internally uses a configurable `top_k` (default 5).

---

## What is stored in the domain databases (assumption)

Each domain has a list of already-chunked records (raw text + metadata). Example:

```json
{
  "chunk_id": "financial_0003",
  "domain": "financial",
  "text": "Please set up ACH for Vendor Z. Routing 021000021 and account 9876543210.",
  "source": {
    "email_id": "email_fin_01",
    "subject": "Vendor payment setup",
    "timestamp": "2026-01-10"
  }
}
```

### Raw text vs vectors (embeddings)

Conceptually we store **both**:
- **Raw chunk text**: what we pass to the LLM as context.
- **Vectors (embeddings)**: numeric “meaning fingerprints” used only for retrieval.

In this demo:
- Raw chunks are saved in `indexes/<domain>.chunks.json`.
- Vectors are stored inside a FAISS index file `indexes/<domain>.faiss`.

### What is a vector (embedding) in plain terms?

A vector is just a list of numbers representing the meaning of text.
- Similar meanings → vectors are close → retrieval finds relevant chunks.
- Different meanings → vectors are far.

---

## Techniques used in this demo

1) **Chunking (assumed upstream)**
   - Emails/documents are split into smaller chunks before indexing.

2) **Embedding + vector search (FAISS)**
   - We embed chunks and the user question using `sentence-transformers/all-MiniLM-L6-v2`.
   - For each selected domain, FAISS retrieves the most similar chunks.

3) **BM25 keyword retrieval (enabled by default)**
   - BM25 matches literal keywords/tokens.
   - Helpful when exact strings matter (codes, IDs, vendor names).

4) **Hybrid retrieval (FAISS + BM25)**
   - We run both retrievers, merge results, dedupe by `chunk_id`, and keep the best score.

5) **Top-K selection**
   - `top_k` (default 5) is a RAG-side parameter controlling how many chunks are sent to the LLM.
   - Databases do not store “top-k”; they store chunks and indexes.

6) **Grounded generation (local Ollama, Qwen2-14B)**
   - Retrieved chunks are formatted as compact context.
   - The prompt instructs the LLM to answer using only the provided context.

7) **Sources / traceability**
   - The CLI prints retrieved sources (domain, chunk_id, score, preview).

---

## Setup

### 1) Start Ollama and ensure model exists

```bash
ollama pull qwen2.5:14b
ollama serve
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

> Note: `numpy<2` is pinned to avoid common binary incompatibility issues on Windows.

### 3) Build indexes from the synthetic chunk data

```bash
python -m src.build_indexes
```

### 4) Run the interactive CLI demo

```bash
python -m src.rag_cli
```

You will be prompted for:
- role (string)
- domains_to_search (comma-separated)
- question

---

## Evaluation

### Retrieval metrics (Precision/Recall/F1@K)

Evaluates whether the expected `chunk_id` appears in the retrieved top K list.

```bash
python -m src.eval_retrieval
```

### End-to-end QA check (LLM output contains expected value)

Calls **Ollama** and checks whether the answer contains the expected target value (routing number / EIN / API key, etc.).

```bash
python -m src.eval_llm_qa
```

---

## Synthetic domains used (derived from the matrix)

- financial, legal, security, hr, strategic, rnd, operational, vendor, scheduling, personal, pii

---

## Next steps (accuracy boosters)

### A) Add re-ranking (recommended)

**Idea:** retrieve more candidates, then re-score them with a stronger model/algorithm.

Typical flow:
1. Retrieve candidate set (`candidate_k = 20`) using FAISS + BM25.
2. Re-rank candidates.
3. Keep final `top_k`.

Two practical rerank options:
- **RRF (Reciprocal Rank Fusion)**: cheap, uses ranks from FAISS/BM25, no extra model.
- **CrossEncoder re-ranker** (SentenceTransformers): more accurate, slower, needs a reranker model.

**Do we need code changes? Yes.** Minimal file-level changes:
- `src/retriever.py`: retrieve `candidate_k` and add a rerank step before returning.
- Add `src/reranker.py`: implement RRF or CrossEncoder scoring.
- `src/rag_cli.py`: optional flag to toggle rerank.
- (Optional) `src/eval_retrieval.py`: A/B compare no-rerank vs rerank.

### B) Add MMR diversification

Reduces near-duplicate chunks in top_k (post-processing step in `src/retriever.py`).

### C) Improve chunking strategy (upstream)

Chunk size and overlap often change recall a lot.

### D) Insert sensitive-matrix / PII policy gate (security step)

Planned placement: **after retrieval, before LLM**.
Uses Stage 1 spans + your role×sensitive matrix to redact or drop disallowed content.
