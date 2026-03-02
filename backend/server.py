# Python backend server for ClairOS AI Handoff Assistant
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import requests
import random
import re
import os
import tempfile
from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag_demo4.src.rag_service import run_rag

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
document_storage = {}
ingestion_status = {}
approval_storage = {
    "items": [],
    "metadata": {}
}

# ── PII detection ──────────────────────────────────────────────────────────────

def detect_pii(text):
    pii_found = []
    redacted_count = 0
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):
        pii_found.append("Social Security Number")
        redacted_count += len(re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text))
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        pii_found.append("Email Address")
        redacted_count += len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
        pii_found.append("Phone Number")
        redacted_count += len(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))
    if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text):
        pii_found.append("Credit Card")
        redacted_count += len(re.findall(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text))
    return {"detected": list(set(pii_found)), "redacted_count": redacted_count}

# ── LLM config ─────────────────────────────────────────────────────────────────

DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "5"))

def _available_categories() -> list[str]:
    index_dir = PROJECT_ROOT / "rag_demo4" / "indexes"
    return sorted([p.name.replace(".chunks.json", "") for p in index_dir.glob("*.chunks.json")])

def calculate_confidence(text, prompt_length):
    base_confidence = 0.7
    if len(text) > 200:
        base_confidence += 0.1
    if re.search(r'\b\d{4}\b', text):
        base_confidence += 0.05
    if re.search(r'\b\d{1,2}/\d{1,2}\b', text):
        base_confidence += 0.05
    if "don't have" in text.lower() or "verified context" in text.lower():
        base_confidence = 0.4 + random.uniform(0, 0.1)
    return round(min(1.0, base_confidence + random.uniform(-0.05, 0.05)), 2)

def call_ollama(prompt, model="qwen2.5:14b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Error calling Ollama: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def call_llm(prompt: str, provider: str = DEFAULT_LLM_PROVIDER, model: Optional[str] = None):
    provider_name = (provider or DEFAULT_LLM_PROVIDER).strip().lower()
    if provider_name in {"ollama", "local", "local_ollama"}:
        return call_ollama(prompt, model=model or DEFAULT_OLLAMA_MODEL)
    return f"Unsupported llm_provider: {provider}. Use ollama."

# ── Background mbox ingestion ──────────────────────────────────────────────────

def run_mbox_ingestion(mbox_path: str, doc_id: str):
    ingestion_status[doc_id] = {"status": "running", "chunks_ingested": 0, "error": None}
    try:
        from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
        from Ingestion.util.parseMbox import controller
        print(f"Starting mbox ingestion for {doc_id}...")
        chunks = controller(mbox_fp=mbox_path, zero_shot_classify_fn=zero_shot_classify)
        ingestion_status[doc_id] = {
            "status": "done",
            "chunks_ingested": len(chunks) if chunks else 0,
            "error": None
        }
        print(f"✓ Ingestion complete: {len(chunks)} chunks")
    except Exception as e:
        ingestion_status[doc_id] = {"status": "failed", "chunks_ingested": 0, "error": str(e)}
        print(f"❌ Ingestion failed: {e}")
    finally:
        try:
            os.remove(mbox_path)
        except Exception:
            pass

# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    content = await file.read()
    doc_id = file.filename

    if file.filename.lower().endswith(".mbox"):
        # Save to temp file for background ingestion
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mbox", dir="/tmp")
        tmp.write(content)
        tmp.close()

        document_storage[doc_id] = "[.mbox file — ingestion in progress. Ask questions after ingestion completes.]"
        background_tasks.add_task(run_mbox_ingestion, tmp.name, doc_id)

        preview_text = content.decode("utf-8", errors="ignore")[:3000]
        brief_prompt = f"""This is a raw email archive. Summarize in 3-4 sentences what topics appear.
Do not include asterisks or meta commentary.
Content preview:
{preview_text}
"""
        pii_results = detect_pii(preview_text)
        ingestion_note = "started"

    else:
        text = content.decode("utf-8", errors="ignore")
        document_storage[doc_id] = text
        pii_results = detect_pii(text)
        brief_prompt = f"""Summarize this document in 3-4 sentences. Focus on key findings and main topics.
Document:
{text[:3000]}
Be specific and actionable.
Do not include anything meta about the prompt in your output, just labels, titles, or headings.
Do not include any asterisks.
"""
        ingestion_note = "not_applicable"

    brief_content = call_llm(brief_prompt)
    confidence = calculate_confidence(brief_content, len(brief_prompt))

    approval_storage["items"] = [{
        "id": "1",
        "type": "overview",
        "title": "Role Overview",
        "content": brief_content[:500],
        "sources": [file.filename],
        "approved": None,
        "flagged": False,
        "confidence": confidence
    }]
    approval_storage["metadata"] = {
        "doc_id": doc_id,
        "filename": file.filename,
        "pii_detected": pii_results["detected"],
        "pii_count": pii_results["redacted_count"]
    }

    return {
        "pii": pii_results,
        "summary": brief_content,
        "filename": file.filename,
        "doc_id": doc_id,
        "confidence": confidence,
        "sources": [{"type": "document", "name": file.filename}],
        "ingestion": ingestion_note
    }

@app.get("/ingestion-status/{doc_id}")
async def get_ingestion_status(doc_id: str):
    if doc_id not in ingestion_status:
        return {"status": "not_started", "chunks_ingested": 0, "error": None}
    return ingestion_status[doc_id]

@app.post("/query")
async def query_document(
    question: str = Form(...),
    doc_id: str = Form(...),
    llm_provider: str = Form(DEFAULT_LLM_PROVIDER),
    llm_model: Optional[str] = Form(None),
):
    if doc_id not in document_storage:
        return {
            "question": question,
            "answer": "Error: Document not found. Please upload the document again.",
            "confidence": 0.0,
            "sources": []
        }

    status = ingestion_status.get(doc_id, {}).get("status")
    if status == "running":
        return {
            "question": question,
            "answer": "Ingestion is still in progress. Please wait a few minutes and try again.",
            "confidence": 0.0,
            "sources": []
        }

    doc_text = document_storage[doc_id]
    categories = _available_categories()
    rag_out = run_rag(
        question=question,
        categories_to_search=categories,
        top_k=DEFAULT_TOP_K,
        llm_provider="ollama",
        llm_model="qwen2.5:14b",
    )
    rag_context = rag_out.get("answer", "")

    combined_prompt = f"""You are ClairOS, an AI employee handoff assistant.
Answer the question using BOTH sources below.
Prioritize the UPLOADED DOCUMENT if it contains the answer.
If neither source contains the answer, say NOT_FOUND.

UPLOADED DOCUMENT ({doc_id}):
{doc_text[:3000]}

ADDITIONAL CONTEXT FROM KNOWLEDGE BASE:
{rag_context}

QUESTION: {question}

ANSWER:"""

    answer = call_llm(combined_prompt)
    confidence = calculate_confidence(answer, len(question))

    sources = [{"type": "document", "name": doc_id}]
    for s in rag_out.get("sources", []):
        sources.append({
            "type": "knowledge_base",
            "name": f"{s.get('domain', '')} | {s.get('subject', '')}"
        })

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }

@app.get("/approval-items")
async def get_approval_items():
    return approval_storage

@app.post("/approve-item")
async def approve_item(item_id: str = Form(...), approved: bool = Form(...), flagged: bool = Form(False)):
    for item in approval_storage["items"]:
        if item["id"] == item_id:
            item["approved"] = approved
            item["flagged"] = flagged
            return {"success": True, "item": item}
    return {"success": False, "error": "Item not found"}

@app.get("/")
def root():
    return {"status": "ClairOS Backend Running!", "message": "Upload files to /upload or query at /query"}