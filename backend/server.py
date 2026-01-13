from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
from typing import Optional

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
    
    # Generate summary using Ollama
    summary_prompt = f"""Summarize this document in 3-4 sentences. Focus on key findings and main topics.
    
Document:
{text[:2000]}  

Provide a brief executive summary."""
    
    summary = call_ollama(summary_prompt)
    
    return {
        "pii": pii_results,
        "summary": summary,
        "filename": file.filename,
        "doc_id": doc_id
    }

@app.post("/query")
async def query_document(question: str = Form(...), doc_id: str = Form(...)):
    if doc_id not in document_storage:
        return {"error": "Document not found"}
    
    full_text = document_storage[doc_id]
    
    query_prompt = f"""Based on the following document, answer this question: {question}

Full Document:
{full_text[:4000]}

Answer:"""
    
    answer = call_ollama(query_prompt)
    return {"question": question, "answer": answer}

@app.get("/")
def root():
    return {"status": "Backend running!", "message": "Upload files to /upload or query at /query"}

# Run with: uvicorn server:app --reload --port 8000