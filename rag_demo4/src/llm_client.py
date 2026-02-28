"""Unified LLM client: local Ollama + OpenAI-compatible API providers."""

import os
import time
from typing import Optional

import requests

DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek_api")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
DEFAULT_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://api.deepseek.com")
DEFAULT_API_MODEL = os.getenv("LLM_API_MODEL", "deepseek-chat")
DEFAULT_API_KEY = os.getenv("LLM_API_KEY", "sk-acb050a499c64547b5a5af2321aee72d")
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _generate_with_ollama(prompt: str, model: str, timeout_s: int) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload, timeout=timeout_s)
    if response.status_code >= 400:
        detail = response.text[:500]
        raise RuntimeError(f"Ollama request failed ({response.status_code}): {detail}")
    return response.json().get("response", "")


def _generate_with_openai_compatible_api(
    prompt: str,
    model: str,
    timeout_s: int,
    api_base_url: str,
    api_key: str,
) -> str:
    if not api_key:
        raise RuntimeError("LLM API key is empty. Set LLM_API_KEY or pass api_key explicitly.")

    url = f"{api_base_url.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    response = None
    last_error = None
    for attempt in range(5):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout_s)
            if response.status_code in RETRYABLE_STATUS_CODES:
                last_error = RuntimeError(
                    f"API returned retryable status {response.status_code}: {response.text[:200]}"
                )
                time.sleep(min(2**attempt, 8))
                continue
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            last_error = exc
            if attempt == 4:
                raise
            time.sleep(min(2**attempt, 8))
    if response is None:
        raise RuntimeError(f"API call failed after retries: {last_error}")

    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        return ""
    return choices[0].get("message", {}).get("content", "")


def generate(
    prompt: str,
    provider: str = DEFAULT_PROVIDER,
    model: Optional[str] = None,
    timeout_s: int = 120,
    api_base_url: str = DEFAULT_API_BASE_URL,
    api_key: str = DEFAULT_API_KEY,
) -> str:
    provider_name = (provider or DEFAULT_PROVIDER).strip().lower()

    if provider_name in {"ollama", "local", "local_ollama"}:
        chosen_model = model or DEFAULT_OLLAMA_MODEL
        return _generate_with_ollama(prompt=prompt, model=chosen_model, timeout_s=timeout_s)

    if provider_name in {"deepseek", "deepseek_api", "api", "openai_compatible"}:
        chosen_model = model or DEFAULT_API_MODEL
        return _generate_with_openai_compatible_api(
            prompt=prompt,
            model=chosen_model,
            timeout_s=timeout_s,
            api_base_url=api_base_url,
            api_key=api_key,
        )

    if provider_name in {"gemini", "google", "google_gemini", "gemini_api"}:
        chosen_model = model or os.getenv("GEMINI_API_MODEL", "gemini-2.0-flash")
        chosen_api_base_url = api_base_url or os.getenv(
            "GEMINI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai"
        )
        chosen_api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        return _generate_with_openai_compatible_api(
            prompt=prompt,
            model=chosen_model,
            timeout_s=timeout_s,
            api_base_url=chosen_api_base_url,
            api_key=chosen_api_key,
        )

    raise ValueError(
        f"Unsupported provider '{provider}'. Use one of: "
        "ollama/local/local_ollama/deepseek/deepseek_api/api/openai_compatible/gemini/google/google_gemini/gemini_api."
    )
