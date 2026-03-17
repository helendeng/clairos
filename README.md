# ClairOS AI Handoff Assistant

An institutional memory platform that ingests employee email archives (.mbox), tags content using zero-shot classification, stores it in a vector database, and lets new employees query it via a RAG-powered chat interface.

ClairOS is an institutional memory platform that:
1. Ingests employee email archives (.mbox files from the Enron dataset)
2. Tags email content using zero-shot classification (facebook/bart-large-mnli)
3. Stores tagged chunks in a Qdrant vector database
4. Lets new employees query the knowledge base via a RAG-powered chat interface
5. Has a manager view for reviewing/approving AI-generated handoff briefs
Privacy goal: Everything runs locally, no external LLM APIs. Uses local Ollama with qwen2.5:14b.

---

## Project Structure

```
pii-demo-project/
├── backend/
│   └── server.py              # FastAPI backend — main entry point
├── src/          
│   └── App.jsx                # React frontend (Vite)
├── Ingestion/                 # Email parsing + zero-shot classification
│   ├── dataTaggers/
│   │   ├── ZeroShot.py        # Loads facebook/bart-large-mnli model
│   │   ├── ZeroShotController.py
│   │   └── ZeroShotValidation.py
│   ├── Schemas/
│   │   ├── schemas.py
│   │   └── taxonomy.py
│   └── util/
│       └── parseMbox.py       # Entry point: controller(mbox_fp, zero_shot_classify_fn)
├── database/                  # Qdrant vector database layer
│   └── core/
│       └── ingest_chunks.py
├── rag_demo4/                 # RAG retrieval + generation
│   └── src/
│       └── rag_service.py     # Entry point: run_rag(question, ...)
├── data/
│   └── Inboxes_Enron_Employees/
│       └── *.mbox             # Sample Enron email archives
└── requirements.txt
```

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- [Ollama](https://ollama.com) installed locally
- Conda (recommended) or a Python virtual environment

---

## Setup

### 1. Install Python dependencies

From the project root:

```bash
pip install -r requirements.txt
```

> **Important:** Every time you `pip install` a new package, add it to `requirements.txt` in the same commit so teammates don't hit missing module errors.

### 2. Install frontend dependencies

```bash
cd pii-demo-project
npm install
```

### 3. Pull the required Ollama model

```bash
ollama pull llama3.2
```

Check available models anytime with `ollama list`.

---

## Running the App (3 terminals required)

You need **three terminals open simultaneously**.

**Terminal 1 — Ollama (LLM inference):**
```bash
ollama serve
```

**Terminal 2 — Backend (FastAPI):**
```bash
cd backend
uvicorn server:app --reload --port 8000
```

Verify it's running: open [http://localhost:8000](http://localhost:8000) — you should see:
```json
{"status": "ClairOS Backend Running!", "message": "Upload files to /upload or query at /query"}
```

**Terminal 3 — Frontend (React/Vite):**
```bash
cd pii-demo-project
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## How It Works

### Manager Flow
1. Upload a `.mbox` file via the Data Ingestion tab
2. The backend calls `parseMbox.py → ZeroShotController.py → ZeroShot.py` to parse and classify email chunks using `facebook/bart-large-mnli`
3. Tagged chunks are stored in the Qdrant vector database
4. The manager reviews the AI-generated handoff brief and approves/rejects/flags content

### Employee Flow
1. View the approved handoff brief
2. Ask questions in the chat tab
3. Answers are generated via the RAG pipeline in `rag_demo4/` using Ollama

---

## Ingestion Pipeline (Technical)

The ingestion entry point is `Ingestion/util/parseMbox.py`:

```python
from Ingestion.util.parseMbox import controller
from Ingestion.dataTaggers.ZeroShot import zero_shot_classify

results = controller('data/Inboxes_Enron_Employees/dasovich.mbox', zero_shot_classify)
```

The pipeline:
1. Parses each email in the `.mbox` into an `EmailRecord`
2. Splits email bodies into sentence/paragraph chunks
3. Runs zero-shot classification against taxonomy labels
4. Returns a list of tagged `OutputSchema` dicts
5. (When enabled) uploads to Qdrant via `database/core/ingest_chunks.py`

> **Note on compute:** `facebook/bart-large-mnli` (1.6GB) runs on CPU but is slow. For faster processing, use a GPU via RunPod or similar. The model falls back to CPU automatically — no code changes needed.

---

## Environment Variables (Backend)

Set these in a `.env` file in `backend/` or export them in your shell:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `deepseek_api` | `deepseek_api` or `ollama` |
| `LLM_API_MODEL` | `deepseek-chat` | Model name for DeepSeek API |
| `LLM_API_BASE_URL` | `https://api.deepseek.com` | DeepSeek API base URL |
| `LLM_API_KEY` | *(hardcoded fallback)* | Your DeepSeek API key |
| `RAG_TOP_K` | `5` | Number of chunks to retrieve |

---

## Common Issues

**`ModuleNotFoundError: No module named 'X'`**
→ Run `pip install -r requirements.txt` from the project root.

**`Error uploading file. Make sure backend is running!`**
→ Check that Terminal 2 (backend) is running and visit [http://localhost:8000](http://localhost:8000).

**Upload works but chat returns no results**
→ Check that Terminal 1 (Ollama) is running: `ollama serve`.

**Backend starts but crashes on import**
→ Make sure you're running uvicorn from the `backend/` directory, not the project root.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python FastAPI |
| LLM Inference | Ollama (local) / DeepSeek API |
| Classification | HuggingFace `facebook/bart-large-mnli` |
| Vector Database | Qdrant |
| RAG | Custom pipeline in `rag_demo4/` |
| Data | Enron Email Dataset (.mbox) |


You need 3 terminal windows running at the same time. 
# Terminal 1: Ollama (The AI Brain)
What it does: Runs the local AI model that answers questions and summarizes documents
How to start:  
bash  
ollama serve  

What you'll see: Messages about the server starting Leave it running! Don't close this window

# Terminal 2: Backend (The Middleman)
What it does: Receives files from your website, detects PII, talks to Ollama, sends results back.  
How to start:  
bash  
export PATH="/usr/local/bin:$PATH"  
cd ~/clairos/pii-demo-project/backend  
uvicorn server:app --reload --port 8000  
What you'll see: "Uvicorn running on http://127.0.0.1:8000" Leave it running! Don't close this window

# Terminal 3: Frontend (The Website)
What it does: Shows the pretty interface you see in your browser.  
How to start:  
bash  
export PATH="/usr/local/bin:$PATH"  
cd ~/clairos/pii-demo-project  
npm run dev  
What you'll see: "Local: http://localhost:5173/" Leave it running! Don't close this window

# Step 4: Open Your Browser
Go to: http://localhost:5173/  
Now you can upload files and ask questions!


# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
