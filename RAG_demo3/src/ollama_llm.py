"""Minimal Ollama client (local) for generation.

Requires:
  ollama serve
  ollama pull qwen2.5:14b
"""

import requests


def generate(prompt: str, model: str = "qwen2.5:14b", timeout_s: int = 120) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(url, json=payload, timeout=timeout_s)
    r.raise_for_status()
    return r.json().get("response", "")
