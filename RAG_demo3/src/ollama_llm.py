"""Backward-compatible Ollama wrapper.

Prefer importing `generate` from `llm_client` for provider switching.
"""

from .llm_client import generate as _generate


def generate(prompt: str, model: str = "qwen2.5:14b", timeout_s: int = 120) -> str:
    return _generate(prompt=prompt, provider="ollama", model=model, timeout_s=timeout_s)
