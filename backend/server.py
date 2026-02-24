from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
import os
from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_service import run_rag  # noqa: E402

# Store documents in memory
document_storage = {}

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple PII detection using regex (your teammates can replace with ML models)
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
    index_dir = PROJECT_ROOT / "indexes"
    return sorted([p.name.replace(".chunks.json", "") for p in index_dir.glob("*.chunks.json")])


def call_ollama(prompt: str, model: str = "llama3.2"):
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
    # Read file content
    content = await file.read()
    text = content.decode('utf-8', errors='ignore')
    
    # Store full document
    doc_id = file.filename
    document_storage[doc_id] = text
    
    # Detect PII
    pii_results = detect_pii(text)
    
    # Generate summary using configured provider
    summary_prompt = f"""Summarize this document in 3-4 sentences. Focus on key findings and main topics.
    
Document:
{text[:2000]}  

Provide a brief executive summary."""
    
    summary = call_llm(summary_prompt, provider=DEFAULT_LLM_PROVIDER)
    
    return {
        "pii": pii_results,
        "summary": summary,
        "filename": file.filename,
        "doc_id": doc_id
    }

@app.post("/query")
async def query_document(
    question: str = Form(...),
    doc_id: str = Form(...),
    categories: str = Form(""),
    llm_provider: str = Form(DEFAULT_LLM_PROVIDER),
    llm_model: Optional[str] = Form(None),
):
    if doc_id not in document_storage:
        return {"error": "Document not found"}

    selected = [x.strip() for x in categories.split(",") if x.strip()]
    categories_to_search = selected or _available_categories()
    rag_out = run_rag(
        question=question,
        categories_to_search=categories_to_search,
        top_k=DEFAULT_TOP_K,
        llm_provider=llm_provider,
        llm_model=llm_model,
    )
    return {
        "question": question,
        "answer": rag_out.get("answer", ""),
        "sources": rag_out.get("sources", []),
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "categories_to_search": categories_to_search,
    }

@app.get("/")
def root():
    return {"status": "Backend running!", "message": "Upload files to /upload or query at /query"}

# Run with: uvicorn server:app --reload --port 8000
