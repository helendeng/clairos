# Python backend server for ClairOS AI Handoff Assistant
# This server handles file uploads, processes documents with an LLM, detects PII, and manages an approval workflow for managers. It also provides a simple query interface for employees to ask questions about
# the uploaded documents. The server uses FastAPI and can call either a local Ollama instance or the DeepSeek API for LLM processing. 
# Helen editing post Lulu changes

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import random
import re
import os
from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1] # Helen changed to parents[1] to go up two levels since server.py is in backend/ and we want to access rag_demo4/src/ files
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag_demo4.src.rag_service import run_rag  
# noqa: E402

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store full documents in memory
document_storage = {}

# Store approval states for manager review
approval_storage = {
    "items": [],
    "metadata": {}
}

# Simple PII detection using regex
def detect_pii(text):
    pii_found = []
    redacted_count = 0
    
    # SSN pattern
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):
        pii_found.append("Social Security Number")
        redacted_count += len(re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text))
    
    # Email pattern
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        pii_found.append("Email Address")
        redacted_count += len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    
    # Phone pattern
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
        pii_found.append("Phone Number")
        redacted_count += len(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))
    
    # Credit card pattern (simple)
    if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text):
        pii_found.append("Credit Card")
        redacted_count += len(re.findall(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text))
    
    return {
        "detected": list(set(pii_found)),
        "redacted_count": redacted_count
    }

DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek_api")
DEFAULT_DEEPSEEK_MODEL = os.getenv("LLM_API_MODEL", "deepseek-chat")
DEFAULT_DEEPSEEK_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://api.deepseek.com")
DEFAULT_DEEPSEEK_API_KEY = os.getenv("LLM_API_KEY", "sk-acb050a499c64547b5a5af2321aee72d")
DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "5"))


def _available_categories() -> list[str]:
    index_dir = PROJECT_ROOT / "rag_demo4" / "indexes"
    return sorted([p.name.replace(".chunks.json", "") for p in index_dir.glob("*.chunks.json")])


# Calculate confidence score based on response characteristics
def calculate_confidence(text, prompt_length):
    base_confidence = 0.7
    
    if len(text) > 200:
        base_confidence += 0.1
    
    if re.search(r'\b\d{4}\b', text):
        base_confidence += 0.05
    if re.search(r'\b\d{1,2}/\d{1,2}\b', text):
        base_confidence += 0.05
    
    if "don't have" in text.lower() or "verified context" in text.lower():
        base_confidence = 0.4 + random.uniform(0, 0.1)  # FIXED: random is now imported
    
    confidence = min(1.0, base_confidence + random.uniform(-0.05, 0.05))
    
    return round(confidence, 2)

# Call Ollama API
def call_ollama(prompt, model="llama3.2"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        return "Error calling Ollama"
    except Exception as e:
        return f"Error: {str(e)}"


def call_deepseek_api(
    prompt: str,
    model: str = DEFAULT_DEEPSEEK_MODEL,
    api_key: str = DEFAULT_DEEPSEEK_API_KEY,
    api_base_url: str = DEFAULT_DEEPSEEK_BASE_URL,
):
    try:
        response = requests.post(
            f"{api_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                return ""
            return choices[0].get("message", {}).get("content", "")
        return f"Error calling DeepSeek API: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def call_llm(prompt: str, provider: str = DEFAULT_LLM_PROVIDER, model: Optional[str] = None):
    provider_name = (provider or DEFAULT_LLM_PROVIDER).strip().lower()
    if provider_name in {"ollama", "local", "local_ollama"}:
        return call_ollama(prompt, model=model or "llama3.2")
    if provider_name in {"deepseek", "deepseek_api", "api", "openai_compatible"}:
        return call_deepseek_api(prompt, model=model or DEFAULT_DEEPSEEK_MODEL)
    return f"Unsupported llm_provider: {provider}. Use deepseek_api or ollama."

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode('utf-8', errors='ignore')
    
    doc_id = file.filename
    document_storage[doc_id] = text
    
    pii_results = detect_pii(text)
    
    # FIXED: was called `summary_prompt` but referenced as `brief_prompt` — unified to one variable
    brief_prompt = f"""Summarize this document in 3-4 sentences. Focus on key findings and main topics.
    
Document:
{text[:3000]}

Format your response clearly with these sections. 
Be specific and actionable. 
Do not include anything meta about the prompt in your output, just labels, titles, or headings. 
Do not include any asterisks. 
"""
    
    brief_content = call_llm(brief_prompt, provider=DEFAULT_LLM_PROVIDER)
    confidence = calculate_confidence(brief_content, len(brief_prompt))
    
    approval_storage["items"] = [
        {
            "id": "1",
            "type": "overview",
            "title": "Role Overview",
            "content": brief_content[:500],
            "sources": [file.filename],
            "approved": None,
            "flagged": False,
            "confidence": confidence
        }
    ]
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
        "sources": [{"type": "document", "name": file.filename}]
    }

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

    categories = _available_categories()
    
    rag_out = run_rag(
        question=question,
        categories_to_search=categories,
        top_k=DEFAULT_TOP_K,
        llm_provider="ollama",
        llm_model="qwen2.5:14b",
    )

    answer = rag_out.get("answer", "")
    confidence = calculate_confidence(answer, len(question))

    sources = [
        {"type": "document", "name": f"{s.get('domain', '')} | {s.get('subject', '')}"}
        for s in rag_out.get("sources", [])
    ]

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }

# FIXED: these endpoints were accidentally swallowed into the ''' comment block
@app.get("/approval-items")
async def get_approval_items():
    """Get items pending manager approval"""
    return approval_storage

@app.post("/approve-item")
async def approve_item(item_id: str = Form(...), approved: bool = Form(...), flagged: bool = Form(False)):
    """Manager approves/rejects an item"""
    for item in approval_storage["items"]:
        if item["id"] == item_id:
            item["approved"] = approved
            item["flagged"] = flagged
            return {"success": True, "item": item}
    return {"success": False, "error": "Item not found"}

@app.get("/")
def root():
    return {"status": "ClairOS Backend Running!", "message": "Upload files to /upload or query at /query"}

# Run with: uvicorn server:app --reload --port 8000