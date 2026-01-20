# v2
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
from typing import Optional
import random

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

# Calculate confidence score based on response characteristics
def calculate_confidence(text, prompt_length):
    """
    Simple confidence scoring - your teammates can replace with real model
    """
    # Base confidence on response length and specificity
    base_confidence = 0.7
    
    # Longer, more detailed responses get higher confidence
    if len(text) > 200:
        base_confidence += 0.1
    
    # If response contains specific numbers/dates, increase confidence
    if re.search(r'\b\d{4}\b', text):  # Contains year
        base_confidence += 0.05
    if re.search(r'\b\d{1,2}/\d{1,2}\b', text):  # Contains date
        base_confidence += 0.05
    
    # If response says "I don't know", set low confidence
    if "don't have" in text.lower() or "verified context" in text.lower():
        base_confidence = 0.4 + random.uniform(0, 0.1)
    
    # Add small random variation
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

# TO HELEN: CUSTOMIZE THE GENERATION OF THE HANDOFF BRIEF HERE! 
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read file content
    content = await file.read()
    text = content.decode('utf-8', errors='ignore')
    
    # Store full document text with filename as ID
    doc_id = file.filename
    document_storage[doc_id] = text
    
    # Detect PII
    pii_results = detect_pii(text)
    
    # Generate handoff brief structure using Ollama
    brief_prompt = f"""Generate a professional employee handoff brief for an existing role based off of data from a transitioning employee. You are addressing the new employee, so stay neutral when talking about the role. Based on the following document, extract:

1. Role Overview (neutral, professional tone, 2-3 sentences about the job responsibilities)
2. Recurring Tasks (ongoing responsibilities with frequency)
3. Non-Recurring Tasks (upcoming deadlines and one-time projects)
4. Key Contacts (important people to know)

Document:
{text[:3000]}

Format your response clearly with these sections. 
Be specific and actionable. 
Do not include anything meta abut the prompt in your output, just labels, titles, or headings. 
Do not include any asterisks. 
"""
    
    brief_content = call_ollama(brief_prompt)
    confidence = calculate_confidence(brief_content, len(brief_prompt))
    
    # Store in approval system for manager review
    approval_storage["items"] = [
        {
            "id": "1",
            "type": "overview",
            "title": "Role Overview",
            "content": brief_content[:500],  # First part is usually overview
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
async def query_document(question: str = Form(...), doc_id: str = Form(...)):
    # Retrieve full document from storage
    if doc_id not in document_storage:
        return {
            "question": question,
            "answer": "Error: Document not found. Please upload the document again.",
            "confidence": 0.0,
            "sources": []
        }
    
    full_text = document_storage[doc_id]
    
    # Use full document for context
    query_prompt = f"""Based on the following document, answer this question: {question}

Full Document:
{full_text[:4000]}

Provide a clear, concise answer. If you cannot find the answer in the document, say "I don't have verified context for that specific question in the documentation."

Answer:"""
    
    answer = call_ollama(query_prompt)
    confidence = calculate_confidence(answer, len(query_prompt))
    
    # Determine sources
    sources = [{"type": "document", "name": doc_id}]
    if "don't have" in answer.lower():
        sources = [{"type": "system", "name": "System Prompt"}]
    
    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }

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