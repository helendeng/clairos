# Python backend server for ClairOS AI Handoff Assistant
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from numpy.ma import count
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
DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "30"))

def _available_categories() -> list[str]:
    index_dir = PROJECT_ROOT / "rag_demo4" / "indexes"
    return sorted([p.name.replace(".chunks.json", "") for p in index_dir.glob("*.chunks.json")])

def calculate_confidence(text, prompt_length):
    # Heuristic for brief generation (no retrieval scores available)
    base_confidence = 0.7
    if len(text) > 200:
        base_confidence += 0.1
    if re.search(r'\b\d{4}\b', text):
        base_confidence += 0.05
    if re.search(r'\b\d{1,2}/\d{1,2}\b', text):
        base_confidence += 0.05
    return min(base_confidence, 1.0)

def calculate_rag_confidence(sources: list) -> float:
    # Based on actual Qdrant cosine similarity scores
    if not sources:
        return 0.0
    scores = [s.get("score", 0.0) for s in sources if s.get("score")]
    if not scores:
        return 0.0
    return round(min(sum(scores) / len(scores), 1.0), 2)

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
def run_mbox_ingestion(mbox_path: str, doc_id: str, brief_prompt: str):
    ingestion_status[doc_id] = {"status": "running", "chunks_ingested": 0, "error": None}
    try:
        # Check if THIS specific file is already ingested
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
            # results = client.scroll(
            #     collection_name="clairos_email_chunks",
            #     scroll_filter=Filter(
            #         must=[FieldCondition(
            #             key="source.email_id",
            #             match=MatchValue(value=f"{doc_id}_0")
            #         )]
            #     ),
            #     limit=1
            # )
            # if results[0]:
            count = client.get_collection("clairos_email_chunks").points_count
            if count > 0:
                print(f"✓ {doc_id} already ingested ({count} chunks), skipping ZeroShot")
                brief_content = call_llm(brief_prompt)
                confidence = calculate_confidence(brief_content, len(brief_prompt))
                document_storage[doc_id] = (
                    f"Email archive: {doc_id}. Contains {count} classified "
                    f"email chunks in knowledge base."
                )
                ingestion_status[doc_id] = {
                    "status": "done",
                    "chunks_ingested": count,
                    "error": None,
                    "brief": brief_content,
                    "confidence": confidence
                }
                approval_storage["items"] = [{
                    "id": "1",
                    "type": "overview",
                    "title": "Role Overview",
                    "content": brief_content[:500],
                    "sources": [doc_id],
                    "approved": None,
                    "flagged": False,
                    "confidence": confidence
                }]
                return
        except Exception as e:
            print(f"Could not check Qdrant, proceeding with full ingestion: {e}")

        # Full ingestion — file not yet in Qdrant
        from database.core.create_collection import create_collection
        create_collection()

        from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
        from Ingestion.util.parseMbox import controller
        print(f"Starting mbox ingestion for {doc_id}...")
        chunks = controller(mbox_fp=mbox_path, zero_shot_classify_fn=zero_shot_classify)

        print("Generating handoff brief...")
        brief_content = call_llm(brief_prompt)
        confidence = calculate_confidence(brief_content, len(brief_prompt))

        document_storage[doc_id] = (
            f"Email archive: {doc_id}. Contains {len(chunks)} classified "
            f"email chunks in knowledge base."
        )
        ingestion_status[doc_id] = {
            "status": "done",
            "chunks_ingested": len(chunks) if chunks else 0,
            "error": None,
            "brief": brief_content,
            "confidence": confidence
        }
        approval_storage["items"] = [{
            "id": "1",
            "type": "overview",
            "title": "Role Overview",
            "content": brief_content[:500],
            "sources": [doc_id],
            "approved": None,
            "flagged": False,
            "confidence": confidence
        }]
        print(f"✓ Done: {len(chunks)} chunks, brief generated")

    except Exception as e:
        ingestion_status[doc_id] = {
            "status": "failed",
            "chunks_ingested": 0,
            "error": str(e),
            "brief": None,
            "confidence": None
        }
        print(f"❌ Ingestion failed: {e}")
    finally:
        try:
            os.remove(mbox_path)
        except Exception:
            pass

# OLD
# def run_mbox_ingestion(mbox_path: str, doc_id: str, brief_prompt: str):
    
#     ingestion_status[doc_id] = {"status": "running", "chunks_ingested": 0, "error": None}
#     try:
#         # Ensure collection exists
#         from database.core.create_collection import create_collection
#         create_collection()
        
#         from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
#         from Ingestion.util.parseMbox import controller
#         print(f"Starting mbox ingestion for {doc_id}...")
#         chunks = controller(mbox_fp=mbox_path, zero_shot_classify_fn=zero_shot_classify)
        
#         print("Generating handoff brief...")
#         brief_content = call_llm(brief_prompt)
#         confidence = calculate_confidence(brief_content, len(brief_prompt))
        
#         ingestion_status[doc_id] = {
#             "status": "done",
#             "chunks_ingested": len(chunks) if chunks else 0,
#             "error": None,
#             "brief": brief_content,
#             "confidence": confidence
#         }
        
#         # add
#         document_storage[doc_id] = (
#     f"Email archive: {doc_id}. "
#     f"Contains {len(chunks)} classified email chunks in the knowledge base. "
#     f"Topics covered: business strategy, regulatory compliance, HR, "
#     f"financial strategy, project metadata, scheduling, and more."
# )

#         approval_storage["items"] = [{
#             "id": "1",
#             "type": "overview",
#             "title": "Role Overview",
#             "content": brief_content[:500],
#             "sources": [doc_id],
#             "approved": None,
#             "flagged": False,
#             "confidence": confidence
#         }]
        
#         print(f"✓ Done: {len(chunks)} chunks, brief generated")
#     except Exception as e:
#         ingestion_status[doc_id] = {"status": "failed", "chunks_ingested": 0, "error": str(e), "brief": None, "confidence": None}
#         print(f"❌ Ingestion failed: {e}")
#     finally:
#         try:
#             os.remove(mbox_path)
#         except Exception:
#             pass

# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    content = await file.read()
    doc_id = file.filename

    if file.filename.lower().endswith(".mbox"):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mbox", dir="/tmp")
        tmp.write(content)
        tmp.close()

        preview_text = content.decode("utf-8", errors="ignore")[:3000]
        pii_results = detect_pii(preview_text)

        brief_prompt = f"""You are Trunq.io, an AI that creates employee handoff briefs.
            Based on this email archive, generate a professional handoff brief covering:
            - The employee's main responsibilities
            - Key projects and topics they were working on
            - Important contacts and relationships
            - Any ongoing issues or priorities to be aware of

            Be specific, actionable, and professional. No asterisks, no meta commentary, no headings with colons.

            Email archive preview:
            {preview_text}
            """
        document_storage[doc_id] = "[.mbox file — ingestion in progress.]"
        ingestion_status[doc_id] = {"status": "running", "chunks_ingested": 0, "error": None, "brief": None, "confidence": None}
        
        # Pass brief_prompt into background task
        background_tasks.add_task(run_mbox_ingestion, tmp.name, doc_id, brief_prompt)

        approval_storage["items"] = []
        approval_storage["metadata"] = {
            "doc_id": doc_id,
            "filename": file.filename,
            "pii_detected": pii_results["detected"],
            "pii_count": pii_results["redacted_count"]
        }

        return {
            "pii": pii_results,
            "summary": None,
            "filename": file.filename,
            "doc_id": doc_id,
            "confidence": None,
            "sources": [{"type": "document", "name": file.filename}],
            "ingestion": "started"
        }
        ingestion_note = "started"

    else:
        text = content.decode("utf-8", errors="ignore")
        document_storage[doc_id] = text
        pii_results = detect_pii(text)
        brief_prompt = f"""You are Trunq.io, an AI that creates employee handoff briefs.
Based on this email archive preview, generate a professional handoff brief covering:
- The employee's main responsibilities
- Key projects and topics they were working on
- Important contacts and relationships
- Any ongoing issues or priorities to be aware of

Be specific, actionable, and professional. Do not include anything meta about the prompt in your output, just labels, titles, or headings.
No asterisks, no meta commentary, no headings with colons.

{text[:3000]}
"""
        ingestion_note = "not_applicable"

    brief_content = call_llm(brief_prompt)
    sources = [{"type": "document", "name": file.filename}]
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

    rag_out = run_rag(
        question=question,
        categories_to_search=_available_categories(),
        top_k=DEFAULT_TOP_K,
        llm_provider="ollama",
        llm_model="qwen2.5:14b",
    )

    answer = rag_out.get("answer", "")
    sources = rag_out.get("sources", [])
    confidence = calculate_rag_confidence(sources)

    formatted_sources = [{"name": s.get("subject") or s.get("chunk_id", ""), "type": "knowledge_base"} for s in sources]

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": formatted_sources
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
    return {"status": "Trunq.io Backend Running!", "message": "Upload files to /upload or query at /query"}