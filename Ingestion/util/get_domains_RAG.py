"""
get_domains_RAG.py

Given a user query string, uses zero-shot NLI classification to determine
which RAG domain indexes to search. The same ZERO_SHOT_LABEL_GROUPS and
CATEGORY_THRESHOLDS used during document ingestion are reused here to
ensure consistent domain routing.
"""

from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
from Ingestion.Schemas.taxonomy import (
    ZERO_SHOT_LABEL_GROUPS,
    CATEGORY_THRESHOLDS,
    LABEL_TO_RAG_DOMAIN,
)

# Fallback confidence threshold for any category not listed in CATEGORY_THRESHOLDS.
# CATEGORY_THRESHOLDS is always the primary source; this only applies to labels
# that were not tuned (e.g. Personal_Life.*).
_DEFAULT_THRESHOLD = 0.5


def get_domains_for_rag(query: str) -> list[str]:
    """
    Classify a user query against the zero-shot label taxonomy and return
    the deduplicated list of RAG domain index names to search.

    Mirrors the ZeroShotController pattern: descriptions from
    ZERO_SHOT_LABEL_GROUPS are used as candidate_labels (multi_label=True),
    per-category thresholds from CATEGORY_THRESHOLDS are applied, and
    passing labels are resolved to RAG index names via LABEL_TO_RAG_DOMAIN.

    Thresholds come from CATEGORY_THRESHOLDS (the tuned values from taxonomy.py).
    _DEFAULT_THRESHOLD is only used as a fallback for labels that are not
    present in CATEGORY_THRESHOLDS.

    Parameters
    ----------
    query : The incoming user question/query string.

    Returns
    -------
    list[str] — sorted, deduplicated domain index names
                (e.g. ["accounting", "business_strategy"]) that correspond
                to files in rag_demo4/indexes/. Returns [] if no label
                clears its threshold.
    """
    domains: set[str] = set()

    for labels_dict in ZERO_SHOT_LABEL_GROUPS.values():
        # Pass descriptions as candidate_labels (same pattern as ZeroShotController).
        # Build a reverse map so we can recover the category key from the result.
        desc_to_key = {desc: key for key, desc in labels_dict.items()}
        candidate_labels = list(labels_dict.values())

        result = zero_shot_classify(query, candidate_labels, multi_label=True)

        for label_desc, score in zip(result["labels"], result["scores"]):
            category_key = desc_to_key.get(label_desc)
            if category_key is None:
                continue

            # Use the tuned threshold from CATEGORY_THRESHOLDS; fall back to
            # _DEFAULT_THRESHOLD only for labels not covered by that dict.
            threshold = CATEGORY_THRESHOLDS.get(category_key, _DEFAULT_THRESHOLD)
            if score < threshold:
                continue

            rag_domains = LABEL_TO_RAG_DOMAIN.get(category_key, [])
            domains.update(rag_domains)

    return sorted(domains)
