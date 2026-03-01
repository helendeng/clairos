"""Local domain router used by rag_demo4.

This keeps routing logic inside rag_demo4 while reusing ingestion taxonomy
and zero-shot classifier from the monorepo Ingestion package.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_root_on_path() -> None:
    # .../clairos/rag_demo4/src/get_domains_rag.py -> repo root is .../clairos
    repo_root = Path(__file__).resolve().parents[2]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


_ensure_repo_root_on_path()

from Ingestion.dataTaggers.ZeroShot import zero_shot_classify  # noqa: E402
from Ingestion.Schemas.taxonomy import (  # noqa: E402
    CATEGORY_THRESHOLDS,
    LABEL_TO_RAG_DOMAIN,
    ZERO_SHOT_LABEL_GROUPS,
)

_DEFAULT_THRESHOLD = 0.5


def get_domains_for_rag(query: str) -> list[str]:
    domains: set[str] = set()

    for labels_dict in ZERO_SHOT_LABEL_GROUPS.values():
        desc_to_key = {desc: key for key, desc in labels_dict.items()}
        candidate_labels = list(labels_dict.values())
        result = zero_shot_classify(query, candidate_labels, multi_label=True)

        for label_desc, score in zip(result["labels"], result["scores"]):
            category_key = desc_to_key.get(label_desc)
            if category_key is None:
                continue
            threshold = CATEGORY_THRESHOLDS.get(category_key, _DEFAULT_THRESHOLD)
            if score < threshold:
                continue
            domains.update(LABEL_TO_RAG_DOMAIN.get(category_key, []))

    return sorted(domains)
