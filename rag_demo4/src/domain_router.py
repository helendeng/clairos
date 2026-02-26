"""Domain routing bridge for RAG CLI.

Resolve domain routing locally first, then fallback to external Ingestion path.
"""

from __future__ import annotations

import importlib
import importlib.util
import os
from pathlib import Path
from typing import Callable


def _load_router_func() -> Callable[[str], list[str]]:
    # Preferred: local router shipped with rag_demo4.
    try:
        from .get_domains_rag import get_domains_for_rag as local_router

        if callable(local_router):
            return local_router
    except Exception:
        pass

    # Secondary: import by module path if Ingestion package is available.
    try:
        mod = importlib.import_module("Ingestion.util.get_domains_RAG")
        fn = getattr(mod, "get_domains_for_rag", None)
        if callable(fn):
            return fn
    except Exception:
        pass

    # Fallback: import directly from explicit file path.
    file_hint = os.getenv("GET_DOMAINS_RAG_PATH", "").strip()
    if file_hint:
        path = Path(file_hint).expanduser().resolve()
        if path.exists():
            spec = importlib.util.spec_from_file_location("external_get_domains_rag", str(path))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                fn = getattr(module, "get_domains_for_rag", None)
                if callable(fn):
                    return fn

    raise RuntimeError(
        "Cannot load domain router. Expected local src.get_domains_rag.get_domains_for_rag, "
        "or Ingestion.util.get_domains_RAG.get_domains_for_rag, "
        "or set env GET_DOMAINS_RAG_PATH to that file."
    )


def get_domains_to_search(query: str) -> list[str]:
    fn = _load_router_func()
    domains = fn(query)
    if not isinstance(domains, list):
        raise TypeError("get_domains_for_rag must return list[str].")
    return [str(d) for d in domains if str(d).strip()]
