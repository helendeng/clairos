# ClairOS RAG Demo3 - Handoff README

This repo now contains:
- A RAG backend pipeline (`src/*`)
- A demo web app (`clairos/src`) + FastAPI bridge (`clairos/backend/server.py`)
- Evaluation scripts for retrieval, QA, and RAGAS

The goal of this README is to help teammates (especially database integration) connect quickly.

## 1) Main Files and Responsibilities

### Core RAG (`src/`)
- `src/retriever.py`
  Hybrid retrieval (FAISS vector + BM25), now with RRF fusion for more stable ranking.
- `src/rag_service.py`
  End-to-end RAG service: retrieve context -> build prompt -> call LLM -> return answer + sources.
- `src/llm_client.py`
  Unified LLM caller. Supports:
  - `deepseek_api` (default)
  - `ollama` (local)
- `src/ollama_llm.py`
  Backward-compatible wrapper for local Ollama only.
- `src/build_indexes.py`
  Builds FAISS indexes from `data/*.chunks.json` into `indexes/`.

### Evaluation (`src/`)
- `src/eval_retrieval.py`
  Retrieval metrics (Precision/Recall/F1), supports `EVAL_TESTS_PATH`.
- `src/eval_llm_qa.py`
  Simple QA accuracy check, supports `EVAL_TESTS_PATH`.
- `src/eval_ragas.py`
  RAGAS metrics, now supports DeepSeek API and `EVAL_TESTS_PATH`.

### Web Demo
- `clairos/backend/server.py`
  FastAPI bridge for web:
  - `/upload`: upload file, basic PII regex check, summary generation
  - `/query`: now calls `src.rag_service.run_rag(...)`
- `clairos/src/App.jsx`
  Demo UI for upload + inquiry (query), with LLM provider switch.

### Data and Indexes
- `data/*.chunks.json`: source chunks
- `indexes/*.faiss` and `indexes/*.chunks.json`: retrieval indexes and chunk copies
- `data/tests.json`: full test set
- `data/tests_singlehop.json`: single-hop subset
- `data/tests_multihop.json`: multi-hop subset

## 2) How To Run

## 2.1 Install
(optional virtual environment)```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

## 2.2 Build indexes
```bash
python -m src.build_indexes
```

## 2.3 CLI RAG
```bash
python -m src.rag_cli
```

### 2.3.1 Realtime DB Retrieval (no JSON export needed)
`rag_cli` now supports live retrieval from Qdrant so database updates are immediately queryable.

PowerShell example:
```powershell
$env:RAG_RETRIEVER_BACKEND="qdrant"   # qdrant | auto | local
$env:QDRANT_URL="https://<your-endpoint>:6333"
$env:QDRANT_API_KEY="<your-api-key>"
$env:QDRANT_COLLECTION_NAME="clairos_email_chunks"  # optional
python -m src.rag_cli
```

Notes:
- `RAG_RETRIEVER_BACKEND=auto` (default): try Qdrant first, fallback to local FAISS/BM25.
- `RAG_RETRIEVER_BACKEND=qdrant`: force live DB retrieval only.
- `RAG_RETRIEVER_BACKEND=local`: keep old behavior (indexes/*.faiss + *.chunks.json).
- If env vars are not set, retriever will try loading Qdrant settings from `../database/Schemas/config.py`.

## 2.4 Web demo backend
```bash
cd clairos/backend
uvicorn server:app --reload --port 8000

(or use): 
cd clairos
npm run dev
```

## 2.5 Web demo frontend (new terminal)
```bash
cd clairos
npm install
npm run dev

(or use)
cd clairos
npm run dev
```


## 2.6 Evaluation examples
```bash
# single-hop ragas
set EVAL_TESTS_PATH=C:\path\to\rag_demo3\data\tests_singlehop.json
set EVAL_LLM_PROVIDER=deepseek_api
python -m src.eval_ragas

(or use)
$env:EVAL_TESTS_PATH="C:\path\to\repo\data\tests_singlehop.json"
$env:EVAL_LLM_PROVIDER="deepseek_api"
python -m src.eval_ragas


# multi-hop ragas
set EVAL_TESTS_PATH=C:\path\to\rag_demo3\data\tests_multihop.json
set EVAL_LLM_PROVIDER=deepseek_api
python -m src.eval_ragas
```

PowerShell form:
```powershell
$env:EVAL_TESTS_PATH="C:\path\to\rag_demo3\data\tests_multihop.json"
$env:EVAL_LLM_PROVIDER="deepseek_api"
python -m src.eval_ragas
```

## 3) What Changed Compared to the Original Baseline

1. Added DeepSeek API support for inquiry and evaluation
- Inquiry path supports `deepseek_api` and `ollama` via unified LLM client.
- RAGAS script also supports DeepSeek API.

2. Website inquiry path now uses RAG pipeline
- Web `/query` now uses `src/rag_service.py` instead of plain direct document prompting.

3. Added a demo website integration path and documented current limits
- Demo UI and backend are runnable for end-to-end demo.
- Current limitations are listed below.

4. Expanded dataset and tests
- Increased chunk counts across categories.
- Expanded total tests and split into single-hop vs multi-hop.
- Improved low RAGAS metrics by tuning retrieval and evaluation prompts.

## 4) Current Limitations (Important)

1. Uploaded file inquiry is not fully indexed into persistent retrieval storage yet
- Upload currently stores file content in memory (`document_storage`), not database.
- RAG retrieval primarily uses prebuilt `indexes/*`.

2. No upstream DB connection yet
- No persistent doc/chunk storage in SQL/NoSQL.
- No production ingestion pipeline.

3. `domains_to_search` is not yet connected to real upstream router
- Current web path can pass/derive categories, but upstream integration is still pending.

## 5) Integration Notes for Database Teammates

Recommended integration points:
- Ingestion: replace in-memory upload flow with DB-backed chunk persistence.
- Index update: add incremental index build/update after new chunk inserts.
- Query: map upstream router output to `categories_to_search` before calling `run_rag`.

Useful function signatures:
- `src.rag_service.run_rag(question, categories_to_search, top_k, llm_provider, llm_model)`
- `src.retriever.DomainRetriever.search(question, domains_to_search, top_k, use_bm25, use_vector, fusion)`

## 6) Next Steps

1. Connect upstream database and router (`domains_to_search`) end-to-end.
2. Enable real-world email ingestion and chunking pipeline.
3. Run larger-scale evaluation (100+ tests) on real data.
4. Add production-safe observability (latency, retrieval hit quality, failure reasons).
