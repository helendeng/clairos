import re
import sys
import os

from Ingestion.Schemas.schemas import EmailRecord, OutputSchema, SourceInfo
from Ingestion.Schemas.taxonomy import TAXONOMY, ZERO_SHOT_LABEL_GROUPS, CATEGORY_THRESHOLDS


def process_email_with_zero_shot(
            email: EmailRecord,
            zero_shot_classify_fn,
            label_groups: dict = ZERO_SHOT_LABEL_GROUPS,
            threshold: float = 0.5,
            split_by: str = "sentence",
        ) -> list[dict]:
    """
    Classifies an EmailRecord with zero-shot and returns a list of OutputSchema objects.

    Runs a separate zero-shot classifier call per label group (from ZERO_SHOT_LABEL_GROUPS),
    then combines results. Each (chunk, tag) pair that clears the confidence threshold
    produces one OutputSchema. Per-category thresholds from CATEGORY_THRESHOLDS are used
    when available, falling back to the default threshold. Domain and subdomain are resolved
    from TAXONOMY using the category key.

    Parameters
    ----------
    email               : EmailRecord
    zero_shot_classify_fn : callable — the HuggingFace pipeline or equivalent
    label_groups        : dict mapping group_name -> {category_key: description}
                          (defaults to ZERO_SHOT_LABEL_GROUPS)
    threshold           : float, default confidence threshold (overridden per-category
                          by CATEGORY_THRESHOLDS where defined)
    split_by            : "sentence" | "paragraph"

    Returns
    -------
    list[OutputSchema]
    """
    full_text = email.body.strip()

    if split_by == "sentence":
        chunks = [n for c in re.split(r"[.!?]+", full_text) if (n := re.sub(r'\s+', ' ', c).strip()) and len(n) > 50]
    elif split_by == "paragraph":
        chunks = [n for p in full_text.split("\n\n") if (n := re.sub(r'\s+', ' ', p).strip())]
    else:
        raise ValueError(f"Invalid split_by: {split_by!r}. Use 'sentence' or 'paragraph'")

    if not chunks:
        return []

    # Build SourceInfo once — it's the same for every chunk of this email
    source = SourceInfo(
        email_id=email.email_id,
        sender=email.sender,
        subject=email.subject,
        cc=email.cc,
        bcc=email.bcc,
        timestamp=email.timestamp,
    )

    # Pre-build (desc_to_key, candidate_labels) once per group, reused across all chunks
    groups = []
    for labels_dict in label_groups.values():
        desc_to_key = {desc: key for key, desc in labels_dict.items()}
        candidate_labels = list(labels_dict.values())
        groups.append((desc_to_key, candidate_labels))

    outputs: list[OutputSchema] = []

    for chunk_id, chunk_text in enumerate(chunks):
        # Collect all qualifying (score, category_key) pairs across all label groups
        candidates: list[tuple[float, str]] = []

        for desc_to_key, candidate_labels in groups:
            result = zero_shot_classify_fn(chunk_text, candidate_labels, multi_label=True)

            for label_desc, score in zip(result["labels"], result["scores"]):
                category_key = desc_to_key.get(label_desc)
                if category_key is None:
                    continue

                category_threshold = CATEGORY_THRESHOLDS.get(category_key, threshold)
                if score < category_threshold:
                    continue

                if TAXONOMY.get(category_key) is not None:
                    candidates.append((score, category_key))

        if not candidates:
            continue

        # Emit one OutputSchema per chunk using the highest-scoring label
        best_score, best_key = max(candidates, key=lambda x: x[0])
        taxonomy_entry = TAXONOMY[best_key]
        outputs.append(
            OutputSchema(
                chunk_id=chunk_id,
                domain=taxonomy_entry["domain"],
                sub_domain=taxonomy_entry["subdomain"],
                text=chunk_text,
                source=source,
            )
        )

    return outputs
